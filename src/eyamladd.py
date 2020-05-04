#!/usr/bin/env python3

import argparse
import json
import logging
import subprocess
import sys
from collections import abc
from copy import copy, deepcopy
from pathlib import Path
from tempfile import NamedTemporaryFile

from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import FoldedScalarString


LOGGER = logging.getLogger()
EYAML_BIN = 'eyaml'


def parse_eyaml_block(block):
    """
    This ugly mess is to get ruamel.yaml to handle the block output from
    eyaml as proper folded style block scalars. By doing it this way we can
    freely use the return value from this function in yaml files without
    thinking about formatting when dumping back to the eyaml file.

    Basically the following is happening:

     1. Remove superfluous spaces and line breaks in every line of the output
     2. Join the lines using the BEL (\a) character, which is the way ruamel
        yaml represents block folds in the FoldedScalarString object
     3. Ensure the last line has a newline to avoid the block being
        represented as block style with the block chomping indicator set (>-).
     4. Then ensure that blob of text is a FoldedScalarString

    It is also possible to just return a long string instead of a folded
    style block scalar, but it is much less readable when the strings are
    getting long.
    """
    lines = [line.strip() for line in block.splitlines()]
    return FoldedScalarString('{}\n'.format('\a\n'.join(lines)))

def encrypt(content, public_key):
    cmd = [
        EYAML_BIN,
        'encrypt',
        '--string', content,
        '--pkcs7-public-key', public_key,
        '--output', 'block',
        ]

    p = subprocess.run(cmd, check=True, capture_output=True, universal_newlines=True)
    LOGGER.debug('Eyaml command output:\n%s', p.stdout)
    return parse_eyaml_block(p.stdout)

def encrypt_all(data, public_key):
    """
    The input must be a dictionary. All leaf nodes will be eyaml encrypted.
    """
    def iter_dict(data):
        for key, value in data.items():
            if isinstance(value, abc.Mapping):
                yield key, dict(iter_dict(value))
            elif isinstance(value, list):
                yield key, list(iter_list(value))
            else:
                yield key, encrypt(value, public_key)

    def iter_list(items):
        for i in items:
            if isinstance(i, abc.Mapping):
                yield dict(iter_dict(i))
            elif isinstance(i, list):
                yield list(iter_list(i))
            else:
                yield encrypt(i, public_key)

    yield from iter_dict(data)

def merge(dst, src):
    for k, v in src.items():
        if isinstance(v, list):
            if k not in dst:
                dst[k] = deepcopy(v)
            else:
                dst[k].extend(v)
        elif isinstance(v, abc.Mapping):
            if k not in dst:
                dst[k] = deepcopy(v)
            else:
                merge(dst[k], v)
        elif isinstance(v, set):
            if k not in dst:
                dst[k] = v.copy()
            else:
                dst[k].update(v.copy())
        else:
            dst[k] = copy(v)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-k', '--eyaml-public-key', metavar='PUBKEY',
                        required=True, help='eyaml public key')
    parser.add_argument('-f', '--filename', metavar='FILENAME', required=True,
                        help='yaml file to merge eyaml data into')
    parser.add_argument('-w', '--write', action='store_true',
                        help='update file instead of printing to stdout')
    parser.add_argument('-s', '--with-document-start', action='store_true',
                        help='add document start indicator (---)')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-', '--stdin', action='store_true',
                       help='read clear text data from stdin')
    group.add_argument('-j', '--json-file', metavar='FILENAME',
                       help='read clear text data from json file')
    args = parser.parse_args()

    # Set up logging
    if args.verbose:
        log_level = 'DEBUG'
    else:
        log_level = 'INFO'

    LOGGER.setLevel(log_level)
    console = logging.StreamHandler()
    LOGGER.addHandler(console)

    eyaml_public_key = Path(args.eyaml_public_key)
    LOGGER.debug('Eyaml public key: %s', eyaml_public_key)

    filename = Path(args.filename)
    LOGGER.debug('Input file: %s', filename)

    yaml = YAML()
    try:
        with open(filename, 'r') as f:
            content = yaml.load(f)
    except FileNotFoundError:
        content = {}

    if args.stdin:
        in_data = json.load(sys.stdin)
    elif args.json_file:
        with open(args.json_file, 'r') as f:
            in_data = json.load(f)
    else:
        LOGGER.error('No input data source')
        return 1

    in_data_enc = dict(encrypt_all(in_data, eyaml_public_key))

    LOGGER.debug('Original content:\n%s', json.dumps(content, indent=2))
    LOGGER.debug('In data:\n%s', json.dumps(in_data, indent=2))
    LOGGER.debug('In data encrypted:\n%s', json.dumps(in_data_enc, indent=2))

    merged = deepcopy(content)
    merge(merged, in_data_enc)

    if args.with_document_start:
        yaml.explicit_start = True

    yaml.dump(merged, sys.stdout)

    if args.write:
        print("Writing changes to '{}'".format(filename))
        with NamedTemporaryFile(dir=filename.parent, prefix='%s.' % filename.name, delete=False) as f:
            yaml.dump(merged, f)
            Path(f.name).rename(filename)


if __name__ == '__main__':
    sys.exit(main())
