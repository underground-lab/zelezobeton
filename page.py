import streamlit as st

from data import texts
from styles import room_description, room_objects, inventory, message
from utils import write_styled, room_listing, inventory_listing

from game import game
from game.classes import Response


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

left_column, right_column = st.columns([2, 1])

objects_in_room = game.current_room.objects
visible_objects = objects_in_room + game.player.inventory
portable_objects = [obj for obj in objects_in_room if obj.portable]

with left_column:
    write_styled(game.current_room.description, style=room_description)

    if objects_in_room:
        write_styled(room_listing(game.current_room), style=room_objects)

    if game.player.inventory:
        write_styled(inventory_listing(game.player), style=inventory)

with right_column:
    for command in game.current_room.exits:
        st.button(
            getattr(texts, 'go_' + command),
            on_click=game.process_command,
            args=(command,)
        )
    examine = st.button(texts.examine, key='examine') if visible_objects else None
    take = st.button(texts.take, key='take') if portable_objects else None

if examine:
    write_styled(texts.examine_what, style=message)
    with st.columns([2, 1])[1]:
        for obj in visible_objects:
            st.button(obj.name, on_click=game.process_command, args=('examine', obj))
elif take:
    write_styled(texts.take_what, style=message)
    with st.columns([2, 1])[1]:
        for obj in portable_objects:
            st.button(obj.name, on_click=game.process_command, args=('take', obj))

show_response(game.get_response())
