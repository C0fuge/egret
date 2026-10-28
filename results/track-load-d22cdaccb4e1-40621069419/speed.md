# Server comparison - Report 1: SPEED (compare run 40621069419)

## Experiment setup

| item | value |
|---|---|
| runner | GitHub-hosted `ubuntu-latest`: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor; Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor; Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor; Linux ubuntu24 4 vCPU Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz; RAM 15989 MB; kernel 6.17.0-1022-azure; JDK Temurin 21 |
| containers | every server: `eclipse-temurin:21-jre`, `--cpus=2 --cpuset-cpus=0,1 --memory=6g --memory-swap=6g`, JVM `-Xmx3g -XX:MaxDirectMemorySize=2g`, `MALLOC_ARENA_MAX=4`, host network; clients (JDBC/ADBC/Flight runners, jcmd sampling) and the S3 server in their own containers on cpus 2,3 |
| servers | ours-new = `7562a5bdb7b9` (DuckDB v1.5.6); ours-27f5 = `27f583adccd7` (DuckDB ?); up-native = `a4ebfbc55e2307b3b7fe104be1144ea8f555bbca` (DuckDB error: INTERNAL: [FlightSQL] Failed to prepare Flight SQL statement (Internal; Prepare). Vendor code: 13); up-main = `dbacd8d585bce2ef2a449c821fe3a53cc6060b57` (DuckDB ?) |
| data | TPC-H SF1 and SF10, DuckDB dbgen, Parquet, 8 files per big table, 122880-row row groups, one data dir `tpch.*` per SF |
| storage | local disk (`file://`, page-cached) and S3 (`rclone serve s3` on the same runner, path style) |
| pairs | every job: ours-new (side A) vs one other server (side B) on the same runner, rounds A B / B A / A B (3), 1 cold run (warm-up) + warm runs per query (SF1 2 warm, SF10 1 warm per round) |
| settings | `def` = each server's default (`duckDbThreads` ours 4, upstream 2); `t8` = `-DduckDbThreads=8` on both |
| batch size | server defaults (not overridden) |
| clients | TPC-H: Python ADBC Flight SQL 1.12.0 (pyarrow 26), Flight SQL JDBC 18.0.0; small queries: same; scans: raw Flight (Arrow Java), ADBC export |
| correctness | TPC-H over ADBC: rows + checksum per query equal to in-process DuckDB on the same files; over JDBC: the result rows compared numerically with the same reference (numbers within a relative 1.5e-9, i.e. two 10-digit roundings; the JDBC runner prints DECIMAL as an exact plain BigDecimal, the reference as %.10g) |
| upstream on S3 | up-native: `s3a://` data dir (Hadoop S3A from its `docker/hadoop-aws` recipe for listing, DuckDB httpfs for scans, `FLIGHT_S3_*` settings); up-main: **n/a**, main at the fork point has no S3 settings (no `FLIGHT_S3_*`, no S3A dependencies) |
| SF30 | not run: SF1+SF10 already fill most of the repo's 10 GB Actions cache, SF30 Parquet (~11 GB) does not fit; generating it per job costs ~20 min of each 4-vCPU runner |
| JVM `d22cdaccb4e1` `def` | `--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED -Darrowflight.plugins.dir=/app/plugins -Darrowflight.duckdb.extensionDir=/ext/duckdb-home/extensions -DduckDbAllowUnsignedExtensions=true -Ds3Endpoint=http://127.0.0.1:9000 -Ds3UrlStyle=path -Ds3Region=us-east-1 -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf10 -cp --port --localhost --hosts` |
| JVM `ours-new` `def` | `--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED -Darrowflight.plugins.dir=/app/plugins -Darrowflight.duckdb.extensionDir=/ext/duckdb-home/extensions -DduckDbAllowUnsignedExtensions=true -Ds3Endpoint=http://127.0.0.1:9000 -Ds3UrlStyle=path -Ds3Region=us-east-1 -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf10 -cp --port --localhost --hosts` |
| JVM `up-native` `def` | `--add-modules --add-exports --add-opens --add-opens --add-opens=java.base/java.nio=ALL-UNNAMED --add-opens --add-opens -Dio.netty.tryReflectionSetAccessible=true -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf10 -DflightCompression=zstd -cp --port --localhost --hosts` |

Times are warm medians in ms (median over rounds of the per-round warm median). **n/a** = not run, failed or wrong
answer (reason in the notes). Last column: same-runner ratio best-upstream / ours-new (> 1 = ours-new faster).

## local, setting `def`

### TPC-H SF10, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 2165 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 332 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1233 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 834 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 1458 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 647 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 1394 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 1741 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 3382 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1503 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 296 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 839 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 2566 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 1016 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 892 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 448 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 1451 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 2458 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 1366 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 1181 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 4591 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 479 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 32270 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF1, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 268 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 50 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 138 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 92 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 137 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 81 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 139 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 172 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 242 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 178 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 36 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 96 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 229 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 112 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 78 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 60 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 144 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 289 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 149 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 119 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 358 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 64 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 3232 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF10, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 2168 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 335 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1217 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 827 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 1446 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 640 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 1398 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 1714 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 3330 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1528 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 298 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 835 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 2346 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 994 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 891 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 470 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 1425 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 2476 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 1356 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 1192 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 4712 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 489 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 32088 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### TPC-H SF1, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 284 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 60 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 140 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 98 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 143 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 88 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 149 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 184 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 249 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 177 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 47 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 100 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 235 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 113 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 81 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 72 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 138 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 288 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 150 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 119 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 362 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 61 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 3338 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### Small queries (ms, p50 / p95 / p99 over all rounds)

| class | client | c | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|---|---|
| point_orders | JDBC | 1 | 25.8 / 35.4 / 46.1 | n/a | n/a | n/a |
| point_orders | JDBC | 8 | 122.6 / 191.0 / 350.8 | n/a | n/a | n/a |
| point_orders | JDBC | 32 | 474.3 / 903.9 / 1064.2 | n/a | n/a | n/a |
| point_orders | ADBC | 1 | 15.7 / 25.0 / 30.5 | n/a | n/a | n/a |
| point_orders | ADBC | 8 | 105.8 / 167.3 / 203.6 | n/a | n/a | n/a |
| point_orders | ADBC | 32 | 384.1 / 774.9 / 954.9 | n/a | n/a | n/a |
| point_lineitem | JDBC | 1 | 34.4 / 46.1 / 53.1 | n/a | n/a | n/a |
| point_lineitem | JDBC | 8 | 189.4 / 290.0 / 509.8 | n/a | n/a | n/a |
| point_lineitem | JDBC | 32 | 750.2 / 1276.7 / 1816.5 | n/a | n/a | n/a |
| point_lineitem | ADBC | 1 | 23.9 / 38.9 / 44.2 | n/a | n/a | n/a |
| point_lineitem | ADBC | 8 | 174.8 / 264.2 / 327.3 | n/a | n/a | n/a |
| point_lineitem | ADBC | 32 | 696.1 / 1133.1 / 1323.9 | n/a | n/a | n/a |
| count_filter | JDBC | 1 | 49.8 / 61.9 / 84.4 | n/a | n/a | n/a |
| count_filter | JDBC | 8 | 227.6 / 290.6 / 317.8 | n/a | n/a | n/a |
| count_filter | JDBC | 32 | 883.3 / 1545.7 / 2170.7 | n/a | n/a | n/a |
| count_filter | ADBC | 1 | 42.0 / 55.8 / 67.9 | n/a | n/a | n/a |
| count_filter | ADBC | 8 | 221.8 / 282.3 / 328.8 | n/a | n/a | n/a |
| count_filter | ADBC | 32 | 815.4 / 1308.4 / 1452.9 | n/a | n/a | n/a |
| limit10_ob | JDBC | 1 | 45.4 / 60.9 / 76.4 | n/a | n/a | n/a |
| limit10_ob | JDBC | 8 | 259.1 / 365.6 / 421.3 | n/a | n/a | n/a |
| limit10_ob | JDBC | 32 | 1040.9 / 1696.4 / 2278.3 | n/a | n/a | n/a |
| limit10_ob | ADBC | 1 | 38.7 / 56.6 / 71.7 | n/a | n/a | n/a |
| limit10_ob | ADBC | 8 | 245.7 / 334.6 / 367.8 | n/a | n/a | n/a |
| limit10_ob | ADBC | 32 | 1058.4 / 1688.6 / 2021.4 | n/a | n/a | n/a |
| meta_tables | JDBC | 1 | 8.9 / 13.9 / 15.3 | n/a | n/a | n/a |
| meta_tables | JDBC | 8 | 15.7 / 38.1 / 535.0 | n/a | n/a | n/a |
| meta_tables | JDBC | 32 | 35.5 / 1316.3 / 2078.5 | n/a | n/a | n/a |
| meta_tables | ADBC | 1 | 8.2 / 11.3 / 12.8 | n/a | n/a | n/a |
| meta_tables | ADBC | 8 | 34.3 / 58.0 / 68.4 | n/a | n/a | n/a |
| meta_tables | ADBC | 32 | 110.9 / 1781.1 / 2726.6 | n/a | n/a | n/a |
| meta_schemas | JDBC | 1 | 7.3 / 11.7 / 21.5 | n/a | n/a | n/a |
| meta_schemas | JDBC | 8 | 13.9 / 28.1 / 36.7 | n/a | n/a | n/a |
| meta_schemas | JDBC | 32 | 26.0 / 68.2 / 167.3 | n/a | n/a | n/a |
| meta_schemas | ADBC | 1 | 5.3 / 8.6 / 9.9 | n/a | n/a | n/a |
| meta_schemas | ADBC | 8 | 21.9 / 41.4 / 51.2 | n/a | n/a | n/a |
| meta_schemas | ADBC | 32 | 59.0 / 138.2 / 249.6 | n/a | n/a | n/a |

Answers per class are compared across servers in the run summary (`summary.md`, correctness gate).

### Scans (`SELECT * FROM tpch.lineitem`, SF10, MB/s of Arrow buffers) and server peak RSS

| metric | ours-new | ours-27f5 | up-native | up-main | ours-new vs best upstream |
|---|---|---|---|---|---|
| raw Flight, 1 stream | 438 | n/a | n/a | n/a | n/a |
| raw Flight, 4 streams | 478 | n/a | n/a | n/a | n/a |
| raw Flight, 8 streams | 439 | n/a | n/a | n/a | n/a |
| full export over ADBC | 522 | n/a | n/a | n/a | n/a |
| server peak RSS (MB) | 1746 | n/a | n/a | n/a | - |

### Server container (docker stats every ~5 s, all workloads of this setting)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| CPU % p50 (200 = both cores) | 199 | n/a | 168 | n/a |
| CPU % max | 211 | n/a | 186 | n/a |
| memory peak (MiB, limit 6144) | 1788 | n/a | 614 | n/a |
| OOM-killed rounds | 0 / 21 | n/a | 0 / 6 | n/a |

## s3, setting `def`

### TPC-H SF10, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 10224 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 4554 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 17435 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 10958 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 20118 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 15573 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 25702 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 26806 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 29148 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 16398 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 3475 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 20483 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 6286 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 19478 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 19062 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 1736 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 25914 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 19228 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 20380 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 23941 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 47457 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 2756 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 387110 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF1, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 841 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 472 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1695 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 1042 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 1621 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 1479 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 2029 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 2319 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 2333 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1567 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 360 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 1847 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 408 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 1564 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 1350 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 168 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 2138 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 1644 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 1659 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 1751 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 3255 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 227 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 31770 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF10, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 10109 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 4654 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 22578 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 11377 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 22947 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 15447 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 24941 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 42240 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 34999 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 21624 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 4723 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 23368 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 6880 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 21774 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 24761 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 1819 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 28668 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 21369 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 23191 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 27147 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 56753 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 3542 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 454912 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### TPC-H SF1, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 730 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 359 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1336 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 814 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 1682 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 1408 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 2019 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 2322 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 2324 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1559 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 393 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 1844 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 398 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 1590 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 1304 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 182 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 2065 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 1710 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 1682 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 1811 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 3176 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 225 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 30934 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### Small queries (ms, p50 / p95 / p99 over all rounds)

| class | client | c | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|---|---|
| point_orders | JDBC | 1 | 29.5 / 35.7 / 39.0 | n/a | n/a | n/a |
| point_orders | JDBC | 8 | 431.0 / 814.5 / 1066.8 | n/a | n/a | n/a |
| point_orders | JDBC | 32 | 1523.1 / 3174.1 / 6916.6 | n/a | n/a | n/a |
| point_orders | ADBC | 1 | 21.7 / 42.7 / 46.8 | n/a | n/a | n/a |
| point_orders | ADBC | 8 | 490.4 / 774.5 / 894.9 | n/a | n/a | n/a |
| point_orders | ADBC | 32 | 1723.7 / 3578.5 / 5803.4 | n/a | n/a | n/a |
| point_lineitem | JDBC | 1 | 25.0 / 48.3 / 53.0 | n/a | n/a | n/a |
| point_lineitem | JDBC | 8 | 252.8 / 549.0 / 7498.3 | n/a | n/a | n/a |
| point_lineitem | JDBC | 32 | 882.7 / 15148.8 / 21706.0 | n/a | n/a | n/a |
| point_lineitem | ADBC | 1 | 18.3 / 29.9 / 37.8 | n/a | n/a | n/a |
| point_lineitem | ADBC | 8 | 298.7 / 491.6 / 6323.4 | n/a | n/a | n/a |
| point_lineitem | ADBC | 32 | 986.6 / 18438.1 / 29078.0 | n/a | n/a | n/a |
| count_filter | JDBC | 1 | 788.9 / 851.9 / 858.8 | n/a | n/a | n/a |
| count_filter | JDBC | 8 | 5770.7 / 12788.5 / 17375.1 | n/a | n/a | n/a |
| count_filter | JDBC | 32 | 16971.9 / 35317.6 / 38465.7 | n/a | n/a | n/a |
| count_filter | ADBC | 1 | 790.3 / 865.6 / 880.5 | n/a | n/a | n/a |
| count_filter | ADBC | 8 | 5508.4 / 8032.6 / 8355.7 | n/a | n/a | n/a |
| count_filter | ADBC | 32 | 20467.3 / 39482.2 / 48236.4 | n/a | n/a | n/a |
| limit10_ob | JDBC | 1 | 128.4 / 163.5 / 176.3 | n/a | n/a | n/a |
| limit10_ob | JDBC | 8 | 861.1 / 1377.0 / 7739.8 | n/a | n/a | n/a |
| limit10_ob | JDBC | 32 | 2893.4 / 5652.5 / 17490.0 | n/a | n/a | n/a |
| limit10_ob | ADBC | 1 | 128.0 / 181.7 / 187.6 | n/a | n/a | n/a |
| limit10_ob | ADBC | 8 | 945.7 / 1637.6 / 6129.5 | n/a | n/a | n/a |
| limit10_ob | ADBC | 32 | 3158.4 / 5828.9 / 26548.1 | n/a | n/a | n/a |
| meta_tables | JDBC | 1 | 8.2 / 11.8 / 14.4 | n/a | n/a | n/a |
| meta_tables | JDBC | 8 | 4.6 / 11.7 / 16.6 | n/a | n/a | n/a |
| meta_tables | JDBC | 32 | 6.2 / 23.9 / 45.4 | n/a | n/a | n/a |
| meta_tables | ADBC | 1 | 7.2 / 11.1 / 18.0 | n/a | n/a | n/a |
| meta_tables | ADBC | 8 | 7.4 / 14.9 / 18.5 | n/a | n/a | n/a |
| meta_tables | ADBC | 32 | 15.9 / 39.8 / 61.1 | n/a | n/a | n/a |
| meta_schemas | JDBC | 1 | 5.3 / 9.0 / 10.4 | n/a | n/a | n/a |
| meta_schemas | JDBC | 8 | 3.8 / 13.1 / 18.4 | n/a | n/a | n/a |
| meta_schemas | JDBC | 32 | 4.3 / 22.2 / 38.7 | n/a | n/a | n/a |
| meta_schemas | ADBC | 1 | 4.7 / 8.5 / 12.4 | n/a | n/a | n/a |
| meta_schemas | ADBC | 8 | 4.6 / 11.4 / 18.5 | n/a | n/a | n/a |
| meta_schemas | ADBC | 32 | 10.7 / 34.8 / 65.1 | n/a | n/a | n/a |

Answers per class are compared across servers in the run summary (`summary.md`, correctness gate).

### Scans (`SELECT * FROM tpch.lineitem`, SF10, MB/s of Arrow buffers) and server peak RSS

| metric | ours-new | ours-27f5 | up-native | up-main | ours-new vs best upstream |
|---|---|---|---|---|---|
| raw Flight, 1 stream | 414 | n/a | n/a | n/a | n/a |
| raw Flight, 4 streams | 483 | n/a | n/a | n/a | n/a |
| raw Flight, 8 streams | 462 | n/a | n/a | n/a | n/a |
| full export over ADBC | 438 | n/a | n/a | n/a | n/a |
| server peak RSS (MB) | 2814 | n/a | n/a | n/a | - |

### Server container (docker stats every ~5 s, all workloads of this setting)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| CPU % p50 (200 = both cores) | 23 | n/a | n/a | n/a |
| CPU % max | 211 | n/a | n/a | n/a |
| memory peak (MiB, limit 6144) | 2729 | n/a | n/a | n/a |
| OOM-killed rounds | 0 / 15 | n/a | n/a | n/a |

