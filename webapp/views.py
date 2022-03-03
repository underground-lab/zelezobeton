from django.shortcuts import render

from engine import Game
from game.data import room_data, object_data


def home(request):
    session = request.session

    # retrieve stored game state or create new
    try:
        game = Game.from_json(session['game'])
    except KeyError:
        game = Game(room_data, object_data)

    # modify game state
    ...

    # store game state
    session['game'] = game.to_json()

    return render(request, 'home.html', {'game': game})
