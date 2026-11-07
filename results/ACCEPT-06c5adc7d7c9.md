# HDFS acceptance (SASL): `server-1.0.0-06c5adc7d7c9`

Run [42351380956](https://github.com/C0fuge/egret/actions/runs/42351380956), workflow `accept-hdfs.yml`, checks from `ci/BUILD-TRACK-TASK.md` "SASL HDFS ACCEPTANCE" (this repo's queries, layout and checks, `ci/accept/`).

**Verdict: SHIP**

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

## Note: check 4 options and coverage (session note, 2026-11-07)

- Run 42351380956 was dispatched by a session (no release-watcher run existed for the tag ~25 min after publication);
  harness unchanged since ea99fcf. Every check 4 server ran with `-DhdfsLocalCopyDir=/copies
  -DhdfsLocalCopyRoomWaitMillis=30000` (input `smalldisk-opts`), as the SHIP runs since `35c15ab226b9`. Check 4 without
  the room wait was not run on this build.
- Build content: kestrel item 37 (a)-(d): storage refusals (HDFS/Ranger `Permission denied`) as PERMISSION_DENIED, a
  table with unreadable footers no longer fails the server start, failed views retried; stop drain through `StopGate`
  (new calls UNAVAILABLE while running calls finish); multi-table refusal reason without SQL; `hdfs=noTicketCache` WARN.
  None of these is exercised by this harness (no denied table, no stop under load, no missing ticket cache): the result
  shows that item 37 did not break checks 1-6. No FRESH wave: the new code is on the HDFS denial / stop path, not
  exercised by the local/S3 waves.
