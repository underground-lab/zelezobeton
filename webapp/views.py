from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from engine.classes import Game
from game.data import title, exit_labels, action_labels, room_data, object_data


def home(request):
    context = {
        'game_in_progress': request.session.get('game') is not None,
        'title': title,
    }
    return render(request, 'home.html', context)


def main(request):
    session = request.session

    # retrieve stored game state or create new
    current_game = session.get('game', Game(room_data, object_data))

    # modify game state
    command = request.POST.get('command')
    message = current_game.process_command(*command.split()) if command else None

    # store game state
    session['game'] = current_game

    context = {
        'game': current_game,
        'title': title,
        'exits': exit_labels,
        'exit_sort_key': list(exit_labels),
        'actions': action_labels,
        'message': message,
        'last_command': request.POST.get('command_text'),
    }
    return render(request, 'main.html', context)


def restart(request):
    request.session.flush()
    return HttpResponseRedirect(reverse('main'))
