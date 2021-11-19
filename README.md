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

You'll need Python 3 (I used the version that ships with Ubuntu 20.04,
which is Python 3.8.10) and the `link-parser` executable installed.

Sources for `link-parser` can be found on GitHub:
[opencog/link-grammar](https://github.com/opencog/link-grammar).  I built
it from source.  YMMV.

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
    ./06_traverse.py
