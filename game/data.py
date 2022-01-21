# coding: utf-8

room_data = {
    'start': {
        'description': 'Popis místnosti 0.',
        'exits': {'north': 'pracovna'},
    },
    'pracovna': {
        'description': 'Popis místnosti 1.',
        'exits': {'south': 'start'},
    },
    'sklad': {
        'description': 'Popis místnosti 2.',
        'exits': {'down': 'sklep'},
    },
    'sklep': {
        'description': 'Popis místnosti 3.',
        'exits': {'up': 'sklad'},
    },
    'inventory': {},
}

object_data = {
    1: {
        'name': 'plechovku',
        'description': 'Přenosný předmět typu krabička, batoh atd. Po jeho otevření se'
                       ' v místě tohoto předmětu objeví jeden nebo více nových'
                       ' předmětů. Následně už tento předmět nelze znova otevřít.',
        'location': 'pracovna',
        'actions': {
            'open': {
                'impact': [
                    ('move_to_same_location', dict(obj_1=2, obj_2=1)),
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
        'location': 'sklep',
        'portable': False,
        'actions': {
            'open': {
                'impact': [
                    ('move_to_room', dict(obj=5, room='sklep')),
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
        'location': 'start',
        'portable': False,
        'actions': {
            'open': {
                'impact': [
                    ('open_exit', dict(room='start', direction='east', destination='sklad')),
                    ('open_exit', dict(room='sklad', direction='west', destination='start')),
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
