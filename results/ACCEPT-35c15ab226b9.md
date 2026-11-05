# HDFS acceptance (SASL): `server-1.0.0-35c15ab226b9`

Run [42113544966](https://github.com/C0fuge/egret/actions/runs/42113544966), workflow `accept-hdfs.yml`, checks from `ci/BUILD-TRACK-TASK.md` "SASL HDFS ACCEPTANCE" (this repo's queries, layout and checks, `ci/accept/`).

**Verdict: DO NOT SHIP**

Cluster: Hadoop 3.1.3, 2 NameNodes HA (ZooKeeper + ZKFC), Kerberos KDC, 3 DataNodes with `dfs.data.transfer.protection=authentication`, short-circuit socket, one Flight server per DataNode in its network namespace, Flight with Kerberos auth + TLS. Answers compared with the same build on DataNodes without data-transfer protection and with in-process DuckDB over the same files.

| check | default x 1 | default x 3 | speed x 1 | speed x 3 |
|---|---|---|---|---|
| 1-tpch-plain | pass 22/22 | pass 66/66 | pass 22/22 | pass 66/66 |
| 1-tpch-schema | pass 22/22 | pass 22/22 | pass 22/22 | pass 22/22 |
| 2-spread | pass 17/17 | pass 47/47 | pass 17/17 | pass 47/47 |
| 3-partial | n/a | pass | n/a | pass |
| 4-smalldisk | pass | pass | **FAIL** | **FAIL** |
| 5-lowdirect | n/a | n/a | n/a | pass |
| 6-logs | pass | pass | pass | pass |

Checks: 1 TPC-H 22/22 plain names and schema-qualified; 2 spread set (plain names; count, full scans, GROUP BY, ORDER BY LIMIT, HAVING, count(DISTINCT), comma join, JOIN ON, q03/q12; part_far whose first file is on dn3 only); 3 partial mode per-node sums = complete (3 servers); 4 `-DhdfsLocalCopyDir` on a 64 MiB tmpfs; 5 3 servers speed + `distributedComplete=true`, `-XX:MaxDirectMemorySize=512m`, 4 full scans of the 12-file lineitem; 6 server logs (`hdfs=reads` per query, short-circuit fd counters grow, no `HdfsNetworkException`).

## Failures

- `speed` x 1: **4-smalldisk**: part-lineitem-sp@n1@partial: [gRPC ResourceExhausted] InternalError: INTERNAL: [FlightSQL] No room on the disk of the node-local copy cache /copies/duckdb-1-16932621313647219913 for this query's 1 new file copies (17313016 bytes, e.g. spread/lineitem_sp/part-05.parquet): 15152338 bytes are free and 6710880 must stay free (hdfsLocalCopyMinFreeBytes); the 0 copies this query reuses take 0 bytes, copies in use by other running queries take 51956526 byte; part-group-sp@n1@partial: [gRPC ResourceExhausted] InternalError: INTERNAL: [FlightSQL] No room on the disk of the node-local copy cache /copies
- `speed` x 3: **4-smalldisk**: part-lineitem-sp@n1@partial: InternalError: INTERNAL: [FlightSQL] all 2 DoGet location(s) failed: DoGet("grpc+tls://172.31.0.14:32010"): rpc error: code = ResourceExhausted desc = No room on the disk of the node-local copy cache /copies/duckdb-1-11425829090633925625 for this query's 1 new file copies (17313016 bytes, e.g. spread/lineitem_sp/part-05.parquet): 14596704 bytes are free and 6710880 must stay free (hdfsLocalCopyMin; part-group-sp@n1@partial: InternalError: INTERNAL: [FlightSQL] all 2 DoGet location(s) failed: DoGet("grpc+tls://172.31.0.14:32010"): rpc error: code = ResourceExhausted

## Reference cells

- reference `default` x 1: setup pass, 61 answers, 0 errors
- reference `default` x 3: setup pass, 135 answers, 0 errors
- reference `speed` x 1: setup pass, 61 answers, 0 errors
- reference `speed` x 3: setup pass, 135 answers, 0 errors

Raw logs: run artifacts `cell-*`.

## Note: check 4 without the item 33 room wait (session note, 2026-11-05)

This run (dispatched by the maintainer's watcher, harness 66aed33) started the check 4 servers WITHOUT
`-DhdfsLocalCopyRoomWaitMillis` (the harness had no way to pass it then). It therefore answers the maintainer's second
question: **without the room wait the speed partial cells still fail** (`part-lineitem-sp` / `part-group-sp` refused
with ResourceExhausted; the refusal counts ~52 MB "copies in use by other running queries"). In the default cells check 4
now passes (complete `sp-group` / `sp-distinct` no longer refused, which failed on `5f60db1ee304` and `50fe065af50c`).
The verdict above is provisional: check 4 with `-DhdfsLocalCopyRoomWaitMillis=30000` on every server still needs one
dispatch of `accept-hdfs.yml` with the new input `smalldisk-opts=-DhdfsLocalCopyRoomWaitMillis=30000`.
