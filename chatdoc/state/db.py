import datetime
import json
from json import JSONEncoder

import psycopg2
import reflex as rx
from psycopg2 import sql

from .models import QA, Chat, Chunk, Document


class ChatEncoder(JSONEncoder):
    def default(self, value):
        if isinstance(value, datetime.datetime):
            return value.timestamp()
        if isinstance(value, list):
            return [self.default(v) for v in value]
        if isinstance(value, dict):
            return dict(value)
        else:
            return value.__dict__


class ListOfListsEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, list):
            return obj
        return json.JSONEncoder.default(self, obj)


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
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS chats (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    userid VARCHAR(255) NOT NULL,
                    messages JSON,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
            placeholders = sql.SQL(", ").join(sql.Placeholder() * len(roles))
            query = sql.SQL(
                """
                SELECT id, name, role, timestamp
                FROM documents
                WHERE role IN ({values})
                """
            ).format(values=placeholders)
            cur.execute(query, roles)
            rows = cur.fetchall()
            return [
                Document(
                    id=row[0],
                    name=row[1],
                    role=row[2],
                    timestamp=row[3],
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

    def store_chat(self, chat: Chat) -> int:
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO chats (name, userid, messages, timestamp)
                VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
                RETURNING id
                """,
                (chat.name, chat.userid, json.dumps(chat.messages)),
            )
            chat_id = cur.fetchone()[0]
            self.conn.commit()
            return chat_id

    def update_chat(self, chat: Chat):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                UPDATE chats
                SET name = %s, userid = %s, messages = %s, timestamp = CURRENT_TIMESTAMP
                WHERE id = %s
                """,
                (
                    chat.name,
                    chat.userid,
                    json.dumps(chat.messages, cls=ChatEncoder),
                    chat.id,
                ),
            )
            self.conn.commit()

    def delete_chat(self, chatid: int):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM chats
                WHERE id = %s
                """,
                (chatid,),
            )
            self.conn.commit()

    def get_chats_by_userid(self, userid: str) -> list[Chat]:
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, name, userid, messages, timestamp
                FROM chats
                WHERE userid = %s
                """,
                (userid,),
            )
            rows = cur.fetchall()

            return [
                Chat(
                    id=row[0],
                    name=row[1],
                    userid=row[2],
                    messages=[
                        QA(
                            question=m["question"],
                            answer=m["answer"],
                            context=[
                                Chunk(
                                    id=c["id"],
                                    page_content=c["page_content"],
                                    metadata=c["metadata"],
                                )
                                for c in m["context"]
                            ],
                            timestamp=datetime.datetime.fromtimestamp(m["timestamp"]),
                        )
                        for m in row[3]
                    ],
                    timestamp=row[4],
                )
                for row in rows
            ]

    def close(self):
        self.conn.close()
