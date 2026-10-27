# Server comparison - Report 1: SPEED (compare run 40481152975)

## Experiment setup

| item | value |
|---|---|
| runner | GitHub-hosted `ubuntu-latest`: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor; Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor; Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor; RAM 15989 MB; kernel 6.17.0-1022-azure; JDK Temurin 21 |
| containers | **no-container reference run**: server in `eclipse-temurin:21-jdk` with an 8 GB memory limit and no CPU limit, clients on the runner host; not the reported numbers |
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
| q01 | scan + aggregation | 1205 | 1073 | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 198 | 185 | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 700 | 616 | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 476 | 420 | n/a | n/a | n/a |
| q05 | 6-way join | 813 | 716 | n/a | n/a | n/a |
| q06 | selective scan | 346 | 312 | n/a | n/a | n/a |
| q07 | joins, group by | 767 | 696 | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 961 | 851 | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 1880 | 1648 | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 836 | 752 | n/a | n/a | n/a |
| q11 | HAVING subquery | 167 | 158 | n/a | n/a | n/a |
| q12 | join, CASE agg | 475 | 419 | n/a | n/a | n/a |
| q13 | outer join, LIKE | 1310 | 1155 | n/a | n/a | n/a |
| q14 | join, CASE | 549 | 496 | n/a | n/a | n/a |
| q15 | view / CTE, max | 496 | 438 | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 300 | 234 | n/a | n/a | n/a |
| q17 | correlated avg | 794 | 715 | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 1382 | 1257 | n/a | n/a | n/a |
| q19 | OR predicates | 764 | 679 | n/a | n/a | n/a |
| q20 | nested IN | 650 | 595 | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 2572 | 2415 | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 275 | 258 | n/a | n/a | n/a |
| **Score** | sum of the 0 queries every shown server answered | n/a | n/a | n/a | n/a | geomean n/a (0 q) |

- up-main: q01 failed; q02 failed; q03 failed; q04 failed; q05 failed; q06 failed; q07 failed; q08 failed; q09 failed; q10 failed; q11 failed; q12 failed; q13 failed; q14 failed; q15 failed; q16 failed; q17 failed; q18 failed; q19 failed; q20 failed; q21 failed; q22 failed
- up-native: not run: not in this setting's jobs

### TPC-H SF1, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 178 | 144 | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 34 | 36 | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 82 | 82 | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 58 | 59 | n/a | n/a | n/a |
| q05 | 6-way join | 88 | 81 | n/a | n/a | n/a |
| q06 | selective scan | 48 | 46 | n/a | n/a | n/a |
| q07 | joins, group by | 90 | 88 | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 104 | 97 | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 147 | 133 | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 117 | 108 | n/a | n/a | n/a |
| q11 | HAVING subquery | 27 | 30 | n/a | n/a | n/a |
| q12 | join, CASE agg | 59 | 56 | n/a | n/a | n/a |
| q13 | outer join, LIKE | 134 | 123 | n/a | n/a | n/a |
| q14 | join, CASE | 70 | 68 | n/a | n/a | n/a |
| q15 | view / CTE, max | 47 | 48 | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 43 | 41 | n/a | n/a | n/a |
| q17 | correlated avg | 82 | 79 | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 169 | 149 | n/a | n/a | n/a |
| q19 | OR predicates | 92 | 96 | n/a | n/a | n/a |
| q20 | nested IN | 76 | 77 | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 226 | 198 | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 48 | 47 | n/a | n/a | n/a |
| **Score** | sum of the 0 queries every shown server answered | n/a | n/a | n/a | n/a | geomean n/a (0 q) |

- up-main: q01 failed; q02 failed; q03 failed; q04 failed; q05 failed; q06 failed; q07 failed; q08 failed; q09 failed; q10 failed; q11 failed; q12 failed; q13 failed; q14 failed; q15 failed; q16 failed; q17 failed; q18 failed; q19 failed; q20 failed; q21 failed; q22 failed
- up-native: not run: not in this setting's jobs

### TPC-H SF10, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | n/a | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 188 | 192 | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 603 | 601 | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 408 | 421 | n/a | n/a | n/a |
| q05 | 6-way join | n/a | n/a | n/a | n/a | n/a |
| q06 | selective scan | n/a | n/a | n/a | n/a | n/a |
| q07 | joins, group by | n/a | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 839 | 858 | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | n/a | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 745 | 751 | n/a | n/a | n/a |
| q11 | HAVING subquery | 155 | 158 | n/a | n/a | n/a |
| q12 | join, CASE agg | 419 | 419 | n/a | n/a | n/a |
| q13 | outer join, LIKE | 1158 | 1155 | n/a | n/a | n/a |
| q14 | join, CASE | 493 | 513 | n/a | n/a | n/a |
| q15 | view / CTE, max | n/a | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 263 | 260 | n/a | n/a | n/a |
| q17 | correlated avg | 715 | 724 | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 1257 | 1222 | n/a | n/a | n/a |
| q19 | OR predicates | n/a | n/a | n/a | n/a | n/a |
| q20 | nested IN | 585 | 593 | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 2443 | 2335 | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 256 | 261 | n/a | n/a | n/a |
| **Score** | sum of the 15 queries every shown server answered | 10527 | 10463 | n/a | n/a | geomean n/a (0 q) |

- ours-new: q01 wrong answer; q05 wrong answer; q06 wrong answer; q07 wrong answer; q09 wrong answer; q15 wrong answer; q19 wrong answer
- ours-27f5: q01 wrong answer; q05 wrong answer; q06 wrong answer; q07 wrong answer; q09 wrong answer; q15 wrong answer; q19 wrong answer
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### TPC-H SF1, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | n/a | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 38 | 46 | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 75 | 85 | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 55 | 60 | n/a | n/a | n/a |
| q05 | 6-way join | n/a | n/a | n/a | n/a | n/a |
| q06 | selective scan | n/a | n/a | n/a | n/a | n/a |
| q07 | joins, group by | n/a | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 96 | 102 | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | n/a | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 117 | 121 | n/a | n/a | n/a |
| q11 | HAVING subquery | 39 | 46 | n/a | n/a | n/a |
| q12 | join, CASE agg | 54 | 62 | n/a | n/a | n/a |
| q13 | outer join, LIKE | 117 | 122 | n/a | n/a | n/a |
| q14 | join, CASE | 62 | 70 | n/a | n/a | n/a |
| q15 | view / CTE, max | n/a | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 62 | 56 | n/a | n/a | n/a |
| q17 | correlated avg | 73 | 81 | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 148 | 151 | n/a | n/a | n/a |
| q19 | OR predicates | n/a | n/a | n/a | n/a | n/a |
| q20 | nested IN | 67 | 73 | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 196 | 202 | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 43 | 49 | n/a | n/a | n/a |
| **Score** | sum of the 15 queries every shown server answered | 1242 | 1326 | n/a | n/a | geomean n/a (0 q) |

- ours-new: q01 wrong answer; q05 wrong answer; q06 wrong answer; q07 wrong answer; q09 wrong answer; q15 wrong answer; q19 wrong answer
- ours-27f5: q01 wrong answer; q05 wrong answer; q06 wrong answer; q07 wrong answer; q09 wrong answer; q15 wrong answer; q19 wrong answer
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### Small queries (ms, p50 / p95 / p99 over all rounds)

| class | client | c | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|---|---|
| point_orders | JDBC | 1 | 20.9 / 29.1 / 38.4 | 22.4 / 33.2 / 37.1 | n/a | n/a (60 errors: t0 r-1: java.sql.SQLException: Error while executing SQL "SELECT o_orderkey, o_) |
| point_orders | JDBC | 8 | 87.2 / 159.6 / 263.3 | 96.8 / 155.3 / 213.2 | n/a | n/a (240 errors: t2 r-1: java.sql.SQLException: Error while executing SQL "SELECT o_orderkey, o_) |
| point_orders | JDBC | 32 | 312.7 / 644.8 / 1210.1 | 334.1 / 579.2 / 691.1 | n/a | n/a (480 errors: t14 r-1: java.sql.SQLException: Error while executing SQL "SELECT o_orderkey, o) |
| point_orders | ADBC | 1 | 12.6 / 17.6 / 20.9 | 16.1 / 21.0 / 21.7 | n/a | n/a |
| point_orders | ADBC | 8 | 66.8 / 105.7 / 131.7 | 81.0 / 118.4 / 133.8 | n/a | n/a (240 errors: t3 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| point_orders | ADBC | 32 | 270.2 / 446.8 / 622.2 | 337.1 / 747.3 / 817.1 | n/a | n/a (480 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| point_lineitem | JDBC | 1 | 26.3 / 33.1 / 37.4 | 28.0 / 38.3 / 45.5 | n/a | n/a (60 errors: t0 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l_) |
| point_lineitem | JDBC | 8 | 136.8 / 240.5 / 431.8 | 143.6 / 211.7 / 301.4 | n/a | n/a (240 errors: t3 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l_) |
| point_lineitem | JDBC | 32 | 505.6 / 832.1 / 1154.1 | 526.1 / 763.3 / 902.3 | n/a | n/a (480 errors: t27 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l) |
| point_lineitem | ADBC | 1 | 17.3 / 21.7 / 24.0 | 20.4 / 25.5 / 28.9 | n/a | n/a |
| point_lineitem | ADBC | 8 | 111.2 / 164.0 / 189.9 | 121.8 / 174.7 / 195.6 | n/a | n/a (240 errors: t4 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| point_lineitem | ADBC | 32 | 467.3 / 700.1 / 840.7 | 480.6 / 701.4 / 889.5 | n/a | n/a (480 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| count_filter | JDBC | 1 | 31.7 / 38.9 / 47.7 | 33.9 / 45.6 / 62.8 | n/a | n/a (60 errors: t0 r-1: java.sql.SQLException: Error while executing SQL "SELECT count(*) FROM) |
| count_filter | JDBC | 8 | 154.6 / 225.8 / 281.0 | 167.9 / 225.4 / 273.0 | n/a | n/a (240 errors: t4 r-1: java.sql.SQLException: Error while executing SQL "SELECT count(*) FROM) |
| count_filter | JDBC | 32 | 555.2 / 878.8 / 1114.1 | 590.7 / 841.3 / 1066.5 | n/a | n/a (480 errors: t28 r-1: java.sql.SQLException: Error while executing SQL "SELECT count(*) FROM) |
| count_filter | ADBC | 1 | 24.5 / 30.0 / 31.5 | 27.1 / 34.5 / 36.1 | n/a | n/a |
| count_filter | ADBC | 8 | 140.9 / 185.3 / 202.0 | 151.9 / 197.8 / 224.8 | n/a | n/a (240 errors: t5 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| count_filter | ADBC | 32 | 546.8 / 810.8 / 978.0 | 586.4 / 874.2 / 998.1 | n/a | n/a (480 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| limit10_ob | JDBC | 1 | 32.2 / 41.4 / 56.1 | 35.6 / 47.5 / 55.9 | n/a | n/a (60 errors: t0 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l_) |
| limit10_ob | JDBC | 8 | 179.4 / 275.2 / 326.3 | 200.0 / 261.9 / 296.6 | n/a | n/a (240 errors: t5 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l_) |
| limit10_ob | JDBC | 32 | 703.2 / 1063.6 / 1271.3 | 717.4 / 1036.8 / 1271.5 | n/a | n/a (480 errors: t11 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l) |
| limit10_ob | ADBC | 1 | 25.7 / 33.5 / 37.8 | 28.5 / 38.1 / 40.3 | n/a | n/a |
| limit10_ob | ADBC | 8 | 163.3 / 215.8 / 230.8 | 168.6 / 228.4 / 250.2 | n/a | n/a (240 errors: t2 r-1: OperationalError: IO: [FlightSQL] error reading from server: EOF (Unava) |
| limit10_ob | ADBC | 32 | 680.0 / 992.4 / 1204.7 | 706.6 / 1051.8 / 1168.4 | n/a | n/a (480 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| meta_tables | JDBC | 1 | 6.9 / 11.2 / 12.5 | 6.5 / 10.9 / 11.7 | n/a | 13.5 / 18.3 / 19.0 |
| meta_tables | JDBC | 8 | 9.2 / 25.4 / 45.8 | 8.4 / 26.6 / 35.2 | n/a | 34.1 / 65.5 / 100.5 |
| meta_tables | JDBC | 32 | 13.5 / 45.8 / 110.7 | 13.2 / 45.0 / 87.1 | n/a | n/a (480 errors: t11 r-1: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRunt) |
| meta_tables | ADBC | 1 | 7.6 / 11.0 / 14.5 | 6.7 / 8.7 / 10.0 | n/a | n/a |
| meta_tables | ADBC | 8 | 21.3 / 41.8 / 321.7 | 19.6 / 310.1 / 569.9 | n/a | n/a (240 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| meta_tables | ADBC | 32 | 57.0 / 689.5 / 1599.5 | 58.3 / 1158.1 / 1769.3 | n/a | n/a (480 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| meta_schemas | JDBC | 1 | 5.7 / 9.1 / 10.9 | 4.8 / 7.8 / 8.8 | n/a | 11.2 / 16.9 / 19.7 |
| meta_schemas | JDBC | 8 | 8.6 / 25.4 / 47.1 | 8.0 / 21.7 / 28.4 | n/a | 30.8 / 67.2 / 110.0 |
| meta_schemas | JDBC | 32 | 13.3 / 53.5 / 156.2 | 11.0 / 48.5 / 81.0 | n/a | n/a (480 errors: t31 r-1: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRunt) |
| meta_schemas | ADBC | 1 | 4.8 / 7.5 / 10.1 | 4.5 / 6.7 / 8.2 | n/a | n/a |
| meta_schemas | ADBC | 8 | 14.3 / 31.3 / 42.0 | 13.8 / 26.3 / 33.0 | n/a | n/a (240 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| meta_schemas | ADBC | 32 | 36.9 / 88.9 / 131.2 | 35.6 / 92.4 / 130.6 | n/a | n/a (480 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |

Answers per class are compared across servers in the run summary (`summary.md`, correctness gate).

### Scans (`SELECT * FROM tpch.lineitem`, SF10, MB/s of Arrow buffers) and server peak RSS

| metric | ours-new | ours-27f5 | up-native | up-main | ours-new vs best upstream |
|---|---|---|---|---|---|
| raw Flight, 1 stream | 490 | 501 | n/a | n/a | n/a |
| raw Flight, 4 streams | 774 | 789 | n/a | n/a | n/a |
| raw Flight, 8 streams | 779 | 778 | n/a | n/a | n/a |
| full export over ADBC | 531 | 535 | n/a | n/a | n/a |
| server peak RSS (MB) | 2448 | 2238 | n/a | 394 | - |

### Server container (docker stats every ~5 s, all workloads of this setting)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| CPU % p50 (200 = both cores) | n/a | n/a | n/a | n/a |
| CPU % max | n/a | n/a | n/a | n/a |
| memory peak (MiB, limit 6144) | n/a | n/a | n/a | n/a |
| OOM-killed rounds | 0 / 9 | 0 / 6 | n/a | 0 / 3 |

## local, setting `t8`

### TPC-H SF10, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 1134 | 1386 | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 193 | 230 | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 707 | 768 | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 446 | 523 | n/a | n/a | n/a |
| q05 | 6-way join | 766 | 904 | n/a | n/a | n/a |
| q06 | selective scan | 330 | 386 | n/a | n/a | n/a |
| q07 | joins, group by | 735 | 868 | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 935 | 1064 | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 1815 | 2027 | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 810 | 964 | n/a | n/a | n/a |
| q11 | HAVING subquery | 166 | 204 | n/a | n/a | n/a |
| q12 | join, CASE agg | 468 | 546 | n/a | n/a | n/a |
| q13 | outer join, LIKE | 1312 | 1515 | n/a | n/a | n/a |
| q14 | join, CASE | 556 | 617 | n/a | n/a | n/a |
| q15 | view / CTE, max | 484 | 572 | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 278 | 315 | n/a | n/a | n/a |
| q17 | correlated avg | 744 | 890 | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 1407 | 1638 | n/a | n/a | n/a |
| q19 | OR predicates | 736 | 860 | n/a | n/a | n/a |
| q20 | nested IN | 635 | 742 | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 2600 | 2759 | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 270 | 316 | n/a | n/a | n/a |
| **Score** | sum of the 0 queries every shown server answered | n/a | n/a | n/a | n/a | geomean n/a (0 q) |

- up-main: q01 failed; q02 failed; q03 failed; q04 failed; q05 failed; q06 failed; q07 failed; q08 failed; q09 failed; q10 failed; q11 failed; q12 failed; q13 failed; q14 failed; q15 failed; q16 failed; q17 failed; q18 failed; q19 failed; q20 failed; q21 failed; q22 failed
- up-native: not run: not in this setting's jobs

### TPC-H SF1, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 173 | 197 | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 40 | 47 | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 82 | 101 | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 63 | 71 | n/a | n/a | n/a |
| q05 | 6-way join | 84 | 105 | n/a | n/a | n/a |
| q06 | selective scan | 46 | 57 | n/a | n/a | n/a |
| q07 | joins, group by | 92 | 110 | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 106 | 130 | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 150 | 173 | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 114 | 135 | n/a | n/a | n/a |
| q11 | HAVING subquery | 30 | 37 | n/a | n/a | n/a |
| q12 | join, CASE agg | 64 | 73 | n/a | n/a | n/a |
| q13 | outer join, LIKE | 142 | 163 | n/a | n/a | n/a |
| q14 | join, CASE | 70 | 83 | n/a | n/a | n/a |
| q15 | view / CTE, max | 50 | 61 | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 44 | 56 | n/a | n/a | n/a |
| q17 | correlated avg | 86 | 98 | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 174 | 216 | n/a | n/a | n/a |
| q19 | OR predicates | 90 | 126 | n/a | n/a | n/a |
| q20 | nested IN | 76 | 107 | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 230 | 286 | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 48 | 62 | n/a | n/a | n/a |
| **Score** | sum of the 0 queries every shown server answered | n/a | n/a | n/a | n/a | geomean n/a (0 q) |

- up-main: q01 failed; q02 failed; q03 failed; q04 failed; q05 failed; q06 failed; q07 failed; q08 failed; q09 failed; q10 failed; q11 failed; q12 failed; q13 failed; q14 failed; q15 failed; q16 failed; q17 failed; q18 failed; q19 failed; q20 failed; q21 failed; q22 failed
- up-native: not run: not in this setting's jobs

### TPC-H SF10, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | n/a | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 235 | 238 | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 756 | 769 | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 526 | 528 | n/a | n/a | n/a |
| q05 | 6-way join | n/a | n/a | n/a | n/a | n/a |
| q06 | selective scan | n/a | n/a | n/a | n/a | n/a |
| q07 | joins, group by | n/a | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 1055 | 1065 | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | n/a | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 936 | 951 | n/a | n/a | n/a |
| q11 | HAVING subquery | 196 | 209 | n/a | n/a | n/a |
| q12 | join, CASE agg | 539 | 545 | n/a | n/a | n/a |
| q13 | outer join, LIKE | 1521 | 1505 | n/a | n/a | n/a |
| q14 | join, CASE | 614 | 618 | n/a | n/a | n/a |
| q15 | view / CTE, max | n/a | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 351 | 372 | n/a | n/a | n/a |
| q17 | correlated avg | 890 | 894 | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 1612 | 1628 | n/a | n/a | n/a |
| q19 | OR predicates | n/a | n/a | n/a | n/a | n/a |
| q20 | nested IN | 735 | 740 | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 2798 | 2758 | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 319 | 330 | n/a | n/a | n/a |
| **Score** | sum of the 15 queries every shown server answered | 13083 | 13150 | n/a | n/a | geomean n/a (0 q) |

- ours-new: q01 wrong answer; q05 wrong answer; q06 wrong answer; q07 wrong answer; q09 wrong answer; q15 wrong answer; q19 wrong answer
- ours-27f5: q01 wrong answer; q05 wrong answer; q06 wrong answer; q07 wrong answer; q09 wrong answer; q15 wrong answer; q19 wrong answer
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### TPC-H SF1, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | n/a | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 54 | 63 | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 98 | 102 | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 73 | 78 | n/a | n/a | n/a |
| q05 | 6-way join | n/a | n/a | n/a | n/a | n/a |
| q06 | selective scan | n/a | n/a | n/a | n/a | n/a |
| q07 | joins, group by | n/a | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 127 | 134 | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | n/a | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 132 | 146 | n/a | n/a | n/a |
| q11 | HAVING subquery | 51 | 64 | n/a | n/a | n/a |
| q12 | join, CASE agg | 71 | 80 | n/a | n/a | n/a |
| q13 | outer join, LIKE | 159 | 169 | n/a | n/a | n/a |
| q14 | join, CASE | 79 | 83 | n/a | n/a | n/a |
| q15 | view / CTE, max | n/a | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 75 | 78 | n/a | n/a | n/a |
| q17 | correlated avg | 102 | 103 | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 208 | 216 | n/a | n/a | n/a |
| q19 | OR predicates | n/a | n/a | n/a | n/a | n/a |
| q20 | nested IN | 87 | 97 | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 248 | 262 | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 55 | 63 | n/a | n/a | n/a |
| **Score** | sum of the 15 queries every shown server answered | 1619 | 1738 | n/a | n/a | geomean n/a (0 q) |

- ours-new: q01 wrong answer; q05 wrong answer; q06 wrong answer; q07 wrong answer; q09 wrong answer; q15 wrong answer; q19 wrong answer
- ours-27f5: q01 wrong answer; q05 wrong answer; q06 wrong answer; q07 wrong answer; q09 wrong answer; q15 wrong answer; q19 wrong answer
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### Small queries (ms, p50 / p95 / p99 over all rounds)

| class | client | c | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|---|---|
| point_orders | JDBC | 1 | 18.9 / 29.3 / 30.8 | 19.7 / 27.9 / 30.7 | n/a | n/a (60 errors: t0 r-1: java.sql.SQLException: Error while executing SQL "SELECT o_orderkey, o_) |
| point_orders | JDBC | 8 | 77.4 / 144.5 / 236.1 | 85.2 / 136.3 / 198.7 | n/a | n/a (240 errors: t2 r-1: java.sql.SQLException: Error while executing SQL "SELECT o_orderkey, o_) |
| point_orders | JDBC | 32 | 265.6 / 518.4 / 913.5 | 290.0 / 517.2 / 763.7 | n/a | n/a (480 errors: t2 r-1: java.sql.SQLException: Error while executing SQL "SELECT o_orderkey, o_) |
| point_orders | ADBC | 1 | 10.5 / 14.3 / 21.6 | 13.0 / 17.9 / 18.7 | n/a | n/a |
| point_orders | ADBC | 8 | 58.7 / 95.7 / 122.7 | 69.9 / 111.3 / 127.8 | n/a | n/a (240 errors: t4 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| point_orders | ADBC | 32 | 255.6 / 414.7 / 475.8 | 306.7 / 498.9 / 605.3 | n/a | n/a (480 errors: t1 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| point_lineitem | JDBC | 1 | 22.8 / 34.1 / 43.4 | 23.5 / 31.0 / 38.2 | n/a | n/a (60 errors: t0 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l_) |
| point_lineitem | JDBC | 8 | 113.3 / 178.0 / 228.1 | 116.4 / 177.2 / 204.5 | n/a | n/a (240 errors: t3 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l_) |
| point_lineitem | JDBC | 32 | 421.9 / 732.3 / 1092.3 | 447.1 / 731.8 / 944.0 | n/a | n/a (480 errors: t9 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l_) |
| point_lineitem | ADBC | 1 | 14.7 / 21.2 / 24.9 | 16.8 / 21.1 / 23.8 | n/a | n/a |
| point_lineitem | ADBC | 8 | 86.6 / 132.3 / 154.3 | 102.0 / 139.0 / 159.6 | n/a | n/a (240 errors: t4 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| point_lineitem | ADBC | 32 | 399.8 / 610.6 / 706.9 | 433.4 / 643.6 / 729.1 | n/a | n/a (480 errors: t1 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| count_filter | JDBC | 1 | 26.6 / 36.9 / 40.6 | 27.9 / 33.5 / 40.1 | n/a | n/a (60 errors: t0 r-1: java.sql.SQLException: Error while executing SQL "SELECT count(*) FROM) |
| count_filter | JDBC | 8 | 110.5 / 172.0 / 219.4 | 123.6 / 180.5 / 238.7 | n/a | n/a (240 errors: t4 r-1: java.sql.SQLException: Error while executing SQL "SELECT count(*) FROM) |
| count_filter | JDBC | 32 | 386.2 / 659.0 / 918.8 | 420.6 / 670.6 / 901.0 | n/a | n/a (480 errors: t28 r-1: java.sql.SQLException: Error while executing SQL "SELECT count(*) FROM) |
| count_filter | ADBC | 1 | 19.9 / 25.2 / 29.1 | 22.1 / 27.8 / 30.1 | n/a | n/a |
| count_filter | ADBC | 8 | 91.7 / 137.5 / 155.1 | 108.1 / 143.5 / 160.6 | n/a | n/a (240 errors: t5 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| count_filter | ADBC | 32 | 388.6 / 561.5 / 650.1 | 435.3 / 642.1 / 788.2 | n/a | n/a (480 errors: t1 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| limit10_ob | JDBC | 1 | 28.2 / 38.2 / 48.3 | 32.8 / 38.5 / 47.4 | n/a | n/a (60 errors: t0 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l_) |
| limit10_ob | JDBC | 8 | 148.5 / 229.9 / 296.5 | 162.8 / 232.6 / 312.6 | n/a | n/a (240 errors: t5 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l_) |
| limit10_ob | JDBC | 32 | 579.8 / 904.8 / 1101.0 | 619.4 / 930.5 / 1236.6 | n/a | n/a (480 errors: t29 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l) |
| limit10_ob | ADBC | 1 | 22.7 / 27.2 / 31.8 | 25.1 / 33.3 / 34.3 | n/a | n/a |
| limit10_ob | ADBC | 8 | 134.5 / 183.0 / 212.9 | 142.2 / 190.2 / 220.1 | n/a | n/a (240 errors: t7 r-1: OperationalError: IO: [FlightSQL] error reading from server: EOF (Unava) |
| limit10_ob | ADBC | 32 | 596.8 / 840.6 / 957.4 | 635.1 / 879.7 / 1032.4 | n/a | n/a (480 errors: t1 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| meta_tables | JDBC | 1 | 6.2 / 10.9 / 15.1 | 5.5 / 10.0 / 17.6 | n/a | 10.9 / 15.0 / 17.9 |
| meta_tables | JDBC | 8 | 9.6 / 29.4 / 40.6 | 8.0 / 27.3 / 42.8 | n/a | 26.1 / 47.5 / 69.1 |
| meta_tables | JDBC | 32 | 15.9 / 685.4 / 1185.3 | 13.4 / 50.8 / 99.9 | n/a | n/a (480 errors: t0 r-1: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRunti) |
| meta_tables | ADBC | 1 | 6.6 / 9.8 / 12.2 | 5.3 / 6.8 / 7.5 | n/a | n/a |
| meta_tables | ADBC | 8 | 19.5 / 42.4 / 57.3 | 16.6 / 37.3 / 45.5 | n/a | n/a (240 errors: t7 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| meta_tables | ADBC | 32 | 50.5 / 117.1 / 161.9 | 45.3 / 109.4 / 155.8 | n/a | n/a (480 errors: t1 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| meta_schemas | JDBC | 1 | 5.0 / 9.7 / 12.0 | 4.0 / 7.3 / 9.3 | n/a | 10.2 / 15.1 / 21.2 |
| meta_schemas | JDBC | 8 | 8.5 / 27.4 / 42.3 | 6.2 / 21.2 / 38.8 | n/a | 24.3 / 44.8 / 59.6 |
| meta_schemas | JDBC | 32 | 13.0 / 59.3 / 106.7 | 11.0 / 50.3 / 79.2 | n/a | n/a (480 errors: t29 r-1: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRunt) |
| meta_schemas | ADBC | 1 | 3.9 / 6.1 / 11.5 | 3.3 / 4.7 / 5.1 | n/a | n/a |
| meta_schemas | ADBC | 8 | 13.8 / 32.1 / 42.7 | 13.0 / 32.1 / 43.0 | n/a | n/a (240 errors: t5 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| meta_schemas | ADBC | 32 | 32.5 / 81.4 / 123.1 | 29.7 / 77.6 / 116.5 | n/a | n/a (480 errors: t1 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |

Answers per class are compared across servers in the run summary (`summary.md`, correctness gate).

### Scans (`SELECT * FROM tpch.lineitem`, SF10, MB/s of Arrow buffers) and server peak RSS

| metric | ours-new | ours-27f5 | up-native | up-main | ours-new vs best upstream |
|---|---|---|---|---|---|
| raw Flight, 1 stream | 631 | 584 | n/a | n/a | n/a |
| raw Flight, 4 streams | 981 | 952 | n/a | n/a | n/a |
| raw Flight, 8 streams | 962 | 899 | n/a | n/a | n/a |
| full export over ADBC | 684 | 635 | n/a | n/a | n/a |
| server peak RSS (MB) | 2646 | 2539 | n/a | 452 | - |

### Server container (docker stats every ~5 s, all workloads of this setting)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| CPU % p50 (200 = both cores) | n/a | n/a | n/a | n/a |
| CPU % max | n/a | n/a | n/a | n/a |
| memory peak (MiB, limit 6144) | n/a | n/a | n/a | n/a |
| OOM-killed rounds | 0 / 9 | 0 / 6 | n/a | 0 / 3 |

## s3, setting `def`

### TPC-H SF10, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 7903 | 12243 | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 3493 | 5240 | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 13608 | 26955 | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 8507 | 13294 | n/a | n/a | n/a |
| q05 | 6-way join | 21203 | 25598 | n/a | n/a | n/a |
| q06 | selective scan | 14245 | 17771 | n/a | n/a | n/a |
| q07 | joins, group by | 27741 | 27948 | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 33885 | 35958 | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 33597 | 39150 | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 19239 | 19553 | n/a | n/a | n/a |
| q11 | HAVING subquery | 4394 | 4450 | n/a | n/a | n/a |
| q12 | join, CASE agg | 21069 | 21021 | n/a | n/a | n/a |
| q13 | outer join, LIKE | 6453 | 6571 | n/a | n/a | n/a |
| q14 | join, CASE | 20106 | 20302 | n/a | n/a | n/a |
| q15 | view / CTE, max | 19796 | 20004 | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 1670 | 1781 | n/a | n/a | n/a |
| q17 | correlated avg | 27196 | 29475 | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 20342 | 21656 | n/a | n/a | n/a |
| q19 | OR predicates | 21087 | 21160 | n/a | n/a | n/a |
| q20 | nested IN | 25486 | 25675 | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 49653 | 49801 | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 2908 | 2849 | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 403581 | 448454 | n/a | n/a | geomean n/a (0 q) |

- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF1, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 734 | 980 | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 352 | 554 | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1361 | 2003 | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 811 | 1278 | n/a | n/a | n/a |
| q05 | 6-way join | 1307 | 2000 | n/a | n/a | n/a |
| q06 | selective scan | 1149 | 1753 | n/a | n/a | n/a |
| q07 | joins, group by | 2312 | 2300 | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 2738 | 2676 | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 2796 | 2851 | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1850 | 1892 | n/a | n/a | n/a |
| q11 | HAVING subquery | 437 | 450 | n/a | n/a | n/a |
| q12 | join, CASE agg | 2009 | 2104 | n/a | n/a | n/a |
| q13 | outer join, LIKE | 488 | 515 | n/a | n/a | n/a |
| q14 | join, CASE | 1944 | 1909 | n/a | n/a | n/a |
| q15 | view / CTE, max | 1554 | 1599 | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 180 | 202 | n/a | n/a | n/a |
| q17 | correlated avg | 2603 | 2594 | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 1864 | 1898 | n/a | n/a | n/a |
| q19 | OR predicates | 2010 | 2068 | n/a | n/a | n/a |
| q20 | nested IN | 2054 | 2121 | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 3649 | 3724 | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 253 | 300 | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 34455 | 37772 | n/a | n/a | geomean n/a (0 q) |

- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF10, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | n/a | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 5203 | 5192 | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 21200 | 20883 | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 12848 | 12996 | n/a | n/a | n/a |
| q05 | 6-way join | n/a | n/a | n/a | n/a | n/a |
| q06 | selective scan | n/a | n/a | n/a | n/a | n/a |
| q07 | joins, group by | n/a | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 39542 | 39492 | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | n/a | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 19041 | 19623 | n/a | n/a | n/a |
| q11 | HAVING subquery | 4410 | 4245 | n/a | n/a | n/a |
| q12 | join, CASE agg | 21049 | 21012 | n/a | n/a | n/a |
| q13 | outer join, LIKE | 6316 | 6505 | n/a | n/a | n/a |
| q14 | join, CASE | 20497 | 20042 | n/a | n/a | n/a |
| q15 | view / CTE, max | n/a | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 1575 | 1641 | n/a | n/a | n/a |
| q17 | correlated avg | 27432 | 27441 | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 20296 | 20302 | n/a | n/a | n/a |
| q19 | OR predicates | n/a | n/a | n/a | n/a | n/a |
| q20 | nested IN | 25160 | 25245 | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 49245 | 49650 | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 2845 | 2946 | n/a | n/a | n/a |
| **Score** | sum of the 15 queries every shown server answered | 276659 | 277215 | n/a | n/a | geomean n/a (0 q) |

- ours-new: q01 wrong answer; q05 wrong answer; q06 wrong answer; q07 wrong answer; q09 wrong answer; q15 wrong answer; q19 wrong answer
- ours-27f5: q01 wrong answer; q05 wrong answer; q06 wrong answer; q07 wrong answer; q09 wrong answer; q15 wrong answer; q19 wrong answer
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### TPC-H SF1, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | n/a | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 386 | 405 | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1337 | 1291 | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 758 | 866 | n/a | n/a | n/a |
| q05 | 6-way join | n/a | n/a | n/a | n/a | n/a |
| q06 | selective scan | n/a | n/a | n/a | n/a | n/a |
| q07 | joins, group by | n/a | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 2802 | 2954 | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | n/a | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1914 | 1972 | n/a | n/a | n/a |
| q11 | HAVING subquery | 404 | 449 | n/a | n/a | n/a |
| q12 | join, CASE agg | 2073 | 1960 | n/a | n/a | n/a |
| q13 | outer join, LIKE | 458 | 482 | n/a | n/a | n/a |
| q14 | join, CASE | 1887 | 1917 | n/a | n/a | n/a |
| q15 | view / CTE, max | n/a | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 154 | 179 | n/a | n/a | n/a |
| q17 | correlated avg | 2599 | 2622 | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 1891 | 1894 | n/a | n/a | n/a |
| q19 | OR predicates | n/a | n/a | n/a | n/a | n/a |
| q20 | nested IN | 2107 | 2120 | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 3658 | 3652 | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 252 | 316 | n/a | n/a | n/a |
| **Score** | sum of the 15 queries every shown server answered | 22680 | 23077 | n/a | n/a | geomean n/a (0 q) |

- ours-new: q01 wrong answer; q05 wrong answer; q06 wrong answer; q07 wrong answer; q09 wrong answer; q15 wrong answer; q19 wrong answer
- ours-27f5: q01 wrong answer; q05 wrong answer; q06 wrong answer; q07 wrong answer; q09 wrong answer; q15 wrong answer; q19 wrong answer
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### Small queries (ms, p50 / p95 / p99 over all rounds)

| class | client | c | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|---|---|
| point_orders | JDBC | 1 | 27.0 / 35.6 / 42.8 | 29.8 / 37.8 / 39.5 | n/a | n/a |
| point_orders | JDBC | 8 | 442.2 / 853.5 / 1168.9 | 410.7 / 654.4 / 802.7 | n/a | n/a |
| point_orders | JDBC | 32 | 1531.9 / 3132.3 / 4236.1 | 1494.4 / 2583.9 / 3271.2 | n/a | n/a |
| point_orders | ADBC | 1 | 20.4 / 40.6 / 45.4 | 23.0 / 38.2 / 65.5 | n/a | n/a |
| point_orders | ADBC | 8 | 433.5 / 843.8 / 1472.6 | 380.2 / 639.6 / 821.4 | n/a | n/a |
| point_orders | ADBC | 32 | 1535.6 / 3165.6 / 10877.2 | 1424.9 / 2600.1 / 3529.8 | n/a | n/a |
| point_lineitem | JDBC | 1 | 23.4 / 42.1 / 50.0 | 24.9 / 42.7 / 48.7 | n/a | n/a |
| point_lineitem | JDBC | 8 | 260.8 / 549.6 / 4444.6 | 252.1 / 356.0 / 433.8 | n/a | n/a |
| point_lineitem | JDBC | 32 | 899.1 / 13006.0 / 25346.7 | 805.2 / 6753.8 / 17784.5 | n/a | n/a |
| point_lineitem | ADBC | 1 | 15.3 / 43.3 / 668.5 | 19.1 / 37.1 / 44.0 | n/a | n/a |
| point_lineitem | ADBC | 8 | 255.5 / 500.2 / 693.7 | 215.6 / 4215.9 / 10314.6 | n/a | n/a |
| point_lineitem | ADBC | 32 | 855.2 / 9423.3 / 28863.4 | 789.0 / 13100.0 / 26670.0 | n/a | n/a |
| count_filter | JDBC | 1 | 641.4 / 1034.1 / 1138.2 | 682.3 / 750.1 / 795.7 | n/a | n/a |
| count_filter | JDBC | 8 | 5600.4 / 8539.0 / 11685.2 | 4841.2 / 5675.2 / 6023.6 | n/a | n/a |
| count_filter | JDBC | 32 | 18489.6 / 32186.5 / 54633.7 | 15783.5 / 28311.6 / 39973.0 | n/a | n/a |
| count_filter | ADBC | 1 | 682.8 / 1101.1 / 1442.7 | 682.3 / 780.4 / 867.0 | n/a | n/a |
| count_filter | ADBC | 8 | 5707.5 / 8731.8 / 9876.0 | 4875.9 / 5849.0 / 8157.0 | n/a | n/a |
| count_filter | ADBC | 32 | 17423.5 / 28697.7 / 45442.0 | 15835.9 / 24705.9 / 30792.5 | n/a | n/a |
| limit10_ob | JDBC | 1 | 141.7 / 201.3 / 210.1 | 103.5 / 139.2 / 231.1 | n/a | n/a |
| limit10_ob | JDBC | 8 | 883.3 / 1539.1 / 4671.5 | 787.6 / 1051.8 / 1267.3 | n/a | n/a |
| limit10_ob | JDBC | 32 | 2942.0 / 10513.8 / 33165.9 | 2685.4 / 3979.3 / 18256.5 | n/a | n/a |
| limit10_ob | ADBC | 1 | 148.1 / 210.4 / 245.6 | 104.2 / 148.2 / 153.1 | n/a | n/a |
| limit10_ob | ADBC | 8 | 863.1 / 1439.2 / 1744.0 | 748.3 / 1083.3 / 3819.6 | n/a | n/a |
| limit10_ob | ADBC | 32 | 2846.3 / 31666.0 / 48958.4 | 2557.7 / 3945.5 / 15970.3 | n/a | n/a |
| meta_tables | JDBC | 1 | 6.6 / 10.0 / 11.0 | 6.5 / 10.3 / 12.5 | n/a | n/a |
| meta_tables | JDBC | 8 | 4.0 / 12.4 / 24.9 | 3.8 / 10.2 / 21.1 | n/a | n/a |
| meta_tables | JDBC | 32 | 3.7 / 21.3 / 68.7 | 3.3 / 17.9 / 44.3 | n/a | n/a |
| meta_tables | ADBC | 1 | 7.3 / 10.6 / 13.9 | 6.3 / 9.9 / 14.3 | n/a | n/a |
| meta_tables | ADBC | 8 | 7.2 / 21.0 / 30.5 | 7.5 / 18.8 / 28.8 | n/a | n/a |
| meta_tables | ADBC | 32 | 11.6 / 40.6 / 123.9 | 11.1 / 45.4 / 96.3 | n/a | n/a |
| meta_schemas | JDBC | 1 | 5.3 / 8.4 / 12.6 | 4.6 / 8.9 / 11.9 | n/a | n/a |
| meta_schemas | JDBC | 8 | 3.0 / 14.0 / 26.7 | 2.5 / 9.4 / 15.8 | n/a | n/a |
| meta_schemas | JDBC | 32 | 3.2 / 37.7 / 83.5 | 2.5 / 20.9 / 38.2 | n/a | n/a |
| meta_schemas | ADBC | 1 | 4.5 / 6.5 / 10.0 | 4.0 / 5.7 / 8.2 | n/a | n/a |
| meta_schemas | ADBC | 8 | 5.0 / 18.4 / 26.8 | 5.1 / 15.5 / 20.9 | n/a | n/a |
| meta_schemas | ADBC | 32 | 8.6 / 37.2 / 90.5 | 7.6 / 31.6 / 82.8 | n/a | n/a |

Answers per class are compared across servers in the run summary (`summary.md`, correctness gate).

### Scans (`SELECT * FROM tpch.lineitem`, SF10, MB/s of Arrow buffers) and server peak RSS

| metric | ours-new | ours-27f5 | up-native | up-main | ours-new vs best upstream |
|---|---|---|---|---|---|
| raw Flight, 1 stream | 433 | 440 | n/a | n/a | n/a |
| raw Flight, 4 streams | 634 | 697 | n/a | n/a | n/a |
| raw Flight, 8 streams | 634 | 706 | n/a | n/a | n/a |
| full export over ADBC | 471 | 472 | n/a | n/a | n/a |
| server peak RSS (MB) | 2271 | 2924 | n/a | n/a | - |

### Server container (docker stats every ~5 s, all workloads of this setting)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| CPU % p50 (200 = both cores) | n/a | n/a | n/a | n/a |
| CPU % max | n/a | n/a | n/a | n/a |
| memory peak (MiB, limit 6144) | n/a | n/a | n/a | n/a |
| OOM-killed rounds | 0 / 12 | 0 / 6 | 0 / 3 | 0 / 3 |

## s3, setting `t8`

### TPC-H SF10, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 13043 | 13446 | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 5461 | 5567 | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 23256 | 23228 | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 14451 | 14073 | n/a | n/a | n/a |
| q05 | 6-way join | 27655 | 36475 | n/a | n/a | n/a |
| q06 | selective scan | 20606 | 19112 | n/a | n/a | n/a |
| q07 | joins, group by | 30603 | 31248 | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 36590 | 37776 | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 36210 | 37678 | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 21430 | 21472 | n/a | n/a | n/a |
| q11 | HAVING subquery | 4503 | 4469 | n/a | n/a | n/a |
| q12 | join, CASE agg | 22558 | 30421 | n/a | n/a | n/a |
| q13 | outer join, LIKE | 7051 | 7191 | n/a | n/a | n/a |
| q14 | join, CASE | 22603 | 22100 | n/a | n/a | n/a |
| q15 | view / CTE, max | 21543 | 21666 | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 1764 | 1964 | n/a | n/a | n/a |
| q17 | correlated avg | 30904 | 29902 | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 22649 | 22350 | n/a | n/a | n/a |
| q19 | OR predicates | 27005 | 23316 | n/a | n/a | n/a |
| q20 | nested IN | 27649 | 27948 | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 55139 | 54967 | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 3061 | 3164 | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 475734 | 489533 | n/a | n/a | geomean n/a (0 q) |

- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF1, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 847 | 1088 | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 409 | 574 | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1405 | 2104 | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 905 | 1303 | n/a | n/a | n/a |
| q05 | 6-way join | 1416 | 2026 | n/a | n/a | n/a |
| q06 | selective scan | 1156 | 1775 | n/a | n/a | n/a |
| q07 | joins, group by | 2011 | 2482 | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 2427 | 2970 | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 2587 | 3016 | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1667 | 1820 | n/a | n/a | n/a |
| q11 | HAVING subquery | 459 | 471 | n/a | n/a | n/a |
| q12 | join, CASE agg | 1836 | 2128 | n/a | n/a | n/a |
| q13 | outer join, LIKE | 433 | 456 | n/a | n/a | n/a |
| q14 | join, CASE | 1616 | 1999 | n/a | n/a | n/a |
| q15 | view / CTE, max | 1478 | 1550 | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 205 | 232 | n/a | n/a | n/a |
| q17 | correlated avg | 2337 | 2721 | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 1688 | 2018 | n/a | n/a | n/a |
| q19 | OR predicates | 1845 | 2230 | n/a | n/a | n/a |
| q20 | nested IN | 1913 | 2101 | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 3496 | 3909 | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 248 | 252 | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 32385 | 39226 | n/a | n/a | geomean n/a (0 q) |

- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF10, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | n/a | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 5686 | 4702 | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 27601 | 24960 | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 13955 | 12144 | n/a | n/a | n/a |
| q05 | 6-way join | n/a | n/a | n/a | n/a | n/a |
| q06 | selective scan | n/a | n/a | n/a | n/a | n/a |
| q07 | joins, group by | n/a | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 44488 | 35178 | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | n/a | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 20850 | 17604 | n/a | n/a | n/a |
| q11 | HAVING subquery | 4439 | 3665 | n/a | n/a | n/a |
| q12 | join, CASE agg | 22325 | 21102 | n/a | n/a | n/a |
| q13 | outer join, LIKE | 6941 | 6178 | n/a | n/a | n/a |
| q14 | join, CASE | 24351 | 18592 | n/a | n/a | n/a |
| q15 | view / CTE, max | n/a | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 1834 | 1732 | n/a | n/a | n/a |
| q17 | correlated avg | 30546 | 29734 | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 22196 | 22112 | n/a | n/a | n/a |
| q19 | OR predicates | n/a | n/a | n/a | n/a | n/a |
| q20 | nested IN | 27638 | 32196 | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 55241 | 54091 | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 3051 | 3204 | n/a | n/a | n/a |
| **Score** | sum of the 15 queries every shown server answered | 311142 | 287190 | n/a | n/a | geomean n/a (0 q) |

- ours-new: q01 wrong answer; q05 wrong answer; q06 wrong answer; q07 wrong answer; q09 wrong answer; q15 wrong answer; q19 wrong answer
- ours-27f5: q01 wrong answer; q05 wrong answer; q06 wrong answer; q07 wrong answer; q09 wrong answer; q15 wrong answer; q19 wrong answer
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### TPC-H SF1, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | n/a | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 399 | 422 | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1351 | 1275 | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 899 | 974 | n/a | n/a | n/a |
| q05 | 6-way join | n/a | n/a | n/a | n/a | n/a |
| q06 | selective scan | n/a | n/a | n/a | n/a | n/a |
| q07 | joins, group by | n/a | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 2901 | 2865 | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | n/a | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1880 | 1932 | n/a | n/a | n/a |
| q11 | HAVING subquery | 437 | 425 | n/a | n/a | n/a |
| q12 | join, CASE agg | 2197 | 2138 | n/a | n/a | n/a |
| q13 | outer join, LIKE | 449 | 575 | n/a | n/a | n/a |
| q14 | join, CASE | 1889 | 1979 | n/a | n/a | n/a |
| q15 | view / CTE, max | n/a | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 226 | 193 | n/a | n/a | n/a |
| q17 | correlated avg | 2600 | 2698 | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 1847 | 2068 | n/a | n/a | n/a |
| q19 | OR predicates | n/a | n/a | n/a | n/a | n/a |
| q20 | nested IN | 2191 | 2255 | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 4052 | 4064 | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 259 | 272 | n/a | n/a | n/a |
| **Score** | sum of the 15 queries every shown server answered | 23577 | 24136 | n/a | n/a | geomean n/a (0 q) |

- ours-new: q01 wrong answer; q05 wrong answer; q06 wrong answer; q07 wrong answer; q09 wrong answer; q15 wrong answer; q19 wrong answer
- ours-27f5: q01 wrong answer; q05 wrong answer; q06 wrong answer; q07 wrong answer; q09 wrong answer; q15 wrong answer; q19 wrong answer
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### Small queries (ms, p50 / p95 / p99 over all rounds)

| class | client | c | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|---|---|
| point_orders | JDBC | 1 | 27.7 / 41.2 / 114.3 | 32.7 / 38.6 / 42.0 | n/a | n/a |
| point_orders | JDBC | 8 | 674.2 / 1386.7 / 2038.9 | 786.3 / 1611.8 / 5786.7 | n/a | n/a |
| point_orders | JDBC | 32 | 2558.6 / 6050.2 / 20783.1 | 2736.8 / 5715.8 / 9261.6 | n/a | n/a |
| point_orders | ADBC | 1 | 22.4 / 56.2 / 178.4 | 25.2 / 39.9 / 47.1 | n/a | n/a |
| point_orders | ADBC | 8 | 628.3 / 1337.9 / 1765.4 | 637.3 / 1432.3 / 1723.5 | n/a | n/a |
| point_orders | ADBC | 32 | 2759.7 / 6203.8 / 11303.2 | 2588.4 / 5576.9 / 12350.1 | n/a | n/a |
| point_lineitem | JDBC | 1 | 23.0 / 44.3 / 66.9 | 27.8 / 45.1 / 50.2 | n/a | n/a |
| point_lineitem | JDBC | 8 | 391.2 / 812.1 / 1058.3 | 416.7 / 967.3 / 6371.1 | n/a | n/a |
| point_lineitem | JDBC | 32 | 1350.6 / 4492.0 / 31519.0 | 1352.4 / 2446.5 / 3049.2 | n/a | n/a |
| point_lineitem | ADBC | 1 | 16.3 / 45.4 / 78.3 | 20.5 / 44.8 / 499.1 | n/a | n/a |
| point_lineitem | ADBC | 8 | 393.0 / 988.2 / 8666.7 | 391.5 / 1200.8 / 6462.5 | n/a | n/a |
| point_lineitem | ADBC | 32 | 1351.9 / 3394.3 / 31207.0 | 1350.4 / 14801.2 / 24032.6 | n/a | n/a |
| count_filter | JDBC | 1 | 728.7 / 1187.8 / 1292.5 | 741.0 / 828.3 / 864.4 | n/a | n/a |
| count_filter | JDBC | 8 | 4789.1 / 7298.7 / 15315.0 | 3757.9 / 6334.9 / 11849.9 | n/a | n/a |
| count_filter | JDBC | 32 | 15782.9 / 45195.4 / 74989.1 | 12950.5 / 41844.0 / 50444.2 | n/a | n/a |
| count_filter | ADBC | 1 | 798.1 / 1235.0 / 1418.0 | 759.7 / 1145.2 / 1318.5 | n/a | n/a |
| count_filter | ADBC | 8 | 4481.9 / 7099.2 / 9562.0 | 4217.6 / 6933.1 / 10075.2 | n/a | n/a |
| count_filter | ADBC | 32 | 15393.3 / 37697.4 / 49458.1 | 13380.4 / 42108.0 / 47733.0 | n/a | n/a |
| limit10_ob | JDBC | 1 | 179.9 / 278.7 / 383.7 | 161.4 / 192.6 / 238.7 | n/a | n/a |
| limit10_ob | JDBC | 8 | 1428.2 / 2463.5 / 2795.9 | 1388.6 / 2613.6 / 11365.9 | n/a | n/a |
| limit10_ob | JDBC | 32 | 5466.8 / 34523.4 / 110086.8 | 5353.6 / 9293.0 / 11152.0 | n/a | n/a |
| limit10_ob | ADBC | 1 | 190.3 / 282.6 / 481.5 | 163.3 / 236.6 / 722.1 | n/a | n/a |
| limit10_ob | ADBC | 8 | 1429.0 / 3159.4 / 19318.4 | 1412.1 / 2554.9 / 8496.3 | n/a | n/a |
| limit10_ob | ADBC | 32 | 5374.5 / 10247.4 / 37842.3 | 5129.8 / 20357.3 / 35315.6 | n/a | n/a |
| meta_tables | JDBC | 1 | 6.3 / 9.9 / 11.6 | 7.3 / 10.9 / 13.5 | n/a | n/a |
| meta_tables | JDBC | 8 | 4.4 / 14.2 / 27.2 | 4.6 / 11.1 / 19.1 | n/a | n/a |
| meta_tables | JDBC | 32 | 4.5 / 28.1 / 93.0 | 4.9 / 23.7 / 71.0 | n/a | n/a |
| meta_tables | ADBC | 1 | 6.7 / 9.2 / 12.1 | 6.4 / 12.8 / 14.3 | n/a | n/a |
| meta_tables | ADBC | 8 | 8.1 / 18.9 / 32.8 | 9.1 / 18.8 / 30.0 | n/a | n/a |
| meta_tables | ADBC | 32 | 12.9 / 41.4 / 130.6 | 15.6 / 45.7 / 77.2 | n/a | n/a |
| meta_schemas | JDBC | 1 | 5.0 / 8.1 / 12.0 | 5.3 / 9.5 / 13.7 | n/a | n/a |
| meta_schemas | JDBC | 8 | 3.7 / 15.8 / 27.4 | 3.4 / 11.6 / 15.9 | n/a | n/a |
| meta_schemas | JDBC | 32 | 3.8 / 32.4 / 111.3 | 3.0 / 26.0 / 111.9 | n/a | n/a |
| meta_schemas | ADBC | 1 | 4.1 / 6.3 / 8.2 | 4.1 / 5.8 / 8.0 | n/a | n/a |
| meta_schemas | ADBC | 8 | 5.4 / 17.2 / 29.8 | 6.1 / 17.3 / 29.9 | n/a | n/a |
| meta_schemas | ADBC | 32 | 9.4 / 40.2 / 100.4 | 11.9 / 38.7 / 93.6 | n/a | n/a |

Answers per class are compared across servers in the run summary (`summary.md`, correctness gate).

### Scans (`SELECT * FROM tpch.lineitem`, SF10, MB/s of Arrow buffers) and server peak RSS

| metric | ours-new | ours-27f5 | up-native | up-main | ours-new vs best upstream |
|---|---|---|---|---|---|
| raw Flight, 1 stream | 417 | 424 | n/a | n/a | n/a |
| raw Flight, 4 streams | 608 | 660 | n/a | n/a | n/a |
| raw Flight, 8 streams | 606 | 594 | n/a | n/a | n/a |
| full export over ADBC | 462 | 431 | n/a | n/a | n/a |
| server peak RSS (MB) | 2666 | 3131 | n/a | n/a | - |

### Server container (docker stats every ~5 s, all workloads of this setting)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| CPU % p50 (200 = both cores) | n/a | n/a | n/a | n/a |
| CPU % max | n/a | n/a | n/a | n/a |
| memory peak (MiB, limit 6144) | n/a | n/a | n/a | n/a |
| OOM-killed rounds | 0 / 12 | 0 / 5 | 0 / 3 | 0 / 3 |

