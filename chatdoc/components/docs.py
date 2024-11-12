from datetime import datetime

import reflex as rx

from chatdoc.state import State
from chatdoc.state.models import Document

from ..constants import DATE, UPLOAD_ID
from .common import content, header
from .navbar import navbar


def upload_form():
    return rx.card(
        rx.heading(State.strings["docs.subheader"]),
        rx.form(
            rx.vstack(
                rx.cond(
                    State.uploading,
                    rx.box(
                        rx.center(State.strings["docs.processing"]),
                        rx.center(rx.spinner()),
                        padding="1em",
                        width="100%",
                    ),
                    rx.box(
                        rx.upload(
                            rx.text(
                                State.strings["docs.description"],
                                weight="bold",
                            ),
                            rx.foreach(rx.selected_files(UPLOAD_ID), rx.text),
                            border="0",
                            id=UPLOAD_ID,
                            padding="3em",
                            width="100%",
                            accept={
                                "application/pdf": [".pdf"],
                                "application/msword": [".docx", ".doc"],
                            },
                            max_files=5,
                            max_size=10 * 1024 * 1024,
                        ),
                        rx.hstack(
                            rx.select(
                                State.user_roles,
                                default_value="Privat",
                                on_change=lambda role: rx.cond(
                                    role == "Privat",
                                    State.set_upload_role(State.preferred_username),
                                    State.set_upload_role(role),
                                ),
                                disabled=State.uploading,
                            ),
                            rx.button(
                                State.strings["docs.upload"],
                                on_click=State.handle_upload(
                                    rx.upload_files(
                                        upload_id=UPLOAD_ID,
                                        on_upload_progress=State.handle_upload_progress,
                                    ),
                                ),
                            ),
                            float="right",
                        ),
                        width="100%",
                    ),
                ),
            ),
        ),
        align_self="center",
        width="50em",
    )


def modal(id: any, name: any) -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon(
                    tag="trash",
                    size=16,
                    color=rx.color("mauve", 12),
                ),
                background_color=rx.color("mauve", 6),
                size="1",
            )
        ),
        rx.dialog.content(
            rx.dialog.title(State.strings["docs.confirm"]),
            rx.flex(
                rx.center(name, font_style="oblique"),
                rx.dialog.close(
                    rx.flex(
                        rx.button(
                            State.strings["docs.delete"],
                            background_color="red",
                            on_click=lambda: State.delete_document(id),
                        ),
                        justify="end",
                    )
                ),
                direction="column",
                spacing="4",
            ),
        ),
    )


def doc(doc: Document) -> rx.Component:
    return rx.card(
        rx.hstack(
            rx.text(
                doc.name,
                weight="bold",
                ellipsis=True,
                overflow="hidden",
                white_space="nowrap",
            ),
            rx.hstack(
                rx.badge(rx.moment(doc.timestamp, format=DATE)),
                rx.badge(
                    doc.role,
                    variant="soft",
                    radius="full",
                ),
                rx.button(
                    rx.icon(
                        tag="download",
                        size=16,
                        color=rx.color("mauve", 12),
                    ),
                    background_color=rx.color("mauve", 6),
                    size="1",
                    on_click=lambda: State.download_file(
                        doc.id,
                        doc.name,
                    ),
                ),
                modal(doc.id, doc.name),
            ),
            width="100%",
            justify="between",
        ),
        width="48em",
    )


def docs_list() -> rx.Component:
    return rx.card(
        rx.center(
            rx.flex(
                rx.hstack(
                    rx.heading(State.strings["docs.title"]),
                    rx.button(
                        rx.icon(tag="refresh-cw", size=16),
                        on_click=State.refresh_docs,
                    ),
                    justify_content="space-between",
                    margin_bottom="1em",
                ),
                rx.cond(
                    State.documents_empty,
                    rx.box(
                        rx.center(State.strings["docs.empty"]),
                        rx.center(
                            State.strings["docs.roles"] + State.user_roles.join(", "),
                        ),
                        margin_y="2em",
                        height="100%",
                    ),
                    rx.scroll_area(
                        rx.center(
                            rx.foreach(State.documents, doc),
                            direction="column",
                            align_self="center",
                            spacing="2",
                        ),
                        type="always",
                        scrollbars="vertical",
                        flex="1",
                    ),
                ),
                width="100%",
                height="100%",
                direction="column",
            ),
            overflow="hidden",
            height="100%",
        ),
        flex="1",
        margin="1em",
        padding="0.5em",
        width="50em",
        align_self="center",
    )


def list_docs() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.heading(State.strings["docs.title"]),
            rx.button(
                rx.icon(
                    tag="refresh-cw",
                    size=16,
                ),
                on_click=State.refresh_docs,
            ),
            justify_content="space-between",
            margin_bottom="1em",
        ),
        rx.cond(
            State.documents_empty,
            rx.box(
                rx.center(State.strings["docs.empty"]),
                rx.center(
                    State.strings["docs.roles"] + State.user_roles.join(", "),
                ),
                margin_y="2em",
            ),
            rx.box(
                rx.scroll_area(
                    rx.foreach(
                        # State.documents,
                        [
                            Document(
                                id=1,
                                name="test",
                                role="test",
                                timestamp=datetime.now(),
                            ),
                            Document(
                                id=1,
                                name="test",
                                role="test",
                                timestamp=datetime.now(),
                            ),
                            Document(
                                id=1,
                                name="test",
                                role="test",
                                timestamp=datetime.now(),
                            ),
                            Document(
                                id=1,
                                name="test",
                                role="test",
                                timestamp=datetime.now(),
                            ),
                            Document(
                                id=1,
                                name="test",
                                role="test",
                                timestamp=datetime.now(),
                            ),
                            Document(
                                id=1,
                                name="test",
                                role="test",
                                timestamp=datetime.now(),
                            ),
                            Document(
                                id=1,
                                name="test",
                                role="test",
                                timestamp=datetime.now(),
                            ),
                            Document(
                                id=1,
                                name="test",
                                role="test",
                                timestamp=datetime.now(),
                            ),
                            Document(
                                id=1,
                                name="test",
                                role="test",
                                timestamp=datetime.now(),
                            ),
                            Document(
                                id=1,
                                name="test",
                                role="test",
                                timestamp=datetime.now(),
                            ),
                        ],
                        lambda doc: rx.card(
                            rx.hstack(
                                rx.text(
                                    doc.name,
                                    weight="bold",
                                    ellipsis=True,
                                    overflow="hidden",
                                    white_space="nowrap",
                                ),
                                rx.hstack(
                                    rx.badge(rx.moment(doc.timestamp, format=DATE)),
                                    rx.badge(
                                        doc.role,
                                        variant="soft",
                                        radius="full",
                                    ),
                                    rx.button(
                                        rx.icon(
                                            tag="download",
                                            size=16,
                                            color=rx.color("mauve", 12),
                                        ),
                                        background_color=rx.color("mauve", 6),
                                        size="1",
                                        on_click=lambda: State.download_file(
                                            doc.id,
                                            doc.name,
                                        ),
                                    ),
                                    modal(doc.id, doc.name),
                                ),
                                width="100%",
                                justify="between",
                            ),
                            width="100%",
                        ),
                    ),
                    width="100%",
                    type="always",
                ),
                width="100%",
                height="100%",
                overflow="hidden",
            ),
        ),
        width="100%",
        max_width="64em",
    )


def docs_view() -> rx.Component:
    return rx.vstack(
        navbar(),
        header(rx.heading(State.strings["docs.header"])),
        content(upload_form(), rx.divider(margin_y="2em"), list_docs()),
        background_color=rx.color("mauve", 1),
        color=rx.color("mauve", 12),
        min_height="100vh",
        align_items="stretch",
        spacing="0",
        on_mount=State.update_strings,
    )


def docs_header():
    return header(rx.heading(State.strings["docs.header"]))
