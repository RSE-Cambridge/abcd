import cmd
from abcd import ABCD

class Shell(ABCD, cmd.Cmd):
    prompt = '(abcd) '

    def __init__(self, db):
        super().__init__(db)

    def do_select(self, arg):
        print(self.select(arg))

    def do_count(self, arg):
        print(self.count(arg))

    def do_keys(self, arg):
        print(self.keys(arg).to_string(index=False))

    def do_hist(self, arg):
        d = self.hist(arg)
        for v, d in zip(d['value'], d['count']):
            print("%30s %d"%(v,d))

    def do_stats(self, arg):
        print(self.select(arg).describe())


    def do_import(self, arg):
        from import_file import import_file

        for f in arg.split():
            print(f"import {f}")
            import_file(self.db, f)


    def do_quit(self, arg):
        return True
    def do_EOF(self, arg):
        print("")
        return self.do_quit(arg)

