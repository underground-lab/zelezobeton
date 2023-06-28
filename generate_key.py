from pathlib import Path
from random import choices
from string import ascii_letters

key_path = (Path(__file__).parent / '.key')
key_path.write_text(''.join(choices(ascii_letters, k=100)), encoding='utf8')
print('Key written to', key_path)
