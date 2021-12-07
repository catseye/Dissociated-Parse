Dissociated Parse
-----------------

A submission for NaNoGenMo 2021 (Issue [#62][]).

It's well known that Markov chains don't understand grammar; any sequences
in the output that might look grammatical are only there because
grammatical-looking sequences are statistically likely.

This is an experimental variation on a Markov generator that _does_ retain
some of the syntactic structure of the original text.

Turns out we can run the Dissociated Press algorithm, not just on a list
of words like usual, but on a forest of parse trees.  I call this variation
**Dissociated Parse**.

For more information on the technique, see
[the algorithm section](#the-algorithm) below.

A 50,277-word novel generated using this technique can be found here:
[The Lion, the Witches, and the Weird Road](generated/The%20Lion,%20the%20Witches,%20and%20the%20Weird%20Road.md).

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
    t-rext out.md > out2.md
    python3 cleanup.py out2.md > 'Your Novel.md'
    pandoc --from=markdown --to=html5 <'Your Novel.md' >'Your Novel.html'
    firefox 'Your Novel.html'

## The algorithm

For background, a description of the Dissociated Press algorithm.

Just as there is more than one algorithm for sorting, there is more than
one algorithm for generating a Markov chain.

The usual algorithm involves analyzing the source text and building
a weighted transition table, then finding a random (but likely) path
through this table.

The probably less well-known algorithm called Dissociated Press goes
like this:

1. load all the words into a list in memory
2. select some word as the starting word
3. print the current word
4. find all occurrences of the current word in the text
5. select one of those occurrences at random and jump to it
6. move to the next word in the text
7. repeat from step 3

Even though this works rather differently from the transition table
algorithm, it produces the same result.  (Exercise for the reader:
convince yourself that it does in fact produce the same result.)

One downside of this algorithm is that it requires the entire text
be kept in memory, rather than just a transition table.  But, this
is also an upside, in the sense that variations on the algorithm can
exploit structure in the text which would not be retained in
the transition table.

Dissociated Parse adapts this to work recursively on parse trees.
Consider a parse tree to consist of a word, a part-of-speech tag,
and zero or more child trees.  Here is a sketch of the algorithm:

    traverse(tree):
        1. find all trees that have the same part-of-speech tag and first word as the current tree
        2. select one of those trees at random and use that tree as the current tree
        3. print the word of the current tree
        4. for each child of the current tree, traverse(child)

## Related work

A previous experiment in adding structure to Markov chains, also during NaNoGenMo, was
[Anne of Green Garbles][], which showed that one can combine two Markov models
to obtain a third model where the generation can switch between discrete states
(like "in narration" and "in dialogue").

[#62]: https://github.com/NaNoGenMo/2021/issues/62
[Anne of Green Garbles]: https://github.com/catseye/NaNoGenMo-Entries-2019/tree/master/Anne%20of%20Green%20Garbles#readme
