#!/usr/bin/env python

import sys, os
from argparse import ArgumentParser
from psycopg2 import connect

from shell import Shell

parser = ArgumentParser(description='import xyz files to database')
parser.add_argument('--db', help="database connection string", default=os.getenv("ABCD_DB", 'postgresql://localhost/abcd'))
parser.add_argument('query', help="optional query string", nargs='*')

args = parser.parse_args()

db = connect(args.db)

if args.query:
    Shell(db).onecmd(' '.join(args.query))
else:
    Shell(db).cmdloop(intro='connected to %s' % args.db)
