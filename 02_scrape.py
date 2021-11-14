#!/usr/bin/env python3

import json
import os
import re
import sys

from bs4 import BeautifulSoup


def scannerate(text):
    pos = 0
    tokens = []
    done = False

    patterns = [
        (r'(\s+)',      'whitespace'),
        ('([\\w\'-]+)', 'word'),
        ('(.)',         'any character'),
    ]
    while pos < len(text):
        for (pattern, pattype) in patterns:
            regexp = re.compile(pattern, flags=re.DOTALL)
            match = regexp.match(text, pos=pos)
            if match:
                token = match.group(1)
                if pattype not in ('whitespace',):
                    tokens.append(token)
                pos += len(token)
                break
    return tokens


def main(args):
    paras = []

    for filename in args:
        with open(filename, 'r') as f:
            text = f.read()
        soup = BeautifulSoup(text, features="html.parser")
        for para in soup.find_all('p'):
            para_text = para.text.replace('--', '—')
            paras.append(scannerate(para_text))

    data = {
        'paragraphs': paras,
    }
    with open('data/all-paragraphs.json', 'w') as f:
        f.write(json.dumps(data, indent=4))

if __name__ == '__main__':
    main(sys.argv[1:])
