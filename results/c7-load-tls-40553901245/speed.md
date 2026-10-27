# Server comparison - Report 1: SPEED (compare run 40553901245)

## Experiment setup

| item | value |
|---|---|
| runner | GitHub-hosted `ubuntu-latest`: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor; RAM 15989 MB; kernel 6.17.0-1022-azure; JDK Temurin 21 |
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
| q01 | scan + aggregation | 2754 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 389 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1486 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 1059 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 1780 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 742 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 1681 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 2074 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 4009 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 2178 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 378 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 1023 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 2935 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 1203 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 1171 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 560 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 1744 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 3243 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 1671 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 1460 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 5570 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 612 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 39722 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### Small queries (ms, p50 / p95 / p99 over all rounds)

| class | client | c | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|---|---|
| point_orders | JDBC | 1 | 26.4 / 35.4 / 40.6 | n/a | n/a | n/a |
| point_orders | JDBC | 8 | 113.8 / 173.0 / 303.6 | n/a | n/a | n/a |
| point_orders | JDBC | 32 | 416.0 / 872.1 / 1039.4 | n/a | n/a | n/a |
| point_orders | ADBC | 1 | 16.8 / 26.6 / 32.1 | n/a | n/a | n/a |
| point_orders | ADBC | 8 | 102.3 / 166.6 / 200.3 | n/a | n/a | n/a |
| point_orders | ADBC | 32 | 384.4 / 722.3 / 844.8 | n/a | n/a | n/a |
| point_lineitem | JDBC | 1 | 35.4 / 44.5 / 46.6 | n/a | n/a | n/a |
| point_lineitem | JDBC | 8 | 183.1 / 310.5 / 531.3 | n/a | n/a | n/a |
| point_lineitem | JDBC | 32 | 757.5 / 1452.5 / 1667.4 | n/a | n/a | n/a |
| point_lineitem | ADBC | 1 | 23.2 / 37.4 / 41.8 | n/a | n/a | n/a |
| point_lineitem | ADBC | 8 | 175.9 / 274.7 / 319.5 | n/a | n/a | n/a |
| point_lineitem | ADBC | 32 | 662.2 / 1098.8 / 1307.3 | n/a | n/a | n/a |
| count_filter | JDBC | 1 | 50.9 / 60.2 / 63.6 | n/a | n/a | n/a |
| count_filter | JDBC | 8 | 226.8 / 291.5 / 323.3 | n/a | n/a | n/a |
| count_filter | JDBC | 32 | 868.3 / 1342.1 / 1659.5 | n/a | n/a | n/a |
| count_filter | ADBC | 1 | 39.5 / 52.3 / 53.9 | n/a | n/a | n/a |
| count_filter | ADBC | 8 | 222.7 / 284.5 / 312.9 | n/a | n/a | n/a |
| count_filter | ADBC | 32 | 820.6 / 1227.0 / 1438.8 | n/a | n/a | n/a |
| limit10_ob | JDBC | 1 | 48.4 / 59.8 / 65.4 | n/a | n/a | n/a |
| limit10_ob | JDBC | 8 | 246.7 / 341.2 / 393.1 | n/a | n/a | n/a |
| limit10_ob | JDBC | 32 | 1065.3 / 1680.5 / 2071.1 | n/a | n/a | n/a |
| limit10_ob | ADBC | 1 | 38.3 / 55.2 / 66.4 | n/a | n/a | n/a |
| limit10_ob | ADBC | 8 | 250.9 / 330.3 / 366.2 | n/a | n/a | n/a |
| limit10_ob | ADBC | 32 | 1000.4 / 1554.0 / 1873.5 | n/a | n/a | n/a |
| meta_tables | JDBC | 1 | 8.8 / 13.0 / 15.1 | n/a | n/a | n/a |
| meta_tables | JDBC | 8 | 17.4 / 330.2 / 786.3 | n/a | n/a | n/a |
| meta_tables | JDBC | 32 | 53.3 / 1565.0 / 2209.4 | n/a | n/a | n/a |
| meta_tables | ADBC | 1 | 8.0 / 10.5 / 10.9 | n/a | n/a | n/a |
| meta_tables | ADBC | 8 | 33.3 / 55.3 / 66.2 | n/a | n/a | n/a |
| meta_tables | ADBC | 32 | 156.6 / 1815.6 / 2523.0 | n/a | n/a | n/a |
| meta_schemas | JDBC | 1 | 7.0 / 12.3 / 15.1 | n/a | n/a | n/a |
| meta_schemas | JDBC | 8 | 12.9 / 30.4 / 35.5 | n/a | n/a | n/a |
| meta_schemas | JDBC | 32 | 30.1 / 92.1 / 131.1 | n/a | n/a | n/a |
| meta_schemas | ADBC | 1 | 5.2 / 7.7 / 10.0 | n/a | n/a | n/a |
| meta_schemas | ADBC | 8 | 21.8 / 40.8 / 48.7 | n/a | n/a | n/a |
| meta_schemas | ADBC | 32 | 68.6 / 158.0 / 195.3 | n/a | n/a | n/a |

Answers per class are compared across servers in the run summary (`summary.md`, correctness gate).

### Scans (`SELECT * FROM tpch.lineitem`, SF10, MB/s of Arrow buffers) and server peak RSS

| metric | ours-new | ours-27f5 | up-native | up-main | ours-new vs best upstream |
|---|---|---|---|---|---|
| raw Flight, 1 stream | n/a | n/a | n/a | n/a | n/a |
| raw Flight, 4 streams | n/a | n/a | n/a | n/a | n/a |
| raw Flight, 8 streams | n/a | n/a | n/a | n/a | n/a |
| full export over ADBC | 426 | n/a | n/a | n/a | n/a |
| server peak RSS (MB) | 2699 | n/a | n/a | n/a | - |

### Server container (docker stats every ~5 s, all workloads of this setting)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| CPU % p50 (200 = both cores) | 200 | n/a | n/a | n/a |
| CPU % max | 220 | n/a | n/a | n/a |
| memory peak (MiB, limit 6144) | 2626 | n/a | n/a | n/a |
| OOM-killed rounds | 0 / 3 | n/a | n/a | n/a |

