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
    dvere = game.objects['dvere']
    assert game.objects_with_action('open') == [dvere]

    response = game.process_command('open', dvere)
    assert response is game.message_ok
    assert game.current_room.exits['east'] is game.rooms['sklad']
    assert game.rooms['sklad'].exits['west'] is game.current_room
    assert not game.objects_with_action('open')

    response = game.process_command('east')
    assert response is game.message_ok
    assert game.current_room is game.rooms['sklad']

    smetak = game.objects['smetak']
    response = game.process_command('take', smetak)
    assert response is game.message_ok
    assert smetak.location is game.inventory

    response = game.process_command('west')
    assert response is game.message_ok
    assert game.current_room is game.rooms['start']

    response = game.process_command('north')
    assert response is game.message_ok
    assert game.current_room is game.rooms['kancelar']
    plechovka = game.objects['plechovka']
    assert game.objects_with_action('open') == [plechovka]

    response = game.process_command('open', plechovka)
    assert 'dvě kancelářské sponky' in response
    assert not game.objects_with_action('open')
    assert len(game.objects_with_action('take')) == 3

    sponky = game.objects['sponky']
    response = game.process_command('take', sponky)
    assert response is game.message_ok
    assert sponky.location is game.inventory

    response = game.process_command('use', smetak)
    assert 'našel malý klíček' in response
    vaza = game.objects['vaza']
    assert vaza not in game.visible_objects

    klicek = game.objects['klicek']
    response = game.process_command('take', klicek)
    assert response is game.message_ok
    assert klicek.location is game.inventory

    response = game.process_command('south')
    assert response is game.message_ok
    assert game.current_room is game.rooms['start']

    response = game.process_command('east')
    assert response is game.message_ok
    assert game.current_room is game.rooms['sklad']
    assert not game.objects_with_action('open')

    response = game.process_command('use', sponky)
    assert 'odemkl zámek mříže' in response
    assert sponky not in game.visible_objects
    mriz = game.objects['mriz']
    assert game.objects_with_action('open') == [mriz]

    response = game.process_command('open', mriz)
    assert response is game.message_ok
    assert not game.objects_with_action('open')

    response = game.process_command('south')
    assert response is game.message_ok
    assert game.current_room is game.rooms['vyklenek']
    assert not game.objects_with_action('open')

    response = game.process_command('use', klicek)
    assert 'odemkl trezor' in response
    assert klicek not in game.visible_objects
    trezor = game.objects['trezor']
    assert game.objects_with_action('open') == [trezor]

    response = game.process_command('open', trezor)
    assert 'našel obálku' in response
    assert not game.objects_with_action('open')

    obalka = game.objects['obalka']
    response = game.process_command('take', obalka)
    assert response is game.message_ok
    assert obalka.location is game.inventory


def test_straightforward_walk_through(game):
    game.process_command('north')
    game.process_command('open', game.objects['plechovka'])
    game.process_command('take', game.objects['sponky'])
    game.process_command('south')
    game.process_command('open', game.objects['dvere'])
    game.process_command('east')
    game.process_command('use', game.objects['sponky'])
    game.process_command('take', game.objects['smetak'])
    game.process_command('west')
    game.process_command('north')
    game.process_command('use', game.objects['smetak'])
    game.process_command('take', game.objects['klicek'])
    game.process_command('south')
    game.process_command('east')
    game.process_command('open', game.objects['mriz'])
    game.process_command('south')
    game.process_command('use', game.objects['klicek'])
    game.process_command('open', game.objects['trezor'])
    game.process_command('take', game.objects['obalka'])


def test_portable_container_opened_before_taken(game):
    game.process_command('north')
    game.process_command('open', game.objects['plechovka'])
    assert game.objects['sponky'].location is game.current_room
    game.process_command('take', game.objects['plechovka'])
    assert game.objects['sponky'] in game.objects_with_action('take')
    assert not game.objects_with_action('open')
    assert not game.objects_with_action('use')


def test_portable_container_opened_after_taken(game):
    game.process_command('north')
    game.process_command('take', game.objects['plechovka'])
    game.process_command('open', game.objects['plechovka'])
    assert game.objects['sponky'].location is game.inventory
    assert game.objects['sponky'] not in game.objects_with_action('take')
    assert not game.objects_with_action('open')
    assert game.objects_with_action('use') == [game.objects['sponky']]
