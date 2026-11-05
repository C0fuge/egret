"""Report of an accept-hdfs.yml run: results/ACCEPT-<id>.md.

  report.py <cells dir> <in dir with expected.json> <id> <run id> <out.md>

<cells dir>/cell-<prot>-<profile>-<n>/ holds cell.json and main.json (ci/accept/cluster.sh). For every
protected cell (sasl) and check: pass / fail / n/a with the first error. Answers (checks 1 and 2) must
equal the reference cell (same build, profile and server count, DataNodes without data-transfer
protection) AND the in-process DuckDB answer over the same files (expected.json); an error, a refusal
or a 0-row answer where the reference has rows is a FAIL. Verdict SHIP only if every check passes.
"""
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import digest  # noqa: E402

GROUPS = [("1-tpch-plain", ("tpch-plain-",)), ("1-tpch-schema", ("tpch-schema-",)),
          ("2-spread", ("sp-", "far-", "scan-"))]
CHECKS = [g for g, _ in GROUPS] + ["3-partial", "4-smalldisk", "5-lowdirect", "6-logs"]


def load(d, name):
    try:
        return json.load(open(os.path.join(d, name)))
    except (OSError, ValueError):
        return None


def compare(group_prefixes, sasl, ref, expected):
    """Returns (status, detail, passed, total) for one answer group."""
    keys = sorted(k for k in sasl if k.split("@")[0].startswith(group_prefixes))
    fails = []
    for k in keys:
        qid = k.split("@")[0]
        a, r, e = sasl[k], ref.get(k), expected.get(qid)
        if "error" in a:
            fails.append(f"{k}: {a['error']}")
            continue
        if e and e["rows"] > 0 and a["rows"] == 0:
            fails.append(f"{k}: 0 rows, reference has {e['rows']} (silent wrong answer)")
            continue
        if e and not digest.same(a, e):
            fails.append(f"{k}: rows {a['rows']} / hash {a['hash'][:10]} != DuckDB rows {e['rows']} / {e['hash'][:10]}"
                         f" (head {a['head'][:1]} vs {e['head'][:1]})")
            continue
        if r and "error" not in r and not digest.same(a, r):
            fails.append(f"{k}: differs from the reference cell (rows {a['rows']} vs {r['rows']})")
    if not keys:
        return "fail", "no answers", 0, 0
    return ("fail" if fails else "pass"), "; ".join(fails), len(keys) - len(fails), len(keys)


def main(cells, base, ident, run_id, out):
    expected = json.load(open(os.path.join(base, "expected.json")))
    server_ref = open(os.path.join(base, "SERVER.txt")).read().strip() if os.path.exists(os.path.join(base, "SERVER.txt")) else ident
    rows, all_pass, details, refnotes = [], True, [], []
    for prof in ("default", "speed"):
        for n in (1, 3):
            d = os.path.join(cells, f"cell-sasl-{prof}-{n}")
            rd = os.path.join(cells, f"cell-open-{prof}-{n}")
            cell, main_ans = load(d, "cell.json") or {}, (load(d, "main.json") or {}).get("answers", {})
            rcell, ref_ans = load(rd, "cell.json") or {}, (load(rd, "main.json") or {}).get("answers", {})
            checks = cell.get("checks", {})
            res = {}
            setup = checks.get("setup", {"status": "fail", "detail": "cell did not finish (see the job log)"})
            for g, pre in GROUPS:
                if setup["status"] != "pass" and not main_ans:
                    res[g] = ("fail", "setup: " + setup.get("detail", ""))
                    continue
                st, dt, ok, tot = compare(pre, main_ans, ref_ans, expected)
                res[g] = (st, f"{ok}/{tot}" + (f": {dt}" if dt else ""))
            for c in CHECKS[3:]:
                x = checks.get(c)
                res[c] = (x["status"], x.get("detail", "")) if x else ("fail", "not run: " + setup.get("detail", "cell did not finish"))
            if "client" in checks:
                res["1-tpch-plain"] = ("fail", res["1-tpch-plain"][1] + "; client: " + checks["client"]["detail"])
            for c in CHECKS:
                if res[c][0] not in ("pass", "n/a"):
                    all_pass = False
                    details.append(f"- `{prof}` x {n}: **{c}**: {res[c][1][:700]}")
            rows.append((prof, n, res))
            rs = rcell.get("checks", {}).get("setup", {}).get("status", "missing")
            rerr = sum(1 for a in ref_ans.values() if "error" in a)
            refnotes.append(f"- reference `{prof}` x {n}: setup {rs}, {len(ref_ans)} answers, {rerr} errors")
    lines = [f"# HDFS acceptance (SASL): `{server_ref}`", "",
             f"Run [{run_id}](https://github.com/C0fuge/egret/actions/runs/{run_id}), workflow `accept-hdfs.yml`, "
             "checks from `ci/BUILD-TRACK-TASK.md` \"SASL HDFS ACCEPTANCE\" (this repo's queries, layout and checks, `ci/accept/`).", "",
             f"**Verdict: {'SHIP' if all_pass else 'DO NOT SHIP'}**", "",
             "Cluster: Hadoop 3.1.3, 2 NameNodes HA (ZooKeeper + ZKFC), Kerberos KDC, 3 DataNodes with "
             "`dfs.data.transfer.protection=authentication`, short-circuit socket, one Flight server per DataNode in its network "
             "namespace, Flight with Kerberos auth + TLS. Answers compared with the same build on DataNodes without data-transfer "
             "protection and with in-process DuckDB over the same files.", "",
             "| check | " + " | ".join(f"{p} x {n}" for p, n, _ in rows) + " |",
             "|---|" + "---|" * len(rows)]
    for c in CHECKS:
        cells_txt = []
        for _, _, res in rows:
            st, dt = res[c]
            short = dt.split(":")[0] if c.startswith(("1-", "2-")) else ""
            cells_txt.append(("pass" if st == "pass" else "n/a" if st == "n/a" else "**FAIL**") + (f" {short}" if short else ""))
        lines.append(f"| {c} | " + " | ".join(cells_txt) + " |")
    lines += ["", "Checks: 1 TPC-H 22/22 plain names and schema-qualified; 2 spread set (plain names; count, full scans, GROUP BY, "
              "ORDER BY LIMIT, HAVING, count(DISTINCT), comma join, JOIN ON, q03/q12; part_far whose first file is on dn3 only); "
              "3 partial mode per-node sums = complete (3 servers); 4 `-DhdfsLocalCopyDir` on a 64 MiB tmpfs; 5 3 servers speed + "
              "`distributedComplete=true`, `-XX:MaxDirectMemorySize=512m`, 4 full scans of the 12-file lineitem; 6 server logs "
              "(`hdfs=reads` per query, short-circuit fd counters grow, no `HdfsNetworkException`).", ""]
    if details:
        lines += ["## Failures", ""] + details + [""]
    lines += ["## Reference cells", ""] + refnotes + ["", "Raw logs: run artifacts `cell-*`."]
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main(*sys.argv[1:6])
