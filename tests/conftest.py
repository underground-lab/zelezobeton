from handpick import values_for_key
import pytest

from engine.classes import Room, Object, Action, Game
from engine.serializer import GameJSONSerializer
from games import game_data


@pytest.fixture
def game():
    return Game(game_data.rooms, game_data.objects)


@pytest.fixture
def game_in_progress(game):
    game.process_command('north')
    game.process_command('open', 'plechovka')
    game.process_command('vezmi', 'sponky')
    game.process_command('south')
    game.process_command('open', 'dvere')
    return game


@pytest.fixture
def serializer():
    return GameJSONSerializer()


@pytest.fixture
def callback_specs():
    return [
        spec
        for spec_list in values_for_key(game_data.objects, ['condition', 'impact'])
        for spec in spec_list
    ]


@pytest.fixture
def exits_from_callback_specs(callback_specs):
    return {
        kwargs['direction']
        for _, kwargs in callback_specs
        if 'direction' in kwargs
    }


@pytest.fixture
def exits_from_room_data():
    return {
        exit_key
        for room in game_data.rooms.values()
        for exit_key in room.get('exits', {})
    }


@pytest.fixture
def actions_from_object_data():
    return {
        action_key
        for obj in game_data.objects.values()
        for action_key in obj.get('actions', {})
    }


@pytest.fixture
def dummy_room():
    return Room('a', {'north': 'b'})


@pytest.fixture
def dummy_room_json():
    return '{"_class": "Room", "_vars": {"description": "a", "exits": {"north": "b"}}}'


@pytest.fixture
def dummy_object(dummy_action):
    return Object('a', 'b', {'take': [dummy_action]})


@pytest.fixture
def dummy_object_json(dummy_action_json):
    return (
        '{"_class": "Object", "_vars": {"name": "a", "location": "b", "actions":'
        ' {"take": ['
        f'{dummy_action_json}'
        ']}}}'
    )


@pytest.fixture
def dummy_obj_with_attr(dummy_action):
    obj = Object('a', 'b', {'take': [dummy_action]})
    obj.unlocked = True
    return obj


@pytest.fixture
def dummy_obj_with_attr_json(dummy_action_json):
    return (
        '{"_class": "Object", "_vars": {"name": "a", "location": "b", "actions":'
        ' {"take": ['
        f'{dummy_action_json}'
        ']}, "unlocked": true}}'
    )


@pytest.fixture
def dummy_action():
    return Action([['a', {'b': 'c'}]], [['d', {'e': 'f'}]], 'OK')


@pytest.fixture
def dummy_action_json():
    return (
        '{"_class": "Action", "_vars": {"condition": [["a", {"b": "c"}]],'
        ' "impact": [["d", {"e": "f"}]], "message": "OK"}}'
    )


@pytest.fixture
def dummy_game(dummy_room, dummy_object):
    return Game({'a': dummy_room}, {'b': dummy_object}, 'a')


@pytest.fixture
def dummy_game_json(dummy_room_json, dummy_object_json):
    return (
        '{"_class": "Game", "_vars": {"rooms": {"a":'
        f' {dummy_room_json}'
        '}, "objects": {"b":'
        f' {dummy_object_json}'
        '}, "current_room_key": "a"}}'
    )
