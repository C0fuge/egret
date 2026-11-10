# HDFS acceptance (SASL): `server-1.0.0-894afb9b48c4`

Run [42772192151](https://github.com/C0fuge/egret/actions/runs/42772192151), workflow `accept-hdfs.yml`, checks from `ci/BUILD-TRACK-TASK.md` "SASL HDFS ACCEPTANCE" (this repo's queries, layout and checks, `ci/accept/`).

**Verdict: DO NOT SHIP**

Cluster: Hadoop 3.1.3, 2 NameNodes HA (ZooKeeper + ZKFC), Kerberos KDC, 3 DataNodes with `dfs.data.transfer.protection=authentication`, short-circuit socket, one Flight server per DataNode in its network namespace, Flight with Kerberos auth + TLS. Answers compared with the same build on DataNodes without data-transfer protection and with in-process DuckDB over the same files.

| check | default x 1 | default x 3 | speed x 1 | speed x 3 |
|---|---|---|---|---|
| 1-tpch-plain | **FAIL** setup | **FAIL** setup | **FAIL** setup | **FAIL** setup |
| 1-tpch-schema | **FAIL** setup | **FAIL** setup | **FAIL** setup | **FAIL** setup |
| 2-spread | **FAIL** setup | **FAIL** setup | **FAIL** setup | **FAIL** setup |
| 3-partial | **FAIL** | **FAIL** | **FAIL** | **FAIL** |
| 4-smalldisk | **FAIL** | **FAIL** | **FAIL** | **FAIL** |
| 5-lowdirect | **FAIL** | **FAIL** | **FAIL** | **FAIL** |
| 6-logs | **FAIL** | **FAIL** | **FAIL** | **FAIL** |

Checks: 1 TPC-H 22/22 plain names and schema-qualified; 2 spread set (plain names; count, full scans, GROUP BY, ORDER BY LIMIT, HAVING, count(DISTINCT), comma join, JOIN ON, q03/q12; part_far whose first file is on dn3 only); 3 partial mode per-node sums = complete (3 servers); 4 `-DhdfsLocalCopyDir` on a 64 MiB tmpfs; 5 3 servers speed + `distributedComplete=true`, `-XX:MaxDirectMemorySize=512m`, 4 full scans of the 12-file lineitem; 6 server logs (`hdfs=reads` per query, short-circuit fd counters grow, no `HdfsNetworkException`).

## Failures

- `default` x 1: **1-tpch-plain**: setup: server did not start: [main] ERROR pro.surpin.data.arrowflight.server.HadoopArrowFlightServer - Error starting server
- `default` x 1: **1-tpch-schema**: setup: server did not start: [main] ERROR pro.surpin.data.arrowflight.server.HadoopArrowFlightServer - Error starting server
- `default` x 1: **2-spread**: setup: server did not start: [main] ERROR pro.surpin.data.arrowflight.server.HadoopArrowFlightServer - Error starting server
- `default` x 1: **3-partial**: not run: server did not start: [main] ERROR pro.surpin.data.arrowflight.server.HadoopArrowFlightServer - Error starting server
- `default` x 1: **4-smalldisk**: not run: server did not start: [main] ERROR pro.surpin.data.arrowflight.server.HadoopArrowFlightServer - Error starting server
- `default` x 1: **5-lowdirect**: not run: server did not start: [main] ERROR pro.surpin.data.arrowflight.server.HadoopArrowFlightServer - Error starting server
- `default` x 1: **6-logs**: not run: server did not start: [main] ERROR pro.surpin.data.arrowflight.server.HadoopArrowFlightServer - Error starting server
- `default` x 3: **1-tpch-plain**: setup: server did not start: WARNING: [172.31.0.12]:5701 [dev] [5.7.0] Connection[id=3, /172.31.0.12:47663->/172.31.0.13:5701, qualifier=null, endpoint=[172.31.0.13]:5701, remoteUuid=b02bf72d-1d1e-4e38-bc02-f95d2e2a0e43, alive=false, connectionType=MEMBER, planeIndex=0] closed. Reason: Exception in Connection[id=3, /172.31.0.12
- `default` x 3: **1-tpch-schema**: setup: server did not start: WARNING: [172.31.0.12]:5701 [dev] [5.7.0] Connection[id=3, /172.31.0.12:47663->/172.31.0.13:5701, qualifier=null, endpoint=[172.31.0.13]:5701, remoteUuid=b02bf72d-1d1e-4e38-bc02-f95d2e2a0e43, alive=false, connectionType=MEMBER, planeIndex=0] closed. Reason: Exception in Connection[id=3, /172.31.0.12
- `default` x 3: **2-spread**: setup: server did not start: WARNING: [172.31.0.12]:5701 [dev] [5.7.0] Connection[id=3, /172.31.0.12:47663->/172.31.0.13:5701, qualifier=null, endpoint=[172.31.0.13]:5701, remoteUuid=b02bf72d-1d1e-4e38-bc02-f95d2e2a0e43, alive=false, connectionType=MEMBER, planeIndex=0] closed. Reason: Exception in Connection[id=3, /172.31.0.12
- `default` x 3: **3-partial**: not run: server did not start: WARNING: [172.31.0.12]:5701 [dev] [5.7.0] Connection[id=3, /172.31.0.12:47663->/172.31.0.13:5701, qualifier=null, endpoint=[172.31.0.13]:5701, remoteUuid=b02bf72d-1d1e-4e38-bc02-f95d2e2a0e43, alive=false, connectionType=MEMBER, planeIndex=0] closed. Reason: Exception in Connection[id=3, /172.31.0.12
- `default` x 3: **4-smalldisk**: not run: server did not start: WARNING: [172.31.0.12]:5701 [dev] [5.7.0] Connection[id=3, /172.31.0.12:47663->/172.31.0.13:5701, qualifier=null, endpoint=[172.31.0.13]:5701, remoteUuid=b02bf72d-1d1e-4e38-bc02-f95d2e2a0e43, alive=false, connectionType=MEMBER, planeIndex=0] closed. Reason: Exception in Connection[id=3, /172.31.0.12
- `default` x 3: **5-lowdirect**: not run: server did not start: WARNING: [172.31.0.12]:5701 [dev] [5.7.0] Connection[id=3, /172.31.0.12:47663->/172.31.0.13:5701, qualifier=null, endpoint=[172.31.0.13]:5701, remoteUuid=b02bf72d-1d1e-4e38-bc02-f95d2e2a0e43, alive=false, connectionType=MEMBER, planeIndex=0] closed. Reason: Exception in Connection[id=3, /172.31.0.12
- `default` x 3: **6-logs**: not run: server did not start: WARNING: [172.31.0.12]:5701 [dev] [5.7.0] Connection[id=3, /172.31.0.12:47663->/172.31.0.13:5701, qualifier=null, endpoint=[172.31.0.13]:5701, remoteUuid=b02bf72d-1d1e-4e38-bc02-f95d2e2a0e43, alive=false, connectionType=MEMBER, planeIndex=0] closed. Reason: Exception in Connection[id=3, /172.31.0.12
- `speed` x 1: **1-tpch-plain**: setup: server did not start: [main] ERROR pro.surpin.data.arrowflight.server.HadoopArrowFlightServer - Error starting server
- `speed` x 1: **1-tpch-schema**: setup: server did not start: [main] ERROR pro.surpin.data.arrowflight.server.HadoopArrowFlightServer - Error starting server
- `speed` x 1: **2-spread**: setup: server did not start: [main] ERROR pro.surpin.data.arrowflight.server.HadoopArrowFlightServer - Error starting server
- `speed` x 1: **3-partial**: not run: server did not start: [main] ERROR pro.surpin.data.arrowflight.server.HadoopArrowFlightServer - Error starting server
- `speed` x 1: **4-smalldisk**: not run: server did not start: [main] ERROR pro.surpin.data.arrowflight.server.HadoopArrowFlightServer - Error starting server
- `speed` x 1: **5-lowdirect**: not run: server did not start: [main] ERROR pro.surpin.data.arrowflight.server.HadoopArrowFlightServer - Error starting server
- `speed` x 1: **6-logs**: not run: server did not start: [main] ERROR pro.surpin.data.arrowflight.server.HadoopArrowFlightServer - Error starting server
- `speed` x 3: **1-tpch-plain**: setup: server did not start: WARNING: [172.31.0.12]:5701 [dev] [5.7.0] Connection[id=1, /172.31.0.12:5701->/172.31.0.14:55257, qualifier=null, endpoint=[172.31.0.14]:5701, remoteUuid=8de6206e-d058-43bc-b1de-2fbbaa4dd804, alive=false, connectionType=MEMBER, planeIndex=0] closed. Reason: Exception in Connection[id=1, /172.31.0.12
- `speed` x 3: **1-tpch-schema**: setup: server did not start: WARNING: [172.31.0.12]:5701 [dev] [5.7.0] Connection[id=1, /172.31.0.12:5701->/172.31.0.14:55257, qualifier=null, endpoint=[172.31.0.14]:5701, remoteUuid=8de6206e-d058-43bc-b1de-2fbbaa4dd804, alive=false, connectionType=MEMBER, planeIndex=0] closed. Reason: Exception in Connection[id=1, /172.31.0.12
- `speed` x 3: **2-spread**: setup: server did not start: WARNING: [172.31.0.12]:5701 [dev] [5.7.0] Connection[id=1, /172.31.0.12:5701->/172.31.0.14:55257, qualifier=null, endpoint=[172.31.0.14]:5701, remoteUuid=8de6206e-d058-43bc-b1de-2fbbaa4dd804, alive=false, connectionType=MEMBER, planeIndex=0] closed. Reason: Exception in Connection[id=1, /172.31.0.12
- `speed` x 3: **3-partial**: not run: server did not start: WARNING: [172.31.0.12]:5701 [dev] [5.7.0] Connection[id=1, /172.31.0.12:5701->/172.31.0.14:55257, qualifier=null, endpoint=[172.31.0.14]:5701, remoteUuid=8de6206e-d058-43bc-b1de-2fbbaa4dd804, alive=false, connectionType=MEMBER, planeIndex=0] closed. Reason: Exception in Connection[id=1, /172.31.0.12
- `speed` x 3: **4-smalldisk**: not run: server did not start: WARNING: [172.31.0.12]:5701 [dev] [5.7.0] Connection[id=1, /172.31.0.12:5701->/172.31.0.14:55257, qualifier=null, endpoint=[172.31.0.14]:5701, remoteUuid=8de6206e-d058-43bc-b1de-2fbbaa4dd804, alive=false, connectionType=MEMBER, planeIndex=0] closed. Reason: Exception in Connection[id=1, /172.31.0.12
- `speed` x 3: **5-lowdirect**: not run: server did not start: WARNING: [172.31.0.12]:5701 [dev] [5.7.0] Connection[id=1, /172.31.0.12:5701->/172.31.0.14:55257, qualifier=null, endpoint=[172.31.0.14]:5701, remoteUuid=8de6206e-d058-43bc-b1de-2fbbaa4dd804, alive=false, connectionType=MEMBER, planeIndex=0] closed. Reason: Exception in Connection[id=1, /172.31.0.12
- `speed` x 3: **6-logs**: not run: server did not start: WARNING: [172.31.0.12]:5701 [dev] [5.7.0] Connection[id=1, /172.31.0.12:5701->/172.31.0.14:55257, qualifier=null, endpoint=[172.31.0.14]:5701, remoteUuid=8de6206e-d058-43bc-b1de-2fbbaa4dd804, alive=false, connectionType=MEMBER, planeIndex=0] closed. Reason: Exception in Connection[id=1, /172.31.0.12

## Reference cells

- reference `default` x 1: setup fail, 0 answers, 0 errors
- reference `default` x 3: setup fail, 0 answers, 0 errors
- reference `speed` x 1: setup fail, 0 answers, 0 errors
- reference `speed` x 3: setup fail, 0 answers, 0 errors

Raw logs: run artifacts `cell-*`.
