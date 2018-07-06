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
        self.verbose and self.q_explain(sql)
        with self.db.cursor() as cursor:
            cursor.execute(sql, *args)

    def q_single(self, sql, *args):
        self.verbose and self.q_explain(sql)
        with self.db.cursor() as cursor:
            cursor.execute(sql, args)
            return cursor.fetchone()[0]

    def q_table(self, sql):
        self.verbose and self.q_explain(sql)
        import pandas.io.sql as sqlio
        return sqlio.read_sql_query(sql, self.db)

    def q_explain(self, sql, *args):
        from inspect import cleandoc
        print('--------------- QUERY --------------- ')
        print(cleandoc(sql))
        print('---------------  PLAN --------------- ')
        v = self.verbose
        self.verbose = False
        for i in self.q_table('explain ' + sql)['QUERY PLAN']:
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


    def delete(self, q):
        return self.q_exec(f'''
            delete from frame_raw where frame_id in (
                with frame as ({self.frame_query()})
                {parse_query(f"select frame_id {q}")("frame")}
            )
        ''')
