import streamlit as st

from data import texts


def listing(strings):
    if not strings:
        return
    if len(strings) == 1:
        return strings[0]
    return f'{", ".join(strings[:-1])} {texts.and_} {strings[-1]}'


def write_styled(text, style):
    st.write(f'<p style="{style}">{text}</p>', unsafe_allow_html=True)


def room_listing(objects):
    object_names = [obj.name for obj in objects.values()]
    return texts.you_see.format(listing(object_names))


def inventory_listing(objects):
    object_names = [obj.name for obj in objects.values()]
    return texts.you_have.format(listing(object_names))
