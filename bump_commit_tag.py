#!/usr/bin/env python

import subprocess
import sys

import tomllib

try:
    rule = sys.argv[1]
except IndexError:
    rule = 'patch'

# bump with poetry
subprocess.run(f'poetry version {rule}'.split())

with open('pyproject.toml', 'rb') as f:
    version = tomllib.load(f)['tool']['poetry']['version']

# commit & tag
subprocess.run(['git', 'commit', '-a', '-m', f'Bump version to {version}'])
subprocess.run(f'git tag {version}'.split())
