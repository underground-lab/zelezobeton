room_data = {
    0: {
        'description': 'Popis místnosti 0.',
        'exits': {'north': 1},
        'objects': [2],
    },
    1: {
        'description': 'Popis místnosti 1.',
        'exits': {'south': 0, 'east': 2},
        'objects': [],
    },
    2: {
        'description': 'Popis místnosti 2.',
        'exits': {'west': 1, 'down': 3},
        'objects': [],
    },
    3: {
        'description': 'Popis místnosti 3.',
        'exits': {'up': 2},
        'objects': [3, 4, 5],
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
    'inventory': [0, 1],
}
