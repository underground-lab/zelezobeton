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


class Game:
    message_ok = 'OK'

    def __init__(self, room_data, object_data, start_location_id='start'):
        self.rooms = {key: Room(**params) for key, params in room_data.items()}
        self.objects = {key: Object(**params) for key, params in object_data.items()}
        for obj in self.objects.values():
            obj.actions = {
                key: [Action(**params) for params in self._ensure_list(action_specs)]
                for key, action_specs in obj.actions.items()
            }

        # replace room ids with Room instances
        for room in self.rooms.values():
            room.exits = {
                key: self.rooms[room_id]
                for key, room_id in room.exits.items()
            }
        for obj in self.objects.values():
            if obj.location in self.rooms:
                obj.location = self.rooms[obj.location]

        self.current_room = self.rooms[start_location_id]

    def _ensure_list(self, action_specs):
        if isinstance(action_specs, list):
            return action_specs
        return [action_specs]

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
            raise InvalidCommand(command, obj.name)

        for action in obj.actions[command]:
            if not self._conditions_met(action):
                continue
            for callback_name, kwargs in action.impact:
                getattr(self, callback_name)(**kwargs)
            return action.message or self.message_ok

        raise InvalidCommand(command, obj.name)

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
            and any(self._conditions_met(action) for action in obj.actions[action_name])
        ]

    def _conditions_met(self, action):
        return all(
            getattr(self, callback_name)(**kwargs)
            for callback_name, kwargs in action.condition
        )

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

    def current_room_is(self, room):
        return self.current_room is self.rooms[room]

    def exit_closed(self, room, direction):
        return direction not in self.rooms[room].exits

    def is_true(self, obj, attr):
        return getattr(self.objects[obj], attr, None) is True

    def not_true(self, obj, attr):
        return not getattr(self.objects[obj], attr, None)

    # callbacks that modify game state
    def move_to_room(self, obj, room):
        self.objects[obj].location = self.rooms[room]

    def move_to_current_room(self, obj):
        self.objects[obj].location = self.current_room

    def move_to_inventory(self, obj):
        self.objects[obj].location = 'inventory'

    def remove_object(self, obj):
        self.objects[obj].location = 'gone'

    def open_exit(self, room, direction, room_2):
        self.rooms[room].exits[direction] = self.rooms[room_2]

    def close_exit(self, room, direction):
        exits = self.rooms[room].exits
        if direction in exits:
            del exits[direction]

    def set_true(self, obj, attr):
        setattr(self.objects[obj], attr, True)


class InvalidCommand(NotImplementedError):
    ...
