from pathlib import Path

import toml

from game.classes import Room, Object, Player, Game
from game.data import room_data, object_data, player_data

ROOT_DIR = Path(__file__).parent.parent
__version__ = toml.load(ROOT_DIR / 'pyproject.toml')['tool']['poetry']['version']

objects = {i: Object(**params) for i, params in object_data.items()}
rooms = {i: Room(**params) for i, params in room_data.items()}
player = Player(**player_data)

# replace integer ids with object references
for room in rooms.values():
    room.objects = [objects[n] for n in room.objects]
player.inventory = [objects[n] for n in player.inventory]

game = Game(rooms, objects, player)
