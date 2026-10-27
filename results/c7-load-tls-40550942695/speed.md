# Server comparison - Report 1: SPEED (compare run 40550942695)

## Experiment setup

| item | value |
|---|---|
| runner | GitHub-hosted `ubuntu-latest`: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor; Linux ubuntu24 4 vCPU Intel(R) Xeon(R) 6973P-C; RAM 15988 MB; kernel 6.17.0-1022-azure; JDK Temurin 21 |
| containers | every server: `eclipse-temurin:21-jre`, `--cpus=2 --cpuset-cpus=0,1 --memory=6g --memory-swap=6g`, JVM `-Xmx3g -XX:MaxDirectMemorySize=2g`, `MALLOC_ARENA_MAX=4`, host network; clients (JDBC/ADBC/Flight runners, jcmd sampling) and the S3 server in their own containers on cpus 2,3 |
| servers | ours-new = `7562a5bdb7b9` (DuckDB v1.5.6); ours-27f5 = `27f583adccd7` (DuckDB ?); up-native = `202b4cef8a395c5ab62456e75fcc027f6f998683` (DuckDB ?); up-main = `dbacd8d585bce2ef2a449c821fe3a53cc6060b57` (DuckDB ?) |
| data | TPC-H SF1 and SF10, DuckDB dbgen, Parquet, 8 files per big table, 122880-row row groups, one data dir `tpch.*` per SF |
| storage | local disk (`file://`, page-cached) and S3 (`rclone serve s3` on the same runner, path style) |
| pairs | every job: ours-new (side A) vs one other server (side B) on the same runner, rounds A B / B A / A B (3), 1 cold run (warm-up) + warm runs per query (SF1 2 warm, SF10 1 warm per round) |
| settings | `def` = each server's default (`duckDbThreads` ours 4, upstream 2); `t8` = `-DduckDbThreads=8` on both |
| batch size | server defaults (not overridden) |
| clients | TPC-H: Python ADBC Flight SQL 1.12.0 (pyarrow 26), Flight SQL JDBC 18.0.0; small queries: same; scans: raw Flight (Arrow Java), ADBC export |
| correctness | TPC-H over ADBC: rows + checksum per query equal to in-process DuckDB on the same files; over JDBC: the result rows compared numerically with the same reference (numbers within a relative 1.5e-9, i.e. two 10-digit roundings; the JDBC runner prints DECIMAL as an exact plain BigDecimal, the reference as %.10g) |
| upstream on S3 | up-native: `s3a://` data dir (Hadoop S3A from its `docker/hadoop-aws` recipe for listing, DuckDB httpfs for scans, `FLIGHT_S3_*` settings); up-main: **n/a**, main at the fork point has no S3 settings (no `FLIGHT_S3_*`, no S3A dependencies) |
| SF30 | not run: SF1+SF10 already fill most of the repo's 10 GB Actions cache, SF30 Parquet (~11 GB) does not fit; generating it per job costs ~20 min of each 4-vCPU runner |
| JVM `ours-new` `def` | `--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED -Darrowflight.plugins.dir=/app/plugins -Darrowflight.duckdb.extensionDir=/ext/duckdb-home/extensions -DduckDbAllowUnsignedExtensions=true -Ds3Endpoint=http://127.0.0.1:9000 -Ds3UrlStyle=path -Ds3Region=us-east-1 -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf10 -cp --port --localhost --hosts` |

Times are warm medians in ms (median over rounds of the per-round warm median). **n/a** = not run, failed or wrong
answer (reason in the notes). Last column: same-runner ratio best-upstream / ours-new (> 1 = ours-new faster).

## local, setting `def`

### TPC-H SF10, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 1726 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 305 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1120 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 818 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 1409 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 608 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 1259 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 1535 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 3095 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1449 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 284 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 732 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 2411 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 1010 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 857 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 431 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 1264 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 2389 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 1446 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 1070 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 3864 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 465 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 29547 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### Small queries (ms, p50 / p95 / p99 over all rounds)

| class | client | c | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|---|---|
| point_orders | JDBC | 1 | 18.8 / 25.9 / 32.5 | n/a | n/a | n/a |
| point_orders | JDBC | 8 | 78.9 / 125.3 / 151.2 | n/a | n/a | n/a |
| point_orders | JDBC | 32 | 326.5 / 608.8 / 788.0 | n/a | n/a | n/a |
| point_orders | ADBC | 1 | 10.9 / 18.1 / 25.7 | n/a | n/a | n/a |
| point_orders | ADBC | 8 | 65.1 / 122.2 / 145.2 | n/a | n/a | n/a |
| point_orders | ADBC | 32 | 267.2 / 488.5 / 611.4 | n/a | n/a | n/a |
| point_lineitem | JDBC | 1 | 23.1 / 31.5 / 35.7 | n/a | n/a | n/a |
| point_lineitem | JDBC | 8 | 117.3 / 183.7 / 232.1 | n/a | n/a | n/a |
| point_lineitem | JDBC | 32 | 496.2 / 870.3 / 1049.3 | n/a | n/a | n/a |
| point_lineitem | ADBC | 1 | 16.0 / 23.5 / 27.8 | n/a | n/a | n/a |
| point_lineitem | ADBC | 8 | 107.2 / 161.5 / 179.1 | n/a | n/a | n/a |
| point_lineitem | ADBC | 32 | 456.8 / 757.0 / 973.1 | n/a | n/a | n/a |
| count_filter | JDBC | 1 | 31.3 / 36.8 / 45.0 | n/a | n/a | n/a |
| count_filter | JDBC | 8 | 131.1 / 175.1 / 202.3 | n/a | n/a | n/a |
| count_filter | JDBC | 32 | 521.4 / 834.6 / 1025.1 | n/a | n/a | n/a |
| count_filter | ADBC | 1 | 24.6 / 37.5 / 46.9 | n/a | n/a | n/a |
| count_filter | ADBC | 8 | 125.3 / 167.3 / 193.1 | n/a | n/a | n/a |
| count_filter | ADBC | 32 | 480.6 / 815.6 / 1087.4 | n/a | n/a | n/a |
| limit10_ob | JDBC | 1 | 30.5 / 41.5 / 42.0 | n/a | n/a | n/a |
| limit10_ob | JDBC | 8 | 169.5 / 246.8 / 332.8 | n/a | n/a | n/a |
| limit10_ob | JDBC | 32 | 688.2 / 1100.0 / 1345.9 | n/a | n/a | n/a |
| limit10_ob | ADBC | 1 | 26.9 / 40.2 / 42.2 | n/a | n/a | n/a |
| limit10_ob | ADBC | 8 | 163.4 / 222.3 / 243.2 | n/a | n/a | n/a |
| limit10_ob | ADBC | 32 | 665.6 / 1087.7 / 1449.8 | n/a | n/a | n/a |
| meta_tables | JDBC | 1 | 6.6 / 9.8 / 11.9 | n/a | n/a | n/a |
| meta_tables | JDBC | 8 | 12.3 / 28.1 / 33.8 | n/a | n/a | n/a |
| meta_tables | JDBC | 32 | 32.1 / 108.4 / 184.6 | n/a | n/a | n/a |
| meta_tables | ADBC | 1 | 6.1 / 8.9 / 11.2 | n/a | n/a | n/a |
| meta_tables | ADBC | 8 | 28.4 / 50.4 / 146.2 | n/a | n/a | n/a |
| meta_tables | ADBC | 32 | 104.8 / 997.0 / 1491.9 | n/a | n/a | n/a |
| meta_schemas | JDBC | 1 | 5.6 / 8.6 / 11.3 | n/a | n/a | n/a |
| meta_schemas | JDBC | 8 | 12.1 / 25.2 / 29.4 | n/a | n/a | n/a |
| meta_schemas | JDBC | 32 | 24.7 / 86.2 / 195.9 | n/a | n/a | n/a |
| meta_schemas | ADBC | 1 | 4.3 / 6.0 / 6.4 | n/a | n/a | n/a |
| meta_schemas | ADBC | 8 | 17.4 / 35.6 / 43.3 | n/a | n/a | n/a |
| meta_schemas | ADBC | 32 | 48.6 / 126.4 / 197.7 | n/a | n/a | n/a |

Answers per class are compared across servers in the run summary (`summary.md`, correctness gate).

### Scans (`SELECT * FROM tpch.lineitem`, SF10, MB/s of Arrow buffers) and server peak RSS

| metric | ours-new | ours-27f5 | up-native | up-main | ours-new vs best upstream |
|---|---|---|---|---|---|
| raw Flight, 1 stream | n/a | n/a | n/a | n/a | n/a |
| raw Flight, 4 streams | n/a | n/a | n/a | n/a | n/a |
| raw Flight, 8 streams | n/a | n/a | n/a | n/a | n/a |
| full export over ADBC | 576 | n/a | n/a | n/a | n/a |
| server peak RSS (MB) | 2694 | n/a | n/a | n/a | - |

### Server container (docker stats every ~5 s, all workloads of this setting)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| CPU % p50 (200 = both cores) | 202 | n/a | n/a | n/a |
| CPU % max | 205 | n/a | n/a | n/a |
| memory peak (MiB, limit 6144) | 5471 | n/a | n/a | n/a |
| OOM-killed rounds | 0 / 6 | n/a | n/a | n/a |

