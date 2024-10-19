import os
from pathlib import Path

import psycopg2
import reflex as rx
from langchain.chains import (
    ConversationalRetrievalChain,
    create_history_aware_retriever,
    create_retrieval_chain,
)
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.schema.document import Document as DocEntry
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from psycopg2 import sql

from chatdoc.constants import UPLOAD_ID

from .auth import SsoState

if "PINECONE_API_KEY" not in os.environ:
    raise ValueError("PINECONE_API_KEY is not set.")

if "OPENAI_API_KEY" not in os.environ:
    raise ValueError("OPENAI_API_KEY is not set.")


class Chunk(rx.Base):
    """A document with metadata."""

    id: str
    page_content: str
    metadata: dict[str, str]


class Document(rx.Base):
    """A document with metadata."""

    id: str | None
    name: str
    role: str
    created_at: str | None


class DatabaseHandler:
    def __init__(self, dbname: str, user: str, password: str, host: str, port: str):
        self.conn = psycopg2.connect(
            dbname=dbname, user=user, password=password, host=host, port=port
        )
        self.ensure_table_exists()

    def ensure_table_exists(self):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS documents (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    role VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            self.conn.commit()

    def store_document(self, document: Document) -> int:
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO documents (name, role, created_at)
                VALUES (%s, %s, CURRENT_TIMESTAMP)
                RETURNING id
                """,
                (document.name, document.role),
            )
            document_id = cur.fetchone()[0]
            self.conn.commit()
            return document_id

    def get_documents_by_roles(self, roles: list[str]) -> list[Document]:
        with self.conn.cursor() as cur:
            query = sql.SQL(
                """
                SELECT id, name, role, created_at
                FROM documents
                WHERE role IN (%s)
                """
            )
            cur.execute(query, (roles))
            rows = cur.fetchall()
            return [
                Document(
                    id=row[0],
                    name=row[1],
                    role=row[2],
                    created_at=row[3].strftime("%d.%m.%y"),
                    # TODO: use datetime to support sorting and moment component
                    # created_at=datetime(*[int(x) for x in re.findall(r"\d+", row[3])]),
                )
                for row in rows
            ]

    def delete_document(self, document_id: int):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM documents
                WHERE id = {0}
                """.format(document_id),
            )
            self.conn.commit()

    def close(self):
        self.conn.close()


class QA(rx.Base):
    """A question and answer pair."""

    question: str
    answer: str
    context: list[Chunk]


DEFAULT_CHATS = {"Intros": []}


class State(rx.State):
    """The app state."""

    uploading: bool = False
    progress: int = 0

    upload_role: str = "user"

    # A dict from the chat name to the list of questions and answers.
    chats: dict[str, list[QA]] = DEFAULT_CHATS

    # The current chat name.
    current_chat = "Intros"

    # The name of the new chat.
    new_chat_name: str = ""

    # The current question.
    question: str

    # Whether we are processing the question.
    processing: bool = False

    #########
    # Chats #
    #########

    def create_chat(self):
        """Create a new chat."""
        # Add the new chat to the list of chats.
        self.current_chat = self.new_chat_name
        self.chats[self.new_chat_name] = []

    def delete_chat(self):
        """Delete the current chat."""
        del self.chats[self.current_chat]
        if len(self.chats) == 0:
            self.chats = DEFAULT_CHATS
        self.current_chat = list(self.chats.keys())[0]

    def set_chat(self, chat_name: str):
        """Set the name of the current chat.

        Args:
            chat_name: The name of the chat.
        """
        self.current_chat = chat_name

    @rx.var
    def chat_titles(self) -> list[str]:
        """Get the list of chat titles.

        Returns:
            The list of chat names.
        """
        return list(self.chats.keys())

    @rx.var
    def current_chat_messages(self):
        """Get the messages for the current chat."""
        return self.chats[self.current_chat]

    #######
    # LLM #
    #######

    @rx.var
    def vectordb(self) -> PineconeVectorStore:
        pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
        embeddings = OpenAIEmbeddings(api_key=os.environ["OPENAI_API_KEY"])

        index_name = "langchain-demo"
        if index_name not in pc.list_indexes().names():
            pc.create_index(
                name=index_name,
                metric="cosine",
                dimension=1536,
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )

        index = pc.Index(index_name)
        return PineconeVectorStore(index=index, embedding=embeddings)

    @rx.var
    def chain(self) -> ConversationalRetrievalChain:
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
            self.vectordb.as_retriever(
                search_kwargs={
                    "k": 2,
                    # "filter": {"role": "file"},
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
        return create_retrieval_chain(history_aware_retriever, question_answer_chain)

    def process_question(self, form_data: dict[str, str]):
        # Get the question from the form
        question = form_data["question"]

        # Check if the question is empty
        if question == "":
            return

        # Add the question to the list of questions.
        qa = QA(question=question, answer="", context=[])
        self.chats[self.current_chat].append(qa)

        # Clear the input and start the processing.
        self.processing = True
        yield

        # Build the messages.
        messages = []
        for qa in self.current_chat_messages:
            messages.append(("user", qa.question))
            messages.append(("ai", qa.answer))

        # Remove the last mock answer.
        messages = messages[:-1]

        for item in self.chain.stream({"input": question, "chat_history": messages}):
            answer = item.get("answer", "")
            self.chats[self.current_chat][-1].answer += answer
            # yield

            context = item.get("context")
            if not context:
                continue

            self.chats[self.current_chat][-1].context = [
                Chunk(id=d.id, page_content=d.page_content, metadata=d.metadata)
                for d in context
            ]
            #     yield

        # Toggle the processing flag.
        self.processing = False

    ##########
    # Upload #
    ##########

    @rx.var
    def db_client(self):
        host = os.environ.get("POSTGRES_HOST", "localhost")
        port = os.environ.get("POSTGRES_PORT", "5432")
        user = os.environ.get("POSTGRES_USER", "postgres")
        password = os.environ.get("POSTGRES_PASSWORD", "")
        dbname = os.environ.get("POSTGRES_DB", "postgres")
        return DatabaseHandler(dbname, user, password, host, port)

    @rx.var
    def documents(self) -> list[Document]:
        return self.db_client.get_documents_by_roles(["user"])

    @rx.var
    def documents_empty(self) -> bool:
        return len(self.documents) == 0

    def set_upload_role(self, data: str):
        self.upload_role = data

    def delete_document(self, document_id: int):
        self.db_client.delete_document(document_id)
        # TODO: Upgrade pinecone plan to support filtering for deletes
        # self.vectordb.delete(filter={"metadata.document_id": document_id})

    # Save the files, create chunks, and add them to the vector store
    async def handle_upload(self, files: list[rx.UploadFile]):
        self.uploading = True
        self.progress = 0

        role = (
            self.upload_role
            if self.upload_role != "Privat"
            else SsoState.preferred_username
        )

        folder = "tmp"
        if not os.path.exists(folder):
            os.makedirs(folder)

        self.progress = 10

        # TODO: avoid collisions and delete temporary files
        documents = []
        increment = 30 / len(files)
        for file in files:
            with open(f"./{folder}/{file.filename}", "wb") as f:
                content = await file.read()
                f.write(content)
                documents.append(Document(role=role, name=file.filename))

            self.progress += increment
            yield

        TMP_DIR = Path("./tmp")
        loader = DirectoryLoader(TMP_DIR.as_posix(), glob="**/*.pdf")
        self.progress = 50
        yield

        docentries = []
        docs = loader.load()
        increment = 30 / len(docs)

        for doc in docs:
            name = doc.metadata.get("source", "").split("/")[-1]
            document_id = self.db_client.store_document(Document(name=name, role=role))

            docentries.append(
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
        chunks = text_splitter.split_documents(docentries)
        self.progress = 80
        yield

        self.vectordb.add_documents(chunks)

        self.progress = 100
        self.uploading = False

    # Upload itself is only the first step of the process (20%)
    def handle_upload_progress(self, progress: dict):
        if self.progress < 100:
            self.progress = round(progress["progress"] * 20)

    def cancel_upload(self):
        self.uploading = False
        return rx.cancel_upload(UPLOAD_ID)
