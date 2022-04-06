from handpick import values_for_key
import pytest

from engine.classes import Game
from engine.serializer import GameJSONSerializer
from game.data import room_data, object_data


@pytest.fixture
def game():
    return Game(room_data, object_data)


@pytest.fixture
def game_in_progress(game):
    game.process_command('north')
    game.process_command('open', 'plechovka')
    game.process_command('take', 'sponky')
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
        for spec_list in values_for_key(object_data, ['condition', 'impact'])
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
        for room in room_data.values()
        for exit_key in room.get('exits', {})
    }


@pytest.fixture
def actions_from_object_data():
    return {
        action_key
        for obj in object_data.values()
        for action_key in obj.get('actions', {})
    }
