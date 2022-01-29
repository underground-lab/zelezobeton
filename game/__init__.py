from pathlib import Path

import toml

from game.classes import Room, Object, Game
from game.data import room_data, object_data

ROOT_DIR = Path(__file__).parent.parent
__version__ = toml.load(ROOT_DIR / 'pyproject.toml')['tool']['poetry']['version']

new_game = Game(room_data, object_data)
