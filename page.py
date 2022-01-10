import streamlit as st

from game import game
from game.data import texts

st.set_page_config(
    page_title=texts.game_title,
    page_icon=texts.icon_char,
)

left_column, right_column = st.columns([2, 1])

with left_column:
    st.write(game.current_room.description)

with right_column:
    for command in game.current_room.exits:
        st.button(
            getattr(texts, 'go_' + command),
            on_click=game.process_command,
            args=(command,)
        )
