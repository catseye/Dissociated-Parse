#!/usr/bin/env python3

import json
import os
import re
import sys
import random


def render(f, productions, tree):
    render_r(f, productions, tree)
    f.write('.\n\n')

def render_r(f, productions, tree):
    if isinstance(tree, str):
        f.write(tree)
        f.write(' ')
    elif isinstance(tree, list):
        tag = tree[0]
        assert isinstance(tag, str)

        # HERE ARE THE KEYS TO
        # ENTER INTO MU-MU
        # FAR FROM THE TRIBES OF THE JAMS:
        if random.randint(1, 4) < 4:
            tree = random.choice(productions[tag])
        assert tree[0] == tag

        for child in tree[1:]:
            render_r(f, productions, child)


def main():
    map = {}

    with open('data/productions.json', 'r') as f:
        productions = json.loads(f.read())

    for i in range(100):
        tree = random.choice(productions['S'])
        render(sys.stdout, productions, tree)

main()
