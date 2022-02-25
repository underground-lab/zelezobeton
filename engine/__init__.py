from pathlib import Path

import toml

from .classes import Game, InvalidCommand

ROOT_DIR = Path(__file__).parent.parent
__version__ = toml.load(ROOT_DIR / 'pyproject.toml')['tool']['poetry']['version']
