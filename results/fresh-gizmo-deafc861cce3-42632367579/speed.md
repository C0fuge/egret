# Server comparison - Report 1: SPEED (compare run 42632367579)

## Experiment setup

| item | value |
|---|---|
| runner | GitHub-hosted `ubuntu-latest`: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor; Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor; Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor; Linux ubuntu26 4 vCPU Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz; RAM 15983 MB; kernel 7.0.0-1019-azure; JDK Temurin 21 |
| containers | **no-container reference run**: server in `eclipse-temurin:21-jdk` with an 8 GB memory limit and no CPU limit, clients on the runner host; not the reported numbers |
| servers | ours-new = `7562a5bdb7b9` (DuckDB ?); ours-27f5 = `27f583adccd7` (DuckDB ?); up-native = `caa12d3c64aeb03252ad4905072f53f754cf19cd` (DuckDB ?); up-main = `dbacd8d585bce2ef2a449c821fe3a53cc6060b57` (DuckDB ?) |
| data | TPC-H SF1 and SF10, DuckDB dbgen, Parquet, 8 files per big table, 122880-row row groups, one data dir `tpch.*` per SF |
| storage | local disk (`file://`, page-cached) and S3 (`rclone serve s3` on the same runner, path style) |
| pairs | every job: ours-new (side A) vs one other server (side B) on the same runner, rounds A B / B A / A B (3), 1 cold run (warm-up) + warm runs per query (SF1 2 warm, SF10 1 warm per round) |
| settings | `def` = each server's default (`duckDbThreads` ours 4, upstream 2); `t8` = `-DduckDbThreads=8` on both |
| batch size | server defaults (not overridden) |
| clients | TPC-H: Python ADBC Flight SQL 1.12.0 (pyarrow 26), Flight SQL JDBC 18.0.0; small queries: same; scans: raw Flight (Arrow Java), ADBC export |
| correctness | TPC-H over ADBC: rows + checksum per query equal to in-process DuckDB on the same files; over JDBC: the result rows compared numerically with the same reference (numbers within a relative 1.5e-9, i.e. two 10-digit roundings; the JDBC runner prints DECIMAL as an exact plain BigDecimal, the reference as %.10g) |
| upstream on S3 | up-native: `s3a://` data dir (Hadoop S3A from its `docker/hadoop-aws` recipe for listing, DuckDB httpfs for scans, `FLIGHT_S3_*` settings); up-main: **n/a**, main at the fork point has no S3 settings (no `FLIGHT_S3_*`, no S3A dependencies) |
| SF30 | not run: SF1+SF10 already fill most of the repo's 10 GB Actions cache, SF30 Parquet (~11 GB) does not fit; generating it per job costs ~20 min of each 4-vCPU runner |
| JVM `deafc861cce3` `def` | `--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED -Darrowflight.plugins.dir=/app/plugins -Darrowflight.duckdb.extensionDir=/ext/duckdb-home/extensions -DduckDbAllowUnsignedExtensions=true -Ds3Endpoint=http://127.0.0.1:9000 -Ds3UrlStyle=path -Ds3Region=us-east-1 -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf10 -DresourceProfile=speed -cp --port --localhost --hosts` |
| JVM `gizmo` `def` | `--backend --port --init-sql-commands-file` |

Times are warm medians in ms (median over rounds of the per-round warm median). **n/a** = not run, failed or wrong
answer (reason in the notes). Last column: same-runner ratio best-upstream / ours-new (> 1 = ours-new faster).

## local, setting `def`

### TPC-H SF10, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | n/a | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | n/a | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | n/a | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | n/a | n/a | n/a | n/a | n/a |
| q05 | 6-way join | n/a | n/a | n/a | n/a | n/a |
| q06 | selective scan | n/a | n/a | n/a | n/a | n/a |
| q07 | joins, group by | n/a | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | n/a | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | n/a | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | n/a | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | n/a | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | n/a | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | n/a | n/a | n/a | n/a | n/a |
| q14 | join, CASE | n/a | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | n/a | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | n/a | n/a | n/a | n/a | n/a |
| q17 | correlated avg | n/a | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | n/a | n/a | n/a | n/a | n/a |
| q19 | OR predicates | n/a | n/a | n/a | n/a | n/a |
| q20 | nested IN | n/a | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | n/a | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | n/a | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | n/a | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-new: not run: not in this setting's jobs
- ours-27f5: not run: not in this setting's jobs
- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF1, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | n/a | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | n/a | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | n/a | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | n/a | n/a | n/a | n/a | n/a |
| q05 | 6-way join | n/a | n/a | n/a | n/a | n/a |
| q06 | selective scan | n/a | n/a | n/a | n/a | n/a |
| q07 | joins, group by | n/a | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | n/a | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | n/a | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | n/a | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | n/a | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | n/a | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | n/a | n/a | n/a | n/a | n/a |
| q14 | join, CASE | n/a | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | n/a | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | n/a | n/a | n/a | n/a | n/a |
| q17 | correlated avg | n/a | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | n/a | n/a | n/a | n/a | n/a |
| q19 | OR predicates | n/a | n/a | n/a | n/a | n/a |
| q20 | nested IN | n/a | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | n/a | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | n/a | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | n/a | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-new: not run: not in this setting's jobs
- ours-27f5: not run: not in this setting's jobs
- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF10, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | n/a | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | n/a | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | n/a | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | n/a | n/a | n/a | n/a | n/a |
| q05 | 6-way join | n/a | n/a | n/a | n/a | n/a |
| q06 | selective scan | n/a | n/a | n/a | n/a | n/a |
| q07 | joins, group by | n/a | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | n/a | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | n/a | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | n/a | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | n/a | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | n/a | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | n/a | n/a | n/a | n/a | n/a |
| q14 | join, CASE | n/a | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | n/a | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | n/a | n/a | n/a | n/a | n/a |
| q17 | correlated avg | n/a | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | n/a | n/a | n/a | n/a | n/a |
| q19 | OR predicates | n/a | n/a | n/a | n/a | n/a |
| q20 | nested IN | n/a | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | n/a | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | n/a | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | n/a | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-new: not run: not in this setting's jobs
- ours-27f5: not run: not in this setting's jobs
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### TPC-H SF1, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | n/a | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | n/a | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | n/a | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | n/a | n/a | n/a | n/a | n/a |
| q05 | 6-way join | n/a | n/a | n/a | n/a | n/a |
| q06 | selective scan | n/a | n/a | n/a | n/a | n/a |
| q07 | joins, group by | n/a | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | n/a | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | n/a | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | n/a | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | n/a | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | n/a | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | n/a | n/a | n/a | n/a | n/a |
| q14 | join, CASE | n/a | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | n/a | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | n/a | n/a | n/a | n/a | n/a |
| q17 | correlated avg | n/a | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | n/a | n/a | n/a | n/a | n/a |
| q19 | OR predicates | n/a | n/a | n/a | n/a | n/a |
| q20 | nested IN | n/a | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | n/a | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | n/a | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | n/a | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-new: not run: not in this setting's jobs
- ours-27f5: not run: not in this setting's jobs
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### Small queries (ms, p50 / p95 / p99 over all rounds)

| class | client | c | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|---|---|
| point_orders | JDBC | 1 | n/a | n/a | n/a | n/a |
| point_orders | JDBC | 8 | n/a | n/a | n/a | n/a |
| point_orders | JDBC | 32 | n/a | n/a | n/a | n/a |
| point_orders | ADBC | 1 | n/a | n/a | n/a | n/a |
| point_orders | ADBC | 8 | n/a | n/a | n/a | n/a |
| point_orders | ADBC | 32 | n/a | n/a | n/a | n/a |
| point_lineitem | JDBC | 1 | n/a | n/a | n/a | n/a |
| point_lineitem | JDBC | 8 | n/a | n/a | n/a | n/a |
| point_lineitem | JDBC | 32 | n/a | n/a | n/a | n/a |
| point_lineitem | ADBC | 1 | n/a | n/a | n/a | n/a |
| point_lineitem | ADBC | 8 | n/a | n/a | n/a | n/a |
| point_lineitem | ADBC | 32 | n/a | n/a | n/a | n/a |
| count_filter | JDBC | 1 | n/a | n/a | n/a | n/a |
| count_filter | JDBC | 8 | n/a | n/a | n/a | n/a |
| count_filter | JDBC | 32 | n/a | n/a | n/a | n/a |
| count_filter | ADBC | 1 | n/a | n/a | n/a | n/a |
| count_filter | ADBC | 8 | n/a | n/a | n/a | n/a |
| count_filter | ADBC | 32 | n/a | n/a | n/a | n/a |
| limit10_ob | JDBC | 1 | n/a | n/a | n/a | n/a |
| limit10_ob | JDBC | 8 | n/a | n/a | n/a | n/a |
| limit10_ob | JDBC | 32 | n/a | n/a | n/a | n/a |
| limit10_ob | ADBC | 1 | n/a | n/a | n/a | n/a |
| limit10_ob | ADBC | 8 | n/a | n/a | n/a | n/a |
| limit10_ob | ADBC | 32 | n/a | n/a | n/a | n/a |
| meta_tables | JDBC | 1 | n/a | n/a | n/a | n/a |
| meta_tables | JDBC | 8 | n/a | n/a | n/a | n/a |
| meta_tables | JDBC | 32 | n/a | n/a | n/a | n/a |
| meta_tables | ADBC | 1 | n/a | n/a | n/a | n/a |
| meta_tables | ADBC | 8 | n/a | n/a | n/a | n/a |
| meta_tables | ADBC | 32 | n/a | n/a | n/a | n/a |
| meta_schemas | JDBC | 1 | n/a | n/a | n/a | n/a |
| meta_schemas | JDBC | 8 | n/a | n/a | n/a | n/a |
| meta_schemas | JDBC | 32 | n/a | n/a | n/a | n/a |
| meta_schemas | ADBC | 1 | n/a | n/a | n/a | n/a |
| meta_schemas | ADBC | 8 | n/a | n/a | n/a | n/a |
| meta_schemas | ADBC | 32 | n/a | n/a | n/a | n/a |

Answers per class are compared across servers in the run summary (`summary.md`, correctness gate).

### Scans (`SELECT * FROM tpch.lineitem`, SF10, MB/s of Arrow buffers) and server peak RSS

| metric | ours-new | ours-27f5 | up-native | up-main | ours-new vs best upstream |
|---|---|---|---|---|---|
| raw Flight, 1 stream | n/a | n/a | n/a | n/a | n/a |
| raw Flight, 4 streams | n/a | n/a | n/a | n/a | n/a |
| raw Flight, 8 streams | n/a | n/a | n/a | n/a | n/a |
| full export over ADBC | n/a | n/a | n/a | n/a | n/a |
| server peak RSS (MB) | n/a | n/a | n/a | n/a | - |

### Server container (docker stats every ~5 s, all workloads of this setting)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| CPU % p50 (200 = both cores) | n/a | n/a | n/a | n/a |
| CPU % max | n/a | n/a | n/a | n/a |
| memory peak (MiB, limit 6144) | n/a | n/a | n/a | n/a |
| OOM-killed rounds | n/a | n/a | n/a | n/a |

## s3, setting `def`

### TPC-H SF10, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | n/a | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | n/a | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | n/a | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | n/a | n/a | n/a | n/a | n/a |
| q05 | 6-way join | n/a | n/a | n/a | n/a | n/a |
| q06 | selective scan | n/a | n/a | n/a | n/a | n/a |
| q07 | joins, group by | n/a | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | n/a | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | n/a | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | n/a | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | n/a | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | n/a | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | n/a | n/a | n/a | n/a | n/a |
| q14 | join, CASE | n/a | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | n/a | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | n/a | n/a | n/a | n/a | n/a |
| q17 | correlated avg | n/a | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | n/a | n/a | n/a | n/a | n/a |
| q19 | OR predicates | n/a | n/a | n/a | n/a | n/a |
| q20 | nested IN | n/a | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | n/a | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | n/a | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | n/a | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-new: not run: not in this setting's jobs
- ours-27f5: not run: not in this setting's jobs
- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF1, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | n/a | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | n/a | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | n/a | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | n/a | n/a | n/a | n/a | n/a |
| q05 | 6-way join | n/a | n/a | n/a | n/a | n/a |
| q06 | selective scan | n/a | n/a | n/a | n/a | n/a |
| q07 | joins, group by | n/a | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | n/a | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | n/a | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | n/a | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | n/a | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | n/a | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | n/a | n/a | n/a | n/a | n/a |
| q14 | join, CASE | n/a | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | n/a | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | n/a | n/a | n/a | n/a | n/a |
| q17 | correlated avg | n/a | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | n/a | n/a | n/a | n/a | n/a |
| q19 | OR predicates | n/a | n/a | n/a | n/a | n/a |
| q20 | nested IN | n/a | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | n/a | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | n/a | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | n/a | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-new: not run: not in this setting's jobs
- ours-27f5: not run: not in this setting's jobs
- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF10, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | n/a | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | n/a | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | n/a | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | n/a | n/a | n/a | n/a | n/a |
| q05 | 6-way join | n/a | n/a | n/a | n/a | n/a |
| q06 | selective scan | n/a | n/a | n/a | n/a | n/a |
| q07 | joins, group by | n/a | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | n/a | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | n/a | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | n/a | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | n/a | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | n/a | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | n/a | n/a | n/a | n/a | n/a |
| q14 | join, CASE | n/a | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | n/a | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | n/a | n/a | n/a | n/a | n/a |
| q17 | correlated avg | n/a | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | n/a | n/a | n/a | n/a | n/a |
| q19 | OR predicates | n/a | n/a | n/a | n/a | n/a |
| q20 | nested IN | n/a | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | n/a | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | n/a | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | n/a | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-new: not run: not in this setting's jobs
- ours-27f5: not run: not in this setting's jobs
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### TPC-H SF1, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | n/a | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | n/a | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | n/a | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | n/a | n/a | n/a | n/a | n/a |
| q05 | 6-way join | n/a | n/a | n/a | n/a | n/a |
| q06 | selective scan | n/a | n/a | n/a | n/a | n/a |
| q07 | joins, group by | n/a | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | n/a | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | n/a | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | n/a | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | n/a | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | n/a | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | n/a | n/a | n/a | n/a | n/a |
| q14 | join, CASE | n/a | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | n/a | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | n/a | n/a | n/a | n/a | n/a |
| q17 | correlated avg | n/a | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | n/a | n/a | n/a | n/a | n/a |
| q19 | OR predicates | n/a | n/a | n/a | n/a | n/a |
| q20 | nested IN | n/a | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | n/a | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | n/a | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | n/a | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-new: not run: not in this setting's jobs
- ours-27f5: not run: not in this setting's jobs
- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### Small queries (ms, p50 / p95 / p99 over all rounds)

| class | client | c | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|---|---|
| point_orders | JDBC | 1 | n/a | n/a | n/a | n/a |
| point_orders | JDBC | 8 | n/a | n/a | n/a | n/a |
| point_orders | JDBC | 32 | n/a | n/a | n/a | n/a |
| point_orders | ADBC | 1 | n/a | n/a | n/a | n/a |
| point_orders | ADBC | 8 | n/a | n/a | n/a | n/a |
| point_orders | ADBC | 32 | n/a | n/a | n/a | n/a |
| point_lineitem | JDBC | 1 | n/a | n/a | n/a | n/a |
| point_lineitem | JDBC | 8 | n/a | n/a | n/a | n/a |
| point_lineitem | JDBC | 32 | n/a | n/a | n/a | n/a |
| point_lineitem | ADBC | 1 | n/a | n/a | n/a | n/a |
| point_lineitem | ADBC | 8 | n/a | n/a | n/a | n/a |
| point_lineitem | ADBC | 32 | n/a | n/a | n/a | n/a |
| count_filter | JDBC | 1 | n/a | n/a | n/a | n/a |
| count_filter | JDBC | 8 | n/a | n/a | n/a | n/a |
| count_filter | JDBC | 32 | n/a | n/a | n/a | n/a |
| count_filter | ADBC | 1 | n/a | n/a | n/a | n/a |
| count_filter | ADBC | 8 | n/a | n/a | n/a | n/a |
| count_filter | ADBC | 32 | n/a | n/a | n/a | n/a |
| limit10_ob | JDBC | 1 | n/a | n/a | n/a | n/a |
| limit10_ob | JDBC | 8 | n/a | n/a | n/a | n/a |
| limit10_ob | JDBC | 32 | n/a | n/a | n/a | n/a |
| limit10_ob | ADBC | 1 | n/a | n/a | n/a | n/a |
| limit10_ob | ADBC | 8 | n/a | n/a | n/a | n/a |
| limit10_ob | ADBC | 32 | n/a | n/a | n/a | n/a |
| meta_tables | JDBC | 1 | n/a | n/a | n/a | n/a |
| meta_tables | JDBC | 8 | n/a | n/a | n/a | n/a |
| meta_tables | JDBC | 32 | n/a | n/a | n/a | n/a |
| meta_tables | ADBC | 1 | n/a | n/a | n/a | n/a |
| meta_tables | ADBC | 8 | n/a | n/a | n/a | n/a |
| meta_tables | ADBC | 32 | n/a | n/a | n/a | n/a |
| meta_schemas | JDBC | 1 | n/a | n/a | n/a | n/a |
| meta_schemas | JDBC | 8 | n/a | n/a | n/a | n/a |
| meta_schemas | JDBC | 32 | n/a | n/a | n/a | n/a |
| meta_schemas | ADBC | 1 | n/a | n/a | n/a | n/a |
| meta_schemas | ADBC | 8 | n/a | n/a | n/a | n/a |
| meta_schemas | ADBC | 32 | n/a | n/a | n/a | n/a |

Answers per class are compared across servers in the run summary (`summary.md`, correctness gate).

### Scans (`SELECT * FROM tpch.lineitem`, SF10, MB/s of Arrow buffers) and server peak RSS

| metric | ours-new | ours-27f5 | up-native | up-main | ours-new vs best upstream |
|---|---|---|---|---|---|
| raw Flight, 1 stream | n/a | n/a | n/a | n/a | n/a |
| raw Flight, 4 streams | n/a | n/a | n/a | n/a | n/a |
| raw Flight, 8 streams | n/a | n/a | n/a | n/a | n/a |
| full export over ADBC | n/a | n/a | n/a | n/a | n/a |
| server peak RSS (MB) | n/a | n/a | n/a | n/a | - |

### Server container (docker stats every ~5 s, all workloads of this setting)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| CPU % p50 (200 = both cores) | n/a | n/a | n/a | n/a |
| CPU % max | n/a | n/a | n/a | n/a |
| memory peak (MiB, limit 6144) | n/a | n/a | n/a | n/a |
| OOM-killed rounds | n/a | n/a | n/a | n/a |

