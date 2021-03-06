import json
from pathlib import Path

from jsonschema.validators import Draft202012Validator, extend
import pytest

from game.data import room_data, object_data

SCHEMAS_DIR = Path(__file__).parent / 'schemas'


def is_list_or_tuple(_, instance):
    return isinstance(instance, (list, tuple))


# validator that type-checks both lists and tuples as arrays
CustomArrayValidator = extend(
    Draft202012Validator,
    type_checker=Draft202012Validator.TYPE_CHECKER.redefine('array', is_list_or_tuple)
)


@pytest.mark.parametrize(
    'data, schema_file',
    (
        (room_data, 'room_schema.json'),
        (object_data, 'obj_schema.json'),
    )
)
def test_data_schema(data, schema_file):
    with open(SCHEMAS_DIR / schema_file) as f:
        schema = json.load(f)
    validator = CustomArrayValidator(schema)
    for item in data.values():
        validator.validate(item)
