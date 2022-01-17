from copy import deepcopy

from pathlib import Path

import toml

from game.classes import Room, Object, Game
from game.data import room_data, object_data

ROOT_DIR = Path(__file__).parent.parent
__version__ = toml.load(ROOT_DIR / 'pyproject.toml')['tool']['poetry']['version']


def new_game():
    room_data_copy = deepcopy(room_data)
    object_data_copy = deepcopy(object_data)

    rooms = {i: Room(**params) for i, params in room_data_copy.items()}
    objects = {i: Object(**params) for i, params in object_data_copy.items()}

    # replace integer ids with object references
    for room in rooms.values():
        room.exits = {key: rooms[room_id] for key, room_id in room.exits.items()}
    for obj in objects.values():
        if obj.location is not None:
            obj.location = rooms[obj.location]

    return Game(rooms, objects)


game = new_game()
