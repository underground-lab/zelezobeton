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
                    ('disable_action', dict(obj='plechovka', action='take')),
                    ('enable_action', dict(obj='klicek', action='use')),
                ],
            },
            'open': {
                'impact': [
                    ('move_to_same_location', dict(obj_1='klicek', obj_2='plechovka')),
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
                    ('disable_action', dict(obj='klicek', action='take')),
                    ('enable_action', dict(obj='klicek', action='use')),
                ],
            },
            'use': {
                'condition': [
                    ('in_inventory', dict(obj='klicek')),
                    ('in_room', dict(obj='dvere')),
                    ('action_disabled', dict(obj='dvere', action='open')),
                ],
                'impact': [
                    ('enable_action', dict(obj='dvere', action='open')),
                    ('remove_object', dict(obj='klicek')),
                ],
                'message': 'Odemkl jsi dveře.',
                'enabled': False,
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
                    ('move_to_room', dict(obj='nuzky', room='sklep')),
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
                    ('open_exit', dict(room='start', direction='east', destination='sklad')),
                    ('open_exit', dict(room='sklad', direction='west', destination='start')),
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
                    ('disable_action', dict(obj='nuzky', action='take')),
                ],
            },
        },
    },
}
