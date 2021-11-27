import string
import sys


def main():
    for line in sys.stdin:
        line = line.replace('..', '.')
        line = line.replace('.,', ',')
        line = line.replace(" 's", "'s")
        line = line.replace('..', '.')
        for letter in string.ascii_lowercase:
            line = line.replace(". " + letter, ".  " + letter.upper())
        if line.startswith(', '):
            line = 'Lo' + line
        if 'gloom' in line:
            line = line.rstrip()
            line2 = line.replace('gloomy', 'cheesy')
            line2 = line2.replace('gloom', 'cheese')
            line = line + '  _' + line2 + '_\n'
        sys.stdout.write(line)


if __name__ == '__main__':
    # Brak, I beg to disagree; CHEESE LOG is the log for me!
    main()
