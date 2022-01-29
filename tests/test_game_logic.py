# coding: utf-8

from copy import deepcopy

import pytest

from game import new_game
from game.classes import InvalidCommand


@pytest.fixture
def game():
    return deepcopy(new_game)


def test_game_walk_through(game):
    assert game.current_room is game.rooms['start']
    assert game.objects_with_action('open') == [game.objects['dvere']]

    response = game.process_command('north')
    assert response is game.message_ok
    assert game.current_room is game.rooms['pracovna']
    assert game.objects_with_action('take') == [game.objects['plechovka']]
    assert game.objects_with_action('open') == [game.objects['plechovka']]

    response = game.process_command('examine', game.objects['plechovka'])
    assert '"plechovka"' in response

    response = game.process_command('take', game.objects['plechovka'])
    assert response is game.message_ok
    assert game.objects['plechovka'].location is game.inventory
    assert game.objects_with_action('open') == [game.objects['plechovka']]
    assert not game.objects_with_action('take')
    assert not game.objects_in_room

    with pytest.raises(InvalidCommand, match=r'west'):
        game.process_command('west')

    with pytest.raises(InvalidCommand, match=r'take.*plechovku'):
        game.process_command('take', game.objects['plechovka'])

    response = game.process_command('south')
    assert response is game.message_ok
    assert 'east' not in game.current_room.exits
    assert game.objects_in_room == [game.objects['dvere']]
    assert not game.objects_with_action('take')
    assert len(game.objects_with_action('open')) == 2
    assert game.objects['klicek'] not in game.visible_objects

    response = game.process_command('open', game.objects['plechovka'])
    assert response == 'V plechovce byl malý klíček.'
    assert game.objects_with_action('open') == [game.objects['dvere']]
    assert game.objects['klicek'].location is game.inventory
    assert game.objects_with_action('use') == [game.objects['klicek']]
    assert not game.objects_with_action('take')

    with pytest.raises(InvalidCommand, match=r'use.*klíček'):
        game.process_command('use', game.objects['klicek'])

    with pytest.raises(InvalidCommand, match=r'open.*plechovku'):
        game.process_command('open', game.objects['plechovka'])

    response = game.process_command('examine', game.objects['dvere'])
    assert '"dveře"' in response

    assert game.objects_with_action('open') == [game.objects['dvere']]

    response = game.process_command('open', game.objects['dvere'])
    assert response == 'Otevřel jsem dveře.'
    assert game.current_room.exits['east'] is game.rooms['sklad']
    assert game.rooms['sklad'].exits['west'] is game.current_room
    assert not game.objects_with_action('open')

    with pytest.raises(InvalidCommand, match=r'open.*dveře'):
        game.process_command('open', game.objects['dvere'])

    response = game.process_command('east')
    assert response is game.message_ok
    assert game.current_room is game.rooms['sklad']

    response = game.process_command('down')
    assert response is game.message_ok
    assert game.current_room is game.rooms['sklep']
    assert not game.objects_with_action('take')
    assert not game.objects_with_action('open')
    assert game.objects['nuzky'] not in game.visible_objects

    response = game.process_command('examine', game.objects['trezor'])
    assert '"trezor"' in response

    with pytest.raises(InvalidCommand, match=r'open.*trezor'):
        game.process_command('open', game.objects['trezor'])

    response = game.process_command('use', game.objects['klicek'])
    assert response == 'Odemkl jsem trezor.'
    assert game.objects['klicek'] not in game.visible_objects

    response = game.process_command('open', game.objects['trezor'])
    assert response == 'V trezoru jsem našel nůžky.'
    assert game.objects['nuzky'].location is game.current_room
    assert game.objects_with_action('take') == [game.objects['nuzky']]
    assert not game.objects_with_action('open')
    assert not game.objects_with_action('use')

    with pytest.raises(InvalidCommand, match=r'open.*trezor'):
        game.process_command('open', game.objects['trezor'])

    response = game.process_command('take', game.objects['nuzky'])
    assert response is game.message_ok
    assert game.objects['nuzky'].location is game.inventory
    assert not game.objects_with_action('take')

    response = game.process_command('up')
    assert response is game.message_ok

    response = game.process_command('west')
    assert response is game.message_ok


def test_straightforward_walk_through(game):
    game.process_command('north')
    game.process_command('open', game.objects['plechovka'])
    game.process_command('take', game.objects['klicek'])
    game.process_command('south')
    game.process_command('open', game.objects['dvere'])
    game.process_command('east')
    game.process_command('down')
    game.process_command('use', game.objects['klicek'])
    game.process_command('open', game.objects['trezor'])
    game.process_command('take', game.objects['nuzky'])
    game.process_command('up')
    game.process_command('west')


def test_portable_container_opened_before_taken(game):
    game.process_command('north')
    game.process_command('open', game.objects['plechovka'])
    assert game.objects['klicek'].location is game.current_room
    game.process_command('take', game.objects['plechovka'])
    assert game.objects_with_action('take') == [game.objects['klicek']]
    assert not game.objects_with_action('open')
    assert not game.objects_with_action('use')


def test_portable_container_opened_after_taken(game):
    game.process_command('north')
    game.process_command('take', game.objects['plechovka'])
    game.process_command('open', game.objects['plechovka'])
    assert game.objects['klicek'].location is game.inventory
    assert not game.objects_with_action('take')
    assert not game.objects_with_action('open')
    assert game.objects_with_action('use') == [game.objects['klicek']]
