#!/usr/bin/env python3

import json
import os
import re
import sys
import subprocess
from tqdm import tqdm

from linktree import make_tree


def main():
    freq = {}

    with open('data/all-sentences.json', 'r') as f:
        data = json.loads(f.read())

    sentences = []
    for n, sent in tqdm(enumerate(data['sentences'])):
        s = ''
        last_word = None
        for word in sent:
            s += ' '
            s += word
            #sys.stdout.write(' ')
            #sys.stdout.write(word)
            last_word = word
        sentences.append(s)
        #sys.stdout.write('\n\n')

    trees = []
    for s in tqdm(sentences):

        if '"' in s:
            continue
        if ';' in s:
            continue
        if ':' in s:
            continue
        if '—' in s:
            continue
        if '!' in s:
            continue
        if 'beautifully' in s:
            continue

        tree = make_tree(s)
        trees.append(tree)

    with open('data/trees.json', 'w') as f:
        f.write(json.dumps({
            'trees': trees
        }, indent=4))

main()
