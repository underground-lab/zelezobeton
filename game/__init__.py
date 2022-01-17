from copy import deepcopy

from pathlib import Path

import toml

from game.classes import Room, Object, Player, Game
from game.data import room_data, object_data, player_data

ROOT_DIR = Path(__file__).parent.parent
__version__ = toml.load(ROOT_DIR / 'pyproject.toml')['tool']['poetry']['version']


def new_game():
    room_data_copy = deepcopy(room_data)
    object_data_copy = deepcopy(object_data)
    player_data_copy = deepcopy(player_data)

    rooms = {i: Room(**params) for i, params in room_data_copy.items()}
    objects = {i: Object(**params) for i, params in object_data_copy.items()}
    player = Player(**player_data_copy)

    # replace integer ids with object references
    for room in rooms.values():
        room.objects = [objects[n] for n in room.objects]
        room.exits = {key: rooms[room_id] for key, room_id in room.exits.items()}

    player.location = rooms[player.location]
    player.inventory = [objects[n] for n in player.inventory]

    return Game(rooms, objects, player)


game = new_game()
