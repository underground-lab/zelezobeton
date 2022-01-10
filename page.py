import streamlit as st

from game import game
from game.data import texts
from game.styles import room_description, room_objects, inventory
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

with right_column:
    for command in game.current_room.exits:
        st.button(
            getattr(texts, 'go_' + command),
            on_click=game.process_command,
            args=(command,)
        )
