# coding: utf-8

room_data = {
    0: {
        'description': 'Popis místnosti 0.',
        'exits': {'north': 1},
        'objects': [2],
    },
    1: {
        'description': 'Popis místnosti 1.',
        'exits': {'south': 0},
        'objects': [4],
    },
    2: {
        'description': 'Popis místnosti 2.',
        'exits': {'down': 3},
    },
    3: {
        'description': 'Popis místnosti 3.',
        'exits': {'up': 2},
        'objects': [3],
    },
}

object_data = {
    0: {
        'name': 'předmět 0',
        'description': 'Popis předmětu 0.',
    },
    1: {
        'name': 'předmět 1',
        'description': 'Popis předmětu 1.',
    },
    2: {
        'name': 'předmět 2',
        'description': 'Popis předmětu 2.',
    },
    3: {
        'name': 'předmět 3',
        'description': 'Popis předmětu 3.',
        'portable': False,
        'actions': {
            'open': {
                'impact': [
                    ('add_to_room', dict(room=3, obj=5)),
                    ('disable_action', dict(obj=3, action='open')),
                ],
            },
        },
    },
    4: {
        'name': 'dveře',
        'description': 'Zavřené dveře na východ.',
        'portable': False,
        'actions': {
            'open': {
                'impact': [
                    ('open_exit', dict(room=1, direction='east', destination=2)),
                    ('open_exit', dict(room=2, direction='west', destination=1)),
                    ('remove_from_room', dict(room=1, obj=4)),
                ],
                'message': 'Otevřel jsi dveře.',
            },
        },
    },
    5: {
        'name': 'předmět 5',
        'description': 'Popis předmětu 5.',
    },
}

player_data = {
    'location': 0,
    'inventory': [0, 1],
}
