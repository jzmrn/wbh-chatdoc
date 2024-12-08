import reflex as rx

from chatdoc.state import State


def login_view() -> rx.Component:
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
