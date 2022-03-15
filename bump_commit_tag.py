#!/usr/bin/env python

import subprocess
import sys

import toml

try:
    rule = sys.argv[1]
except IndexError:
    rule = 'patch'

# bump with poetry
subprocess.run(f'poetry version {rule}', shell=True)

# write new version to VERSION
version = toml.load('pyproject.toml')['tool']['poetry']['version']
print('Updating VERSION')
with open('VERSION', 'w') as f:
    print(version, file=f)

# commit & tag
subprocess.run(f'git commit -a -m "Bump version to {version}"', shell=True)
subprocess.run(f'git tag {version}', shell=True)
