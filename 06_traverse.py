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

        # key each tree by its part of speech plus the first word (only) of its content.
        words = []
        for child in tree:
            if isinstance(child, str):
                words.append(child)
        key = '-'.join(words[:2])

        # HERE ARE THE KEYS TO
        # ENTER INTO MU-MU
        # FAR FROM THE TRIBES OF THE JAMS:
        tree = random.choice(productions[key])

        for child in tree[1:]:
            render_r(f, productions, child)


def main():
    map = {}

    with open('data/productions.json', 'r') as f:
        productions = json.loads(f.read())

    for c in range(1, 37):
        sys.stdout.write('# Chapter {}\n\n'.format(c))
        for i in range(100):
            tree = random.choice(productions['S'])
            render(sys.stdout, productions, tree)

main()
