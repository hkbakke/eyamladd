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

    pip3 install -r requirements.txt
    gem install hiera-eyaml

## Debian

    apt install hiera-eyaml python3-ruamel.yaml

# Installation

    cp eyamladd.py /usr/local/bin/eyamladd

# Usage
By default eyamladd only outputs the resulting merged file to stdout. Add the
`--write` argument to actually update the target file. The update is performed
atomically.

    # Consume cleartext properties from stdin from other scripts, encrypt the
    # leaf values and merge into target.eyaml.
    # This is only an example, do not put cleartext secrets directly on the
    # command line!
    printf '{"passphrase": "secret_stuff"}' | eyamladd \
        --eyaml-public-key eyaml-public-key.asc \
        --filename target.eyaml \
        --stdin

    # Read cleartext properties from file instead of stdin
    eyamladd \
        --eyaml-public-key eyaml-public-key.asc \
        --filename target.eyaml \
        --json-file cleartext.json
