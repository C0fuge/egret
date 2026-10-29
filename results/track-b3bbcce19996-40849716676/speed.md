# Server comparison - Report 1: SPEED (compare run 40849716676)

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
| JVM `b3bbcce19996` `def` | `--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED -Darrowflight.plugins.dir=/app/plugins -Darrowflight.duckdb.extensionDir=/ext/duckdb-home/extensions -DduckDbAllowUnsignedExtensions=true -Ds3Endpoint=http://127.0.0.1:9000 -Ds3UrlStyle=path -Ds3Region=us-east-1 -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf10 -cp --port --localhost --hosts` |
| JVM `ours-new` `def` | `--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED -Darrowflight.plugins.dir=/app/plugins -Darrowflight.duckdb.extensionDir=/ext/duckdb-home/extensions -DduckDbAllowUnsignedExtensions=true -Ds3Endpoint=http://127.0.0.1:9000 -Ds3UrlStyle=path -Ds3Region=us-east-1 -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf10 -cp --port --localhost --hosts` |

Times are warm medians in ms (median over rounds of the per-round warm median). **n/a** = not run, failed or wrong
answer (reason in the notes). Last column: same-runner ratio best-upstream / ours-new (> 1 = ours-new faster).

## local, setting `def`

### TPC-H SF10, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 1596 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 260 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1373 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 647 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 1113 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 502 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 1093 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 1385 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 2925 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1237 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 238 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 649 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 1917 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 801 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 707 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 375 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 1093 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 1984 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 1101 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 940 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 4282 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 387 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 26605 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF1, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 200 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 42 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 114 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 74 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 110 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 63 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 117 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 139 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 211 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 151 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 31 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 78 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 193 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 93 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 65 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 49 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 110 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 219 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 121 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 93 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 307 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 70 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 2650 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF10, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 1562 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 255 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 972 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 638 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 1132 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 485 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 1046 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 1372 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 2838 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1232 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 234 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 615 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 1868 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 774 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 668 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 362 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 1075 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 1975 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 1083 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 929 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 4214 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 395 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 25724 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### TPC-H SF1, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 205 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 49 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 112 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 80 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 118 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 68 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 121 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 156 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 214 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 150 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 38 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 84 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 190 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 91 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 70 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 61 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 116 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 231 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 123 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 94 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 325 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 54 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 2750 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### Small queries (ms, p50 / p95 / p99 over all rounds)

| class | client | c | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|---|---|
| point_orders | JDBC | 1 | 16.9 / 23.4 / 25.4 | n/a | n/a | n/a |
| point_orders | JDBC | 8 | 84.3 / 135.2 / 160.8 | n/a | n/a | n/a |
| point_orders | JDBC | 32 | 341.5 / 687.9 / 895.0 | n/a | n/a | n/a |
| point_orders | ADBC | 1 | 12.0 / 18.8 / 20.3 | n/a | n/a | n/a |
| point_orders | ADBC | 8 | 70.0 / 110.0 / 141.3 | n/a | n/a | n/a |
| point_orders | ADBC | 32 | 298.3 / 650.6 / 847.4 | n/a | n/a | n/a |
| point_lineitem | JDBC | 1 | 23.5 / 32.5 / 44.1 | n/a | n/a | n/a |
| point_lineitem | JDBC | 8 | 141.4 / 213.7 / 303.9 | n/a | n/a | n/a |
| point_lineitem | JDBC | 32 | 617.8 / 1062.6 / 1546.7 | n/a | n/a | n/a |
| point_lineitem | ADBC | 1 | 17.8 / 27.9 / 30.6 | n/a | n/a | n/a |
| point_lineitem | ADBC | 8 | 131.2 / 202.5 / 223.7 | n/a | n/a | n/a |
| point_lineitem | ADBC | 32 | 546.1 / 924.7 / 1187.3 | n/a | n/a | n/a |
| count_filter | JDBC | 1 | 36.7 / 48.2 / 53.1 | n/a | n/a | n/a |
| count_filter | JDBC | 8 | 170.7 / 222.0 / 236.6 | n/a | n/a | n/a |
| count_filter | JDBC | 32 | 700.1 / 1077.4 / 1266.5 | n/a | n/a | n/a |
| count_filter | ADBC | 1 | 31.6 / 41.9 / 47.1 | n/a | n/a | n/a |
| count_filter | ADBC | 8 | 172.2 / 235.5 / 267.1 | n/a | n/a | n/a |
| count_filter | ADBC | 32 | 655.1 / 1392.8 / 1626.6 | n/a | n/a | n/a |
| limit10_ob | JDBC | 1 | 34.6 / 45.6 / 56.5 | n/a | n/a | n/a |
| limit10_ob | JDBC | 8 | 209.7 / 294.2 / 359.6 | n/a | n/a | n/a |
| limit10_ob | JDBC | 32 | 872.2 / 1337.9 / 1542.0 | n/a | n/a | n/a |
| limit10_ob | ADBC | 1 | 28.8 / 41.8 / 50.1 | n/a | n/a | n/a |
| limit10_ob | ADBC | 8 | 215.1 / 299.0 / 339.6 | n/a | n/a | n/a |
| limit10_ob | ADBC | 32 | 838.6 / 1385.3 / 1718.6 | n/a | n/a | n/a |
| meta_tables | JDBC | 1 | 5.8 / 8.3 / 9.4 | n/a | n/a | n/a |
| meta_tables | JDBC | 8 | 10.7 / 23.8 / 31.0 | n/a | n/a | n/a |
| meta_tables | JDBC | 32 | 21.0 / 56.7 / 151.3 | n/a | n/a | n/a |
| meta_tables | ADBC | 1 | 5.4 / 7.1 / 7.7 | n/a | n/a | n/a |
| meta_tables | ADBC | 8 | 23.7 / 356.7 / 621.7 | n/a | n/a | n/a |
| meta_tables | ADBC | 32 | 66.1 / 184.6 / 1480.4 | n/a | n/a | n/a |
| meta_schemas | JDBC | 1 | 4.2 / 6.8 / 7.5 | n/a | n/a | n/a |
| meta_schemas | JDBC | 8 | 9.3 / 21.9 / 26.7 | n/a | n/a | n/a |
| meta_schemas | JDBC | 32 | 18.9 / 48.1 / 66.4 | n/a | n/a | n/a |
| meta_schemas | ADBC | 1 | 3.2 / 5.1 / 6.5 | n/a | n/a | n/a |
| meta_schemas | ADBC | 8 | 15.7 / 31.9 / 41.5 | n/a | n/a | n/a |
| meta_schemas | ADBC | 32 | 37.3 / 88.0 / 199.7 | n/a | n/a | n/a |

Answers per class are compared across servers in the run summary (`summary.md`, correctness gate).

### Scans (`SELECT * FROM tpch.lineitem`, SF10, MB/s of Arrow buffers) and server peak RSS

| metric | ours-new | ours-27f5 | up-native | up-main | ours-new vs best upstream |
|---|---|---|---|---|---|
| raw Flight, 1 stream | 533 | n/a | n/a | n/a | n/a |
| raw Flight, 4 streams | 565 | n/a | n/a | n/a | n/a |
| raw Flight, 8 streams | 505 | n/a | n/a | n/a | n/a |
| full export over ADBC | 638 | n/a | n/a | n/a | n/a |
| server peak RSS (MB) | 1704 | n/a | n/a | n/a | - |

### Server container (docker stats every ~5 s, all workloads of this setting)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| CPU % p50 (200 = both cores) | 201 | n/a | n/a | n/a |
| CPU % max | 204 | n/a | n/a | n/a |
| memory peak (MiB, limit 6144) | 1657 | n/a | n/a | n/a |
| OOM-killed rounds | 0 / 6 | n/a | n/a | n/a |

## s3, setting `def`

### TPC-H SF10, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 7635 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 3173 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 15772 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 8853 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 16818 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 12202 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 17170 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 24567 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 19843 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 19820 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 3362 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 21747 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 4390 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 14983 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 12772 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 1298 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 18601 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 15201 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 17110 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 17472 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 39054 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 1714 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 313557 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF1, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 809 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 393 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1442 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 900 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 1397 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 1254 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 1641 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 1902 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 1995 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1334 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 299 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 1506 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 387 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 1345 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 1105 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 116 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 1745 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 1446 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 1410 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 1445 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 2652 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 203 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 26726 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF10, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 6921 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 3296 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 12551 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 8425 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 14213 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 11333 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 16275 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 18833 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 19737 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 12165 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 2507 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 14105 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 5502 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 17594 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 17183 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 1532 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 23638 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 17896 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 18352 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 21785 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 43493 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 2537 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 309873 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### TPC-H SF1, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 787 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 390 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1395 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 896 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 1443 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 1247 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 1585 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 1963 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 1992 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1279 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 294 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 1514 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 381 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 1291 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 1110 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 139 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 1704 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 1448 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 1361 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 1441 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 2600 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 196 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 26456 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### Small queries (ms, p50 / p95 / p99 over all rounds)

| class | client | c | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|---|---|
| point_orders | JDBC | 1 | 31.2 / 40.2 / 45.3 | n/a | n/a | n/a |
| point_orders | JDBC | 8 | 440.3 / 842.4 / 981.6 | n/a | n/a | n/a |
| point_orders | JDBC | 32 | 1706.8 / 3167.3 / 4135.8 | n/a | n/a | n/a |
| point_orders | ADBC | 1 | 22.1 / 73.7 / 81.1 | n/a | n/a | n/a |
| point_orders | ADBC | 8 | 485.8 / 840.1 / 949.7 | n/a | n/a | n/a |
| point_orders | ADBC | 32 | 1851.6 / 3610.4 / 5487.8 | n/a | n/a | n/a |
| point_lineitem | JDBC | 1 | 26.5 / 45.6 / 48.1 | n/a | n/a | n/a |
| point_lineitem | JDBC | 8 | 276.5 / 506.8 / 657.8 | n/a | n/a | n/a |
| point_lineitem | JDBC | 32 | 944.0 / 4096.2 / 19738.7 | n/a | n/a | n/a |
| point_lineitem | ADBC | 1 | 18.2 / 49.8 / 1131.2 | n/a | n/a | n/a |
| point_lineitem | ADBC | 8 | 302.5 / 582.9 / 6694.9 | n/a | n/a | n/a |
| point_lineitem | ADBC | 32 | 1085.3 / 18524.1 / 29688.1 | n/a | n/a | n/a |
| count_filter | JDBC | 1 | 845.4 / 918.0 / 946.8 | n/a | n/a | n/a |
| count_filter | JDBC | 8 | 6341.7 / 7995.4 / 8431.8 | n/a | n/a | n/a |
| count_filter | JDBC | 32 | 18342.8 / 28934.6 / 30182.0 | n/a | n/a | n/a |
| count_filter | ADBC | 1 | 842.0 / 1246.0 / 1359.1 | n/a | n/a | n/a |
| count_filter | ADBC | 8 | 6080.4 / 9567.7 / 13894.6 | n/a | n/a | n/a |
| count_filter | ADBC | 32 | 21417.3 / 31259.3 / 37642.4 | n/a | n/a | n/a |
| limit10_ob | JDBC | 1 | 134.7 / 176.3 / 184.8 | n/a | n/a | n/a |
| limit10_ob | JDBC | 8 | 899.5 / 1438.0 / 1817.4 | n/a | n/a | n/a |
| limit10_ob | JDBC | 32 | 3271.3 / 5510.0 / 18912.7 | n/a | n/a | n/a |
| limit10_ob | ADBC | 1 | 142.3 / 193.5 / 1138.2 | n/a | n/a | n/a |
| limit10_ob | ADBC | 8 | 988.7 / 1697.1 / 2138.6 | n/a | n/a | n/a |
| limit10_ob | ADBC | 32 | 3621.8 / 6134.3 / 27983.6 | n/a | n/a | n/a |
| meta_tables | JDBC | 1 | 8.3 / 12.3 / 13.3 | n/a | n/a | n/a |
| meta_tables | JDBC | 8 | 5.5 / 13.0 / 16.8 | n/a | n/a | n/a |
| meta_tables | JDBC | 32 | 6.6 / 20.4 / 41.9 | n/a | n/a | n/a |
| meta_tables | ADBC | 1 | 7.4 / 16.3 / 21.4 | n/a | n/a | n/a |
| meta_tables | ADBC | 8 | 8.4 / 27.6 / 34.6 | n/a | n/a | n/a |
| meta_tables | ADBC | 32 | 18.2 / 49.0 / 68.6 | n/a | n/a | n/a |
| meta_schemas | JDBC | 1 | 6.9 / 10.5 / 12.6 | n/a | n/a | n/a |
| meta_schemas | JDBC | 8 | 4.4 / 13.0 / 17.5 | n/a | n/a | n/a |
| meta_schemas | JDBC | 32 | 4.9 / 21.4 / 57.6 | n/a | n/a | n/a |
| meta_schemas | ADBC | 1 | 4.9 / 8.0 / 10.5 | n/a | n/a | n/a |
| meta_schemas | ADBC | 8 | 5.7 / 17.1 / 21.6 | n/a | n/a | n/a |
| meta_schemas | ADBC | 32 | 12.2 / 39.0 / 75.0 | n/a | n/a | n/a |

Answers per class are compared across servers in the run summary (`summary.md`, correctness gate).

### Scans (`SELECT * FROM tpch.lineitem`, SF10, MB/s of Arrow buffers) and server peak RSS

| metric | ours-new | ours-27f5 | up-native | up-main | ours-new vs best upstream |
|---|---|---|---|---|---|
| raw Flight, 1 stream | 386 | n/a | n/a | n/a | n/a |
| raw Flight, 4 streams | 421 | n/a | n/a | n/a | n/a |
| raw Flight, 8 streams | 400 | n/a | n/a | n/a | n/a |
| full export over ADBC | 428 | n/a | n/a | n/a | n/a |
| server peak RSS (MB) | 2640 | n/a | n/a | n/a | - |

### Server container (docker stats every ~5 s, all workloads of this setting)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| CPU % p50 (200 = both cores) | 32 | n/a | n/a | n/a |
| CPU % max | 205 | n/a | n/a | n/a |
| memory peak (MiB, limit 6144) | 2428 | n/a | n/a | n/a |
| OOM-killed rounds | 0 / 12 | n/a | n/a | n/a |

