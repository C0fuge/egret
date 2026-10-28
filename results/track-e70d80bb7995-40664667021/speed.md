# Server comparison - Report 1: SPEED (compare run 40664667021)

## Experiment setup

| item | value |
|---|---|
| runner | GitHub-hosted `ubuntu-latest`: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor; Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor; Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor; Linux ubuntu24 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C; Linux ubuntu24 4 vCPU Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz; RAM 15983 MB; kernel 7.0.0-1017-azure; JDK Temurin 21 |
| containers | every server: `eclipse-temurin:21-jre`, `--cpus=2 --cpuset-cpus=0,1 --memory=6g --memory-swap=6g`, JVM `-Xmx3g -XX:MaxDirectMemorySize=2g`, `MALLOC_ARENA_MAX=4`, host network; clients (JDBC/ADBC/Flight runners, jcmd sampling) and the S3 server in their own containers on cpus 2,3 |
| servers | ours-new = `7562a5bdb7b9` (DuckDB v1.5.6); ours-27f5 = `27f583adccd7` (DuckDB ?); up-native = `109b9199125cda3486911609c99ebec1da05cb98` (DuckDB error: INTERNAL: [FlightSQL] Failed to prepare Flight SQL statement (Internal; Prepare). Vendor code: 13); up-main = `dbacd8d585bce2ef2a449c821fe3a53cc6060b57` (DuckDB ?) |
| data | TPC-H SF1 and SF10, DuckDB dbgen, Parquet, 8 files per big table, 122880-row row groups, one data dir `tpch.*` per SF |
| storage | local disk (`file://`, page-cached) and S3 (`rclone serve s3` on the same runner, path style) |
| pairs | every job: ours-new (side A) vs one other server (side B) on the same runner, rounds A B / B A / A B (3), 1 cold run (warm-up) + warm runs per query (SF1 2 warm, SF10 1 warm per round) |
| settings | `def` = each server's default (`duckDbThreads` ours 4, upstream 2); `t8` = `-DduckDbThreads=8` on both |
| batch size | server defaults (not overridden) |
| clients | TPC-H: Python ADBC Flight SQL 1.12.0 (pyarrow 26), Flight SQL JDBC 18.0.0; small queries: same; scans: raw Flight (Arrow Java), ADBC export |
| correctness | TPC-H over ADBC: rows + checksum per query equal to in-process DuckDB on the same files; over JDBC: the result rows compared numerically with the same reference (numbers within a relative 1.5e-9, i.e. two 10-digit roundings; the JDBC runner prints DECIMAL as an exact plain BigDecimal, the reference as %.10g) |
| upstream on S3 | up-native: `s3a://` data dir (Hadoop S3A from its `docker/hadoop-aws` recipe for listing, DuckDB httpfs for scans, `FLIGHT_S3_*` settings); up-main: **n/a**, main at the fork point has no S3 settings (no `FLIGHT_S3_*`, no S3A dependencies) |
| SF30 | not run: SF1+SF10 already fill most of the repo's 10 GB Actions cache, SF30 Parquet (~11 GB) does not fit; generating it per job costs ~20 min of each 4-vCPU runner |
| JVM `4bb6441569be` `def` | `--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED -Darrowflight.plugins.dir=/app/plugins -Darrowflight.duckdb.extensionDir=/ext/duckdb-home/extensions -DduckDbAllowUnsignedExtensions=true -Ds3Endpoint=http://127.0.0.1:9000 -Ds3UrlStyle=path -Ds3Region=us-east-1 -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf10 -cp --port --localhost --hosts` |
| JVM `4e77c6bda59a` `def` | `--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED -Darrowflight.plugins.dir=/app/plugins -Darrowflight.duckdb.extensionDir=/ext/duckdb-home/extensions -DduckDbAllowUnsignedExtensions=true -Ds3Endpoint=http://127.0.0.1:9000 -Ds3UrlStyle=path -Ds3Region=us-east-1 -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=s3://default/sf1 -DduckDbThreads=4 -Darrowflight.s3.cacheMegabytes=1024 -cp --port --localhost --hosts` |
| JVM `e70d80bb7995` `def` | `--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED -Darrowflight.plugins.dir=/app/plugins -Darrowflight.duckdb.extensionDir=/ext/duckdb-home/extensions -DduckDbAllowUnsignedExtensions=true -Ds3Endpoint=http://127.0.0.1:9000 -Ds3UrlStyle=path -Ds3Region=us-east-1 -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf10 -cp --port --localhost --hosts` |
| JVM `ours-new` `def` | `--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED -Darrowflight.plugins.dir=/app/plugins -Darrowflight.duckdb.extensionDir=/ext/duckdb-home/extensions -DduckDbAllowUnsignedExtensions=true -Ds3Endpoint=http://127.0.0.1:9000 -Ds3UrlStyle=path -Ds3Region=us-east-1 -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf10 -cp --port --localhost --hosts` |
| JVM `up-native` `def` | `--add-modules --add-exports --add-opens --add-opens --add-opens=java.base/java.nio=ALL-UNNAMED --add-opens --add-opens -Dio.netty.tryReflectionSetAccessible=true -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf10 -cp --port --localhost --hosts` |

Times are warm medians in ms (median over rounds of the per-round warm median). **n/a** = not run, failed or wrong
answer (reason in the notes). Last column: same-runner ratio best-upstream / ours-new (> 1 = ours-new faster).

## local, setting `def`

### TPC-H SF10, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 2368 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 392 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1488 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 982 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 1731 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 776 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 1678 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 2023 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 3804 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1872 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 392 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 998 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 2854 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 1169 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 1087 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 537 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 1653 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 3016 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 1589 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 1408 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 5114 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 598 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 37529 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF1, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 300 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 60 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 170 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 110 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 165 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 103 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 189 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 203 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 293 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 214 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 44 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 116 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 277 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 135 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 95 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 76 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 167 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 346 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 178 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 142 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 447 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 103 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 3933 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF10, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 2343 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 409 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1470 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 983 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 1736 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 784 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 1676 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 2018 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 3791 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1823 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 356 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 1003 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 2835 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 1174 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 1075 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 566 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 1664 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 3029 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 1608 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 1424 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 5140 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 583 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 37490 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### TPC-H SF1, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 309 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 74 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 164 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 139 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 177 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 98 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 183 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 210 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 303 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 221 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 52 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 118 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 286 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 134 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 97 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 96 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 171 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 360 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 182 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 142 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 444 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 70 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 4030 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### Small queries (ms, p50 / p95 / p99 over all rounds)

| class | client | c | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|---|---|
| point_orders | JDBC | 1 | 20.0 / 29.7 / 33.3 | n/a | n/a | n/a |
| point_orders | JDBC | 8 | 92.4 / 143.2 / 171.8 | n/a | n/a | n/a |
| point_orders | JDBC | 32 | 366.1 / 676.1 / 880.7 | n/a | n/a | n/a |
| point_orders | ADBC | 1 | 12.4 / 23.5 / 25.4 | n/a | n/a | n/a |
| point_orders | ADBC | 8 | 73.7 / 120.9 / 149.3 | n/a | n/a | n/a |
| point_orders | ADBC | 32 | 325.8 / 589.8 / 780.9 | n/a | n/a | n/a |
| point_lineitem | JDBC | 1 | 27.3 / 37.5 / 41.1 | n/a | n/a | n/a |
| point_lineitem | JDBC | 8 | 155.4 / 239.2 / 290.5 | n/a | n/a | n/a |
| point_lineitem | JDBC | 32 | 618.2 / 1090.2 / 1335.5 | n/a | n/a | n/a |
| point_lineitem | ADBC | 1 | 20.4 / 31.7 / 33.9 | n/a | n/a | n/a |
| point_lineitem | ADBC | 8 | 133.8 / 203.8 / 275.5 | n/a | n/a | n/a |
| point_lineitem | ADBC | 32 | 597.9 / 981.3 / 1094.9 | n/a | n/a | n/a |
| count_filter | JDBC | 1 | 38.8 / 49.0 / 52.3 | n/a | n/a | n/a |
| count_filter | JDBC | 8 | 182.3 / 234.4 / 264.6 | n/a | n/a | n/a |
| count_filter | JDBC | 32 | 690.6 / 1051.4 / 1263.4 | n/a | n/a | n/a |
| count_filter | ADBC | 1 | 33.4 / 42.5 / 47.3 | n/a | n/a | n/a |
| count_filter | ADBC | 8 | 172.6 / 238.0 / 262.7 | n/a | n/a | n/a |
| count_filter | ADBC | 32 | 698.7 / 1048.1 / 1266.8 | n/a | n/a | n/a |
| limit10_ob | JDBC | 1 | 37.5 / 47.6 / 59.8 | n/a | n/a | n/a |
| limit10_ob | JDBC | 8 | 222.6 / 300.7 / 352.3 | n/a | n/a | n/a |
| limit10_ob | JDBC | 32 | 876.5 / 1371.9 / 1624.9 | n/a | n/a | n/a |
| limit10_ob | ADBC | 1 | 31.2 / 50.0 / 52.6 | n/a | n/a | n/a |
| limit10_ob | ADBC | 8 | 219.0 / 318.7 / 385.8 | n/a | n/a | n/a |
| limit10_ob | ADBC | 32 | 882.1 / 1360.9 / 1668.3 | n/a | n/a | n/a |
| meta_tables | JDBC | 1 | 7.0 / 10.2 / 14.8 | n/a | n/a | n/a |
| meta_tables | JDBC | 8 | 11.2 / 29.1 / 33.5 | n/a | n/a | n/a |
| meta_tables | JDBC | 32 | 26.3 / 501.3 / 1852.9 | n/a | n/a | n/a |
| meta_tables | ADBC | 1 | 5.8 / 7.7 / 9.1 | n/a | n/a | n/a |
| meta_tables | ADBC | 8 | 27.4 / 293.1 / 627.4 | n/a | n/a | n/a |
| meta_tables | ADBC | 32 | 72.7 / 146.5 / 195.1 | n/a | n/a | n/a |
| meta_schemas | JDBC | 1 | 5.0 / 8.3 / 13.9 | n/a | n/a | n/a |
| meta_schemas | JDBC | 8 | 11.1 / 25.5 / 33.2 | n/a | n/a | n/a |
| meta_schemas | JDBC | 32 | 24.4 / 61.1 / 138.4 | n/a | n/a | n/a |
| meta_schemas | ADBC | 1 | 3.7 / 5.9 / 6.6 | n/a | n/a | n/a |
| meta_schemas | ADBC | 8 | 17.4 / 34.3 / 45.1 | n/a | n/a | n/a |
| meta_schemas | ADBC | 32 | 42.2 / 92.1 / 122.3 | n/a | n/a | n/a |

Answers per class are compared across servers in the run summary (`summary.md`, correctness gate).

### Scans (`SELECT * FROM tpch.lineitem`, SF10, MB/s of Arrow buffers) and server peak RSS

| metric | ours-new | ours-27f5 | up-native | up-main | ours-new vs best upstream |
|---|---|---|---|---|---|
| raw Flight, 1 stream | 548 | n/a | 666 | n/a | n/a |
| raw Flight, 4 streams | 556 | n/a | 867 | n/a | n/a |
| raw Flight, 8 streams | 494 | n/a | 878 | n/a | n/a |
| full export over ADBC | 632 | n/a | 820 | n/a | n/a |
| server peak RSS (MB) | 1711 | n/a | 3732 | n/a | - |

### Server container (docker stats every ~5 s, all workloads of this setting)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| CPU % p50 (200 = both cores) | 200 | n/a | 202 | n/a |
| CPU % max | 204 | n/a | 204 | n/a |
| memory peak (MiB, limit 6144) | 1604 | n/a | 3514 | n/a |
| OOM-killed rounds | 0 / 6 | n/a | 0 / 3 | n/a |

## s3, setting `def`

### TPC-H SF10, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 8486 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 3862 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 21752 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 14463 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 26139 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 19508 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 29689 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 34200 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 36057 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 20606 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 4736 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 24846 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 6866 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 22045 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 21472 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 1836 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 28250 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 22788 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 23099 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 27134 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 52748 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 3134 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 453716 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF1, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 821 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 389 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1400 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 906 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 1359 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 1198 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 1666 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 1943 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 2052 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1286 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 289 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 1545 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 354 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 1340 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 1042 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 120 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 1701 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 1443 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 1468 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 1396 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 2780 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 193 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 26691 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF10, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 9029 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 5688 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 23687 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 14425 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 26736 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 20442 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 30993 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 38544 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 35385 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 22351 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 4948 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 24695 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 7205 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 21935 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 21706 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 1719 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 28891 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 22555 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 23926 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 27044 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 53466 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 3238 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 468608 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### TPC-H SF1, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 743 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 412 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1404 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 852 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 1353 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 1147 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 1651 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 1865 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 1952 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1342 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 333 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 1474 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 403 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 1297 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 1091 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 134 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 1706 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 1443 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 1390 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 1485 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 2759 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 196 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 26432 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### Small queries (ms, p50 / p95 / p99 over all rounds)

| class | client | c | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|---|---|
| point_orders | JDBC | 1 | 25.1 / 34.8 / 46.6 | n/a | n/a | n/a |
| point_orders | JDBC | 8 | 331.0 / 539.7 / 622.4 | n/a | n/a | n/a |
| point_orders | JDBC | 32 | 1261.1 / 2029.9 / 2466.3 | n/a | n/a | n/a |
| point_orders | ADBC | 1 | 17.0 / 30.1 / 39.9 | n/a | n/a | n/a |
| point_orders | ADBC | 8 | 302.2 / 530.8 / 630.5 | n/a | n/a | n/a |
| point_orders | ADBC | 32 | 1351.9 / 2627.8 / 3360.1 | n/a | n/a | n/a |
| point_lineitem | JDBC | 1 | 20.4 / 39.3 / 47.3 | n/a | n/a | n/a |
| point_lineitem | JDBC | 8 | 186.6 / 315.1 / 441.3 | n/a | n/a | n/a |
| point_lineitem | JDBC | 32 | 624.5 / 1101.6 / 1330.0 | n/a | n/a | n/a |
| point_lineitem | ADBC | 1 | 14.2 / 32.2 / 39.9 | n/a | n/a | n/a |
| point_lineitem | ADBC | 8 | 177.2 / 492.5 / 5189.6 | n/a | n/a | n/a |
| point_lineitem | ADBC | 32 | 673.3 / 8939.7 / 19478.5 | n/a | n/a | n/a |
| count_filter | JDBC | 1 | 690.4 / 793.2 / 817.9 | n/a | n/a | n/a |
| count_filter | JDBC | 8 | 3650.7 / 4101.6 / 4385.3 | n/a | n/a | n/a |
| count_filter | JDBC | 32 | 12964.3 / 18451.0 / 25995.1 | n/a | n/a | n/a |
| count_filter | ADBC | 1 | 686.7 / 766.0 / 834.5 | n/a | n/a | n/a |
| count_filter | ADBC | 8 | 3706.6 / 4248.5 / 4440.8 | n/a | n/a | n/a |
| count_filter | ADBC | 32 | 13586.0 / 22682.6 / 24159.4 | n/a | n/a | n/a |
| limit10_ob | JDBC | 1 | 112.1 / 159.7 / 185.7 | n/a | n/a | n/a |
| limit10_ob | JDBC | 8 | 592.9 / 845.3 / 1032.6 | n/a | n/a | n/a |
| limit10_ob | JDBC | 32 | 2339.5 / 3490.1 / 4367.4 | n/a | n/a | n/a |
| limit10_ob | ADBC | 1 | 112.8 / 146.1 / 168.5 | n/a | n/a | n/a |
| limit10_ob | ADBC | 8 | 590.0 / 916.1 / 2914.7 | n/a | n/a | n/a |
| limit10_ob | ADBC | 32 | 2535.6 / 4809.4 / 26009.4 | n/a | n/a | n/a |
| meta_tables | JDBC | 1 | 5.9 / 10.1 / 12.5 | n/a | n/a | n/a |
| meta_tables | JDBC | 8 | 4.5 / 9.9 / 15.1 | n/a | n/a | n/a |
| meta_tables | JDBC | 32 | 5.3 / 20.0 / 34.3 | n/a | n/a | n/a |
| meta_tables | ADBC | 1 | 5.4 / 8.8 / 12.2 | n/a | n/a | n/a |
| meta_tables | ADBC | 8 | 6.5 / 15.5 / 20.8 | n/a | n/a | n/a |
| meta_tables | ADBC | 32 | 11.7 / 33.1 / 59.1 | n/a | n/a | n/a |
| meta_schemas | JDBC | 1 | 4.6 / 6.8 / 8.1 | n/a | n/a | n/a |
| meta_schemas | JDBC | 8 | 3.2 / 8.7 / 12.6 | n/a | n/a | n/a |
| meta_schemas | JDBC | 32 | 4.1 / 19.8 / 43.0 | n/a | n/a | n/a |
| meta_schemas | ADBC | 1 | 3.2 / 5.7 / 7.3 | n/a | n/a | n/a |
| meta_schemas | ADBC | 8 | 4.0 / 11.3 / 18.5 | n/a | n/a | n/a |
| meta_schemas | ADBC | 32 | 7.4 / 24.7 / 37.3 | n/a | n/a | n/a |

Answers per class are compared across servers in the run summary (`summary.md`, correctness gate).

### Scans (`SELECT * FROM tpch.lineitem`, SF10, MB/s of Arrow buffers) and server peak RSS

| metric | ours-new | ours-27f5 | up-native | up-main | ours-new vs best upstream |
|---|---|---|---|---|---|
| raw Flight, 1 stream | 560 | n/a | n/a | n/a | n/a |
| raw Flight, 4 streams | 706 | n/a | n/a | n/a | n/a |
| raw Flight, 8 streams | 686 | n/a | n/a | n/a | n/a |
| full export over ADBC | 611 | n/a | n/a | n/a | n/a |
| server peak RSS (MB) | 2890 | n/a | n/a | n/a | - |

### Server container (docker stats every ~5 s, all workloads of this setting)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| CPU % p50 (200 = both cores) | 26 | n/a | n/a | n/a |
| CPU % max | 205 | n/a | n/a | n/a |
| memory peak (MiB, limit 6144) | 2790 | n/a | n/a | n/a |
| OOM-killed rounds | 0 / 12 | n/a | n/a | n/a |

