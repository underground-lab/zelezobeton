# coding: utf-8

title = 'Železo, beton'

exit_keys = ('north', 'south', 'west', 'east', 'up', 'down')
exits = dict(
    zip(
        exit_keys,
        ('na sever', 'na jih', 'na západ', 'na východ', 'nahoru', 'dolů')
    )
)

action_keys = ('examine', 'take', 'open', 'use')
imperative = dict(
    zip(
        action_keys,
        ('prozkoumej', 'vezmi', 'otevři', 'použij')
    )
)
