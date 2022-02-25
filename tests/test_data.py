from handpick import values_for_key
import pytest

from engine import Game
from game.data import room_data, object_data


def test_all_exits_exist():
    for room_key, room in room_data.items():
        for target_room_key in room.get('exits', {}).values():
            assert target_room_key in room_data, \
                f'Unknown room {target_room_key!r} in exits of room {room_key!r}'


def test_all_exit_relations_are_symmetric():
    opposites = dict(
        north='south', south='north', west='east', east='west', up='down', down='up'
    )
    for room_key, room in room_data.items():
        for direction, target_room_key in room.get('exits', {}).items():
            target_room = room_data[target_room_key]
            opposite_direction = opposites[direction]
            assert target_room.get('exits', {}).get(opposite_direction) == room_key, \
                f'Asymmetric exits between rooms {room_key!r} and {target_room_key!r}'


def test_no_room_has_exit_to_itself():
    for room_key, room in room_data.items():
        assert room_key not in room.get('exits', {}).values(), \
            f'Room {room_key!r} has an exit to itself'


def test_all_object_locations_exist():
    for obj_key, obj in object_data.items():
        if 'location' not in obj:
            continue
        location = obj['location']
        assert location in room_data or location == 'inventory', \
            f'Unknown location {location!r} of object {obj_key!r}'


@pytest.fixture
def callback_specs():
    return [
        spec
        for spec_list in values_for_key(object_data, ['condition', 'impact'])
        for spec in spec_list
    ]


def test_callback_specs_use_existing_callback_names(callback_specs):
    for spec in callback_specs:
        callback_name = spec[0]
        assert hasattr(Game, callback_name), f'Unknown callback {callback_name!r}'


def test_callback_specs_use_existing_room_keys(callback_specs):
    for spec in callback_specs:
        kwargs = spec[1]
        if 'room' in kwargs:
            room_key = kwargs['room']
            assert room_key in room_data, f'Unknown room {room_key!r} in {kwargs}'
        if 'room_2' in kwargs:
            room_key = kwargs['room_2']
            assert room_key in room_data, f'Unknown room {room_key!r} in {kwargs}'


def test_callback_specs_use_existing_object_keys(callback_specs):
    for spec in callback_specs:
        kwargs = spec[1]
        if 'obj' in kwargs:
            obj_key = kwargs['obj']
            assert obj_key in object_data, f'Unknown object {obj_key!r} in {kwargs}'
