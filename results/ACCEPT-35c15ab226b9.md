# HDFS acceptance (SASL): `server-1.0.0-35c15ab226b9`

Run [42196478105](https://github.com/C0fuge/egret/actions/runs/42196478105), workflow `accept-hdfs.yml`, checks from `ci/BUILD-TRACK-TASK.md` "SASL HDFS ACCEPTANCE" (this repo's queries, layout and checks, `ci/accept/`).

**Verdict: SHIP** (with `-DhdfsLocalCopyRoomWaitMillis=30000` on every check 4 server; see the note on the run without it)

Cluster: Hadoop 3.1.3, 2 NameNodes HA (ZooKeeper + ZKFC), Kerberos KDC, 3 DataNodes with `dfs.data.transfer.protection=authentication`, short-circuit socket, one Flight server per DataNode in its network namespace, Flight with Kerberos auth + TLS. Answers compared with the same build on DataNodes without data-transfer protection and with in-process DuckDB over the same files.

| check | default x 1 | default x 3 | speed x 1 | speed x 3 |
|---|---|---|---|---|
| 1-tpch-plain | pass 22/22 | pass 66/66 | pass 22/22 | pass 66/66 |
| 1-tpch-schema | pass 22/22 | pass 22/22 | pass 22/22 | pass 22/22 |
| 2-spread | pass 17/17 | pass 47/47 | pass 17/17 | pass 47/47 |
| 3-partial | n/a | pass | n/a | pass |
| 4-smalldisk | pass | pass | pass | pass |
| 5-lowdirect | n/a | n/a | n/a | pass |
| 6-logs | pass | pass | pass | pass |

Checks: 1 TPC-H 22/22 plain names and schema-qualified; 2 spread set (plain names; count, full scans, GROUP BY, ORDER BY LIMIT, HAVING, count(DISTINCT), comma join, JOIN ON, q03/q12; part_far whose first file is on dn3 only); 3 partial mode per-node sums = complete (3 servers); 4 `-DhdfsLocalCopyDir` on a 64 MiB tmpfs; 5 3 servers speed + `distributedComplete=true`, `-XX:MaxDirectMemorySize=512m`, 4 full scans of the 12-file lineitem; 6 server logs (`hdfs=reads` per query, short-circuit fd counters grow, no `HdfsNetworkException`).

## Reference cells

- reference `default` x 1: setup pass, 61 answers, 0 errors
- reference `default` x 3: setup pass, 135 answers, 0 errors
- reference `speed` x 1: setup pass, 61 answers, 0 errors
- reference `speed` x 3: setup pass, 135 answers, 0 errors

Raw logs: run artifacts `cell-*`.

## Note: check 4 with and without the item 33 room wait (session note, 2026-11-06)

- This run (42196478105, harness a06ac49) started every check 4 server with `-DhdfsLocalCopyDir=/copies
  -DhdfsLocalCopyRoomWaitMillis=30000` (input `smalldisk-opts`). All checks pass in all 4 cells: verdict SHIP.
- The earlier watcher run [42113544966](https://github.com/C0fuge/egret/actions/runs/42113544966) (harness 66aed33)
  started them WITHOUT the room wait: checks 1, 2, 3, 5, 6 passed everywhere and check 4 passed in both default cells,
  but **failed in both speed cells**: partial `part-lineitem-sp` / `part-group-sp` refused with ResourceExhausted, the
  refusal counting ~52 MB as "copies in use by other running queries". The room wait is opt-in in this build, so with
  the shipped defaults the speed profile on a small copy disk still refuses these partial queries.
