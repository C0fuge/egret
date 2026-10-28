# Server comparison - Report 1: SPEED (compare run 40699820075)

## Experiment setup

| item | value |
|---|---|
| runner | GitHub-hosted `ubuntu-latest`: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor; Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor; Linux ubuntu24 4 vCPU Intel(R) Xeon(R) 6973P-C; Linux ubuntu24 4 vCPU Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz; RAM 15983 MB; kernel 7.0.0-1017-azure; JDK Temurin 21 |
| containers | every server: `eclipse-temurin:21-jre`, `--cpus=2 --cpuset-cpus=0,1 --memory=6g --memory-swap=6g`, JVM `-Xmx3g -XX:MaxDirectMemorySize=2g`, `MALLOC_ARENA_MAX=4`, host network; clients (JDBC/ADBC/Flight runners, jcmd sampling) and the S3 server in their own containers on cpus 2,3 |
| servers | ours-new = `7562a5bdb7b9` (DuckDB v1.5.6); ours-27f5 = `27f583adccd7` (DuckDB ?); up-native = `9db2bf16a0d15a657f491bb18de1ef50e2e208a8` (DuckDB ?); up-main = `dbacd8d585bce2ef2a449c821fe3a53cc6060b57` (DuckDB ?) |
| data | TPC-H SF1 and SF10, DuckDB dbgen, Parquet, 8 files per big table, 122880-row row groups, one data dir `tpch.*` per SF |
| storage | local disk (`file://`, page-cached) and S3 (`rclone serve s3` on the same runner, path style) |
| pairs | every job: ours-new (side A) vs one other server (side B) on the same runner, rounds A B / B A / A B (3), 1 cold run (warm-up) + warm runs per query (SF1 2 warm, SF10 1 warm per round) |
| settings | `def` = each server's default (`duckDbThreads` ours 4, upstream 2); `t8` = `-DduckDbThreads=8` on both |
| batch size | server defaults (not overridden) |
| clients | TPC-H: Python ADBC Flight SQL 1.12.0 (pyarrow 26), Flight SQL JDBC 18.0.0; small queries: same; scans: raw Flight (Arrow Java), ADBC export |
| correctness | TPC-H over ADBC: rows + checksum per query equal to in-process DuckDB on the same files; over JDBC: the result rows compared numerically with the same reference (numbers within a relative 1.5e-9, i.e. two 10-digit roundings; the JDBC runner prints DECIMAL as an exact plain BigDecimal, the reference as %.10g) |
| upstream on S3 | up-native: `s3a://` data dir (Hadoop S3A from its `docker/hadoop-aws` recipe for listing, DuckDB httpfs for scans, `FLIGHT_S3_*` settings); up-main: **n/a**, main at the fork point has no S3 settings (no `FLIGHT_S3_*`, no S3A dependencies) |
| SF30 | not run: SF1+SF10 already fill most of the repo's 10 GB Actions cache, SF30 Parquet (~11 GB) does not fit; generating it per job costs ~20 min of each 4-vCPU runner |
| JVM `94ad61021d93` `def` | `--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED -Darrowflight.plugins.dir=/app/plugins -Darrowflight.duckdb.extensionDir=/ext/duckdb-home/extensions -DduckDbAllowUnsignedExtensions=true -Ds3Endpoint=http://127.0.0.1:9000 -Ds3UrlStyle=path -Ds3Region=us-east-1 -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf10 -cp --port --localhost --hosts` |
| JVM `ours-new` `def` | `--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED -Darrowflight.plugins.dir=/app/plugins -Darrowflight.duckdb.extensionDir=/ext/duckdb-home/extensions -DduckDbAllowUnsignedExtensions=true -Ds3Endpoint=http://127.0.0.1:9000 -Ds3UrlStyle=path -Ds3Region=us-east-1 -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf10 -cp --port --localhost --hosts` |

Times are warm medians in ms (median over rounds of the per-round warm median). **n/a** = not run, failed or wrong
answer (reason in the notes). Last column: same-runner ratio best-upstream / ours-new (> 1 = ours-new faster).

## local, setting `def`

### TPC-H SF10, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 2637 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 393 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1455 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 975 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 1695 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 747 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 1639 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 1986 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 3931 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1845 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 362 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 1003 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 2807 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 1171 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 1040 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 533 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 1695 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 2965 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 1615 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 1392 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 5201 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 572 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 37659 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF1, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 354 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 57 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 152 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 107 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 164 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 90 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 186 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 200 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 300 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 206 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 44 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 117 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 277 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 130 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 96 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 76 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 172 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 356 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 173 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 143 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 427 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 83 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 3910 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF10, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 2635 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 392 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1406 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 981 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 1682 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 751 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 1616 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 1964 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 3889 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1756 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 360 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 1001 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 2800 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 1167 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 1054 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 600 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 1706 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 2949 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 1628 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 1391 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 5242 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 557 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 37527 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### TPC-H SF1, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 352 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 72 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 162 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 117 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 175 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 97 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 176 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 207 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 294 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 221 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 53 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 121 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 291 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 131 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 95 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 94 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 166 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 357 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 177 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 147 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 424 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 71 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 4000 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### Small queries (ms, p50 / p95 / p99 over all rounds)

| class | client | c | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|---|---|
| point_orders | JDBC | 1 | 26.5 / 42.7 / 48.4 | n/a | n/a | n/a |
| point_orders | JDBC | 8 | 120.7 / 197.0 / 368.7 | n/a | n/a | n/a |
| point_orders | JDBC | 32 | 487.1 / 907.0 / 1333.3 | n/a | n/a | n/a |
| point_orders | ADBC | 1 | 16.9 / 28.3 / 29.4 | n/a | n/a | n/a |
| point_orders | ADBC | 8 | 103.5 / 158.6 / 181.5 | n/a | n/a | n/a |
| point_orders | ADBC | 32 | 391.4 / 729.6 / 1038.7 | n/a | n/a | n/a |
| point_lineitem | JDBC | 1 | 36.3 / 50.3 / 58.7 | n/a | n/a | n/a |
| point_lineitem | JDBC | 8 | 197.1 / 306.0 / 597.7 | n/a | n/a | n/a |
| point_lineitem | JDBC | 32 | 743.0 / 1250.5 / 1607.8 | n/a | n/a | n/a |
| point_lineitem | ADBC | 1 | 25.5 / 41.3 / 46.2 | n/a | n/a | n/a |
| point_lineitem | ADBC | 8 | 180.8 / 275.5 / 344.3 | n/a | n/a | n/a |
| point_lineitem | ADBC | 32 | 690.9 / 1159.1 / 1394.1 | n/a | n/a | n/a |
| count_filter | JDBC | 1 | 50.3 / 62.6 / 64.5 | n/a | n/a | n/a |
| count_filter | JDBC | 8 | 230.4 / 293.2 / 325.1 | n/a | n/a | n/a |
| count_filter | JDBC | 32 | 908.6 / 1497.7 / 1917.4 | n/a | n/a | n/a |
| count_filter | ADBC | 1 | 43.1 / 54.0 / 57.6 | n/a | n/a | n/a |
| count_filter | ADBC | 8 | 225.8 / 287.8 / 359.6 | n/a | n/a | n/a |
| count_filter | ADBC | 32 | 849.6 / 1337.8 / 1530.5 | n/a | n/a | n/a |
| limit10_ob | JDBC | 1 | 47.5 / 59.3 / 71.6 | n/a | n/a | n/a |
| limit10_ob | JDBC | 8 | 266.2 / 382.8 / 464.6 | n/a | n/a | n/a |
| limit10_ob | JDBC | 32 | 1108.4 / 1787.4 / 2116.4 | n/a | n/a | n/a |
| limit10_ob | ADBC | 1 | 39.3 / 55.5 / 69.0 | n/a | n/a | n/a |
| limit10_ob | ADBC | 8 | 257.6 / 375.8 / 396.7 | n/a | n/a | n/a |
| limit10_ob | ADBC | 32 | 1113.8 / 1754.5 / 1890.0 | n/a | n/a | n/a |
| meta_tables | JDBC | 1 | 9.8 / 15.0 / 20.9 | n/a | n/a | n/a |
| meta_tables | JDBC | 8 | 17.1 / 507.6 / 752.0 | n/a | n/a | n/a |
| meta_tables | JDBC | 32 | 34.9 / 1315.8 / 2122.3 | n/a | n/a | n/a |
| meta_tables | ADBC | 1 | 8.6 / 12.9 / 15.9 | n/a | n/a | n/a |
| meta_tables | ADBC | 8 | 37.0 / 61.6 / 79.0 | n/a | n/a | n/a |
| meta_tables | ADBC | 32 | 122.9 / 1957.0 / 2857.4 | n/a | n/a | n/a |
| meta_schemas | JDBC | 1 | 7.1 / 15.2 / 22.7 | n/a | n/a | n/a |
| meta_schemas | JDBC | 8 | 13.4 / 28.4 / 38.1 | n/a | n/a | n/a |
| meta_schemas | JDBC | 32 | 27.6 / 68.6 / 217.3 | n/a | n/a | n/a |
| meta_schemas | ADBC | 1 | 5.8 / 9.5 / 12.1 | n/a | n/a | n/a |
| meta_schemas | ADBC | 8 | 23.2 / 42.9 / 47.5 | n/a | n/a | n/a |
| meta_schemas | ADBC | 32 | 64.4 / 151.0 / 284.6 | n/a | n/a | n/a |

Answers per class are compared across servers in the run summary (`summary.md`, correctness gate).

### Scans (`SELECT * FROM tpch.lineitem`, SF10, MB/s of Arrow buffers) and server peak RSS

| metric | ours-new | ours-27f5 | up-native | up-main | ours-new vs best upstream |
|---|---|---|---|---|---|
| raw Flight, 1 stream | 426 | n/a | n/a | n/a | n/a |
| raw Flight, 4 streams | 436 | n/a | n/a | n/a | n/a |
| raw Flight, 8 streams | 410 | n/a | n/a | n/a | n/a |
| full export over ADBC | 505 | n/a | n/a | n/a | n/a |
| server peak RSS (MB) | 1693 | n/a | n/a | n/a | - |

### Server container (docker stats every ~5 s, all workloads of this setting)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| CPU % p50 (200 = both cores) | 199 | n/a | n/a | n/a |
| CPU % max | 206 | n/a | n/a | n/a |
| memory peak (MiB, limit 6144) | 4921 | n/a | n/a | n/a |
| OOM-killed rounds | 0 / 9 | n/a | n/a | n/a |

## s3, setting `def`

### TPC-H SF10, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 9156 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 5692 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 23563 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 14086 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 26270 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 19601 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 30257 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 37609 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 35628 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 21816 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 4551 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 23051 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 9112 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 21586 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 22077 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 1950 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 28450 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 22629 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 23317 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 27189 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 53345 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 3243 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 464178 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF1, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 700 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 341 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1204 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 763 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 1212 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 1289 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 1469 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 1606 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 1651 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1114 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 256 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 1446 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 369 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 1125 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 986 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 129 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 1473 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 1329 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 1232 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 1221 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 2355 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 192 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 23462 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF10, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 8599 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 5439 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 23536 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 14893 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 30594 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 20698 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 30897 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 38546 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 35342 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 26313 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 4564 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 25986 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 6983 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 22344 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 21541 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 1949 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 29364 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 28194 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 24567 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 27899 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 53397 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 3197 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 484842 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### TPC-H SF1, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 721 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 583 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1273 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 845 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 1210 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 1161 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 1528 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 1830 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 1791 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1224 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 290 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 1277 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 378 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 1156 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 952 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 159 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 1458 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 1392 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 1244 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 1251 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 2362 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 157 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 24242 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### Small queries (ms, p50 / p95 / p99 over all rounds)

| class | client | c | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|---|---|
| point_orders | JDBC | 1 | 29.0 / 36.9 / 43.6 | n/a | n/a | n/a |
| point_orders | JDBC | 8 | 500.9 / 840.2 / 956.3 | n/a | n/a | n/a |
| point_orders | JDBC | 32 | 1572.5 / 3253.7 / 8076.6 | n/a | n/a | n/a |
| point_orders | ADBC | 1 | 21.9 / 38.5 / 42.6 | n/a | n/a | n/a |
| point_orders | ADBC | 8 | 459.9 / 813.9 / 982.5 | n/a | n/a | n/a |
| point_orders | ADBC | 32 | 1903.2 / 3204.0 / 3691.9 | n/a | n/a | n/a |
| point_lineitem | JDBC | 1 | 24.9 / 42.7 / 46.4 | n/a | n/a | n/a |
| point_lineitem | JDBC | 8 | 296.4 / 509.2 / 672.0 | n/a | n/a | n/a |
| point_lineitem | JDBC | 32 | 943.7 / 16563.1 / 27602.4 | n/a | n/a | n/a |
| point_lineitem | ADBC | 1 | 16.4 / 35.2 / 42.6 | n/a | n/a | n/a |
| point_lineitem | ADBC | 8 | 297.2 / 602.2 / 5459.6 | n/a | n/a | n/a |
| point_lineitem | ADBC | 32 | 1052.8 / 2007.1 / 35438.3 | n/a | n/a | n/a |
| count_filter | JDBC | 1 | 777.0 / 866.9 / 889.4 | n/a | n/a | n/a |
| count_filter | JDBC | 8 | 5872.1 / 12070.7 / 15350.6 | n/a | n/a | n/a |
| count_filter | JDBC | 32 | 17730.5 / 33348.8 / 40898.1 | n/a | n/a | n/a |
| count_filter | ADBC | 1 | 756.3 / 848.2 / 888.1 | n/a | n/a | n/a |
| count_filter | ADBC | 8 | 5729.5 / 8432.0 / 9013.7 | n/a | n/a | n/a |
| count_filter | ADBC | 32 | 20533.3 / 30554.5 / 61846.5 | n/a | n/a | n/a |
| limit10_ob | JDBC | 1 | 124.5 / 187.4 / 194.3 | n/a | n/a | n/a |
| limit10_ob | JDBC | 8 | 932.7 / 1581.8 / 1746.7 | n/a | n/a | n/a |
| limit10_ob | JDBC | 32 | 2948.2 / 5506.3 / 9734.3 | n/a | n/a | n/a |
| limit10_ob | ADBC | 1 | 128.2 / 171.5 / 193.4 | n/a | n/a | n/a |
| limit10_ob | ADBC | 8 | 966.3 / 1549.6 / 7560.3 | n/a | n/a | n/a |
| limit10_ob | ADBC | 32 | 3440.2 / 5372.3 / 6004.7 | n/a | n/a | n/a |
| meta_tables | JDBC | 1 | 8.6 / 12.0 / 18.4 | n/a | n/a | n/a |
| meta_tables | JDBC | 8 | 5.1 / 12.3 / 20.7 | n/a | n/a | n/a |
| meta_tables | JDBC | 32 | 5.8 / 23.9 / 39.0 | n/a | n/a | n/a |
| meta_tables | ADBC | 1 | 7.6 / 12.7 / 13.5 | n/a | n/a | n/a |
| meta_tables | ADBC | 8 | 7.1 / 17.0 / 22.5 | n/a | n/a | n/a |
| meta_tables | ADBC | 32 | 14.6 / 37.9 / 62.7 | n/a | n/a | n/a |
| meta_schemas | JDBC | 1 | 5.6 / 10.6 / 12.5 | n/a | n/a | n/a |
| meta_schemas | JDBC | 8 | 3.9 / 11.0 / 24.8 | n/a | n/a | n/a |
| meta_schemas | JDBC | 32 | 4.8 / 25.0 / 41.4 | n/a | n/a | n/a |
| meta_schemas | ADBC | 1 | 4.7 / 9.0 / 13.0 | n/a | n/a | n/a |
| meta_schemas | ADBC | 8 | 4.9 / 11.7 / 17.3 | n/a | n/a | n/a |
| meta_schemas | ADBC | 32 | 10.0 / 38.6 / 65.5 | n/a | n/a | n/a |

Answers per class are compared across servers in the run summary (`summary.md`, correctness gate).

### Scans (`SELECT * FROM tpch.lineitem`, SF10, MB/s of Arrow buffers) and server peak RSS

| metric | ours-new | ours-27f5 | up-native | up-main | ours-new vs best upstream |
|---|---|---|---|---|---|
| raw Flight, 1 stream | 395 | n/a | n/a | n/a | n/a |
| raw Flight, 4 streams | 445 | n/a | n/a | n/a | n/a |
| raw Flight, 8 streams | 434 | n/a | n/a | n/a | n/a |
| full export over ADBC | 445 | n/a | n/a | n/a | n/a |
| server peak RSS (MB) | 2689 | n/a | n/a | n/a | - |

### Server container (docker stats every ~5 s, all workloads of this setting)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| CPU % p50 (200 = both cores) | 29 | n/a | n/a | n/a |
| CPU % max | 205 | n/a | n/a | n/a |
| memory peak (MiB, limit 6144) | 2788 | n/a | n/a | n/a |
| OOM-killed rounds | 0 / 12 | n/a | n/a | n/a |

