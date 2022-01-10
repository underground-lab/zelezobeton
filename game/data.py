from types import SimpleNamespace

texts = SimpleNamespace(
    game_title='Název hry',
    icon_char='\N{POTATO}',
    you_see='Vidíš',
    you_have='Máš u sebe',
    and_='a',
    go_north='Jdi na sever',
    go_south='Jdi na jih',
    go_west='Jdi na západ',
    go_east='Jdi na východ',
)

room_data = {
    0: {
        'description': 'Popis místnosti 0.',
        'exits': {'north': 1, 'south': 2, 'west': 3, 'east': 4},
        'objects': [],
    },
    1: {
        'description': 'Popis místnosti 1.',
        'exits': {'south': 0},
        'objects': [0, 1, 2],
    },
    2: {
        'description': 'Popis místnosti 2.',
        'exits': {'north': 0},
        'objects': [3],
    },
    3: {
        'description': 'Popis místnosti 3.',
        'exits': {'east': 0},
        'objects': [],
    },
    4: {
        'description': 'Popis místnosti 4.',
        'exits': {'west': 0},
        'objects': [],
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
    },
    4: {
        'name': 'předmět 4',
        'description': 'Popis předmětu 4.',
    },
    5: {
        'name': 'předmět 5',
        'description': 'Popis předmětu 5.',
    },
}

player_data = {
    'location': 0,
    'inventory': [4, 5],
}
