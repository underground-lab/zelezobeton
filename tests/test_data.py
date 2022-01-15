from collections import Counter
from itertools import chain

import pytest

import game.callbacks
from game.data import room_data, object_data, player_data


def test_all_exits_exist():
    for room_id, room in room_data.items():
        for target_room_id in room['exits'].values():
            assert target_room_id in room_data, \
                f'Unknown room {target_room_id} in exits of room {room_id}'


def test_all_exit_relations_are_symmetric():
    opposites = dict(
        north='south', south='north', west='east', east='west', up='down', down='up'
    )
    for room_id, room in room_data.items():
        for direction, target_room_id in room['exits'].items():
            target_room = room_data[target_room_id]
            opposite_direction = opposites[direction]
            assert target_room['exits'].get(opposite_direction) == room_id, \
                f'Asymmetric exits between rooms {room_id} and {target_room_id}'


def test_no_room_has_exit_to_itself():
    for room_id, room in room_data.items():
        assert room_id not in room['exits'].values(), \
            f'Room {room_id} has an exit to itself'


def test_all_objects_exist():
    for room_id, room in room_data.items():
        for obj_id in room.get('objects', []):
            assert obj_id in object_data, \
                f'Unknown object {obj_id} in room {room_id}'

    for obj_id in player_data['inventory']:
        assert obj_id in object_data, f'Unknown object {obj_id} in inventory'


def test_no_object_occurs_more_than_once():
    occurrences = chain(
        *(room.get('objects', []) for room in room_data.values()),
        player_data['inventory']
    )
    most_common, count = Counter(occurrences).most_common()[0]
    assert count <= 1, f'Object {most_common} occurs in more than one place'


@pytest.fixture
def impact_specs():
    return [
        impact_spec
        for obj in object_data.values()
        for action in obj.get('actions', {}).values()
        for impact_spec in action['impact']
    ]


def test_impact_specs_use_existing_callback_names(impact_specs):
    for impact_spec in impact_specs:
        callback_name = impact_spec[0]
        assert hasattr(game.callbacks, callback_name), \
            f'Unknown callback {callback_name!r}'


def test_impact_specs_use_existing_room_ids(impact_specs):
    for impact_spec in impact_specs:
        kwargs = impact_spec[1]
        if 'room' in kwargs:
            room_id = kwargs['room']
            assert room_id in room_data, f'Unknown room {room_id} in {impact_spec}'


def test_impact_specs_use_existing_object_ids(impact_specs):
    for impact_spec in impact_specs:
        kwargs = impact_spec[1]
        if 'obj' in kwargs:
            obj_id = kwargs['obj']
            assert obj_id in object_data, f'Unknown object {obj_id} in {impact_spec}'
