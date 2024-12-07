import reflex as rx

from chatdoc.state import State
from chatdoc.state.models import Document

from ..constants import DATE, UPLOAD_ID
from .common import content, page


def upload_form():
    return rx.card(
        rx.heading(State.strings["docs.subheader"]),
        rx.form(
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
                            default_value=State.strings["docs.private"],
                            on_change=State.set_upload_role,
                        ),
                        rx.button(
                            State.strings["docs.upload"],
                            type="submit",
                            on_click=State.handle_upload(
                                rx.upload_files(upload_id=UPLOAD_ID),
                            ),
                        ),
                        float="right",
                    ),
                    width="100%",
                ),
            ),
            on_submit=lambda: State.set_uploading(True),
        ),
        align_self="center",
        width="50em",
        margin_top="1em",
        margin_bottom="0.5em",
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
                rx.center(name, font_style="oblique", height="6em"),
                rx.dialog.close(
                    rx.flex(
                        rx.button(
                            State.strings["menu.cancel"],
                            background_color="gray",
                        ),
                        rx.button(
                            State.strings["docs.delete"],
                            background_color="red",
                            on_click=lambda: State.delete_document(id),
                        ),
                        spacing="2",
                        justify="end",
                    ),
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
                    rx.heading(
                        f"{State.strings["docs.title"]} ({State.documents_count})"
                    ),
                    rx.hstack(
                        rx.select(
                            State.filters,
                            default_value=State.strings["docs.all"],
                            on_change=State.set_filter,
                        ),
                        rx.button(
                            rx.icon(tag="refresh-cw", size=16),
                            on_click=State.refresh_docs,
                        ),
                    ),
                    justify_content="space-between",
                    margin_bottom="1em",
                ),
                rx.cond(
                    State.documents_empty,
                    rx.center(
                        rx.center(State.strings["docs.empty"]),
                        rx.center(
                            State.strings["docs.roles"] + State.user_roles.join(", "),
                        ),
                        direction="column",
                        margin_y="2em",
                        height="100%",
                    ),
                    rx.scroll_area(
                        rx.center(
                            rx.foreach(State.filtered_documents, doc),
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
        margin_bottom="1em",
        margin_top="0.5em",
        padding="0.5em",
        width="50em",
        align_self="center",
    )


def docs_view() -> rx.Component:
    return page([content([upload_form(), docs_list()])])
