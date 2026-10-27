"""scan_adbc.py <uri> <sql>: full export of one query result through Python ADBC Flight SQL, batch by batch (nothing kept).
Prints: adbcscan wall=<s> rows=<n> batches=<n> mb=<Arrow buffer MB> rows_per_s=<n> mb_per_s=<x> errors=<0|1>."""
import sys
import time

import adbc_driver_flightsql as a
import adbc_driver_flightsql.dbapi as d

uri, sql = sys.argv[1], sys.argv[2]
rows = batches = nbytes = err = 0
t0 = time.perf_counter()
try:
    con = d.connect(uri, db_kwargs={a.DatabaseOptions.AUTHORIZATION_HEADER.value: "Bearer unused"})
    with con.cursor() as cur:
        cur.execute(sql)
        for b in cur.fetch_record_batch():
            rows += b.num_rows
            batches += 1
            nbytes += b.nbytes
    con.close()
except Exception as e:
    err = 1
    print(f"{type(e).__name__}: {str(e)[:300]}", file=sys.stderr)
wall = time.perf_counter() - t0
mb = nbytes / 1e6
print(f"adbcscan wall={wall:.2f} rows={rows} batches={batches} mb={mb:.0f} rows_per_s={rows / wall:.0f} mb_per_s={mb / wall:.1f} errors={err}")
