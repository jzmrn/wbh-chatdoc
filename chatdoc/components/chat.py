import reflex as rx
import reflex_chakra as rc

from chatdoc.components.common import content, header
from chatdoc.state import QA, Chunk, State
from chatdoc.state.models import Chat

from .loading import loading_icon
from .navbar import navbar

message_style = dict(
    display="inline-block",
    padding_x="1em",
    border_radius="8px",
    max_width=["30em", "30em", "40em", "40em", "40em", "40em"],
)


def sidebar_chat(chat: Chat) -> rx.Component:
    return rx.hstack(
        rx.button(
            chat.name,
            on_click=lambda: State.set_chat(chat.id),
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
            rx.heading(State.strings["chat.header"], color=rx.color("mauve", 11)),
            rx.divider(),
            rx.cond(
                State.creating_chat,
                rx.skeleton(sidebar_chat(Chat(name="...", userid="..."))),
            ),
            rx.foreach(State.chats, lambda chat: sidebar_chat(chat)),
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


def modal() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.button(rx.icon(tag="message-square-plus"))),
        rx.dialog.content(
            rx.hstack(
                rx.input(
                    placeholder="Type something...",
                    on_blur=State.set_new_chat_name,
                    width=["15em", "20em", "30em", "30em", "30em", "30em"],
                ),
                rx.dialog.close(
                    rx.button(
                        State.strings["chat.create"],
                        on_click=lambda: State.create_chat(State.preferred_username),
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
            rx.text(qa.timestamp, from_now=True),
            margin_top="1em",
            text_align="center",
        ),
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
    return rx.hstack(
        rx.hover_card.root(
            rx.hover_card.trigger(
                rx.link(
                    docx.metadata["source"],
                    color_scheme="blue",
                    underline="always",
                    on_click=lambda: State.download_file(
                        docx.metadata["document_id"], docx.metadata["source"]
                    ),
                ),
            ),
            rx.hover_card.content(rx.text(docx.page_content)),
        ),
    )


def chat() -> rx.Component:
    return content(
        rx.box(rx.foreach(State.current_chat.messages, message), width="100%"),
    )


def action_bar() -> rx.Component:
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
                            placeholder=State.strings["chat.input"],
                            id="question",
                            width=["10em", "15em", "25em", "35em", "40em", "40em"],
                        ),
                        rx.button(
                            rx.cond(
                                State.processing,
                                loading_icon(height="1em"),
                                rx.text(State.strings["chat.send"]),
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
                        State.current_chat.name,
                        modal(),
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
                margin_left="16em",
                margin_top="4em",
            ),
        ),
        background_color=rx.color("mauve", 1),
        color=rx.color("mauve", 12),
        align_items="stretch",
        spacing="0",
        on_mount=State.update_strings,
    )
