import json

from .classes import Room, Object, Action, Game

SUPPORTED_CLASSES = (Room, Object, Action, Game)


class GameJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, SUPPORTED_CLASSES):
            return {'_class': obj.__class__.__name__, '_vars': vars(obj)}
        return super().default(obj)


encoder = GameJSONEncoder(ensure_ascii=False)


def custom_class_hook(obj):
    if '_class' not in obj or '_vars' not in obj:
        return obj
    cls = globals()[obj['_class']]
    if cls not in SUPPORTED_CLASSES:
        return obj
    return cls(**obj['_vars'])


decoder = json.JSONDecoder(object_hook=custom_class_hook)


class GameJSONSerializer:
    """Custom JSON serializer to be used by Django session backend."""
    def dumps(self, data):
        return encoder.encode(data).encode()

    def loads(self, data):
        return decoder.decode(data.decode())
