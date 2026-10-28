# Server comparison - Report 1: SPEED (compare run 40638050743)

## Experiment setup

| item | value |
|---|---|
| runner | GitHub-hosted `ubuntu-latest`: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor; Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor; Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor; Linux ubuntu24 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C; Linux ubuntu24 4 vCPU Intel(R) Xeon(R) 6973P-C; RAM 15989 MB; kernel 6.17.0-1022-azure; JDK Temurin 21 |
| containers | every server: `eclipse-temurin:21-jre`, `--cpus=2 --cpuset-cpus=0,1 --memory=6g --memory-swap=6g`, JVM `-Xmx3g -XX:MaxDirectMemorySize=2g`, `MALLOC_ARENA_MAX=4`, host network; clients (JDBC/ADBC/Flight runners, jcmd sampling) and the S3 server in their own containers on cpus 2,3 |
| servers | ours-new = `7562a5bdb7b9` (DuckDB v1.5.6); ours-27f5 = `27f583adccd7` (DuckDB ?); up-native = `0f77f2cdfa7fa00556ce338723038593e904b066` (DuckDB error: INTERNAL: [FlightSQL] Failed to prepare Flight SQL statement (Internal; Prepare). Vendor code: 13); up-main = `dbacd8d585bce2ef2a449c821fe3a53cc6060b57` (DuckDB ?) |
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
| JVM `d22cdaccb4e1` `def` | `--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED -Darrowflight.plugins.dir=/app/plugins -Darrowflight.duckdb.extensionDir=/ext/duckdb-home/extensions -DduckDbAllowUnsignedExtensions=true -Ds3Endpoint=http://127.0.0.1:9000 -Ds3UrlStyle=path -Ds3Region=us-east-1 -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=s3://default/sf10 -cp --port --localhost --hosts` |
| JVM `ours-new` `def` | `--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED -Darrowflight.plugins.dir=/app/plugins -Darrowflight.duckdb.extensionDir=/ext/duckdb-home/extensions -DduckDbAllowUnsignedExtensions=true -Ds3Endpoint=http://127.0.0.1:9000 -Ds3UrlStyle=path -Ds3Region=us-east-1 -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf10 -cp --port --localhost --hosts` |
| JVM `up-native` `def` | `--add-modules --add-exports --add-opens --add-opens --add-opens=java.base/java.nio=ALL-UNNAMED --add-opens --add-opens -Dio.netty.tryReflectionSetAccessible=true -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf10 -cp --port --localhost --hosts` |

Times are warm medians in ms (median over rounds of the per-round warm median). **n/a** = not run, failed or wrong
answer (reason in the notes). Last column: same-runner ratio best-upstream / ours-new (> 1 = ours-new faster).

## local, setting `def`

### TPC-H SF10, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 1726 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 309 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1116 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 763 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 1363 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 574 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 1255 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 1560 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 3106 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1421 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 263 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 779 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 2348 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 907 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 808 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 441 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 1246 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 2302 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 1222 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 1062 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 3856 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 443 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 28870 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF1, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 218 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 45 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 121 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 82 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 125 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 74 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 138 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 155 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 238 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 178 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 33 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 87 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 216 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 106 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 71 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 64 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 125 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 269 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 137 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 147 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 344 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 58 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 3031 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF10, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 1771 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 311 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1089 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 744 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 1351 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 582 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 1266 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 1529 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 3134 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1519 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 268 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 735 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 2325 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 972 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 811 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 450 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 1232 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 2254 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 1213 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 1053 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 3858 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 447 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 28914 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### TPC-H SF1, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 225 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 55 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 126 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 89 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 130 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 83 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 138 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 171 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 237 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 172 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 47 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 87 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 211 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 113 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 74 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 69 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 131 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 263 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 140 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 111 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 334 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 55 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 3061 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### Small queries (ms, p50 / p95 / p99 over all rounds)

| class | client | c | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|---|---|
| point_orders | JDBC | 1 | 22.0 / 31.9 / 38.4 | n/a | n/a | n/a |
| point_orders | JDBC | 8 | 113.7 / 178.9 / 344.7 | n/a | n/a | n/a |
| point_orders | JDBC | 32 | 480.6 / 920.4 / 1177.7 | n/a | n/a | n/a |
| point_orders | ADBC | 1 | 15.0 / 23.3 / 26.2 | n/a | n/a | n/a |
| point_orders | ADBC | 8 | 97.6 / 147.5 / 200.0 | n/a | n/a | n/a |
| point_orders | ADBC | 32 | 378.2 / 733.8 / 903.5 | n/a | n/a | n/a |
| point_lineitem | JDBC | 1 | 30.9 / 40.3 / 46.7 | n/a | n/a | n/a |
| point_lineitem | JDBC | 8 | 184.3 / 291.5 / 370.0 | n/a | n/a | n/a |
| point_lineitem | JDBC | 32 | 713.0 / 1149.6 / 1400.3 | n/a | n/a | n/a |
| point_lineitem | ADBC | 1 | 24.2 / 35.5 / 43.6 | n/a | n/a | n/a |
| point_lineitem | ADBC | 8 | 170.4 / 245.2 / 295.3 | n/a | n/a | n/a |
| point_lineitem | ADBC | 32 | 718.8 / 1140.6 / 1306.4 | n/a | n/a | n/a |
| count_filter | JDBC | 1 | 46.4 / 60.0 / 62.7 | n/a | n/a | n/a |
| count_filter | JDBC | 8 | 222.9 / 297.0 / 327.8 | n/a | n/a | n/a |
| count_filter | JDBC | 32 | 822.6 / 1340.4 / 1747.9 | n/a | n/a | n/a |
| count_filter | ADBC | 1 | 41.4 / 55.4 / 66.6 | n/a | n/a | n/a |
| count_filter | ADBC | 8 | 213.6 / 266.0 / 289.2 | n/a | n/a | n/a |
| count_filter | ADBC | 32 | 831.0 / 1198.4 / 1435.0 | n/a | n/a | n/a |
| limit10_ob | JDBC | 1 | 44.0 / 52.2 / 56.9 | n/a | n/a | n/a |
| limit10_ob | JDBC | 8 | 255.6 / 350.4 / 478.7 | n/a | n/a | n/a |
| limit10_ob | JDBC | 32 | 975.3 / 1667.9 / 1960.5 | n/a | n/a | n/a |
| limit10_ob | ADBC | 1 | 36.3 / 47.5 / 56.7 | n/a | n/a | n/a |
| limit10_ob | ADBC | 8 | 243.9 / 327.1 / 369.8 | n/a | n/a | n/a |
| limit10_ob | ADBC | 32 | 987.7 / 1515.4 / 1722.2 | n/a | n/a | n/a |
| meta_tables | JDBC | 1 | 7.6 / 11.9 / 13.1 | n/a | n/a | n/a |
| meta_tables | JDBC | 8 | 12.8 / 28.9 / 40.8 | n/a | n/a | n/a |
| meta_tables | JDBC | 32 | 33.1 / 1679.3 / 2183.0 | n/a | n/a | n/a |
| meta_tables | ADBC | 1 | 7.3 / 10.7 / 11.5 | n/a | n/a | n/a |
| meta_tables | ADBC | 8 | 32.0 / 52.9 / 63.8 | n/a | n/a | n/a |
| meta_tables | ADBC | 32 | 96.7 / 1740.6 / 2556.3 | n/a | n/a | n/a |
| meta_schemas | JDBC | 1 | 5.3 / 9.2 / 14.0 | n/a | n/a | n/a |
| meta_schemas | JDBC | 8 | 11.4 / 24.3 / 28.6 | n/a | n/a | n/a |
| meta_schemas | JDBC | 32 | 22.0 / 70.2 / 130.1 | n/a | n/a | n/a |
| meta_schemas | ADBC | 1 | 4.8 / 7.5 / 11.5 | n/a | n/a | n/a |
| meta_schemas | ADBC | 8 | 20.5 / 38.6 / 54.8 | n/a | n/a | n/a |
| meta_schemas | ADBC | 32 | 50.6 / 113.9 / 184.3 | n/a | n/a | n/a |

Answers per class are compared across servers in the run summary (`summary.md`, correctness gate).

### Scans (`SELECT * FROM tpch.lineitem`, SF10, MB/s of Arrow buffers) and server peak RSS

| metric | ours-new | ours-27f5 | up-native | up-main | ours-new vs best upstream |
|---|---|---|---|---|---|
| raw Flight, 1 stream | 456 | n/a | n/a | n/a | n/a |
| raw Flight, 4 streams | 503 | n/a | n/a | n/a | n/a |
| raw Flight, 8 streams | 471 | n/a | n/a | n/a | n/a |
| full export over ADBC | 541 | n/a | n/a | n/a | n/a |
| server peak RSS (MB) | 1743 | n/a | n/a | n/a | - |

### Server container (docker stats every ~5 s, all workloads of this setting)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| CPU % p50 (200 = both cores) | 202 | n/a | 201 | n/a |
| CPU % max | 211 | n/a | 204 | n/a |
| memory peak (MiB, limit 6144) | 5501 | n/a | 5036 | n/a |
| OOM-killed rounds | 0 / 9 | n/a | 0 / 3 | n/a |

## s3, setting `def`

### TPC-H SF10, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 7031 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 3350 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 12734 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 8203 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 14317 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 11216 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 16334 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 18915 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 23186 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 11955 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 2482 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 17718 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 5748 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 17512 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 17222 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 1581 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 23276 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 17988 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 18753 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 21984 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 45059 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 2543 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 319107 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF1, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 803 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 399 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1461 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 945 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 1408 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 1150 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 1593 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 1863 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 1954 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1304 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 302 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 1454 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 378 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 1240 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 1010 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 114 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 1692 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 1413 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 1358 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 1409 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 2495 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 200 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 25945 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF10, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 8351 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 3793 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 23297 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 13042 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 24946 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 19750 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 30389 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 39596 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 34441 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 21520 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 4703 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 24262 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 6345 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 21245 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 21157 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 1951 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 28004 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 22300 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 23761 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 27555 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 51689 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 4001 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 456098 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### TPC-H SF1, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 744 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 379 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1434 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 851 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 1354 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 1103 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 1594 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 1843 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 1863 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1316 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 298 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 1484 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 378 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 1292 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 1060 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 131 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 1702 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 1398 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 1442 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 1407 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 2657 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 201 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 25931 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### Small queries (ms, p50 / p95 / p99 over all rounds)

| class | client | c | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|---|---|
| point_orders | JDBC | 1 | 29.0 / 35.0 / 38.1 | n/a | n/a | n/a |
| point_orders | JDBC | 8 | 429.0 / 699.3 / 818.1 | n/a | n/a | n/a |
| point_orders | JDBC | 32 | 1608.0 / 3038.7 / 4136.0 | n/a | n/a | n/a |
| point_orders | ADBC | 1 | 22.0 / 33.9 / 41.0 | n/a | n/a | n/a |
| point_orders | ADBC | 8 | 451.1 / 832.1 / 978.1 | n/a | n/a | n/a |
| point_orders | ADBC | 32 | 1555.6 / 2859.0 / 3695.4 | n/a | n/a | n/a |
| point_lineitem | JDBC | 1 | 24.8 / 45.4 / 55.5 | n/a | n/a | n/a |
| point_lineitem | JDBC | 8 | 251.8 / 408.3 / 498.9 | n/a | n/a | n/a |
| point_lineitem | JDBC | 32 | 935.9 / 5991.6 / 15954.4 | n/a | n/a | n/a |
| point_lineitem | ADBC | 1 | 17.5 / 36.5 / 38.1 | n/a | n/a | n/a |
| point_lineitem | ADBC | 8 | 285.7 / 4882.2 / 7959.5 | n/a | n/a | n/a |
| point_lineitem | ADBC | 32 | 886.9 / 5092.3 / 17138.4 | n/a | n/a | n/a |
| count_filter | JDBC | 1 | 749.0 / 803.1 / 841.7 | n/a | n/a | n/a |
| count_filter | JDBC | 8 | 5172.5 / 5779.2 / 9409.3 | n/a | n/a | n/a |
| count_filter | JDBC | 32 | 16666.7 / 26062.9 / 27611.5 | n/a | n/a | n/a |
| count_filter | ADBC | 1 | 748.9 / 848.3 / 869.5 | n/a | n/a | n/a |
| count_filter | ADBC | 8 | 5634.3 / 7745.7 / 8308.1 | n/a | n/a | n/a |
| count_filter | ADBC | 32 | 16867.3 / 47584.5 / 55431.8 | n/a | n/a | n/a |
| limit10_ob | JDBC | 1 | 125.4 / 160.7 / 166.6 | n/a | n/a | n/a |
| limit10_ob | JDBC | 8 | 787.9 / 1100.1 / 1250.4 | n/a | n/a | n/a |
| limit10_ob | JDBC | 32 | 2935.8 / 5184.2 / 17570.6 | n/a | n/a | n/a |
| limit10_ob | ADBC | 1 | 134.7 / 175.8 / 183.7 | n/a | n/a | n/a |
| limit10_ob | ADBC | 8 | 910.6 / 1521.1 / 1686.4 | n/a | n/a | n/a |
| limit10_ob | ADBC | 32 | 2965.0 / 5213.0 / 11962.7 | n/a | n/a | n/a |
| meta_tables | JDBC | 1 | 8.1 / 13.4 / 14.4 | n/a | n/a | n/a |
| meta_tables | JDBC | 8 | 5.0 / 14.2 / 22.2 | n/a | n/a | n/a |
| meta_tables | JDBC | 32 | 5.3 / 18.2 / 55.0 | n/a | n/a | n/a |
| meta_tables | ADBC | 1 | 7.9 / 14.1 / 22.8 | n/a | n/a | n/a |
| meta_tables | ADBC | 8 | 7.5 / 19.6 / 33.4 | n/a | n/a | n/a |
| meta_tables | ADBC | 32 | 15.4 / 41.5 / 85.4 | n/a | n/a | n/a |
| meta_schemas | JDBC | 1 | 5.4 / 9.1 / 10.7 | n/a | n/a | n/a |
| meta_schemas | JDBC | 8 | 4.0 / 11.5 / 16.9 | n/a | n/a | n/a |
| meta_schemas | JDBC | 32 | 4.8 / 19.3 / 47.2 | n/a | n/a | n/a |
| meta_schemas | ADBC | 1 | 4.9 / 7.5 / 8.8 | n/a | n/a | n/a |
| meta_schemas | ADBC | 8 | 5.2 / 14.6 / 18.6 | n/a | n/a | n/a |
| meta_schemas | ADBC | 32 | 10.8 / 36.1 / 62.5 | n/a | n/a | n/a |

Answers per class are compared across servers in the run summary (`summary.md`, correctness gate).

### Scans (`SELECT * FROM tpch.lineitem`, SF10, MB/s of Arrow buffers) and server peak RSS

| metric | ours-new | ours-27f5 | up-native | up-main | ours-new vs best upstream |
|---|---|---|---|---|---|
| raw Flight, 1 stream | 408 | n/a | n/a | n/a | n/a |
| raw Flight, 4 streams | 481 | n/a | n/a | n/a | n/a |
| raw Flight, 8 streams | 459 | n/a | n/a | n/a | n/a |
| full export over ADBC | 455 | n/a | n/a | n/a | n/a |
| server peak RSS (MB) | 2807 | n/a | n/a | n/a | - |

### Server container (docker stats every ~5 s, all workloads of this setting)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| CPU % p50 (200 = both cores) | 28 | n/a | n/a | n/a |
| CPU % max | 210 | n/a | n/a | n/a |
| memory peak (MiB, limit 6144) | 2713 | n/a | n/a | n/a |
| OOM-killed rounds | 0 / 12 | n/a | n/a | n/a |

