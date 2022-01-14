from game import game


def test_game():
    assert game.objects[0] in game.player.inventory
    assert game.current_room is game.rooms[0]
    assert game.objects[2] in game.objects_in_room
    assert game.objects[2] in game.portable_objects

    game.process_command('take', game.objects[2])
    assert game.objects[2] not in game.objects_in_room
    assert game.objects[2] in game.player.inventory
    assert not game.objects_in_room

    game.process_command('north')
    assert game.current_room is game.rooms[1]
    game.process_command('east')
    assert game.current_room is game.rooms[2]

    game.process_command('down')
    assert game.current_room is game.rooms[3]
    assert game.objects[3] in game.objects_in_room
    assert game.objects[4] in game.objects_in_room
    assert game.objects[3] not in game.portable_objects
    assert game.objects[4] in game.portable_objects

    game.process_command('take', game.objects[4])
    assert game.objects[4] not in game.objects_in_room
    assert game.objects[4] in game.player.inventory
