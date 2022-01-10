from game.data import texts


def listing(strings):
    if not strings:
        return
    if len(strings) == 1:
        return strings[0]
    return f'{", ".join(strings[:-1])} {texts.and_} {strings[-1]}'
