import reflex as rx

from chatdoc.state import SsoState, State


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
                rx.heading("chatdoc."),
                align_items="center",
                height="100%",
            ),
            rx.hstack(
                navbar_icons_item("Chat", "messages-square", "/chat"),
                navbar_icons_item("Docs", "file-text", "/docs"),
                spacing="5",
                align_items="center",
                height="100%",
            ),
            rx.hstack(
                rx.badge(
                    SsoState.user_name,
                    variant="soft",
                ),
                rx.button(
                    rx.icon(
                        tag="log-out",
                        color=rx.color("mauve", 12),
                    ),
                    on_click=SsoState.logout,
                    background_color=rx.color("mauve", 6),
                ),
                align_items="center",
            ),
            justify_content="space-between",
            align_items="center",
        ),
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
        align_items="center",
    )
