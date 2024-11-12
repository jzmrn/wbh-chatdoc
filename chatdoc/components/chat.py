from datetime import datetime

import reflex as rx
import reflex_chakra as rc

from chatdoc.state import QA, Chunk, State
from chatdoc.state.models import Chat

from ..constants import DATE_TIME
from .common import content, page

message_style = dict(
    display="inline-block",
    padding_x="1em",
    border_radius="8px",
    max_width=["30em", "30em", "40em", "40em", "40em", "40em"],
)


def sidebar_chat(chat: Chat) -> rx.Component:
    return rx.button(
        chat.name,
        on_click=lambda: State.set_chat(chat.id),
        width="100%",
        variant="surface",
        text_overflow="ellipsis",
        overflow="hidden",
        white_space="nowrap",
    )


def sidebar() -> rx.Component:
    return rx.card(
        rx.flex(
            rx.heading(State.strings["chat.header"], padding_bottom="2em"),
            rx.divider(),
            rx.scroll_area(
                rx.flex(
                    rx.foreach(
                        State.chats.keys(),
                        lambda chat: rx.box(
                            rx.flex(
                                rx.heading(
                                    rx.cond(
                                        chat == datetime.now().strftime("%d.%m.%Y"),
                                        State.strings["chat.today"],
                                        chat,
                                    ),
                                    size="2",
                                    color=rx.color("mauve", 12),
                                    position="sticky",
                                ),
                                rx.foreach(State.chats[chat], sidebar_chat),
                                spacing="2",
                                direction="column",
                            ),
                            width="100%",
                        ),
                    ),
                    direction="column",
                    align="stretch",
                    spacing="6",
                    width="14em",
                    padding="0.5em",
                ),
                type="always",
                scrollbars="vertical",
                flex="1",
            ),
            direction="column",
            align="stretch",
            height="100%",
        ),
        bg=rx.color("accent", 3),
        width="16em",
        padding="0.5em",
        margin="1em",
    )


def modal() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.button(rx.icon(tag="message-square-plus"))),
        rx.dialog.content(
            rx.dialog.title(State.strings["chat.title"]),
            rx.flex(
                rx.input(
                    placeholder=State.strings["chat.placeholder"],
                    on_blur=State.set_new_chat_name,
                ),
                rx.dialog.close(
                    rx.flex(
                        rx.button(
                            State.strings["chat.create"],
                            on_click=State.create_chat,
                        ),
                        justify="end",
                    )
                ),
                direction="column",
                spacing="4",
            ),
        ),
    )


def message(qa: QA) -> rx.Component:
    return rx.box(
        rx.box(
            rx.moment(qa.timestamp, format=DATE_TIME),
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
                    rx.cond(
                        State.processing & qa == State.current_chat.messages[-1],
                        rx.image(
                            src="https://media.tenor.com/NqKNFHSmbssAAAAi/discord-loading-dots-discord-loading.gif",
                            width="2em",
                            margin="1em",
                        ),
                        rx.markdown(State.strings["chat.empty"]),
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
            id=rx.cond(qa == State.current_chat.messages[-1], "latest", "any"),
        ),
        width="46em",
    )


def display_ref(chunk: Chunk) -> rx.Component:
    m = chunk.metadata
    return rx.hstack(
        rx.hover_card.root(
            rx.hover_card.trigger(
                rx.link(
                    rx.cond(
                        m.contains("page_id"),
                        f"{m["source"]} ({State.strings["chat.page"]}: {m['page_id']})",
                        m["source"],
                    ),
                    color_scheme="blue",
                    underline="always",
                    on_click=lambda: State.download_file(m["document_id"], m["source"]),
                ),
            ),
            rx.hover_card.content(rx.text(chunk.page_content)),
        ),
    )


def messages() -> rx.Component:
    return rx.card(
        rx.center(
            rx.flex(
                rx.scroll_area(
                    rx.center(
                        rx.foreach(State.current_chat.messages, message),
                        direction="column",
                        align_self="center",
                    ),
                    type="always",
                    scrollbars="vertical",
                ),
                width="48em",
                height="100%",
            ),
            overflow="hidden",
            height="100%",
        ),
        width="50em",
        flex="1",
        margin="1em",
        padding="0.5em",
    )


def actions() -> rx.Component:
    return rx.card(
        rx.form(
            rc.form_control(
                rx.flex(
                    rx.input(
                        rx.input.slot(
                            rx.tooltip(
                                rx.icon("info", size=18),
                                content=State.strings["chat.info"],
                            )
                        ),
                        max_length=1000,
                        placeholder=State.strings["chat.input"],
                        id="question",
                        flex="1",
                    ),
                    rx.button(
                        rx.cond(
                            State.processing,
                            rx.spinner(),
                            rx.text(State.strings["chat.send"]),
                        ),
                        type="submit",
                    ),
                    direction="row",
                    align="stretch",
                    align_items="center",
                    spacing="2",
                ),
                is_disabled=State.processing,
            ),
            on_submit=State.process_question,
            reset_on_submit=True,
            width="100%",
        ),
        backdrop_filter="auto",
        width="50em",
        backdrop_blur="lg",
        background_color=rx.color("mauve", 2),
        padding="0.5em",
        margin="1em",
    )


def header():
    return rx.card(
        rx.hstack(
            rx.heading(
                State.current_chat.name,
                text_overflow="ellipsis",
                overflow="hidden",
                white_space="nowrap",
                max_width="70%",
            ),
            rx.hstack(
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
            justify_content="space-between",
        ),
        margin="1em",
        padding="1em",
        width="50em",
    )


def chat_view():
    return page([sidebar(), content([header(), messages(), actions()])])
