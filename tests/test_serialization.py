# coding: utf-8

from engine.classes import Room, Object, Action, game_encoder, game_decoder


def test_encode_room(game):
    room = game.rooms['start']
    assert game_encoder.encode(room) == (
        '{"_class": "Room", "_kwargs": {"description": "Popis místnosti \\"Chodba\\".",'
        ' "exits": {"north": "kancelar"}}}'
    )


def test_encode_action(game):
    action = game.objects['klicek'].actions['take'][0]
    assert game_encoder.encode(action) == (
        '{"_class": "Action", "_kwargs": {"condition": [["in_room", {"obj": "klicek"}]'
        '], "impact": [["move_to_inventory", {"obj": "klicek"}]], "message": null}}'
    )


def test_encode_object(game):
    obj = game.objects['dvere']
    encoded = game_encoder.encode(obj)
    assert encoded.startswith('{"_class": "Object", "_kwargs": {"')
    assert '"open": [{"_class": "Action", "_kwargs": {"' in encoded


def test_encode_game(game):
    encoded = game.to_json()
    assert encoded.startswith('{"room_data": {"start": {"_class": "Room", "_kwargs": {"')
    assert '"klicek": {"_class": "Object", "_kwargs": {"' in encoded
    assert '"use": [{"_class": "Action", "_kwargs": {"' in encoded


def test_decode_room():
    assert game_decoder.decode(
        '{"_class": "Room", "_kwargs": {"description": "a", "exits": {"north": "b"}}}'
    ) == Room('a', {'north': 'b'})


def test_decode_action():
    assert game_decoder.decode(
        '{"_class": "Action", "_kwargs": {"condition": [["a", {"b": "c"}]],'
        ' "impact": [["d", {"e": "f"}]], "message": "OK"}}'
    ) == Action([['a', {'b': 'c'}]], [['d', {'e': 'f'}]], 'OK')


def test_decode_object():
    assert game_decoder.decode(
        '{"_class": "Object", "_kwargs": {"name": "a", "description": "b",'
        ' "location": "c", "actions": {"use": [{"_class": "Action", "_kwargs": {}}]}}}'
    ) == Object('a', 'b', 'c', {'use': [Action()]})


def test_roundtrip_no_error(game):
    game.from_json(game.to_json())
