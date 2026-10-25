"""TPC-H Parquet data for the screening jobs (DuckDB dbgen).

  datagen.py gen <out-root> <sf>                 -> <out-root>/tpch/<table>/*.parquet (default layout)
  datagen.py relayout <src-root> <dst-root> <l>  -> <dst-root>/tpch: lineitem and orders rewritten in layout <l>,
                                                    the other tables hard-linked from <src-root>

Default layout (same as the reference stand): 8 writer threads, tables > 1M rows one file per thread
(PER_THREAD_OUTPUT), ROW_GROUP_SIZE 122880; small tables one file.
Layouts: rg1m (ROW_GROUP_SIZE 1048576), rg32k (32768), files64m (FILE_SIZE_BYTES 64MB, many files),
onefile (one file per table).
"""
import os
import shutil
import subprocess
import sys
import time

import duckdb

TABLES = ["lineitem", "orders", "partsupp", "part", "customer", "supplier", "nation", "region"]
LAYOUTS = {
    "rg1m": "ROW_GROUP_SIZE 1048576, PER_THREAD_OUTPUT TRUE",
    "rg32k": "ROW_GROUP_SIZE 32768, PER_THREAD_OUTPUT TRUE",
    "files64m": "ROW_GROUP_SIZE 122880, FILE_SIZE_BYTES '64MB'",
    "onefile": "ROW_GROUP_SIZE 122880",
}


def connect(tmp):
    con = duckdb.connect(os.path.join(tmp, "gen.duckdb"))
    con.execute("SET threads = 8")
    con.execute(f"SET temp_directory = '{tmp}/spill'")
    return con


def count_files(d):
    return len([f for f in os.listdir(d) if f.endswith(".parquet")])


def gen(out, sf):
    tmp = out + ".tmp"
    os.makedirs(tmp, exist_ok=True)
    con = connect(tmp)
    con.execute("INSTALL tpch; LOAD tpch")
    t0 = time.time()
    con.execute(f"CALL dbgen(sf = {sf})")
    print(f"dbgen sf={sf} {time.time() - t0:.1f} s", flush=True)
    for t in TABLES:
        d = os.path.join(out, "tpch", t)
        os.makedirs(d, exist_ok=True)
        rows = con.execute(f"SELECT count(*) FROM {t}").fetchone()[0]
        t1 = time.time()
        if rows > 1_000_000:
            con.execute(f"COPY (SELECT * FROM {t}) TO '{d}' (FORMAT PARQUET, PER_THREAD_OUTPUT TRUE, ROW_GROUP_SIZE 122880, OVERWRITE_OR_IGNORE TRUE)")
        else:
            con.execute(f"COPY (SELECT * FROM {t}) TO '{d}/data_0.parquet' (FORMAT PARQUET, ROW_GROUP_SIZE 122880)")
        print(f"{t:9s} rows={rows:<10d} files={count_files(d):<3d} {time.time() - t1:.1f} s", flush=True)
    con.close()
    shutil.rmtree(tmp)


def relayout(src, dst, layout):
    opts = LAYOUTS[layout]
    os.makedirs(os.path.join(dst, "tpch"), exist_ok=True)
    tmp = dst + ".tmp"
    os.makedirs(tmp, exist_ok=True)
    con = connect(tmp)
    for t in TABLES:
        s = os.path.join(src, "tpch", t)
        d = os.path.join(dst, "tpch", t)
        if t not in ("lineitem", "orders"):
            subprocess.run(["cp", "-al", s, d], check=True)
            continue
        os.makedirs(d, exist_ok=True)
        t1 = time.time()
        # same row order as the source (file order, then row order inside each file)
        q = f"SELECT * EXCLUDE (filename, file_row_number) FROM read_parquet('{s}/*.parquet', filename = true, file_row_number = true) ORDER BY filename, file_row_number"
        target = f"{d}/data_0.parquet" if layout == "onefile" else d
        extra = "" if layout == "onefile" else ", OVERWRITE_OR_IGNORE TRUE"
        con.execute(f"COPY ({q}) TO '{target}' (FORMAT PARQUET, {opts}{extra})")
        print(f"{t:9s} layout={layout} files={count_files(d):<4d} {time.time() - t1:.1f} s", flush=True)
    con.close()
    shutil.rmtree(tmp)


if __name__ == "__main__":
    if sys.argv[1] == "gen":
        gen(sys.argv[2], float(sys.argv[3]))
    else:
        relayout(sys.argv[2], sys.argv[3], sys.argv[4])
