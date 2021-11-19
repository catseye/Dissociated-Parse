Dissociated Parse
-----------------

A submission for NaNoGenMo 2021 ([#62][]).

[#62]: https://github.com/NaNoGenMo/2021/issues/62

It's well known that Markov chains don't understand grammar; any sequences
in the output that might look grammatical are only there because
grammatical-looking sequences are statistically likely.

This is an experimental variation on a Markov generator that _does_ retain
some of the syntactic structure of the original text.

Turns out we can run the Dissociated Press algorithm, not just on a list
of words like usual, but on a forest of parse trees.  I call this variation
**Dissociated Parse**.

## To run

To replicate what's been generated here, you'll need to have installed:

*   Python 3.  (I used the version that ships with Ubuntu 20.04,
    which is Python 3.8.10.)
*   The `link-parser` executable.  Sources can be found on GitHub:
    [opencog/link-grammar](https://github.com/opencog/link-grammar).
    I built it from source.  YMMV.
*   `t-rext`.  The latest version runs only under Python 2.7.  I ran
    it from a Docker container: https://hub.docker.com/r/catseye/t-rext
*   `pandoc`.  This was just to make the HTML version from the generated
    Markdown.  I installed it using `apt`.

After you have the executables, you can:

    virtualenv --python=python3.8 venv
    source venv/bin/activate
    pip install -r requirements.txt

    mkdir -p download data
    ./01_fetch.py
    ./02_scrape.py download/*
    ./03_sentencify.py
    ./04_parse.py                # this one will take a while
    ./05_build.py
    ./06_traverse.py 'Give your Novel a Title Here' >out.md
    wc -w out.md
    t-rext out.md > 'Your Novel.md'
    pandoc --from=markdown --to=html5 <'Your Novel.md' >'Your Novel.html'
    firefox 'Your Novel.html'
