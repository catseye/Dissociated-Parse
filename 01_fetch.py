#!/usr/bin/env python3

from time import sleep
import requests
import os

WWOZ = ['https://en.wikisource.org/wiki/The_Wonderful_Wizard_of_Oz/Chapter_{}'.format(c) for c in range(1, 25)]
PAGES = '\n'.join(WWOZ)


def main():
    print('Start!')
    for url in PAGES.split():
        dest = os.path.join('download', url.replace(':', '_').replace('/', '_'))
        print(url, '-->', dest)
        if os.path.exists(dest):
            print(dest, 'already exists, skipping')
            continue
        sleep(10)
        print('Fetching...')
        r = requests.get(url)
        with open(dest, 'w') as f:
            f.write(r.text)

main()

