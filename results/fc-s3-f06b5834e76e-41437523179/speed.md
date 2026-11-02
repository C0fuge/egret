# Server comparison - Report 1: SPEED (compare run 41437523179)

## Experiment setup

| item | value |
|---|---|
| runner | GitHub-hosted `ubuntu-latest`: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor; Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor; Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor; RAM 15983 MB; kernel 7.0.0-1017-azure; JDK Temurin 21 |
| containers | **no-container reference run**: server in `eclipse-temurin:21-jdk` with an 8 GB memory limit and no CPU limit, clients on the runner host; not the reported numbers |
| servers | ours-new = `7562a5bdb7b9` (DuckDB ?); ours-27f5 = `27f583adccd7` (DuckDB ?); up-native = `6e264c10f4031edcc7c021cd86dc807c8fff9bc6` (DuckDB error: INTERNAL: [FlightSQL] Failed to prepare Flight SQL statement (Internal; Prepare). Vendor code: 13); up-main = `dbacd8d585bce2ef2a449c821fe3a53cc6060b57` (DuckDB ?) |
| data | TPC-H SF1 and SF10, DuckDB dbgen, Parquet, 8 files per big table, 122880-row row groups, one data dir `tpch.*` per SF |
| storage | local disk (`file://`, page-cached) and S3 (`rclone serve s3` on the same runner, path style) |
| pairs | every job: ours-new (side A) vs one other server (side B) on the same runner, rounds A B / B A / A B (3), 1 cold run (warm-up) + warm runs per query (SF1 2 warm, SF10 1 warm per round) |
| settings | `def` = each server's default (`duckDbThreads` ours 4, upstream 2); `t8` = `-DduckDbThreads=8` on both |
| batch size | server defaults (not overridden) |
| clients | TPC-H: Python ADBC Flight SQL 1.12.0 (pyarrow 26), Flight SQL JDBC 18.0.0; small queries: same; scans: raw Flight (Arrow Java), ADBC export |
| correctness | TPC-H over ADBC: rows + checksum per query equal to in-process DuckDB on the same files; over JDBC: the result rows compared numerically with the same reference (numbers within a relative 1.5e-9, i.e. two 10-digit roundings; the JDBC runner prints DECIMAL as an exact plain BigDecimal, the reference as %.10g) |
| upstream on S3 | up-native: `s3a://` data dir (Hadoop S3A from its `docker/hadoop-aws` recipe for listing, DuckDB httpfs for scans, `FLIGHT_S3_*` settings); up-main: **n/a**, main at the fork point has no S3 settings (no `FLIGHT_S3_*`, no S3A dependencies) |
| SF30 | not run: SF1+SF10 already fill most of the repo's 10 GB Actions cache, SF30 Parquet (~11 GB) does not fit; generating it per job costs ~20 min of each 4-vCPU runner |
| JVM `f06b5834e76e` `def` | `--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED -Darrowflight.plugins.dir=/app/plugins -Darrowflight.duckdb.extensionDir=/ext/duckdb-home/extensions -DduckDbAllowUnsignedExtensions=true -Ds3Endpoint=http://127.0.0.1:9000 -Ds3UrlStyle=path -Ds3Region=us-east-1 -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=s3://default/sf10 -DresourceProfile=speed -DduckDbExternalFileCache=true -cp --port --localhost --hosts` |
| JVM `up-native` `def` | `--add-modules --add-exports --add-opens --add-opens --add-opens=java.base/java.nio=ALL-UNNAMED --add-opens --add-opens -Dio.netty.tryReflectionSetAccessible=true -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=s3a://default/sf10 -cp --port --localhost --hosts` |

Times are warm medians in ms (median over rounds of the per-round warm median). **n/a** = not run, failed or wrong
answer (reason in the notes). Last column: same-runner ratio best-upstream / ours-new (> 1 = ours-new faster).

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
| **Score** | sum of the 0 queries every shown server answered | n/a | n/a | n/a | n/a | geomean n/a (0 q) |

- up-native: failed: advertised schema differs from the data (e.g. float64 vs decimal(38,4)): ADBC rejects the stream: q06; failed: subquery table not rewritten: DuckDB `schema "tpch" does not exist`: q04; failed: the server's schema resolver rejects it (upstream: single-table parser, `Can only select from ONE table`; `AVG` unsupported on main): q01 q02 q03 q05 q07 q08 q09 q10 q11 q12 q13 q14 q15 q16 q17 q18 q19 q20 q21 q22
- ours-new: not run: not in this setting's jobs
- ours-27f5: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### Small queries (ms, p50 / p95 / p99 over all rounds)

| class | client | c | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|---|---|
| point_orders | JDBC | 1 | n/a | n/a | 30.4 / 39.2 / 48.2 | n/a |
| point_orders | JDBC | 8 | n/a | n/a | n/a (159 errors: t0 r5: java.sql.SQLException: Error while executing SQL "SELECT o_orderkey, o_c) | n/a |
| point_orders | JDBC | 32 | n/a | n/a | n/a | n/a |
| point_orders | ADBC | 1 | n/a | n/a | n/a | n/a |
| point_orders | ADBC | 8 | n/a | n/a | n/a (240 errors: t0 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| point_orders | ADBC | 32 | n/a | n/a | n/a (480 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| point_lineitem | JDBC | 1 | n/a | n/a | 31.7 / 51.2 / 70.7 | n/a |
| point_lineitem | JDBC | 8 | n/a | n/a | n/a (156 errors: t0 r5: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l_l) | n/a |
| point_lineitem | JDBC | 32 | n/a | n/a | n/a | n/a |
| point_lineitem | ADBC | 1 | n/a | n/a | n/a | n/a |
| point_lineitem | ADBC | 8 | n/a | n/a | n/a (240 errors: t0 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| point_lineitem | ADBC | 32 | n/a | n/a | n/a (480 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| count_filter | JDBC | 1 | n/a | n/a | 50.7 / 109.8 / 1141.3 | n/a |
| count_filter | JDBC | 8 | n/a | n/a | n/a (171 errors: t0 r4: java.sql.SQLException: Error while executing SQL "SELECT count(*) FROM t) | n/a |
| count_filter | JDBC | 32 | n/a | n/a | n/a | n/a |
| count_filter | ADBC | 1 | n/a | n/a | n/a | n/a |
| count_filter | ADBC | 8 | n/a | n/a | n/a (240 errors: t0 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| count_filter | ADBC | 32 | n/a | n/a | n/a (480 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| limit10_ob | JDBC | 1 | n/a | n/a | 5357.3 / 5610.6 / 7598.9 | n/a |
| limit10_ob | JDBC | 8 | n/a | n/a | n/a (178 errors: t4 r0: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRuntim) | n/a |
| limit10_ob | JDBC | 32 | n/a | n/a | n/a | n/a |
| limit10_ob | ADBC | 1 | n/a | n/a | n/a | n/a |
| limit10_ob | ADBC | 8 | n/a | n/a | n/a (240 errors: t0 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| limit10_ob | ADBC | 32 | n/a | n/a | n/a (480 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| meta_tables | JDBC | 1 | n/a | n/a | 8.9 / 247.8 / 786.9 | n/a |
| meta_tables | JDBC | 8 | n/a | n/a | n/a (165 errors: t0 r5: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRuntim) | n/a |
| meta_tables | JDBC | 32 | n/a | n/a | n/a | n/a |
| meta_tables | ADBC | 1 | n/a | n/a | n/a | n/a |
| meta_tables | ADBC | 8 | n/a | n/a | n/a (240 errors: t0 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| meta_tables | ADBC | 32 | n/a | n/a | n/a (480 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| meta_schemas | JDBC | 1 | n/a | n/a | 6.4 / 10.0 / 10.7 | n/a |
| meta_schemas | JDBC | 8 | n/a | n/a | n/a (162 errors: t0 r5: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRuntim) | n/a |
| meta_schemas | JDBC | 32 | n/a | n/a | n/a | n/a |
| meta_schemas | ADBC | 1 | n/a | n/a | n/a | n/a |
| meta_schemas | ADBC | 8 | n/a | n/a | n/a (240 errors: t0 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| meta_schemas | ADBC | 32 | n/a | n/a | n/a (480 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |

Answers per class are compared across servers in the run summary (`summary.md`, correctness gate).

### Scans (`SELECT * FROM tpch.lineitem`, SF10, MB/s of Arrow buffers) and server peak RSS

| metric | ours-new | ours-27f5 | up-native | up-main | ours-new vs best upstream |
|---|---|---|---|---|---|
| raw Flight, 1 stream | n/a | n/a | 322 | n/a | n/a |
| raw Flight, 4 streams | n/a | n/a | 583 | n/a | n/a |
| raw Flight, 8 streams | n/a | n/a | 597 | n/a | n/a |
| full export over ADBC | n/a | n/a | 540 | n/a | n/a |
| server peak RSS (MB) | n/a | n/a | 5882 | n/a | - |

### Server container (docker stats every ~5 s, all workloads of this setting)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| CPU % p50 (200 = both cores) | n/a | n/a | 137 | n/a |
| CPU % max | n/a | n/a | 205 | n/a |
| memory peak (MiB, limit 6144) | n/a | n/a | 6093 | n/a |
| OOM-killed rounds | n/a | n/a | 3 / 9 | n/a |

