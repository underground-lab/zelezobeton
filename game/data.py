# coding: utf-8

room_data = {
    'start': {
        'description': 'Popis místnosti "Chodba".',
        'exits': {'north': 'kancelar'},
    },
    'kancelar': {
        'description': 'Popis místnosti "Kancelář".',
        'exits': {'south': 'start'},
    },
    'sklad': {
        'description': 'Popis místnosti "Sklad".',
    },
    'vyklenek': {
        'description': 'Popis místnosti "Výklenek".',
    },
}

object_data = {

    # Předmět, který je na začátku hry v inventáři
    'mince': {
        'name': 'minci',
        'description': 'Popis předmětu "mince".',
        'location': 'inventory',
   },

    # Přenosný předmět typu krabička, batoh atd. Po jeho otevření se
    # v místě tohoto předmětu objeví jeden nebo více nových předmětů.
    # Následně už nelze otevřít.
    'plechovka': {
        'name': 'plechovku',
        'description': 'Popis předmětu "plechovka".',
        'location': 'kancelar',
        'actions': {
            'take': {
                'impact': [
                    ('move_to_inventory', dict(obj='plechovka')),
                ],
            },
            'open': [
                {
                    'condition': [
                        ('in_room', dict(obj='plechovka')),
                        ('is_undiscovered', dict(obj='sponky')),
                    ],
                    'impact': [
                        ('move_to_current_room', dict(obj='sponky')),
                        ('disable_action', dict(obj='plechovka', action='open')),
                    ],
                    'message': 'V plechovce jsou jen dvě kancelářské sponky.',
                },
                {
                    'condition': [
                        ('in_inventory', dict(obj='plechovka')),
                        ('is_undiscovered', dict(obj='sponky')),
                    ],
                    'impact': [
                        ('move_to_inventory', dict(obj='sponky')),
                        ('disable_action', dict(obj='plechovka', action='open')),
                    ],
                    'message': 'V plechovce jsem našel dvě kancelářské sponky.',
                },
            ],
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
                    ('current_room_is', dict(room='vyklenek')),
                ],
                'impact': [
                    ('enable_action', dict(obj='trezor', action='open')),
                    ('remove_object', dict(obj='klicek')),
                ],
                'message': 'Klíčkem jsem odemkl trezor.',
            },
        },
    },

    # Nepřenosný předmět typu skříň, bedna atd. Po jeho otevření se
    # v místnosti objeví jeden nebo více nových předmětů. Následně už
    # nelze otevřít.
    'trezor': {
        'name': 'trezor',
        'description': 'Popis předmětu "trezor".',
        'location': 'vyklenek',
        'actions': {
            'open': {
                'condition': [
                    ('is_gone', dict(obj='klicek')),
                    ('is_undiscovered', dict(obj='obalka')),
                ],
                'impact': [
                    ('move_to_current_room', dict(obj='obalka')),
                    ('disable_action', dict(obj='trezor', action='open')),
                ],
                'message': 'V trezoru jsem našel obálku.',
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
            },
        },
    },

    'sponky': {
        'name': 'sponky',
        'description': 'Popis předmětu "sponky".',
        'actions': {
            'take': {
                'impact': [
                    ('move_to_inventory', dict(obj='sponky')),
                ],
            },
            'use': [
                {
                    'condition': [
                        ('current_room_is', dict(room='sklad')),
                    ],
                    'impact': [
                        ('remove_object', dict(obj='sponky')),
                        ('enable_action', dict(obj='mriz', action='open')),
                    ],
                    'message': 'Pomocí kancelářských sponek jsem odemkl zámek mříže.',
                },
                {
                    'message': 'Nevím jak.',
                },
            ],
        },
    },

    'obalka': {
        'name': 'obálku',
        'description': 'Popis předmětu "obálka".',
        'actions': {
            'take': {
                'impact': [
                    ('move_to_inventory', dict(obj='obalka')),
                ],
            },
        },
    },

    'smetak': {
        'name': 'smeták',
        'description': 'Popis předmětu "smeták".',
        'location': 'sklad',
        'actions': {
            'take': {
                'impact': [
                    ('move_to_inventory', dict(obj='smetak')),
                ],
            },
            'use': {
                'condition': [
                    ('current_room_is', dict(room='kancelar')),
                    ('is_visible', dict(obj='vaza')),
                ],
                'impact': [
                    ('move_to_current_room', dict(obj='klicek')),
                    ('remove_object', dict(obj='vaza')),
                    ('disable_action', dict(obj='smetak', action='use')),
                ],
                'message': 'Smetl jsem vázu z knihovny a v jejích střepech jsem našel'
                           ' malý klíček.'
            },
        },
    },

    # Předmět s nestandardní akcí 'take'.
    'vaza': {
        'name': 'vázu',
        'description': 'Popis předmětu "váza".',
        'location': 'kancelar',
        'actions': {
            'take': {
                'message': 'Nedosáhnu na ni. Stojí na vysoké knihovně.',
            },
        },
    },

    # Další předmět typu dveře.
    'mriz': {
        'name': 'mříž',
        'description': 'Popis předmětu "mříž".',
        'location': 'sklad',
        'actions': {
            'open': {
                'condition': [
                    ('is_gone', dict(obj='sponky')),
                ],
                'impact': [
                    ('open_exit', dict(room='sklad', direction='south', room_2='vyklenek')),
                    ('open_exit', dict(room='vyklenek', direction='north', room_2='sklad')),
                    ('disable_action', dict(obj='mriz', action='open')),
                ],
                'enabled': False,
            },
        },
    },
}
