from copy import deepcopy
from dataclasses import dataclass, field
import json
from typing import Optional


@dataclass
class Room:
    description: str
    exits: dict = field(default_factory=dict)


@dataclass
class Object:
    name: str
    description: str
    location: str = 'undiscovered'
    actions: dict = field(default_factory=dict)


@dataclass
class Action:
    condition: list = field(default_factory=list)
    impact: list = field(default_factory=list)
    message: Optional[str] = None


class Game:
    message_ok = 'OK'

    def __init__(self, room_data, object_data, current_room='start'):
        self.rooms = self._rooms_from_data(room_data)
        self.objects = self._objects_from_data(object_data)
        self._current_room = current_room

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
        if command in ('north', 'south', 'west', 'east', 'up', 'down'):
            try:
                self._current_room = self.current_room.exits[command]
            except KeyError:
                raise InvalidCommand(command) from None
            return self.message_ok

        obj_key = params[0]
        obj = self.objects[obj_key]
        if command == 'examine' and obj_key in self.visible_objects:
            return obj.description

        if obj_key not in self.objects_with_action(command):
            raise InvalidCommand(command, obj_key)

        for action in obj.actions[command]:
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
        return self.rooms[self._current_room]

    @property
    def objects_in_room(self):
        return {
            obj_key: obj for obj_key, obj in self.objects.items()
            if obj.location == self._current_room
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
        return self._current_room == room

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
        self.objects[obj].location = self._current_room

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

    # serialization
    def to_json(self):
        return game_encoder.encode(self)

    @classmethod
    def from_json(cls, json_str):
        return cls(**game_decoder.decode(json_str))


class InvalidCommand(NotImplementedError):
    pass


class GameJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (Room, Object, Action)):
            return {'_class': obj.__class__.__name__, '_kwargs': obj.__dict__}
        if isinstance(obj, Game):
            return {
                'room_data': obj.rooms,
                'object_data': obj.objects,
                'current_room': obj._current_room,
            }
        return super().default(obj)


game_encoder = GameJSONEncoder(ensure_ascii=False)


def custom_class_hook(obj):
    if '_class' in obj:
        cls = {'Room': Room, 'Object': Object, 'Action': Action}[obj['_class']]
        return cls(**obj['_kwargs'])
    return obj


game_decoder = json.JSONDecoder(object_hook=custom_class_hook)
