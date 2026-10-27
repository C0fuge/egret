# Server comparison - Report 1: SPEED (compare run 40540885908)

## Experiment setup

| item | value |
|---|---|
| runner | GitHub-hosted `ubuntu-latest`: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor; Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor; Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor; Linux ubuntu24 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C; Linux ubuntu24 4 vCPU Intel(R) Xeon(R) 6973P-C; Linux ubuntu24 4 vCPU Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz; RAM 15989 MB; kernel 6.17.0-1022-azure; JDK Temurin 21 |
| containers | every server: `eclipse-temurin:21-jre`, `--cpus=2 --cpuset-cpus=0,1 --memory=6g --memory-swap=6g`, JVM `-Xmx3g -XX:MaxDirectMemorySize=2g`, `MALLOC_ARENA_MAX=4`, host network; clients (JDBC/ADBC/Flight runners, jcmd sampling) and the S3 server in their own containers on cpus 2,3 |
| servers | ours-new = `7562a5bdb7b9` (DuckDB v1.5.6); ours-27f5 = `27f583adccd7` (DuckDB v1.5.6); up-native = `202b4cef8a395c5ab62456e75fcc027f6f998683` (DuckDB error: INTERNAL: [FlightSQL] Failed to prepare Flight SQL statement (Internal; Prepare). Vendor code: 13); up-main = `dbacd8d585bce2ef2a449c821fe3a53cc6060b57` (DuckDB error: INTERNAL: [FlightSQL] Error getting Arrow schema for query (Internal; ExecuteQuery). Vendor code: 13) |
| data | TPC-H SF1 and SF10, DuckDB dbgen, Parquet, 8 files per big table, 122880-row row groups, one data dir `tpch.*` per SF |
| storage | local disk (`file://`, page-cached) and S3 (`rclone serve s3` on the same runner, path style) |
| pairs | every job: ours-new (side A) vs one other server (side B) on the same runner, rounds A B / B A / A B (3), 1 cold run (warm-up) + warm runs per query (SF1 2 warm, SF10 1 warm per round) |
| settings | `def` = each server's default (`duckDbThreads` ours 4, upstream 2); `t8` = `-DduckDbThreads=8` on both |
| batch size | server defaults (not overridden) |
| clients | TPC-H: Python ADBC Flight SQL 1.12.0 (pyarrow 26), Flight SQL JDBC 18.0.0; small queries: same; scans: raw Flight (Arrow Java), ADBC export |
| correctness | TPC-H over ADBC: rows + checksum per query equal to in-process DuckDB on the same files; over JDBC: the result rows compared numerically with the same reference (numbers within a relative 1.5e-9, i.e. two 10-digit roundings; the JDBC runner prints DECIMAL as an exact plain BigDecimal, the reference as %.10g) |
| upstream on S3 | up-native: `s3a://` data dir (Hadoop S3A from its `docker/hadoop-aws` recipe for listing, DuckDB httpfs for scans, `FLIGHT_S3_*` settings); up-main: **n/a**, main at the fork point has no S3 settings (no `FLIGHT_S3_*`, no S3A dependencies) |
| SF30 | not run: SF1+SF10 already fill most of the repo's 10 GB Actions cache, SF30 Parquet (~11 GB) does not fit; generating it per job costs ~20 min of each 4-vCPU runner |
| JVM `ours-27f5` `def` | `--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED -Darrowflight.plugins.dir=/app/plugins -Darrowflight.duckdb.extensionDir=/ext/duckdb-home/extensions -DduckDbAllowUnsignedExtensions=true -Ds3Endpoint=http://127.0.0.1:9000 -Ds3UrlStyle=path -Ds3Region=us-east-1 -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf10 -cp --port --localhost --hosts` |
| JVM `ours-27f5` `t8` | `--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED -Darrowflight.plugins.dir=/app/plugins -Darrowflight.duckdb.extensionDir=/ext/duckdb-home/extensions -DduckDbAllowUnsignedExtensions=true -Ds3Endpoint=http://127.0.0.1:9000 -Ds3UrlStyle=path -Ds3Region=us-east-1 -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf10 -DduckDbThreads=8 -cp --port --localhost --hosts` |
| JVM `ours-new` `def` | `--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED -Darrowflight.plugins.dir=/app/plugins -Darrowflight.duckdb.extensionDir=/ext/duckdb-home/extensions -DduckDbAllowUnsignedExtensions=true -Ds3Endpoint=http://127.0.0.1:9000 -Ds3UrlStyle=path -Ds3Region=us-east-1 -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf10 -cp --port --localhost --hosts` |
| JVM `ours-new` `t8` | `--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED -Darrowflight.plugins.dir=/app/plugins -Darrowflight.duckdb.extensionDir=/ext/duckdb-home/extensions -DduckDbAllowUnsignedExtensions=true -Ds3Endpoint=http://127.0.0.1:9000 -Ds3UrlStyle=path -Ds3Region=us-east-1 -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf10 -DduckDbThreads=8 -cp --port --localhost --hosts` |
| JVM `up-main` `def` | `--add-modules --add-exports --add-opens --add-opens --add-opens=java.base/java.nio=ALL-UNNAMED --add-opens --add-opens -Dio.netty.tryReflectionSetAccessible=true -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf10 -cp --port --localhost --hosts` |
| JVM `up-main` `t8` | `--add-modules --add-exports --add-opens --add-opens --add-opens=java.base/java.nio=ALL-UNNAMED --add-opens --add-opens -Dio.netty.tryReflectionSetAccessible=true -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf10 -DduckDbThreads=8 -cp --port --localhost --hosts` |
| JVM `up-native` `def` | `--add-modules --add-exports --add-opens --add-opens --add-opens=java.base/java.nio=ALL-UNNAMED --add-opens --add-opens -Dio.netty.tryReflectionSetAccessible=true -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf10 -cp --port --localhost --hosts` |
| JVM `up-native` `t8` | `--add-modules --add-exports --add-opens --add-opens --add-opens=java.base/java.nio=ALL-UNNAMED --add-opens --add-opens -Dio.netty.tryReflectionSetAccessible=true -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf10 -DduckDbThreads=8 -cp --port --localhost --hosts` |

Times are warm medians in ms (median over rounds of the per-round warm median). **n/a** = not run, failed or wrong
answer (reason in the notes). Last column: same-runner ratio best-upstream / ours-new (> 1 = ours-new faster).

## local, setting `def`

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
| CPU % p50 (200 = both cores) | 201 | 201 | 202 | 179 |
| CPU % max | 211 | 204 | 205 | 209 |
| memory peak (MiB, limit 6144) | 6118 | 5752 | 5228 | 6127 |
| OOM-killed rounds | 0 / 21 | 0 / 6 | 0 / 9 | 3 / 6 |

## local, setting `t8`

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
| CPU % p50 (200 = both cores) | 200 | 201 | 201 | 178 |
| CPU % max | 203 | 203 | 204 | 206 |
| memory peak (MiB, limit 6144) | 6059 | 5923 | 5549 | 6140 |
| OOM-killed rounds | 0 / 18 | 0 / 6 | 0 / 6 | 3 / 6 |

