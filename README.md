To run
------

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

