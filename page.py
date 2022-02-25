import streamlit as st

from data import texts
from styles import room_description, room_objects, inventory, message
from utils import write_styled, room_listing, inventory_listing

from game import Game, __version__
from game.classes import InvalidCommand
from game.data import room_data, object_data

if not hasattr(st.session_state, 'game'):
    st.session_state.game = Game(room_data, object_data)
game = st.session_state.game


def restart():
    del st.session_state.game


def execute(*args, store_response=True):
    try:
        response = game.process_command(*args)
    except InvalidCommand:
        response = texts.invalid
    if store_response:
        st.session_state.response = response


st.set_page_config(
    page_title=texts.game_title,
    page_icon=texts.icon_char,
)

st.sidebar.title(texts.game_title)
st.sidebar.caption(texts.version_info.format(__version__))
st.sidebar.button(texts.restart, on_click=restart)

left_column, right_column = st.columns([2, 1])

with left_column:
    write_styled(game.current_room.description, style=room_description)

    if game.objects_in_room:
        write_styled(room_listing(game.objects_in_room), style=room_objects)

    if game.objects_in_inventory:
        write_styled(inventory_listing(game.objects_in_inventory), style=inventory)

with right_column:
    for command in game.current_room.exits:
        st.button(
            getattr(texts, 'go_' + command),
            on_click=execute,
            args=(command,),
            kwargs=dict(store_response=False),
        )
    examine = st.button(texts.examine) if game.visible_objects else None
    buttons = {
        command: st.button(getattr(texts, command))
        for command in ('take', 'open', 'use')
        if game.objects_with_action(command)
    }

if examine:
    write_styled(texts.examine_what, style=message)
    with st.columns([2, 1])[1]:
        for obj_key, obj in game.visible_objects.items():
            st.button(obj.name, on_click=execute, args=('examine', obj_key))
for command, button in buttons.items():
    if button:
        write_styled(getattr(texts, command + '_what'), style=message)
        _, right_column = st.columns([2, 1])
        with right_column:
            for obj_key, obj in game.objects_with_action(command).items():
                st.button(obj.name, on_click=execute, args=(command, obj_key))

try:
    write_styled(st.session_state.response, style=message)
    del st.session_state.response
except AttributeError:
    pass
