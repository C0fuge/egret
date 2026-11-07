# HDFS acceptance (SASL): `server-1.0.0-06c5adc7d7c9`

Run [42390647941](https://github.com/C0fuge/egret/actions/runs/42390647941), workflow `accept-hdfs.yml`, checks from `ci/BUILD-TRACK-TASK.md` "SASL HDFS ACCEPTANCE" (this repo's queries, layout and checks, `ci/accept/`).

**Verdict: DO NOT SHIP**

Cluster: Hadoop 3.1.3, 2 NameNodes HA (ZooKeeper + ZKFC), Kerberos KDC, 3 DataNodes with `dfs.data.transfer.protection=authentication`, short-circuit socket, one Flight server per DataNode in its network namespace, Flight with Kerberos auth + TLS. Answers compared with the same build on DataNodes without data-transfer protection and with in-process DuckDB over the same files.

| check | default x 1 | default x 3 | speed x 1 | speed x 3 |
|---|---|---|---|---|
| 1-tpch-plain | pass 22/22 | pass 66/66 | **FAIL** setup | **FAIL** setup |
| 1-tpch-schema | pass 22/22 | pass 22/22 | **FAIL** setup | **FAIL** setup |
| 2-spread | pass 17/17 | pass 47/47 | **FAIL** setup | **FAIL** setup |
| 3-partial | n/a | pass | **FAIL** | **FAIL** |
| 4-smalldisk | pass | pass | **FAIL** | **FAIL** |
| 5-lowdirect | n/a | n/a | **FAIL** | **FAIL** |
| 6-logs | pass | pass | **FAIL** | **FAIL** |

Checks: 1 TPC-H 22/22 plain names and schema-qualified; 2 spread set (plain names; count, full scans, GROUP BY, ORDER BY LIMIT, HAVING, count(DISTINCT), comma join, JOIN ON, q03/q12; part_far whose first file is on dn3 only); 3 partial mode per-node sums = complete (3 servers); 4 `-DhdfsLocalCopyDir` on a 64 MiB tmpfs; 5 3 servers speed + `distributedComplete=true`, `-XX:MaxDirectMemorySize=512m`, 4 full scans of the 12-file lineitem; 6 server logs (`hdfs=reads` per query, short-circuit fd counters grow, no `HdfsNetworkException`).

## Failures

- `speed` x 1: **1-tpch-plain**: setup: layout: layout FAIL: /data/spread/lineitem_sp/part-01.parquet: a DataNode holds it whole (17 blocks, {'12': 6, '13': 11, '14': 17})
- `speed` x 1: **1-tpch-schema**: setup: layout: layout FAIL: /data/spread/lineitem_sp/part-01.parquet: a DataNode holds it whole (17 blocks, {'12': 6, '13': 11, '14': 17})
- `speed` x 1: **2-spread**: setup: layout: layout FAIL: /data/spread/lineitem_sp/part-01.parquet: a DataNode holds it whole (17 blocks, {'12': 6, '13': 11, '14': 17})
- `speed` x 1: **3-partial**: not run: layout: layout FAIL: /data/spread/lineitem_sp/part-01.parquet: a DataNode holds it whole (17 blocks, {'12': 6, '13': 11, '14': 17})
- `speed` x 1: **4-smalldisk**: not run: layout: layout FAIL: /data/spread/lineitem_sp/part-01.parquet: a DataNode holds it whole (17 blocks, {'12': 6, '13': 11, '14': 17})
- `speed` x 1: **5-lowdirect**: not run: layout: layout FAIL: /data/spread/lineitem_sp/part-01.parquet: a DataNode holds it whole (17 blocks, {'12': 6, '13': 11, '14': 17})
- `speed` x 1: **6-logs**: not run: layout: layout FAIL: /data/spread/lineitem_sp/part-01.parquet: a DataNode holds it whole (17 blocks, {'12': 6, '13': 11, '14': 17})
- `speed` x 3: **1-tpch-plain**: setup: layout: layout FAIL: /data/spread/lineitem_sp/part-07.parquet: a DataNode holds it whole (17 blocks, {'12': 10, '13': 7, '14': 17})
- `speed` x 3: **1-tpch-schema**: setup: layout: layout FAIL: /data/spread/lineitem_sp/part-07.parquet: a DataNode holds it whole (17 blocks, {'12': 10, '13': 7, '14': 17})
- `speed` x 3: **2-spread**: setup: layout: layout FAIL: /data/spread/lineitem_sp/part-07.parquet: a DataNode holds it whole (17 blocks, {'12': 10, '13': 7, '14': 17})
- `speed` x 3: **3-partial**: not run: layout: layout FAIL: /data/spread/lineitem_sp/part-07.parquet: a DataNode holds it whole (17 blocks, {'12': 10, '13': 7, '14': 17})
- `speed` x 3: **4-smalldisk**: not run: layout: layout FAIL: /data/spread/lineitem_sp/part-07.parquet: a DataNode holds it whole (17 blocks, {'12': 10, '13': 7, '14': 17})
- `speed` x 3: **5-lowdirect**: not run: layout: layout FAIL: /data/spread/lineitem_sp/part-07.parquet: a DataNode holds it whole (17 blocks, {'12': 10, '13': 7, '14': 17})
- `speed` x 3: **6-logs**: not run: layout: layout FAIL: /data/spread/lineitem_sp/part-07.parquet: a DataNode holds it whole (17 blocks, {'12': 10, '13': 7, '14': 17})

## Reference cells

- reference `default` x 1: setup pass, 61 answers, 0 errors
- reference `default` x 3: setup pass, 135 answers, 0 errors
- reference `speed` x 1: setup fail, 0 answers, 0 errors
- reference `speed` x 3: setup pass, 135 answers, 0 errors

Raw logs: run artifacts `cell-*`.
