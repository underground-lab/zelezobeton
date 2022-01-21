def move_to_room(game, obj, room):
    game.objects[obj].location = game.rooms[room]


def remove_object(game, obj):
    game.objects[obj].location = None


def move_to_same_location(game, obj_1, obj_2):
    game.objects[obj_1].location = game.objects[obj_2].location


def enable_action(game, obj, action):
    game.objects[obj].actions[action]['enabled'] = True


def disable_action(game, obj, action):
    game.objects[obj].actions[action]['enabled'] = False


def open_exit(game, room, direction, destination):
    game.rooms[room].exits[direction] = game.rooms[destination]


def close_exit(game, room, direction):
    exits = game.rooms[room].exits
    if direction in exits:
        del exits[direction]
