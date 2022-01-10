from dataclasses import dataclass, field

from game.data import texts
from game.utils import listing


@dataclass
class Room:
    description: str
    exits: dict = field(default_factory=dict)
    objects: list = field(default_factory=list)


@dataclass
class Object:
    name: str
    description: str


@dataclass
class Player:
    location: int
    inventory: list = field(default_factory=list)


class Game:
    def __init__(self, rooms, objects, player):
        self.rooms = rooms
        self.objects = objects
        self.player = player
        self.response = None

    def process_command(self, command, *params):
        exits = self.current_room.exits
        if command in ('north', 'south', 'west', 'east', 'up', 'down'):
            if command in exits:
                self.player.location = exits[command]
        elif command == 'take':
            obj_id = params[0]
            self.current_room.objects.remove(obj_id)
            self.player.inventory.append(obj_id)
            self.response = texts.ok

    @property
    def current_room(self):
        return self.rooms[self.player.location]

    def room_listing(self):
        object_names = [
            self.objects[obj_id].name
            for obj_id in self.current_room.objects
        ]
        return f'{texts.you_see} {listing(object_names)}.'

    def inventory_listing(self):
        object_names = [
            self.objects[obj_id].name
            for obj_id in self.player.inventory
        ]
        return f'{texts.you_have} {listing(object_names)}.'

    def get_response(self):
        value = self.response
        self.response = None
        return value
