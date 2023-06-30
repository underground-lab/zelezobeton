from django.shortcuts import render, redirect

from engine.classes import Game
from games import game_data


def home(request):
    context = {
        'game_in_progress': request.session.get('game') is not None,
        'title': game_data.title,
    }
    return render(request, 'home.html', context)


def main(request):
    session = request.session

    # retrieve stored game state or create new
    current_game = session.get('game') or Game(game_data.rooms, game_data.objects)

    # modify game state
    command = request.POST.get('command')
    message = current_game.process_command(*command.split()) if command else None

    # store game state
    session['game'] = current_game

    context = {
        'game': current_game,
        'title': game_data.title,
        'exits': game_data.exit_labels,
        'exit_sort_key': list(game_data.exit_labels),
        'actions': game_data.action_labels,
        'message': message,
        'last_command': request.POST.get('command_text'),
    }
    return render(request, 'main.html', context)


def restart(request):
    request.session.flush()
    return redirect('main')
