# HDFS acceptance (SASL): `server-1.0.0-50fe065af50c`

Run [42055012677](https://github.com/C0fuge/egret/actions/runs/42055012677), workflow `accept-hdfs.yml`, checks from `ci/BUILD-TRACK-TASK.md` "SASL HDFS ACCEPTANCE" (this repo's queries, layout and checks, `ci/accept/`).

**Verdict: DO NOT SHIP**

Check 4 detail (kestrel item 33; harness unchanged since `5f60db1ee304`, a5a0469): copies are now batched for the scans and some aggregates (17-75 copy batches per cell, peak tmpfs use 56369152 of 67108864 bytes, never full, no "No space left"), and the over-size join (`sp-join-lineitem`, 13 copies, 212 MB) is an allowed RESOURCE_EXHAUSTED refusal. **Still failing in all 4 cells: complete `sp-group` and `sp-distinct` (9 copies, ~156 MB) are refused outright ("Nothing was copied") instead of running in copy batches.** New in this build: the refusal says "copies in use by running queries take 51955890 bytes" (about 3 lineitem_sp files) although the client sends one query at a time and every earlier stream was read to the end and closed; with `5f60db1ee304` the same refusal saw all 67108864 bytes free. So copies of finished queries stay pinned (likely the item 33 "reused copies pinned first" path). In the speed cells this also refuses the partial `part-lineitem-sp` and `part-group-sp` (1 copy, 17 MB, with ~15 MB free), which passed on `5f60db1ee304`. Checks 1, 2, 3, 5, 6 pass in every cell.

Cluster: Hadoop 3.1.3, 2 NameNodes HA (ZooKeeper + ZKFC), Kerberos KDC, 3 DataNodes with `dfs.data.transfer.protection=authentication`, short-circuit socket, one Flight server per DataNode in its network namespace, Flight with Kerberos auth + TLS. Answers compared with the same build on DataNodes without data-transfer protection and with in-process DuckDB over the same files.

| check | default x 1 | default x 3 | speed x 1 | speed x 3 |
|---|---|---|---|---|
| 1-tpch-plain | pass 22/22 | pass 66/66 | pass 22/22 | pass 66/66 |
| 1-tpch-schema | pass 22/22 | pass 22/22 | pass 22/22 | pass 22/22 |
| 2-spread | pass 17/17 | pass 47/47 | pass 17/17 | pass 47/47 |
| 3-partial | n/a | pass | n/a | pass |
| 4-smalldisk | **FAIL** | **FAIL** | **FAIL** | **FAIL** |
| 5-lowdirect | n/a | n/a | n/a | pass |
| 6-logs | pass | pass | pass | pass |

Checks: 1 TPC-H 22/22 plain names and schema-qualified; 2 spread set (plain names; count, full scans, GROUP BY, ORDER BY LIMIT, HAVING, count(DISTINCT), comma join, JOIN ON, q03/q12; part_far whose first file is on dn3 only); 3 partial mode per-node sums = complete (3 servers); 4 `-DhdfsLocalCopyDir` on a 64 MiB tmpfs; 5 3 servers speed + `distributedComplete=true`, `-XX:MaxDirectMemorySize=512m`, 4 full scans of the 12-file lineitem; 6 server logs (`hdfs=reads` per query, short-circuit fd counters grow, no `HdfsNetworkException`).

## Failures

- `default` x 1: **4-smalldisk**: sp-group@n1@complete: [gRPC ResourceExhausted] InternalError: INTERNAL: [FlightSQL] No room on the disk of the node-local copy cache /copies/duckdb-1-17957107412941605315 for this query's 9 file copies (155906121 bytes, e.g. spread/lineitem_sp/part-00.parquet): 15147008 bytes are free and 6710880 must stay free (hdfsLocalCopyMinFreeBytes); copies in use by running queries take 51955890 bytes. Nothing was copied; retry when other queries end, o; sp-distinct@n1@complete: [gRPC ResourceExhausted] InternalError: INTERNAL: [FlightSQL] No room on the disk of the node-local copy cache /copies/duckdb-
- `default` x 3: **4-smalldisk**: sp-group@n1@complete: [gRPC ResourceExhausted] InternalError: INTERNAL: [FlightSQL] No room on the disk of the node-local copy cache /copies/duckdb-1-5552034732008884308 for this query's 9 file copies (155906121 bytes, e.g. spread/lineitem_sp/part-00.parquet): 15147008 bytes are free and 6710880 must stay free (hdfsLocalCopyMinFreeBytes); copies in use by running queries take 51955890 bytes. Nothing was copied; retry when other queries end, or; sp-distinct@n1@complete: [gRPC ResourceExhausted] InternalError: INTERNAL: [FlightSQL] No room on the disk of the node-local copy cache /copies/duckdb-
- `speed` x 1: **4-smalldisk**: sp-group@n1@complete: [gRPC ResourceExhausted] InternalError: INTERNAL: [FlightSQL] No room on the disk of the node-local copy cache /copies/duckdb-1-7932806205823759955 for this query's 9 file copies (155906121 bytes, e.g. spread/lineitem_sp/part-00.parquet): 15147008 bytes are free and 6710880 must stay free (hdfsLocalCopyMinFreeBytes); copies in use by running queries take 51955890 bytes. Nothing was copied; retry when other queries end, or; sp-distinct@n1@complete: [gRPC ResourceExhausted] InternalError: INTERNAL: [FlightSQL] No room on the disk of the node-local copy cache /copies/duckdb-
- `speed` x 3: **4-smalldisk**: sp-group@n1@complete: [gRPC ResourceExhausted] InternalError: INTERNAL: [FlightSQL] No room on the disk of the node-local copy cache /copies/duckdb-1-16736447884973181713 for this query's 9 file copies (155906121 bytes, e.g. spread/lineitem_sp/part-00.parquet): 15147008 bytes are free and 6710880 must stay free (hdfsLocalCopyMinFreeBytes); copies in use by running queries take 51955890 bytes. Nothing was copied; retry when other queries end, o; sp-distinct@n1@complete: [gRPC ResourceExhausted] InternalError: INTERNAL: [FlightSQL] No room on the disk of the node-local copy cache /copies/duckdb-

## Reference cells

- reference `default` x 1: setup pass, 61 answers, 0 errors
- reference `default` x 3: setup pass, 135 answers, 0 errors
- reference `speed` x 1: setup pass, 61 answers, 0 errors
- reference `speed` x 3: setup pass, 135 answers, 0 errors

Raw logs: run artifacts `cell-*`.
