#!/usr/bin/env python

from pathlib import Path
from random import randint

key_path = (Path(__file__).parent / '.key')
key = bytes(randint(33, 126) for _ in range(100))

key_path.write_bytes(key)
print(f'{len(key)} bytes written to {key_path}')
