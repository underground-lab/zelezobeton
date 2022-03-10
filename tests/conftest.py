import pytest

from engine import Game
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
