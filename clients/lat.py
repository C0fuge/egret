"""lat.py <uri> <conc> <rounds> <out.csv>: the Lat.java small-query mix through Python ADBC Flight SQL (one process per client).
Classes: meta_tables (adbc_get_objects depth=tables), meta_schemas (depth=db_schemas), point_orders, point_lineitem, limit10, limit10_ob (LIMIT 10 with ORDER BY),
count_filter, prep_point (same parameterised text every time: the dbapi cursor keeps the prepared statement)."""
import sys, time, datetime, multiprocessing as mp
import flightconn
import adbc_driver_flightsql.dbapi as d, adbc_driver_flightsql as a

import os
CLASSES = [c for c in os.environ.get("SMALL_CLASSES", "").split(",") if c] or \
    ["meta_tables", "meta_schemas", "point_orders", "point_lineitem", "limit10", "limit10_ob", "count_filter", "prep_point"]

def okey(seed):
    r = 1 + (seed * 2654435761 + 12345) % 14_999_999
    return (r // 8) * 32 + (r % 8)

def day(seed):
    return (datetime.date(1992, 1, 1) + datetime.timedelta(days=(seed * 40503) % 2400)).isoformat()

def one_round(conn, cur, pcur, tid, r, conc, out):
    seed = tid * 100_003 + r + 7
    for k in range(len(CLASSES)):
        cls = CLASSES[(k + tid) % len(CLASSES)]
        t0 = time.perf_counter(); rows = 0; val = 0.0; ok = 1
        try:
            if cls == "meta_tables":
                t = conn.adbc_get_objects(depth="tables", db_schema_filter="tpch").read_all()
                rows = sum(len(s["db_schema_tables"] or []) for c in t.to_pylist() for s in (c["catalog_db_schemas"] or []))
            elif cls == "meta_schemas":
                t = conn.adbc_get_objects(depth="db_schemas").read_all()
                rows = sum(len(c["catalog_db_schemas"] or []) for c in t.to_pylist())
            elif cls == "prep_point":
                pcur.execute("SELECT o_orderkey, o_totalprice FROM tpch.orders WHERE o_orderkey = ?", parameters=(okey(seed * 3 + 1),))
                t = pcur.fetch_arrow_table(); rows = t.num_rows; val = float(sum(x or 0 for x in t.column(1).to_pylist()))
            else:
                sql = {"point_orders": f"SELECT o_orderkey, o_custkey, o_totalprice, o_orderdate FROM tpch.orders WHERE o_orderkey = {okey(seed * 3)}",
                       "point_lineitem": f"SELECT l_orderkey, l_linenumber, l_quantity, l_extendedprice FROM tpch.lineitem WHERE l_orderkey = {okey(seed * 3 + 2)}",
                       "limit10": "SELECT l_orderkey, l_partkey, l_quantity, l_comment FROM tpch.lineitem LIMIT 10",
                       "limit10_ob": "SELECT l_orderkey, l_linenumber, l_quantity, l_comment FROM tpch.lineitem ORDER BY l_orderkey, l_linenumber LIMIT 10",
                       "count_filter": f"SELECT count(*) FROM tpch.orders WHERE o_orderdate = DATE '{day(seed)}'"}[cls]
                cur.execute(sql); t = cur.fetch_arrow_table(); rows = t.num_rows
                if cls != "limit10":
                    col = t.column(0 if t.num_columns == 1 else 2)
                    val = float(sum(float(x or 0) for x in col.to_pylist()))
        except Exception as e:
            ok = 0; print(f"{cls} t{tid} r{r}: {type(e).__name__}: {str(e)[:200]}", file=sys.stderr)
        ms = (time.perf_counter() - t0) * 1000
        if out is not None:
            out.append(f"adbc,{conc},{cls},{tid},{r},{ms:.3f},{rows},{val:.2f},{ok}")

def worker(args):
    uri, conc, rounds, tid, barrier = args
    conn = d.connect(uri, db_kwargs=flightconn.db_kwargs())
    cur = conn.cursor(); pcur = conn.cursor()
    one_round(conn, cur, pcur, tid, -1, conc, None)
    barrier.wait()
    out = []
    for r in range(rounds):
        one_round(conn, cur, pcur, tid, r, conc, out)
    cur.close(); pcur.close(); conn.close()
    return out

if __name__ == "__main__":
    uri, conc, rounds, path = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    m = mp.Manager(); barrier = m.Barrier(conc + 1)
    with mp.Pool(conc) as pool:
        res = pool.map_async(worker, [(uri, conc, rounds, t, barrier) for t in range(conc)], chunksize=1)
        barrier.wait(); t0 = time.perf_counter()
        lines = [l for part in res.get() for l in part]
        wall = time.perf_counter() - t0
    with open(path, "w") as f:
        f.write("client,conc,class,thread,round,lat_ms,rows,val,ok\n" + "\n".join(lines) + "\n")
    err = sum(1 for l in lines if l.endswith(",0"))
    print(f"adbc conc={conc} rounds={rounds} queries={len(lines)} wall={wall:.2f}s qps={len(lines)/wall:.1f} errors={err}")
