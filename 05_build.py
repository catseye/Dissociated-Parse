#!/usr/bin/env python3

import json
import os
import re
import sys


def render(f, tree):
    render_r(f, tree)
    f.write('\n')

def render_r(f, tree):
    if isinstance(tree, str):
        f.write(tree)
        f.write(' ')
    elif isinstance(tree, list):
        tag = tree[0]
        assert isinstance(tag, str)
        for child in tree[1:]:
            render_r(f, child)


def enter(map, tree):
    if isinstance(tree, str):
        return
    elif isinstance(tree, list):
        tag = tree[0]
        assert isinstance(tag, str)
        map.setdefault(tag, []).append(tree)
        for child in tree[1:]:
            enter(map, child)


def main():
    map = {}

    with open('data/trees.json', 'r') as f:
        data = json.loads(f.read())

    # for tree in data['trees']:
    #     render(sys.stdout, tree)

    for tree in data['trees']:
        enter(map, tree)

    with open('data/productions.json', 'w') as f:
        f.write(json.dumps(map, indent=4))

main()
