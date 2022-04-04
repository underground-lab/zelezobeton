# coding: utf-8

title = 'Železo, beton'

exit_keys = ('north', 'south', 'west', 'east', 'up', 'down')
exits = dict(
    zip(
        exit_keys,
        ('na sever', 'na jih', 'na západ', 'na východ', 'nahoru', 'dolů')
    )
)

commands = ('examine', 'take', 'open', 'use')
imperative = dict(zip(commands, ('prozkoumej', 'vezmi', 'otevři', 'použij')))
