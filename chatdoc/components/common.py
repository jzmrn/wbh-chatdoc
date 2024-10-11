import reflex as rx


def content(*items: rx.Component) -> rx.Component:
    return rx.vstack(
        *items,
        py="8",
        flex="1",
        width="100%",
        max_width="50em",
        padding_x="4px",
        align_self="center",
        overflow="hidden",
        padding_bottom="5em",
    )
