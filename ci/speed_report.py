"""speed_report.py <jobs-dir> <out.md> <run id>: Report 1 (SPEED) of the 4-server comparison from the compare jobs (wave c2-speed).

Every job pairs ours-new (side A) with one other server (side B) on the same runner. Absolute numbers per server: median over
rounds within its job; ours-new: median over all its jobs of the same storage and setting. The last column is the
same-runner ratio (best upstream time / ours-new time, > 1 = ours-new faster; scans: ours-new MB/s / best upstream MB/s),
taken inside each upstream pair job, so runner-to-runner noise does not enter it. Correctness: a TPC-H query whose rows or
checksum differ from in-process DuckDB on the same files (or that failed) is n/a for that server and never ranked; the
Score row sums only the queries every shown server answered correctly. Writes <out.md> and <out>-queries.csv.
"""
import collections
import csv
import glob
import hashlib
import json
import math
import os
import re
import statistics as st
import sys

sys.path.insert(0, os.path.dirname(__file__))
from aggregate import pct  # noqa: E402

SERVERS = ["ours-new", "ours-27f5", "up-native", "up-main"]
UP = ["up-native", "up-main"]
CLASSES = ["point_orders", "point_lineitem", "count_filter", "limit10_ob", "meta_tables", "meta_schemas"]


def med(xs):
    xs = [x for x in xs if x is not None]
    return st.median(xs) if xs else None


def tsv(p):
    return {r["query"]: r for r in csv.DictReader(open(p), delimiter="\t")} if os.path.exists(p) else None


def canon(p):
    """rows of a result .tsv for a numeric comparison: numbers as floats, rows sorted by a coarse (6-digit) key"""
    if not os.path.exists(p):
        return None
    def fld(v):
        try:
            return int(v) if re.fullmatch(r"-?\d+", v) else float(v)
        except ValueError:
            return v
    rows = [tuple(fld(v) for v in line.split("\t")) for line in open(p).read().splitlines() if line]
    return sorted(rows, key=lambda r: tuple(f"{v:.6g}" if isinstance(v, float) else str(v) for v in r))


def same(a, b):
    """two canon() results equal, numbers within a relative 1.5e-9 (two 10-digit roundings at most: DECIMAL exact vs %.10g)"""
    if a is None or b is None or len(a) != len(b):
        return False
    for x, y in zip(a, b):
        if len(x) != len(y):
            return False
        for u, v in zip(x, y):
            if isinstance(u, (int, float)) and isinstance(v, (int, float)):
                if not math.isclose(u, v, rel_tol=1.5e-9, abs_tol=1e-12):
                    return False
            elif u != v:
                return False
    return True


def load(src):
    jobs = []
    for job in sorted(glob.glob(os.path.join(src, "*"))):
        if not os.path.exists(os.path.join(job, "job.json")):
            continue
        m = json.load(open(os.path.join(job, "job.json")))
        m["containers"] = os.path.exists(os.path.join(job, "containers.txt"))
        m["setting"] = "t8" if "Threads=8" in (m.get("flags_a") or "") else "def"
        ref = {n: tsv(os.path.join(job, "ref", n, "summary.tsv")) or {} for n in ("adbc1", "adbc10")}
        sides = {}
        for s in "AB":
            name = m.get(f"name_{s.lower()}") or m.get(f"server_{s.lower()}")
            rounds = sorted(glob.glob(os.path.join(job, s, "r*")))
            sides[name] = rounds
        jobs.append((os.path.basename(job), m, ref, sides))
    # JDBC: the runner formats DECIMAL / DOUBLE values differently from the ADBC reference (BigDecimal plain string vs
    # %.10g), so its answers are compared numerically (relative 1.5e-9) with the reference rows
    for jid, _, ref, _ in jobs:
        for w, a in (("jdbc1", "adbc1"), ("jdbc10", "adbc10")):
            ref[w] = {q: {"rows": x["rows"], "checksum": canon(os.path.join(src, jid, "ref", a, q + ".tsv"))} for q, x in ref[a].items()}
    return jobs


REASONS = [  # client error text -> short reason (the server-side exception is in the job log)
    ("Failed to prepare Flight SQL statement", "the server's schema resolver rejects it (upstream: single-table parser, `Can only select from ONE table`; `AVG` unsupported on main)"),
    ("Error getting Arrow schema", "the server's schema resolver rejects it (upstream: single-table parser, `Can only select from ONE table`; `AVG` unsupported on main)"),
    ("does not exist because schema", "subquery table not rewritten: DuckDB `schema \"tpch\" does not exist`"),
    ("inconsistent schema", "advertised schema differs from the data (e.g. float64 vs decimal(38,4)): ADBC rejects the stream"),
]


def reason(p):
    t = " ".join(open(p).read().split())[:400]
    return next((r for k, r in REASONS if k in t), t[:160])


def tpch(rounds, ref, w):
    """per query: (median warm s, cold s median, ok) over rounds; ok = every round correct"""
    out = {}
    per = []
    for r in rounds:
        p = tsv(os.path.join(r, w, "summary.tsv"))
        if p is not None and w.startswith("jdbc"):
            for q, x in p.items():
                if x["status"] == "ok":
                    x["checksum"] = canon(os.path.join(r, w, q + ".tsv"))
        if p is not None:
            per.append(p)
    if not per:
        return None
    for q in sorted(ref):
        rs = [p.get(q) for p in per]
        ok = all(x is not None and x["status"] == "ok" and x["rows"] == ref[q]["rows"]
                 and (same(x["checksum"], ref[q]["checksum"]) if w.startswith("jdbc") else x["checksum"] == ref[q]["checksum"]) for x in rs)
        why = "" if ok else ("failed" if any(x is None or x["status"] != "ok" for x in rs) else "wrong answer")
        if why == "failed":
            why = "failed: " + next((reason(os.path.join(r, w, q + ".error")) for r in rounds
                                     if os.path.exists(os.path.join(r, w, q + ".error"))), "no result")
        out[q] = {"warm": med([float(x["median_s"]) for x in rs if x and x["status"] == "ok"]),
                  "cold": med([float(x["cold_s"]) for x in rs if x and x["status"] == "ok"]), "ok": ok, "why": why}
    return out


def small(rounds, cl, c):
    lat = collections.defaultdict(list)
    err = collections.Counter()
    for r in rounds:
        p = os.path.join(r, f"small-{cl}-c{c}.csv")
        if not os.path.exists(p):
            continue
        for x in csv.DictReader(open(p)):
            if x["ok"] == "1":
                lat[x["class"]].append(float(x["lat_ms"]))
            else:
                err[x["class"]] += 1
    return {k: {"p50": pct(v, .5), "p95": pct(v, .95), "p99": pct(v, .99), "n": len(v), "err": err[k]} for k, v in lat.items()} | \
        {k: {"err": n, "n": 0} for k, n in err.items() if k not in lat}


def scans(rounds):
    v = collections.defaultdict(list)
    for r in rounds:
        txt = open(os.path.join(r, "result.txt")).read() if os.path.exists(os.path.join(r, "result.txt")) else ""
        for m in re.finditer(r"^scan conc=(\d+) .*?rows=(\d+) .*?mb_per_s=([\d.]+).*?errors=(\d+)", txt, re.M):
            if not int(m.group(4)) and int(m.group(2)) and int(m.group(2)) % 59986052 == 0:
                v[f"scan{m.group(1)}"].append(float(m.group(3)))
        m = re.search(r"^adbcscan .*?rows=(\d+) .*?mb_per_s=([\d.]+) errors=(\d+)", txt, re.M)
        if m and not int(m.group(3)) and int(m.group(1)) % 59986052 == 0:
            v["adbcscan"].append(float(m.group(2)))
        mp = os.path.join(r, "mem.txt")
        if os.path.exists(mp):
            hw = [int(x) for x in re.findall(r"hwm=(\d+)", open(mp).read())]
            if hw:
                v["rss"].append(max(hw))
    return {k: med(x) for k, x in v.items()}


def mib(t):
    m = re.match(r"([\d.]+)\s*([KMG]i?B|B)", t.strip())
    if not m:
        return None
    return float(m.group(1)) * {"B": 1 / 2**20, "KiB": 1 / 1024, "KB": 1 / 1024, "MiB": 1, "MB": 1, "GiB": 1024, "GB": 1024}[m.group(2)]


def container(rounds):
    """docker stats of the server container (CPU % of one core, memory MiB; samples every ~5 s) and OOM kills"""
    cpu, mem, oom = [], [], 0
    for r in rounds:
        p = os.path.join(r, "docker-stats.tsv")
        for line in open(p) if os.path.exists(p) else []:
            x = line.rstrip("\n").split("\t")
            if len(x) >= 3 and x[1].endswith("%"):
                cpu.append(float(x[1][:-1]))
                v = mib(x[2].split("/")[0])
                if v is not None:
                    mem.append(v)
        p = os.path.join(r, "container.txt")
        if os.path.exists(p) and "oom=true" in open(p).read():
            oom += 1
    return {"cpu_p50": pct(cpu, .5) if cpu else None, "cpu_max": max(cpu) if cpu else None,
            "mem_max": max(mem) if mem else None, "oom": oom, "n": len(cpu), "rounds": len(rounds)}


def group(notes):
    """'q01 failed: why' notes -> 'failed: why: q01 q04'; other notes unchanged"""
    by, rest = collections.defaultdict(list), []
    for n in sorted(notes):
        q, _, why = n.partition(" ")
        (by[why].append(q) if re.fullmatch(r"q\d+", q) else rest.append(n))
    return [f"{why}: {' '.join(qs)}" for why, qs in sorted(by.items())] + rest


def f(x, n=0):
    return "n/a" if x is None else f"{x:.{n}f}"


def main():
    src, dst, run = sys.argv[1], sys.argv[2], sys.argv[3]
    jobs = load(src)
    if not jobs:
        print("no jobs")
        return
    L, rows_csv = [], []
    m0 = jobs[0][1]
    srv = dict(m0.get("servers", {}))
    for _, m, _, _ in jobs:  # a server's id from a job that ran it (merged runs may resolve up-native differently)
        for k in (m.get("name_a"), m.get("name_b")):
            if k in m.get("servers", {}):
                srv[k] = m["servers"][k]
    # setup
    duck, cmds = {}, {}
    for _, m, _, sides in jobs:
        for name, rounds in sides.items():
            for r in rounds:
                p = os.path.join(r, "start-times.txt")
                if os.path.exists(p) and name not in duck:
                    mm = re.search(r"duckdb=(.*)", open(p).read())
                    if mm:
                        duck[name] = mm.group(1).strip()
                p = os.path.join(r, "jvm-cmd.json")
                if os.path.exists(p) and (name, m["setting"]) not in cmds:
                    cmds[(name, m["setting"])] = " ".join(x for x in json.load(open(p)) if x.startswith("-") and "S3_" not in x)
    runners = sorted({m.get("runner", "") for _, m, _, _ in jobs})
    L += [f"# Server comparison - Report 1: SPEED (compare run {run})", "",
          "## Experiment setup", "", "| item | value |", "|---|---|",
          f"| runner | GitHub-hosted `ubuntu-latest`: {'; '.join(runners)}; RAM {m0.get('mem_mb', '?')} MB; kernel {m0.get('kernel', '?')}; JDK Temurin 21 |",
          ("| containers | every server: `eclipse-temurin:21-jre`, `--cpus=2 --cpuset-cpus=0,1 --memory=6g --memory-swap=6g`, JVM `-Xmx3g -XX:MaxDirectMemorySize=2g`, `MALLOC_ARENA_MAX=4`, host network; clients (JDBC/ADBC/Flight runners, jcmd sampling) and the S3 server in their own containers on cpus 2,3 |" if all(m["containers"] for _, m, _, _ in jobs) else
           "| containers | **no-container reference run**: server in `eclipse-temurin:21-jdk` with an 8 GB memory limit and no CPU limit, clients on the runner host; not the reported numbers |"),
          "| servers | " + "; ".join(f"{k} = `{srv.get(k, '?')}` (DuckDB {duck.get(k, '?')})" for k in SERVERS) + " |",
          "| data | TPC-H SF1 and SF10, DuckDB dbgen, Parquet, 8 files per big table, 122880-row row groups, one data dir `tpch.*` per SF |",
          "| storage | local disk (`file://`, page-cached) and S3 (`rclone serve s3` on the same runner, path style) |",
          "| pairs | every job: ours-new (side A) vs one other server (side B) on the same runner, rounds A B / B A / A B (3), 1 cold run (warm-up) + warm runs per query (SF1 2 warm, SF10 1 warm per round) |",
          "| settings | `def` = each server's default (`duckDbThreads` ours 4, upstream 2); `t8` = `-DduckDbThreads=8` on both |",
          "| batch size | server defaults (not overridden) |",
          "| clients | TPC-H: Python ADBC Flight SQL 1.12.0 (pyarrow 26), Flight SQL JDBC 18.0.0; small queries: same; scans: raw Flight (Arrow Java), ADBC export |",
          "| correctness | TPC-H over ADBC: rows + checksum per query equal to in-process DuckDB on the same files; over JDBC: the result rows compared numerically with the same reference (numbers within a relative 1.5e-9, i.e. two 10-digit roundings; the JDBC runner prints DECIMAL as an exact plain BigDecimal, the reference as %.10g) |",
          "| upstream on S3 | up-native: `s3a://` data dir (Hadoop S3A from its `docker/hadoop-aws` recipe for listing, DuckDB httpfs for scans, `FLIGHT_S3_*` settings); up-main: **n/a**, main at the fork point has no S3 settings (no `FLIGHT_S3_*`, no S3A dependencies) |",
          "| SF30 | not run: SF1+SF10 already fill most of the repo's 10 GB Actions cache, SF30 Parquet (~11 GB) does not fit; generating it per job costs ~20 min of each 4-vCPU runner |",
          ] + [f"| JVM `{k[0]}` `{k[1]}` | `{v}` |" for k, v in sorted(cmds.items())] + [""]
    L += ["Times are warm medians in ms (median over rounds of the per-round warm median). **n/a** = not run, failed or wrong",
          "answer (reason in the notes). Last column: same-runner ratio best-upstream / ours-new (> 1 = ours-new faster).", ""]
    for storage in ("local", "s3"):
        for setting in ("def", "t8"):
            js = [j for j in jobs if j[1].get("storage") == storage and j[1]["setting"] == setting]
            if not js:
                continue
            L += [f"## {storage}, setting `{setting}`", ""]
            for w, label in (("adbc10", "TPC-H SF10, ADBC"), ("adbc1", "TPC-H SF1, ADBC"), ("jdbc10", "TPC-H SF10, JDBC"), ("jdbc1", "TPC-H SF1, JDBC")):
                vals = collections.defaultdict(list)   # (server, q) -> [per job dict]
                ratio = collections.defaultdict(dict)  # q -> up -> same-runner up/ours
                ref = {}
                for jid, m, rf, sides in js:
                    ref = ref or rf.get(w, {})
                    t = {name: tpch(rounds, rf.get(w, {}), w) for name, rounds in sides.items()}
                    for name, d in t.items():
                        for q, x in (d or {}).items():
                            vals[(name, q)].append(x)
                    b = m.get("name_b")
                    if b in UP and t.get("ours-new") and t.get(b):
                        for q in t[b]:
                            a, u = t["ours-new"].get(q), t[b][q]
                            if a and a["ok"] and u["ok"] and a["warm"] and u["warm"] is not None:
                                ratio[q][b] = u["warm"] / a["warm"]
                if not vals:
                    continue
                qs = sorted({q for _, q in vals})
                shown = [s for s in SERVERS if any((s, q) in vals for q in qs)]
                L += [f"### {label}", "", "| Q | Pattern | " + " | ".join(f"{s} (ms)" for s in SERVERS) + " | ours-new vs best upstream |",
                      "|---|---|" + "---|" * (len(SERVERS) + 1)]
                notes, cell, okall = collections.defaultdict(set), {}, collections.defaultdict(bool)
                for q in qs:
                    row = []
                    for s in SERVERS:
                        xs = vals.get((s, q))
                        if not xs:
                            cell[(s, q)] = None
                            row.append("n/a")
                            continue
                        good = all(x["ok"] for x in xs)
                        v = med([x["warm"] for x in xs]) if good else None
                        cell[(s, q)] = v
                        if not good:
                            notes[s].add(f"{q} {next(x['why'] for x in xs if not x['ok'])}")
                        row.append(f(v * 1000 if v is not None else None))
                        rows_csv.append([storage, setting, w, q, s, v, med([x["cold"] for x in xs]), good])
                    rr = ratio.get(q, {})
                    best = min(rr.values()) if rr else None
                    L.append(f"| {q} | {PATTERN.get(q, '')} | " + " | ".join(row) + f" | {f(best, 2) + 'x' if best else 'n/a'} |")
                common = [q for q in qs if all(cell.get((s, q)) is not None for s in shown)]
                gm = [math.log(min(ratio[q].values())) for q in qs if ratio.get(q)]
                L.append(f"| **Score** | sum of the {len(common)} queries every shown server answered | "
                         + " | ".join(f(sum(cell[(s, q)] for q in common) * 1000) if s in shown and common else "n/a" for s in SERVERS)
                         + f" | geomean {f(math.exp(sum(gm) / len(gm)), 2) + 'x' if gm else 'n/a'} ({len(gm)} q) |")
                for s in SERVERS:
                    if s not in shown:
                        notes[s].add("not run: " + ("upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)" if s in UP and w.startswith("jdbc") else "not in this setting's jobs"))
                L += [""] + [f"- {s}: " + "; ".join(group(v)) for s, v in notes.items() if v] + [""]
            # small queries
            L += ["### Small queries (ms, p50 / p95 / p99 over all rounds)", "",
                  "| class | client | c | " + " | ".join(SERVERS) + " |", "|---|---|---|" + "---|" * len(SERVERS)]
            for cls in CLASSES:
                for cl in ("jdbc", "adbc"):
                    for c in (1, 8, 32):
                        cells = []
                        for s in SERVERS:
                            rs = [r for _, m, _, sides in js for name, rounds in sides.items() if name == s for r in rounds]
                            x = small(rs, cl, c).get(cls) if rs else None
                            if not x:
                                cells.append("n/a")
                            elif x["err"]:
                                errs = [open(e).read().splitlines() for r in rs for e in glob.glob(os.path.join(r, f"small-{cl}-c{c}.err"))]
                                first = next((l for ls in errs for l in ls if l.startswith(cls)), "")
                                cells.append(f"n/a ({x['err']} errors{': ' + first[len(cls):][:80].strip(': ') if first else ''})")
                            else:
                                cells.append(f"{x['p50']:.1f} / {x['p95']:.1f} / {x['p99']:.1f}")
                        L.append(f"| {cls} | {cl.upper()} | {c} | " + " | ".join(cells) + " |")
            L += ["", "Answers per class are compared across servers in the run summary (`summary.md`, correctness gate).", ""]
            # scans
            L += ["### Scans (`SELECT * FROM tpch.lineitem`, SF10, MB/s of Arrow buffers) and server peak RSS", "",
                  "| metric | " + " | ".join(SERVERS) + " | ours-new vs best upstream |", "|---|" + "---|" * (len(SERVERS) + 1)]
            sc = collections.defaultdict(lambda: collections.defaultdict(list))
            sr = collections.defaultdict(list)
            for _, m, _, sides in js:
                if "scan" not in m.get("workloads", ""):
                    continue
                per = {name: scans(rounds) for name, rounds in sides.items()}
                for name, d in per.items():
                    for k, v in d.items():
                        sc[name][k].append(v)
                b = m.get("name_b")
                if b in UP:
                    for k in ("scan1", "scan4", "scan8", "adbcscan"):
                        if per.get("ours-new", {}).get(k) and per[b].get(k):
                            sr[k].append(per["ours-new"][k] / per[b][k])
            for k, lab in (("scan1", "raw Flight, 1 stream"), ("scan4", "raw Flight, 4 streams"), ("scan8", "raw Flight, 8 streams"),
                           ("adbcscan", "full export over ADBC"), ("rss", "server peak RSS (MB)")):
                L.append(f"| {lab} | " + " | ".join(f(med(sc[s][k])) for s in SERVERS)
                         + f" | {f(min(sr[k]), 2) + 'x' if sr.get(k) else ('-' if k == 'rss' else 'n/a')} |")
            L.append("")
            L += ["### Server container (docker stats every ~5 s, all workloads of this setting)", "",
                  "| metric | " + " | ".join(SERVERS) + " |", "|---|" + "---|" * len(SERVERS)]
            ct = {s: container([r for _, m, _, sides in js for name, rounds in sides.items() if name == s for r in rounds]) for s in SERVERS}
            for k, lab, n in (("cpu_p50", "CPU % p50 (200 = both cores)", 0), ("cpu_max", "CPU % max", 0), ("mem_max", "memory peak (MiB, limit 6144)", 0)):
                L.append(f"| {lab} | " + " | ".join(f(ct[s][k], n) for s in SERVERS) + " |")
            L.append("| OOM-killed rounds | " + " | ".join(f"{ct[s]['oom']} / {ct[s]['rounds']}" if ct[s]["rounds"] else "n/a" for s in SERVERS) + " |")
            L.append("")
    open(dst, "w").write("\n".join(L) + "\n")
    with open(os.path.splitext(dst)[0] + "-queries.csv", "w", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["storage", "setting", "workload", "query", "server", "warm_median_s", "cold_median_s", "correct"])
        wr.writerows(rows_csv)
    print("\n".join(L))


PATTERN = {"q01": "scan + aggregation", "q02": "correlated subquery, joins", "q03": "3-way join, top-N", "q04": "EXISTS semi-join",
           "q05": "6-way join", "q06": "selective scan", "q07": "joins, group by", "q08": "8-way join, CASE", "q09": "joins, LIKE, heavy",
           "q10": "4-way join, top-N", "q11": "HAVING subquery", "q12": "join, CASE agg", "q13": "outer join, LIKE", "q14": "join, CASE",
           "q15": "view / CTE, max", "q16": "NOT IN, distinct", "q17": "correlated avg", "q18": "IN subquery, big group by",
           "q19": "OR predicates", "q20": "nested IN", "q21": "EXISTS / NOT EXISTS", "q22": "substring, NOT EXISTS"}

if __name__ == "__main__":
    main()
