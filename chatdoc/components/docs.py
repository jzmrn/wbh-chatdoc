import os

import reflex as rx

from .common import content, header
from .navbar import navbar

UPLOAD_ID = "upload"


class UploadHandler(rx.State):
    uploading: bool = False
    progress: int = 0

    async def handle_upload(self, files: list[rx.UploadFile]):
        self.progress = 0

        # TODO: avoid collisions and delete temporary files
        folder = "tmp"
        if not os.path.exists(folder):
            os.makedirs(folder)

        for file in files:
            print(f"Processing {file.filename}")
            with open(f"./{folder}/{file.filename}", "wb") as f:
                f.write(await file.read())

    def handle_upload_progress(self, progress: dict):
        self.uploading = True
        self.progress = round(progress["progress"] * 100)
        if self.progress >= 100:
            self.uploading = False

    def cancel_upload(self):
        self.uploading = False
        return rx.cancel_upload(UPLOAD_ID)


def upload_form():
    return rx.vstack(
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
        rx.progress(value=UploadHandler.progress, max=100),
        rx.button(
            "Upload",
            on_click=UploadHandler.handle_upload(
                rx.upload_files(
                    upload_id=UPLOAD_ID,
                    on_upload_progress=UploadHandler.handle_upload_progress,
                ),
            ),
            disabled=UploadHandler.uploading,
        ),
        align_self="center",
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
