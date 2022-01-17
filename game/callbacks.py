def add_to_room(game, room, obj):
    game.objects[obj].location = game.rooms[room]


def remove_object(game, obj):
    game.objects[obj].location = None

def add_to_same_location(game, obj_1, obj_2):
    if game.objects[obj_1].location is game.current_room:
        game.objects[obj_2].location = game.current_room
    else:
        game.objects[obj_2].location = 'inventory'



def enable_action(game, obj, action):
    game.objects[obj].actions[action]['enabled'] = True


def disable_action(game, obj, action):
    game.objects[obj].actions[action]['enabled'] = False


def open_exit(game, room, direction, destination):
    game.rooms[room].exits[direction] = game.rooms[destination]


def close_exit(game, room, direction):
    if direction in game.rooms[room].exits:
        del game.rooms[room].exits[direction]
