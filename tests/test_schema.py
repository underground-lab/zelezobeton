import json
from pathlib import Path

from jsonschema.validators import Draft202012Validator, extend
import pytest

from games import game_data

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
        (game_data.rooms, 'room_schema.json'),
        (game_data.objects, 'obj_schema.json'),
    )
)
def test_data_schema(data, schema_file):
    with (SCHEMAS_DIR / schema_file).open(encoding='utf8') as f:
        schema = json.load(f)
    validator = CustomArrayValidator(schema)
    for item in data.values():
        validator.validate(item)
