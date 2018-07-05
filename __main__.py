#!/usr/bin/env python

import sys, os
from argparse import ArgumentParser

parser = ArgumentParser(description='import xyz files to database')
parser.add_argument('--db', help="database connection string", default=os.getenv("ABCD_DB", 'postgresql://localhost'))
parser.add_argument('query', help="optional query string", nargs='*')

args = parser.parse_args()

from .shell import Shell

if args.query:
    Shell(args.db).onecmd(' '.join(args.query))
else:
    Shell(args.db).cmdloop(intro='connected to %s' % args.db)
