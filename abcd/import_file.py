import numpy as np

from psycopg2.extras import execute_batch, Json
from ase.io import read

def info(frame):
    frame_info = frame.info.copy()
    frame_info['total_energy'] = frame.get_total_energy()

    return {k:Json({kk:(vv.tolist() if isinstance(vv, np.ndarray) else vv) for kk,vv in v.items() })
        for k,v in {'info': frame_info, 'atom': frame.arrays}.items()}

def import_file(db, filename):
    frames = [info(frame) for frame in read(filename, ':')]
    print(len(frames))
    with db:
        execute_batch(db.cursor(), "insert into frame_raw (info) values (%(info)s)", frames, page_size=500)
