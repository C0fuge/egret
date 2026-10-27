# Server comparison - Report 1: SPEED (compare run 40490378159)

## Experiment setup

| item | value |
|---|---|
| runner | GitHub-hosted `ubuntu-latest`: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor; Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor; Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor; RAM 15989 MB; kernel 6.17.0-1022-azure; JDK Temurin 21 |
| containers | every server: `eclipse-temurin:21-jre`, `--cpus=2 --cpuset-cpus=0,1 --memory=6g --memory-swap=6g`, JVM `-Xmx3g -XX:MaxDirectMemorySize=2g`, `MALLOC_ARENA_MAX=4`, host network; clients (JDBC/ADBC/Flight runners, jcmd sampling) and the S3 server in their own containers on cpus 2,3 |
| servers | ours-new = `7562a5bdb7b9` (DuckDB v1.5.6); ours-27f5 = `27f583adccd7` (DuckDB v1.5.6); up-native = `30855be44317d344f76d89043f1a6513afe60a8b` (DuckDB ?); up-main = `dbacd8d585bce2ef2a449c821fe3a53cc6060b57` (DuckDB error: INTERNAL: [FlightSQL] Error getting Arrow schema for query (Internal; ExecuteQuery). Vendor code: 13) |
| data | TPC-H SF1 and SF10, DuckDB dbgen, Parquet, 8 files per big table, 122880-row row groups, one data dir `tpch.*` per SF |
| storage | local disk (`file://`, page-cached) and S3 (`rclone serve s3` on the same runner, path style) |
| pairs | every job: ours-new (side A) vs one other server (side B) on the same runner, rounds A B / B A / A B (3), 1 cold run (warm-up) + warm runs per query (SF1 2 warm, SF10 1 warm per round) |
| settings | `def` = each server's default (`duckDbThreads` ours 4, upstream 2); `t8` = `-DduckDbThreads=8` on both |
| batch size | server defaults (not overridden) |
| clients | TPC-H: Python ADBC Flight SQL 1.12.0 (pyarrow 26), Flight SQL JDBC 18.0.0; small queries: same; scans: raw Flight (Arrow Java), ADBC export |
| SF30 | not run: SF1+SF10 already fill most of the repo's 10 GB Actions cache, SF30 Parquet (~11 GB) does not fit; generating it per job costs ~20 min of each 4-vCPU runner |
| JVM `ours-27f5` `def` | `--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED -Darrowflight.plugins.dir=/app/plugins -Darrowflight.duckdb.extensionDir=/ext/duckdb-home/extensions -DduckDbAllowUnsignedExtensions=true -Ds3Endpoint=http://127.0.0.1:9000 -Ds3UrlStyle=path -Ds3Region=us-east-1 -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf10 -cp --port --localhost --hosts` |
| JVM `ours-27f5` `t8` | `--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED -Darrowflight.plugins.dir=/app/plugins -Darrowflight.duckdb.extensionDir=/ext/duckdb-home/extensions -DduckDbAllowUnsignedExtensions=true -Ds3Endpoint=http://127.0.0.1:9000 -Ds3UrlStyle=path -Ds3Region=us-east-1 -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf10 -DduckDbThreads=8 -cp --port --localhost --hosts` |
| JVM `ours-new` `def` | `--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED -Darrowflight.plugins.dir=/app/plugins -Darrowflight.duckdb.extensionDir=/ext/duckdb-home/extensions -DduckDbAllowUnsignedExtensions=true -Ds3Endpoint=http://127.0.0.1:9000 -Ds3UrlStyle=path -Ds3Region=us-east-1 -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf10 -cp --port --localhost --hosts` |
| JVM `ours-new` `t8` | `--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED -Darrowflight.plugins.dir=/app/plugins -Darrowflight.duckdb.extensionDir=/ext/duckdb-home/extensions -DduckDbAllowUnsignedExtensions=true -Ds3Endpoint=http://127.0.0.1:9000 -Ds3UrlStyle=path -Ds3Region=us-east-1 -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf10 -DduckDbThreads=8 -cp --port --localhost --hosts` |
| JVM `up-main` `def` | `--add-modules --add-exports --add-opens --add-opens --add-opens=java.base/java.nio=ALL-UNNAMED --add-opens --add-opens -Dio.netty.tryReflectionSetAccessible=true -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf1 -cp --port --localhost --hosts` |
| JVM `up-main` `t8` | `--add-modules --add-exports --add-opens --add-opens --add-opens=java.base/java.nio=ALL-UNNAMED --add-opens --add-opens -Dio.netty.tryReflectionSetAccessible=true -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf1 -DduckDbThreads=8 -cp --port --localhost --hosts` |

Times are warm medians in ms (median over rounds of the per-round warm median). **n/a** = not run, failed or wrong
answer (reason in the notes). Last column: same-runner ratio best-upstream / ours-new (> 1 = ours-new faster).

## local, setting `def`

### TPC-H SF10, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 2204 | 1510 | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 317 | 251 | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1208 | 862 | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 800 | 615 | n/a | n/a | n/a |
| q05 | 6-way join | 1382 | 1076 | n/a | n/a | n/a |
| q06 | selective scan | 611 | 470 | n/a | n/a | n/a |
| q07 | joins, group by | 1388 | 996 | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 1708 | 1194 | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 3192 | 2508 | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1467 | 1115 | n/a | n/a | n/a |
| q11 | HAVING subquery | 292 | 212 | n/a | n/a | n/a |
| q12 | join, CASE agg | 814 | 598 | n/a | n/a | n/a |
| q13 | outer join, LIKE | 2337 | 1822 | n/a | n/a | n/a |
| q14 | join, CASE | 959 | 728 | n/a | n/a | n/a |
| q15 | view / CTE, max | 865 | 639 | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 475 | 326 | n/a | n/a | n/a |
| q17 | correlated avg | 1394 | 1024 | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 2449 | 1738 | n/a | n/a | n/a |
| q19 | OR predicates | 1382 | 1001 | n/a | n/a | n/a |
| q20 | nested IN | 1242 | 848 | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 4800 | 3723 | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 494 | 367 | n/a | n/a | n/a |
| **Score** | sum of the 0 queries every shown server answered | n/a | n/a | n/a | n/a | geomean n/a (0 q) |

- up-main: q01 failed; q02 failed; q03 failed; q04 failed; q05 failed; q06 failed; q07 failed; q08 failed; q09 failed; q10 failed; q11 failed; q12 failed; q13 failed; q14 failed; q15 failed; q16 failed; q17 failed; q18 failed; q19 failed; q20 failed; q21 failed; q22 failed
- up-native: not run: not in this setting's jobs

### TPC-H SF1, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 290 | 205 | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 54 | 47 | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 136 | 113 | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 94 | 70 | n/a | n/a | n/a |
| q05 | 6-way join | 138 | 105 | n/a | n/a | n/a |
| q06 | selective scan | 80 | 66 | n/a | n/a | n/a |
| q07 | joins, group by | 148 | 119 | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 176 | 128 | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 248 | 182 | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 177 | 131 | n/a | n/a | n/a |
| q11 | HAVING subquery | 42 | 37 | n/a | n/a | n/a |
| q12 | join, CASE agg | 103 | 76 | n/a | n/a | n/a |
| q13 | outer join, LIKE | 241 | 179 | n/a | n/a | n/a |
| q14 | join, CASE | 112 | 87 | n/a | n/a | n/a |
| q15 | view / CTE, max | 76 | 63 | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 66 | 51 | n/a | n/a | n/a |
| q17 | correlated avg | 136 | 109 | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 289 | 217 | n/a | n/a | n/a |
| q19 | OR predicates | 150 | 123 | n/a | n/a | n/a |
| q20 | nested IN | 124 | 101 | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 355 | 298 | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 58 | 47 | n/a | n/a | n/a |
| **Score** | sum of the 0 queries every shown server answered | n/a | n/a | n/a | n/a | geomean n/a (0 q) |

- up-main: q01 failed; q02 failed; q03 failed; q04 failed; q05 failed; q06 failed; q07 failed; q08 failed; q09 failed; q10 failed; q11 failed; q12 failed; q13 failed; q14 failed; q15 failed; q16 failed; q17 failed; q18 failed; q19 failed; q20 failed; q21 failed; q22 failed
- up-native: not run: not in this setting's jobs

### TPC-H SF10, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | n/a | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 241 | 260 | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 861 | 917 | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 606 | 608 | n/a | n/a | n/a |
| q05 | 6-way join | n/a | n/a | n/a | n/a | n/a |
| q06 | selective scan | n/a | n/a | n/a | n/a | n/a |
| q07 | joins, group by | n/a | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 1462 | 1291 | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | n/a | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1135 | 1136 | n/a | n/a | n/a |
| q11 | HAVING subquery | 225 | 218 | n/a | n/a | n/a |
| q12 | join, CASE agg | 617 | 605 | n/a | n/a | n/a |
| q13 | outer join, LIKE | 1813 | 1812 | n/a | n/a | n/a |
| q14 | join, CASE | 748 | 741 | n/a | n/a | n/a |
| q15 | view / CTE, max | n/a | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 351 | 351 | n/a | n/a | n/a |
| q17 | correlated avg | 1045 | 1037 | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 1846 | 1796 | n/a | n/a | n/a |
| q19 | OR predicates | n/a | n/a | n/a | n/a | n/a |
| q20 | nested IN | 870 | 858 | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 4293 | 3635 | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 373 | 352 | n/a | n/a | n/a |
| **Score** | sum of the 15 queries every shown server answered | 16486 | 15617 | n/a | n/a | geomean n/a (0 q) |

- ours-new: q01 wrong answer; q05 wrong answer; q06 wrong answer; q07 wrong answer; q09 wrong answer; q15 wrong answer; q19 wrong answer
- ours-27f5: q01 wrong answer; q05 wrong answer; q06 wrong answer; q07 wrong answer; q09 wrong answer; q15 wrong answer; q19 wrong answer
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### TPC-H SF1, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | n/a | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 49 | 58 | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 109 | 107 | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 86 | 78 | n/a | n/a | n/a |
| q05 | 6-way join | n/a | n/a | n/a | n/a | n/a |
| q06 | selective scan | n/a | n/a | n/a | n/a | n/a |
| q07 | joins, group by | n/a | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 139 | 136 | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | n/a | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 138 | 153 | n/a | n/a | n/a |
| q11 | HAVING subquery | 43 | 44 | n/a | n/a | n/a |
| q12 | join, CASE agg | 88 | 78 | n/a | n/a | n/a |
| q13 | outer join, LIKE | 177 | 193 | n/a | n/a | n/a |
| q14 | join, CASE | 88 | 86 | n/a | n/a | n/a |
| q15 | view / CTE, max | n/a | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 59 | 66 | n/a | n/a | n/a |
| q17 | correlated avg | 116 | 107 | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 221 | 220 | n/a | n/a | n/a |
| q19 | OR predicates | n/a | n/a | n/a | n/a | n/a |
| q20 | nested IN | 105 | 96 | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 294 | 271 | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 51 | 53 | n/a | n/a | n/a |
| **Score** | sum of the 15 queries every shown server answered | 1763 | 1746 | n/a | n/a | geomean n/a (0 q) |

- ours-new: q01 wrong answer; q05 wrong answer; q06 wrong answer; q07 wrong answer; q09 wrong answer; q15 wrong answer; q19 wrong answer
- ours-27f5: q01 wrong answer; q05 wrong answer; q06 wrong answer; q07 wrong answer; q09 wrong answer; q15 wrong answer; q19 wrong answer
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### Small queries (ms, p50 / p95 / p99 over all rounds)

| class | client | c | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|---|---|
| point_orders | JDBC | 1 | 24.4 / 35.8 / 38.4 | 28.1 / 38.3 / 43.5 | n/a | n/a (60 errors: t0 r-1: java.sql.SQLException: Error while executing SQL "SELECT o_orderkey, o_) |
| point_orders | JDBC | 8 | 115.6 / 197.9 / 405.5 | 130.3 / 190.9 / 226.1 | n/a | n/a (240 errors: t2 r-1: java.sql.SQLException: Error while executing SQL "SELECT o_orderkey, o_) |
| point_orders | JDBC | 32 | 507.9 / 1005.6 / 1524.1 | 511.3 / 888.2 / 1005.4 | n/a | n/a (480 errors: t31 r-1: java.sql.SQLException: Error while executing SQL "SELECT o_orderkey, o) |
| point_orders | ADBC | 1 | 15.6 / 25.3 / 32.3 | 20.3 / 27.7 / 46.1 | n/a | n/a |
| point_orders | ADBC | 8 | 98.4 / 153.5 / 178.0 | 125.5 / 186.6 / 231.4 | n/a | n/a (240 errors: t3 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| point_orders | ADBC | 32 | 402.7 / 760.2 / 947.6 | 429.1 / 743.8 / 893.1 | n/a | n/a (480 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| point_lineitem | JDBC | 1 | 34.0 / 43.6 / 61.9 | 38.5 / 49.1 / 66.4 | n/a | n/a (60 errors: t0 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l_) |
| point_lineitem | JDBC | 8 | 190.2 / 300.6 / 413.1 | 202.1 / 301.4 / 432.2 | n/a | n/a (240 errors: t3 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l_) |
| point_lineitem | JDBC | 32 | 787.1 / 1342.8 / 1743.5 | 786.9 / 1247.2 / 1531.0 | n/a | n/a (480 errors: t21 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l) |
| point_lineitem | ADBC | 1 | 24.4 / 37.1 / 40.6 | 29.2 / 45.9 / 53.8 | n/a | n/a |
| point_lineitem | ADBC | 8 | 174.4 / 266.8 / 324.8 | 195.0 / 278.6 / 330.0 | n/a | n/a (240 errors: t4 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| point_lineitem | ADBC | 32 | 744.0 / 1186.8 / 1491.7 | 776.4 / 1177.3 / 1476.7 | n/a | n/a (480 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| count_filter | JDBC | 1 | 48.9 / 60.3 / 67.7 | 52.0 / 64.7 / 73.3 | n/a | n/a (60 errors: t0 r-1: java.sql.SQLException: Error while executing SQL "SELECT count(*) FROM) |
| count_filter | JDBC | 8 | 236.2 / 289.8 / 329.0 | 244.7 / 321.9 / 389.7 | n/a | n/a (240 errors: t4 r-1: java.sql.SQLException: Error while executing SQL "SELECT count(*) FROM) |
| count_filter | JDBC | 32 | 882.7 / 1446.4 / 1999.3 | 955.5 / 1601.0 / 1905.0 | n/a | n/a (480 errors: t21 r-1: java.sql.SQLException: Error while executing SQL "SELECT count(*) FROM) |
| count_filter | ADBC | 1 | 40.7 / 54.2 / 70.3 | 46.7 / 70.9 / 81.4 | n/a | n/a |
| count_filter | ADBC | 8 | 231.0 / 302.2 / 337.7 | 239.8 / 297.3 / 325.4 | n/a | n/a (240 errors: t5 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| count_filter | ADBC | 32 | 891.5 / 1332.4 / 1544.5 | 962.9 / 1471.5 / 1716.0 | n/a | n/a (480 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| limit10_ob | JDBC | 1 | 44.6 / 61.5 / 81.3 | 50.7 / 68.7 / 77.4 | n/a | n/a (60 errors: t0 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l_) |
| limit10_ob | JDBC | 8 | 268.5 / 376.1 / 454.5 | 283.7 / 387.1 / 446.6 | n/a | n/a (240 errors: t5 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l_) |
| limit10_ob | JDBC | 32 | 1079.7 / 1714.4 / 2047.4 | 1162.6 / 1761.6 / 2334.4 | n/a | n/a (480 errors: t21 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l) |
| limit10_ob | ADBC | 1 | 37.8 / 58.0 / 66.7 | 42.7 / 63.9 / 71.4 | n/a | n/a |
| limit10_ob | ADBC | 8 | 254.0 / 361.3 / 398.6 | 266.0 / 348.7 / 437.2 | n/a | n/a (240 errors: t3 r-1: OperationalError: IO: [FlightSQL] error reading from server: EOF (Unava) |
| limit10_ob | ADBC | 32 | 1074.2 / 1681.5 / 2023.1 | 1185.1 / 1763.9 / 2066.8 | n/a | n/a (480 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| meta_tables | JDBC | 1 | 8.3 / 13.4 / 21.6 | 8.0 / 12.4 / 13.7 | n/a | 13.8 / 21.9 / 27.1 |
| meta_tables | JDBC | 8 | 12.1 / 27.7 / 37.0 | 13.8 / 342.3 / 838.2 | n/a | 41.7 / 72.2 / 107.9 |
| meta_tables | JDBC | 32 | 29.1 / 1271.7 / 1926.0 | 31.1 / 1193.0 / 1840.1 | n/a | n/a (480 errors: t0 r-1: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRunti) |
| meta_tables | ADBC | 1 | 8.2 / 12.1 / 15.7 | 7.8 / 9.6 / 11.1 | n/a | n/a |
| meta_tables | ADBC | 8 | 31.6 / 101.0 / 607.2 | 31.1 / 58.1 / 70.9 | n/a | n/a (240 errors: t3 r-1: OperationalError: IO: [FlightSQL] error reading from server: EOF (Unava) |
| meta_tables | ADBC | 32 | 89.8 / 948.7 / 2363.6 | 96.4 / 1899.4 / 3081.7 | n/a | n/a (480 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| meta_schemas | JDBC | 1 | 6.4 / 10.4 / 12.5 | 6.1 / 9.0 / 9.8 | n/a | 11.1 / 17.7 / 22.6 |
| meta_schemas | JDBC | 8 | 11.6 / 28.3 / 38.5 | 11.7 / 26.5 / 43.8 | n/a | 38.4 / 62.9 / 97.8 |
| meta_schemas | JDBC | 32 | 22.5 / 67.1 / 155.6 | 22.8 / 63.7 / 112.4 | n/a | n/a (480 errors: t0 r-1: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRunti) |
| meta_schemas | ADBC | 1 | 5.3 / 7.8 / 8.7 | 4.9 / 7.8 / 8.2 | n/a | n/a |
| meta_schemas | ADBC | 8 | 19.0 / 35.7 / 41.3 | 19.2 / 38.9 / 53.1 | n/a | n/a (240 errors: t3 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| meta_schemas | ADBC | 32 | 53.0 / 111.9 / 184.8 | 53.5 / 123.3 / 175.1 | n/a | n/a (480 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |

Answers per class are compared across servers in the run summary (`summary.md`, correctness gate).

### Scans (`SELECT * FROM tpch.lineitem`, SF10, MB/s of Arrow buffers) and server peak RSS

| metric | ours-new | ours-27f5 | up-native | up-main | ours-new vs best upstream |
|---|---|---|---|---|---|
| raw Flight, 1 stream | 418 | 446 | n/a | n/a | n/a |
| raw Flight, 4 streams | 502 | 499 | n/a | n/a | n/a |
| raw Flight, 8 streams | 460 | 462 | n/a | n/a | n/a |
| full export over ADBC | 535 | 514 | n/a | n/a | n/a |
| server peak RSS (MB) | 2188 | 1764 | n/a | 389 | - |

### Server container (docker stats every ~5 s, all workloads of this setting)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| CPU % p50 (200 = both cores) | 204 | 204 | n/a | 1 |
| CPU % max | 212 | 210 | n/a | 211 |
| memory peak (MiB, limit 6144) | 2741 | 1794 | n/a | 6141 |
| OOM-killed rounds | 0 / 9 | 0 / 6 | n/a | 3 / 3 |

## local, setting `t8`

### TPC-H SF10, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 2774 | 2799 | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 412 | 409 | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1555 | 1518 | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 1002 | 998 | n/a | n/a | n/a |
| q05 | 6-way join | 1800 | 1770 | n/a | n/a | n/a |
| q06 | selective scan | 756 | 757 | n/a | n/a | n/a |
| q07 | joins, group by | 1708 | 1714 | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 2082 | 2047 | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 4078 | 4161 | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1896 | 1842 | n/a | n/a | n/a |
| q11 | HAVING subquery | 372 | 396 | n/a | n/a | n/a |
| q12 | join, CASE agg | 1289 | 1039 | n/a | n/a | n/a |
| q13 | outer join, LIKE | 3028 | 3036 | n/a | n/a | n/a |
| q14 | join, CASE | 1228 | 1213 | n/a | n/a | n/a |
| q15 | view / CTE, max | 1103 | 1101 | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 634 | 596 | n/a | n/a | n/a |
| q17 | correlated avg | 1754 | 1744 | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 3665 | 3242 | n/a | n/a | n/a |
| q19 | OR predicates | 1684 | 1671 | n/a | n/a | n/a |
| q20 | nested IN | 1456 | 1446 | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 5668 | 5403 | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 613 | 590 | n/a | n/a | n/a |
| **Score** | sum of the 0 queries every shown server answered | n/a | n/a | n/a | n/a | geomean n/a (0 q) |

- up-main: q01 failed; q02 failed; q03 failed; q04 failed; q05 failed; q06 failed; q07 failed; q08 failed; q09 failed; q10 failed; q11 failed; q12 failed; q13 failed; q14 failed; q15 failed; q16 failed; q17 failed; q18 failed; q19 failed; q20 failed; q21 failed; q22 failed
- up-native: not run: not in this setting's jobs

### TPC-H SF1, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 392 | 385 | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 70 | 79 | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 174 | 188 | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 124 | 122 | n/a | n/a | n/a |
| q05 | 6-way join | 178 | 180 | n/a | n/a | n/a |
| q06 | selective scan | 96 | 107 | n/a | n/a | n/a |
| q07 | joins, group by | 190 | 204 | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 220 | 225 | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 310 | 314 | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 218 | 229 | n/a | n/a | n/a |
| q11 | HAVING subquery | 50 | 59 | n/a | n/a | n/a |
| q12 | join, CASE agg | 122 | 138 | n/a | n/a | n/a |
| q13 | outer join, LIKE | 289 | 304 | n/a | n/a | n/a |
| q14 | join, CASE | 139 | 146 | n/a | n/a | n/a |
| q15 | view / CTE, max | 104 | 106 | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 82 | 89 | n/a | n/a | n/a |
| q17 | correlated avg | 172 | 177 | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 396 | 401 | n/a | n/a | n/a |
| q19 | OR predicates | 186 | 193 | n/a | n/a | n/a |
| q20 | nested IN | 154 | 178 | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 457 | 473 | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 84 | 82 | n/a | n/a | n/a |
| **Score** | sum of the 0 queries every shown server answered | n/a | n/a | n/a | n/a | geomean n/a (0 q) |

- up-main: q01 failed; q02 failed; q03 failed; q04 failed; q05 failed; q06 failed; q07 failed; q08 failed; q09 failed; q10 failed; q11 failed; q12 failed; q13 failed; q14 failed; q15 failed; q16 failed; q17 failed; q18 failed; q19 failed; q20 failed; q21 failed; q22 failed
- up-native: not run: not in this setting's jobs

### TPC-H SF10, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | n/a | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 420 | 430 | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1493 | 1484 | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 1003 | 994 | n/a | n/a | n/a |
| q05 | 6-way join | n/a | n/a | n/a | n/a | n/a |
| q06 | selective scan | n/a | n/a | n/a | n/a | n/a |
| q07 | joins, group by | n/a | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 2060 | 2083 | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | n/a | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1844 | 1878 | n/a | n/a | n/a |
| q11 | HAVING subquery | 361 | 374 | n/a | n/a | n/a |
| q12 | join, CASE agg | 1035 | 1040 | n/a | n/a | n/a |
| q13 | outer join, LIKE | 3043 | 3024 | n/a | n/a | n/a |
| q14 | join, CASE | 1217 | 1215 | n/a | n/a | n/a |
| q15 | view / CTE, max | n/a | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 600 | 626 | n/a | n/a | n/a |
| q17 | correlated avg | 1744 | 1751 | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 3770 | 3783 | n/a | n/a | n/a |
| q19 | OR predicates | n/a | n/a | n/a | n/a | n/a |
| q20 | nested IN | 1432 | 1439 | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 5401 | 5452 | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 603 | 618 | n/a | n/a | n/a |
| **Score** | sum of the 15 queries every shown server answered | 26026 | 26191 | n/a | n/a | geomean n/a (0 q) |

- ours-new: q01 wrong answer; q05 wrong answer; q06 wrong answer; q07 wrong answer; q09 wrong answer; q15 wrong answer; q19 wrong answer
- ours-27f5: q01 wrong answer; q05 wrong answer; q06 wrong answer; q07 wrong answer; q09 wrong answer; q15 wrong answer; q19 wrong answer
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### TPC-H SF1, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | n/a | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 79 | 89 | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 186 | 196 | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 124 | 141 | n/a | n/a | n/a |
| q05 | 6-way join | n/a | n/a | n/a | n/a | n/a |
| q06 | selective scan | n/a | n/a | n/a | n/a | n/a |
| q07 | joins, group by | n/a | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 218 | 236 | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | n/a | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 219 | 230 | n/a | n/a | n/a |
| q11 | HAVING subquery | 62 | 68 | n/a | n/a | n/a |
| q12 | join, CASE agg | 130 | 145 | n/a | n/a | n/a |
| q13 | outer join, LIKE | 297 | 292 | n/a | n/a | n/a |
| q14 | join, CASE | 144 | 144 | n/a | n/a | n/a |
| q15 | view / CTE, max | n/a | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 111 | 111 | n/a | n/a | n/a |
| q17 | correlated avg | 174 | 178 | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 402 | 406 | n/a | n/a | n/a |
| q19 | OR predicates | n/a | n/a | n/a | n/a | n/a |
| q20 | nested IN | 153 | 162 | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 446 | 447 | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 78 | 82 | n/a | n/a | n/a |
| **Score** | sum of the 15 queries every shown server answered | 2823 | 2927 | n/a | n/a | geomean n/a (0 q) |

- ours-new: q01 wrong answer; q05 wrong answer; q06 wrong answer; q07 wrong answer; q09 wrong answer; q15 wrong answer; q19 wrong answer
- ours-27f5: q01 wrong answer; q05 wrong answer; q06 wrong answer; q07 wrong answer; q09 wrong answer; q15 wrong answer; q19 wrong answer
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### Small queries (ms, p50 / p95 / p99 over all rounds)

| class | client | c | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|---|---|
| point_orders | JDBC | 1 | 25.2 / 35.4 / 45.9 | 28.1 / 40.1 / 42.8 | n/a | n/a (60 errors: t0 r-1: java.sql.SQLException: Error while executing SQL "SELECT o_orderkey, o_) |
| point_orders | JDBC | 8 | 134.9 / 218.1 / 304.3 | 146.8 / 222.1 / 258.2 | n/a | n/a (240 errors: t2 r-1: java.sql.SQLException: Error while executing SQL "SELECT o_orderkey, o_) |
| point_orders | JDBC | 32 | 596.0 / 1185.3 / 1589.7 | 625.1 / 1068.7 / 1292.6 | n/a | n/a (480 errors: t2 r-1: java.sql.SQLException: Error while executing SQL "SELECT o_orderkey, o_) |
| point_orders | ADBC | 1 | 17.0 / 25.7 / 33.4 | 20.9 / 30.5 / 31.9 | n/a | n/a |
| point_orders | ADBC | 8 | 108.7 / 178.0 / 195.1 | 139.7 / 213.0 / 262.5 | n/a | n/a (240 errors: t4 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| point_orders | ADBC | 32 | 474.6 / 852.3 / 1034.2 | 496.7 / 839.7 / 1088.5 | n/a | n/a (480 errors: t7 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| point_lineitem | JDBC | 1 | 34.4 / 46.4 / 51.1 | 38.3 / 49.4 / 63.1 | n/a | n/a (60 errors: t0 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l_) |
| point_lineitem | JDBC | 8 | 201.7 / 304.0 / 416.6 | 205.4 / 289.5 / 433.3 | n/a | n/a (240 errors: t3 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l_) |
| point_lineitem | JDBC | 32 | 823.0 / 1374.4 / 1682.3 | 877.0 / 1290.2 / 1552.5 | n/a | n/a (480 errors: t9 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l_) |
| point_lineitem | ADBC | 1 | 25.0 / 38.9 / 47.7 | 30.2 / 42.6 / 46.7 | n/a | n/a |
| point_lineitem | ADBC | 8 | 185.4 / 291.4 / 364.9 | 200.8 / 313.0 / 401.2 | n/a | n/a (240 errors: t4 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| point_lineitem | ADBC | 32 | 780.6 / 1300.4 / 1575.4 | 783.9 / 1198.4 / 1384.7 | n/a | n/a (480 errors: t7 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| count_filter | JDBC | 1 | 50.7 / 66.4 / 84.7 | 54.3 / 65.8 / 70.7 | n/a | n/a (60 errors: t0 r-1: java.sql.SQLException: Error while executing SQL "SELECT count(*) FROM) |
| count_filter | JDBC | 8 | 208.8 / 291.9 / 409.4 | 220.7 / 296.9 / 306.1 | n/a | n/a (240 errors: t4 r-1: java.sql.SQLException: Error while executing SQL "SELECT count(*) FROM) |
| count_filter | JDBC | 32 | 831.9 / 1441.9 / 2169.7 | 913.1 / 1786.9 / 2216.3 | n/a | n/a (480 errors: t10 r-1: java.sql.SQLException: Error while executing SQL "SELECT count(*) FROM) |
| count_filter | ADBC | 1 | 43.3 / 56.4 / 73.9 | 47.3 / 58.6 / 59.6 | n/a | n/a |
| count_filter | ADBC | 8 | 203.9 / 297.4 / 346.0 | 220.4 / 292.2 / 331.3 | n/a | n/a (240 errors: t5 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| count_filter | ADBC | 32 | 829.8 / 1372.9 / 1623.3 | 950.9 / 1504.6 / 1742.4 | n/a | n/a (480 errors: t7 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| limit10_ob | JDBC | 1 | 47.9 / 61.3 / 67.8 | 54.2 / 70.1 / 88.3 | n/a | n/a (60 errors: t0 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l_) |
| limit10_ob | JDBC | 8 | 281.3 / 406.4 / 475.5 | 291.3 / 399.9 / 449.9 | n/a | n/a (240 errors: t5 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l_) |
| limit10_ob | JDBC | 32 | 1151.7 / 1811.1 / 2074.4 | 1191.8 / 1865.9 / 2393.3 | n/a | n/a (480 errors: t29 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l) |
| limit10_ob | ADBC | 1 | 40.8 / 57.3 / 68.4 | 44.2 / 66.7 / 71.6 | n/a | n/a |
| limit10_ob | ADBC | 8 | 271.9 / 404.5 / 457.1 | 289.6 / 397.0 / 457.9 | n/a | n/a (240 errors: t0 r-1: OperationalError: IO: [FlightSQL] error reading from server: EOF (Unava) |
| limit10_ob | ADBC | 32 | 1170.5 / 1799.0 / 2136.8 | 1278.5 / 1934.5 / 2285.5 | n/a | n/a (480 errors: t7 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| meta_tables | JDBC | 1 | 8.4 / 13.3 / 18.7 | 8.1 / 12.8 / 16.4 | n/a | 14.1 / 24.5 / 26.4 |
| meta_tables | JDBC | 8 | 13.5 / 36.9 / 94.8 | 13.8 / 437.0 / 917.1 | n/a | 41.5 / 74.8 / 91.3 |
| meta_tables | JDBC | 32 | 35.9 / 1334.8 / 1997.9 | 36.0 / 490.4 / 1816.7 | n/a | n/a (480 errors: t12 r-1: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRunt) |
| meta_tables | ADBC | 1 | 8.2 / 12.6 / 19.2 | 7.4 / 10.4 / 12.5 | n/a | n/a |
| meta_tables | ADBC | 8 | 34.8 / 100.6 / 493.2 | 33.3 / 64.0 / 77.8 | n/a | n/a (240 errors: t4 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| meta_tables | ADBC | 32 | 101.8 / 1093.1 / 2645.4 | 112.0 / 1613.1 / 3300.5 | n/a | n/a (480 errors: t7 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| meta_schemas | JDBC | 1 | 6.4 / 10.2 / 12.6 | 5.8 / 8.9 / 10.3 | n/a | 11.6 / 17.8 / 21.4 |
| meta_schemas | JDBC | 8 | 15.1 / 37.2 / 48.4 | 11.9 / 27.3 / 45.8 | n/a | 38.8 / 64.2 / 87.2 |
| meta_schemas | JDBC | 32 | 24.5 / 77.7 / 120.8 | 25.6 / 76.8 / 133.9 | n/a | n/a (480 errors: t12 r-1: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRunt) |
| meta_schemas | ADBC | 1 | 5.0 / 9.3 / 15.3 | 4.8 / 7.6 / 8.1 | n/a | n/a |
| meta_schemas | ADBC | 8 | 20.7 / 45.9 / 63.3 | 20.8 / 54.5 / 68.9 | n/a | n/a (240 errors: t4 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| meta_schemas | ADBC | 32 | 54.9 / 142.2 / 213.3 | 55.9 / 119.7 / 185.2 | n/a | n/a (480 errors: t7 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |

Answers per class are compared across servers in the run summary (`summary.md`, correctness gate).

### Scans (`SELECT * FROM tpch.lineitem`, SF10, MB/s of Arrow buffers) and server peak RSS

| metric | ours-new | ours-27f5 | up-native | up-main | ours-new vs best upstream |
|---|---|---|---|---|---|
| raw Flight, 1 stream | 438 | 422 | n/a | n/a | n/a |
| raw Flight, 4 streams | 452 | 428 | n/a | n/a | n/a |
| raw Flight, 8 streams | 393 | 381 | n/a | n/a | n/a |
| full export over ADBC | 513 | 485 | n/a | n/a | n/a |
| server peak RSS (MB) | 2251 | 1922 | n/a | 413 | - |

### Server container (docker stats every ~5 s, all workloads of this setting)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| CPU % p50 (200 = both cores) | 201 | 201 | n/a | 1 |
| CPU % max | 211 | 204 | n/a | 204 |
| memory peak (MiB, limit 6144) | 2664 | 1924 | n/a | 6143 |
| OOM-killed rounds | 0 / 9 | 0 / 6 | n/a | 3 / 3 |

## s3, setting `def`

### TPC-H SF10, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 8215 | 10617 | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 3638 | 4490 | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 18855 | 18699 | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 11767 | 11527 | n/a | n/a | n/a |
| q05 | 6-way join | 20997 | 21690 | n/a | n/a | n/a |
| q06 | selective scan | 12883 | 18257 | n/a | n/a | n/a |
| q07 | joins, group by | 18446 | 24513 | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 24168 | 28259 | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 21940 | 28960 | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 13432 | 17536 | n/a | n/a | n/a |
| q11 | HAVING subquery | 3589 | 3747 | n/a | n/a | n/a |
| q12 | join, CASE agg | 19801 | 20340 | n/a | n/a | n/a |
| q13 | outer join, LIKE | 5631 | 5518 | n/a | n/a | n/a |
| q14 | join, CASE | 18891 | 19489 | n/a | n/a | n/a |
| q15 | view / CTE, max | 17294 | 17445 | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 1547 | 1665 | n/a | n/a | n/a |
| q17 | correlated avg | 23897 | 26397 | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 17797 | 18244 | n/a | n/a | n/a |
| q19 | OR predicates | 19045 | 18759 | n/a | n/a | n/a |
| q20 | nested IN | 21849 | 22303 | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 50013 | 52387 | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 2685 | 2566 | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 356380 | 393408 | n/a | n/a | geomean n/a (0 q) |

- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF1, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 774 | 912 | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 378 | 513 | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1401 | 1821 | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 853 | 1131 | n/a | n/a | n/a |
| q05 | 6-way join | 1352 | 1840 | n/a | n/a | n/a |
| q06 | selective scan | 1162 | 1631 | n/a | n/a | n/a |
| q07 | joins, group by | 1628 | 2095 | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 1857 | 2394 | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 2088 | 2469 | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1317 | 1702 | n/a | n/a | n/a |
| q11 | HAVING subquery | 307 | 387 | n/a | n/a | n/a |
| q12 | join, CASE agg | 1465 | 1899 | n/a | n/a | n/a |
| q13 | outer join, LIKE | 373 | 462 | n/a | n/a | n/a |
| q14 | join, CASE | 1249 | 1703 | n/a | n/a | n/a |
| q15 | view / CTE, max | 1052 | 1407 | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 158 | 173 | n/a | n/a | n/a |
| q17 | correlated avg | 1698 | 2295 | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 1407 | 1800 | n/a | n/a | n/a |
| q19 | OR predicates | 1488 | 1770 | n/a | n/a | n/a |
| q20 | nested IN | 1416 | 1839 | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 2616 | 3496 | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 200 | 248 | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 26239 | 33987 | n/a | n/a | geomean n/a (0 q) |

- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF10, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | n/a | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 4549 | 4606 | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 20050 | 18889 | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 11407 | 11497 | n/a | n/a | n/a |
| q05 | 6-way join | n/a | n/a | n/a | n/a | n/a |
| q06 | selective scan | n/a | n/a | n/a | n/a | n/a |
| q07 | joins, group by | n/a | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 28140 | 28118 | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | n/a | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 17368 | 16985 | n/a | n/a | n/a |
| q11 | HAVING subquery | 3761 | 3697 | n/a | n/a | n/a |
| q12 | join, CASE agg | 19600 | 19355 | n/a | n/a | n/a |
| q13 | outer join, LIKE | 5612 | 5440 | n/a | n/a | n/a |
| q14 | join, CASE | 17527 | 17752 | n/a | n/a | n/a |
| q15 | view / CTE, max | n/a | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 1574 | 1474 | n/a | n/a | n/a |
| q17 | correlated avg | 23402 | 23505 | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 17745 | 17807 | n/a | n/a | n/a |
| q19 | OR predicates | n/a | n/a | n/a | n/a | n/a |
| q20 | nested IN | 22256 | 22344 | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 43746 | 42841 | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 2534 | 2500 | n/a | n/a | n/a |
| **Score** | sum of the 15 queries every shown server answered | 239271 | 236810 | n/a | n/a | geomean n/a (0 q) |

- ours-new: q01 wrong answer; q05 wrong answer; q06 wrong answer; q07 wrong answer; q09 wrong answer; q15 wrong answer; q19 wrong answer
- ours-27f5: q01 wrong answer; q05 wrong answer; q06 wrong answer; q07 wrong answer; q09 wrong answer; q15 wrong answer; q19 wrong answer
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### TPC-H SF1, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | n/a | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 371 | 413 | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1292 | 1261 | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 1099 | 1167 | n/a | n/a | n/a |
| q05 | 6-way join | n/a | n/a | n/a | n/a | n/a |
| q06 | selective scan | n/a | n/a | n/a | n/a | n/a |
| q07 | joins, group by | n/a | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 2446 | 2662 | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | n/a | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1609 | 1661 | n/a | n/a | n/a |
| q11 | HAVING subquery | 358 | 344 | n/a | n/a | n/a |
| q12 | join, CASE agg | 1843 | 1953 | n/a | n/a | n/a |
| q13 | outer join, LIKE | 436 | 466 | n/a | n/a | n/a |
| q14 | join, CASE | 1694 | 1700 | n/a | n/a | n/a |
| q15 | view / CTE, max | n/a | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 183 | 181 | n/a | n/a | n/a |
| q17 | correlated avg | 2247 | 2260 | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 1737 | 1839 | n/a | n/a | n/a |
| q19 | OR predicates | n/a | n/a | n/a | n/a | n/a |
| q20 | nested IN | 1744 | 1847 | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 3448 | 3410 | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 246 | 251 | n/a | n/a | n/a |
| **Score** | sum of the 15 queries every shown server answered | 20753 | 21415 | n/a | n/a | geomean n/a (0 q) |

- ours-new: q01 wrong answer; q05 wrong answer; q06 wrong answer; q07 wrong answer; q09 wrong answer; q15 wrong answer; q19 wrong answer
- ours-27f5: q01 wrong answer; q05 wrong answer; q06 wrong answer; q07 wrong answer; q09 wrong answer; q15 wrong answer; q19 wrong answer
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### Small queries (ms, p50 / p95 / p99 over all rounds)

| class | client | c | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|---|---|
| point_orders | JDBC | 1 | 31.6 / 42.5 / 81.3 | 38.7 / 52.5 / 60.8 | n/a | n/a |
| point_orders | JDBC | 8 | 391.9 / 691.0 / 830.4 | 425.7 / 685.7 / 1130.4 | n/a | n/a |
| point_orders | JDBC | 32 | 1525.0 / 3461.4 / 12410.5 | 1522.0 / 2819.4 / 4026.9 | n/a | n/a |
| point_orders | ADBC | 1 | 24.1 / 45.4 / 76.2 | 28.2 / 46.4 / 148.6 | n/a | n/a |
| point_orders | ADBC | 8 | 383.0 / 673.5 / 854.7 | 447.0 / 794.8 / 946.1 | n/a | n/a |
| point_orders | ADBC | 32 | 1526.4 / 3441.0 / 10015.4 | 1601.8 / 3333.9 / 8736.3 | n/a | n/a |
| point_lineitem | JDBC | 1 | 29.6 / 50.2 / 641.4 | 34.8 / 55.5 / 132.2 | n/a | n/a |
| point_lineitem | JDBC | 8 | 242.2 / 460.6 / 1729.4 | 263.3 / 4242.3 / 7517.9 | n/a | n/a |
| point_lineitem | JDBC | 32 | 865.8 / 10152.6 / 39720.0 | 866.8 / 8914.6 / 20416.5 | n/a | n/a |
| point_lineitem | ADBC | 1 | 18.8 / 39.0 / 93.8 | 25.2 / 41.5 / 47.8 | n/a | n/a |
| point_lineitem | ADBC | 8 | 247.8 / 454.2 / 4467.8 | 261.7 / 462.0 / 555.2 | n/a | n/a |
| point_lineitem | ADBC | 32 | 844.8 / 11619.8 / 26394.5 | 949.1 / 10278.9 / 19062.1 | n/a | n/a |
| count_filter | JDBC | 1 | 663.5 / 797.4 / 904.7 | 640.2 / 725.3 / 760.5 | n/a | n/a |
| count_filter | JDBC | 8 | 5014.1 / 8304.4 / 8956.5 | 4996.6 / 5693.6 / 8761.6 | n/a | n/a |
| count_filter | JDBC | 32 | 16596.8 / 33208.9 / 48158.4 | 16679.9 / 26980.3 / 29454.1 | n/a | n/a |
| count_filter | ADBC | 1 | 679.6 / 1123.7 / 1249.9 | 675.9 / 753.9 / 801.3 | n/a | n/a |
| count_filter | ADBC | 8 | 5114.8 / 8107.2 / 10604.0 | 5326.4 / 7987.1 / 8183.7 | n/a | n/a |
| count_filter | ADBC | 32 | 16790.0 / 31452.2 / 51520.0 | 16337.1 / 46134.3 / 55985.2 | n/a | n/a |
| limit10_ob | JDBC | 1 | 128.2 / 208.0 / 422.9 | 112.8 / 139.2 / 178.3 | n/a | n/a |
| limit10_ob | JDBC | 8 | 748.0 / 1220.0 / 11469.9 | 786.5 / 1455.5 / 7198.0 | n/a | n/a |
| limit10_ob | JDBC | 32 | 2815.4 / 33752.4 / 66779.2 | 2741.9 / 5697.1 / 33658.3 | n/a | n/a |
| limit10_ob | ADBC | 1 | 126.3 / 204.3 / 251.9 | 110.6 / 140.8 / 152.4 | n/a | n/a |
| limit10_ob | ADBC | 8 | 758.3 / 1273.4 / 2471.3 | 837.1 / 1335.4 / 1608.3 | n/a | n/a |
| limit10_ob | ADBC | 32 | 2758.2 / 15930.8 / 54486.0 | 2850.5 / 5683.0 / 28653.6 | n/a | n/a |
| meta_tables | JDBC | 1 | 8.4 / 14.4 / 18.1 | 8.6 / 13.4 / 14.7 | n/a | n/a |
| meta_tables | JDBC | 8 | 5.5 / 17.1 / 25.3 | 5.4 / 12.6 / 18.6 | n/a | n/a |
| meta_tables | JDBC | 32 | 5.9 / 25.5 / 63.5 | 7.3 / 27.5 / 40.0 | n/a | n/a |
| meta_tables | ADBC | 1 | 8.8 / 15.0 / 19.4 | 7.8 / 13.3 / 17.2 | n/a | n/a |
| meta_tables | ADBC | 8 | 8.5 / 23.1 / 30.5 | 8.1 / 20.2 / 37.6 | n/a | n/a |
| meta_tables | ADBC | 32 | 18.0 / 49.2 / 69.3 | 17.8 / 51.3 / 84.2 | n/a | n/a |
| meta_schemas | JDBC | 1 | 6.3 / 12.2 / 15.7 | 6.5 / 11.3 / 14.7 | n/a | n/a |
| meta_schemas | JDBC | 8 | 4.7 / 16.5 / 30.6 | 4.4 / 12.8 / 20.6 | n/a | n/a |
| meta_schemas | JDBC | 32 | 6.0 / 34.3 / 66.3 | 5.7 / 29.1 / 44.2 | n/a | n/a |
| meta_schemas | ADBC | 1 | 5.1 / 8.5 / 13.2 | 5.0 / 7.5 / 9.3 | n/a | n/a |
| meta_schemas | ADBC | 8 | 5.9 / 16.7 / 26.0 | 5.6 / 14.1 / 19.7 | n/a | n/a |
| meta_schemas | ADBC | 32 | 11.6 / 45.6 / 83.6 | 11.6 / 43.4 / 118.8 | n/a | n/a |

Answers per class are compared across servers in the run summary (`summary.md`, correctness gate).

### Scans (`SELECT * FROM tpch.lineitem`, SF10, MB/s of Arrow buffers) and server peak RSS

| metric | ours-new | ours-27f5 | up-native | up-main | ours-new vs best upstream |
|---|---|---|---|---|---|
| raw Flight, 1 stream | 401 | 409 | n/a | n/a | n/a |
| raw Flight, 4 streams | 486 | 486 | n/a | n/a | n/a |
| raw Flight, 8 streams | 457 | 461 | n/a | n/a | n/a |
| full export over ADBC | 441 | 418 | n/a | n/a | n/a |
| server peak RSS (MB) | 2188 | 2601 | n/a | n/a | - |

### Server container (docker stats every ~5 s, all workloads of this setting)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| CPU % p50 (200 = both cores) | 33 | 20 | n/a | n/a |
| CPU % max | 211 | 210 | n/a | n/a |
| memory peak (MiB, limit 6144) | 2772 | 2553 | n/a | n/a |
| OOM-killed rounds | 0 / 12 | 0 / 6 | 0 / 3 | 0 / 3 |

## s3, setting `t8`

### TPC-H SF10, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 9705 | 10350 | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 4038 | 4474 | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 17605 | 24798 | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 10501 | 11043 | n/a | n/a | n/a |
| q05 | 6-way join | 19050 | 23243 | n/a | n/a | n/a |
| q06 | selective scan | 16249 | 11003 | n/a | n/a | n/a |
| q07 | joins, group by | 24297 | 24327 | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 29906 | 28550 | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 39133 | 28736 | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 23469 | 16896 | n/a | n/a | n/a |
| q11 | HAVING subquery | 5041 | 3601 | n/a | n/a | n/a |
| q12 | join, CASE agg | 26301 | 25858 | n/a | n/a | n/a |
| q13 | outer join, LIKE | 7293 | 5854 | n/a | n/a | n/a |
| q14 | join, CASE | 24190 | 17797 | n/a | n/a | n/a |
| q15 | view / CTE, max | 23171 | 12730 | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 1821 | 1181 | n/a | n/a | n/a |
| q17 | correlated avg | 32450 | 19117 | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 24600 | 17918 | n/a | n/a | n/a |
| q19 | OR predicates | 25417 | 18023 | n/a | n/a | n/a |
| q20 | nested IN | 30950 | 21912 | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 59892 | 43137 | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 3196 | 2826 | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 458275 | 373374 | n/a | n/a | geomean n/a (0 q) |

- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF1, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 834 | 724 | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 436 | 534 | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1452 | 1548 | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 899 | 1042 | n/a | n/a | n/a |
| q05 | 6-way join | 1449 | 1653 | n/a | n/a | n/a |
| q06 | selective scan | 1335 | 1096 | n/a | n/a | n/a |
| q07 | joins, group by | 1673 | 1914 | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 2046 | 2085 | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 2061 | 2460 | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1378 | 1964 | n/a | n/a | n/a |
| q11 | HAVING subquery | 344 | 381 | n/a | n/a | n/a |
| q12 | join, CASE agg | 1591 | 1842 | n/a | n/a | n/a |
| q13 | outer join, LIKE | 421 | 433 | n/a | n/a | n/a |
| q14 | join, CASE | 1355 | 1659 | n/a | n/a | n/a |
| q15 | view / CTE, max | 1198 | 1468 | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 158 | 145 | n/a | n/a | n/a |
| q17 | correlated avg | 1845 | 2200 | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 1360 | 1628 | n/a | n/a | n/a |
| q19 | OR predicates | 1490 | 1575 | n/a | n/a | n/a |
| q20 | nested IN | 1487 | 1770 | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 2802 | 3159 | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 197 | 238 | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 27811 | 31518 | n/a | n/a | geomean n/a (0 q) |

- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF10, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | n/a | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 3760 | 3046 | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 18109 | 13023 | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 11202 | 9293 | n/a | n/a | n/a |
| q05 | 6-way join | n/a | n/a | n/a | n/a | n/a |
| q06 | selective scan | n/a | n/a | n/a | n/a | n/a |
| q07 | joins, group by | n/a | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 28486 | 20411 | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | n/a | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 16980 | 11644 | n/a | n/a | n/a |
| q11 | HAVING subquery | 3887 | 3687 | n/a | n/a | n/a |
| q12 | join, CASE agg | 18639 | 17856 | n/a | n/a | n/a |
| q13 | outer join, LIKE | 5616 | 4526 | n/a | n/a | n/a |
| q14 | join, CASE | 18125 | 14686 | n/a | n/a | n/a |
| q15 | view / CTE, max | n/a | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 1817 | 1476 | n/a | n/a | n/a |
| q17 | correlated avg | 23942 | 16212 | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 17573 | 12098 | n/a | n/a | n/a |
| q19 | OR predicates | n/a | n/a | n/a | n/a | n/a |
| q20 | nested IN | 22512 | 14667 | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 43809 | 47534 | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 2874 | 2135 | n/a | n/a | n/a |
| **Score** | sum of the 15 queries every shown server answered | 237331 | 192294 | n/a | n/a | geomean n/a (0 q) |

- ours-new: q01 wrong answer; q05 wrong answer; q06 wrong answer; q07 wrong answer; q09 wrong answer; q15 wrong answer; q19 wrong answer
- ours-27f5: q01 wrong answer; q05 wrong answer; q06 wrong answer; q07 wrong answer; q09 wrong answer; q15 wrong answer; q19 wrong answer
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### TPC-H SF1, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | n/a | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 521 | 361 | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1147 | 1454 | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 693 | 796 | n/a | n/a | n/a |
| q05 | 6-way join | n/a | n/a | n/a | n/a | n/a |
| q06 | selective scan | n/a | n/a | n/a | n/a | n/a |
| q07 | joins, group by | n/a | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 2700 | 2500 | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | n/a | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1564 | 1623 | n/a | n/a | n/a |
| q11 | HAVING subquery | 255 | 331 | n/a | n/a | n/a |
| q12 | join, CASE agg | 1708 | 1556 | n/a | n/a | n/a |
| q13 | outer join, LIKE | 353 | 425 | n/a | n/a | n/a |
| q14 | join, CASE | 1722 | 1526 | n/a | n/a | n/a |
| q15 | view / CTE, max | n/a | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 266 | 446 | n/a | n/a | n/a |
| q17 | correlated avg | 2313 | 1576 | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 1607 | 1917 | n/a | n/a | n/a |
| q19 | OR predicates | n/a | n/a | n/a | n/a | n/a |
| q20 | nested IN | 1735 | 2366 | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 3114 | 4454 | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 181 | 173 | n/a | n/a | n/a |
| **Score** | sum of the 15 queries every shown server answered | 19879 | 21504 | n/a | n/a | geomean n/a (0 q) |

- ours-new: q01 wrong answer; q05 wrong answer; q06 wrong answer; q07 wrong answer; q09 wrong answer; q15 wrong answer; q19 wrong answer
- ours-27f5: q01 wrong answer; q05 wrong answer; q06 wrong answer; q07 wrong answer; q09 wrong answer; q15 wrong answer; q19 wrong answer
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### Small queries (ms, p50 / p95 / p99 over all rounds)

| class | client | c | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|---|---|
| point_orders | JDBC | 1 | 32.7 / 46.0 / 105.0 | 35.1 / 119.9 / 200.0 | n/a | n/a |
| point_orders | JDBC | 8 | 590.0 / 1130.0 / 1428.8 | 525.4 / 997.2 / 1368.9 | n/a | n/a |
| point_orders | JDBC | 32 | 2259.4 / 6007.1 / 32553.2 | 1985.2 / 3766.5 / 12173.7 | n/a | n/a |
| point_orders | ADBC | 1 | 24.1 / 49.8 / 125.9 | 26.8 / 70.5 / 84.3 | n/a | n/a |
| point_orders | ADBC | 8 | 627.0 / 1136.4 / 1788.6 | 540.3 / 948.7 / 1151.7 | n/a | n/a |
| point_orders | ADBC | 32 | 2259.4 / 5776.6 / 8562.5 | 2095.7 / 3941.6 / 16184.7 | n/a | n/a |
| point_lineitem | JDBC | 1 | 28.6 / 50.7 / 81.8 | 29.5 / 224.5 / 351.8 | n/a | n/a |
| point_lineitem | JDBC | 8 | 346.8 / 749.3 / 10083.9 | 267.3 / 554.6 / 912.1 | n/a | n/a |
| point_lineitem | JDBC | 32 | 1212.0 / 3694.1 / 61919.9 | 954.5 / 13197.5 / 21295.2 | n/a | n/a |
| point_lineitem | ADBC | 1 | 20.5 / 39.6 / 46.9 | 22.2 / 139.8 / 198.2 | n/a | n/a |
| point_lineitem | ADBC | 8 | 351.6 / 718.9 / 933.4 | 295.5 / 520.5 / 5984.1 | n/a | n/a |
| point_lineitem | ADBC | 32 | 1242.6 / 4147.5 / 33211.8 | 969.2 / 1675.2 / 12950.9 | n/a | n/a |
| count_filter | JDBC | 1 | 736.0 / 850.5 / 978.9 | 631.9 / 1093.1 / 1170.0 | n/a | n/a |
| count_filter | JDBC | 8 | 3951.5 / 6150.2 / 7140.5 | 2984.0 / 6701.9 / 10803.4 | n/a | n/a |
| count_filter | JDBC | 32 | 14524.5 / 35512.1 / 61087.7 | 8331.6 / 12357.5 / 25240.8 | n/a | n/a |
| count_filter | ADBC | 1 | 754.9 / 878.6 / 1024.4 | 630.3 / 810.6 / 871.2 | n/a | n/a |
| count_filter | ADBC | 8 | 4212.2 / 7949.2 / 18099.2 | 2694.7 / 3287.7 / 3486.2 | n/a | n/a |
| count_filter | ADBC | 32 | 13472.7 / 32199.7 / 59043.5 | 9125.1 / 23830.7 / 27309.9 | n/a | n/a |
| limit10_ob | JDBC | 1 | 168.7 / 236.0 / 265.9 | 145.8 / 388.8 / 525.5 | n/a | n/a |
| limit10_ob | JDBC | 8 | 1251.2 / 2467.6 / 24209.4 | 970.3 / 1610.4 / 2060.9 | n/a | n/a |
| limit10_ob | JDBC | 32 | 4805.3 / 66440.5 / 94941.2 | 3774.0 / 17478.2 / 33883.8 | n/a | n/a |
| limit10_ob | ADBC | 1 | 162.1 / 253.1 / 394.7 | 136.2 / 298.1 / 322.0 | n/a | n/a |
| limit10_ob | ADBC | 8 | 1285.6 / 2234.3 / 2937.7 | 989.4 / 1605.0 / 5301.5 | n/a | n/a |
| limit10_ob | ADBC | 32 | 4647.9 / 35006.3 / 67750.8 | 3845.6 / 6325.0 / 16187.9 | n/a | n/a |
| meta_tables | JDBC | 1 | 8.5 / 14.5 / 16.5 | 7.1 / 12.0 / 14.0 | n/a | n/a |
| meta_tables | JDBC | 8 | 6.2 / 17.0 / 28.3 | 6.1 / 15.1 / 21.0 | n/a | n/a |
| meta_tables | JDBC | 32 | 8.5 / 27.5 / 59.4 | 10.7 / 30.0 / 44.9 | n/a | n/a |
| meta_tables | ADBC | 1 | 9.4 / 15.5 / 21.9 | 6.7 / 10.7 / 17.5 | n/a | n/a |
| meta_tables | ADBC | 8 | 9.8 / 23.2 / 31.3 | 8.8 / 22.2 / 32.7 | n/a | n/a |
| meta_tables | ADBC | 32 | 24.3 / 56.7 / 79.1 | 27.5 / 67.1 / 109.7 | n/a | n/a |
| meta_schemas | JDBC | 1 | 6.7 / 11.3 / 18.5 | 5.1 / 9.4 / 13.5 | n/a | n/a |
| meta_schemas | JDBC | 8 | 5.3 / 17.6 / 27.4 | 4.9 / 11.7 / 21.4 | n/a | n/a |
| meta_schemas | JDBC | 32 | 7.9 / 39.7 / 73.4 | 7.8 / 32.5 / 65.2 | n/a | n/a |
| meta_schemas | ADBC | 1 | 5.4 / 10.4 / 12.2 | 4.1 / 9.1 / 10.2 | n/a | n/a |
| meta_schemas | ADBC | 8 | 7.0 / 16.5 / 24.5 | 6.1 / 17.4 / 24.0 | n/a | n/a |
| meta_schemas | ADBC | 32 | 15.0 / 50.7 / 98.5 | 15.8 / 50.2 / 89.1 | n/a | n/a |

Answers per class are compared across servers in the run summary (`summary.md`, correctness gate).

### Scans (`SELECT * FROM tpch.lineitem`, SF10, MB/s of Arrow buffers) and server peak RSS

| metric | ours-new | ours-27f5 | up-native | up-main | ours-new vs best upstream |
|---|---|---|---|---|---|
| raw Flight, 1 stream | 398 | 411 | n/a | n/a | n/a |
| raw Flight, 4 streams | 467 | 495 | n/a | n/a | n/a |
| raw Flight, 8 streams | 415 | 452 | n/a | n/a | n/a |
| full export over ADBC | 400 | 484 | n/a | n/a | n/a |
| server peak RSS (MB) | 2577 | 3152 | n/a | n/a | - |

### Server container (docker stats every ~5 s, all workloads of this setting)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| CPU % p50 (200 = both cores) | 38 | 29 | n/a | n/a |
| CPU % max | 211 | 206 | n/a | n/a |
| memory peak (MiB, limit 6144) | 3166 | 2962 | n/a | n/a |
| OOM-killed rounds | 0 / 12 | 0 / 6 | 0 / 3 | 0 / 3 |

