"""aggregate.py <artifacts-dir> <out-dir> <title>: one table row per A/B job (variant vs default on the same runner).

Every job artifact holds A/r<N>/ and B/r<N>/ (ab.sh) and job.json ({"variant", "flags", "layout", "storage"}).
Per side: median over rounds of p50/p95 small-query latency (JDBC and ADBC at 1/8/32 clients), TPC-H SF1/SF10 sums of
warm medians, full lineitem scan MB/s at 1 and 4 concurrent scans, heavy4 (q01 q09 q18 q21 at once) slowest query,
peak RSS. Ratio = B / A (< 1 is faster for times, > 1 is faster for MB/s). Correctness gate: TPC-H answer md5 of both
sides equals the reference (SF10 9e2af63e8711, SF1 de713f9eea2f), small-query answer signatures equal, no failures.
"""
import csv
import glob
import json
import os
import re
import statistics as st
import sys

REF = {"jdbc10": "9e2af63e8711", "jdbc1": "de713f9eea2f"}


def pct(xs, q):
    xs = sorted(xs)
    if not xs:
        return None
    k = (len(xs) - 1) * q
    i = int(k)
    return xs[i] if i + 1 >= len(xs) else xs[i] + (xs[i + 1] - xs[i]) * (k - i)


def med(xs):
    xs = [x for x in xs if x is not None]
    return st.median(xs) if xs else None


def small(d, client, conc):
    p = os.path.join(d, f"small-{client}-c{conc}.csv")
    if not os.path.exists(p):
        return None
    rows = list(csv.DictReader(open(p)))
    lat = [float(r["lat_ms"]) for r in rows if r["ok"] == "1"]
    sig = {}
    for r in rows:
        a = sig.setdefault(r["class"], [0, 0.0])
        a[0] += int(r["rows"])
        a[1] += float(r["val"])
    return {"p50": pct(lat, .5), "p95": pct(lat, .95), "err": sum(1 for r in rows if r["ok"] != "1"),
            "sig": ";".join(f"{k}:{v[0]}:{v[1]:.0f}" for k, v in sorted(sig.items()))}


def side_round(d):
    txt = open(os.path.join(d, "result.txt")).read() if os.path.exists(os.path.join(d, "result.txt")) else ""
    r = {"fails": []}
    if "START FAILED" in txt:
        r["fails"].append("start failed")
    if "SERVER DIED" in txt:
        r["fails"].append("server died")
    for c in (1, 8, 32):
        for cl in ("jdbc", "adbc"):
            s = small(d, cl, c)
            r[f"{cl}{c}"] = s
            if s and s["err"]:
                r["fails"].append(f"{cl}{c} {s['err']} errors")
    for n in ("jdbc10", "jdbc1"):
        m = re.search(rf"^{n}: ok=(\d+) cold_sum=([\d.]+) median_sum=([\d.]+) md5=(\w+)", txt, re.M)
        if m:
            r[n] = {"ok": int(m.group(1)), "cold": float(m.group(2)), "med": float(m.group(3)), "md5": m.group(4)}
            if m.group(4) != REF[n]:
                r["fails"].append(f"{n} md5 {m.group(4)} ({m.group(1)}/22 ok)")
    for m in re.finditer(r"^scan conc=(\d+) .*?rows=(\d+) mb=\d+ rows_per_s=\d+ mb_per_s=([\d.]+).*?errors=(\d+)", txt, re.M):
        r[f"scan{m.group(1)}"] = float(m.group(3))
        if int(m.group(4)) or int(m.group(2)) % 59986052:
            r["fails"].append(f"scan{m.group(1)} rows={m.group(2)} errors={m.group(4)}")
    m = re.search(r"^heavy4: (.*)$", txt, re.M)
    if m:
        qs = re.findall(r"(q\d\d)=(\w+)/([\d.]+)/", m.group(1))
        r["heavy4"] = max([float(q[2]) for q in qs], default=None)
        if sum(1 for q in qs if q[1] == "ok") != 4:
            r["fails"].append("heavy4 failures")
    hw = [int(x) for x in re.findall(r"hwm=(\d+)", open(os.path.join(d, "mem.txt")).read())] if os.path.exists(os.path.join(d, "mem.txt")) else []
    r["rss"] = max(hw, default=None)
    return r


def side(job, s):
    rs = [side_round(d) for d in sorted(glob.glob(os.path.join(job, s, "r*")))]
    out = {"n": len(rs), "fails": sorted({f for r in rs for f in r["fails"]}),
           "sig": {r["jdbc1"]["sig"] for r in rs if r.get("jdbc1")}}
    for c in (1, 8, 32):
        for cl in ("jdbc", "adbc"):
            out[f"{cl}{c}_p50"] = med([r[f"{cl}{c}"]["p50"] for r in rs if r.get(f"{cl}{c}")])
            out[f"{cl}{c}_p95"] = med([r[f"{cl}{c}"]["p95"] for r in rs if r.get(f"{cl}{c}")])
    for n in ("jdbc10", "jdbc1"):
        out[n] = med([r[n]["med"] for r in rs if r.get(n)])
    for k in ("scan1", "scan4", "heavy4"):
        out[k] = med([r.get(k) for r in rs])
    out["rss"] = max([r["rss"] for r in rs if r["rss"]], default=None)
    return out


def ratio(b, a):
    return None if a in (None, 0) or b is None else b / a


def fmt(x, n=2):
    return "-" if x is None else f"{x:.{n}f}"


def main():
    src, dst, title = sys.argv[1], sys.argv[2], sys.argv[3]
    os.makedirs(dst, exist_ok=True)
    rows = []
    for job in sorted(glob.glob(os.path.join(src, "*"))):
        meta = json.load(open(os.path.join(job, "job.json"))) if os.path.exists(os.path.join(job, "job.json")) else {"variant": os.path.basename(job)}
        a, b = side(job, "A"), side(job, "B")
        if not a["n"] or not b["n"]:
            rows.append((meta, a, b, "no rounds"))
            continue
        gate = []
        if a["fails"] or b["fails"]:
            gate.append("A: " + ", ".join(a["fails"]) if a["fails"] else "")
            gate.append("B: " + ", ".join(b["fails"]) if b["fails"] else "")
        if a["sig"] and b["sig"] and a["sig"] != b["sig"]:
            gate.append("small-query answers differ")
        rows.append((meta, a, b, "; ".join(g for g in gate if g) or "OK"))
    keys = [("jdbc1_p50", "small JDBC c1 p50"), ("jdbc1_p95", "c1 p95"), ("jdbc32_p95", "c32 p95"), ("adbc1_p50", "ADBC c1 p50"),
            ("adbc32_p95", "ADBC c32 p95"), ("jdbc1", "SF1 JDBC"), ("jdbc10", "SF10 JDBC"), ("scan1", "scan MB/s x1"),
            ("scan4", "scan MB/s x4"), ("heavy4", "heavy4 max"), ("rss", "RSS peak")]
    lines = [f"# {title}", "", "Ratio = variant / default on the same runner (median of rounds per side). Times: < 1 = variant faster;",
             "scan MB/s: > 1 = variant faster; RSS: < 1 = variant smaller. Absolute default values in the second table.", "",
             "| variant | storage | layout | flags | rounds A/B | " + " | ".join(k[1] for k in keys) + " | correctness |",
             "|" + "---|" * (6 + len(keys))]
    for meta, a, b, gate in rows:
        cells = [fmt(ratio(b.get(k), a.get(k))) for k, _ in keys]
        lines.append(f"| {meta.get('variant')} | {meta.get('storage', '')} | {meta.get('layout', 'default')} | `{meta.get('flags', '') or '-'}` | "
                     f"{a['n']}/{b['n']} | " + " | ".join(cells) + f" | {gate} |")
    lines += ["", "Absolute values (default side A / variant side B; ms, s, MB/s, MB):", "",
              "| variant | " + " | ".join(k[1] for k in keys) + " |", "|" + "---|" * (1 + len(keys))]
    for meta, a, b, gate in rows:
        lines.append(f"| {meta.get('variant')} | " + " | ".join(f"{fmt(a.get(k), 1)} / {fmt(b.get(k), 1)}" for k, _ in keys) + " |")
    open(os.path.join(dst, "summary.md"), "w").write("\n".join(lines) + "\n")
    with open(os.path.join(dst, "summary.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["variant", "storage", "layout", "flags", "rounds_a", "rounds_b"] + [f"{k}_{s}" for k, _ in keys for s in ("a", "b", "ratio")] + ["correctness"])
        for meta, a, b, gate in rows:
            w.writerow([meta.get("variant"), meta.get("storage"), meta.get("layout"), meta.get("flags"), a["n"], b["n"]]
                       + [v for k, _ in keys for v in (a.get(k), b.get(k), ratio(b.get(k), a.get(k)))] + [gate])
    print("\n".join(lines))


if __name__ == "__main__":
    main()
