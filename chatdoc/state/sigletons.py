import os

import msal
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
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


class Sso:
    _instance = None
    app: msal.ClientApplication

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Sso, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):  # Ensure __init__ runs only once
            client_id: str = os.environ.get("AZURE_CLIENT_ID")
            client_secret: str = os.environ.get("AZURE_CLIENT_SECRET")
            tenant_id: str = os.environ.get("AZURE_TENANT_ID")

            authority = f"https://login.microsoftonline.com/{tenant_id}"
            cache = msal.TokenCache()

            if client_secret:
                self.app = msal.ConfidentialClientApplication(
                    client_id=client_id,
                    client_credential=client_secret,
                    authority=authority,
                    token_cache=cache,
                )
            else:
                self.app = msal.PublicClientApplication(
                    client_id=client_id,
                    authority=authority,
                    token_cache=cache,
                )

            self.initialized = True

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
