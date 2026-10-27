"""tpch_adbc.py <uri> <queries-dir> <reps> <out-dir>: TPC-H (any *.sql set) through Python ADBC Flight SQL.

<uri> grpc://host:port, or duckdb:<data-root> for the reference answers (in-process DuckDB, views tpch.<table> over
<data-root>/tpch/<table>/*.parquet, same timing and normalisation). Per query: <reps> runs (first = cold), wall time of
execute + fetch of the whole Arrow result, row count, checksum (rows normalised as in FlightTpch.java: non-integer
numbers to 10 significant digits, sorted). Writes <out-dir>/<query>.tsv and <out-dir>/summary.tsv:
query, status, rows, checksum, cold_s, min_s, median_s (same columns as FlightTpch.java).
"""
import datetime
import decimal
import glob
import hashlib
import os
import sys
import time

TABLES = ["lineitem", "orders", "partsupp", "part", "customer", "supplier", "nation", "region"]


def norm(v):
    if v is None:
        return "NULL"
    if isinstance(v, bool):
        return str(v).lower()
    if isinstance(v, int):
        return str(v)
    if isinstance(v, (float, decimal.Decimal)):
        return f"{float(v):.10g}"
    if isinstance(v, (datetime.date, datetime.datetime)):
        return v.isoformat()
    return str(v)


def rows_of(t):
    cols = [c.to_pylist() for c in t.columns]
    return ["\t".join(norm(c[i]) for c in cols) for i in range(t.num_rows)]


def connect(uri):
    if uri.startswith("duckdb:"):
        import duckdb
        con = duckdb.connect()
        con.execute("CREATE SCHEMA tpch")
        for t in TABLES:
            con.execute(f"CREATE VIEW tpch.{t} AS SELECT * FROM read_parquet('{uri[7:]}/tpch/{t}/*.parquet')")
        return con, lambda sql: con.execute(sql).fetch_arrow_table()
    import flightconn
    import adbc_driver_flightsql as a
    import adbc_driver_flightsql.dbapi as d
    con = d.connect(uri, db_kwargs=flightconn.db_kwargs())

    def run(sql):
        with con.cursor() as cur:
            cur.execute(sql)
            return cur.fetch_arrow_table()
    return con, run


def main():
    uri, qdir, reps, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
    os.makedirs(out, exist_ok=True)
    con, run = connect(uri)
    summary = ["query\tstatus\trows\tchecksum\tcold_s\tmin_s\tmedian_s"]
    for q in sorted(glob.glob(os.path.join(qdir, "*.sql"))):
        name = os.path.basename(q)[:-4]
        sql = open(q).read().strip().rstrip(";")
        times, rows = [], None
        try:
            for _ in range(reps):
                t0 = time.perf_counter()
                t = run(sql)
                times.append(time.perf_counter() - t0)
                if rows is None:
                    rows = rows_of(t)
        except Exception as e:
            open(os.path.join(out, name + ".error"), "w").write(f"{type(e).__name__}: {e}\n")
            print(f"{name:6s} FAIL   {str(e).splitlines()[0][:200] if str(e) else type(e).__name__}", flush=True)
            summary.append(f"{name}\tFAIL\t\t\t\t\t")
            continue
        open(os.path.join(out, name + ".tsv"), "w").write("\n".join(rows) + "\n")
        chk = hashlib.sha256("\n".join(sorted(rows)).encode()).hexdigest()[:12]
        warm = sorted(times[1:] or times)
        line = f"{name}\tok\t{len(rows)}\t{chk}\t{times[0]:.3f}\t{warm[0]:.3f}\t{warm[len(warm) // 2]:.3f}"
        print(line, flush=True)
        summary.append(line)
    con.close()
    open(os.path.join(out, "summary.tsv"), "w").write("\n".join(summary) + "\n")


if __name__ == "__main__":
    main()
