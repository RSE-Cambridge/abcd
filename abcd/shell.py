import cmd
from .ABCD import ABCD

class Shell(ABCD, cmd.Cmd):
    prompt = '(abcd) '

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error = False

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


    def do_read(self, arg):
        for f in arg.split():
            print(f"read {f}", self.read(f))

    def do_tag(self, arg):
        tag, *rest = arg.split()
        self.tag(tag, ' '.join(rest))

    def do_delete(self, arg):
        self.delete(arg)

    def default(self, arg):
        super().default(arg)
        self.error = True

    def onecmd(self, arg):
        super().onecmd(arg)
        return self.error


    def do_quit(self, arg):
        return True
    def do_EOF(self, arg):
        print("")
        return self.do_quit(arg)

