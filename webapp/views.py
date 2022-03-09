from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from engine import Game
from game.data import room_data, object_data
from . import czech


def home(request):
    session = request.session

    # retrieve stored game state or create new
    try:
        game = Game.from_json(session['game'])
    except KeyError:
        game = Game(room_data, object_data)

    # modify game state
    command = request.POST.get('command')
    response = game.process_command(*command.split()) if command else None

    # store game state
    session['game'] = game.to_json()

    context = dict(
        game=game,
        labels=czech,
        commands=[
            cmd for cmd in ('take', 'open', 'use')
            if game.objects_with_action(cmd)
        ],
        message=response
    )
    return render(request, 'home.html', context)


def select_object(request):
    session = request.session
    command = request.POST.get('command')

    game = Game.from_json(session['game'])
    objects = game.objects_with_action(command)

    context = dict(
        command=command,
        objects=objects,
        labels=czech
    )
    return render(request, 'select_object.html', context)


def restart(request):
    if request.method == 'POST':
        session = request.session
        session.flush()
    return HttpResponseRedirect(reverse('home'))
