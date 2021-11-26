import string
import sys


def main():
    for line in sys.stdin:
        line = line.replace('..', '.')
        line = line.replace('.,', ',')
        line = line.replace(" 's", "'s")
        for letter in string.ascii_lowercase:
            line = line.replace(". " + letter, ".  " + letter.upper())
        if line.startswith(', '):
            line = 'Lo' + line
        if 'gloom' in line:
            line = line.rstrip() + '  _' + line.rstrip() + '_\n'
        sys.stdout.write(line)


if __name__ == '__main__':
    # MAKE MINE A 99
    main()
