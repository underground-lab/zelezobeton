from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from engine.classes import Game
from game.data import room_data, object_data
from . import czech


def home(request):
    session = request.session

    # retrieve stored game state or create new
    game = session.get('game', Game(room_data, object_data))

    # modify game state
    command = request.POST.get('command')
    response = game.process_command(*command.split()) if command else None

    # store game state
    session['game'] = game

    context = dict(game=game, labels=czech, message=response)
    return render(request, 'home.html', context)


def restart(request):
    if request.method == 'POST':
        session = request.session
        session.flush()
    return HttpResponseRedirect(reverse('home'))
