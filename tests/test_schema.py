import json
from pathlib import Path

from jsonschema.validators import Draft202012Validator, extend

from game.data import room_data, object_data

SCHEMAS_DIR = Path(__file__).parent / 'schemas'


def is_list_or_tuple(_, instance):
    return isinstance(instance, (list, tuple))


# validator that type-checks both lists and tuples as arrays
CustomArrayValidator = extend(
    Draft202012Validator,
    type_checker=Draft202012Validator.TYPE_CHECKER.redefine('array', is_list_or_tuple)
)


def test_room_data_schema():
    with open(SCHEMAS_DIR / 'room_schema.json') as f:
        schema = json.load(f)
    validator = CustomArrayValidator(schema)
    for room in room_data.values():
        validator.validate(room)


def test_object_data_schema():
    with open(SCHEMAS_DIR / 'obj_schema.json') as f:
        schema = json.load(f)
    validator = CustomArrayValidator(schema)
    for obj in object_data.values():
        validator.validate(obj)
