"""robust_report.py <jobs-dir> <out.md> <run id>: Report 3 (ROBUSTNESS) of the 4-server comparison from the compare jobs
(waves c4-robust: soak, cold start, cancel; c5-threads: ours-new duckDbThreads sweep). Same containers as Reports 1 and 2.
- soak: 30 min, 32 ADBC small-query clients in 6 x 5-min segments + 1 heavy stream (q01 / q18 alternating); RSS, heap,
  GC and threads every 10 s; p95 per segment (latency drift = last / first segment), errors, heavy query times;
- cold start: 5 starts on SF10: port answers, server log "started", first query (connect + SELECT version()), idle RSS;
- cancel: SF10 q18 / q21 / lagg (single-table lineitem aggregation) cancelled from the client after 1 s: client return time and the time until the server process
  CPU falls below 0.1 core for 1 s (server-side evidence the work stopped);
- threads: ours-new duckDbThreads 4 (A) vs 1 / 2 / 8 (B) on the same runner: TPC-H SF1 / SF10 ADBC sums, small c1 / c32 p50;
- cluster: 3-node cluster on one runner, A and B sides of each job (flags may differ, e.g. distributedComplete off / on):
  SF10 ADBC wall time and correct answers per check (all up, node 3 stopped, node 3 back, ...) and the event lines per round.
"""
import collections
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from load_report import lat_csv  # noqa: E402
from speed_report import SERVERS, f, med, small, tsv  # noqa: E402


def load(src):
    jobs = []
    for job in sorted(glob.glob(os.path.join(src, "*"))):
        if not os.path.exists(os.path.join(job, "job.json")):
            continue
        m = json.load(open(os.path.join(job, "job.json")))
        ref = {n: tsv(os.path.join(job, "ref", n, "summary.tsv")) or {} for n in ("adbc1", "adbc10")}
        sides = {}
        for s in "AB":
            name = m.get(f"name_{s.lower()}") or m.get(f"server_{s.lower()}")
            fl = m.get(f"flags_{s.lower()}") or ""
            mm = re.search(r"duckDbThreads=(\d+)", fl)
            key = f"{name} t{mm.group(1)}" if m["variant"].startswith("threads") else name
            if m["variant"].startswith("threads") and not mm:
                key = f"{name} t4"
            sides[key] = sorted(glob.glob(os.path.join(job, s, "r*")))
        jobs.append((m, ref, sides))
    return jobs


def soak(rounds):
    out = collections.defaultdict(list)
    for r in rounds:
        p = os.path.join(r, "soak-jvm.txt")
        if not os.path.exists(p):
            continue
        rss, heap, gcn, gct, thr, freq = [], [], {}, {}, [], 1e9
        for line in open(p):
            m = re.match(r"== (\d+) .*?VmRSS:\s*(\d+) kB.*?Threads:\s*(\d+)", line)
            if m:
                rss.append(int(m.group(2)) // 1024)
                thr.append(int(m.group(3)))
            m = re.search(r"garbage-first heap\s+total (\d+)K, used (\d+)K", line) or re.search(r"heap\s+total (\d+)K, used (\d+)K", line)
            if m:
                heap.append(int(m.group(2)) // 1024)
            m = re.match(r"sun\.gc\.collector\.(\d)\.(invocations|time)=(\d+)", line.strip())
            if m:
                (gcn if m.group(2) == "invocations" else gct)[m.group(1)] = int(m.group(3))
            m = re.match(r"sun\.os\.hrt\.frequency=(\d+)", line.strip())
            if m:
                freq = int(m.group(1))
        if rss:
            out["rss_first"].append(rss[0]); out["rss_last"].append(rss[-1]); out["rss_max"].append(max(rss))
            out["thr_max"].append(max(thr))
        if heap:
            out["heap_max"].append(max(heap))
        if gcn:
            out["gc_n"].append(sum(gcn.values()))
            out["gc_s"].append(sum(gct.values()) / freq)
        segs = [lat_csv(os.path.join(r, f"soak-seg{i}.csv")) for i in range(1, 7)]
        segs = [x for x in segs if x]
        if segs:
            out["p95_first"].append(segs[0]["p95"]); out["p95_last"].append(segs[-1]["p95"])
            out["qps"].append(med([(x["n"] - x["err"]) / 300.0 for x in segs]))
            out["err"].append(sum(x["err"] for x in segs))
            out["segs"].append(len(segs))
        p = os.path.join(r, "soak-heavy.txt")
        for line in open(p) if os.path.exists(p) else []:
            x = line.split()
            if len(x) >= 5:
                if x[3] == "ok":
                    out["heavy_" + x[1]].append(float(x[4]))
                else:
                    out["heavy_fail"].append(1)
        txt = open(os.path.join(r, "result.txt")).read() if os.path.exists(os.path.join(r, "result.txt")) else ""
        out["died"].append(1 if "SERVER DIED" in txt else 0)
    return out


def cold(rounds):
    out = collections.defaultdict(list)
    for r in rounds:
        p = os.path.join(r, "start-times.txt")
        txt = open(p).read() if os.path.exists(p) else ""
        part = txt.split("== cold 1", 1)[1] if "== cold 1" in txt else ""
        out["port"] += [int(x) for x in re.findall(r"port_ms=(\d+)", part)]
        out["started"] += [int(x) for x in re.findall(r"started_s=(\d+)ms", part)]
        out["first"] += [int(x) for x in re.findall(r"first_query_ms=(\d+)", part)]
        mp = os.path.join(r, "mem.txt")
        for line in open(mp) if os.path.exists(mp) else []:
            m = re.match(r"cold\d+ rss=(\d+)", line)
            if m:
                out["idle_rss"].append(int(m.group(1)))
    return out


def cancel(rounds, q):
    out = collections.defaultdict(list)
    for r in rounds:
        txt = open(os.path.join(r, "result.txt")).read() if os.path.exists(os.path.join(r, "result.txt")) else ""
        m = re.search(rf"^cancel query={q} sent=(\S+) returned=(\S+) return_s=(\S+) outcome=(\S+)(.*)$", txt, re.M)
        if not m:
            continue
        out["outcome"].append(m.group(4) + (f" ({m.group(5).strip()[:70]})" if m.group(4) != "cancelled" else ""))
        if m.group(3) != "n/a":
            out["ret"].append(float(m.group(3)))
        if m.group(1) == "none":
            continue
        sent = float(m.group(1))
        samples = []
        p = os.path.join(r, f"cancel-{q}-cpu.txt")
        for line in open(p) if os.path.exists(p) else []:
            x = line.split()
            if len(x) == 3:
                samples.append((float(x[0]), int(x[1]) + int(x[2])))
        drop = None
        for i in range(1, len(samples)):
            if samples[i][0] < sent:
                continue
            # first point after the cancel from which the CPU rate stays < 0.1 core for >= 1 s
            j = i
            while j < len(samples) and samples[j][0] - samples[i - 1][0] < 1.0:
                j += 1
            if j >= len(samples):
                break
            rate = (samples[j][1] - samples[i - 1][1]) / 100.0 / (samples[j][0] - samples[i - 1][0])
            if rate < 0.1:
                drop = samples[i - 1][0] - sent
                break
        out["drop"].append(max(drop, 0.0) if drop is not None else None)
    return out


def cluster(src):
    """Cluster tables straight from each round's result.txt (sides A / B kept apart: both may run the same build)."""
    L = []
    for job in sorted(glob.glob(os.path.join(src, "*"))):
        if not os.path.exists(os.path.join(job, "job.json")):
            continue
        m = json.load(open(os.path.join(job, "job.json")))
        if "cluster" not in m.get("workloads", ""):
            continue
        L += [f"## 3-node cluster: {m['variant']} ({m.get('storage', '?')})", ""]
        for s in "AB":
            lab = f"{m.get(f'name_{s.lower()}') or m.get(f'server_{s.lower()}')} `{m.get(f'flags_{s.lower()}') or '-'}`"
            checks, events = collections.OrderedDict(), []
            rounds = sorted(glob.glob(os.path.join(job, s, "r*")))
            for r in rounds:
                rp = os.path.join(r, "result.txt")
                lines = open(rp).read().splitlines() if os.path.exists(rp) else []
                rn = os.path.basename(r)
                for ln in lines:
                    mm = re.match(r"cluster ([\w-]+): wall_s=([\d.]+) queries=(\d+) ok=(\d+) correct=(\d+) failed=\[(.*)\]", ln)
                    if mm:
                        checks.setdefault(mm.group(1), []).append((rn, float(mm.group(2)), mm.group(3), mm.group(4), mm.group(5), mm.group(6).strip()))
                    elif ln.startswith("cluster"):
                        events.append(f"{rn}: {ln[:220]}")
            L += [f"Side {s} = {lab}, rounds with data: {len(rounds)}", "",
                  "| check | wall s median | per round wall s | correct / queries per round | failed |", "|---|---|---|---|---|"]
            for k, v in checks.items():
                L.append(f"| {k} | {f(med([x[1] for x in v]), 1)} | " + " ".join(f"{x[0]}={x[1]:.1f}" for x in v)
                         + " | " + " ".join(f"{x[4]}/{x[2]}" for x in v) + " | " + (" ".join(sorted({x[5] for x in v if x[5]})) or "-") + " |")
            L += [""] + [f"- {e}" for e in events] + [""]
    return L


def main():
    src, dst, run = sys.argv[1], sys.argv[2], sys.argv[3]
    jobs = load(src)
    if not jobs:
        print("no jobs")
        return
    srv = jobs[0][0].get("servers", {})
    by = collections.defaultdict(list)
    for m, ref, sides in jobs:
        for name, rounds in sides.items():
            by[name] += rounds
    L = [f"# Server comparison - Report 3: ROBUSTNESS (compare run {run})", "",
         "Same runner type and containers as Reports 1 and 2 (server: `eclipse-temurin:21-jre`, 2 CPUs on cpus 0,1, 6 GB, "
         "`-Xmx3g -XX:MaxDirectMemorySize=2g`; clients on cpus 2,3). Servers: " + "; ".join(f"{k} = `{srv.get(k, '?')}`" for k in SERVERS) + ".", ""]
    if any("soak" in m.get("workloads", "") for m, _, _ in jobs):
        so = {s: soak(by.get(s, [])) for s in SERVERS}
        L += ["## Soak: 30 min, 32 ADBC small-query clients + 1 heavy SF10 stream", "",
              "| metric | " + " | ".join(SERVERS) + " |", "|---|" + "---|" * len(SERVERS)]
        for k, lab, n in (("rss_first", "RSS MiB at start", 0), ("rss_last", "RSS MiB at end", 0), ("rss_max", "RSS MiB max", 0),
                          ("heap_max", "heap used MiB max", 0), ("gc_n", "GC count (30 min)", 0), ("gc_s", "GC time s", 1),
                          ("thr_max", "threads max", 0), ("qps", "small QPS (median segment)", 0), ("p95_first", "small p95 ms, first 5 min", 1),
                          ("p95_last", "small p95 ms, last 5 min", 1), ("heavy_q01", "heavy q01 s (median)", 1), ("heavy_q18", "heavy q18 s (median)", 1)):
            L.append(f"| {lab} | " + " | ".join(f(med(so[s][k]), n) for s in SERVERS) + " |")
        L.append("| errors: small / heavy failed / server died | " + " | ".join(
            f"{sum(so[s]['err'])} / {len(so[s]['heavy_fail'])} / {sum(so[s]['died'])}" if so[s]["segs"] else "n/a" for s in SERVERS) + " |")
        L += ["", "Direct (off-heap) memory is not sampled separately (no NMT in the measured JVM): RSS minus heap is the off-heap estimate.", ""]
    if any("coldstart" in m.get("workloads", "") for m, _, _ in jobs):
        co = {s: cold(by.get(s, [])) for s in SERVERS}
        L += ["## Cold start (SF10 data dir, 5 starts per round)", "",
              "| metric (median) | " + " | ".join(SERVERS) + " |", "|---|" + "---|" * len(SERVERS)]
        for k, lab in (("port", "port answers, ms after `docker run`"), ("started", "'started' log line, ms"),
                       ("first", "first query (connect + SELECT version()), ms"), ("idle_rss", "idle RSS MiB, 5 s after first query")):
            L.append(f"| {lab} | " + " | ".join(f(med(co[s][k])) + (f" (n={len(co[s][k])})" if co[s][k] else "") for s in SERVERS) + " |")
        L.append("")
    if any("cancel" in m.get("workloads", "") for m, _, _ in jobs):
        L += ["## Cancel a running SF10 query after 1 s (ADBC `adbc_cancel`)", "",
              "| query | metric | " + " | ".join(SERVERS) + " |", "|---|---|" + "---|" * len(SERVERS)]
        for q in ("q18", "q21", "lagg"):
            ca = {s: cancel(by.get(s, []), q) for s in SERVERS}
            L.append(f"| {q} | client returns, s after cancel | " + " | ".join(f(med(ca[s]["ret"]), 2) for s in SERVERS) + " |")
            L.append(f"| {q} | server CPU < 0.1 core, s after cancel | " + " | ".join(
                (f(med([x for x in ca[s]["drop"] if x is not None]), 2) + (f" ({ca[s]['drop'].count(None)} never)" if None in ca[s]["drop"] else ""))
                if ca[s]["drop"] else "n/a" for s in SERVERS) + " |")
            L.append(f"| {q} | outcome | " + " | ".join(", ".join(sorted(set(ca[s]["outcome"]))) or "n/a" for s in SERVERS) + " |")
        L.append("")
    tj = [(m, ref, sides) for m, ref, sides in jobs if m["variant"].startswith("threads")]
    if tj:
        keys = ["ours-new t1", "ours-new t2", "ours-new t4", "ours-new t8"]
        L += ["## ours-new `duckDbThreads` sweep (2-CPU container)", "",
              "t4 runs in every job (side A); each other value is its own same-runner pair against t4.", "",
              "| metric | " + " | ".join(k.split()[1] for k in keys) + " |", "|---|" + "---|" * len(keys)]
        for w, lab in (("adbc1", "TPC-H SF1 ADBC, sum of warm medians s"), ("adbc10", "TPC-H SF10 ADBC, sum of warm medians s")):
            row = []
            for k in keys:
                sums = []
                for m, ref, sides in tj:
                    for r in sides.get(k, []):
                        d = tsv(os.path.join(r, w, "summary.tsv"))
                        rf = ref.get(w, {})
                        if d and rf and all(q in d and d[q]["status"] == "ok" and d[q]["checksum"] == rf[q]["checksum"] for q in rf):
                            sums.append(sum(float(d[q]["median_s"]) for q in rf))
                row.append(f(med(sums), 2) + (f" (n={len(sums)})" if sums else ""))
            L.append(f"| {lab} | " + " | ".join(row) + " |")
        for c in (1, 32):
            for cl in ("jdbc", "adbc"):
                row = []
                for k in keys:
                    rs = [r for _, _, sides in tj for r in sides.get(k, [])]
                    x = small(rs, cl, c) if rs else {}
                    p = [v["p50"] for v in x.values() if v.get("n")]
                    row.append(f(med(p), 1) if p else "n/a")
                L.append(f"| small {cl.upper()} c{c}: median of class p50 ms | " + " | ".join(row) + " |")
        L.append("")
    cj = [m for m, _, _ in jobs if "cluster" in m.get("workloads", "")]
    if cj:
        L += cluster(src)
    else:
        L += ["Not in this run (ours only, next session): 3-node cluster on one runner (node stopped before / killed during a query),",
              "Trino SF1 through our plugin, stock Flight SQL JDBC driver TPC-H SF1 (see Report 1 JDBC tables: upstream fails there).", ""]
    open(dst, "w").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
