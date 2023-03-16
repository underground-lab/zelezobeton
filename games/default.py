from pathlib import Path

import yaml

with (Path(__file__).parent / 'default.yaml').open(encoding='utf-8') as f:
    title, exit_labels, action_labels, rooms, objects = yaml.safe_load_all(f)
