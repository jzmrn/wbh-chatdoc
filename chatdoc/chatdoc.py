"""The main Chat app."""

import reflex as rx

from chatdoc.components import chat_view, docs_view
from chatdoc.constants import OPTION_ENGLISH, OPTION_GERMAN
from chatdoc.state import State


@rx.page(route="/callback", on_load=State.callback)
def callback() -> rx.Component:
    return rx.container()


@rx.page(route="/logout", on_load=State.logout)
def logout() -> rx.Component:
    return rx.container("Logged out")


@rx.page(route="/chat", on_load=State.require_auth)
def chat() -> rx.Component:
    return chat_view()


@rx.page(route="/docs", on_load=State.require_auth)
def docs() -> rx.Component:
    return docs_view()


@rx.page(route="/login", on_load=State.redirect_sso)
def login() -> rx.Component:
    return rx.container()


@rx.page(route="/")
def main() -> rx.Component:
    return rx.cond(State.check_auth, chat_view(), unauth_view())


def unauth_view() -> rx.Component:
    return rx.flex(
        rx.card(
            rx.vstack(
                rx.flex(
                    rx.heading(
                        State.strings["title"],
                        size="4",
                        as_="h3",
                        text_align="left",
                        width="100%",
                    ),
                    rx.heading(
                        State.strings["login.header"],
                        size="6",
                        as_="h2",
                        text_align="left",
                        width="100%",
                    ),
                    rx.text(State.strings["login.description"]),
                    rx.spacer(),
                    rx.select(
                        State.languages,
                        default_value=State.language,
                        on_change=State.select_language,
                    ),
                    rx.spacer(),
                    rx.button(
                        rx.icon(tag="log-in"),
                        rx.text("Sign in with Microsoft"),
                        variant="outline",
                        size="3",
                        on_click=State.redirect_sso,
                    ),
                    direction="column",
                    justify="start",
                    spacing="4",
                    width="100%",
                ),
                spacing="6",
                width="100%",
            ),
            size="4",
            max_width="28em",
            width="100%",
        ),
        on_mount=State.update_strings,
        height="100vh",
        align="center",
        justify="center",
    )


app = rx.App(
    theme=rx.theme(
        appearance="dark",
        accent_color="violet",
    ),
)
