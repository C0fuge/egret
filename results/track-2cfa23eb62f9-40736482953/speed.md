# Server comparison - Report 1: SPEED (compare run 40736482953)

## Experiment setup

| item | value |
|---|---|
| runner | GitHub-hosted `ubuntu-latest`: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor; Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor; Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor; Linux ubuntu24 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C; Linux ubuntu24 4 vCPU Intel(R) Xeon(R) 6973P-C; RAM 15982 MB; kernel 7.0.0-1017-azure; JDK Temurin 21 |
| containers | every server: `eclipse-temurin:21-jre`, `--cpus=2 --cpuset-cpus=0,1 --memory=6g --memory-swap=6g`, JVM `-Xmx3g -XX:MaxDirectMemorySize=2g`, `MALLOC_ARENA_MAX=4`, host network; clients (JDBC/ADBC/Flight runners, jcmd sampling) and the S3 server in their own containers on cpus 2,3 |
| servers | ours-new = `7562a5bdb7b9` (DuckDB v1.5.6); ours-27f5 = `27f583adccd7` (DuckDB ?); up-native = `1de5f6b4b218f83f01a3adf2708af5f36f80811b` (DuckDB ?); up-main = `dbacd8d585bce2ef2a449c821fe3a53cc6060b57` (DuckDB ?) |
| data | TPC-H SF1 and SF10, DuckDB dbgen, Parquet, 8 files per big table, 122880-row row groups, one data dir `tpch.*` per SF |
| storage | local disk (`file://`, page-cached) and S3 (`rclone serve s3` on the same runner, path style) |
| pairs | every job: ours-new (side A) vs one other server (side B) on the same runner, rounds A B / B A / A B (3), 1 cold run (warm-up) + warm runs per query (SF1 2 warm, SF10 1 warm per round) |
| settings | `def` = each server's default (`duckDbThreads` ours 4, upstream 2); `t8` = `-DduckDbThreads=8` on both |
| batch size | server defaults (not overridden) |
| clients | TPC-H: Python ADBC Flight SQL 1.12.0 (pyarrow 26), Flight SQL JDBC 18.0.0; small queries: same; scans: raw Flight (Arrow Java), ADBC export |
| correctness | TPC-H over ADBC: rows + checksum per query equal to in-process DuckDB on the same files; over JDBC: the result rows compared numerically with the same reference (numbers within a relative 1.5e-9, i.e. two 10-digit roundings; the JDBC runner prints DECIMAL as an exact plain BigDecimal, the reference as %.10g) |
| upstream on S3 | up-native: `s3a://` data dir (Hadoop S3A from its `docker/hadoop-aws` recipe for listing, DuckDB httpfs for scans, `FLIGHT_S3_*` settings); up-main: **n/a**, main at the fork point has no S3 settings (no `FLIGHT_S3_*`, no S3A dependencies) |
| SF30 | not run: SF1+SF10 already fill most of the repo's 10 GB Actions cache, SF30 Parquet (~11 GB) does not fit; generating it per job costs ~20 min of each 4-vCPU runner |
| JVM `2cfa23eb62f9` `def` | `--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED -Darrowflight.plugins.dir=/app/plugins -Darrowflight.duckdb.extensionDir=/ext/duckdb-home/extensions -DduckDbAllowUnsignedExtensions=true -Ds3Endpoint=http://127.0.0.1:9000 -Ds3UrlStyle=path -Ds3Region=us-east-1 -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf10 -cp --port --localhost --hosts` |
| JVM `ours-new` `def` | `--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED -Darrowflight.plugins.dir=/app/plugins -Darrowflight.duckdb.extensionDir=/ext/duckdb-home/extensions -DduckDbAllowUnsignedExtensions=true -Ds3Endpoint=http://127.0.0.1:9000 -Ds3UrlStyle=path -Ds3Region=us-east-1 -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf10 -cp --port --localhost --hosts` |

Times are warm medians in ms (median over rounds of the per-round warm median). **n/a** = not run, failed or wrong
answer (reason in the notes). Last column: same-runner ratio best-upstream / ours-new (> 1 = ours-new faster).

## local, setting `def`

### TPC-H SF10, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 1891 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 329 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1215 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 843 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 1431 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 641 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 1400 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 1678 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 3493 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1567 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 298 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 815 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 2577 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 1006 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 931 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 494 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 1358 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 2524 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 1356 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 1186 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 4744 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 511 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 32288 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF1, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 246 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 50 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 148 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 93 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 136 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 85 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 163 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 177 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 276 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 198 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 39 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 99 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 242 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 114 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 75 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 68 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 136 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 279 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 154 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 121 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 391 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 82 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 3372 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF10, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 1912 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 340 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1244 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 855 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 1445 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 621 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 1375 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 1667 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 3419 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1568 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 306 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 834 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 2596 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 998 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 885 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 500 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 1403 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 2521 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 1410 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 1144 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 4845 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 485 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 32373 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### TPC-H SF1, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 261 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 63 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 137 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 104 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 150 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 90 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 159 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 181 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 285 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 181 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 48 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 104 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 238 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 117 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 82 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 77 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 146 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 291 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 151 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 124 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 385 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 61 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 3435 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### Small queries (ms, p50 / p95 / p99 over all rounds)

| class | client | c | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|---|---|
| point_orders | JDBC | 1 | 20.3 / 28.8 / 31.1 | n/a | n/a | n/a |
| point_orders | JDBC | 8 | 100.4 / 168.9 / 304.5 | n/a | n/a | n/a |
| point_orders | JDBC | 32 | 395.0 / 786.5 / 1076.6 | n/a | n/a | n/a |
| point_orders | ADBC | 1 | 14.4 / 25.5 / 33.6 | n/a | n/a | n/a |
| point_orders | ADBC | 8 | 80.9 / 130.7 / 149.1 | n/a | n/a | n/a |
| point_orders | ADBC | 32 | 346.5 / 636.7 / 754.1 | n/a | n/a | n/a |
| point_lineitem | JDBC | 1 | 26.6 / 36.9 / 38.6 | n/a | n/a | n/a |
| point_lineitem | JDBC | 8 | 154.0 / 249.9 / 416.1 | n/a | n/a | n/a |
| point_lineitem | JDBC | 32 | 636.9 / 1098.6 / 1527.4 | n/a | n/a | n/a |
| point_lineitem | ADBC | 1 | 20.6 / 30.0 / 33.9 | n/a | n/a | n/a |
| point_lineitem | ADBC | 8 | 134.4 / 193.6 / 224.8 | n/a | n/a | n/a |
| point_lineitem | ADBC | 32 | 617.6 / 979.9 / 1221.8 | n/a | n/a | n/a |
| count_filter | JDBC | 1 | 41.2 / 52.2 / 55.2 | n/a | n/a | n/a |
| count_filter | JDBC | 8 | 194.9 / 245.1 / 271.2 | n/a | n/a | n/a |
| count_filter | JDBC | 32 | 780.7 / 1225.1 / 1499.4 | n/a | n/a | n/a |
| count_filter | ADBC | 1 | 35.6 / 48.8 / 67.3 | n/a | n/a | n/a |
| count_filter | ADBC | 8 | 198.2 / 258.3 / 287.5 | n/a | n/a | n/a |
| count_filter | ADBC | 32 | 735.0 / 1092.1 / 1335.4 | n/a | n/a | n/a |
| limit10_ob | JDBC | 1 | 39.1 / 53.9 / 59.0 | n/a | n/a | n/a |
| limit10_ob | JDBC | 8 | 233.9 / 302.5 / 331.7 | n/a | n/a | n/a |
| limit10_ob | JDBC | 32 | 949.3 / 1467.0 / 1655.7 | n/a | n/a | n/a |
| limit10_ob | ADBC | 1 | 32.9 / 48.1 / 52.7 | n/a | n/a | n/a |
| limit10_ob | ADBC | 8 | 237.9 / 339.5 / 408.9 | n/a | n/a | n/a |
| limit10_ob | ADBC | 32 | 925.9 / 1421.0 / 1650.3 | n/a | n/a | n/a |
| meta_tables | JDBC | 1 | 7.0 / 12.0 / 25.3 | n/a | n/a | n/a |
| meta_tables | JDBC | 8 | 11.5 / 25.3 / 30.5 | n/a | n/a | n/a |
| meta_tables | JDBC | 32 | 28.0 / 1289.5 / 1810.7 | n/a | n/a | n/a |
| meta_tables | ADBC | 1 | 7.1 / 10.4 / 11.8 | n/a | n/a | n/a |
| meta_tables | ADBC | 8 | 29.9 / 372.0 / 647.7 | n/a | n/a | n/a |
| meta_tables | ADBC | 32 | 71.9 / 144.3 / 202.4 | n/a | n/a | n/a |
| meta_schemas | JDBC | 1 | 5.6 / 9.0 / 9.3 | n/a | n/a | n/a |
| meta_schemas | JDBC | 8 | 11.0 / 24.2 / 33.2 | n/a | n/a | n/a |
| meta_schemas | JDBC | 32 | 21.1 / 56.1 / 126.8 | n/a | n/a | n/a |
| meta_schemas | ADBC | 1 | 4.7 / 7.5 / 11.1 | n/a | n/a | n/a |
| meta_schemas | ADBC | 8 | 17.3 / 34.2 / 40.6 | n/a | n/a | n/a |
| meta_schemas | ADBC | 32 | 43.7 / 95.0 / 225.1 | n/a | n/a | n/a |

Answers per class are compared across servers in the run summary (`summary.md`, correctness gate).

### Scans (`SELECT * FROM tpch.lineitem`, SF10, MB/s of Arrow buffers) and server peak RSS

| metric | ours-new | ours-27f5 | up-native | up-main | ours-new vs best upstream |
|---|---|---|---|---|---|
| raw Flight, 1 stream | 454 | n/a | n/a | n/a | n/a |
| raw Flight, 4 streams | 489 | n/a | n/a | n/a | n/a |
| raw Flight, 8 streams | 445 | n/a | n/a | n/a | n/a |
| full export over ADBC | 490 | n/a | n/a | n/a | n/a |
| server peak RSS (MB) | 1708 | n/a | n/a | n/a | - |

### Server container (docker stats every ~5 s, all workloads of this setting)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| CPU % p50 (200 = both cores) | 200 | n/a | n/a | n/a |
| CPU % max | 203 | n/a | n/a | n/a |
| memory peak (MiB, limit 6144) | 1637 | n/a | n/a | n/a |
| OOM-killed rounds | 0 / 6 | n/a | n/a | n/a |

## s3, setting `def`

### TPC-H SF10, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 7276 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 3290 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 14167 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 8325 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 14791 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 11152 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 16570 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 20212 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 23998 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 13575 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 2559 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 18380 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 7094 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 11965 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 17470 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 1655 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 23599 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 17811 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 18645 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 21817 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 43295 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 2305 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 319951 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF1, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 694 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 404 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 2094 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 935 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 1342 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 1082 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 1384 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 1856 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 1648 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1160 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 313 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 1285 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 615 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 1425 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 1005 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 146 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 1705 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 1475 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 1224 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 1439 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 3704 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 172 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 27107 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF10, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 7231 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 3301 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 13107 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 8363 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 14643 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 11750 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 16675 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 20422 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 19387 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 17514 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 3742 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 20347 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 5606 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 17708 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 17534 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 1628 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 23897 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 19176 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 19136 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 26802 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 44048 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 2644 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 334661 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### TPC-H SF1, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 865 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 675 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1220 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 801 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 1369 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 1005 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 1415 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 2204 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 1767 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1353 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 367 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 1427 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 414 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 1072 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 909 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 176 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 1503 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 1498 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 1462 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 1336 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 2228 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 157 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 25223 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### Small queries (ms, p50 / p95 / p99 over all rounds)

| class | client | c | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|---|---|
| point_orders | JDBC | 1 | 30.5 / 41.4 / 50.7 | n/a | n/a | n/a |
| point_orders | JDBC | 8 | 406.1 / 757.1 / 1347.7 | n/a | n/a | n/a |
| point_orders | JDBC | 32 | 1557.3 / 3392.8 / 8302.0 | n/a | n/a | n/a |
| point_orders | ADBC | 1 | 22.0 / 37.1 / 38.9 | n/a | n/a | n/a |
| point_orders | ADBC | 8 | 467.8 / 769.1 / 992.0 | n/a | n/a | n/a |
| point_orders | ADBC | 32 | 1676.1 / 3031.8 / 3943.8 | n/a | n/a | n/a |
| point_lineitem | JDBC | 1 | 24.0 / 43.8 / 50.2 | n/a | n/a | n/a |
| point_lineitem | JDBC | 8 | 248.6 / 447.3 / 532.4 | n/a | n/a | n/a |
| point_lineitem | JDBC | 32 | 928.1 / 15888.4 / 24721.4 | n/a | n/a | n/a |
| point_lineitem | ADBC | 1 | 17.1 / 25.7 / 38.5 | n/a | n/a | n/a |
| point_lineitem | ADBC | 8 | 298.8 / 559.9 / 8952.7 | n/a | n/a | n/a |
| point_lineitem | ADBC | 32 | 904.6 / 10988.5 / 20994.3 | n/a | n/a | n/a |
| count_filter | JDBC | 1 | 758.1 / 876.7 / 915.1 | n/a | n/a | n/a |
| count_filter | JDBC | 8 | 5570.9 / 8032.4 / 10923.3 | n/a | n/a | n/a |
| count_filter | JDBC | 32 | 20219.4 / 34210.1 / 40572.7 | n/a | n/a | n/a |
| count_filter | ADBC | 1 | 758.1 / 855.6 / 881.8 | n/a | n/a | n/a |
| count_filter | ADBC | 8 | 5815.4 / 8420.3 / 8784.0 | n/a | n/a | n/a |
| count_filter | ADBC | 32 | 18592.3 / 33174.3 / 53703.2 | n/a | n/a | n/a |
| limit10_ob | JDBC | 1 | 124.4 / 164.5 / 183.0 | n/a | n/a | n/a |
| limit10_ob | JDBC | 8 | 849.8 / 1259.3 / 1363.7 | n/a | n/a | n/a |
| limit10_ob | JDBC | 32 | 2979.3 / 5690.6 / 22142.0 | n/a | n/a | n/a |
| limit10_ob | ADBC | 1 | 119.1 / 178.2 / 182.4 | n/a | n/a | n/a |
| limit10_ob | ADBC | 8 | 965.0 / 1545.4 / 3635.9 | n/a | n/a | n/a |
| limit10_ob | ADBC | 32 | 3091.7 / 5588.3 / 15402.7 | n/a | n/a | n/a |
| meta_tables | JDBC | 1 | 8.0 / 12.6 / 16.3 | n/a | n/a | n/a |
| meta_tables | JDBC | 8 | 5.0 / 13.7 / 23.5 | n/a | n/a | n/a |
| meta_tables | JDBC | 32 | 5.7 / 20.5 / 40.7 | n/a | n/a | n/a |
| meta_tables | ADBC | 1 | 7.2 / 11.5 / 14.8 | n/a | n/a | n/a |
| meta_tables | ADBC | 8 | 8.1 / 28.1 / 36.6 | n/a | n/a | n/a |
| meta_tables | ADBC | 32 | 17.0 / 46.0 / 69.9 | n/a | n/a | n/a |
| meta_schemas | JDBC | 1 | 5.4 / 8.9 / 9.3 | n/a | n/a | n/a |
| meta_schemas | JDBC | 8 | 4.1 / 12.8 / 20.7 | n/a | n/a | n/a |
| meta_schemas | JDBC | 32 | 5.6 / 21.0 / 45.9 | n/a | n/a | n/a |
| meta_schemas | ADBC | 1 | 4.8 / 8.2 / 10.1 | n/a | n/a | n/a |
| meta_schemas | ADBC | 8 | 5.3 / 17.9 / 21.8 | n/a | n/a | n/a |
| meta_schemas | ADBC | 32 | 11.4 / 35.6 / 69.3 | n/a | n/a | n/a |

Answers per class are compared across servers in the run summary (`summary.md`, correctness gate).

### Scans (`SELECT * FROM tpch.lineitem`, SF10, MB/s of Arrow buffers) and server peak RSS

| metric | ours-new | ours-27f5 | up-native | up-main | ours-new vs best upstream |
|---|---|---|---|---|---|
| raw Flight, 1 stream | 392 | n/a | n/a | n/a | n/a |
| raw Flight, 4 streams | 451 | n/a | n/a | n/a | n/a |
| raw Flight, 8 streams | 423 | n/a | n/a | n/a | n/a |
| full export over ADBC | 412 | n/a | n/a | n/a | n/a |
| server peak RSS (MB) | 2630 | n/a | n/a | n/a | - |

### Server container (docker stats every ~5 s, all workloads of this setting)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| CPU % p50 (200 = both cores) | 29 | n/a | n/a | n/a |
| CPU % max | 206 | n/a | n/a | n/a |
| memory peak (MiB, limit 6144) | 2488 | n/a | n/a | n/a |
| OOM-killed rounds | 0 / 12 | n/a | n/a | n/a |

