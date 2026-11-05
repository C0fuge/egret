# HDFS acceptance (SASL): `server-1.0.0-8060179bce0c`

Run [41995351608](https://github.com/C0fuge/egret/actions/runs/41995351608), workflow `accept-hdfs.yml`, checks from `ci/BUILD-TRACK-TASK.md` "SASL HDFS ACCEPTANCE" (this repo's queries, layout and checks, `ci/accept/`).

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
| 6-logs | **FAIL** | **FAIL** | **FAIL** | **FAIL** |

Checks: 1 TPC-H 22/22 plain names and schema-qualified; 2 spread set (plain names; count, full scans, GROUP BY, ORDER BY LIMIT, HAVING, count(DISTINCT), comma join, JOIN ON, q03/q12; part_far whose first file is on dn3 only); 3 partial mode per-node sums = complete (3 servers); 4 `-DhdfsLocalCopyDir` on a 64 MiB tmpfs; 5 3 servers speed + `distributedComplete=true`, `-XX:MaxDirectMemorySize=512m`, 4 full scans of the 12-file lineitem; 6 server logs (`hdfs=reads` per query, short-circuit fd counters grow, no `HdfsNetworkException`).

## Failures

- `default` x 1: **4-smalldisk**: part-lineitem-sp@n1@complete: InternalError: INTERNAL: [FlightSQL] No room on the disk of the node-local copy cache /copies/duckdb-1-11638727023179555436 for this query's 1 file copies (17316181 bytes, e.g. spread/lineitem_sp/part-00.parquet): 67108864 bytes are free and 1073741824 must stay free (hdfsLocalCopyMinFreeBytes); copies in use by running queries take 0 bytes. Nothing was copied; retry when other queries end, or giv; part-orders-sp@n1@complete: InternalError: INTERNAL: [FlightSQL] No room on the disk of the node-local copy cache /copies/duckdb-1-11638727023179555436 for this query's
- `default` x 1: **6-logs**: queries without an hdfs=reads line: queries=61 reads=16 missing=45 paths=complete-answer:45 sample=complete-answer 06238691ef ok; complete-answer 2e48b271f9 ok; complete-answer 00e22915be ok; hdfs=reads lines 16 < queries sent 61;
- `default` x 3: **4-smalldisk**: part-lineitem-sp@n1@complete: InternalError: INTERNAL: [FlightSQL] No room on the disk of the node-local copy cache /copies/duckdb-1-8138692189149084710 for this query's 1 file copies (17316181 bytes, e.g. spread/lineitem_sp/part-00.parquet): 67108864 bytes are free and 1073741824 must stay free (hdfsLocalCopyMinFreeBytes); copies in use by running queries take 0 bytes. Nothing was copied; retry when other queries end, or give; part-orders-sp@n1@complete: InternalError: INTERNAL: [FlightSQL] No room on the disk of the node-local copy cache /copies/duckdb-1-8138692189149084710 for this query's 
- `default` x 3: **6-logs**: queries without an hdfs=reads line: queries=101 reads=55 missing=46 paths=complete-answer:46 sample=complete-answer 06238691ef ok; complete-answer 2e48b271f9 ok; complete-answer 00e22915be ok; hdfs=reads lines 83 < queries sent 147;
- `speed` x 1: **4-smalldisk**: part-lineitem-sp@n1@complete: InternalError: INTERNAL: [FlightSQL] No room on the disk of the node-local copy cache /copies/duckdb-1-17455266055284344676 for this query's 1 file copies (17316181 bytes, e.g. spread/lineitem_sp/part-00.parquet): 67108864 bytes are free and 1073741824 must stay free (hdfsLocalCopyMinFreeBytes); copies in use by running queries take 0 bytes. Nothing was copied; retry when other queries end, or giv; part-orders-sp@n1@complete: InternalError: INTERNAL: [FlightSQL] No room on the disk of the node-local copy cache /copies/duckdb-1-17455266055284344676 for this query's
- `speed` x 1: **6-logs**: queries without an hdfs=reads line: queries=61 reads=16 missing=45 paths=complete-answer:45 sample=complete-answer 06238691ef ok; complete-answer 2e48b271f9 ok; complete-answer 00e22915be ok; hdfs=reads lines 16 < queries sent 61;
- `speed` x 3: **4-smalldisk**: part-lineitem-sp@n1@complete: InternalError: INTERNAL: [FlightSQL] No room on the disk of the node-local copy cache /copies/duckdb-1-11429132786366979529 for this query's 1 file copies (17316181 bytes, e.g. spread/lineitem_sp/part-00.parquet): 67108864 bytes are free and 1073741824 must stay free (hdfsLocalCopyMinFreeBytes); copies in use by running queries take 0 bytes. Nothing was copied; retry when other queries end, or giv; part-orders-sp@n1@complete: InternalError: INTERNAL: [FlightSQL] No room on the disk of the node-local copy cache /copies/duckdb-1-11429132786366979529 for this query's
- `speed` x 3: **6-logs**: queries without an hdfs=reads line: queries=185 reads=139 missing=46 paths=complete-answer:46 sample=complete-answer 06238691ef ok; complete-answer 2e48b271f9 ok; complete-answer 00e22915be ok;

## Reference cells

- reference `default` x 1: setup pass, 61 answers, 0 errors
- reference `default` x 3: setup pass, 135 answers, 0 errors
- reference `speed` x 1: setup pass, 61 answers, 0 errors
- reference `speed` x 3: setup pass, 135 answers, 0 errors

Raw logs: run artifacts `cell-*`.
