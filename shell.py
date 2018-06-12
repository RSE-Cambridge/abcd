import cmd
from expr import parse_query

def frame_query(cursor):
    cursor.execute('select key, key_type from frame_keys');
    q = ['frame_id']
    for key, key_type in cursor:
        try:
            cast_type = {
                'number':'numeric',
                'string':'text',
                }[key_type]
        except KeyError:
            continue
        q.append(f'(info->>\'{key}\')::{cast_type} as {key}')
    return f'(select {", ".join(q)} from frame_raw)'


class Shell(cmd.Cmd):
    prompt = '(abcd) '

    def __init__(self, db):
        super().__init__()
        self.db = db

    def do_select(self, arg):
        with self.db as db, db.cursor() as cursor:
            cursor.execute(f'with frame as {frame_query(cursor)} {parse_query(f"select {arg}")("frame")}')
            for x in cursor:
                print('\t\t'.join(str(y) for y in x))

    def do_count(self, arg):
        with self.db as db, db.cursor() as cursor:
            cursor.execute(f'with frame as {frame_query(cursor)} {parse_query(f"count {arg}")("frame")}')
            print("%d matching frames" % cursor.fetchone()[0])


    def do_keys(self, arg):
        with self.db as db, db.cursor() as cursor:
            cursor.execute(f'''
                    select count(*), key, jsonb_typeof(info->key) as key_type
                    from (
                        select info, jsonb_object_keys(info) as key
                        from (
                            with frame as {frame_query(cursor)} {parse_query(f"select frame_id {arg}")("frame")}
                        ) as frame_filtered natural inner join frame_raw
                    ) x
                    where key=key
                    group by key, key_type
                    ''')

            print('%10s %10s %s'%('count','type','key'))
            print('----------')
            for count, key, key_type in cursor:
                print("%10d %10s %s"%(count, key_type, key))
            return None


    def do_stats(self, arg):
        with self.db as db, db.cursor() as cursor:
            cursor.execute(f'with frame as {frame_query(cursor)} {parse_query(f"stats {arg}")("frame")}')
            vmin, vmax, vavg = cursor.fetchone()
            print(f'min {vmin}')
            print(f'max {vmax}')
            print(f'avg {vavg}')

    def do_hist(self, arg):
        with self.db as db, db.cursor() as cursor:
            cursor.execute('select key_type from frame_keys where key=%s', (arg.split(' ')[0],))
            key_type = cursor.fetchone()[0]

            if key_type == 'number':
                cursor.execute(f'with frame as {frame_query(cursor)} {parse_query(f"hist_num {arg}")("frame")}')
                import numpy as np
                freqs, bins = np.histogram(np.fromiter((float(x[0]) for x in cursor.fetchall()), np.float), bins=20)
                for freq, edge in zip([int(30*f/np.max(freqs)) for f in freqs], bins):
                    print('%12.6f %s' % (edge, '*'*freq))

            elif key_type == 'string':
                cursor.execute(f'with frame as {frame_query(cursor)} {parse_query(f"hist_str {arg}")("frame")}')
                counts = {value: count for value, count in cursor}
                count_max = max(counts.values())
                for value in sorted(counts):
                    count = counts[value]
                    freq = count/count_max
                    print('%10d %40s %s' % (count, value, '*'*30*int(freq)))

            else:
                print(f'don\'t know how to plot histogram for type {key_type}')

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

