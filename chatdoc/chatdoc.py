"""The main Chat app."""

import reflex as rx
from chatdoc.components import chat, navbar
from chatdoc.state import SsoState


@rx.page(route="/callback", on_load=SsoState.callback)
def callback() -> rx.Component:
    return rx.container()


@rx.page(route="/logout", on_load=SsoState.logout)
def logout() -> rx.Component:
    return rx.container("Logged out")


@rx.page(route="/home", on_load=SsoState.require_auth)
def home() -> rx.Component:
    return auth_view()


@rx.page(route="/login", on_load=SsoState.redirect_sso)
def login() -> rx.Component:
    return rx.container()


@rx.page(route="/")
def main() -> rx.Component:
    return rx.cond(SsoState.check_auth, auth_view(), unauth_view())


def auth_view() -> rx.Component:
    return rx.chakra.vstack(
        navbar(),
        chat.chat(),
        chat.action_bar(),
        background_color=rx.color("mauve", 1),
        color=rx.color("mauve", 12),
        min_height="100vh",
        align_items="stretch",
        spacing="0",
    )


def unauth_view() -> rx.Component:
    return rx.flex(
        rx.card(
            rx.vstack(
                rx.flex(
                    rx.heading(
                        "chatdoc",
                        size="4",
                        as_="h3",
                        text_align="left",
                        width="100%",
                    ),
                    rx.heading(
                        "Sign in to your account",
                        size="6",
                        as_="h2",
                        text_align="left",
                        width="100%",
                    ),
                    direction="column",
                    justify="start",
                    spacing="4",
                    width="100%",
                ),
                rx.button(
                    rx.icon(tag="log-in"),
                    rx.text("Sign in with Microsoft"),
                    variant="outline",
                    size="3",
                    width="100%",
                    on_click=SsoState.redirect_sso,
                ),
                spacing="6",
                width="100%",
            ),
            size="4",
            max_width="28em",
            width="100%",
        ),
        align="center",
        justify="center",
    )


app = rx.App(
    theme=rx.theme(
        appearance="dark",
        accent_color="violet",
    ),
)
