# HDFS acceptance (SASL): `server-1.0.0-37bf9401d77c`

Run [42790907501](https://github.com/C0fuge/egret/actions/runs/42790907501) (7 cells) + `only` rerun [42800586401](https://github.com/C0fuge/egret/actions/runs/42800586401) of the reference cell open-speed-1 (base-run 42790907501; the first attempt failed at setup, `KDC did not come up`, infra), workflow `accept-hdfs.yml`, checks from `ci/BUILD-TRACK-TASK.md` "SASL HDFS ACCEPTANCE" (this repo's queries, layout and checks, `ci/accept/`).

**Verdict: DO NOT SHIP**

Cluster: Hadoop 3.1.3, 2 NameNodes HA (ZooKeeper + ZKFC), Kerberos KDC, 3 DataNodes with `dfs.data.transfer.protection=authentication`, short-circuit socket, one Flight server per DataNode in its network namespace, Flight with Kerberos auth + TLS. Answers compared with the same build on DataNodes without data-transfer protection and with in-process DuckDB over the same files.

| check | default x 1 | default x 3 | speed x 1 | speed x 3 |
|---|---|---|---|---|
| 1-tpch-plain | pass 22/22 | pass 66/66 | pass 22/22 | pass 66/66 |
| 1-tpch-schema | pass 22/22 | pass 22/22 | pass 22/22 | pass 22/22 |
| 2-spread | pass 17/17 | pass 47/47 | pass 17/17 | pass 47/47 |
| 3-partial | n/a | pass | n/a | pass |
| 4-smalldisk | pass | pass | pass | pass |
| 5-lowdirect | n/a | n/a | n/a | pass |
| 6-logs | **FAIL** | **FAIL** | **FAIL** | **FAIL** |

Checks: 1 TPC-H 22/22 plain names and schema-qualified; 2 spread set (plain names; count, full scans, GROUP BY, ORDER BY LIMIT, HAVING, count(DISTINCT), comma join, JOIN ON, q03/q12; part_far whose first file is on dn3 only); 3 partial mode per-node sums = complete (3 servers); 4 `-DhdfsLocalCopyDir` on a 64 MiB tmpfs; 5 3 servers speed + `distributedComplete=true`, `-XX:MaxDirectMemorySize=512m`, 4 full scans of the 12-file lineitem; 6 server logs (`hdfs=reads` per query, short-circuit fd counters grow, no `HdfsNetworkException`).

## Failures

- `default` x 1: **6-logs**: queries without an hdfs=reads line: queries=61 reads=0 missing=61 paths=complete-answer:61 sample=complete-answer 06238691ef ok; complete-answer 2e48b271f9 ok; complete-answer 00e22915be ok; hdfs=reads lines 0 < queries sent 61;
- `default` x 3: **6-logs**: queries without an hdfs=reads line: queries=101 reads=0 missing=101 paths=complete-answer:65,duckdb-aggregation:36 sample=complete-answer 06238691ef ok; complete-answer 2e48b271f9 ok; complete-answer 00e22915be ok; hdfs=reads lines 0 < queries sent 147;
- `speed` x 1: **6-logs**: queries without an hdfs=reads line: queries=61 reads=0 missing=61 paths=complete-answer:61 sample=complete-answer 06238691ef ok; complete-answer 2e48b271f9 ok; complete-answer 00e22915be ok; hdfs=reads lines 0 < queries sent 61;
- `speed` x 3: **6-logs**: queries without an hdfs=reads line: queries=185 reads=0 missing=185 paths=duckdb-aggregation:120,complete-answer:65 sample=complete-answer 06238691ef ok; complete-answer 2e48b271f9 ok; complete-answer 00e22915be ok; hdfs=reads lines 0 < queries sent 147;

## Reference cells

- reference `default` x 1: setup pass, 61 answers, 0 errors
- reference `default` x 3: setup pass, 135 answers, 0 errors
- reference `speed` x 1: setup pass, 61 answers, 0 errors
- reference `speed` x 3: setup pass, 135 answers, 0 errors

## Check 6: cause (session note, 2026-11-10)

Answers are all right in every cell (checks 1-5 pass; the reference speed x 1 cell now passes too). Check 6 fails only
on its first part, the per-query `hdfs=reads` line: 0 such lines in every SASL cell. Short-circuit fd requests on the
DataNodes grow (0 -> 783) and there is no `HdfsNetworkException`.

Cause, from the server source at the tag: `hdfs=reads` is logged only on the whole-file / local-copy path
(`ExecutionService.copies`). Item 41 (hadoopfs afc6 + default `hdfsSaslDataTransfer=auto`) turns on direct SASL reads
of non-local blocks, so that path is no longer taken and no line is written. kestrel's own CI made the same choice:
commit 8766455b makes its `sasl-direct` cell skip the per-query `hdfs=reads` check of item 32. This is a design change
in the server that conflicts with check 6 as written ("every query has an `hdfs=reads` line"; "no DuckDB read of a
non-local file through hadoopfs" is what direct mode does on purpose).

The server start line (`hdfs=saslDataTransfer ... direct=true`) is in the cell artifacts only; this session could not
download them, so it is not confirmed here.

**Maintainer decision needed:** (a) keep check 6 as is (the server should log `hdfs=reads` in direct mode too), or
(b) change check 6 for direct mode (e.g. require a direct-read counter line instead) or run the acceptance with
`-DhdfsSaslDataTransfer=off`. Until then the verdict stays DO NOT SHIP on check 6 only.

Raw logs: run artifacts `cell-*`.
