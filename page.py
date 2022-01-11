import streamlit as st

from game import game
from game.data import texts
from game.styles import room_description, room_objects, inventory, message
from game.utils import write_styled

st.set_page_config(
    page_title=texts.game_title,
    page_icon=texts.icon_char,
)

left_column, right_column = st.columns([2, 1])

with left_column:
    write_styled(game.current_room.description, style=room_description)

    if game.current_room.objects:
        write_styled(game.room_listing(), style=room_objects)

    if game.player.inventory:
        write_styled(game.inventory_listing(), style=inventory)

visible_objects = game.current_room.objects + game.player.inventory

with right_column:
    for command in game.current_room.exits:
        st.button(
            getattr(texts, 'go_' + command),
            on_click=game.process_command,
            args=(command,)
        )

    if visible_objects:
        st.button(texts.examine, key='examine')

    if game.current_room.objects:
        st.button(texts.take, key='take')

if getattr(st.session_state, 'take', None):
    write_styled(texts.take_what, style=message)
    for i in game.current_room.objects:
        st.button(
            game.objects[i].name,
            on_click=game.process_command,
            args=('take', i)
        )
elif getattr(st.session_state, 'examine', None):
    write_styled(texts.examine_what, style=message)
    for i in visible_objects:
        st.button(
            game.objects[i].name,
            on_click=game.process_command,
            args=('examine', i)
        )

message_text = game.get_response()
if message_text:
    write_styled(message_text, style=message)
