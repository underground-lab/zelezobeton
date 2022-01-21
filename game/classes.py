from dataclasses import dataclass, field
from typing import Optional

from game import callbacks


class InvalidCommand(ValueError):
    ...


@dataclass
class Room:
    description: Optional[str] = None
    exits: dict = field(default_factory=dict)


@dataclass
class Object:
    name: str
    description: str
    location: Optional[Room] = None
    actions: dict = field(default_factory=dict)


@dataclass
class Action:
    condition: list = field(default_factory=list)
    impact: list = field(default_factory=list)
    message: Optional[str] = None
    enabled: bool = True


class Game:
    message_ok = 'OK'

    def __init__(self, room_data, object_data, start_location_id='start'):
        self.rooms = {key: Room(**params) for key, params in room_data.items()}
        self.objects = {key: Object(**params) for key, params in object_data.items()}
        for obj in self.objects.values():
            obj.actions = {key: Action(**params) for key, params in obj.actions.items()}

        # replace integer ids with object references
        for room in self.rooms.values():
            room.exits = {
                key: self.rooms[room_id]
                for key, room_id in room.exits.items()
            }
        for obj in self.objects.values():
            if obj.location is not None:
                obj.location = self.rooms[obj.location]

        self.current_room = self.rooms[start_location_id]
        self.inventory = self.rooms.pop('inventory')

    def process_command(self, command, *params):
        if command in ('north', 'south', 'west', 'east', 'up', 'down'):
            try:
                self.current_room = self.current_room.exits[command]
            except KeyError:
                raise InvalidCommand(command) from None
            return self.message_ok

        obj = params[0]
        if command == 'examine' and obj in self.visible_objects:
            return obj.description

        if obj not in self.objects_with_action(command):
            raise InvalidCommand(command, obj.name) from None

        action = obj.actions[command]
        for condition_spec in action.condition:
            callback_name, kwargs = condition_spec
            if not getattr(callbacks, callback_name)(self, **kwargs):
                raise InvalidCommand(command, obj.name) from None

        for impact_spec in action.impact:
            callback_name, kwargs = impact_spec
            getattr(callbacks, callback_name)(self, **kwargs)
        return action.message or self.message_ok

    @property
    def objects_in_room(self):
        return [
            obj for obj in self.objects.values()
            if obj.location is self.current_room
        ]

    @property
    def objects_in_inventory(self):
        return [obj for obj in self.objects.values() if obj.location is self.inventory]

    @property
    def visible_objects(self):
        return self.objects_in_room + self.objects_in_inventory

    def objects_with_action(self, action):
        return [
            obj for obj in self.visible_objects
            if action in obj.actions and obj.actions[action].enabled
        ]
