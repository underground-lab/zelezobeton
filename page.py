import streamlit as st

from game import game
from game.data import texts
from game.styles import room_description, room_objects, inventory, message
from game.utils import write_styled, room_listing, inventory_listing


def show_response(response):
    if response is None:
        return

    response, *params = response
    if response == 'ok':
        write_styled(texts.ok, style=message)
    elif response == 'description':
        write_styled(params[0].description, style=message)


st.set_page_config(
    page_title=texts.game_title,
    page_icon=texts.icon_char,
)

left_column, right_column = st.columns([2, 1])

with left_column:
    write_styled(game.current_room.description, style=room_description)

    if game.current_room.objects:
        write_styled(room_listing(game.current_room), style=room_objects)

    if game.player.inventory:
        write_styled(inventory_listing(game.player), style=inventory)

visible_objects = game.current_room.objects + game.player.inventory

with right_column:
    for command in game.current_room.exits:
        st.button(
            getattr(texts, 'go_' + command),
            on_click=game.process_command,
            args=(command,)
        )
    examine = st.button(texts.examine, key='examine') if visible_objects else None
    take = st.button(texts.take, key='take') if game.current_room.objects else None

if take:
    write_styled(texts.take_what, style=message)
    with st.columns([2, 1])[1]:
        for obj in game.current_room.objects:
            st.button(obj.name, on_click=game.process_command, args=('take', obj))
elif examine:
    write_styled(texts.examine_what, style=message)
    with st.columns([2, 1])[1]:
        for obj in visible_objects:
            st.button(obj.name, on_click=game.process_command, args=('examine', obj))

show_response(game.get_response())
