import os

from langchain.chains import (
    ConversationalRetrievalChain,
    create_history_aware_retriever,
    create_retrieval_chain,
)
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

from .db import DatabaseHandler


class Vector:
    _instance = None
    db: PineconeVectorStore

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Vector, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):  # Ensure __init__ runs only once
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
            self.db = PineconeVectorStore(index=index, embedding=embeddings)
            self.initialized = True

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


class Database:
    _instance = None
    db: DatabaseHandler

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):  # Ensure __init__ runs only once
            host = os.environ.get("POSTGRES_HOST", "localhost")
            port = os.environ.get("POSTGRES_PORT", "5432")
            user = os.environ.get("POSTGRES_USER", "postgres")
            password = os.environ.get("POSTGRES_PASSWORD", "")
            dbname = os.environ.get("POSTGRES_DB", "postgres")

            self.db = DatabaseHandler(dbname, user, password, host, port)
            self.initialized = True

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


class Chain:
    _instance = None
    chain: ConversationalRetrievalChain

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Chain, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
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
        self.chain = create_retrieval_chain(
            history_aware_retriever, question_answer_chain
        )
        self.initialized = True

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
