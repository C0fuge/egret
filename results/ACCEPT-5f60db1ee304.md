# HDFS acceptance (SASL): `server-1.0.0-5f60db1ee304`

Run [42018218548](https://github.com/C0fuge/egret/actions/runs/42018218548), workflow `accept-hdfs.yml`, checks from `ci/BUILD-TRACK-TASK.md` "SASL HDFS ACCEPTANCE" (this repo's queries, layout and checks, `ci/accept/`).

**Verdict: DO NOT SHIP**

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

- `default` x 1: **4-smalldisk**: sp-group@n1@complete: InternalError: INTERNAL: [FlightSQL] No room on the disk of the node-local copy cache /copies/duckdb-1-3468675549158551444 for this query's 9 file copies (155906121 bytes, e.g. spread/lineitem_sp/part-00.parquet): 67108864 bytes are free and 6710880 must stay free (hdfsLocalCopyMinFreeBytes); copies in use by running queries take 0 bytes. Nothing was copied; retry when other queries end, or give h; sp-distinct@n1@complete: InternalError: INTERNAL: [FlightSQL] No room on the disk of the node-local copy cache /copies/duckdb-1-3468675549158551444 for this query's 9 file copi
- `default` x 3: **4-smalldisk**: sp-group@n1@complete: InternalError: INTERNAL: [FlightSQL] No room on the disk of the node-local copy cache /copies/duckdb-1-18375256495392475240 for this query's 9 file copies (155906121 bytes, e.g. spread/lineitem_sp/part-00.parquet): 67108864 bytes are free and 6710880 must stay free (hdfsLocalCopyMinFreeBytes); copies in use by running queries take 0 bytes. Nothing was copied; retry when other queries end, or give ; sp-distinct@n1@complete: InternalError: INTERNAL: [FlightSQL] No room on the disk of the node-local copy cache /copies/duckdb-1-18375256495392475240 for this query's 9 file cop
- `speed` x 1: **4-smalldisk**: sp-group@n1@complete: InternalError: INTERNAL: [FlightSQL] No room on the disk of the node-local copy cache /copies/duckdb-1-5272062969298715196 for this query's 9 file copies (155906121 bytes, e.g. spread/lineitem_sp/part-00.parquet): 67108864 bytes are free and 6710880 must stay free (hdfsLocalCopyMinFreeBytes); copies in use by running queries take 0 bytes. Nothing was copied; retry when other queries end, or give h; sp-distinct@n1@complete: InternalError: INTERNAL: [FlightSQL] No room on the disk of the node-local copy cache /copies/duckdb-1-5272062969298715196 for this query's 9 file copi
- `speed` x 3: **4-smalldisk**: sp-group@n1@complete: InternalError: INTERNAL: [FlightSQL] No room on the disk of the node-local copy cache /copies/duckdb-1-10214320028759296990 for this query's 9 file copies (155906121 bytes, e.g. spread/lineitem_sp/part-00.parquet): 67108864 bytes are free and 6710880 must stay free (hdfsLocalCopyMinFreeBytes); copies in use by running queries take 0 bytes. Nothing was copied; retry when other queries end, or give ; sp-distinct@n1@complete: InternalError: INTERNAL: [FlightSQL] No room on the disk of the node-local copy cache /copies/duckdb-1-10214320028759296990 for this query's 9 file cop

## Reference cells

- reference `default` x 1: setup pass, 61 answers, 0 errors
- reference `default` x 3: setup pass, 135 answers, 0 errors
- reference `speed` x 1: setup pass, 61 answers, 0 errors
- reference `speed` x 3: setup pass, 135 answers, 0 errors

Raw logs: run artifacts `cell-*`.
