from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from engine import Game
from game.data import room_data, object_data
from . import exits_czech


def home(request):
    session = request.session

    # retrieve stored game state or create new
    try:
        game = Game.from_json(session['game'])
    except KeyError:
        game = Game(room_data, object_data)

    # modify game state
    command = request.POST.get('command')
    response = game.process_command(command) if command else None

    # store game state
    session['game'] = game.to_json()

    context = dict(
        game=game,
        in_room_names=[obj.name for obj in game.objects_in_room.values()],
        in_inventory_names=[obj.name for obj in game.objects_in_inventory.values()],
        exits_czech=exits_czech,
        message=response
    )
    return render(request, 'home.html', context)


def restart(request):
    if request.method == 'POST':
        session = request.session
        session.flush()
    return HttpResponseRedirect(reverse('home'))
