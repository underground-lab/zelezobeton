from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from engine.classes import Game
from game import labels
from game.data import room_data, object_data


def main(request):
    session = request.session

    # retrieve stored game state or create new
    game = session.get('game', Game(room_data, object_data))

    # modify game state
    command = request.POST.get('command')
    response = game.process_command(*command.split()) if command else None

    # store game state
    session['game'] = game

    context = dict(game=game, labels=labels, message=response)
    return render(request, 'main.html', context)


def restart(request):
    if request.method == 'POST':
        session = request.session
        session.flush()
    return HttpResponseRedirect(reverse('main'))
