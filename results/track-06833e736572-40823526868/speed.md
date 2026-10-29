# Server comparison - Report 1: SPEED (compare run 40823526868)

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
| JVM `06833e736572` `def` | `--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED -Darrowflight.plugins.dir=/app/plugins -Darrowflight.duckdb.extensionDir=/ext/duckdb-home/extensions -DduckDbAllowUnsignedExtensions=true -Ds3Endpoint=http://127.0.0.1:9000 -Ds3UrlStyle=path -Ds3Region=us-east-1 -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf10 -cp --port --localhost --hosts` |
| JVM `ours-new` `def` | `--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED -Darrowflight.plugins.dir=/app/plugins -Darrowflight.duckdb.extensionDir=/ext/duckdb-home/extensions -DduckDbAllowUnsignedExtensions=true -Ds3Endpoint=http://127.0.0.1:9000 -Ds3UrlStyle=path -Ds3Region=us-east-1 -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf10 -cp --port --localhost --hosts` |

Times are warm medians in ms (median over rounds of the per-round warm median). **n/a** = not run, failed or wrong
answer (reason in the notes). Last column: same-runner ratio best-upstream / ours-new (> 1 = ours-new faster).

## local, setting `def`

### TPC-H SF10, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 2664 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 397 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1519 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 1008 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 1723 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 748 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 1668 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 2042 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 4284 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1859 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 387 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 1029 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 2912 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 1227 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 1076 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 575 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 1721 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 3151 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 1696 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 1434 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 5828 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 611 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 39559 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF1, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 342 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 58 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 178 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 136 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 170 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 97 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 182 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 208 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 320 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 219 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 46 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 118 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 313 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 139 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 98 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 77 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 167 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 366 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 182 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 146 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 492 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 71 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 4125 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF10, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 2695 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 403 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1608 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 1012 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 1749 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 755 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 1697 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 2119 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 4229 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1896 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 363 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 1030 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 2885 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 1209 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 1092 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 593 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 1733 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 3772 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 1677 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 1410 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 5676 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 618 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 40221 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### TPC-H SF1, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 353 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 71 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 176 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 124 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 181 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 107 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 179 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 217 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 320 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 228 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 55 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 133 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 297 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 139 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 96 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 91 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 168 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 368 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 182 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 147 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 494 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 76 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 4202 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### Small queries (ms, p50 / p95 / p99 over all rounds)

| class | client | c | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|---|---|
| point_orders | JDBC | 1 | 25.0 / 36.9 / 39.0 | n/a | n/a | n/a |
| point_orders | JDBC | 8 | 119.9 / 191.2 / 358.2 | n/a | n/a | n/a |
| point_orders | JDBC | 32 | 508.5 / 935.3 / 1427.5 | n/a | n/a | n/a |
| point_orders | ADBC | 1 | 16.6 / 26.9 / 30.7 | n/a | n/a | n/a |
| point_orders | ADBC | 8 | 101.3 / 159.7 / 185.0 | n/a | n/a | n/a |
| point_orders | ADBC | 32 | 381.5 / 738.1 / 867.4 | n/a | n/a | n/a |
| point_lineitem | JDBC | 1 | 33.1 / 44.0 / 46.9 | n/a | n/a | n/a |
| point_lineitem | JDBC | 8 | 181.7 / 268.9 / 420.0 | n/a | n/a | n/a |
| point_lineitem | JDBC | 32 | 737.8 / 1290.7 / 1783.5 | n/a | n/a | n/a |
| point_lineitem | ADBC | 1 | 24.5 / 35.7 / 45.7 | n/a | n/a | n/a |
| point_lineitem | ADBC | 8 | 175.7 / 259.8 / 299.6 | n/a | n/a | n/a |
| point_lineitem | ADBC | 32 | 700.5 / 1145.1 / 1319.5 | n/a | n/a | n/a |
| count_filter | JDBC | 1 | 48.5 / 64.9 / 78.8 | n/a | n/a | n/a |
| count_filter | JDBC | 8 | 237.9 / 285.9 / 325.0 | n/a | n/a | n/a |
| count_filter | JDBC | 32 | 882.5 / 1440.8 / 2070.3 | n/a | n/a | n/a |
| count_filter | ADBC | 1 | 42.3 / 52.2 / 53.6 | n/a | n/a | n/a |
| count_filter | ADBC | 8 | 219.4 / 286.3 / 317.8 | n/a | n/a | n/a |
| count_filter | ADBC | 32 | 854.4 / 1299.5 / 1515.3 | n/a | n/a | n/a |
| limit10_ob | JDBC | 1 | 43.8 / 54.2 / 62.6 | n/a | n/a | n/a |
| limit10_ob | JDBC | 8 | 262.0 / 369.3 / 463.1 | n/a | n/a | n/a |
| limit10_ob | JDBC | 32 | 1061.2 / 1683.4 / 2279.6 | n/a | n/a | n/a |
| limit10_ob | ADBC | 1 | 38.4 / 56.8 / 61.6 | n/a | n/a | n/a |
| limit10_ob | ADBC | 8 | 254.7 / 349.0 / 385.3 | n/a | n/a | n/a |
| limit10_ob | ADBC | 32 | 1056.9 / 1791.5 / 2132.2 | n/a | n/a | n/a |
| meta_tables | JDBC | 1 | 7.8 / 14.7 / 21.0 | n/a | n/a | n/a |
| meta_tables | JDBC | 8 | 14.6 / 41.6 / 603.8 | n/a | n/a | n/a |
| meta_tables | JDBC | 32 | 36.4 / 1448.3 / 2327.0 | n/a | n/a | n/a |
| meta_tables | ADBC | 1 | 7.9 / 10.2 / 11.5 | n/a | n/a | n/a |
| meta_tables | ADBC | 8 | 34.3 / 56.7 / 65.3 | n/a | n/a | n/a |
| meta_tables | ADBC | 32 | 109.2 / 1824.5 / 2672.9 | n/a | n/a | n/a |
| meta_schemas | JDBC | 1 | 6.1 / 10.9 / 18.1 | n/a | n/a | n/a |
| meta_schemas | JDBC | 8 | 12.7 / 26.8 / 30.9 | n/a | n/a | n/a |
| meta_schemas | JDBC | 32 | 24.3 / 75.2 / 147.9 | n/a | n/a | n/a |
| meta_schemas | ADBC | 1 | 4.9 / 6.6 / 8.5 | n/a | n/a | n/a |
| meta_schemas | ADBC | 8 | 22.8 / 40.6 / 49.3 | n/a | n/a | n/a |
| meta_schemas | ADBC | 32 | 57.4 / 138.9 / 2416.8 | n/a | n/a | n/a |

Answers per class are compared across servers in the run summary (`summary.md`, correctness gate).

### Scans (`SELECT * FROM tpch.lineitem`, SF10, MB/s of Arrow buffers) and server peak RSS

| metric | ours-new | ours-27f5 | up-native | up-main | ours-new vs best upstream |
|---|---|---|---|---|---|
| raw Flight, 1 stream | 436 | n/a | n/a | n/a | n/a |
| raw Flight, 4 streams | 460 | n/a | n/a | n/a | n/a |
| raw Flight, 8 streams | 420 | n/a | n/a | n/a | n/a |
| full export over ADBC | 532 | n/a | n/a | n/a | n/a |
| server peak RSS (MB) | 1727 | n/a | n/a | n/a | - |

### Server container (docker stats every ~5 s, all workloads of this setting)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| CPU % p50 (200 = both cores) | 201 | n/a | n/a | n/a |
| CPU % max | 205 | n/a | n/a | n/a |
| memory peak (MiB, limit 6144) | 1700 | n/a | n/a | n/a |
| OOM-killed rounds | 0 / 6 | n/a | n/a | n/a |

## s3, setting `def`

### TPC-H SF10, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 8563 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 3700 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 22551 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 13800 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 25902 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 19987 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 30453 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 37456 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 34360 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 21803 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 4701 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 25147 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 6884 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 21462 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 20738 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 1975 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 28408 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 22510 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 23961 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 26689 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 52401 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 3042 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 456493 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF1, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 812 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 385 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1535 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 904 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 1441 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 1292 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 1711 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 2012 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 2083 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1425 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 341 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 1644 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 377 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 1344 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 1120 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 118 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 1736 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 1551 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 1470 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 1500 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 2805 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 187 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 27793 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF10, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 6763 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 3381 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 19428 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 9741 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 16406 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 13024 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 17105 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 22361 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 19758 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 11216 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 2617 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 17719 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 4083 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 14307 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 11036 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 1285 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 16788 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 13900 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 13986 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 19096 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 29786 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 1633 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 285419 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### TPC-H SF1, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 816 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 400 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1496 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 903 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 1387 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 1298 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 1753 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 2141 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 2055 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1464 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 333 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 1599 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 370 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 1400 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 1114 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 136 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 1760 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 1492 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 1484 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 1557 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 2797 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 178 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 27933 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### Small queries (ms, p50 / p95 / p99 over all rounds)

| class | client | c | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|---|---|
| point_orders | JDBC | 1 | 24.5 / 36.3 / 40.2 | n/a | n/a | n/a |
| point_orders | JDBC | 8 | 336.0 / 535.3 / 686.5 | n/a | n/a | n/a |
| point_orders | JDBC | 32 | 1308.4 / 2144.1 / 2832.2 | n/a | n/a | n/a |
| point_orders | ADBC | 1 | 18.8 / 42.6 / 63.1 | n/a | n/a | n/a |
| point_orders | ADBC | 8 | 332.9 / 503.7 / 629.8 | n/a | n/a | n/a |
| point_orders | ADBC | 32 | 1309.7 / 2214.2 / 2734.3 | n/a | n/a | n/a |
| point_lineitem | JDBC | 1 | 20.2 / 73.1 / 638.3 | n/a | n/a | n/a |
| point_lineitem | JDBC | 8 | 188.5 / 892.0 / 5531.3 | n/a | n/a | n/a |
| point_lineitem | JDBC | 32 | 602.8 / 1117.0 / 1419.0 | n/a | n/a | n/a |
| point_lineitem | ADBC | 1 | 15.5 / 35.5 / 531.7 | n/a | n/a | n/a |
| point_lineitem | ADBC | 8 | 179.7 / 306.7 / 386.1 | n/a | n/a | n/a |
| point_lineitem | ADBC | 32 | 648.2 / 8666.6 / 21586.4 | n/a | n/a | n/a |
| count_filter | JDBC | 1 | 675.6 / 758.3 / 779.1 | n/a | n/a | n/a |
| count_filter | JDBC | 8 | 3641.9 / 4137.3 / 4243.7 | n/a | n/a | n/a |
| count_filter | JDBC | 32 | 13103.2 / 22061.6 / 27808.5 | n/a | n/a | n/a |
| count_filter | ADBC | 1 | 692.7 / 786.7 / 898.6 | n/a | n/a | n/a |
| count_filter | ADBC | 8 | 3710.8 / 4179.5 / 4353.4 | n/a | n/a | n/a |
| count_filter | ADBC | 32 | 12385.8 / 14436.9 / 15414.4 | n/a | n/a | n/a |
| limit10_ob | JDBC | 1 | 110.6 / 161.0 / 687.1 | n/a | n/a | n/a |
| limit10_ob | JDBC | 8 | 610.7 / 887.3 / 2917.4 | n/a | n/a | n/a |
| limit10_ob | JDBC | 32 | 2362.0 / 3481.1 / 4119.3 | n/a | n/a | n/a |
| limit10_ob | ADBC | 1 | 107.1 / 144.1 / 157.1 | n/a | n/a | n/a |
| limit10_ob | ADBC | 8 | 616.3 / 863.4 / 970.0 | n/a | n/a | n/a |
| limit10_ob | ADBC | 32 | 2362.9 / 3430.6 / 6164.4 | n/a | n/a | n/a |
| meta_tables | JDBC | 1 | 6.3 / 9.5 / 11.0 | n/a | n/a | n/a |
| meta_tables | JDBC | 8 | 4.9 / 11.1 / 18.4 | n/a | n/a | n/a |
| meta_tables | JDBC | 32 | 5.7 / 17.8 / 31.6 | n/a | n/a | n/a |
| meta_tables | ADBC | 1 | 5.5 / 8.2 / 11.9 | n/a | n/a | n/a |
| meta_tables | ADBC | 8 | 7.5 / 25.4 / 28.9 | n/a | n/a | n/a |
| meta_tables | ADBC | 32 | 17.5 / 46.2 / 57.4 | n/a | n/a | n/a |
| meta_schemas | JDBC | 1 | 4.3 / 6.3 / 9.4 | n/a | n/a | n/a |
| meta_schemas | JDBC | 8 | 3.5 / 9.7 / 11.7 | n/a | n/a | n/a |
| meta_schemas | JDBC | 32 | 4.8 / 17.0 / 39.6 | n/a | n/a | n/a |
| meta_schemas | ADBC | 1 | 3.0 / 7.0 / 7.8 | n/a | n/a | n/a |
| meta_schemas | ADBC | 8 | 4.5 / 16.2 / 20.8 | n/a | n/a | n/a |
| meta_schemas | ADBC | 32 | 11.1 / 34.5 / 61.3 | n/a | n/a | n/a |

Answers per class are compared across servers in the run summary (`summary.md`, correctness gate).

### Scans (`SELECT * FROM tpch.lineitem`, SF10, MB/s of Arrow buffers) and server peak RSS

| metric | ours-new | ours-27f5 | up-native | up-main | ours-new vs best upstream |
|---|---|---|---|---|---|
| raw Flight, 1 stream | 569 | n/a | n/a | n/a | n/a |
| raw Flight, 4 streams | 641 | n/a | n/a | n/a | n/a |
| raw Flight, 8 streams | 606 | n/a | n/a | n/a | n/a |
| full export over ADBC | 533 | n/a | n/a | n/a | n/a |
| server peak RSS (MB) | 2858 | n/a | n/a | n/a | - |

### Server container (docker stats every ~5 s, all workloads of this setting)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| CPU % p50 (200 = both cores) | 29 | n/a | n/a | n/a |
| CPU % max | 206 | n/a | n/a | n/a |
| memory peak (MiB, limit 6144) | 2653 | n/a | n/a | n/a |
| OOM-killed rounds | 0 / 12 | n/a | n/a | n/a |

