from copy import deepcopy
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Room:
    description: str
    exits: dict = field(default_factory=dict)


class Object:
    def __init__(self, name, location='undiscovered', actions=None, **kwargs):
        self.name = name
        self.location = location
        self.actions = actions or {}
        # set additional instance variables
        vars(self).update(kwargs)


@dataclass
class Action:
    condition: list = field(default_factory=list)
    impact: list = field(default_factory=list)
    message: Optional[str] = None


class Game:
    message_ok = 'OK'

    def __init__(self, rooms, objects, current_room_key='start'):
        self.rooms = self._rooms_from_data(rooms)
        self.objects = self._objects_from_data(objects)
        self.current_room_key = current_room_key

    def _rooms_from_data(self, data):
        return {
            key: self._ensure_class(item, Room)
            for key, item in deepcopy(data).items()
        }

    def _objects_from_data(self, data):
        result = {}
        for key, item in deepcopy(data).items():
            obj = self._ensure_class(item, Object)
            # replace action specs with Action instances
            obj.actions = {
                key: [
                    self._ensure_class(item, Action)
                    for item in self._ensure_list(action_specs)
                ]
                for key, action_specs in obj.actions.items()
            }
            result[key] = obj
        return result

    @staticmethod
    def _ensure_class(obj, cls):
        if isinstance(obj, cls):
            return obj
        return cls(**obj)

    @staticmethod
    def _ensure_list(action_specs):
        if isinstance(action_specs, list):
            return action_specs
        return [action_specs]

    def process_command(self, command, *params):
        if command in self.current_room.exits:
            self.current_room_key = self.current_room.exits[command]
            return self.message_ok

        if not params:
            raise InvalidCommand(command)

        obj_key = params[0]
        if obj_key in self.objects_with_action(command):
            for action in self.objects[obj_key].actions[command]:
                if self._conditions_met(action):
                    self._apply_impact(action)
                    return action.message or self.message_ok

        raise InvalidCommand(command, obj_key)

    def _conditions_met(self, action):
        return all(
            getattr(self, callback_name)(**kwargs)
            for callback_name, kwargs in action.condition
        )

    def _apply_impact(self, action):
        for callback_name, kwargs in action.impact:
            getattr(self, callback_name)(**kwargs)

    @property
    def current_room(self):
        return self.rooms[self.current_room_key]

    @property
    def objects_in_room(self):
        return {
            obj_key: obj for obj_key, obj in self.objects.items()
            if obj.location == self.current_room_key
        }

    @property
    def objects_in_inventory(self):
        return {
            obj_key: obj for obj_key, obj in self.objects.items()
            if obj.location == 'inventory'
        }

    @property
    def visible_objects(self):
        return {**self.objects_in_room, **self.objects_in_inventory}

    def objects_with_action(self, action_name):
        return {
            obj_key: obj for obj_key, obj in self.visible_objects.items()
            if action_name in obj.actions
            and any(self._conditions_met(action) for action in obj.actions[action_name])
        }

    def available_actions(self):
        result = {}
        for action_name in ('examine', 'take', 'open', 'use'):
            objects = self.objects_with_action(action_name)
            if objects:
                result[action_name] = objects
        return result

    # callbacks that don't modify game state
    def is_visible(self, obj):
        return obj in self.visible_objects

    def in_room(self, obj):
        return obj in self.objects_in_room

    def in_inventory(self, obj):
        return self.objects[obj].location == 'inventory'

    def is_undiscovered(self, obj):
        return self.objects[obj].location == 'undiscovered'

    def is_gone(self, obj):
        return self.objects[obj].location == 'gone'

    def current_room_is(self, room):
        return self.current_room_key == room

    def exit_closed(self, room, direction):
        return direction not in self.rooms[room].exits

    def is_true(self, obj, attr):
        return getattr(self.objects[obj], attr, None) is True

    def not_true(self, obj, attr):
        return not getattr(self.objects[obj], attr, None)

    # callbacks that modify game state
    def move_to_room(self, obj, room):
        self.objects[obj].location = room

    def move_to_current_room(self, obj):
        self.objects[obj].location = self.current_room_key

    def move_to_inventory(self, obj):
        self.objects[obj].location = 'inventory'

    def remove_object(self, obj):
        self.objects[obj].location = 'gone'

    def open_exit(self, room, direction, room_2):
        self.rooms[room].exits[direction] = room_2

    def close_exit(self, room, direction):
        exits = self.rooms[room].exits
        if direction in exits:
            del exits[direction]

    def set_true(self, obj, attr):
        setattr(self.objects[obj], attr, True)


class InvalidCommand(NotImplementedError):
    pass
