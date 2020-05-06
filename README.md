# Description
eyamladd makes it easier to selectively add one or more eyaml encrypted
properties to both existing and new yaml/eyaml files without having to manually
edit them with `eyaml edit`. Its main purpose is to be used by other scripts.
It works by taking the data you want to encrypt as json input, which eyamladd
then recursively iterates over and eyaml encrypts every leaf node. The
new encrypted properties are then merged into the target yaml-compatible file.
It does this without needing the private key as it only touches the properties
provided in the input data.

# Requirements
## Using pip and gem

    pip3 install -r requirements.txt --user
    gem install hiera-eyaml

## Debian

    pip3 install -r requirements.txt --user
    apt install hiera-eyaml

# Installation

    cp eyamladd.py /usr/local/bin/eyamladd

# Usage
By default eyamladd only outputs the resulting merged file to stdout. Add the
`--write` argument to actually update the target file. The update is performed
atomically. Note thate these are only examples. Do not put cleartext secrets
directly on the command line!

    # Consume cleartext properties from stdin, encrypt the leaf values and
    # merge into target.eyaml.
    printf '{"passphrase": "secret_stuff"}' | eyamladd \
        --eyaml-public-key eyaml-public-key.asc \
        --filename target.eyaml \
        --stdin

    # Same as above, but without merging into a file. Useful if all you want to
    # do is encrypt the input.
    printf '{"passphrase": "secret_stuff"}' | eyamladd \
        --eyaml-public-key eyaml-public-key.asc \
        --stdin

    # Read cleartext properties from file instead of stdin
    eyamladd \
        --eyaml-public-key eyaml-public-key.asc \
        --filename target.eyaml \
        --json-file cleartext.json

# Tests

    # Use a venv or install with --user
    pip3 install -r test-requirements.txt --upgrade
    PYTHONPATH=src/ pytest --cov=eyamladd -vv
