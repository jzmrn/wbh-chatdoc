import reflex as rx

from chatdoc.constants import UPLOAD_ID
from chatdoc.state import SsoState, State

from .common import content, header
from .navbar import navbar


def upload_form():
    return rx.vstack(
        rx.form(
            rx.upload(
                rx.text("Drag and drop files here or click to select files"),
                border="1px dotted rgb(107,99,246)",
                id=UPLOAD_ID,
                padding="5em",
                accept={
                    "application/pdf": [".pdf"],
                },
                max_files=5,
            ),
            rx.divider(),
            rx.heading("Selected files:"),
            rx.vstack(rx.foreach(rx.selected_files(UPLOAD_ID), rx.text)),
            rx.divider(),
            rx.progress(value=State.progress, max=100),
            rx.divider(),
            rx.hstack(
                rx.select(
                    SsoState.user_roles,
                    default_value=SsoState.preferred_username,
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
                    disabled=State.uploading,
                ),
            ),
            align_self="center",
        ),
    )


def docs_view() -> rx.Component:
    return rx.vstack(
        navbar(),
        header(rx.heading("Docs")),
        content(
            upload_form(),
        ),
        background_color=rx.color("mauve", 1),
        color=rx.color("mauve", 12),
        min_height="100vh",
        align_items="stretch",
        spacing="0",
    )
