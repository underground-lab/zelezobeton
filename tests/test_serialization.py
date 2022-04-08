def test_dumps_room(serializer, dummy_room, dummy_room_json):
    assert serializer.dumps(dummy_room).decode() == dummy_room_json


def test_dumps_object(serializer, dummy_object, dummy_object_json):
    assert serializer.dumps(dummy_object).decode() == dummy_object_json


def test_dumps_object_with_additional_attr(serializer, dummy_obj_with_attr, dummy_obj_with_attr_json):
    assert serializer.dumps(dummy_obj_with_attr).decode() == dummy_obj_with_attr_json


def test_dumps_action(serializer, dummy_action, dummy_action_json):
    assert serializer.dumps(dummy_action).decode() == dummy_action_json


def test_dumps_game(serializer, dummy_game, dummy_game_json):
    assert serializer.dumps(dummy_game).decode() == dummy_game_json


def test_loads_room(serializer, dummy_room_json, dummy_room):
    assert serializer.loads(dummy_room_json.encode()) == dummy_room


def test_loads_object(serializer, dummy_object_json, dummy_object):
    decoded = serializer.loads(dummy_object_json.encode())
    assert type(decoded) is type(dummy_object)
    assert vars(decoded) == vars(dummy_object)


def test_loads_object_with_additional_attr(serializer, dummy_obj_with_attr_json, dummy_obj_with_attr):
    decoded = serializer.loads(dummy_obj_with_attr_json.encode())
    assert type(decoded) is type(dummy_obj_with_attr)
    assert vars(decoded) == vars(dummy_obj_with_attr)


def test_loads_action(serializer, dummy_action_json, dummy_action):
    assert serializer.loads(dummy_action_json.encode()) == dummy_action


def test_loads_game(serializer, dummy_game_json, dummy_game):
    decoded = serializer.loads(dummy_game_json.encode())
    assert type(decoded) is type(dummy_game)
    decoded_obj = decoded.objects.pop('b')
    dummy_obj = dummy_game.objects.pop('b')
    assert vars(decoded) == vars(dummy_game)
    assert type(decoded_obj) is type(dummy_obj)
    assert vars(decoded_obj) == vars(dummy_obj)


def test_roundtrip_no_error(serializer, game):
    serializer.loads(serializer.dumps(game))
