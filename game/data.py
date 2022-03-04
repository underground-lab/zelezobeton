# coding: utf-8

room_data = {
    'start': {
        'description': 'Popis místnosti „Chodba“.',
        'exits': {'north': 'kancelar'},
    },
    'kancelar': {
        'description': 'Popis místnosti „Kancelář“.',
        'exits': {'south': 'start'},
    },
    'sklad': {
        'description': 'Popis místnosti „Sklad“.',
    },
    'vyklenek': {
        'description': 'Popis místnosti „Výklenek“.',
    },
}

object_data = {

    # Předmět, který je na začátku hry v inventáři
    'mince': {
        'name': 'minci',
        'description': 'Popis předmětu „mince“.',
        'location': 'inventory',
    },

    # Předmět typu 'přenosný kontejner'
    'plechovka': {
        'name': 'plechovku',
        'description': 'Popis předmětu „plechovka“.',
        'location': 'kancelar',
        'actions': {
            'take': {
                'condition': [
                    ('in_room', dict(obj='plechovka')),
                ],
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
                    ],
                    'message': 'V plechovce jsem našel dvě kancelářské sponky.',
                },
            ],
        },
    },

    'klicek': {
        'name': 'klíček',
        'description': 'Popis předmětu „klíček“.',
        'actions': {
            'take': {
                'condition': [
                    ('in_room', dict(obj='klicek')),
                ],
                'impact': [
                    ('move_to_inventory', dict(obj='klicek')),
                ],
            },
            'use': [
                {
                    'condition': [
                        ('current_room_is', dict(room='vyklenek')),
                        ('not_true', dict(obj='trezor', attr='unlocked')),
                    ],
                    'impact': [
                        ('set_true', dict(obj='trezor', attr='unlocked')),
                    ],
                    'message': 'Klíčkem jsem odemkl trezor.',
                },
                {
                    'condition': [
                        ('in_inventory', dict(obj='klicek')),
                    ],
                    'message': 'Nevím jak.',
                },
            ],
        },
    },

    # Předmět typu 'nepřenosný kontejner'
    'trezor': {
        'name': 'trezor',
        'description': 'Popis předmětu „trezor“.',
        'location': 'vyklenek',
        'actions': {
            'open': [
                {
                    'condition': [
                        ('is_true', dict(obj='trezor', attr='unlocked')),
                        ('is_undiscovered', dict(obj='obalka')),
                    ],
                    'impact': [
                        ('move_to_current_room', dict(obj='obalka')),
                    ],
                    'message': 'V trezoru jsem našel obálku.',
                },
                {
                    'condition': [
                        ('not_true', dict(obj='trezor', attr='unlocked')),
                    ],
                    'message': 'Je zamčený.',
                },
            ],
        },
    },

    # Předmět typu 'odemčené dveře'
    'dvere': {
        'name': 'dveře',
        'description': 'Popis předmětu „dveře“.',
        'location': 'start',
        'actions': {
            'open': {
                'condition': [
                    ('exit_closed', dict(room='start', direction='east')),
                ],
                'impact': [
                    ('open_exit', dict(room='start', direction='east', room_2='sklad')),
                    ('open_exit', dict(room='sklad', direction='west', room_2='start')),
                ],
            },
        },
    },

    'sponky': {
        'name': 'sponky',
        'description': 'Popis předmětu „sponky“.',
        'actions': {
            'take': {
                'condition': [
                    ('in_room', dict(obj='sponky')),
                ],
                'impact': [
                    ('move_to_inventory', dict(obj='sponky')),
                ],
            },
            'use': [
                {
                    'condition': [
                        ('current_room_is', dict(room='sklad')),
                        ('not_true', dict(obj='mriz', attr='unlocked')),
                    ],
                    'impact': [
                        ('set_true', dict(obj='mriz', attr='unlocked')),
                    ],
                    'message': 'Pomocí kancelářských sponek jsem odemkl zámek mříže.',
                },
                {
                    'condition': [
                        ('in_inventory', dict(obj='sponky')),
                    ],
                    'message': 'Nevím jak.',
                },
            ],
        },
    },

    'obalka': {
        'name': 'obálku',
        'description': 'Popis předmětu „obálka“.',
        'actions': {
            'take': {
                'condition': [
                    ('in_room', dict(obj='obalka')),
                ],
                'impact': [
                    ('move_to_inventory', dict(obj='obalka')),
                ],
            },
        },
    },

    'smetak': {
        'name': 'smeták',
        'description': 'Popis předmětu „smeták“.',
        'location': 'sklad',
        'actions': {
            'take': {
                'condition': [
                    ('in_room', dict(obj='smetak')),
                ],
                'impact': [
                    ('move_to_inventory', dict(obj='smetak')),
                ],
            },
            'use': [
                {
                    'condition': [
                        ('current_room_is', dict(room='kancelar')),
                        ('is_visible', dict(obj='vaza')),
                    ],
                    'impact': [
                        ('move_to_current_room', dict(obj='klicek')),
                        ('remove_object', dict(obj='vaza')),
                    ],
                    'message': 'Smetl jsem vázu z knihovny a v jejích střepech jsem'
                               ' našel malý klíček.'
                },
                {
                    'condition': [
                        ('in_inventory', dict(obj='smetak')),
                    ],
                    'message': 'Nevím jak.',
                },
            ],
        },
    },

    # Předmět s nestandardní akcí vezmi/take.
    'vaza': {
        'name': 'vázu',
        'description': 'Popis předmětu „váza“.',
        'location': 'kancelar',
        'actions': {
            'take': {
                'message': 'Nedosáhnu na ni. Stojí na vysoké knihovně.',
            },
        },
    },

    # Předmět s nestandardní akcí vezmi/take.
    'krabice': {
        'name': 'krabici hřebíků',
        'description': 'Popis předmětu "krabice hřebíků".',
        'location': 'sklad',
        'actions': {
            'take': {
                'condition': [
                    ('is_undiscovered', dict(obj='hrebik')),
                ],
                'impact': [
                    ('move_to_inventory', dict(obj='hrebik')),
                ],
                'message': 'Jeden bude stačit.',
            },
        },
    },

    'hrebik': {
        'name': 'hřebík',
        'description': 'Popis předmětu „hřebík“.',
    },

    # Předmět typu 'zamčené dveře'
    'mriz': {
        'name': 'mříž',
        'description': 'Popis předmětu „mříž“.',
        'location': 'sklad',
        'actions': {
            'open': [
                {
                    'condition': [
                        ('is_true', dict(obj='mriz', attr='unlocked')),
                        ('exit_closed', dict(room='sklad', direction='south')),
                    ],
                    'impact': [
                        ('open_exit',
                         dict(room='sklad', direction='south', room_2='vyklenek')),
                        ('open_exit',
                         dict(room='vyklenek', direction='north', room_2='sklad')),
                    ],
                },
                {
                    'condition': [
                        ('not_true', dict(obj='mriz', attr='unlocked')),
                    ],
                    'message': 'Je zamčená.',
                },
            ],
        },
    },
}
