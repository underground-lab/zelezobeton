from jsonschema import validate
from jsonschema.validators import Draft202012Validator, extend

from game.data import room_data, object_data


def is_list_or_tuple(_, instance):
    return isinstance(instance, (list, tuple))


ValidatorWithTupleSupport = extend(
    Draft202012Validator,
    type_checker=Draft202012Validator.TYPE_CHECKER.redefine('array', is_list_or_tuple)
)


def test_room_data_schema():
    schema = {
        '$schema': 'https://json-schema.org/draft/2020-12/schema',
        'type': 'object',
        'properties': {
            'description': {'type': 'string'},
            'exits': {
                'type': 'object',
                'patternProperties': {
                    '^(north|south|west|east|up|down)$': {'enum': list(room_data)},
                },
                'additionalProperties': False,
            },
        },
        'additionalProperties': False,
    }
    for room in room_data.values():
        validate(room, schema=schema)


def test_object_data_schema():
    callbacks_schema = {
        'type': 'array',
        'items': {
            'type': 'array',
            'prefixItems': [
                # callback name
                {'type': 'string'},
                # kwargs
                {
                    'type': 'object',
                    'patternProperties': {
                        '^(room|room_2|obj|obj_2|action|direction)$': {'type': 'string'},
                    },
                    'minProperties': 1,
                    'additionalProperties': False,
                },
            ],
            'items': False,    # no additional items
            'minItems': 2,
        },
        'minItems': 1,
        'uniqueItems': True,
    }
    actions_schema = {
        'type': 'object',
        'properties': {
            'condition': callbacks_schema,
            'impact': callbacks_schema,
            'message': {'type': 'string'},
            'enabled': {'type': 'boolean'},
        },
        'additionalProperties': False,
    }
    schema = {
        '$schema': 'https://json-schema.org/draft/2020-12/schema',
        'type': 'object',
        'properties': {
            'name': {'type': 'string'},
            'description': {'type': 'string'},
            'location': {'type': 'string'},
            'actions': {
                'type': 'object',
                'patternProperties': {
                    '^(take|open|use)$': actions_schema,
                },
                'minProperties': 1,
                'additionalProperties': False,
            },
        },
        'required': ['name', 'description'],
        'additionalProperties': False,
    }
    validator = ValidatorWithTupleSupport(schema)
    for obj in object_data.values():
        validator.validate(obj)
