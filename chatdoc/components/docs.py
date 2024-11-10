import reflex as rx

from chatdoc.state import State

from ..constants import DATE, UPLOAD_ID
from .common import content, header
from .navbar import navbar


def upload_form():
    return rx.vstack(
        rx.heading(State.strings["docs.subheader"]),
        rx.form(
            rx.vstack(
                rx.upload(
                    rx.text(
                        State.strings["docs.description"],
                        weight="bold",
                    ),
                    rx.foreach(rx.selected_files(UPLOAD_ID), rx.text),
                    border="1px dotted rgb(107,99,246)",
                    id=UPLOAD_ID,
                    padding="3em",
                    width="40em",
                    accept={
                        "application/pdf": [".pdf"],
                        "application/msword": [".docx", ".doc"],
                    },
                    max_files=5,
                    max_size=10 * 1024 * 1024,
                ),
                rx.cond(
                    State.uploading,
                    rx.box(
                        rx.center(State.strings["docs.processing"]),
                        rx.progress(value=State.progress, max=100),
                        padding="1em",
                        width="100%",
                    ),
                    rx.box(
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


def list_docs() -> rx.Component:
    return rx.vstack(
        rx.box(
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
                rx.vstack(
                    rx.foreach(
                        State.documents,
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
                ),
            ),
            width="100%",
        ),
        width="100%",
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
