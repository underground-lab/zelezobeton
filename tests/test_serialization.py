# coding: utf-8

from engine.classes import Room, Object, Action


def test_dumps_room(game, serializer):
    room = game.rooms['start']
    assert serializer.dumps(room) == (
        '{"_class": "Room", "_vars": {"description": "Popis místnosti „Chodba“.",'
        ' "exits": {"north": "kancelar"}}}'
    ).encode()


def test_dumps_action(game, serializer):
    action = game.objects['klicek'].actions['take'][0]
    assert serializer.dumps(action) == (
        b'{"_class": "Action", "_vars": {"condition": [["in_room", {"obj": "klicek"}]'
        b'], "impact": [["move_to_inventory", {"obj": "klicek"}]], "message": null}}'
    )


def test_dumps_object(game, serializer):
    obj = game.objects['dvere']
    encoded = serializer.dumps(obj)
    assert encoded.startswith(b'{"_class": "Object", "_vars": {"')
    assert b'"open": [{"_class": "Action", "_vars": {"' in encoded


def test_dumps_object_with_additional_attribute(game, serializer):
    obj = game.objects['mriz']
    obj.unlocked = True
    encoded = serializer.dumps(obj)
    assert encoded.startswith(b'{"_class": "Object", "_vars": {"')
    assert b'"unlocked": true' in encoded


def test_dumps_game(game, serializer):
    encoded = serializer.dumps(game)
    assert encoded.startswith(b'{"_class": "Game", "_vars": {"')
    assert b'"start": {"_class": "Room", "_vars": {"' in encoded
    assert b'"klicek": {"_class": "Object", "_vars": {"' in encoded
    assert b'"use": [{"_class": "Action", "_vars": {"' in encoded


def test_loads_room(serializer):
    assert serializer.loads(
        b'{"_class": "Room", "_vars": {"description": "a",'
        b' "exits": {"north": "b"}}}'
    ) == Room('a', {'north': 'b'})


def test_loads_action(serializer):
    assert serializer.loads(
        b'{"_class": "Action", "_vars": {"condition": [["a", {"b": "c"}]],'
        b' "impact": [["d", {"e": "f"}]], "message": "OK"}}'
    ) == Action([['a', {'b': 'c'}]], [['d', {'e': 'f'}]], 'OK')


def test_loads_object(serializer):
    assert serializer.loads(
        b'{"_class": "Object", "_vars": {"name": "a",'
        b' "location": "b", "actions": {"use": [{"_class": "Action",'
        b' "_vars": {}}]}}}'
    ) == Object('a', 'b', {'use': [Action()]})


def test_loads_object_with_additional_attribute(serializer):
    decoded = serializer.loads(
        b'{"_class": "Object", "_vars": {"name": "a", "description": "b",'
        b' "location": "c", "actions": {}, "unlocked": true}}'
    )
    assert decoded.unlocked is True


def test_roundtrip_no_error(game, serializer):
    serializer.loads(serializer.dumps(game))
