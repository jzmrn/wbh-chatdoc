import reflex as rx

from .navbar import navbar


def content(blocks: list[rx.Component]) -> rx.Component:
    return rx.box(
        rx.flex(
            *blocks,
            direction="column",
            align="stretch",
            align_self="center",
            height="100%",
        ),
        flex="1",
    )


def page(content: list[rx.Component]) -> rx.Component:
    return rx.flex(
        navbar(),
        rx.flex(
            *content,
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
