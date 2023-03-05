#!/usr/bin/env python

import subprocess
import sys

import toml

try:
    rule = sys.argv[1]
except IndexError:
    rule = 'patch'

# bump with poetry
subprocess.run(f'poetry version {rule}'.split())

# write new version to VERSION
version = toml.load('pyproject.toml')['tool']['poetry']['version']
print('Updating VERSION')
with open('VERSION', 'w', encoding='utf-8') as f:
    print(version, file=f)

# commit & tag
subprocess.run(['git', 'commit', '-a', '-m', f'Bump version to {version}'])
subprocess.run(f'git tag {version}'.split())
