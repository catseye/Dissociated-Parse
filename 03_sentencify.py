#!/usr/bin/env python3

import json
import os
import re


def main():
    freq = {}

    with open('data/all-paragraphs.json', 'r') as f:
        data = json.loads(f.read())

    sentences = []
    for n, para in enumerate(data['paragraphs']):
        sentence = []
        in_quotes = False
        for m, word in enumerate(para):
            sentence.append(word)
            if word in ('"'):
                in_quotes = not in_quotes
            elif word in ('.', '!') and not in_quotes:
                sentences.append(sentence)
                sentence = []
        if sentence:
            sentences.append(sentence)

    new_data = {
        'sentences': sentences,
    }

    with open('data/all-sentences.json', 'w') as f:
        f.write(json.dumps(new_data, indent=4))

main()
