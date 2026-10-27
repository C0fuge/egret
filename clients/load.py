"""load.py <uri> <conc> <warmup_s> <duration_s> <out.csv>: closed-loop small-query load through Python ADBC Flight SQL.
<conc> clients (threads spread over up to 4 processes, one connection each) run the lat.py query mix back to back: <warmup_s>
not recorded, then <duration_s> recorded. Same CSV as lat.py; prints: adbc conc=<n> ... qps=<recorded queries / duration_s>."""
import multiprocessing as mp
import os
import sys
import threading
import time

import adbc_driver_flightsql as a
import adbc_driver_flightsql.dbapi as d

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lat import one_round  # noqa: E402


def client(uri, conc, tid, t0, warm, dur, out):
    try:
        conn = d.connect(uri, db_kwargs={a.DatabaseOptions.AUTHORIZATION_HEADER.value: "Bearer unused"})
        cur, pcur = conn.cursor(), conn.cursor()
    except Exception as e:
        print(f"connect t{tid}: {type(e).__name__}: {str(e)[:200]}", file=sys.stderr)
        out.append(f"adbc,{conc},connect,{tid},0,0,0,0,0")
        return
    r = 0
    while time.time() < t0 + warm + dur:
        one_round(conn, cur, pcur, tid, r, conc, out if time.time() >= t0 + warm else None)
        r += 1
    cur.close(); pcur.close(); conn.close()


def proc(args):
    uri, conc, tids, t0, warm, dur = args
    out = []
    ts = [threading.Thread(target=client, args=(uri, conc, t, t0, warm, dur, out)) for t in tids]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    return out


if __name__ == "__main__":
    uri, conc, warm, dur, path = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
    n = min(conc, 4)
    t0 = time.time() + 3  # common start after the processes are up
    with mp.Pool(n) as pool:
        lines = [l for part in pool.map(proc, [(uri, conc, list(range(i, conc, n)), t0, warm, dur) for i in range(n)]) for l in part]
    with open(path, "w") as f:
        f.write("client,conc,class,thread,round,lat_ms,rows,val,ok\n" + "\n".join(lines) + "\n")
    err = sum(1 for l in lines if l.endswith(",0"))
    print(f"adbc conc={conc} warmup={warm:g}s duration={dur:g}s queries={len(lines)} qps={len(lines) / dur:.1f} errors={err}")
