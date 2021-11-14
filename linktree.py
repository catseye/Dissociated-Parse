'''Parse sentences into trees using link-parser, then parse
link-parser's output into a Python data structure.'''

import json
import re
import subprocess
import sys


class Scanner(object):
    def __init__(self, text):
        self.text = str(text)
        self.token = None
        self.type = None
        self.all_text = text
        self.scan()

    def near_text(self, length=10):
        return self.all_text
        if len(self.text) < length:
            return self.text
        return self.text[:length]

    def scan_pattern(self, pattern, type, token_group=1, rest_group=2):
        pattern = r'^(' + pattern + r')(.*?)$'
        match = re.match(pattern, self.text, re.DOTALL)
        if not match:
            return False
        else:
            self.type = type
            self.token = match.group(token_group)
            self.text = match.group(rest_group)
            return True

    def scan(self):
        self.scan_pattern(r'[ \t\n\r]*', 'whitespace')
        if not self.text:
            self.token = None
            self.type = 'EOF'
            return
        if self.scan_pattern(r'\(|\)', 'bracket'):
            return
        if self.scan_pattern(r"[a-zA-Z_.,'{][^\s)]*", 'word'):
            return
        if self.scan_pattern(r'.', 'unknown character'):
            return
        else:
            raise AssertionError("this should never happen, self.text=(%s)" % self.text)

    def expect(self, token):
        if self.token == token:
            self.scan()
        else:
            raise SyntaxError(u"Expected '%s', but found '%s' (near '%s')" %
                              (token, self.token, self.near_text()))

    def on(self, *tokens):
        return self.token in tokens

    def on_type(self, *types):
        return self.type in types

    def check_type(self, *types):
        if not self.on_type(*types):
            raise SyntaxError(u"Expected %s, but found %s ('%s') (near '%s')" %
                              (types, self.type, self.token, self.near_text()))

    def consume(self, *tokens):
        if self.token in tokens:
            self.scan()
            return True
        else:
            return False


class Parser(object):
    def __init__(self, text):
        self.scanner = Scanner(text)

    def sexps(self):
        many = []
        while not self.scanner.on_type('EOF'):
            many.append(self.sexp())
        return many

    def sexp(self):
        if self.scanner.on_type('word'):
            t = self.scanner.token
            self.scanner.scan()
            return t
        else:
            items = []
            self.scanner.expect('(')
            while not self.scanner.on(')'):
                items.append(self.sexp())
            self.scanner.expect(')')
            return items


# ----------------------------------------------------------------------------------------------------


def clean_atom(atom):
    match = re.match(r'^\{(.*?)\}$', atom)
    if match:
        return match.group(1)
    match = re.match(r'^(.*?)(\.|\{)', atom)
    if match and match.group(1):
        return match.group(1)
    else:
        return atom


def clean_sexp(sexp):
    if isinstance(sexp, str):
        return clean_atom(sexp)
    elif isinstance(sexp, list):
        return [clean_sexp(s) for s in sexp]
    else:
        raise NotImplementedError(sexp)


def unparse(sexp):
    if isinstance(sexp, str):
        return clean_atom(sexp)
    elif isinstance(sexp, list):
        x = ' '.join([unparse(s) for s in sexp[1:]])
        return x.replace(' .', '.')
    else:
        raise NotImplementedError(sexp)


def make_tree(sentence):
    sentence = sentence.strip()

    with open('/tmp/sentence.txt', 'w') as f:
        f.write(sentence + '\n')

    result = subprocess.run(
        """link-parser -constituents=1 -graphics=0 -verbosity=0 < /tmp/sentence.txt | grep '^[( ]'""",
        shell=True,
        stdout=subprocess.PIPE,
    )
    text = result.stdout.decode('utf-8')

    p = Parser(text)
    return clean_sexp(p.sexp())


# ----------------------------------------------------------------------------------------------------


def get_subject(sexp):
    if isinstance(sexp, str):
        return None
    elif isinstance(sexp, list):
        if sexp[0] == 'S':
            return get_subject(sexp[1])
        elif sexp[0] == 'NP':
            return sexp
        else:
            return None
    else:
        return None


def get_vp(sexp):
    if isinstance(sexp, str):
        return None
    elif isinstance(sexp, list):
        if sexp[0] == 'S':
            return get_vp(sexp[2])
        elif sexp[0] == 'VP':
            return sexp
        else:
            return None
    else:
        return None


def merge_vps(subj, s1, s2):
    vp1 = get_vp(s1)
    if vp1 is None:
        raise ValueError(s1)
    vp2 = get_vp(s2)
    if vp2 is None:
        raise ValueError(s2)
    return ['S', subj, ['VP', vp1, 'and', vp2], '.']


def contains_none(sexp):
    if sexp is None:
        return True
    elif isinstance(sexp, str):
        return False
    elif isinstance(sexp, list):
        return any([contains_none(s) for s in sexp])
    else:
        raise NotImplementedError(sexp)


def depth(sexp):
    if sexp is None:
        return 0
    elif isinstance(sexp, str):
        return 1
    elif isinstance(sexp, list):
        return 1 + max([depth(s) for s in sexp])
    else:
        raise NotImplementedError(sexp)
