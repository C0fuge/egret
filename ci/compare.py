"""compare.py <jobs-dir> <out-dir> <title>: tables of the compare workflow (server A vs server B on the same runner).

Every job dir holds A/r<N>/ and B/r<N>/ (ab.sh), ref/adbc1/ ref/adbc10/ (reference answers of in-process DuckDB on the
same Parquet files, tpch_adbc.py) and job.json. Per side and metric: median over rounds (small-query p50/p95 per client
and concurrency, TPC-H sum of warm per-query medians, scan MB/s, peak RSS); ratio = B / A.

Correctness: a side's value for a workload is n/a (disqualified, never ranked) when any round of it failed: TPC-H over
ADBC with any query answer (rows + checksum) different from the reference or failed; TPC-H over JDBC with md5 different
from the reference of aggregate.py; a small-query client/concurrency with errors or with per-class answer sums
different from the most common ones of all sides of the run; scans with errors or wrong row counts.
"""
import collections
import csv
import glob
import json
import os
import re
import statistics as st
import sys

sys.path.insert(0, os.path.dirname(__file__))
from aggregate import REF, pct  # noqa: E402

CC = [(cl, c) for cl in ("jdbc", "adbc") for c in (1, 8, 32)]


def small(d, cl, c):
    p = os.path.join(d, f"small-{cl}-c{c}.csv")
    if not os.path.exists(p):
        return None
    rows = list(csv.DictReader(open(p)))
    lat = [float(r["lat_ms"]) for r in rows if r["ok"] == "1"]
    sig = collections.defaultdict(lambda: [0, 0.0])
    for r in rows:
        sig[r["class"]][0] += int(r["rows"])
        sig[r["class"]][1] += float(r["val"])
    return {"p50": pct(lat, .5), "p95": pct(lat, .95), "p99": pct(lat, .99), "err": sum(1 for r in rows if r["ok"] != "1"), "n": len(rows),
            "sig": {k: f"{v[0]}:{v[1]:.0f}" for k, v in sig.items()}}


def tpch_summary(d):
    p = os.path.join(d, "summary.tsv")
    if not os.path.exists(p):
        return None
    return {r["query"]: r for r in csv.DictReader(open(p), delimiter="\t")}


def side_round(d, ref):
    txt = open(os.path.join(d, "result.txt")).read() if os.path.exists(os.path.join(d, "result.txt")) else ""
    r = {"fail": collections.defaultdict(list), "val": {}}
    if "START FAILED" in txt or "SERVER DIED" in txt:
        r["fail"]["server"].append(" ".join(sorted(set(re.findall(r"START FAILED\s*\w*|SERVER DIED after \w+", txt)))))
    for cl, c in CC:
        s = small(d, cl, c)
        if s is None:
            continue
        r[f"{cl}{c}"] = s
        if s["err"]:
            r["fail"][f"small-{cl}{c}"].append(f"{s['err']}/{s['n']} errors")
        for p in ("p50", "p95", "p99"):
            r["val"][f"{cl}{c}_{p}"] = s[p]
    for n in ("jdbc10", "jdbc1"):
        m = re.search(rf"^{n}: ok=(\d+) cold_sum=([\d.]+) median_sum=([\d.]+) md5=(\w+)", txt, re.M)
        if m:
            r["val"][n] = float(m.group(3))
            if m.group(4) != REF[n]:
                r["fail"][n].append(f"md5 {m.group(4)} ({m.group(1)}/22 ok)")
    for n in ("adbc10", "adbc1"):
        s = tpch_summary(os.path.join(d, n))
        if s is None:
            continue
        bad = [q for q, x in ref.get(n, {}).items() if q not in s or s[q]["status"] != "ok"
               or (s[q]["rows"], s[q]["checksum"]) != (x["rows"], x["checksum"])]
        failed = [q for q in bad if q not in s or s[q]["status"] != "ok"]
        if not ref.get(n):
            r["fail"][n].append("no reference")
        elif bad:
            wrong = [q for q in bad if q not in failed]
            if wrong:
                r["fail"][n].append("wrong " + ",".join(wrong))
            if failed:
                r["fail"][n].append("failed " + ",".join(failed))
        r["val"][n] = sum(float(x["median_s"]) for x in s.values() if x["status"] == "ok") if not bad else None
    for m in re.finditer(r"^scan conc=(\d+) .*?rows=(\d+) mb=\d+ rows_per_s=\d+ mb_per_s=([\d.]+).*?errors=(\d+)", txt, re.M):
        r["val"][f"scan{m.group(1)}"] = float(m.group(3))
        if int(m.group(4)) or int(m.group(2)) % 59986052:
            r["fail"][f"scan{m.group(1)}"].append(f"rows={m.group(2)} errors={m.group(4)}")
    m = re.search(r"^adbcscan wall=[\d.]+ rows=(\d+) .*?mb_per_s=([\d.]+) errors=(\d+)", txt, re.M)
    if m:
        r["val"]["adbcscan"] = float(m.group(2))
        if int(m.group(3)) or int(m.group(1)) % 59986052:
            r["fail"]["adbcscan"].append(f"rows={m.group(1)} errors={m.group(3)}")
    mp = os.path.join(d, "mem.txt")
    hw = [int(x) for x in re.findall(r"hwm=(\d+)", open(mp).read())] if os.path.exists(mp) else []
    r["val"]["rss"] = max(hw, default=None)
    return r


METRICS = ([(f"{cl}{c}_p{p}", f"small {cl.upper()} c{c} p{p}", "ms", f"small-{cl}{c}") for cl, c in CC for p in (50, 95, 99)]
           + [("adbc1", "TPC-H SF1 ADBC (sum of medians)", "s", "adbc1"), ("adbc10", "TPC-H SF10 ADBC (sum of medians)", "s", "adbc10"),
              ("jdbc1", "TPC-H SF1 JDBC (sum of medians)", "s", "jdbc1"), ("jdbc10", "TPC-H SF10 JDBC (sum of medians)", "s", "jdbc10"),
              ("scan1", "lineitem scan x1", "MB/s", "scan1"), ("scan4", "lineitem scan x4", "MB/s", "scan4"),
              ("scan8", "lineitem scan x8", "MB/s", "scan8"), ("adbcscan", "lineitem export ADBC", "MB/s", "adbcscan"),
              ("rss", "server RSS peak", "MB", "rss")])
OVERVIEW = ["adbc1_p50", "adbc32_p95", "jdbc1_p50", "jdbc32_p95", "adbc1", "adbc10", "jdbc10", "scan1"]


def fmt(x, n=2):
    return "n/a" if x is None else f"{x:.{n}f}"


def main():
    src, dst, title = sys.argv[1], sys.argv[2], sys.argv[3]
    # runs listed in ci/ignored-runs.txt (wrong server build, superseded) must not commit results: fail the aggregate step
    ign = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ignored-runs.txt")
    run = os.environ.get("GITHUB_RUN_ID", "")
    if run and os.path.exists(ign) and run in {l.split("#")[0].strip() for l in open(ign)}:
        sys.exit(f"run {run} is listed in ci/ignored-runs.txt: no results committed")
    os.makedirs(dst, exist_ok=True)
    jobs = []
    for job in sorted(glob.glob(os.path.join(src, "*"))):
        meta = json.load(open(os.path.join(job, "job.json"))) if os.path.exists(os.path.join(job, "job.json")) else {"variant": os.path.basename(job)}
        ref = {n: tpch_summary(os.path.join(job, "ref", n)) or {} for n in ("adbc1", "adbc10")}
        sides = {s: [side_round(d, ref) for d in sorted(glob.glob(os.path.join(job, s, "r*")))] for s in "AB"}
        jobs.append((os.path.basename(job), meta, sides))
    # small-query reference answers: most common per-class sums over all sides and rounds of the run
    votes = collections.defaultdict(collections.Counter)
    for _, _, sides in jobs:
        for rs in sides.values():
            for r in rs:
                for cl, c in CC:
                    for k, v in (r.get(f"{cl}{c}") or {}).get("sig", {}).items():
                        votes[(cl, c, k)][v] += 1
    sig_ref = {k: v.most_common(1)[0][0] for k, v in votes.items()}
    for _, _, sides in jobs:
        for rs in sides.values():
            for r in rs:
                for cl, c in CC:
                    wrong = [k for k, v in (r.get(f"{cl}{c}") or {}).get("sig", {}).items() if sig_ref[(cl, c, k)] != v]
                    if wrong:
                        r["fail"][f"small-{cl}{c}"].append("answers differ: " + ",".join(sorted(wrong)))

    def agg(rs):
        fails = collections.defaultdict(set)
        for r in rs:
            for k, v in r["fail"].items():
                fails[k].update(v)
        out = {}
        for key, _, _, wl in METRICS:
            xs = [r["val"].get(key) for r in rs]
            if wl in fails or "server" in fails and all(x is None for x in xs):
                out[key] = None
            else:
                xs = [x for x in xs if x is not None]
                out[key] = st.median(xs) if xs else None
        return out, fails

    lines = [f"# {title}", "",
             "Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet",
             "data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;",
             "scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate",
             "(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against",
             "in-process DuckDB on the same files.", "", "## Overview (ratios B / A)", "",
             "| job | A | B | storage | runner | rounds A/B | " + " | ".join(next(m[1] for m in METRICS if m[0] == k) for k in OVERVIEW) + " | disqualified |",
             "|" + "---|" * (7 + len(OVERVIEW))]
    detail, rows_csv = [], []
    for jid, meta, sides in jobs:
        (a, fa), (b, fb) = agg(sides["A"]), agg(sides["B"])
        sa = f"{meta.get('name_a') or meta.get('server_a', '')} `{meta.get('flags_a', '') or '-'}`"
        sb = f"{meta.get('name_b') or meta.get('server_b', '')} `{meta.get('flags_b', '') or '-'}`"
        dq = "; ".join(f"{s}: " + ", ".join(f"{k} ({'; '.join(sorted(v))})" for k, v in sorted(f.items())) for s, f in (("A", fa), ("B", fb)) if f) or "none"
        rat = {k: (b[k] / a[k] if a.get(k) and b.get(k) is not None else None) for k, *_ in METRICS}
        lines.append(f"| {jid} | {sa} | {sb} | {meta.get('storage', '')} | {meta.get('runner', '')} | {len(sides['A'])}/{len(sides['B'])} | "
                     + " | ".join(fmt(rat[k]) for k in OVERVIEW) + f" | {dq} |")
        detail += ["", f"### {jid}: A = {sa}, B = {sb}, {meta.get('storage', '')}", "",
                   f"Runner: {meta.get('runner', '')}. Workloads: `{meta.get('workloads', '')}`"
                   + (f", small-query classes `{meta['small_classes']}`" if meta.get("small_classes") else "") + ".", "",
                   "| metric | unit | A median | B median | B / A | per-round B / A |", "|---|---|---|---|---|---|"]
        for key, label, unit, wl in METRICS:
            if a[key] is None and b[key] is None and wl not in fa and wl not in fb:
                continue
            pr = [rb["val"].get(key) / ra["val"].get(key) for ra, rb in zip(sides["A"], sides["B"])
                  if ra["val"].get(key) and rb["val"].get(key) is not None and wl not in fa and wl not in fb]
            detail.append(f"| {label} | {unit} | {fmt(a[key], 1)} | {fmt(b[key], 1)} | {fmt(rat[key])} | "
                          + (" ".join(f"{x:.2f}" for x in pr) or "-") + " |")
            rows_csv.append([jid, meta.get("server_a"), meta.get("flags_a"), meta.get("server_b"), meta.get("flags_b"), meta.get("storage"),
                             meta.get("runner"), key, unit, a[key], b[key], rat[key], " ".join(f"{x:.3f}" for x in pr)])
        if fa or fb:
            detail.append("")
            detail.append("Correctness gate: " + dq + ".")
    lines += ["", "## Per job (absolute medians and ratios)"] + detail
    open(os.path.join(dst, "summary.md"), "w").write("\n".join(lines) + "\n")
    with open(os.path.join(dst, "summary.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["job", "server_a", "flags_a", "server_b", "flags_b", "storage", "runner", "metric", "unit", "a_median", "b_median", "ratio_b_a", "per_round_ratios"])
        w.writerows(rows_csv)
    print("\n".join(lines))


if __name__ == "__main__":
    main()
