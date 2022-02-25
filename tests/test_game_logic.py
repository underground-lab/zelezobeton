# coding: utf-8

from copy import deepcopy

import pytest

from engine import Game, InvalidCommand
from game.data import room_data, object_data


@pytest.fixture
def game():
    return deepcopy(Game(room_data, object_data))


@pytest.fixture
def game_in_progress(game):
    game.process_command('north')
    game.process_command('open', 'plechovka')
    game.process_command('take', 'sponky')
    game.process_command('south')
    game.process_command('open', 'dvere')
    return game


def test_game_walk_through(game):
    assert game.current_room is game.rooms['start']
    assert list(game.objects_with_action('open')) == ['dvere']

    response = game.process_command('open', 'dvere')
    assert response is game.message_ok
    assert game.current_room.exits['east'] is game.rooms['sklad']
    assert game.rooms['sklad'].exits['west'] is game.current_room
    assert not game.objects_with_action('open')

    response = game.process_command('east')
    assert response is game.message_ok
    assert game.current_room is game.rooms['sklad']

    # cannot be used before taken
    with pytest.raises(InvalidCommand):
        game.process_command('use', 'smetak')

    response = game.process_command('take', 'smetak')
    assert response is game.message_ok
    assert 'smetak' in game.objects_in_inventory

    # cannot take again
    with pytest.raises(InvalidCommand):
        game.process_command('take', 'smetak')

    response = game.process_command('take', 'krabice')
    assert 'Jeden bude stačit' in response
    assert 'krabice' not in game.objects_in_inventory
    assert 'hrebik' in game.objects_in_inventory

    response = game.process_command('west')
    assert response is game.message_ok
    assert game.current_room is game.rooms['start']

    response = game.process_command('north')
    assert response is game.message_ok
    assert game.current_room is game.rooms['kancelar']
    assert list(game.objects_with_action('open')) == ['plechovka']

    response = game.process_command('open', 'plechovka')
    assert 'dvě kancelářské sponky' in response
    assert not game.objects_with_action('open')
    assert len(game.objects_with_action('take')) == 3

    # cannot be used before taken
    with pytest.raises(InvalidCommand):
        game.process_command('use', 'sponky')

    response = game.process_command('take', 'sponky')
    assert response is game.message_ok
    assert 'sponky' in game.objects_in_inventory

    # cannot take again
    with pytest.raises(InvalidCommand):
        game.process_command('take', 'sponky')

    response = game.process_command('use', 'smetak')
    assert 'našel malý klíček' in response
    assert 'vaza' not in game.visible_objects

    # use again
    response = game.process_command('use', 'smetak')
    assert 'Nevím jak' in response

    # cannot be used before taken
    with pytest.raises(InvalidCommand):
        game.process_command('use', 'klicek')

    response = game.process_command('take', 'klicek')
    assert response is game.message_ok
    assert 'klicek' in game.objects_in_inventory

    # cannot take again
    with pytest.raises(InvalidCommand):
        game.process_command('take', 'klicek')

    response = game.process_command('take', 'plechovka')
    assert response is game.message_ok
    assert 'plechovka' in game.objects_in_inventory

    # cannot take again
    with pytest.raises(InvalidCommand):
        game.process_command('take', 'plechovka')

    response = game.process_command('south')
    assert response is game.message_ok
    assert game.current_room is game.rooms['start']

    response = game.process_command('east')
    assert response is game.message_ok
    assert game.current_room is game.rooms['sklad']

    response = game.process_command('open', 'mriz')
    assert response == 'Je zamčená.'

    response = game.process_command('use', 'sponky')
    assert 'odemkl zámek mříže' in response
    assert game.objects['mriz'].unlocked is True
    assert list(game.objects_with_action('open')) == ['mriz']

    # use again
    response = game.process_command('use', 'sponky')
    assert 'Nevím jak' in response

    response = game.process_command('open', 'mriz')
    assert response is game.message_ok
    assert not game.objects_with_action('open')

    response = game.process_command('south')
    assert response is game.message_ok
    assert game.current_room is game.rooms['vyklenek']

    response = game.process_command('open', 'trezor')
    assert response == 'Je zamčený.'

    response = game.process_command('use', 'klicek')
    assert 'odemkl trezor' in response
    assert game.objects['trezor'].unlocked is True
    assert list(game.objects_with_action('open')) == ['trezor']

    # use again
    response = game.process_command('use', 'klicek')
    assert 'Nevím jak' in response

    response = game.process_command('open', 'trezor')
    assert 'našel obálku' in response
    assert not game.objects_with_action('open')

    response = game.process_command('take', 'obalka')
    assert response is game.message_ok
    assert 'obalka' in game.objects_in_inventory

    # cannot take again
    with pytest.raises(InvalidCommand):
        game.process_command('take', 'obalka')


def test_straightforward_walk_through(game):
    game.process_command('north')
    game.process_command('open', 'plechovka')
    game.process_command('take', 'sponky')
    game.process_command('south')
    game.process_command('open', 'dvere')
    game.process_command('east')
    game.process_command('use', 'sponky')
    game.process_command('take', 'smetak')
    game.process_command('west')
    game.process_command('north')
    game.process_command('use', 'smetak')
    game.process_command('take', 'klicek')
    game.process_command('south')
    game.process_command('east')
    game.process_command('open', 'mriz')
    game.process_command('south')
    game.process_command('use', 'klicek')
    game.process_command('open', 'trezor')
    game.process_command('take', 'obalka')


def test_portable_container_opened_before_taken(game):
    game.process_command('north')
    game.process_command('open', 'plechovka')
    assert game.objects['sponky'].location is game.current_room
    game.process_command('take', 'plechovka')
    assert 'sponky' in game.objects_with_action('take')
    assert not game.objects_with_action('open')
    assert not game.objects_with_action('use')


def test_portable_container_opened_after_taken(game):
    game.process_command('north')
    game.process_command('take', 'plechovka')
    game.process_command('open', 'plechovka')
    assert 'sponky' in game.objects_in_inventory
    assert 'sponky' not in game.objects_with_action('take')
    assert not game.objects_with_action('open')
    assert list(game.objects_with_action('use')) == ['sponky']


@pytest.mark.parametrize(
    'command, obj_key',
    (
        ('examine', 'plechovka'),    # examine invisible object
        ('take', 'plechovka'),    # take invisible object
        ('take', 'sponky'),    # take already taken object
        ('take', 'dvere'),    # take unexpected object
        ('open', 'trezor'),    # open invisible object
        ('open', 'dvere'),    # open already open object
        ('open', 'sponky'),    # open unexpected object
        ('use', 'smetak'),    # use invisible object
        ('use', 'dvere'),    # use unexpected object
    ),
)
def test_invalid_commands(game_in_progress, command, obj_key):
    with pytest.raises(InvalidCommand):
        game_in_progress.process_command(command, obj_key)
