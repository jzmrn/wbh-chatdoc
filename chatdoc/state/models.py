from datetime import datetime

import reflex as rx


class Chunk(rx.Base):
    """A document with metadata."""

    id: str
    page_content: str
    metadata: dict[str, str]


class Document(rx.Base):
    """A document with metadata."""

    id: int | None
    name: str
    role: str
    timestamp: datetime = datetime.now()


class QA(rx.Base):
    """A question and answer pair."""

    question: str
    answer: str
    context: list[Chunk]
    timestamp: datetime = datetime.now()


class Chat(rx.Base):
    """A chat session."""

    id: int | None
    name: str
    userid: str
    messages: list[QA] = []
    timestamp: datetime = datetime.now()
