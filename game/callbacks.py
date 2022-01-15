def add_to_room(room, obj):
    room.objects.append(obj)


def remove_from_room(room, obj):
    room.objects.remove(obj)


def enable_action(obj, action):
    obj.actions[action]['enabled'] = True


def disable_action(obj, action):
    obj.actions[action]['enabled'] = False
