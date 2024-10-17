import reflex as rx


def content(*items: rx.Component) -> rx.Component:
    return rx.vstack(
        *items,
        py="8",
        flex="1",
        width="100%",
        max_width="50em",
        padding_x="4px",
        padding_top="10em",
        align_self="center",
        overflow="hidden",
        padding_bottom="5em",
    )


def header(title: str, *items: rx.Component) -> rx.Component:
    return rx.box(
        rx.card(
            rx.hstack(
                rx.heading(
                    title,
                    text_overflow="ellipsis",
                    overflow="hidden",
                    white_space="nowrap",
                    max_width="70%",
                ),
                rx.hstack(*items),
                justify_content="space-between",
            ),
        ),
        position="fixed",
        top="5em",
        width="100%",
        max_width="50em",
        align_self="center",
        overflow="hidden",
    )
