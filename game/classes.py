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

    def process_command(self, command):
        exits = self.current_room.exits
        if command in ('north', 'south', 'west', 'east'):
            if command in exits:
                self.player.location = exits[command]

    @property
    def current_room(self):
        return self.rooms[self.player.location]

    def room_listing(self):
        object_names = [
            self.objects[obj_id].name
            for obj_id in self.current_room.objects
        ]
        return f'{texts.you_see} {listing(object_names)}.'
