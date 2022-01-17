def add_to_room(game, room, obj):
    game.rooms[room].objects.append(game.objects[obj])


def remove_from_room(game, room, obj):
    game.rooms[room].objects.remove(game.objects[obj])




def enable_action(game, obj, action):
    game.objects[obj].actions[action]['enabled'] = True


def disable_action(game, obj, action):
    game.objects[obj].actions[action]['enabled'] = False


def open_exit(game, room, direction, destination):
    game.rooms[room].exits[direction] = game.rooms[destination]


def close_exit(game, room, direction):
    if direction in game.rooms[room].exits:
        del game.rooms[room].exits[direction]
