"""The main Chat app."""

import reflex as rx

from chatdoc.components import chat_view, docs_view
from chatdoc.components.chat import actions, chat_header, messages, sidebar
from chatdoc.components.navbar import navbar
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


@rx.page(route="/test")
def test() -> rx.Component:
    return rx.flex(
        navbar(),
        rx.flex(
            rx.box(
                rx.flex(
                    rx.box(
                        rx.text("Test1"),
                    ),
                    rx.scroll_area(
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        rx.text("Test2"),
                        type="always",
                        scrollbars="vertical",
                        background_color="purple",
                        flex="20",
                    ),
                    # rx.box(
                    #     rx.text("Test2"),
                    #     flex="1",
                    # ),
                    # rx.box(
                    #     rx.text("Test3"),
                    # ),
                    direction="column",
                    align="stretch",
                    height="100%",
                ),
                background_color="red",
                width="100px",
            ),
            rx.box(
                rx.flex(
                    rx.box(
                        rx.text("Test1"),
                        background_color="purple",
                        width="100px",
                    ),
                    rx.flex(
                        rx.scroll_area(
                            rx.text("Test2"),
                            rx.text("Test2"),
                            rx.text("Test2"),
                            rx.text("Test2"),
                            rx.text("Test2"),
                            rx.text("Test2"),
                            rx.text("Test2", background_color="purple", flex="1"),
                            type="always",
                            justify="stretch",
                            scrollbars="vertical",
                            display="flex",
                            overflow="hidden",
                            width="",
                            style={},
                        ),
                        flex="1",
                        align="stretch",
                        direction="column",
                    ),
                    rx.box(
                        rx.text("Test3"),
                        width="100px",
                        background_color="purple",
                    ),
                    direction="column",
                    align="stretch",
                    height="100%",
                ),
                background_color="green",
                flex="1",
            ),
            align="stretch",
            direction="row",
            width="100%",
            flex="1",
            overflow="hidden",
        ),
        direction="column",
        align="stretch",
        background_color="yellow",
        height="100vh",
    )


@rx.page(route="/new")
def new() -> rx.Component:
    return page(
        sidebar=sidebar(), header=chat_header(), content=messages(), footer=actions()
    )


def page(
    sidebar: rx.Component | None = None,
    header: rx.Component | None = None,
    content: rx.Component | None = None,
    footer: rx.Component | None = None,
) -> rx.Component:
    return rx.flex(
        navbar(),
        rx.flex(
            sidebar,
            rx.box(
                rx.flex(
                    header,
                    content,
                    footer,
                    direction="column",
                    align="stretch",
                    align_self="center",
                    height="100%",
                ),
                flex="1",
            ),
            align="stretch",
            direction="row",
            width="100%",
            max_width="72em",
            align_self="center",
            flex="1",
            overflow="hidden",
        ),
        direction="column",
        align="stretch",
        height="100vh",
    )


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
        appearance="light",
        accent_color="violet",
    ),
)
