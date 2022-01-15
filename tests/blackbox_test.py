from game import game


def test_game():
    assert game.objects[0] in game.player.inventory
    assert game.objects[1] in game.player.inventory
    assert game.current_room is game.rooms[0]
    assert game.objects[2] in game.portable_objects

    game.process_command('take', game.objects[2])
    assert game.objects[2] in game.player.inventory
    assert not game.objects_in_room

    game.process_command('north')
    assert game.current_room is game.rooms[1]
    assert 'east' not in game.current_room.exits
    assert game.objects[4] in game.objects_in_room
    assert not game.portable_objects
    assert game.objects[4] in game.objects_with_action('open')

    game.process_command('open', game.objects[4])
    assert game.current_room.exits['east'] == 2
    assert not game.objects_in_room
    assert not game.objects_with_action('open')

    game.process_command('east')
    assert game.current_room is game.rooms[2]

    game.process_command('down')
    assert game.current_room is game.rooms[3]
    assert game.objects[3] in game.objects_in_room
    assert not game.portable_objects
    assert game.objects[5] not in game.visible_objects
    assert game.objects[3] in game.objects_with_action('open')

    game.process_command('open', game.objects[3])
    assert game.objects[5] in game.portable_objects
    assert not game.objects_with_action('open')

    game.process_command('take', game.objects[5])
    assert game.objects[5] not in game.objects_in_room
    assert game.objects[5] in game.player.inventory
    assert not game.portable_objects
