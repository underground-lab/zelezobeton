from dataclasses import dataclass, field
from typing import Optional

from game import callbacks


@dataclass
class Room:
    description: Optional[str] = None
    exits: dict = field(default_factory=dict)


@dataclass
class Object:
    name: str
    description: str
    location: Optional[Room] = None
    portable: bool = True
    actions: dict = field(default_factory=dict)


class Game:
    def __init__(self, room_data, object_data, start_location_id=0):
        self.rooms = {i: Room(**params) for i, params in room_data.items()}
        self.objects = {i: Object(**params) for i, params in object_data.items()}

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
        exits = self.current_room.exits
        if command in ('north', 'south', 'west', 'east', 'up', 'down'):
            if command in exits:
                self.current_room = exits[command]
        elif command == 'examine':
            obj = params[0]
            return obj.description
        elif command == 'take':
            obj = params[0]
            obj.location = self.inventory
            return 'OK'
        else:
            obj = params[0]
            action = obj.actions[command]
            for impact_spec in action['impact']:
                callback_name, kwargs = impact_spec
                getattr(callbacks, callback_name)(self, **kwargs)
            return action.get('message') or 'OK'

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

    @property
    def portable_objects(self):
        return [obj for obj in self.objects_in_room if obj.portable]

    def objects_with_action(self, action):
        return [
            obj for obj in self.visible_objects
            if action in obj.actions and obj.actions[action].get('enabled', True)
        ]
