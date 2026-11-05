"""Normalised digests of query answers (ci/accept): row count, an order-insensitive hash and, for
queries with ORDER BY, an ordered hash, plus the first rows for the report.

Numbers (decimal, float) are compared at 9 significant digits (CAST to DOUBLE, printf %.9g): the
same build may sum in another order on another node; everything else as text. NULL is '\\N'.
"""
import hashlib

import duckdb
import pyarrow as pa

NUMERIC = ("DECIMAL", "DOUBLE", "FLOAT", "REAL")


def _expr(name, dtype):
    col = '"' + name.replace('"', '""') + '"'
    if dtype.upper().startswith(NUMERIC):
        return f"coalesce(printf('%.9g', CAST({col} AS DOUBLE)), '\\N')"
    return f"coalesce(CAST({col} AS VARCHAR), '\\N')"


def digest(table: pa.Table, ordered: bool, keep: int = 3) -> dict:
    """Digest of one answer (an Arrow table)."""
    con = duckdb.connect()
    con.execute("SET threads = 1")  # keeps the answer's row order for the ordered hash
    con.register("t", table)
    cols = con.execute("DESCRIBE t").fetchall()
    if not cols:
        return {"rows": table.num_rows, "hash": "0", "ohash": None, "head": []}
    line = "concat_ws('|', " + ", ".join(_expr(c[0], c[1]) for c in cols) + ")"
    rows, h = con.execute(f"SELECT count(*), CAST(coalesce(sum(CAST(hash({line}) AS HUGEINT)), 0) % 18446744073709551616 AS VARCHAR) FROM t").fetchone()
    out = {"rows": rows, "hash": h, "ohash": None, "head": []}
    if ordered and rows <= 1_000_000:
        sha = hashlib.sha256()
        for (s,) in con.execute(f"SELECT {line} FROM t").fetchall():
            sha.update(s.encode() + b"\n")
        out["ohash"] = sha.hexdigest()[:16]
    out["head"] = [r[0] for r in con.execute(f"SELECT {line} FROM t LIMIT {keep}").fetchall()]
    con.close()
    return out


def same(a: dict, b: dict) -> bool:
    """True when two digests describe the same answer (ordered hash only when both have one)."""
    if a.get("rows") != b.get("rows") or a.get("hash") != b.get("hash"):
        return False
    if a.get("ohash") and b.get("ohash"):
        return a["ohash"] == b["ohash"]
    return True
