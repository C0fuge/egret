# Server comparison - Report 1: SPEED (compare run 40550556746)

## Experiment setup

| item | value |
|---|---|
| runner | GitHub-hosted `ubuntu-latest`: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor; Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor; RAM 15989 MB; kernel 6.17.0-1022-azure; JDK Temurin 21 |
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
| JVM `ours-new` `def` | `--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED -Darrowflight.plugins.dir=/app/plugins -Darrowflight.duckdb.extensionDir=/ext/duckdb-home/extensions -DduckDbAllowUnsignedExtensions=true -Ds3Endpoint=http://127.0.0.1:9000 -Ds3UrlStyle=path -Ds3Region=us-east-1 -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf1 -DduckDbThreads=1 -cp --port --localhost --hosts` |

Times are warm medians in ms (median over rounds of the per-round warm median). **n/a** = not run, failed or wrong
answer (reason in the notes). Last column: same-runner ratio best-upstream / ours-new (> 1 = ours-new faster).

## local, setting `def`

### TPC-H SF10, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 2571 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 382 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1423 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 930 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 1673 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 738 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 1629 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 1961 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 3796 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1713 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 338 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 989 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 2604 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 1144 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 947 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 468 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 1685 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 3851 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 2066 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 1370 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 5090 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 560 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 37928 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF1, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 313 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 67 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 151 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 110 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 163 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 100 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 170 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 209 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 285 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 188 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 48 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 114 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 231 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 133 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 86 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 66 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 162 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 332 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 173 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 135 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 401 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 68 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 3705 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### Small queries (ms, p50 / p95 / p99 over all rounds)

| class | client | c | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|---|---|
| point_orders | JDBC | 1 | 22.3 / 33.5 / 40.4 | n/a | n/a | n/a |
| point_orders | JDBC | 8 | 84.9 / 143.6 / 183.1 | n/a | n/a | n/a |
| point_orders | JDBC | 32 | 298.2 / 654.8 / 953.5 | n/a | n/a | n/a |
| point_orders | ADBC | 1 | 14.7 / 20.5 / 26.9 | n/a | n/a | n/a |
| point_orders | ADBC | 8 | 70.6 / 117.2 / 154.1 | n/a | n/a | n/a |
| point_orders | ADBC | 32 | 270.1 / 552.9 / 694.5 | n/a | n/a | n/a |
| point_lineitem | JDBC | 1 | 29.9 / 46.1 / 53.9 | n/a | n/a | n/a |
| point_lineitem | JDBC | 8 | 158.8 / 229.6 / 287.4 | n/a | n/a | n/a |
| point_lineitem | JDBC | 32 | 586.8 / 976.0 / 1273.2 | n/a | n/a | n/a |
| point_lineitem | ADBC | 1 | 22.8 / 36.2 / 42.3 | n/a | n/a | n/a |
| point_lineitem | ADBC | 8 | 145.8 / 207.9 / 249.2 | n/a | n/a | n/a |
| point_lineitem | ADBC | 32 | 576.6 / 913.8 / 1093.8 | n/a | n/a | n/a |
| count_filter | JDBC | 1 | 48.1 / 66.0 / 80.8 | n/a | n/a | n/a |
| count_filter | JDBC | 8 | 254.7 / 335.8 / 364.8 | n/a | n/a | n/a |
| count_filter | JDBC | 32 | 932.6 / 1321.4 / 1560.6 | n/a | n/a | n/a |
| count_filter | ADBC | 1 | 40.9 / 56.7 / 69.5 | n/a | n/a | n/a |
| count_filter | ADBC | 8 | 249.6 / 328.4 / 352.1 | n/a | n/a | n/a |
| count_filter | ADBC | 32 | 916.9 / 1270.0 / 1598.6 | n/a | n/a | n/a |
| limit10_ob | JDBC | 1 | 40.2 / 62.6 / 67.7 | n/a | n/a | n/a |
| limit10_ob | JDBC | 8 | 233.2 / 297.2 / 333.5 | n/a | n/a | n/a |
| limit10_ob | JDBC | 32 | 883.4 / 1359.6 / 1695.5 | n/a | n/a | n/a |
| limit10_ob | ADBC | 1 | 34.4 / 52.2 / 59.6 | n/a | n/a | n/a |
| limit10_ob | ADBC | 8 | 226.9 / 301.1 / 351.8 | n/a | n/a | n/a |
| limit10_ob | ADBC | 32 | 896.7 / 1332.7 / 1579.1 | n/a | n/a | n/a |
| meta_tables | JDBC | 1 | 6.9 / 11.3 / 15.3 | n/a | n/a | n/a |
| meta_tables | JDBC | 8 | 10.7 / 26.0 / 79.5 | n/a | n/a | n/a |
| meta_tables | JDBC | 32 | 22.7 / 401.5 / 1700.1 | n/a | n/a | n/a |
| meta_tables | ADBC | 1 | 6.7 / 9.4 / 11.3 | n/a | n/a | n/a |
| meta_tables | ADBC | 8 | 23.9 / 256.9 / 644.7 | n/a | n/a | n/a |
| meta_tables | ADBC | 32 | 64.5 / 614.0 / 1797.2 | n/a | n/a | n/a |
| meta_schemas | JDBC | 1 | 5.0 / 8.8 / 10.4 | n/a | n/a | n/a |
| meta_schemas | JDBC | 8 | 9.2 / 21.2 / 31.4 | n/a | n/a | n/a |
| meta_schemas | JDBC | 32 | 19.2 / 52.6 / 86.4 | n/a | n/a | n/a |
| meta_schemas | ADBC | 1 | 4.5 / 7.1 / 8.8 | n/a | n/a | n/a |
| meta_schemas | ADBC | 8 | 15.7 / 33.3 / 43.3 | n/a | n/a | n/a |
| meta_schemas | ADBC | 32 | 40.1 / 84.4 / 140.0 | n/a | n/a | n/a |

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
| CPU % p50 (200 = both cores) | 198 | n/a | n/a | n/a |
| CPU % max | 206 | n/a | n/a | n/a |
| memory peak (MiB, limit 6144) | 2317 | n/a | n/a | n/a |
| OOM-killed rounds | 0 / 9 | n/a | n/a | n/a |

