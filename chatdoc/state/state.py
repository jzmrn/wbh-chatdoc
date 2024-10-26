import json
import os
import pathlib
from typing import Any, Dict

import msal
import reflex as rx
from langchain.schema.document import Document as DocEntry
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders.pdf import PyPDFLoader

from chatdoc.constants import LANGKEYS, OPTION_ENGLISH, OPTION_GERMAN, UPLOAD_ID

from .models import QA, Chat, Chunk, Document
from .sigletons import Chain, Database, Vector

if "PINECONE_API_KEY" not in os.environ:
    raise ValueError("PINECONE_API_KEY is not set.")

if "OPENAI_API_KEY" not in os.environ:
    raise ValueError("OPENAI_API_KEY is not set.")

ENV_VAR_CLIENT_ID = "AZURE_CLIENT_ID"
ENV_VAR_CLIENT_SECRET = "AZURE_CLIENT_SECRET"
ENV_VAR_TENANT_ID = "AZURE_TENANT_ID"

if not os.getenv(ENV_VAR_CLIENT_ID):
    raise Exception(f"Please set {ENV_VAR_CLIENT_ID} environment variable.")

if not os.getenv(ENV_VAR_CLIENT_SECRET):
    raise Exception(f"Please set {ENV_VAR_CLIENT_SECRET} environment variable.")

if not os.getenv(ENV_VAR_TENANT_ID):
    raise Exception(f"Please set {ENV_VAR_TENANT_ID} environment variable.")

client_id: str = os.environ.get(ENV_VAR_CLIENT_ID)
client_secret: str = os.environ.get(ENV_VAR_CLIENT_SECRET)
tenant_id: str = os.environ.get(ENV_VAR_TENANT_ID)

authority = f"https://login.microsoftonline.com/{tenant_id}"
login_redirect = "/chat"
cache = msal.TokenCache()

sso_app: msal.ClientApplication
if client_secret:
    sso_app = msal.ConfidentialClientApplication(
        client_id=client_id,
        client_credential=client_secret,
        authority=authority,
        token_cache=cache,
    )
else:
    sso_app = msal.PublicClientApplication(
        client_id=client_id,
        authority=authority,
        token_cache=cache,
    )


def key_recursion(t: dict[str, Any], prefix: str = "") -> dict[str, Any]:
    """
    Returns a 'flatten' dictionary
    :param t:
    :param prefix:
    :return:
    """
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

    creating_chat: bool = False
    uploading: bool = False
    progress: int = 0

    selected_chat: int | None = None

    upload_role: str | None = None

    # The name of the new chat.
    new_chat_name: str = ""

    cached_chats: dict[int, Chat] | None = None
    cached_documents: dict[int, Document] | None = None

    # The current question.
    question: str

    # Whether we are processing the question.
    processing: bool = False

    _access_token: str = ""
    _flow: dict
    _token: Dict[str, str] = {}

    #########
    # Login #
    #########

    def redirect_sso(self) -> rx.Component:
        self._flow = sso_app.initiate_auth_code_flow(
            scopes=[], redirect_uri=f"{self.router.page.host}/callback"
        )
        return rx.redirect(self._flow["auth_uri"])

    def require_auth(self):
        # TODO: validate token
        if not self._token:
            return self.redirect_sso()

    @rx.var(cache=True)
    def check_auth(self) -> bool:
        # TODO: validate token
        return True if self._token else False

    @rx.var(cache=True)
    def user_name(self) -> str:
        return self._token.get("name")

    @rx.var(cache=True)
    def preferred_username(self) -> str:
        return self._token.get("preferred_username")

    @rx.var(cache=True)
    def user_roles(self) -> list[str]:
        # TODO: do not hardcode but mock user roles
        return ["Privat", "Support", "chatdoc", "Public"]

    def logout(self):
        self._token = {}
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
            "client-secret": client_secret,
        }
        try:
            result = sso_app.acquire_token_by_auth_code_flow(
                self._flow, auth_response, scopes=[]
            )
        except Exception:
            return rx.toast("error something went wrong")

        self._access_token = result.get("access_token")
        self._token = result.get("id_token_claims")
        return rx.redirect(login_redirect)

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
            return Chat(name="General", userid="user", messages=[])

        if len(self.chats) == 0:
            chat = Chat(name="General", userid=self.preferred_username, messages=[])
            chat.id = Database.get_instance().db.store_chat(chat)
            self.cached_chats[chat.id] = chat
            self.selected_chat = chat.id

        if self.selected_chat is None or self.selected_chat not in self.cached_chats:
            self.selected_chat = self.chats[0].id

        return self.cached_chats[self.selected_chat]

    @rx.var(cache=True)
    def chats(self) -> list[Chat]:
        if self.preferred_username is None:
            return []

        if self.cached_chats is None:
            chats = Database.get_instance().db.get_chats_by_userid(
                self.preferred_username
            )
            self.cached_chats = {chat.id: chat for chat in chats}

        return list(self.cached_chats.values())

    def create_chat(self, userid: str):
        self.creating_chat = True
        yield

        chat = chat = Chat(
            name=self.new_chat_name,
            userid=f"{userid}",
            messages=[],
        )
        chat.id = Database.get_instance().db.store_chat(chat)

        self.creating_chat = False
        self.cached_chats[chat.id] = chat

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

    def process_question(self, form_data: dict[str, str]):
        # Get the question from the form
        question = form_data["question"]

        # Check if the question is empty
        if question == "":
            return

        # Add the question to the list of questions.
        qa = QA(question=question, answer="", context=[])
        self.current_chat.messages.append(qa)

        # Clear the input and start the processing.
        self.processing = True
        yield

        # Build the messages.
        messages = []
        for qa in self.current_chat.messages:
            messages.append(("user", qa.question))
            messages.append(("ai", qa.answer))

        # Remove the last mock answer.
        messages = messages[:-1]

        for item in Chain.get_instance().chain.stream(
            {"input": question, "chat_history": messages}
        ):
            answer = item.get("answer", "")
            self.cached_chats[self.selected_chat].messages[-1].answer += answer
            yield

            context = item.get("context")
            if not context:
                continue

            self.cached_chats[self.selected_chat].messages[-1].context = [
                Chunk(id=d.id, page_content=d.page_content, metadata=d.metadata)
                for d in context
            ]
            yield

        Database.get_instance().db.update_chat(self.cached_chats[self.selected_chat])
        self.processing = False

    ##########
    # Upload #
    ##########

    @rx.var(cache=True)
    def documents(self) -> list[Document]:
        if self.preferred_username is None:
            return {}

        if self.cached_documents is None:
            docs = Database.get_instance().db.get_documents_by_roles(
                [*self.user_roles, self.preferred_username]
            )
            self.cached_documents = {doc.id: doc for doc in docs}

        return list(self.cached_documents.values())

    @rx.var(cache=True)
    def documents_empty(self) -> bool:
        return len(self.documents) == 0

    def set_upload_role(self, data: str):
        self.upload_role = data

    def delete_document(self, document_id: int):
        Database.get_instance().db.delete_document(document_id)
        if document_id in self.cached_documents:
            del self.cached_documents[document_id]
        # TODO: Upgrade pinecone plan to support filtering for deletes
        # self._vectordb.delete(filter={"metadata.document_id": document_id})

    # Save the files, create chunks, and add them to the vector store
    async def handle_upload(self, files: list[rx.UploadFile]):
        self.uploading = True
        self.progress = 0
        role = self.upload_role if self.upload_role else self.preferred_username

        folder = "tmp"
        if not os.path.exists(folder):
            os.makedirs(folder)

        self.progress = 10
        yield

        increment = 70 / len(files)
        documents = []

        # TODO: avoid collisions and delete temporary files
        for file in files:
            name = file.filename
            path = f"./{folder}/{name}"

            with open(path, "wb") as f:
                content = await file.read()
                f.write(content)

                d = Document(name=name, role=role)
                document_id = Database.get_instance().db.store_document(d)
                d.id = document_id
                self.cached_documents[d.id] = d

                docs = PyPDFLoader(path).load()

                for doc in docs:
                    documents.append(
                        DocEntry(
                            page_content=doc.page_content,
                            metadata={
                                **doc.metadata,
                                "role": role,
                                "source": name,
                                "document_id": document_id,
                            },
                        )
                    )

            self.progress += increment
            yield

        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        chunks = text_splitter.split_documents(documents)
        self.progress = 80
        yield

        Vector.get_instance().db.add_documents(chunks)

        self.progress = 100
        self.uploading = False

    # Upload itself is only the first step of the process (20%)
    def handle_upload_progress(self, progress: dict):
        if self.progress < 100:
            self.progress = round(progress["progress"] * 20)

    def cancel_upload(self):
        self.uploading = False
        return rx.cancel_upload(UPLOAD_ID)


# dokument bei klick auf referenz öffnen

# session cookie?
# dokumente nach datum durchsuchen?

# sprechblasen (optional)
# message streaming (optional)
