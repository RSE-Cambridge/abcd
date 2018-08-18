from sys import exit
from os import getenv
from argparse import ArgumentParser
from abcd import Shell

def main():
    parser = ArgumentParser(description='import xyz files to database')
    parser.add_argument('--db', help="database connection string", default=getenv("ABCD_DB", 'postgresql://localhost'))
    parser.add_argument('-v', help="verbose- print info about database interactions", action="store_true")
    parser.add_argument('query', help="optional query string", nargs='*')

    args = parser.parse_args()


    if args.query:
        return Shell(args.db, args.v).onecmd(' '.join(args.query))
    else:
        return Shell(args.db, args.v).cmdloop(intro='connected to %s' % args.db)

if __name__ == '__main__':
    exit(main())
