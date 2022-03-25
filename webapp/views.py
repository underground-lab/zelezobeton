from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from engine.classes import Game
from game import labels
from game.data import room_data, object_data


def home(request):
    game = request.session.get('game')
    context = dict(game=game, labels=labels)
    return render(request, 'home.html', context)


def main(request):
    session = request.session

    # retrieve stored game state or create new
    game = session.get('game', Game(room_data, object_data))
    context = dict(game=game, labels=labels)

    # modify game state
    command = request.POST.get('command')
    context['message'] = game.process_command(*command.split()) if command else None
    context['last_command'] = request.POST.get('command_text')

    # store game state
    session['game'] = game

    return render(request, 'main.html', context)


def restart(request):
    request.session.flush()
    return HttpResponseRedirect(reverse('main'))
