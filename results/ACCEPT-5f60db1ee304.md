# HDFS acceptance (SASL): `server-1.0.0-5f60db1ee304`

Run [42027069331](https://github.com/C0fuge/egret/actions/runs/42027069331), workflow `accept-hdfs.yml`, checks from `ci/BUILD-TRACK-TASK.md` "SASL HDFS ACCEPTANCE" (this repo's queries, layout and checks, `ci/accept/`).

**Verdict: DO NOT SHIP**

Cells: sasl from the `only` rerun 42027069331 (harness a5a0469: check 4 reads the gRPC status from the full error text), reference cells from the full run [42018218548](https://github.com/C0fuge/egret/actions/runs/42018218548). Check 4 detail: the over-size join (`sp-join-lineitem`, 13 copies, 212 MB) is refused with RESOURCE_EXHAUSTED (allowed) in every cell; the remaining failures are complete `sp-group` and `sp-distinct` (9 copies, 156 MB > 64 MiB disk), refused outright ("Nothing was copied") instead of running in copy batches. Smaller complete copies, partial mode and the complete spread scan are exact; tmpfs never full. Item 32's small-disk reserve (6710880 bytes = 10 %) applies, so `-DhdfsLocalCopyMinFreeBytes=8m` was not needed.

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

- `default` x 1: **4-smalldisk**: sp-group@n1@complete: [gRPC ResourceExhausted] InternalError: INTERNAL: [FlightSQL] No room on the disk of the node-local copy cache /copies/duckdb-1-8340292135721250005 for this query's 9 file copies (155906121 bytes, e.g. spread/lineitem_sp/part-00.parquet): 67108864 bytes are free and 6710880 must stay free (hdfsLocalCopyMinFreeBytes); copies in use by running queries take 0 bytes. Nothing was copied; retry when other queries end, or give h; sp-distinct@n1@complete: [gRPC ResourceExhausted] InternalError: INTERNAL: [FlightSQL] No room on the disk of the node-local copy cache /copies/duckdb-
- `default` x 3: **4-smalldisk**: sp-group@n1@complete: [gRPC ResourceExhausted] InternalError: INTERNAL: [FlightSQL] No room on the disk of the node-local copy cache /copies/duckdb-1-7809810825271710308 for this query's 9 file copies (155906121 bytes, e.g. spread/lineitem_sp/part-00.parquet): 67108864 bytes are free and 6710880 must stay free (hdfsLocalCopyMinFreeBytes); copies in use by running queries take 0 bytes. Nothing was copied; retry when other queries end, or give h; sp-distinct@n1@complete: [gRPC ResourceExhausted] InternalError: INTERNAL: [FlightSQL] No room on the disk of the node-local copy cache /copies/duckdb-
- `speed` x 1: **4-smalldisk**: sp-group@n1@complete: [gRPC ResourceExhausted] InternalError: INTERNAL: [FlightSQL] No room on the disk of the node-local copy cache /copies/duckdb-1-11928020892091157321 for this query's 9 file copies (155906121 bytes, e.g. spread/lineitem_sp/part-00.parquet): 67108864 bytes are free and 6710880 must stay free (hdfsLocalCopyMinFreeBytes); copies in use by running queries take 0 bytes. Nothing was copied; retry when other queries end, or give ; sp-distinct@n1@complete: [gRPC ResourceExhausted] InternalError: INTERNAL: [FlightSQL] No room on the disk of the node-local copy cache /copies/duckdb-
- `speed` x 3: **4-smalldisk**: sp-group@n1@complete: [gRPC ResourceExhausted] InternalError: INTERNAL: [FlightSQL] No room on the disk of the node-local copy cache /copies/duckdb-1-15356069138075936372 for this query's 9 file copies (155906121 bytes, e.g. spread/lineitem_sp/part-00.parquet): 67108864 bytes are free and 6710880 must stay free (hdfsLocalCopyMinFreeBytes); copies in use by running queries take 0 bytes. Nothing was copied; retry when other queries end, or give ; sp-distinct@n1@complete: [gRPC ResourceExhausted] InternalError: INTERNAL: [FlightSQL] No room on the disk of the node-local copy cache /copies/duckdb-

## Reference cells

- reference `default` x 1: setup pass, 61 answers, 0 errors
- reference `default` x 3: setup pass, 135 answers, 0 errors
- reference `speed` x 1: setup pass, 61 answers, 0 errors
- reference `speed` x 3: setup pass, 135 answers, 0 errors

Raw logs: run artifacts `cell-*`.
