"""Data and local reference answers for the HDFS acceptance check (accept-hdfs.yml).

  data.py <in-dir>

Writes <in>/data/tpch/<table>/*.parquet (TPC-H SF1, DuckDB dbgen; lineitem in 12 files, orders in 4,
the rest one file each) and <in>/data/far/part_far/{0,1,2}.parquet (part in three files; the
cluster script puts file 0 only on a DataNode without a server so that the FIRST file of a table
the queries do not touch is on another node). The HDFS schemas (tpch, spread) are laid out from
these files by ci/accept/cluster.sh. Then <in>/expected.json: every check query of ci/accept/queries.py
answered by in-process DuckDB over the same local files, as normalised digests (ci/accept/digest.py).
This is a second reference: the primary one is the same build on DataNodes without data-transfer
protection; a 0-row answer where DuckDB has rows is a silent wrong answer either way.
"""
import json
import os
import sys

import duckdb

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import digest  # noqa: E402
import queries  # noqa: E402

SPLIT = {"lineitem": 12, "orders": 4}


def main(base):
    data = os.path.join(base, "data")
    con = duckdb.connect()
    con.execute("SET threads = 4")
    con.execute("INSTALL tpch; LOAD tpch; CALL dbgen(sf = 1)")
    tables = [r[0] for r in con.execute("SHOW TABLES").fetchall()]
    for t in tables:
        d = os.path.join(data, "tpch", t)
        os.makedirs(d, exist_ok=True)
        parts = SPLIT.get(t, 1)
        key = {"lineitem": "l_orderkey", "orders": "o_orderkey"}.get(t)
        for i in range(parts):
            where = f"WHERE {key} % {parts} = {i}" if parts > 1 else ""
            con.execute(f"COPY (SELECT * FROM {t} {where}) TO '{d}/part-{i:02d}.parquet' (FORMAT PARQUET, ROW_GROUP_SIZE 122880)")
        print(t, con.execute(f"SELECT count(*) FROM {t}").fetchone()[0], "rows,", parts, "file(s)", flush=True)
    far = os.path.join(data, "far", "part_far")
    os.makedirs(far, exist_ok=True)
    for i in range(3):
        con.execute(f"COPY (SELECT * FROM part WHERE p_partkey % 3 = {i}) TO '{far}/{i}.parquet' (FORMAT PARQUET)")
    # local views with the HDFS names: tpch.<t>, spread.lineitem_sp / orders_sp / part_far, plain names too
    ref = duckdb.connect()
    ref.execute("CREATE SCHEMA tpch; CREATE SCHEMA spread")
    for t in tables:
        src = f"read_parquet('{data}/tpch/{t}/*.parquet')"
        ref.execute(f"CREATE VIEW tpch.{t} AS SELECT * FROM {src}")
        ref.execute(f"CREATE VIEW main.{t} AS SELECT * FROM {src}")
    for name, t in (("lineitem_sp", "lineitem"), ("orders_sp", "orders")):
        ref.execute(f"CREATE VIEW spread.{name} AS SELECT * FROM read_parquet('{data}/tpch/{t}/*.parquet')")
        ref.execute(f"CREATE VIEW main.{name} AS SELECT * FROM spread.{name}")
    ref.execute(f"CREATE VIEW spread.part_far AS SELECT * FROM read_parquet('{far}/*.parquet')")
    ref.execute("CREATE VIEW main.part_far AS SELECT * FROM spread.part_far")
    expected = {}
    for q in queries.all_queries():
        tab = ref.execute(q.sql).fetch_arrow_table()
        expected[q.id] = digest.digest(tab, q.ordered)
    with open(os.path.join(base, "expected.json"), "w") as f:
        json.dump(expected, f, indent=1, sort_keys=True)
    print(len(expected), "expected answers", flush=True)


if __name__ == "__main__":
    main(sys.argv[1])
