# Server comparison - Report 1: SPEED (compare run 40772221252)

## Experiment setup

| item | value |
|---|---|
| runner | GitHub-hosted `ubuntu-latest`: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor; Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor; Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor; RAM 15983 MB; kernel 7.0.0-1017-azure; JDK Temurin 21 |
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
| JVM `9044653333cd` `def` | `--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED -Darrowflight.plugins.dir=/app/plugins -Darrowflight.duckdb.extensionDir=/ext/duckdb-home/extensions -DduckDbAllowUnsignedExtensions=true -Ds3Endpoint=http://127.0.0.1:9000 -Ds3UrlStyle=path -Ds3Region=us-east-1 -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf10 -cp --port --localhost --hosts` |
| JVM `ours-new` `def` | `--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED -Darrowflight.plugins.dir=/app/plugins -Darrowflight.duckdb.extensionDir=/ext/duckdb-home/extensions -DduckDbAllowUnsignedExtensions=true -Ds3Endpoint=http://127.0.0.1:9000 -Ds3UrlStyle=path -Ds3Region=us-east-1 -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf10 -cp --port --localhost --hosts` |

Times are warm medians in ms (median over rounds of the per-round warm median). **n/a** = not run, failed or wrong
answer (reason in the notes). Last column: same-runner ratio best-upstream / ours-new (> 1 = ours-new faster).

## local, setting `def`

### TPC-H SF10, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 2678 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 416 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1614 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 1025 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 1768 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 754 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 1737 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 2086 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 4302 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1898 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 362 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 1032 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 2961 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 1231 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 1105 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 572 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 1746 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 3265 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 1691 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 1441 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 5832 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 601 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 40117 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF1, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 345 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 76 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 176 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 117 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 176 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 93 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 179 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 211 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 315 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 225 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 46 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 128 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 306 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 140 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 96 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 79 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 167 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 367 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 185 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 153 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 486 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 77 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 4143 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF10, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 2711 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 411 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1573 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 1027 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 1763 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 760 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 1724 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 2115 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 4219 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1909 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 367 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 1038 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 2932 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 1216 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 1121 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 620 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 1814 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 4047 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 1691 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 1445 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 5834 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 647 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 40984 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### TPC-H SF1, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 355 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 71 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 169 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 124 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 177 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 106 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 184 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 219 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 311 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 235 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 61 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 121 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 297 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 143 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 101 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 99 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 166 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 372 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 186 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 150 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 464 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 70 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 4181 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### Small queries (ms, p50 / p95 / p99 over all rounds)

| class | client | c | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|---|---|
| point_orders | JDBC | 1 | 17.1 / 26.0 / 38.8 | n/a | n/a | n/a |
| point_orders | JDBC | 8 | 79.9 / 133.3 / 188.2 | n/a | n/a | n/a |
| point_orders | JDBC | 32 | 319.8 / 605.0 / 760.6 | n/a | n/a | n/a |
| point_orders | ADBC | 1 | 10.7 / 19.8 / 28.0 | n/a | n/a | n/a |
| point_orders | ADBC | 8 | 64.9 / 109.8 / 133.3 | n/a | n/a | n/a |
| point_orders | ADBC | 32 | 256.3 / 594.6 / 802.5 | n/a | n/a | n/a |
| point_lineitem | JDBC | 1 | 23.4 / 36.1 / 38.0 | n/a | n/a | n/a |
| point_lineitem | JDBC | 8 | 126.2 / 195.7 / 298.6 | n/a | n/a | n/a |
| point_lineitem | JDBC | 32 | 532.0 / 883.4 / 1054.4 | n/a | n/a | n/a |
| point_lineitem | ADBC | 1 | 15.6 / 27.9 / 33.8 | n/a | n/a | n/a |
| point_lineitem | ADBC | 8 | 112.4 / 171.5 / 209.4 | n/a | n/a | n/a |
| point_lineitem | ADBC | 32 | 482.1 / 849.6 / 1034.2 | n/a | n/a | n/a |
| count_filter | JDBC | 1 | 32.7 / 42.3 / 46.7 | n/a | n/a | n/a |
| count_filter | JDBC | 8 | 137.0 / 193.9 / 241.5 | n/a | n/a | n/a |
| count_filter | JDBC | 32 | 561.2 / 904.7 / 1224.7 | n/a | n/a | n/a |
| count_filter | ADBC | 1 | 26.7 / 38.0 / 43.0 | n/a | n/a | n/a |
| count_filter | ADBC | 8 | 137.3 / 185.2 / 209.6 | n/a | n/a | n/a |
| count_filter | ADBC | 32 | 510.3 / 1001.0 / 1345.1 | n/a | n/a | n/a |
| limit10_ob | JDBC | 1 | 30.7 / 44.0 / 53.9 | n/a | n/a | n/a |
| limit10_ob | JDBC | 8 | 181.0 / 263.2 / 316.7 | n/a | n/a | n/a |
| limit10_ob | JDBC | 32 | 780.9 / 1199.2 / 1423.2 | n/a | n/a | n/a |
| limit10_ob | ADBC | 1 | 24.5 / 44.6 / 51.6 | n/a | n/a | n/a |
| limit10_ob | ADBC | 8 | 176.6 / 251.0 / 309.4 | n/a | n/a | n/a |
| limit10_ob | ADBC | 32 | 725.2 / 1300.8 / 1613.5 | n/a | n/a | n/a |
| meta_tables | JDBC | 1 | 6.4 / 10.7 / 19.9 | n/a | n/a | n/a |
| meta_tables | JDBC | 8 | 11.1 / 26.0 / 31.5 | n/a | n/a | n/a |
| meta_tables | JDBC | 32 | 27.9 / 70.7 / 95.1 | n/a | n/a | n/a |
| meta_tables | ADBC | 1 | 5.3 / 7.9 / 11.3 | n/a | n/a | n/a |
| meta_tables | ADBC | 8 | 25.4 / 57.4 / 504.0 | n/a | n/a | n/a |
| meta_tables | ADBC | 32 | 74.1 / 1274.6 / 1772.8 | n/a | n/a | n/a |
| meta_schemas | JDBC | 1 | 4.8 / 8.4 / 10.7 | n/a | n/a | n/a |
| meta_schemas | JDBC | 8 | 9.6 / 24.8 / 29.5 | n/a | n/a | n/a |
| meta_schemas | JDBC | 32 | 24.0 / 68.0 / 107.3 | n/a | n/a | n/a |
| meta_schemas | ADBC | 1 | 3.1 / 5.5 / 5.9 | n/a | n/a | n/a |
| meta_schemas | ADBC | 8 | 16.3 / 31.9 / 38.4 | n/a | n/a | n/a |
| meta_schemas | ADBC | 32 | 39.1 / 81.9 / 130.2 | n/a | n/a | n/a |

Answers per class are compared across servers in the run summary (`summary.md`, correctness gate).

### Scans (`SELECT * FROM tpch.lineitem`, SF10, MB/s of Arrow buffers) and server peak RSS

| metric | ours-new | ours-27f5 | up-native | up-main | ours-new vs best upstream |
|---|---|---|---|---|---|
| raw Flight, 1 stream | 638 | n/a | n/a | n/a | n/a |
| raw Flight, 4 streams | 667 | n/a | n/a | n/a | n/a |
| raw Flight, 8 streams | 617 | n/a | n/a | n/a | n/a |
| full export over ADBC | 776 | n/a | n/a | n/a | n/a |
| server peak RSS (MB) | 1737 | n/a | n/a | n/a | - |

### Server container (docker stats every ~5 s, all workloads of this setting)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| CPU % p50 (200 = both cores) | 201 | n/a | n/a | n/a |
| CPU % max | 205 | n/a | n/a | n/a |
| memory peak (MiB, limit 6144) | 4460 | n/a | n/a | n/a |
| OOM-killed rounds | 0 / 9 | n/a | n/a | n/a |

## s3, setting `def`

### TPC-H SF10, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 7337 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 3507 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 12379 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 7504 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 14270 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 11382 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 15507 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 18534 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 18630 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 11042 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 2354 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 13023 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 3646 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 17424 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 11208 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 1520 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 16426 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 11997 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 15734 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 14731 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 30137 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 2019 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 260311 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF1, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 697 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 367 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1259 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 817 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 1302 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 1142 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 1523 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 1704 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 1720 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1153 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 276 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 1326 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 305 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 1144 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 1042 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 137 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 1487 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 1323 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 1340 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 1262 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 2463 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 174 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 23963 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF10, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 7976 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 3373 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 13710 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 10089 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 15936 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 12772 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 18079 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 19428 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 24739 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 14857 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 3059 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 15392 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 3798 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 12287 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 12397 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 1837 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 26414 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 18628 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 16216 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 21836 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 42054 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 2695 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 317572 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### TPC-H SF1, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 666 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 354 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1342 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 817 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 1268 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 1092 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 1455 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 1706 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 1778 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1222 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 285 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 1482 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 305 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 1148 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 955 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 169 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 1544 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 1383 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 1296 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 1336 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 2469 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 158 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 24230 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### Small queries (ms, p50 / p95 / p99 over all rounds)

| class | client | c | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|---|---|
| point_orders | JDBC | 1 | 33.7 / 45.6 / 52.9 | n/a | n/a | n/a |
| point_orders | JDBC | 8 | 359.7 / 700.3 / 930.6 | n/a | n/a | n/a |
| point_orders | JDBC | 32 | 1547.8 / 2749.2 / 7633.6 | n/a | n/a | n/a |
| point_orders | ADBC | 1 | 24.8 / 49.6 / 78.9 | n/a | n/a | n/a |
| point_orders | ADBC | 8 | 347.3 / 631.0 / 787.8 | n/a | n/a | n/a |
| point_orders | ADBC | 32 | 1649.7 / 3105.6 / 4193.3 | n/a | n/a | n/a |
| point_lineitem | JDBC | 1 | 27.5 / 93.4 / 642.2 | n/a | n/a | n/a |
| point_lineitem | JDBC | 8 | 227.3 / 397.4 / 480.7 | n/a | n/a | n/a |
| point_lineitem | JDBC | 32 | 862.3 / 15203.5 / 24658.0 | n/a | n/a | n/a |
| point_lineitem | ADBC | 1 | 20.8 / 102.7 / 1263.5 | n/a | n/a | n/a |
| point_lineitem | ADBC | 8 | 209.8 / 392.9 / 461.6 | n/a | n/a | n/a |
| point_lineitem | ADBC | 32 | 884.3 / 1993.7 / 18440.5 | n/a | n/a | n/a |
| count_filter | JDBC | 1 | 659.9 / 745.1 / 767.7 | n/a | n/a | n/a |
| count_filter | JDBC | 8 | 5377.0 / 6848.3 / 11525.8 | n/a | n/a | n/a |
| count_filter | JDBC | 32 | 16232.3 / 26365.1 / 33725.2 | n/a | n/a | n/a |
| count_filter | ADBC | 1 | 646.6 / 1106.0 / 1190.3 | n/a | n/a | n/a |
| count_filter | ADBC | 8 | 5386.0 / 6173.3 / 6439.8 | n/a | n/a | n/a |
| count_filter | ADBC | 32 | 18215.7 / 44299.1 / 57882.4 | n/a | n/a | n/a |
| limit10_ob | JDBC | 1 | 117.9 / 194.0 / 1063.2 | n/a | n/a | n/a |
| limit10_ob | JDBC | 8 | 744.0 / 1125.7 / 1229.7 | n/a | n/a | n/a |
| limit10_ob | JDBC | 32 | 2805.0 / 9172.7 / 27444.7 | n/a | n/a | n/a |
| limit10_ob | ADBC | 1 | 127.4 / 187.0 / 712.1 | n/a | n/a | n/a |
| limit10_ob | ADBC | 8 | 719.3 / 1072.6 / 1231.3 | n/a | n/a | n/a |
| limit10_ob | ADBC | 32 | 2984.3 / 5325.7 / 9977.2 | n/a | n/a | n/a |
| meta_tables | JDBC | 1 | 8.8 / 13.7 / 20.4 | n/a | n/a | n/a |
| meta_tables | JDBC | 8 | 6.1 / 13.7 / 22.0 | n/a | n/a | n/a |
| meta_tables | JDBC | 32 | 5.8 / 23.5 / 54.4 | n/a | n/a | n/a |
| meta_tables | ADBC | 1 | 8.0 / 13.2 / 17.4 | n/a | n/a | n/a |
| meta_tables | ADBC | 8 | 9.9 / 28.0 / 31.0 | n/a | n/a | n/a |
| meta_tables | ADBC | 32 | 16.3 / 43.2 / 65.8 | n/a | n/a | n/a |
| meta_schemas | JDBC | 1 | 6.5 / 9.9 / 12.0 | n/a | n/a | n/a |
| meta_schemas | JDBC | 8 | 4.6 / 16.5 / 25.6 | n/a | n/a | n/a |
| meta_schemas | JDBC | 32 | 5.7 / 27.5 / 52.7 | n/a | n/a | n/a |
| meta_schemas | ADBC | 1 | 5.0 / 8.1 / 9.1 | n/a | n/a | n/a |
| meta_schemas | ADBC | 8 | 5.9 / 18.5 / 23.2 | n/a | n/a | n/a |
| meta_schemas | ADBC | 32 | 12.1 / 40.8 / 80.9 | n/a | n/a | n/a |

Answers per class are compared across servers in the run summary (`summary.md`, correctness gate).

### Scans (`SELECT * FROM tpch.lineitem`, SF10, MB/s of Arrow buffers) and server peak RSS

| metric | ours-new | ours-27f5 | up-native | up-main | ours-new vs best upstream |
|---|---|---|---|---|---|
| raw Flight, 1 stream | 399 | n/a | n/a | n/a | n/a |
| raw Flight, 4 streams | 442 | n/a | n/a | n/a | n/a |
| raw Flight, 8 streams | 438 | n/a | n/a | n/a | n/a |
| full export over ADBC | 439 | n/a | n/a | n/a | n/a |
| server peak RSS (MB) | 2781 | n/a | n/a | n/a | - |

### Server container (docker stats every ~5 s, all workloads of this setting)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| CPU % p50 (200 = both cores) | 32 | n/a | n/a | n/a |
| CPU % max | 207 | n/a | n/a | n/a |
| memory peak (MiB, limit 6144) | 2542 | n/a | n/a | n/a |
| OOM-killed rounds | 0 / 12 | n/a | n/a | n/a |

