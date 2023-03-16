from importlib import import_module
from pathlib import Path


def _import_games():
    for py_file in Path(__file__).parent.glob('*.py'):
        short_name = py_file.stem
        if short_name == '__init__':
            continue
        module = import_module(f'.{short_name}', __name__)
        if all(
            hasattr(module, attr_name)
            for attr_name in (
                'title', 'exit_labels', 'room_data', 'objects'
            )
        ):
            yield short_name, module


_all_games = dict(_import_games())
game_data = _all_games['default']
