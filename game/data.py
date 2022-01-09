from types import SimpleNamespace

texts = SimpleNamespace(
    go_north='Jdi na sever',
    go_south='Jdi na jih',
    go_west='Jdi na západ',
    go_east='Jdi na východ',
)

room_data = {
    0: {
        'description': 'Popis místnosti 0.',
        'exits': {'north': 1, 'south': 2, 'west': 3, 'east': 4},
    },
    1: {
        'description': 'Popis místnosti 1.',
        'exits': {'south': 0},
    },
    2: {
        'description': 'Popis místnosti 2.',
        'exits': {'north': 0},
    },
    3: {
        'description': 'Popis místnosti 3.',
        'exits': {'east': 0},
    },
    4: {
        'description': 'Popis místnosti 4.',
        'exits': {'west': 0},
    },
}

player_data = {
    'location': 0,
}
