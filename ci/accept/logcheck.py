"""Check 6 helper of ci/accept/cluster.sh: matches the server's hdfs=reads lines to its queries by qid.

  logcheck.py <server log>...

Every query a server runs writes one execution-path event (`[execution-path-log] ... qid=<q> node=<n>
executionPath=<p> ... event={json}`); a query whose files the server inspected writes
`qid=<q> node=<n> hdfs=reads files=...`. Prints one line:
  queries=<qids with an event> reads=<qids with an hdfs=reads line> missing=<qids without one>
  [paths=<execution path>:<count>,...] [sample=<path> <digest10> <failure reason>; ...]
Matching by qid (any node) instead of comparing totals: distributed sub-queries on other nodes would
otherwise inflate the count and hide a query without a line.
"""
import collections
import json
import re
import sys

EVENT = re.compile(r"\[execution-path-log\].* qid=(\S+) node=\S+ executionPath=(\S+) .*?event=(\{.*\})\s*$")
READS = re.compile(r" qid=(\S+) node=\S+ hdfs=reads ")


def main(paths):
    events, reads = {}, set()
    for p in paths:
        try:
            lines = open(p, errors="replace").read().splitlines()
        except OSError:
            continue
        for line in lines:
            m = EVENT.search(line)
            if m:
                try:
                    ev = json.loads(m.group(3))
                except ValueError:
                    ev = {}
                events.setdefault(m.group(1), (m.group(2), ev))
                continue
            m = READS.search(line)
            if m:
                reads.add(m.group(1))
    missing = [q for q in events if q not in reads]
    out = f"queries={len(events)} reads={len(set(events) & reads)} missing={len(missing)}"
    if missing:
        paths_count = collections.Counter(events[q][0] for q in missing)
        out += " paths=" + ",".join(f"{k}:{v}" for k, v in paths_count.most_common())
        sample = []
        for q in missing[:3]:
            path, ev = events[q]
            reason = (ev.get("failure_reason") or ev.get("reason") or "ok")[:80]
            sample.append(f"{path} {str(ev.get('query_digest', ''))[:10]} {reason}")
        out += " sample=" + "; ".join(sample)
    print(out.replace("|", "/"))


if __name__ == "__main__":
    main(sys.argv[1:])
