import reflex as rx
from reflex.style import toggle_color_mode

from chatdoc.state import State


def navbar_link(text: str, url: str) -> rx.Component:
    return rx.link(rx.text(text, size="4", weight="medium"), href=url)


def navbar_icons_item(text: str, icon: str, url: str) -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.icon(icon),
            rx.text(text, size="4", weight="medium"),
        ),
        href=url,
    )


def navbar():
    return rx.box(
        rx.hstack(
            rx.hstack(
                rx.heading(State.strings["title"]),
                align_items="center",
                height="100%",
            ),
            rx.hstack(
                navbar_icons_item(
                    State.strings["menu.chat"], "messages-square", "/chat"
                ),
                navbar_icons_item(State.strings["menu.docs"], "file-text", "/docs"),
                spacing="5",
                align_items="center",
                height="100%",
            ),
            rx.hstack(
                rx.badge(
                    State.user_name,
                    variant="soft",
                ),
                rx.button(
                    rx.icon(
                        tag="sun-moon",
                        color=rx.color("mauve", 12),
                    ),
                    background_color=rx.color("mauve", 6),
                    on_click=toggle_color_mode,
                ),
                rx.button(
                    rx.icon(
                        tag="log-out",
                        color=rx.color("mauve", 12),
                    ),
                    on_click=State.logout,
                    background_color=rx.color("mauve", 6),
                ),
                align="center",
            ),
            justify_content="space-between",
            align="center",
            height="100%",
        ),
        align="center",
        backdrop_filter="auto",
        backdrop_blur="lg",
        padding="12px",
        border_bottom=f"1px solid {rx.color('mauve', 3)}",
        background_color=rx.color("mauve", 2),
        position="fixed",
        top="0",
        height="4em",
        z_index="100",
        width="100%",
    )
