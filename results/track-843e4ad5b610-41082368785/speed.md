# Server comparison - Report 1: SPEED (compare run 41082368785)

## Experiment setup

| item | value |
|---|---|
| runner | GitHub-hosted `ubuntu-latest`: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor; RAM 15983 MB; kernel 7.0.0-1017-azure; JDK Temurin 21 |
| containers | **no-container reference run**: server in `eclipse-temurin:21-jdk` with an 8 GB memory limit and no CPU limit, clients on the runner host; not the reported numbers |
| servers | ours-new = `7562a5bdb7b9` (DuckDB ?); ours-27f5 = `27f583adccd7` (DuckDB ?); up-native = `9fb08d9dd24df3cb838a3172f9375560bb6dc70a` (DuckDB error: INTERNAL: [FlightSQL] Failed to prepare Flight SQL statement (Internal; Prepare). Vendor code: 13); up-main = `dbacd8d585bce2ef2a449c821fe3a53cc6060b57` (DuckDB ?) |
| data | TPC-H SF1 and SF10, DuckDB dbgen, Parquet, 8 files per big table, 122880-row row groups, one data dir `tpch.*` per SF |
| storage | local disk (`file://`, page-cached) and S3 (`rclone serve s3` on the same runner, path style) |
| pairs | every job: ours-new (side A) vs one other server (side B) on the same runner, rounds A B / B A / A B (3), 1 cold run (warm-up) + warm runs per query (SF1 2 warm, SF10 1 warm per round) |
| settings | `def` = each server's default (`duckDbThreads` ours 4, upstream 2); `t8` = `-DduckDbThreads=8` on both |
| batch size | server defaults (not overridden) |
| clients | TPC-H: Python ADBC Flight SQL 1.12.0 (pyarrow 26), Flight SQL JDBC 18.0.0; small queries: same; scans: raw Flight (Arrow Java), ADBC export |
| correctness | TPC-H over ADBC: rows + checksum per query equal to in-process DuckDB on the same files; over JDBC: the result rows compared numerically with the same reference (numbers within a relative 1.5e-9, i.e. two 10-digit roundings; the JDBC runner prints DECIMAL as an exact plain BigDecimal, the reference as %.10g) |
| upstream on S3 | up-native: `s3a://` data dir (Hadoop S3A from its `docker/hadoop-aws` recipe for listing, DuckDB httpfs for scans, `FLIGHT_S3_*` settings); up-main: **n/a**, main at the fork point has no S3 settings (no `FLIGHT_S3_*`, no S3A dependencies) |
| SF30 | not run: SF1+SF10 already fill most of the repo's 10 GB Actions cache, SF30 Parquet (~11 GB) does not fit; generating it per job costs ~20 min of each 4-vCPU runner |
| JVM `843e4ad5b610` `def` | `--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED -Darrowflight.plugins.dir=/app/plugins -Darrowflight.duckdb.extensionDir=/ext/duckdb-home/extensions -DduckDbAllowUnsignedExtensions=true -Ds3Endpoint=http://127.0.0.1:9000 -Ds3UrlStyle=path -Ds3Region=us-east-1 -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf10 -DresourceProfile=speed -cp --port --localhost --hosts` |
| JVM `up-native` `def` | `--add-modules --add-exports --add-opens --add-opens --add-opens=java.base/java.nio=ALL-UNNAMED --add-opens --add-opens -Dio.netty.tryReflectionSetAccessible=true -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf10 -cp --port --localhost --hosts` |

Times are warm medians in ms (median over rounds of the per-round warm median). **n/a** = not run, failed or wrong
answer (reason in the notes). Last column: same-runner ratio best-upstream / ours-new (> 1 = ours-new faster).

## local, setting `def`

### Small queries (ms, p50 / p95 / p99 over all rounds)

| class | client | c | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|---|---|
| point_orders | JDBC | 1 | n/a | n/a | 24.8 / 39.0 / 58.0 | n/a |
| point_orders | JDBC | 8 | n/a | n/a | n/a | n/a |
| point_orders | JDBC | 32 | n/a | n/a | n/a (480 errors: t5 r-1: java.sql.SQLException: Error while executing SQL "SELECT o_orderkey, o_) | n/a |
| point_orders | ADBC | 1 | n/a | n/a | n/a | n/a |
| point_orders | ADBC | 8 | n/a | n/a | n/a | n/a |
| point_orders | ADBC | 32 | n/a | n/a | n/a (480 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| point_lineitem | JDBC | 1 | n/a | n/a | 34.8 / 53.9 / 59.8 | n/a |
| point_lineitem | JDBC | 8 | n/a | n/a | n/a | n/a |
| point_lineitem | JDBC | 32 | n/a | n/a | n/a (480 errors: t5 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l_) | n/a |
| point_lineitem | ADBC | 1 | n/a | n/a | n/a | n/a |
| point_lineitem | ADBC | 8 | n/a | n/a | n/a | n/a |
| point_lineitem | ADBC | 32 | n/a | n/a | n/a (480 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| count_filter | JDBC | 1 | n/a | n/a | 91.0 / 120.2 / 137.8 | n/a |
| count_filter | JDBC | 8 | n/a | n/a | n/a | n/a |
| count_filter | JDBC | 32 | n/a | n/a | n/a (480 errors: t16 r-1: java.sql.SQLException: Error while executing SQL "SELECT count(*) FROM) | n/a |
| count_filter | ADBC | 1 | n/a | n/a | n/a | n/a |
| count_filter | ADBC | 8 | n/a | n/a | n/a | n/a |
| count_filter | ADBC | 32 | n/a | n/a | n/a (480 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| limit10_ob | JDBC | 1 | n/a | n/a | 8132.9 / 8389.4 / 8505.2 | n/a |
| limit10_ob | JDBC | 8 | n/a | n/a | n/a | n/a |
| limit10_ob | JDBC | 32 | n/a | n/a | n/a (480 errors: t0 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l_) | n/a |
| limit10_ob | ADBC | 1 | n/a | n/a | n/a | n/a |
| limit10_ob | ADBC | 8 | n/a | n/a | n/a | n/a |
| limit10_ob | ADBC | 32 | n/a | n/a | n/a (480 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| meta_tables | JDBC | 1 | n/a | n/a | 85.9 / 194.5 / 213.0 | n/a |
| meta_tables | JDBC | 8 | n/a | n/a | n/a | n/a |
| meta_tables | JDBC | 32 | n/a | n/a | n/a (480 errors: t5 r-1: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRunti) | n/a |
| meta_tables | ADBC | 1 | n/a | n/a | n/a | n/a |
| meta_tables | ADBC | 8 | n/a | n/a | n/a | n/a |
| meta_tables | ADBC | 32 | n/a | n/a | n/a (480 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| meta_schemas | JDBC | 1 | n/a | n/a | 8.2 / 14.7 / 16.0 | n/a |
| meta_schemas | JDBC | 8 | n/a | n/a | n/a | n/a |
| meta_schemas | JDBC | 32 | n/a | n/a | n/a (480 errors: t5 r-1: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRunti) | n/a |
| meta_schemas | ADBC | 1 | n/a | n/a | n/a | n/a |
| meta_schemas | ADBC | 8 | n/a | n/a | n/a | n/a |
| meta_schemas | ADBC | 32 | n/a | n/a | n/a (480 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |

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
| CPU % p50 (200 = both cores) | n/a | n/a | 152 | n/a |
| CPU % max | n/a | n/a | 209 | n/a |
| memory peak (MiB, limit 6144) | n/a | n/a | 5128 | n/a |
| OOM-killed rounds | n/a | n/a | 3 / 6 | n/a |

## s3, setting `def`

### Small queries (ms, p50 / p95 / p99 over all rounds)

| class | client | c | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|---|---|
| point_orders | JDBC | 1 | n/a | n/a | 39.3 / 54.9 / 68.1 | n/a |
| point_orders | JDBC | 8 | n/a | n/a | n/a (189 errors: t5 r2: java.sql.SQLException: Error while executing SQL "SELECT o_orderkey, o_c) | n/a |
| point_orders | JDBC | 32 | n/a | n/a | n/a | n/a |
| point_orders | ADBC | 1 | n/a | n/a | n/a | n/a |
| point_orders | ADBC | 8 | n/a | n/a | n/a (240 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| point_orders | ADBC | 32 | n/a | n/a | n/a (480 errors: t1 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| point_lineitem | JDBC | 1 | n/a | n/a | 42.8 / 113.0 / 4171.8 | n/a |
| point_lineitem | JDBC | 8 | n/a | n/a | n/a (186 errors: t5 r2: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l_l) | n/a |
| point_lineitem | JDBC | 32 | n/a | n/a | n/a | n/a |
| point_lineitem | ADBC | 1 | n/a | n/a | n/a | n/a |
| point_lineitem | ADBC | 8 | n/a | n/a | n/a (240 errors: t3 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| point_lineitem | ADBC | 32 | n/a | n/a | n/a (480 errors: t1 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| count_filter | JDBC | 1 | n/a | n/a | 74.4 / 1111.3 / 1178.3 | n/a |
| count_filter | JDBC | 8 | n/a | n/a | n/a (201 errors: t3 r1: java.sql.SQLException: Error while executing SQL "SELECT count(*) FROM t) | n/a |
| count_filter | JDBC | 32 | n/a | n/a | n/a | n/a |
| count_filter | ADBC | 1 | n/a | n/a | n/a | n/a |
| count_filter | ADBC | 8 | n/a | n/a | n/a (240 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| count_filter | ADBC | 32 | n/a | n/a | n/a (480 errors: t1 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| limit10_ob | JDBC | 1 | n/a | n/a | 7988.9 / 8511.8 / 11138.3 | n/a |
| limit10_ob | JDBC | 8 | n/a | n/a | n/a (210 errors: t5 r-1: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRunti) | n/a |
| limit10_ob | JDBC | 32 | n/a | n/a | n/a | n/a |
| limit10_ob | ADBC | 1 | n/a | n/a | n/a | n/a |
| limit10_ob | ADBC | 8 | n/a | n/a | n/a (240 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| limit10_ob | ADBC | 32 | n/a | n/a | n/a (480 errors: t1 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| meta_tables | JDBC | 1 | n/a | n/a | 32.3 / 848.9 / 1524.6 | n/a |
| meta_tables | JDBC | 8 | n/a | n/a | n/a (195 errors: t3 r1: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRuntim) | n/a |
| meta_tables | JDBC | 32 | n/a | n/a | n/a | n/a |
| meta_tables | ADBC | 1 | n/a | n/a | n/a | n/a |
| meta_tables | ADBC | 8 | n/a | n/a | n/a (240 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| meta_tables | ADBC | 32 | n/a | n/a | n/a (480 errors: t1 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| meta_schemas | JDBC | 1 | n/a | n/a | 7.5 / 12.3 / 14.8 | n/a |
| meta_schemas | JDBC | 8 | n/a | n/a | n/a (192 errors: t3 r1: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRuntim) | n/a |
| meta_schemas | JDBC | 32 | n/a | n/a | n/a | n/a |
| meta_schemas | ADBC | 1 | n/a | n/a | n/a | n/a |
| meta_schemas | ADBC | 8 | n/a | n/a | n/a (240 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| meta_schemas | ADBC | 32 | n/a | n/a | n/a (480 errors: t1 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |

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
| CPU % p50 (200 = both cores) | n/a | n/a | 140 | n/a |
| CPU % max | n/a | n/a | 206 | n/a |
| memory peak (MiB, limit 6144) | n/a | n/a | 6066 | n/a |
| OOM-killed rounds | n/a | n/a | 3 / 3 | n/a |

