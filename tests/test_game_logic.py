# coding: utf-8

import pytest

from engine.classes import InvalidCommand


def objects_with_action(game, action_key):
    return {
        obj_key: obj
        for obj_key, obj in game.visible_objects.items()
        if any(
            game._conditions_met(action)
            for action in obj.actions.get(action_key, [])
        )
    }


def test_game_walk_through(game):
    assert game.current_room is game.rooms['start']
    assert list(objects_with_action(game, 'open')) == ['dvere']

    response = game.process_command('open', 'dvere')
    assert response is game.message_ok
    assert game.current_room.exits['east'] == 'sklad'
    assert game.rooms['sklad'].exits['west'] == game.current_room_key
    assert not objects_with_action(game, 'open')

    response = game.process_command('east')
    assert response is game.message_ok
    assert game.current_room is game.rooms['sklad']

    # cannot be used before taken
    with pytest.raises(InvalidCommand):
        game.process_command('use', 'smetak')

    response = game.process_command('vezmi', 'smetak')
    assert response is game.message_ok
    assert 'smetak' in game.objects_in_inventory

    # cannot take again
    with pytest.raises(InvalidCommand):
        game.process_command('vezmi', 'smetak')

    response = game.process_command('vezmi', 'krabice')
    assert 'Jeden bude stačit' in response
    assert 'krabice' not in game.objects_in_inventory
    assert 'hrebik' in game.objects_in_inventory

    response = game.process_command('west')
    assert response is game.message_ok
    assert game.current_room is game.rooms['start']

    response = game.process_command('north')
    assert response is game.message_ok
    assert game.current_room is game.rooms['kancelar']
    assert list(objects_with_action(game, 'open')) == ['plechovka']

    response = game.process_command('open', 'plechovka')
    assert 'dvě kancelářské sponky' in response
    assert not objects_with_action(game, 'open')
    assert set(objects_with_action(game, 'vezmi')) == {'plechovka', 'sponky', 'vaza'}

    # cannot be used before taken
    with pytest.raises(InvalidCommand):
        game.process_command('use', 'sponky')

    response = game.process_command('vezmi', 'sponky')
    assert response is game.message_ok
    assert 'sponky' in game.objects_in_inventory

    # cannot take again
    with pytest.raises(InvalidCommand):
        game.process_command('vezmi', 'sponky')

    response = game.process_command('use', 'smetak')
    assert 'rozbila na kousky' in response
    assert 'vaza' not in game.visible_objects
    assert 'strepy' in objects_with_action(game, 'prozkoumej')

    # use again
    response = game.process_command('use', 'smetak')
    assert 'Nevím jak' in response

    response = game.process_command('prozkoumej', 'strepy')
    assert 'našel malý klíček' in response
    assert not objects_with_action(game, 'prozkoumej')

    # cannot be used before taken
    with pytest.raises(InvalidCommand):
        game.process_command('use', 'klicek')

    response = game.process_command('vezmi', 'klicek')
    assert response is game.message_ok
    assert 'klicek' in game.objects_in_inventory

    # cannot take again
    with pytest.raises(InvalidCommand):
        game.process_command('vezmi', 'klicek')

    response = game.process_command('vezmi', 'plechovka')
    assert response is game.message_ok
    assert 'plechovka' in game.objects_in_inventory

    # cannot take again
    with pytest.raises(InvalidCommand):
        game.process_command('vezmi', 'plechovka')

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
    assert list(objects_with_action(game, 'open')) == ['mriz']

    # use again
    response = game.process_command('use', 'sponky')
    assert 'Nevím jak' in response

    response = game.process_command('open', 'mriz')
    assert response is game.message_ok
    assert game.current_room.exits['south'] == 'vyklenek'
    assert game.rooms['vyklenek'].exits['north'] == game.current_room_key
    assert not objects_with_action(game, 'open')

    response = game.process_command('south')
    assert response is game.message_ok
    assert game.current_room is game.rooms['vyklenek']

    response = game.process_command('open', 'trezor')
    assert response == 'Je zamčený.'

    response = game.process_command('use', 'klicek')
    assert 'odemkl trezor' in response
    assert game.objects['trezor'].unlocked is True
    assert list(objects_with_action(game, 'open')) == ['trezor']

    # use again
    response = game.process_command('use', 'klicek')
    assert 'Nevím jak' in response

    response = game.process_command('open', 'trezor')
    assert 'našel obálku' in response
    assert not objects_with_action(game, 'open')

    response = game.process_command('vezmi', 'obalka')
    assert response is game.message_ok
    assert 'obalka' in game.objects_in_inventory

    # cannot take again
    with pytest.raises(InvalidCommand):
        game.process_command('vezmi', 'obalka')


def test_straightforward_walk_through(game):
    game.process_command('north')
    game.process_command('open', 'plechovka')
    game.process_command('vezmi', 'sponky')
    game.process_command('south')
    game.process_command('open', 'dvere')
    game.process_command('east')
    game.process_command('use', 'sponky')
    game.process_command('vezmi', 'smetak')
    game.process_command('west')
    game.process_command('north')
    game.process_command('use', 'smetak')
    game.process_command('prozkoumej', 'strepy')
    game.process_command('vezmi', 'klicek')
    game.process_command('south')
    game.process_command('east')
    game.process_command('open', 'mriz')
    game.process_command('south')
    game.process_command('use', 'klicek')
    game.process_command('open', 'trezor')
    game.process_command('vezmi', 'obalka')


def test_portable_container_opened_before_taken(game):
    game.process_command('north')
    game.process_command('open', 'plechovka')
    assert game.objects['sponky'].location == game.current_room_key
    game.process_command('vezmi', 'plechovka')
    assert 'sponky' in objects_with_action(game, 'vezmi')
    assert not objects_with_action(game, 'open')
    assert not objects_with_action(game, 'use')


def test_portable_container_opened_after_taken(game):
    game.process_command('north')
    game.process_command('vezmi', 'plechovka')
    game.process_command('open', 'plechovka')
    assert 'sponky' in game.objects_in_inventory
    assert 'sponky' not in objects_with_action(game, 'vezmi')
    assert not objects_with_action(game, 'open')
    assert list(objects_with_action(game, 'use')) == ['sponky']


@pytest.mark.parametrize(
    'command, obj_key',
    (
        ('prozkoumej', 'plechovka'),    # examine invisible object
        ('vezmi', 'plechovka'),    # take invisible object
        ('vezmi', 'sponky'),    # take already taken object
        ('vezmi', 'dvere'),    # take unexpected object
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


def test_available_actions(game):
    available = game.available_actions()
    assert list(available) == ['open']
    assert list(available['open']) == ['dvere']

    game.process_command('north')
    available = game.available_actions()
    assert list(available) == ['vezmi', 'open']
    assert list(available['vezmi']) == ['plechovka', 'vaza']
    assert list(available['open']) == ['plechovka']

    game.process_command('open', 'plechovka')
    available = game.available_actions()
    assert list(available) == ['vezmi']
    assert list(available['vezmi']) == ['plechovka', 'sponky', 'vaza']


def test_default_object_name(game):
    assert game.objects['trezor'].name == 'trezor'
    assert game.objects['kladivo'].name == 'kladivo'
