from collections import Counter
from itertools import chain

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
