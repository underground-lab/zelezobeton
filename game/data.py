# coding: utf-8

room_data = {
    0: {
        'description': 'Popis místnosti 0.',
        'exits': {'north': 1},
        'objects': [1],
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
    1: {
        'name': 'plechovku',
        'description': 'Přenosný předmět typu krabička, batoh atd. Po jeho otevření se'
                       ' v místě tohoto předmětu objeví jeden nebo více nových'
                       ' předmětů. Následně už tento předmět nelze znova otevřít.',
        'actions': {
            'open': {
                'impact': [
                    ('add_to_same_location', dict(obj_1=1, obj_2=2)),
                    ('disable_action', dict(obj=1, action='open')),
                ],
                'message': 'V plechovce byl malý klíček.',
            },
        },
    },
    2: {
        'name': 'klíček',
        'description': 'Běžný přenosný předmět.',
    },
    3: {
        'name': 'skříňku',
        'description': 'Nepřenosný předmět typu skříň, bedna atd. Po jeho otevření se'
                       ' v místnosti objeví jeden nebo více nových předmětů.'
                       ' Následně už tento předmět nelze znova otevřít.',
        'portable': False,
        'actions': {
            'open': {
                'impact': [
                    ('add_to_room', dict(room=3, obj=5)),
                    ('disable_action', dict(obj=3, action='open')),
                ],
                'message': 'Ve skříňce jsi našel nůžky.',
            },
        },
    },
    4: {
        'name': 'dveře',
        'description': 'Nepřenosný předmět typu dveře, poklop atd. Po jeho otevření se'
                       ' objeví nový východ z místnosti. Následně už tento předmět'
                       ' nelze znova otevřít.',
        'portable': False,
        'actions': {
            'open': {
                'impact': [
                    ('open_exit', dict(room=1, direction='east', destination=2)),
                    ('open_exit', dict(room=2, direction='west', destination=1)),
                    ('disable_action', dict(obj=4, action='open')),
                ],
                'message': 'Otevřel jsi dveře.',
            },
        },
    },
    5: {
        'name': 'nůžky',
        'description': 'Běžný přenosný předmět.',
    },
}

player_data = {
    'location': 0,
    'inventory': [],
}
