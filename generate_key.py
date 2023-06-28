import secrets
from pathlib import Path

key_path = Path(__file__).parent / '.key'
key_path.write_text(secrets.token_hex(), encoding='utf8')
print('Key written to', key_path)
