import pytest

from game import new_game


@pytest.fixture
def game():
    return new_game()


def test_game_walk_through(game):
    assert game.current_room is game.rooms[0]
    assert game.objects[1] in game.portable_objects
    assert game.objects[1] in game.objects_with_action('open')

    response = game.process_command('examine', game.objects[1])
    assert 'předmět typu krabička' in response

    response = game.process_command('take', game.objects[1])
    assert response == 'OK'
    assert game.objects[1].location == 'inventory'
    assert game.objects[1] in game.objects_with_action('open')
    assert not game.objects_in_room

    response = game.process_command('north')
    assert response is None
    assert game.current_room is game.rooms[1]
    assert 'east' not in game.current_room.exits
    assert game.objects[4] in game.objects_in_room
    assert not game.portable_objects
    assert len(game.objects_with_action('open')) == 2

    response = game.process_command('open', game.objects[1])
    assert response == 'V plechovce byl malý klíček.'
    assert len(game.objects_with_action('open')) == 1
    assert game.objects[2].location == 'inventory'

    response = game.process_command('open', game.objects[4])
    assert response == 'Otevřel jsi dveře.'
    assert game.current_room.exits['east'] is game.rooms[2]
    assert not game.objects_with_action('open')

    response = game.process_command('east')
    assert response is None
    assert game.current_room is game.rooms[2]

    response = game.process_command('down')
    assert response is None
    assert game.current_room is game.rooms[3]
    assert game.objects[3] in game.objects_in_room
    assert not game.portable_objects
    assert game.objects[5] not in game.visible_objects
    assert game.objects[3] in game.objects_with_action('open')

    response = game.process_command('open', game.objects[3])
    assert response == 'Ve skříňce jsi našel nůžky.'
    assert game.objects[5] in game.portable_objects
    assert not game.objects_with_action('open')

    response = game.process_command('examine', game.objects[5])
    assert response == 'Běžný přenosný předmět.'

    response = game.process_command('take', game.objects[5])
    assert response == 'OK'
    assert game.objects[5] not in game.objects_in_room
    assert game.objects[5].location == 'inventory'
    assert not game.portable_objects


def test_portable_container_opened_before_taken(game):
    game.process_command('open', game.objects[1])
    assert game.objects[2].location is game.current_room


def test_portable_container_opened_after_taken(game):
    game.process_command('take', game.objects[1])
    game.process_command('open', game.objects[1])
    assert game.objects[2].location == 'inventory'
