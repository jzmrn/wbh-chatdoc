import reflex as rx

from chatdoc.components import chat_view, docs_view, login_view
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
    return rx.cond(State.check_auth, chat_view(), login_view())


app = rx.App(
    theme=rx.theme(
        appearance="light",
        accent_color="violet",
    ),
)
