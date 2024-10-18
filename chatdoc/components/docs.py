import reflex as rx

from chatdoc.constants import UPLOAD_ID
from chatdoc.state import SsoState, State

from .common import content, header
from .navbar import navbar


def upload_form():
    return rx.vstack(
        rx.heading("Upload documents"),
        rx.form(
            rx.vstack(
                rx.upload(
                    rx.text(
                        "Drag and drop files here or click to select files",
                        weight="bold",
                    ),
                    rx.foreach(rx.selected_files(UPLOAD_ID), rx.text),
                    border="1px dotted rgb(107,99,246)",
                    id=UPLOAD_ID,
                    padding="3em",
                    width="40em",
                    accept={"application/pdf": [".pdf"]},
                    max_files=5,
                    max_size=10 * 1024 * 1024,
                ),
                rx.cond(
                    State.uploading,
                    rx.box(
                        rx.center("Your files are uploaded and processed..."),
                        rx.progress(value=State.progress, max=100),
                        padding="1em",
                        width="100%",
                    ),
                    rx.box(
                        rx.hstack(
                            rx.select(
                                SsoState.user_roles,
                                default_value="Privat",
                                on_change=State.set_upload_role,
                                disabled=State.uploading,
                            ),
                            rx.button(
                                "Upload",
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
    )


def list_docs() -> rx.Component:
    return rx.vstack(
        rx.heading("Documents"),
        rx.box(
            rx.vstack(
                rx.foreach(
                    State.documents,
                    lambda doc: rx.card(
                        rx.hstack(
                            rx.text(doc.name, weight="bold"),
                            rx.hstack(
                                rx.badge(
                                    doc.role,
                                    variant="soft",
                                    radius="full",
                                ),
                                rx.button(
                                    rx.icon(
                                        tag="trash",
                                        color=rx.color("mauve", 12),
                                    ),
                                    background_color=rx.color("mauve", 6),
                                    size="1",
                                    on_click=lambda: State.delete_document(doc.id),
                                ),
                            ),
                            width="100%",
                            justify="between",
                        ),
                        width="100%",
                    ),
                ),
                width="100%",
            ),
            width="100%",
        ),
        width="100%",
    )


def docs_view() -> rx.Component:
    return rx.vstack(
        navbar(),
        header(rx.heading("Docs")),
        content(upload_form(), rx.divider(margin_y="2em"), list_docs()),
        background_color=rx.color("mauve", 1),
        color=rx.color("mauve", 12),
        min_height="100vh",
        align_items="stretch",
        spacing="0",
    )
