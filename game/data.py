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
    'plechovka': {
        'name': 'plechovku',
        'description': 'Přenosný předmět typu krabička, batoh atd. Po jeho otevření se'
                       ' v místě tohoto předmětu objeví jeden nebo více nových'
                       ' předmětů. Následně už tento předmět nelze znova otevřít.',
        'location': 'pracovna',
        'actions': {
            'take': {
                'impact': [
                    ('move_to_inventory', dict(obj='plechovka')),
                ],
            },
            'open': {
                'impact': [
                    ('move_to_same_location', dict(obj='klicek', obj_2='plechovka')),
                    ('disable_action', dict(obj='plechovka', action='open')),
                ],
                'message': 'V plechovce byl malý klíček.',
            },
        },
    },
    'klicek': {
        'name': 'klíček',
        'description': 'Běžný přenosný předmět.',
        'actions': {
            'take': {
                'impact': [
                    ('move_to_inventory', dict(obj='klicek')),
                ],
            },
            'use': {
                'condition': [
                    ('current_room_is', dict(room='start')),
                ],
                'impact': [
                    ('enable_action', dict(obj='dvere', action='open')),
                    ('remove_object', dict(obj='klicek')),
                ],
                'message': 'Odemkl jsi dveře.',
            },
        },
    },
    'skrinka': {
        'name': 'skříňku',
        'description': 'Nepřenosný předmět typu skříň, bedna atd. Po jeho otevření se'
                       ' v místnosti objeví jeden nebo více nových předmětů.'
                       ' Následně už tento předmět nelze znova otevřít.',
        'location': 'sklep',
        'actions': {
            'open': {
                'impact': [
                    ('move_to_current_room', dict(obj='nuzky')),
                    ('disable_action', dict(obj='skrinka', action='open')),
                ],
                'message': 'Ve skříňce jsi našel nůžky.',
            },
        },
    },
    'dvere': {
        'name': 'dveře',
        'description': 'Nepřenosný předmět typu dveře, poklop atd. Po jeho otevření se'
                       ' objeví nový východ z místnosti. Následně už tento předmět'
                       ' nelze znova otevřít.',
        'location': 'start',
        'actions': {
            'open': {
                'impact': [
                    ('open_exit', dict(room='start', direction='east', room_2='sklad')),
                    ('open_exit', dict(room='sklad', direction='west', room_2='start')),
                    ('disable_action', dict(obj='dvere', action='open')),
                ],
                'message': 'Otevřel jsi dveře.',
                'enabled': False,
            },
        },
    },
    'nuzky': {
        'name': 'nůžky',
        'description': 'Běžný přenosný předmět.',
        'actions': {
            'take': {
                'impact': [
                    ('move_to_inventory', dict(obj='nuzky')),
                ],
            },
        },
    },
}
