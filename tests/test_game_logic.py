# coding: utf-8

import pytest

from game import new_game
from game.classes import InvalidCommand


@pytest.fixture
def game():
    return new_game()


def test_game_walk_through(game):
    assert game.current_room is game.rooms['start']

    response = game.process_command('north')
    assert response is game.message_ok
    assert game.current_room is game.rooms['pracovna']

    assert game.objects['plechovka'] in game.objects_with_action('take')
    assert game.objects['plechovka'] in game.objects_with_action('open')

    response = game.process_command('examine', game.objects['plechovka'])
    assert 'předmět typu krabička' in response

    response = game.process_command('take', game.objects['plechovka'])
    assert response is game.message_ok
    assert game.objects['plechovka'].location is game.inventory
    assert game.objects['plechovka'] in game.objects_with_action('open')
    assert not game.objects_in_room

    with pytest.raises(InvalidCommand, match=r'west'):
        game.process_command('west')

    with pytest.raises(InvalidCommand, match=r'take.*plechovku'):
        game.process_command('take', game.objects['plechovka'])

    response = game.process_command('south')
    assert response is game.message_ok
    assert game.current_room is game.rooms['start']
    assert 'east' not in game.current_room.exits
    assert game.objects['dvere'] in game.objects_in_room
    assert not game.objects_with_action('take')
    assert game.objects_with_action('open') == [game.objects['plechovka']]

    response = game.process_command('open', game.objects['plechovka'])
    assert response == 'V plechovce byl malý klíček.'
    assert not game.objects_with_action('open')
    assert game.objects['klicek'].location is game.inventory

    with pytest.raises(InvalidCommand, match=r'open.*plechovku'):
        game.process_command('open', game.objects['plechovka'])

    response = game.process_command('examine', game.objects['dvere'])
    assert 'předmět typu dveře' in response

    with pytest.raises(InvalidCommand, match=r'open.*dveře'):
        game.process_command('open', game.objects['dvere'])

    response = game.process_command('use', game.objects['klicek'])
    assert response == 'Odemkl jsi dveře.'

    response = game.process_command('open', game.objects['dvere'])
    assert response == 'Otevřel jsi dveře.'
    assert game.current_room.exits['east'] is game.rooms['sklad']
    assert not game.objects_with_action('open')

    with pytest.raises(InvalidCommand, match=r'open.*dveře'):
        game.process_command('open', game.objects['dvere'])

    response = game.process_command('east')
    assert response is game.message_ok
    assert game.current_room is game.rooms['sklad']

    response = game.process_command('down')
    assert response is game.message_ok
    assert game.current_room is game.rooms['sklep']
    assert game.objects['skrinka'] in game.objects_in_room
    assert not game.objects_with_action('take')
    assert game.objects['nuzky'] not in game.visible_objects
    assert game.objects['skrinka'] in game.objects_with_action('open')

    response = game.process_command('examine', game.objects['skrinka'])
    assert 'předmět typu skříň' in response

    response = game.process_command('open', game.objects['skrinka'])
    assert response == 'Ve skříňce jsi našel nůžky.'
    assert game.objects['nuzky'] in game.objects_with_action('take')
    assert not game.objects_with_action('open')

    with pytest.raises(InvalidCommand, match=r'open.*skříňku'):
        game.process_command('open', game.objects['skrinka'])

    response = game.process_command('take', game.objects['nuzky'])
    assert response is game.message_ok
    assert game.objects['nuzky'] not in game.objects_in_room
    assert game.objects['nuzky'].location is game.inventory
    assert not game.objects_with_action('take')

    with pytest.raises(InvalidCommand, match=r'open.*nůžky'):
        game.process_command('open', game.objects['nuzky'])


def test_portable_container_opened_before_taken(game):
    game.process_command('north')
    game.process_command('open', game.objects['plechovka'])
    assert game.objects['klicek'].location is game.current_room
    assert game.objects['klicek'] in game.objects_with_action('take')


def test_portable_container_opened_after_taken(game):
    game.process_command('north')
    game.process_command('take', game.objects['plechovka'])
    game.process_command('open', game.objects['plechovka'])
    assert game.objects['klicek'].location is game.inventory
    assert not game.objects_with_action('take')
