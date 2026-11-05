# HDFS acceptance (SASL): `server-1.0.0-8060179bce0c`

Run [41986696064](https://github.com/C0fuge/egret/actions/runs/41986696064), workflow `accept-hdfs.yml`, checks from `ci/BUILD-TRACK-TASK.md` "SASL HDFS ACCEPTANCE" (this repo's queries, layout and checks, `ci/accept/`).

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
| 6-logs | **FAIL** | **FAIL** | **FAIL** | pass |

Checks: 1 TPC-H 22/22 plain names and schema-qualified; 2 spread set (plain names; count, full scans, GROUP BY, ORDER BY LIMIT, HAVING, count(DISTINCT), comma join, JOIN ON, q03/q12; part_far whose first file is on dn3 only); 3 partial mode per-node sums = complete (3 servers); 4 `-DhdfsLocalCopyDir` on a 64 MiB tmpfs; 5 3 servers speed + `distributedComplete=true`, `-XX:MaxDirectMemorySize=512m`, 4 full scans of the 12-file lineitem; 6 server logs (`hdfs=reads` per query, short-circuit fd counters grow, no `HdfsNetworkException`).

## Failures

- `default` x 1: **4-smalldisk**: part-lineitem-sp@n1@complete: InternalError: INTERNAL: [FlightSQL] No room on the disk of the node-local copy cache /copies/duckdb-1-9971558103099708072 for this query's 1 file copies (17316181 bytes, e.g. spread/lineitem_sp/part-00.parquet): 67108864 bytes are free and 1073741824 must stay free (hdfsLocalCopyMinFreeBytes); copies in use by running queries take 0 bytes. Nothing was copied; retry when other queries end, or give; part-orders-sp@n1@complete: InternalError: INTERNAL: [FlightSQL] No room on the disk of the node-local copy cache /copies/duckdb-1-9971558103099708072 for this query's 
- `default` x 1: **6-logs**: hdfs=reads lines 16 < queries 61;
- `default` x 3: **4-smalldisk**: part-lineitem-sp@n1@complete: InternalError: INTERNAL: [FlightSQL] No room on the disk of the node-local copy cache /copies/duckdb-1-14848949417843701231 for this query's 1 file copies (17316181 bytes, e.g. spread/lineitem_sp/part-00.parquet): 67108864 bytes are free and 1073741824 must stay free (hdfsLocalCopyMinFreeBytes); copies in use by running queries take 0 bytes. Nothing was copied; retry when other queries end, or giv; part-orders-sp@n1@complete: InternalError: INTERNAL: [FlightSQL] No room on the disk of the node-local copy cache /copies/duckdb-1-14848949417843701231 for this query's
- `default` x 3: **6-logs**: hdfs=reads lines 85 < queries 147;
- `speed` x 1: **4-smalldisk**: part-lineitem-sp@n1@complete: InternalError: INTERNAL: [FlightSQL] No room on the disk of the node-local copy cache /copies/duckdb-1-13601315809089267505 for this query's 1 file copies (17316181 bytes, e.g. spread/lineitem_sp/part-00.parquet): 67108864 bytes are free and 1073741824 must stay free (hdfsLocalCopyMinFreeBytes); copies in use by running queries take 0 bytes. Nothing was copied; retry when other queries end, or giv; part-orders-sp@n1@complete: InternalError: INTERNAL: [FlightSQL] No room on the disk of the node-local copy cache /copies/duckdb-1-13601315809089267505 for this query's
- `speed` x 1: **6-logs**: hdfs=reads lines 16 < queries 61;
- `speed` x 3: **4-smalldisk**: part-lineitem-sp@n1@complete: InternalError: INTERNAL: [FlightSQL] No room on the disk of the node-local copy cache /copies/duckdb-1-18202937474141635427 for this query's 1 file copies (17316181 bytes, e.g. spread/lineitem_sp/part-00.parquet): 67108864 bytes are free and 1073741824 must stay free (hdfsLocalCopyMinFreeBytes); copies in use by running queries take 0 bytes. Nothing was copied; retry when other queries end, or giv; part-orders-sp@n1@complete: InternalError: INTERNAL: [FlightSQL] No room on the disk of the node-local copy cache /copies/duckdb-1-18202937474141635427 for this query's

## Reference cells

- reference `default` x 1: setup pass, 61 answers, 0 errors
- reference `default` x 3: setup pass, 135 answers, 0 errors
- reference `speed` x 1: setup pass, 61 answers, 0 errors
- reference `speed` x 3: setup pass, 135 answers, 0 errors

Raw logs: run artifacts `cell-*`.
