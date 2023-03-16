import inspect

from engine.classes import Game
from games import game_data


def test_all_exits_exist():
    for room_key, room in game_data.room_data.items():
        for target_room_key in room.get('exits', {}).values():
            assert target_room_key in game_data.room_data, \
                f'Unknown room {target_room_key!r} in exits of room {room_key!r}'


def test_all_exit_relations_are_symmetric():
    opposites = dict(
        north='south', south='north', west='east', east='west', up='down', down='up'
    )
    for room_key, room in game_data.room_data.items():
        for direction, target_room_key in room.get('exits', {}).items():
            target_room = game_data.room_data[target_room_key]
            opposite_direction = opposites[direction]
            assert target_room.get('exits', {}).get(opposite_direction) == room_key, \
                f'Asymmetric exits between rooms {room_key!r} and {target_room_key!r}'


def test_no_room_has_exit_to_itself():
    for room_key, room in game_data.room_data.items():
        assert room_key not in room.get('exits', {}).values(), \
            f'Room {room_key!r} has an exit to itself'


def test_all_object_locations_exist():
    for obj_key, obj in game_data.objects.items():
        if 'location' not in obj:
            continue
        location = obj['location']
        assert location in game_data.room_data or location == 'inventory', \
            f'Unknown location {location!r} of object {obj_key!r}'


def test_callback_specs_use_existing_callback_names(callback_specs):
    for spec in callback_specs:
        method_name = spec[0]
        assert hasattr(Game, method_name), f'Unknown callback {method_name!r}'


def test_callback_specs_use_existing_room_keys(callback_specs):
    for spec in callback_specs:
        kwargs = spec[1]
        if 'room' in kwargs:
            room_key = kwargs['room']
            assert room_key in game_data.room_data, \
                f'Unknown room {room_key!r} in {kwargs}'
        if 'target' in kwargs:
            room_key = kwargs['target']
            assert room_key in game_data.room_data, \
                f'Unknown room {room_key!r} in {kwargs}'


def test_callback_specs_use_existing_object_keys(callback_specs):
    for spec in callback_specs:
        kwargs = spec[1]
        if 'obj' in kwargs:
            obj_key = kwargs['obj']
            assert obj_key in game_data.objects, \
                f'Unknown object {obj_key!r} in {kwargs}'


def test_callback_specs_use_correct_kwargs(callback_specs):
    for method_name, kwargs in callback_specs:
        method_params = inspect.signature(getattr(Game, method_name)).parameters
        expected_kws = method_params.keys() - {'self'}
        given_kws = kwargs.keys()
        assert given_kws == expected_kws, \
            f'Incorrect kwargs {given_kws} for {method_name!r}: expected {expected_kws}'
