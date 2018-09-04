from .expr import parse_query

class ABCD:
    def __init__(self, db, verbose=False):
        super().__init__()
        from psycopg2 import connect
        self.db = connect(db)
        self.verbose = verbose

    def frame_query(self):
        with self.db.cursor() as cursor:
            cursor.execute('select key, key_type from frame_keys')
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


    def q_exec(self, sql, *args):
        self.verbose and self.q_explain(sql, *args)
        with self.db, self.db.cursor() as cursor:
            cursor.execute(sql, args)

    def q_single(self, sql, *args):
        self.verbose and self.q_explain(sql, *args)
        with self.db.cursor() as cursor:
            cursor.execute(sql, args)
            return cursor.fetchone()[0]

    def q_table(self, sql, *args):
        self.verbose and self.q_explain(sql)
        import pandas.io.sql as sqlio
        return sqlio.read_sql_query(sql, self.db, params=args)

    def q_explain(self, sql, *args):
        from inspect import cleandoc
        print('--------------- QUERY --------------- ')
        print(cleandoc(sql))
        print('---------------  PLAN --------------- ')
        v = self.verbose
        self.verbose = False
        for i in self.q_table('explain ' + sql, *args)['QUERY PLAN']:
            print(i)
        self.verbose = v


    def typeof(self, col):
        return self.q_single('''
            select key_type from frame_keys where key=%s
        ''', col)

    def count(self, q=''):
        return self.q_single(f'''
            with frame as ({self.frame_query()})
            {parse_query(f"count {q}")("frame")}
        ''')


    def keys(self, q=''):
        return self.q_table(f'''
            select count(*), key, jsonb_typeof(info->key) as key_type
            from (
                select info, jsonb_object_keys(info) as key
                from (
                    with frame as
                        {self.frame_query()}
                        {parse_query(f"select frame_id {q}")("frame")}
                ) as frame_filtered natural inner join frame_raw
            ) x
            where key=key
            group by key, key_type
        ''').sort_values('key')


    def select(self, q):
        return self.q_table(f'''
            with frame as ({self.frame_query()})
            {parse_query(f"select {q}")("frame")}
        ''')


    def hist(self, q):
        return getattr(self, f'hist_{self.typeof(q.split(" ")[0])}')(q)

    def hist_number(self, q):
        from numpy import histogram, max
        from pandas import DataFrame
        count, bin = histogram(self.q_table(f'''
            with frame as ({self.frame_query()})
            {parse_query(f"hist_num {q}")("frame")}
        '''), bins=20)
        return DataFrame(data=dict(
            count=count,
            freq=count/max(count),
            value=bin[:-1],
        ))

    def hist_string(self, q):
        return self.q_table(f'''
            with frame as ({self.frame_query()})
           {parse_query(f"hist_str {q}")("frame")}
        ''')


    def read(self, filename):
        from numpy import ndarray
        from psycopg2.extras import execute_batch, Json
        from ase.io import read

        def info(frame):
            frame_info = frame.info.copy()
            frame_info['total_energy'] = frame.get_total_energy()

            return {
                k:Json({
                    kk:(vv.tolist() if isinstance(vv, ndarray) else vv)
                    for kk,vv in v.items() 
                })
                for k,v in {'info': frame_info, 'atom': frame.arrays}.items() 
            }

        frames = [info(f) for f in read(filename, ':')]
        with self.db, self.db.cursor() as cursor:
            execute_batch(cursor, "insert into frame_raw (info, atom) values (%(info)s, %(atom)s)",
                    frames, page_size=500)
        return len(frames)

    def write(self, filename, q):
        from ase import Atoms
        from ase.io import write
        from numpy import asarray

        frames = []
        for index, frame in self.q_table(f'''
            select info, atom from frame_raw where frame_id in (
                with frame as ({self.frame_query()})
                {parse_query(f"select frame_id")("frame")}
            )
        ''').iterrows():
            a = Atoms(numbers=frame.atom['numbers'], positions=frame.atom['positions'])
            a.info = {k:v for k, v in frame.info.items() if k != "total_energy"}
            for k, v in frame.atom.items():
                if k == 'positions':
                    continue
                if k == 'numbers':
                    continue
                a.new_array(k, asarray(v))
            frames.append(a)

        write(filename, frames)

    def set(self, key, value, q):
        return self.q_exec('''
            update frame_raw set info = jsonb_set(info, '{%s}', '%s', true) where frame_id in (
                with frame as (%s) %s
            )
        '''%(key, value, self.frame_query(), parse_query(f"select frame_id {q}")("frame"))) 

    def delete(self, q):
        return self.q_exec(f'''
            delete from frame_raw where frame_id in (
                with frame as ({self.frame_query()})
                {parse_query(f"select frame_id {q}")("frame")}
            )
        ''')
