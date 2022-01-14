from dataclasses import dataclass, field
from enum import Enum

Response = Enum('Response', 'OK DESCRIPTION')


@dataclass
class Room:
    description: str
    exits: dict = field(default_factory=dict)
    objects: list = field(default_factory=list)


@dataclass
class Object:
    name: str
    description: str
    portable: bool = True
    actions: dict = field(default_factory=dict)


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
        elif command == 'examine':
            obj = params[0]
            self.response = (Response.DESCRIPTION, obj)
        elif command == 'take':
            obj = params[0]
            self.current_room.objects.remove(obj)
            self.player.inventory.append(obj)
            self.response = (Response.OK,)

    @property
    def current_room(self):
        return self.rooms[self.player.location]

    @property
    def objects_in_room(self):
        return self.current_room.objects

    @property
    def visible_objects(self):
        return self.objects_in_room + self.player.inventory

    @property
    def portable_objects(self):
        return [obj for obj in self.objects_in_room if obj.portable]

    def objects_with_action(self, action):
        return [
            obj for obj in self.visible_objects
            if action in obj.actions and obj.actions[action].get('enabled', True)
        ]

    def pop_response(self):
        value = self.response
        self.response = None
        return value
