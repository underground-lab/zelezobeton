# coding: utf-8

room_data = {
    'start': {
        'description': 'Popis místnosti "Chodba".',
        'exits': {'north': 'pracovna'},
    },
    'pracovna': {
        'description': 'Popis místnosti "Pracovna".',
        'exits': {'south': 'start'},
    },
    'sklad': {
        'description': 'Popis místnosti "Sklad".',
        'exits': {'down': 'sklep'},
    },
    'sklep': {
        'description': 'Popis místnosti "Sklep".',
        'exits': {'up': 'sklad'},
    },
    'inventory': {},
}

object_data = {
    # Přenosný předmět typu krabička, batoh atd. Po jeho otevření se
    # v místě tohoto předmětu objeví jeden nebo více nových předmětů.
    # Následně už nelze otevřít.
    'plechovka': {
        'name': 'plechovku',
        'description': 'Popis předmětu "plechovka".',
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
        'description': 'Popis předmětu "klíček".',
        'actions': {
            'take': {
                'impact': [
                    ('move_to_inventory', dict(obj='klicek')),
                ],
            },
            'use': {
                'condition': [
                    ('current_room_is', dict(room='sklep')),
                ],
                'impact': [
                    ('enable_action', dict(obj='trezor', action='open')),
                    ('remove_object', dict(obj='klicek')),
                ],
                'message': 'Odemkl jsem trezor.',
            },
        },
    },

    # Nepřenosný předmět typu skříň, bedna atd. Po jeho otevření se
    # v místnosti objeví jeden nebo více nových předmětů. Následně už
    # nelze otevřít.
    'trezor': {
        'name': 'trezor',
        'description': 'Popis předmětu "trezor".',
        'location': 'sklep',
        'actions': {
            'open': {
                'impact': [
                    ('move_to_current_room', dict(obj='nuzky')),
                    ('disable_action', dict(obj='trezor', action='open')),
                ],
                'message': 'V trezoru jsem našel nůžky.',
                'enabled': False,
            },
        },
    },

    # Nepřenosný předmět typu dveře, poklop atd. Po jeho otevření se
    # objeví nový východ z místnosti. Následně už nelze otevřít.
    'dvere': {
        'name': 'dveře',
        'description': 'Popis předmětu "dveře".',
        'location': 'start',
        'actions': {
            'open': {
                'impact': [
                    ('open_exit', dict(room='start', direction='east', room_2='sklad')),
                    ('open_exit', dict(room='sklad', direction='west', room_2='start')),
                    ('disable_action', dict(obj='dvere', action='open')),
                ],
                'message': 'Otevřel jsem dveře.',
            },
        },
    },
    'nuzky': {
        'name': 'nůžky',
        'description': 'Popis předmětu "nůžky".',
        'actions': {
            'take': {
                'impact': [
                    ('move_to_inventory', dict(obj='nuzky')),
                ],
            },
        },
    },
}
