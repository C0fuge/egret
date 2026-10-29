# Server comparison - Report 1: SPEED (compare run 40800578035)

## Experiment setup

| item | value |
|---|---|
| runner | GitHub-hosted `ubuntu-latest`: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor; Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor; Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor; Linux ubuntu24 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C; RAM 15983 MB; kernel 7.0.0-1017-azure; JDK Temurin 21 |
| containers | every server: `eclipse-temurin:21-jre`, `--cpus=2 --cpuset-cpus=0,1 --memory=6g --memory-swap=6g`, JVM `-Xmx3g -XX:MaxDirectMemorySize=2g`, `MALLOC_ARENA_MAX=4`, host network; clients (JDBC/ADBC/Flight runners, jcmd sampling) and the S3 server in their own containers on cpus 2,3 |
| servers | ours-new = `7562a5bdb7b9` (DuckDB v1.5.6); ours-27f5 = `27f583adccd7` (DuckDB ?); up-native = `1de5f6b4b218f83f01a3adf2708af5f36f80811b` (DuckDB error: INTERNAL: [FlightSQL] Failed to prepare Flight SQL statement (Internal; Prepare). Vendor code: 13); up-main = `dbacd8d585bce2ef2a449c821fe3a53cc6060b57` (DuckDB ?) |
| data | TPC-H SF1 and SF10, DuckDB dbgen, Parquet, 8 files per big table, 122880-row row groups, one data dir `tpch.*` per SF |
| storage | local disk (`file://`, page-cached) and S3 (`rclone serve s3` on the same runner, path style) |
| pairs | every job: ours-new (side A) vs one other server (side B) on the same runner, rounds A B / B A / A B (3), 1 cold run (warm-up) + warm runs per query (SF1 2 warm, SF10 1 warm per round) |
| settings | `def` = each server's default (`duckDbThreads` ours 4, upstream 2); `t8` = `-DduckDbThreads=8` on both |
| batch size | server defaults (not overridden) |
| clients | TPC-H: Python ADBC Flight SQL 1.12.0 (pyarrow 26), Flight SQL JDBC 18.0.0; small queries: same; scans: raw Flight (Arrow Java), ADBC export |
| correctness | TPC-H over ADBC: rows + checksum per query equal to in-process DuckDB on the same files; over JDBC: the result rows compared numerically with the same reference (numbers within a relative 1.5e-9, i.e. two 10-digit roundings; the JDBC runner prints DECIMAL as an exact plain BigDecimal, the reference as %.10g) |
| upstream on S3 | up-native: `s3a://` data dir (Hadoop S3A from its `docker/hadoop-aws` recipe for listing, DuckDB httpfs for scans, `FLIGHT_S3_*` settings); up-main: **n/a**, main at the fork point has no S3 settings (no `FLIGHT_S3_*`, no S3A dependencies) |
| SF30 | not run: SF1+SF10 already fill most of the repo's 10 GB Actions cache, SF30 Parquet (~11 GB) does not fit; generating it per job costs ~20 min of each 4-vCPU runner |
| JVM `881bbf73e946` `def` | `--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED -Darrowflight.plugins.dir=/app/plugins -Darrowflight.duckdb.extensionDir=/ext/duckdb-home/extensions -DduckDbAllowUnsignedExtensions=true -Ds3Endpoint=http://127.0.0.1:9000 -Ds3UrlStyle=path -Ds3Region=us-east-1 -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf10 -cp --port --localhost --hosts` |
| JVM `ours-new` `def` | `--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED -Darrowflight.plugins.dir=/app/plugins -Darrowflight.duckdb.extensionDir=/ext/duckdb-home/extensions -DduckDbAllowUnsignedExtensions=true -Ds3Endpoint=http://127.0.0.1:9000 -Ds3UrlStyle=path -Ds3Region=us-east-1 -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf10 -cp --port --localhost --hosts` |
| JVM `up-native` `def` | `--add-modules --add-exports --add-opens --add-opens --add-opens=java.base/java.nio=ALL-UNNAMED --add-opens --add-opens -Dio.netty.tryReflectionSetAccessible=true -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf10 -cp --port --localhost --hosts` |

Times are warm medians in ms (median over rounds of the per-round warm median). **n/a** = not run, failed or wrong
answer (reason in the notes). Last column: same-runner ratio best-upstream / ours-new (> 1 = ours-new faster).

## local, setting `def`

### TPC-H SF10, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 2674 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 400 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1567 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 1008 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 1702 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 748 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 1687 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 2021 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 4322 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1881 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 384 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 1049 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 2901 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 1190 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 1069 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 569 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 1722 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 3173 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 1675 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 1400 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 5528 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 585 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 39255 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF1, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 342 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 65 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 172 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 112 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 167 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 96 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 181 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 204 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 307 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 223 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 44 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 118 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 295 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 132 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 96 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 78 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 168 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 354 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 177 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 179 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 460 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 71 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 4041 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF10, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 2657 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 406 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1552 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 1011 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 1741 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 749 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 1673 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 2067 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 4239 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1847 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 365 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 1025 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 2860 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 1208 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 1084 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 570 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 1733 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 3790 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 1668 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 1397 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 5539 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 587 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 39768 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### TPC-H SF1, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 357 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 72 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 186 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 126 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 169 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 106 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 177 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 209 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 297 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 225 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 56 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 122 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 286 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 133 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 97 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 95 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 164 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 363 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 182 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 145 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 458 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 71 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 4096 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### Small queries (ms, p50 / p95 / p99 over all rounds)

| class | client | c | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|---|---|
| point_orders | JDBC | 1 | 20.6 / 29.8 / 33.8 | n/a | n/a | n/a |
| point_orders | JDBC | 8 | 92.5 / 147.5 / 210.3 | n/a | n/a | n/a |
| point_orders | JDBC | 32 | 371.5 / 717.6 / 1089.6 | n/a | n/a | n/a |
| point_orders | ADBC | 1 | 12.6 / 18.1 / 19.2 | n/a | n/a | n/a |
| point_orders | ADBC | 8 | 75.4 / 121.2 / 146.0 | n/a | n/a | n/a |
| point_orders | ADBC | 32 | 338.9 / 617.3 / 742.4 | n/a | n/a | n/a |
| point_lineitem | JDBC | 1 | 27.6 / 40.5 / 45.8 | n/a | n/a | n/a |
| point_lineitem | JDBC | 8 | 144.9 / 226.0 / 301.6 | n/a | n/a | n/a |
| point_lineitem | JDBC | 32 | 628.9 / 1108.3 / 1461.4 | n/a | n/a | n/a |
| point_lineitem | ADBC | 1 | 20.4 / 29.3 / 34.9 | n/a | n/a | n/a |
| point_lineitem | ADBC | 8 | 132.9 / 200.4 / 232.0 | n/a | n/a | n/a |
| point_lineitem | ADBC | 32 | 618.9 / 1018.4 / 1172.9 | n/a | n/a | n/a |
| count_filter | JDBC | 1 | 39.1 / 48.2 / 64.2 | n/a | n/a | n/a |
| count_filter | JDBC | 8 | 177.0 / 233.8 / 268.9 | n/a | n/a | n/a |
| count_filter | JDBC | 32 | 707.2 / 1102.1 / 1258.4 | n/a | n/a | n/a |
| count_filter | ADBC | 1 | 33.0 / 43.8 / 46.3 | n/a | n/a | n/a |
| count_filter | ADBC | 8 | 177.3 / 239.0 / 263.7 | n/a | n/a | n/a |
| count_filter | ADBC | 32 | 687.8 / 1024.4 / 1234.0 | n/a | n/a | n/a |
| limit10_ob | JDBC | 1 | 37.3 / 47.1 / 49.6 | n/a | n/a | n/a |
| limit10_ob | JDBC | 8 | 217.6 / 318.5 / 355.1 | n/a | n/a | n/a |
| limit10_ob | JDBC | 32 | 936.5 / 1407.3 / 1641.5 | n/a | n/a | n/a |
| limit10_ob | ADBC | 1 | 30.4 / 44.5 / 49.9 | n/a | n/a | n/a |
| limit10_ob | ADBC | 8 | 215.9 / 313.0 / 360.7 | n/a | n/a | n/a |
| limit10_ob | ADBC | 32 | 914.7 / 1397.8 / 1620.7 | n/a | n/a | n/a |
| meta_tables | JDBC | 1 | 7.3 / 11.7 / 24.6 | n/a | n/a | n/a |
| meta_tables | JDBC | 8 | 11.7 / 28.6 / 42.8 | n/a | n/a | n/a |
| meta_tables | JDBC | 32 | 29.3 / 80.0 / 1044.8 | n/a | n/a | n/a |
| meta_tables | ADBC | 1 | 6.6 / 8.1 / 9.6 | n/a | n/a | n/a |
| meta_tables | ADBC | 8 | 29.0 / 407.2 / 680.7 | n/a | n/a | n/a |
| meta_tables | ADBC | 32 | 75.7 / 170.4 / 295.9 | n/a | n/a | n/a |
| meta_schemas | JDBC | 1 | 5.2 / 9.1 / 10.2 | n/a | n/a | n/a |
| meta_schemas | JDBC | 8 | 11.3 / 24.5 / 44.5 | n/a | n/a | n/a |
| meta_schemas | JDBC | 32 | 24.8 / 65.2 / 87.5 | n/a | n/a | n/a |
| meta_schemas | ADBC | 1 | 4.1 / 7.2 / 8.0 | n/a | n/a | n/a |
| meta_schemas | ADBC | 8 | 16.8 / 34.9 / 42.8 | n/a | n/a | n/a |
| meta_schemas | ADBC | 32 | 49.7 / 112.0 / 199.5 | n/a | n/a | n/a |

Answers per class are compared across servers in the run summary (`summary.md`, correctness gate).

### Scans (`SELECT * FROM tpch.lineitem`, SF10, MB/s of Arrow buffers) and server peak RSS

| metric | ours-new | ours-27f5 | up-native | up-main | ours-new vs best upstream |
|---|---|---|---|---|---|
| raw Flight, 1 stream | 544 | n/a | 683 | n/a | n/a |
| raw Flight, 4 streams | 547 | n/a | 876 | n/a | n/a |
| raw Flight, 8 streams | 486 | n/a | 898 | n/a | n/a |
| full export over ADBC | 623 | n/a | 858 | n/a | n/a |
| server peak RSS (MB) | 1699 | n/a | 3845 | n/a | - |

### Server container (docker stats every ~5 s, all workloads of this setting)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| CPU % p50 (200 = both cores) | 201 | n/a | 202 | n/a |
| CPU % max | 220 | n/a | 205 | n/a |
| memory peak (MiB, limit 6144) | 4431 | n/a | 3670 | n/a |
| OOM-killed rounds | 0 / 9 | n/a | 0 / 3 | n/a |

## s3, setting `def`

### TPC-H SF10, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 6950 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 3246 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 12803 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 8423 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 14216 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 11405 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 16499 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 18512 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 19427 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 12028 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 2559 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 13936 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 4808 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 15565 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 14392 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 1232 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 15606 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 12955 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 18284 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 14602 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 29428 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 1627 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 268503 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF1, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 1102 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 560 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1824 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 1165 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 1883 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 1499 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 2049 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 2565 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 2594 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1746 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 424 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 1825 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 556 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 1757 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 1329 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 210 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 2198 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 1795 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 1840 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 1862 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 3439 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 292 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 34514 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF10, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 6933 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 3298 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 13047 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 8029 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 14081 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 11097 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 16311 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 18541 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 22267 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 11782 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 2483 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 14351 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 5591 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 18143 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 17302 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 1540 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 23444 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 17956 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 18688 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 21861 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 43014 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 2555 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 312314 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### TPC-H SF1, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 1085 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 554 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1803 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 1124 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 1883 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 1486 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 2819 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 2526 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 2544 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1702 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 456 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 1751 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 551 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 1709 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 1379 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 236 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 2210 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 1812 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 1822 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 1783 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 3491 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 296 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 35022 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### Small queries (ms, p50 / p95 / p99 over all rounds)

| class | client | c | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|---|---|
| point_orders | JDBC | 1 | 29.8 / 50.9 / 89.9 | n/a | n/a | n/a |
| point_orders | JDBC | 8 | 316.4 / 591.8 / 785.6 | n/a | n/a | n/a |
| point_orders | JDBC | 32 | 1293.2 / 2148.7 / 2477.0 | n/a | n/a | n/a |
| point_orders | ADBC | 1 | 21.6 / 46.7 / 54.9 | n/a | n/a | n/a |
| point_orders | ADBC | 8 | 312.4 / 543.3 / 617.6 | n/a | n/a | n/a |
| point_orders | ADBC | 32 | 1322.8 / 2092.8 / 2556.4 | n/a | n/a | n/a |
| point_lineitem | JDBC | 1 | 23.1 / 48.4 / 152.5 | n/a | n/a | n/a |
| point_lineitem | JDBC | 8 | 177.2 / 321.0 / 384.6 | n/a | n/a | n/a |
| point_lineitem | JDBC | 32 | 609.4 / 2193.8 / 15604.4 | n/a | n/a | n/a |
| point_lineitem | ADBC | 1 | 16.1 / 37.1 / 59.4 | n/a | n/a | n/a |
| point_lineitem | ADBC | 8 | 176.0 / 437.5 / 5209.5 | n/a | n/a | n/a |
| point_lineitem | ADBC | 32 | 610.4 / 1220.1 / 4717.4 | n/a | n/a | n/a |
| count_filter | JDBC | 1 | 643.4 / 811.8 / 962.7 | n/a | n/a | n/a |
| count_filter | JDBC | 8 | 3759.2 / 4352.9 / 4536.1 | n/a | n/a | n/a |
| count_filter | JDBC | 32 | 12731.4 / 21271.3 / 26155.0 | n/a | n/a | n/a |
| count_filter | ADBC | 1 | 693.3 / 925.6 / 1039.1 | n/a | n/a | n/a |
| count_filter | ADBC | 8 | 3769.8 / 4592.1 / 4906.5 | n/a | n/a | n/a |
| count_filter | ADBC | 32 | 12371.0 / 14800.2 / 15411.3 | n/a | n/a | n/a |
| limit10_ob | JDBC | 1 | 115.2 / 219.1 / 248.1 | n/a | n/a | n/a |
| limit10_ob | JDBC | 8 | 589.3 / 898.8 / 1110.2 | n/a | n/a | n/a |
| limit10_ob | JDBC | 32 | 2308.7 / 3470.6 / 21511.4 | n/a | n/a | n/a |
| limit10_ob | ADBC | 1 | 109.7 / 226.2 / 261.0 | n/a | n/a | n/a |
| limit10_ob | ADBC | 8 | 598.2 / 922.3 / 1071.0 | n/a | n/a | n/a |
| limit10_ob | ADBC | 32 | 2400.3 / 3269.4 / 3710.2 | n/a | n/a | n/a |
| meta_tables | JDBC | 1 | 7.1 / 9.9 / 12.7 | n/a | n/a | n/a |
| meta_tables | JDBC | 8 | 5.2 / 14.4 / 17.8 | n/a | n/a | n/a |
| meta_tables | JDBC | 32 | 6.3 / 19.5 / 36.0 | n/a | n/a | n/a |
| meta_tables | ADBC | 1 | 5.9 / 9.6 / 14.0 | n/a | n/a | n/a |
| meta_tables | ADBC | 8 | 8.1 / 28.5 / 33.2 | n/a | n/a | n/a |
| meta_tables | ADBC | 32 | 16.4 / 41.7 / 71.5 | n/a | n/a | n/a |
| meta_schemas | JDBC | 1 | 4.8 / 8.2 / 13.5 | n/a | n/a | n/a |
| meta_schemas | JDBC | 8 | 4.1 / 11.4 / 14.0 | n/a | n/a | n/a |
| meta_schemas | JDBC | 32 | 5.1 / 19.3 / 35.2 | n/a | n/a | n/a |
| meta_schemas | ADBC | 1 | 3.8 / 7.3 / 8.5 | n/a | n/a | n/a |
| meta_schemas | ADBC | 8 | 5.7 / 19.6 / 24.8 | n/a | n/a | n/a |
| meta_schemas | ADBC | 32 | 11.9 / 32.6 / 53.1 | n/a | n/a | n/a |

Answers per class are compared across servers in the run summary (`summary.md`, correctness gate).

### Scans (`SELECT * FROM tpch.lineitem`, SF10, MB/s of Arrow buffers) and server peak RSS

| metric | ours-new | ours-27f5 | up-native | up-main | ours-new vs best upstream |
|---|---|---|---|---|---|
| raw Flight, 1 stream | 360 | n/a | n/a | n/a | n/a |
| raw Flight, 4 streams | 494 | n/a | n/a | n/a | n/a |
| raw Flight, 8 streams | 457 | n/a | n/a | n/a | n/a |
| full export over ADBC | 353 | n/a | n/a | n/a | n/a |
| server peak RSS (MB) | 2732 | n/a | n/a | n/a | - |

### Server container (docker stats every ~5 s, all workloads of this setting)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| CPU % p50 (200 = both cores) | 26 | n/a | n/a | n/a |
| CPU % max | 205 | n/a | n/a | n/a |
| memory peak (MiB, limit 6144) | 2446 | n/a | n/a | n/a |
| OOM-killed rounds | 0 / 12 | n/a | n/a | n/a |

