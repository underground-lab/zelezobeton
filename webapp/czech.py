# coding: utf-8

title = 'Železo, beton'

exits = {
    'north': 'na sever',
    'south': 'na jih',
    'west': 'na západ',
    'east': 'na východ',
    'up': 'nahoru',
    'down': 'dolů',
}

commands = ('examine', 'take', 'open', 'use')
infinitive = dict(zip(commands, ('prozkoumat', 'vzít', 'otevřít', 'použít')))
imperative = dict(zip(commands, ('prozkoumej', 'vezmi', 'otevři', 'použij')))
