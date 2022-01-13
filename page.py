import sys

import streamlit as st

from data import texts
from styles import room_description, room_objects, inventory, message
from utils import write_styled, room_listing, inventory_listing

from game import game, __version__
from game.classes import Response


def restart():
    """Force restart by simply removing `game` from imported modules."""
    del sys.modules['game']


def show_response(response):
    if response is None:
        return

    response_code, *params = response
    if response_code is Response.OK:
        write_styled(texts.ok, style=message)
    elif response_code is Response.DESCRIPTION:
        write_styled(params[0].description, style=message)


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

    if game.player.inventory:
        write_styled(inventory_listing(game.player.inventory), style=inventory)

with right_column:
    for command in game.current_room.exits:
        st.button(
            getattr(texts, 'go_' + command),
            on_click=game.process_command,
            args=(command,)
        )
    examine = st.button(texts.examine, key='examine') if game.visible_objects else None
    take = st.button(texts.take, key='take') if game.portable_objects else None

if examine:
    write_styled(texts.examine_what, style=message)
    with st.columns([2, 1])[1]:
        for obj in game.visible_objects:
            st.button(obj.name, on_click=game.process_command, args=('examine', obj))
elif take:
    write_styled(texts.take_what, style=message)
    with st.columns([2, 1])[1]:
        for obj in game.portable_objects:
            st.button(obj.name, on_click=game.process_command, args=('take', obj))

show_response(game.pop_response())
