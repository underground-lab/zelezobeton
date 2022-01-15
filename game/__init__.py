from copy import deepcopy

from pathlib import Path

import toml

from game.classes import Room, Object, Player, Game
from game.data import room_data, object_data, player_data

ROOT_DIR = Path(__file__).parent.parent
__version__ = toml.load(ROOT_DIR / 'pyproject.toml')['tool']['poetry']['version']

room_data = deepcopy(room_data)
object_data = deepcopy(object_data)
player_data = deepcopy(player_data)

objects = {i: Object(**params) for i, params in object_data.items()}
rooms = {i: Room(**params) for i, params in room_data.items()}
player = Player(**player_data)

# replace integer ids with object references
for room in rooms.values():
    room.objects = [objects[n] for n in room.objects]
    room.exits = {key: rooms[room_id] for key, room_id in room.exits.items()}

player.location = rooms[player.location]
player.inventory = [objects[n] for n in player.inventory]

for obj in objects.values():
    for action in obj.actions.values():
        for impact_spec in action['impact']:
            _, kwargs = impact_spec
            if 'room' in kwargs:
                kwargs['room'] = rooms[kwargs['room']]
            if 'destination' in kwargs:
                kwargs['destination'] = rooms[kwargs['destination']]
            if 'obj' in kwargs:
                kwargs['obj'] = objects[kwargs['obj']]

game = Game(rooms, objects, player)
