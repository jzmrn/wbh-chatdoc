import json
import os
import pathlib
from datetime import datetime
from typing import Any, Dict

import reflex as rx
from langchain.chains import (
    create_history_aware_retriever,
    create_retrieval_chain,
)
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.schema.document import Document as DocEntry
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import (
    PyPDFLoader,
    UnstructuredWordDocumentLoader,
)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

from chatdoc.constants import LANGKEYS, OPTION_ENGLISH, OPTION_GERMAN, UPLOAD_ID

from .models import QA, Chat, Chunk, Document
from .sigletons import Database, Sso, Vector


def key_recursion(t: dict[str, Any], prefix: str = "") -> dict[str, Any]:
    ret = {}
    for k, v in t.items():
        if len(prefix) > 0:
            k = prefix + "." + k

        if isinstance(v, dict):
            ret.update(key_recursion(v, k))
        else:
            ret[k] = v
    return ret


class State(rx.State):
    """The app state."""

    language: str = OPTION_GERMAN
    path: str = "assets/locales"
    strings: dict[str, str] = key_recursion(
        json.loads(
            (
                pathlib.Path(path) / LANGKEYS[OPTION_GERMAN] / "translation.json"
            ).read_text(encoding="utf-8")
        )
    )
    languages: list[str] = [OPTION_GERMAN, OPTION_ENGLISH]
    filter: str | None = None

    uploading: bool = False
    selected_chat: int | None = None
    upload_role: str | None = None
    new_chat_name: str = ""

    cached_chats: dict[int, Chat] | None = None
    cached_documents: dict[int, Document] | None = None

    processing: bool = False

    access_token: str = ""
    flow: dict
    token: Dict[str, str] = {}

    #########
    # Login #
    #########

    def redirect_sso(self) -> rx.Component:
        self.flow = Sso.get_instance().app.initiate_auth_code_flow(
            scopes=[],
            redirect_uri=f"{self.router.page.host}/callback",
        )
        return rx.redirect(self.flow["auth_uri"])

    def require_auth(self):
        # TODO: validate token
        if not self.token:
            return self.redirect_sso()

    @rx.var(cache=True)
    def check_auth(self) -> bool:
        # TODO: validate token
        return True if self.token else False

    @rx.var(cache=True)
    def user_name(self) -> str:
        # TODO: handle none
        return self.token.get("name")

    @rx.var(cache=True)
    def preferred_username(self) -> str:
        # TODO: handle none
        return self.token.get("preferred_username")

    @rx.var(cache=True)
    def user_roles(self) -> list[str]:
        # TODO: do not hardcode user roles
        match self.user_name:
            case "Jan Zimmermann":
                return ["Support", "chatdoc"]
            case "Max Krischker":
                return ["Management", "chatdoc"]
            case "Daniel Keiss":
                return ["Management", "Support"]
            case _:
                return ["Public"]

    @rx.var(cache=True)
    def user_roles_ui(self) -> list[str]:
        return [self.strings["docs.private"], *self.user_roles]

    @rx.var(cache=True)
    def user_roles_backend(self) -> list[str]:
        return [self.preferred_username, *self.user_roles]

    def logout(self):
        self.token = {}
        # This will logout the user from the SSO provider
        # return rx.redirect(authority + "/oauth2/v2.0/logout")
        return rx.redirect(self.router.page.host)

    def callback(self):
        query_components = self.router.page.params

        auth_response = {
            "code": query_components.get("code"),
            "client_info": query_components.get("client_info"),
            "state": query_components.get("state"),
            "session_state": query_components.get("session_state"),
            "client-secret": os.environ.get("AZURE_CLIENT_SECRET"),
        }

        try:
            result = Sso.get_instance().app.acquire_token_by_auth_code_flow(
                self.flow, auth_response, scopes=[]
            )

            access_token = result.get("access_token")
            token = result.get("id_token_claims")

            if not token or not access_token:
                return rx.redirect("/login")

            self.token = token
            self.access_token = access_token
            return rx.redirect("/chat")

        except Exception as e:
            print(e)
            yield rx.toast("error something went wrong")
            return rx.redirect("/login")

    ############
    # Language #
    ############

    def select_language(self, lng: str):
        if lng in self.languages:
            self.language = lng
            self.update_strings()

    def update_strings(self):
        if self.language not in LANGKEYS:
            return

        self.strings = key_recursion(
            json.loads(
                (
                    pathlib.Path(self.path)
                    / LANGKEYS[self.language]
                    / "translation.json"
                ).read_text(encoding="utf-8")
            )
        )

    #########
    # Chats #
    #########

    @rx.var(cache=True)
    def current_chat(self) -> Chat:
        if self.preferred_username is None:
            return Chat(
                name="General", userid="user", messages=[], timestamp=datetime.now()
            )

        self._ensure_chats()
        if self.selected_chat is None or self.selected_chat not in self.cached_chats:
            self.selected_chat = list(self.cached_chats.values())[-1].id

        return self.cached_chats[self.selected_chat]

    @rx.var(cache=True)
    def empty_messages(self) -> bool:
        return len(self.current_chat.messages) == 0

    def _ensure_chats(self):
        if not self.cached_chats:
            chats = Database.get_instance().db.get_chats_by_userid(
                self.preferred_username
            )
            self.cached_chats = {chat.id: chat for chat in chats}

        if len(self.cached_chats.keys()) == 0:
            chat = Chat(
                name="General",
                userid=self.preferred_username,
                messages=[],
                timestamp=datetime.now(),
            )
            chat.id = Database.get_instance().db.store_chat(chat)
            self.cached_chats[chat.id] = chat
            self.selected_chat = chat.id

    @rx.var(cache=True)
    def chats(self) -> dict[str, list[Chat]]:
        if self.preferred_username is None:
            return {}

        self._ensure_chats()
        sorted_chats = sorted(
            self.cached_chats.values(),
            key=self._chat_timestamp,
            reverse=True,
        )

        chats = {}
        for chat in sorted_chats:
            key = self._chat_timestamp(chat).strftime("%d.%m.%Y")
            if key not in chats:
                chats[key] = []
            chats[key].append(chat)

        return chats

    def _chat_timestamp(self, chat: Chat):
        return (
            chat.timestamp if len(chat.messages) == 0 else chat.messages[-1].timestamp
        )

    def create_chat(self):
        if self.new_chat_name == "":
            return rx.toast.error(self.strings["chat.error"], position="bottom-center")

        if len(self.cached_chats.keys()) > 99:
            categories = self.chats.keys()
            if len(categories) > 0:
                category = categories[-1]
                chat = self.chats[category][0]

                Database.get_instance().db.delete_chat(chat.id)
                del self.cached_chats[chat.id]

        chat = chat = Chat(
            name=self.new_chat_name,
            userid=f"{self.preferred_username}",
            messages=[],
            timestamp=datetime.now(),
        )
        chat.id = Database.get_instance().db.store_chat(chat)

        self.cached_chats[chat.id] = chat
        self.selected_chat = chat.id

    def delete_chat(self):
        id = self.current_chat.id
        if id and self.selected_chat and self.selected_chat == id:
            Database.get_instance().db.delete_chat(id)
            del self.cached_chats[self.selected_chat]

    def set_chat(self, chatid: int):
        self.selected_chat = chatid

    def add_message(self, message: QA):
        self.current_chat.messages.append(message)

    #######
    # LLM #
    #######

    def process_question(self, form_data: dict[str, Any]):
        try:
            # Get the question from the form
            question = form_data.get("question", "")

            # Input validation
            if not isinstance(question, str) or question == "":
                return

            # Clear the input and start the processing.
            self.processing = True
            yield

            # Add the question to the list of questions.
            qa = QA(question=question, answer="", context=[], timestamp=datetime.now())
            self.current_chat.messages.append(qa)
            yield rx.scroll_to("latest")

            # Build the messages.
            messages = []
            for qa in self.current_chat.messages:
                messages.append(("user", qa.question))
                messages.append(("ai", qa.answer))

            # Remove the last mock answer.
            messages = messages[:-1]

            llm = ChatOpenAI(
                model_name="gpt-3.5-turbo",
                temperature=0,
                api_key=os.environ["OPENAI_API_KEY"],
            )

            # Contextualize question
            contextualize_q_system_prompt = (
                "Given a chat history and the latest user question "
                "which might reference context in the chat history, "
                "formulate a standalone question which can be understood "
                "without the chat history. Do NOT answer the question, just "
                "reformulate it if needed and otherwise return it as is."
            )
            contextualize_q_prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", contextualize_q_system_prompt),
                    MessagesPlaceholder("chat_history"),
                    ("human", "{input}"),
                ]
            )

            history_aware_retriever = create_history_aware_retriever(
                llm,
                Vector.get_instance().db.as_retriever(
                    search_kwargs={
                        "k": 2,
                        "filter": {"role": {"$in": self.user_roles_backend}},
                    },
                ),
                contextualize_q_prompt,
            )

            # Answer question
            qa_system_prompt = (
                "You are an assistant called chatdoc for question-answering tasks."
                "Use the following pieces of retrieved context to answer the "
                "question. If you don't know the answer, just say that you "
                "don't know. Use three sentences maximum and keep the answer "
                "concise."
                "Context: {context}"
            )
            qa_prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", qa_system_prompt),
                    MessagesPlaceholder("chat_history"),
                    ("human", "{input}"),
                ]
            )

            # Below we use create_stuff_documents_chain to feed all retrieved context
            # into the LLM. Note that we can also use StuffDocumentsChain and other
            # instances of BaseCombineDocumentsChain.
            question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
            chain = create_retrieval_chain(
                history_aware_retriever, question_answer_chain
            )

            for item in chain.stream({"input": question, "chat_history": messages}):
                answer = item.get("answer", "")
                self.cached_chats[self.selected_chat].messages[-1].answer += answer
                yield

                context = item.get("context")
                if not context:
                    continue

                chunks = [
                    Chunk(
                        id=d.id,
                        page_content=d.page_content,
                        metadata={
                            **d.metadata,
                            **(
                                {"page": int(m.get("page", 0)) + 1}
                                if "page" in m
                                else {}
                            ),
                        }
                        if isinstance(m := d.metadata, dict)
                        else {},
                    )
                    for d in context
                ]

                current_context = {
                    (c.metadata.get("source"), c.metadata.get("page")): c
                    for c in self.cached_chats[self.selected_chat].messages[-1].context
                }

                for chunk in chunks:
                    key = (chunk.metadata.get("source"), chunk.metadata.get("page"))
                    if key not in current_context:
                        current_context[key] = chunk

                self.cached_chats[self.selected_chat].messages[-1].context = list(
                    current_context.values()
                )
                yield

            Database.get_instance().db.update_chat(
                self.cached_chats[self.selected_chat]
            )

        except Exception as e:
            print(e)

        finally:
            self.processing = False

        return rx.scroll_to("latest")

    ##########
    # Upload #
    ##########

    @rx.var(cache=True)
    def filters(self) -> list[str]:
        return [self.strings["docs.all"], *self.user_roles_ui]

    def set_filter(self, role: str):
        self.filter = role

    @rx.var(cache=True)
    def filtered_documents(self) -> list[Document]:
        if self.preferred_username is None:
            return []

        self._ensure_docs()
        if not self.filter or self.filter == self.strings["docs.all"]:
            return list(self.cached_documents.values())

        role = (
            self.preferred_username
            if self.filter == self.strings["docs.private"]
            else self.filter
        )
        return [doc for doc in self.cached_documents.values() if doc.role == role]

    def refresh_docs(self):
        docs = Database.get_instance().db.get_documents_by_roles(
            [*self.user_roles, self.preferred_username]
        )
        self.cached_documents = {doc.id: doc for doc in docs}

    @rx.var(cache=True)
    def documents(self) -> list[Document]:
        if self.preferred_username is None:
            return []

        self._ensure_docs()
        return list(self.cached_documents.values())

    def _ensure_docs(self):
        if self.cached_documents is None:
            self.refresh_docs()

    @rx.var(cache=True)
    def documents_empty(self) -> bool:
        return len(self.filtered_documents) == 0

    @rx.var(cache=True)
    def documents_count(self):
        return len(self.filtered_documents)

    def set_upload_role(self, data: str):
        self.upload_role = data

    def delete_document(self, document_id: int):
        Database.get_instance().db.delete_document(document_id)
        if document_id in self.cached_documents:
            del self.cached_documents[document_id]
        # TODO: Upgrade pinecone plan to support filtering for deletes
        # self._vectordb.delete(filter={"metadata.document_id": document_id})

    def process_docs(self, role: str, files: list[rx.UploadFile]):
        docs = []
        documents = []

        for file in files:
            name = file.filename.split("/")[-1]
            extension = name.split(".")[-1]

            doc = Document(name=name, role=role, timestamp=datetime.now())
            document_id = Database.get_instance().db.store_document(doc)
            doc.id = document_id
            docs.append(doc)

            dir = os.getenv("STORAGE_MOUNT")
            path = f"{dir}/{document_id}"
            with open(path, "wb") as f:
                content = file.file.read()
                f.write(content)

            match extension:
                case "pdf":
                    loader = PyPDFLoader(path)
                case "docx" | "doc":
                    loader = UnstructuredWordDocumentLoader(path, mode="elements")
                case _:
                    raise ValueError("Unsupported file format")

            for chunk in loader.load():
                page = chunk.metadata.get("page_number") or int(
                    chunk.metadata.get("page", 0) + 1
                )
                documents.append(
                    DocEntry(
                        page_content=chunk.page_content,
                        metadata={
                            **chunk.metadata,
                            **({"page_id": page} if page else {}),
                            "role": role,
                            "source": name,
                            "document_id": document_id,
                        },
                    )
                )

        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        chunks = text_splitter.split_documents(documents)

        Vector.get_instance().db.add_documents(chunks)

        return docs

    @rx.var
    def now(self) -> str:
        return datetime.now().strftime("%d.%m.%Y")

    @rx.event
    def handle_upload(self, files: list[rx.UploadFile]):
        role = self.upload_role if self.upload_role else self.preferred_username
        role = role if role != self.strings["docs.private"] else self.preferred_username

        try:
            docs = self.process_docs(role, files)
            for doc in docs:
                self.cached_documents[doc.id] = doc

        except Exception as e:
            print(e)
            yield rx.toast.error(self.strings["error.upload"], position="bottom-center")

        finally:
            self.uploading = False

    @rx.event
    def set_uploading(self, value: bool):
        self.uploading = value

    @rx.event
    def download_file(self, fid: int, filename: str):
        try:
            dir = os.getenv("STORAGE_MOUNT")
            path = f"{dir}/{int(float(fid))}"
            with open(path, "rb") as f:
                data = f.read()
            return rx.download(data=data, filename=filename)

        except Exception as e:
            print(e)
            return rx.toast.error(
                self.strings["error.download"], position="bottom-center"
            )
