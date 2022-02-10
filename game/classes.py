from dataclasses import dataclass, field
from typing import Optional, Union


@dataclass
class Room:
    description: str
    exits: dict = field(default_factory=dict)


@dataclass
class Object:
    name: str
    description: str
    location: Union[str, Room] = 'undiscovered'
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
            if obj.location in self.rooms:
                obj.location = self.rooms[obj.location]

        self.current_room = self.rooms[start_location_id]

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
        if not self._conditions_met(action):
            raise InvalidCommand(command, obj.name) from None

        for callback_name, kwargs in action.impact:
            getattr(self, callback_name)(**kwargs)
        return action.message or self.message_ok

    @property
    def objects_in_room(self):
        return [
            obj for obj in self.objects.values()
            if obj.location is self.current_room
        ]

    @property
    def objects_in_inventory(self):
        return [obj for obj in self.objects.values() if obj.location == 'inventory']

    @property
    def visible_objects(self):
        return self.objects_in_room + self.objects_in_inventory

    def objects_with_action(self, action_name):
        return [
            obj for obj in self.visible_objects
            if action_name in obj.actions
            and self._action_enabled(obj, action_name)
        ]

    def _conditions_met(self, action):
        for callback_name, kwargs in action.condition:
            if not getattr(self, callback_name)(**kwargs):
                return False
        return True

    def _action_enabled(self, obj, action_name):
        if not obj.actions[action_name].enabled:
            return False
        if action_name == 'take' and obj.location == 'inventory':
            # cannot take object already taken
            return False
        if (action_name == 'use' and 'take' in obj.actions
                and obj.location != 'inventory'):
            # can only use portable object if taken
            return False
        return True

    # callbacks that don't modify game state
    def is_visible(self, obj):
        return self.objects[obj] in self.visible_objects

    def in_room(self, obj):
        return self.objects[obj].location is self.current_room

    def in_inventory(self, obj):
        return self.objects[obj].location == 'inventory'

    def is_undiscovered(self, obj):
        return self.objects[obj].location == 'undiscovered'

    def is_gone(self, obj):
        return self.objects[obj].location == 'gone'

    def action_enabled(self, obj, action):
        return self.objects[obj].actions[action].enabled

    def action_disabled(self, obj, action):
        return not self.objects[obj].actions[action].enabled

    def current_room_is(self, room):
        return self.current_room is self.rooms[room]

    # callbacks that modify game state
    def move_to_room(self, obj, room):
        self.objects[obj].location = self.rooms[room]

    def move_to_current_room(self, obj):
        self.objects[obj].location = self.current_room

    def move_to_inventory(self, obj):
        self.objects[obj].location = 'inventory'

    def remove_object(self, obj):
        self.objects[obj].location = 'gone'

    def move_to_same_location(self, obj, obj_2):
        self.objects[obj].location = self.objects[obj_2].location

    def enable_action(self, obj, action):
        self.objects[obj].actions[action].enabled = True

    def disable_action(self, obj, action):
        self.objects[obj].actions[action].enabled = False

    def open_exit(self, room, direction, room_2):
        self.rooms[room].exits[direction] = self.rooms[room_2]

    def close_exit(self, room, direction):
        exits = self.rooms[room].exits
        if direction in exits:
            del exits[direction]


class InvalidCommand(NotImplementedError):
    ...
