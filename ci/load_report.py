"""load_report.py <jobs-dir> <out.md> <run id>: Report 2 (LOAD) of the 4-server comparison from the compare jobs (wave c3-load).

Every job pairs ours-new (side A) with one other server (side B) on the same runner, in identically limited containers.
Per server and setting: values are medians over rounds (and, for ours-new, over all its jobs of that setting).
- load steps: closed-loop small queries (point orders / lineitem, filtered count) at 1/8/32/64/128 clients, 10 s warm-up +
  60 s recorded: QPS, p50/p95/p99 (ms), errors, server CPU % (docker stats mean in the step) and server memory (docker stats
  max in the step; RSS from /proc at the step end); saturation = highest step with p95 < 100 ms and 0 errors;
- mixed: 32 ADBC small-query clients alone and with 2 heavy SF10 streams (q01, q18 back to back);
- heavy4a: q01 q09 q18 q21 at once over ADBC: slowest time, failures, peak RSS;
- netem: loopback 10 ms RTT, 1 Gbit/s: SF10 TPC-H over ADBC (sum of warm medians of correctly answered queries) and the full
  lineitem export over ADBC.
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
from aggregate import pct  # noqa: E402
from speed_report import SERVERS, f, med, mib, tsv  # noqa: E402

STEPS = [1, 8, 32, 64, 128]


def load(src):
    jobs = []
    for job in sorted(glob.glob(os.path.join(src, "*"))):
        if not os.path.exists(os.path.join(job, "job.json")):
            continue
        m = json.load(open(os.path.join(job, "job.json")))
        m["setting"] = ("zstd" if "flightCompression=zstd" in (m.get("flags_b") or "") else
                        "t8" if "Threads=8" in (m.get("flags_a") or "") else "def")
        ref = tsv(os.path.join(job, "ref", "adbc10", "summary.tsv")) or {}
        sides = {(m.get(f"name_{s.lower()}") or m.get(f"server_{s.lower()}")): sorted(glob.glob(os.path.join(job, s, "r*"))) for s in "AB"}
        jobs.append((m, ref, sides))
    return jobs


def windows(r):
    w, p = {}, os.path.join(r, "steps.tsv")
    for line in open(p) if os.path.exists(p) else []:
        x = line.rstrip("\n").split("\t")
        if len(x) >= 3:
            w.setdefault(x[0], {})[x[1]] = int(x[2])
    return {k: (v["begin"], v["end"]) for k, v in w.items() if "begin" in v and "end" in v}


def dstats(r):
    out, p = [], os.path.join(r, "docker-stats.tsv")
    for line in open(p) if os.path.exists(p) else []:
        x = line.rstrip("\n").split("\t")
        if len(x) >= 3 and x[1].endswith("%"):
            out.append((int(x[0]), float(x[1][:-1]), mib(x[2].split("/")[0])))
    return out


def in_step(r, name):
    w = windows(r).get(name)
    if not w:
        return None, None
    xs = [(c, m) for t, c, m in dstats(r) if w[0] <= t <= w[1]]
    if not xs:
        return None, None
    return st.mean(c for c, _ in xs), max((m for _, m in xs if m is not None), default=None)


def lat_csv(p):
    lat, err = [], 0
    if not os.path.exists(p):
        return None
    for x in csv.DictReader(open(p)):
        if x["ok"] == "1":
            lat.append(float(x["lat_ms"]))
        else:
            err += 1
    return {"n": len(lat) + err, "err": err, "p50": pct(lat, .5) if lat else None, "p95": pct(lat, .95) if lat else None,
            "p99": pct(lat, .99) if lat else None}


def rss_at(r, name):
    p = os.path.join(r, "mem.txt")
    for line in open(p) if os.path.exists(p) else []:
        if line.startswith(name + " "):
            m = re.search(r"rss=(\d+) hwm=(\d+)", line)
            if m:
                return int(m.group(1)), int(m.group(2))
    return None, None


def first_err(r, name):
    p = os.path.join(r, name + ".err")
    if os.path.exists(p):
        for line in open(p):
            if line.strip():
                return line.strip()[:120]
    return ""


def main():
    src, dst, run = sys.argv[1], sys.argv[2], sys.argv[3]
    jobs = load(src)
    if not jobs:
        print("no jobs")
        return
    srv = jobs[0][0].get("servers", {})
    L = [f"# Server comparison - Report 2: LOAD (compare run {run})", "",
         "## Setup", "", "| item | value |", "|---|---|",
         f"| runner | GitHub-hosted `ubuntu-latest`: {'; '.join(sorted({m.get('runner', '') for m, _, _ in jobs}))}; RAM {jobs[0][0].get('mem_mb', '?')} MB |",
         "| containers | every server: `eclipse-temurin:21-jre`, `--cpus=2 --cpuset-cpus=0,1 --memory=6g --memory-swap=6g`, JVM `-Xmx3g -XX:MaxDirectMemorySize=2g`, `MALLOC_ARENA_MAX=4`; load generators in their own container on cpus 2,3 (so the client side has 2 cores too: at 64/128 clients the client can be the limit, see client notes) |",
         "| servers | " + "; ".join(f"{k} = `{srv.get(k, '?')}`" for k in SERVERS) + " |",
         "| data | TPC-H SF10 Parquet on local disk (load, mixed, heavy, netem) |",
         "| pairs | ours-new (side A) vs one other server (side B) on the same runner, rounds A B / B A / A B |",
         "| load mix | `point_orders`, `point_lineitem`, `count_filter` (every server answers them; upstream has no JDBC prepared statements) |",
         "| settings | `def` = each server's default `duckDbThreads` (ours 4, upstream 2); `t8` = 8 on both; `zstd` = netem path only, up-native with its ZSTD batch compression (`-DflightCompression=zstd`, decoded by ADBC) vs ours plain (up-main has no such option) |", ""]
    for setting in ("def", "t8", "zstd"):
        js = [j for j in jobs if j[0]["setting"] == setting]
        if not js:
            continue
        L += [f"## Setting `{setting}`", ""]
        # load steps
        for cl in ("jdbc", "adbc"):
            L += [f"### Closed-loop load, {cl.upper()} (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)", "",
                  "| clients | " + " | ".join(SERVERS) + " |", "|---|" + "---|" * len(SERVERS)]
            sat = {}
            for c in STEPS:
                cells = []
                for s in SERVERS:
                    rs = [r for m, _, sides in js if "load" in m.get("workloads", "") for name, rounds in sides.items() if name == s for r in rounds]
                    vals = []
                    for r in rs:
                        x = lat_csv(os.path.join(r, f"load-{cl}-c{c}.csv"))
                        if x is None:
                            continue
                        cpu, mem = in_step(r, f"load-{cl}-c{c}")
                        vals.append(x | {"qps": (x["n"] - x["err"]) / 60.0, "cpu": cpu, "mem": mem, "e1": first_err(r, f"load-{cl}-c{c}")})
                    if not vals:
                        cells.append("n/a")
                        continue
                    q = med([v["qps"] for v in vals])
                    p95 = med([v["p95"] for v in vals])
                    errs = sum(v["err"] for v in vals)
                    if p95 is not None and p95 < 100 and errs == 0:
                        sat[s] = c
                    e1 = next((v["e1"] for v in vals if v["err"] and v["e1"]), "")
                    cells.append(f"{f(q)} / {f(med([v['p50'] for v in vals]), 1)} / {f(p95, 1)} / {f(med([v['p99'] for v in vals]), 1)} / "
                                 f"{errs}{' (' + e1[:60] + ')' if e1 else ''} / {f(med([v['cpu'] for v in vals]))} / {f(max((v['mem'] for v in vals if v['mem']), default=None))}")
                L.append(f"| {c} | " + " | ".join(cells) + " |")
            L.append("| **saturation** (highest step with p95 < 100 ms, 0 errors) | " + " | ".join(str(sat.get(s, "none")) for s in SERVERS) + " |")
            L.append("")
        # mixed
        L += ["### Mixed load: 32 ADBC small-query clients alone / with 2 heavy SF10 streams (q01, q18)", "",
              "| metric | " + " | ".join(SERVERS) + " |", "|---|" + "---|" * len(SERVERS)]
        mix = collections.defaultdict(lambda: collections.defaultdict(list))
        for m, ref, sides in js:
            if "mixed" not in m.get("workloads", ""):
                continue
            for s, rounds in sides.items():
                for r in rounds:
                    for k in ("mixed-base", "mixed-small"):
                        x = lat_csv(os.path.join(r, k + ".csv"))
                        if x:
                            mix[s][k + "-qps"].append((x["n"] - x["err"]) / 60.0)
                            mix[s][k + "-p95"].append(x["p95"])
                            mix[s][k + "-err"].append(x["err"])
                    p = os.path.join(r, "mixed-heavy.txt")
                    for line in open(p) if os.path.exists(p) else []:
                        x = line.split()
                        if len(x) >= 7:
                            ok = x[3] == "ok" and ref.get(x[1], {}).get("checksum") in (None, x[6])
                            mix[s][x[1] + ("" if ok else "-bad")].append(float(x[4]))
        for k, lab, n in (("mixed-base-qps", "small QPS alone", 0), ("mixed-small-qps", "small QPS with heavy", 0),
                          ("mixed-base-p95", "small p95 ms alone", 1), ("mixed-small-p95", "small p95 ms with heavy", 1),
                          ("q01", "heavy q01 s (median of runs during the window)", 2), ("q18", "heavy q18 s", 2)):
            L.append(f"| {lab} | " + " | ".join(f(med(mix[s][k]), n) for s in SERVERS) + " |")
        L.append("| small errors alone / with heavy; heavy failures or wrong answers | " + " | ".join(
            f"{sum(mix[s]['mixed-base-err'])} / {sum(mix[s]['mixed-small-err'])}; {len(mix[s]['q01-bad']) + len(mix[s]['q18-bad'])}" if mix[s] else "n/a"
            for s in SERVERS) + " |")
        L.append("")
        # heavy4a and netem
        L += ["### 4 heavy SF10 queries at once (q01 q09 q18 q21, ADBC) and network-limited client path (netem 10 ms RTT, 1 Gbit/s)", "",
              "| metric | " + " | ".join(SERVERS) + " |", "|---|" + "---|" * len(SERVERS)]
        hv = collections.defaultdict(lambda: collections.defaultdict(list))
        for m, ref, sides in js:
            for s, rounds in sides.items():
                for r in rounds:
                    if "heavy4a" in m.get("workloads", ""):
                        ts, bad = [], 0
                        for q in ("q01", "q09", "q18", "q21"):
                            x = (tsv(os.path.join(r, f"heavy4a-{q}", "summary.tsv")) or {}).get(q)
                            if x and x["status"] == "ok" and ref.get(q, {}).get("checksum") in (None, x["checksum"]):
                                ts.append(float(x["cold_s"]))
                            else:
                                bad += 1
                        hv[s]["h4-slow"].append(max(ts) if ts and not bad else None)
                        hv[s]["h4-bad"].append(bad)
                        hv[s]["h4-rss"].append(rss_at(r, "heavy4a")[1])
                    if "netem" in m.get("workloads", ""):
                        d = tsv(os.path.join(r, "netem10", "summary.tsv"))
                        if d:
                            good = [q for q in ref if q in d and d[q]["status"] == "ok" and d[q]["checksum"] == ref[q]["checksum"]]
                            hv[s]["nt-sum"].append(sum(float(d[q]["median_s"]) for q in good))
                            hv[s]["nt-ok"].append(len(good))
                        txt = open(os.path.join(r, "result.txt")).read() if os.path.exists(os.path.join(r, "result.txt")) else ""
                        mm = re.search(r"^netem adbcscan .*?mb_per_s=([\d.]+) errors=(\d+)", txt, re.M)
                        if mm and not int(mm.group(2)):
                            hv[s]["nt-scan"].append(float(mm.group(1)))
        L.append("| heavy x4: slowest query s (n/a if any failed) | " + " | ".join(f(med(hv[s]["h4-slow"]), 1) for s in SERVERS) + " |")
        L.append("| heavy x4: failed or wrong (all rounds) | " + " | ".join(str(sum(hv[s]["h4-bad"])) if hv[s]["h4-bad"] else "n/a" for s in SERVERS) + " |")
        L.append("| heavy x4: server peak RSS MiB | " + " | ".join(f(max((x for x in hv[s]["h4-rss"] if x), default=None)) for s in SERVERS) + " |")
        L.append("| netem: SF10 TPC-H ADBC, sum of warm medians s (correct queries) | " + " | ".join(
            f"{f(med(hv[s]['nt-sum']), 1)} ({min(hv[s]['nt-ok'])}/22 q)" if hv[s]["nt-sum"] else "n/a" for s in SERVERS) + " |")
        L.append("| netem: full lineitem export over ADBC, MB/s | " + " | ".join(f(med(hv[s]["nt-scan"])) for s in SERVERS) + " |")
        L.append("")
    if not any(m["setting"] == "zstd" for m, _, _ in jobs):
        L += ["Not in this run: up-native with its ZSTD Flight compression on the netem path (job `new-vs-native-zstd-netem`).", ""]
    L += ["Not yet in this report: TLS + token on/off for ours.", ""]
    open(dst, "w").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
