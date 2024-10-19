import reflex as rx
import reflex_chakra as rc

from chatdoc.components.common import content, header
from chatdoc.state import QA, Chunk, State

from .loading import loading_icon
from .navbar import navbar

message_style = dict(
    display="inline-block",
    padding_x="1em",
    border_radius="8px",
    max_width=["30em", "30em", "40em", "40em", "40em", "40em"],
)


def sidebar_chat(chat: str) -> rx.Component:
    return rx.hstack(
        rx.button(
            chat,
            on_click=lambda: State.set_chat(chat),
            width="100%",
            variant="surface",
            text_overflow="ellipsis",
            overflow="hidden",
            white_space="nowrap",
        ),
        width="100%",
    )


def sidebar() -> rx.Component:
    return rx.vstack(
        rx.vstack(
            rx.heading("Chats", color=rx.color("mauve", 11)),
            rx.divider(),
            rx.foreach(State.chat_titles, lambda chat: sidebar_chat(chat)),
            align_items="stretch",
            width="100%",
        ),
        spacing="5",
        position="fixed",
        margin_top="4em",
        padding_x="1em",
        padding_y="1.5em",
        bg=rx.color("accent", 3),
        align="start",
        height="100%",
        width="16em",
    )


def modal(trigger) -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(trigger),
        rx.dialog.content(
            rx.hstack(
                rx.input(
                    placeholder="Type something...",
                    on_blur=State.set_new_chat_name,
                    width=["15em", "20em", "30em", "30em", "30em", "30em"],
                ),
                rx.dialog.close(
                    rx.button(
                        "Create chat",
                        on_click=State.create_chat,
                    ),
                ),
                background_color=rx.color("mauve", 1),
                spacing="2",
                width="100%",
            ),
        ),
    )


def message(qa: QA) -> rx.Component:
    return rx.box(
        rx.box(
            rx.markdown(
                qa.question,
                background_color=rx.color("mauve", 4),
                color=rx.color("mauve", 12),
                **message_style,
            ),
            margin_top="1em",
            text_align="right",
        ),
        rx.box(
            rx.vstack(
                rx.cond(
                    qa.answer == "",
                    rx.image(
                        src="https://media.tenor.com/NqKNFHSmbssAAAAi/discord-loading-dots-discord-loading.gif",
                        width="2em",
                        margin="1em",
                    ),
                    rx.vstack(
                        rx.markdown(qa.answer),
                        rx.foreach(qa.context, display_ref),
                        padding_bottom="1em",
                    ),
                ),
            ),
            background_color=rx.color("accent", 4),
            color=rx.color("accent", 12),
            text_align="left",
            margin_top="1em",
            **message_style,
        ),
        width="100%",
    )


def display_ref(docx: Chunk) -> rx.Component:
    return rx.hover_card.root(
        rx.hover_card.trigger(
            rx.link(
                docx.metadata["source"],
                color_scheme="blue",
                underline="always",
            ),
        ),
        rx.hover_card.content(rx.text(docx.page_content)),
    )


def chat() -> rx.Component:
    """List all the messages in a single conversation."""
    return content(
        rx.box(rx.foreach(State.chats[State.current_chat], message), width="100%"),
    )


def action_bar() -> rx.Component:
    """The action bar to send a new message."""
    return rx.center(
        rx.vstack(
            rx.form(
                rc.form_control(
                    rx.hstack(
                        rx.input(
                            rx.input.slot(
                                rx.tooltip(
                                    rx.icon("info", size=18),
                                    content="Enter a question to get a response.",
                                )
                            ),
                            placeholder="Type something...",
                            id="question",
                            width=["15em", "20em", "45em", "50em", "50em", "50em"],
                        ),
                        rx.button(
                            rx.cond(
                                State.processing,
                                loading_icon(height="1em"),
                                rx.text("Send"),
                            ),
                            type="submit",
                        ),
                        align_items="center",
                    ),
                    is_disabled=State.processing,
                ),
                on_submit=State.process_question,
                reset_on_submit=True,
            ),
            align_items="center",
        ),
        position="fixed",
        padding_right="16em",
        bottom="0",
        padding_y="16px",
        backdrop_filter="auto",
        backdrop_blur="lg",
        border_top=f"1px solid {rx.color('mauve', 3)}",
        background_color=rx.color("mauve", 2),
        width="100%",
    )


def chat_view() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.hstack(
            sidebar(),
            rx.box(
                rx.vstack(
                    header(
                        State.current_chat,
                        modal(rx.button("+ New chat")),
                        rx.button(
                            rx.icon(
                                tag="trash",
                                on_click=State.delete_chat,
                                color=rx.color("mauve", 12),
                            ),
                            background_color=rx.color("mauve", 6),
                        ),
                    ),
                    chat(),
                    action_bar(),
                ),
                flex="1",
                padding_left="16em",
                padding_top="4em",
            ),
        ),
        background_color=rx.color("mauve", 1),
        color=rx.color("mauve", 12),
        align_items="stretch",
        spacing="0",
    )
