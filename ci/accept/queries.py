"""Queries of the HDFS acceptance check (ci/accept), written for this repo from the maintainer's test list.

Groups:
  tpch-plain   TPC-H q01-q22 with PLAIN table names (queries/tpch, as benchmark clients send them)
  tpch-schema  TPC-H q01-q22 schema-qualified (queries/tpch-schema)
  spread       plain names over spread.lineitem_sp (1 MiB blocks, replication 2) and spread.orders_sp
               (1 MiB blocks, replication 1): no DataNode holds any of their files whole
  far          spread.part_far, whose FIRST file is only on a DataNode without a server
  scan         full scans (row count + hash): lineitem_sp and the 12-file tpch lineitem
"""
import os
import re
from dataclasses import dataclass

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "queries")


@dataclass(frozen=True)
class Query:
    id: str
    group: str
    sql: str
    ordered: bool


def _read(d, n):
    with open(os.path.join(ROOT, d, f"q{n:02d}.sql")) as f:
        return f.read().strip().rstrip(";")


def _ordered(sql):
    return re.search(r"\border\s+by\b", sql, re.I) is not None


def _spread(sql):
    sql = re.sub(r"\blineitem\b", "lineitem_sp", sql)
    return re.sub(r"\borders\b", "orders_sp", sql)


SPREAD = {
    "sp-count": "SELECT count(*) AS n FROM lineitem_sp",
    "sp-sum": "SELECT count(*) AS n, sum(l_quantity) AS q, sum(l_extendedprice) AS p FROM lineitem_sp",
    "sp-group": ("SELECT l_returnflag, l_linestatus, count(*) AS n, sum(l_quantity) AS q, avg(l_discount) AS d"
                 " FROM lineitem_sp GROUP BY l_returnflag, l_linestatus"),
    "sp-group-order-limit": ("SELECT l_suppkey, sum(l_quantity) AS q FROM lineitem_sp GROUP BY l_suppkey"
                             " ORDER BY q DESC, l_suppkey LIMIT 10"),
    "sp-having": ("SELECT l_orderkey, sum(l_quantity) AS q FROM lineitem_sp GROUP BY l_orderkey"
                  " HAVING sum(l_quantity) > 300"),
    "sp-distinct": "SELECT count(DISTINCT l_partkey) AS n, count(DISTINCT l_suppkey) AS s FROM lineitem_sp",
    "sp-orders-count": "SELECT count(*) AS n, sum(o_totalprice) AS t FROM orders_sp",
    "sp-orders-group": "SELECT o_orderpriority, count(*) AS n FROM orders_sp GROUP BY o_orderpriority",
    "sp-comma-join": ("SELECT count(*) AS n, sum(o.o_totalprice) AS t FROM orders_sp o, customer c"
                      " WHERE o.o_custkey = c.c_custkey"),
    "sp-join-on": ("SELECT c.c_mktsegment, count(*) AS n FROM orders_sp o JOIN customer c"
                   " ON o.o_custkey = c.c_custkey GROUP BY c.c_mktsegment"),
    "sp-join-lineitem": ("SELECT count(*) AS n, sum(l.l_quantity) AS q FROM lineitem_sp l JOIN orders_sp o"
                         " ON l.l_orderkey = o.o_orderkey"),
}
FAR = {
    "far-count": "SELECT count(*) AS n, sum(p_retailprice) AS r FROM part_far",
    "far-group": "SELECT p_mfgr, count(*) AS n FROM part_far GROUP BY p_mfgr",
}
SCAN = {
    "scan-lineitem-sp": "SELECT * FROM lineitem_sp",
    "scan-lineitem": "SELECT * FROM tpch.lineitem",
}
# partial mode (check 3): additive answers, summed over the per-node parts; the server requires
# schema-qualified names for partial results (INVALID_ARGUMENT otherwise, by design)
PARTIAL = {
    "part-lineitem-sp": "SELECT count(*) AS n, sum(l_quantity) AS q FROM spread.lineitem_sp",
    "part-orders-sp": "SELECT count(*) AS n, sum(o_totalprice) AS t FROM spread.orders_sp",
    "part-lineitem": "SELECT count(*) AS n, sum(l_quantity) AS q FROM tpch.lineitem",
    "part-group-sp": ("SELECT l_returnflag, l_linestatus, count(*) AS n, sum(l_quantity) AS q"
                      " FROM spread.lineitem_sp GROUP BY l_returnflag, l_linestatus"),
}


def tpch(group):
    d = "tpch" if group == "tpch-plain" else "tpch-schema"
    return [Query(f"{group}-q{n:02d}", group, s, _ordered(s)) for n in range(1, 23) for s in [_read(d, n)]]


def spread():
    out = [Query(k, "spread", v, _ordered(v)) for k, v in SPREAD.items()]
    for n in (3, 12):
        s = _spread(_read("tpch", n))
        out.append(Query(f"sp-q{n:02d}", "spread", s, _ordered(s)))
    return out


def far():
    return [Query(k, "far", v, _ordered(v)) for k, v in FAR.items()]


def scans():
    return [Query(k, "scan", v, False) for k, v in SCAN.items()]


def partial():
    return [Query(k, "partial", v, False) for k, v in PARTIAL.items()]


def all_queries():
    return tpch("tpch-plain") + tpch("tpch-schema") + spread() + far() + scans() + partial()
