# Server comparison - Report 1: SPEED (compare run 40569584228)

## Experiment setup

| item | value |
|---|---|
| runner | GitHub-hosted `ubuntu-latest`: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor; Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor; RAM 15989 MB; kernel 6.17.0-1022-azure; JDK Temurin 21 |
| containers | every server: `eclipse-temurin:21-jre`, `--cpus=2 --cpuset-cpus=0,1 --memory=6g --memory-swap=6g`, JVM `-Xmx3g -XX:MaxDirectMemorySize=2g`, `MALLOC_ARENA_MAX=4`, host network; clients (JDBC/ADBC/Flight runners, jcmd sampling) and the S3 server in their own containers on cpus 2,3 |
| servers | ours-new = `7562a5bdb7b9` (DuckDB v1.5.6); ours-27f5 = `27f583adccd7` (DuckDB ?); up-native = `a4ebfbc55e2307b3b7fe104be1144ea8f555bbca` (DuckDB ?); up-main = `dbacd8d585bce2ef2a449c821fe3a53cc6060b57` (DuckDB ?) |
| data | TPC-H SF1 and SF10, DuckDB dbgen, Parquet, 8 files per big table, 122880-row row groups, one data dir `tpch.*` per SF |
| storage | local disk (`file://`, page-cached) and S3 (`rclone serve s3` on the same runner, path style) |
| pairs | every job: ours-new (side A) vs one other server (side B) on the same runner, rounds A B / B A / A B (3), 1 cold run (warm-up) + warm runs per query (SF1 2 warm, SF10 1 warm per round) |
| settings | `def` = each server's default (`duckDbThreads` ours 4, upstream 2); `t8` = `-DduckDbThreads=8` on both |
| batch size | server defaults (not overridden) |
| clients | TPC-H: Python ADBC Flight SQL 1.12.0 (pyarrow 26), Flight SQL JDBC 18.0.0; small queries: same; scans: raw Flight (Arrow Java), ADBC export |
| correctness | TPC-H over ADBC: rows + checksum per query equal to in-process DuckDB on the same files; over JDBC: the result rows compared numerically with the same reference (numbers within a relative 1.5e-9, i.e. two 10-digit roundings; the JDBC runner prints DECIMAL as an exact plain BigDecimal, the reference as %.10g) |
| upstream on S3 | up-native: `s3a://` data dir (Hadoop S3A from its `docker/hadoop-aws` recipe for listing, DuckDB httpfs for scans, `FLIGHT_S3_*` settings); up-main: **n/a**, main at the fork point has no S3 settings (no `FLIGHT_S3_*`, no S3A dependencies) |
| SF30 | not run: SF1+SF10 already fill most of the repo's 10 GB Actions cache, SF30 Parquet (~11 GB) does not fit; generating it per job costs ~20 min of each 4-vCPU runner |
| JVM `84fec772ec50` `def` | `--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED -Darrowflight.plugins.dir=/app/plugins -Darrowflight.duckdb.extensionDir=/ext/duckdb-home/extensions -DduckDbAllowUnsignedExtensions=true -Ds3Endpoint=http://127.0.0.1:9000 -Ds3UrlStyle=path -Ds3Region=us-east-1 -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=s3://default/sf1 -DduckDbThreads=4 -cp --port --localhost --hosts` |
| JVM `ours-cache` `def` | `--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED -Darrowflight.plugins.dir=/app/plugins -Darrowflight.duckdb.extensionDir=/ext/duckdb-home/extensions -DduckDbAllowUnsignedExtensions=true -Ds3Endpoint=http://127.0.0.1:9000 -Ds3UrlStyle=path -Ds3Region=us-east-1 -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=s3://default/sf1 -DduckDbThreads=4 -Darrowflight.s3.cacheMegabytes=1024 -cp --port --localhost --hosts` |
| JVM `ours-new` `def` | `--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED -Darrowflight.plugins.dir=/app/plugins -Darrowflight.duckdb.extensionDir=/ext/duckdb-home/extensions -DduckDbAllowUnsignedExtensions=true -Ds3Endpoint=http://127.0.0.1:9000 -Ds3UrlStyle=path -Ds3Region=us-east-1 -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=s3://default/sf1 -DduckDbThreads=4 -cp --port --localhost --hosts` |

Times are warm medians in ms (median over rounds of the per-round warm median). **n/a** = not run, failed or wrong
answer (reason in the notes). Last column: same-runner ratio best-upstream / ours-new (> 1 = ours-new faster).

## s3, setting `def`

### TPC-H SF10, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 10240 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 4496 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 18191 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 11337 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 24357 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 16044 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 24255 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 27950 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 34695 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 17039 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 3706 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 19808 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 5563 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 17350 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 14866 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 1242 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 18135 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 14802 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 15132 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 17285 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 35694 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 2048 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 354235 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF1, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 748 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 387 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1463 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 1001 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 1441 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 1255 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 1623 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 2010 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 2101 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1382 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 345 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 1599 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 386 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 1354 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 1083 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 120 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 1756 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 1581 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 1456 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 1462 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 2659 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 199 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 27411 | n/a | n/a | n/a | geomean n/a (0 q) |

- ours-27f5: not run: not in this setting's jobs
- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### Small queries (ms, p50 / p95 / p99 over all rounds)

| class | client | c | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|---|---|
| point_orders | JDBC | 1 | 28.3 / 49.2 / 76.5 | n/a | n/a | n/a |
| point_orders | JDBC | 8 | 452.0 / 803.1 / 988.0 | n/a | n/a | n/a |
| point_orders | JDBC | 32 | 1591.2 / 3082.4 / 3917.5 | n/a | n/a | n/a |
| point_orders | ADBC | 1 | 23.6 / 44.1 / 63.0 | n/a | n/a | n/a |
| point_orders | ADBC | 8 | 448.2 / 782.8 / 945.3 | n/a | n/a | n/a |
| point_orders | ADBC | 32 | 1600.1 / 3113.2 / 5658.2 | n/a | n/a | n/a |
| point_lineitem | JDBC | 1 | 23.0 / 48.2 / 696.9 | n/a | n/a | n/a |
| point_lineitem | JDBC | 8 | 281.2 / 1191.2 / 7290.9 | n/a | n/a | n/a |
| point_lineitem | JDBC | 32 | 854.7 / 10842.2 / 17113.0 | n/a | n/a | n/a |
| point_lineitem | ADBC | 1 | 17.1 / 42.0 / 51.1 | n/a | n/a | n/a |
| point_lineitem | ADBC | 8 | 262.8 / 539.5 / 4850.6 | n/a | n/a | n/a |
| point_lineitem | ADBC | 32 | 858.2 / 4709.0 / 21861.6 | n/a | n/a | n/a |
| count_filter | JDBC | 1 | 817.9 / 1257.1 / 2451.6 | n/a | n/a | n/a |
| count_filter | JDBC | 8 | 5489.7 / 7983.2 / 16206.0 | n/a | n/a | n/a |
| count_filter | JDBC | 32 | 17347.1 / 27010.4 / 57262.3 | n/a | n/a | n/a |
| count_filter | ADBC | 1 | 821.6 / 1147.9 / 1342.6 | n/a | n/a | n/a |
| count_filter | ADBC | 8 | 5522.2 / 7683.0 / 7994.5 | n/a | n/a | n/a |
| count_filter | ADBC | 32 | 16800.0 / 30207.4 / 47424.9 | n/a | n/a | n/a |
| limit10_ob | JDBC | 1 | 136.7 / 204.3 / 363.0 | n/a | n/a | n/a |
| limit10_ob | JDBC | 8 | 866.3 / 1496.1 / 6598.6 | n/a | n/a | n/a |
| limit10_ob | JDBC | 32 | 2944.4 / 5397.9 / 21284.2 | n/a | n/a | n/a |
| limit10_ob | ADBC | 1 | 135.5 / 191.4 / 232.5 | n/a | n/a | n/a |
| limit10_ob | ADBC | 8 | 872.5 / 1417.8 / 1819.0 | n/a | n/a | n/a |
| limit10_ob | ADBC | 32 | 2993.4 / 5243.5 / 13493.4 | n/a | n/a | n/a |
| meta_tables | JDBC | 1 | 7.0 / 11.3 / 16.3 | n/a | n/a | n/a |
| meta_tables | JDBC | 8 | 4.7 / 11.3 / 16.8 | n/a | n/a | n/a |
| meta_tables | JDBC | 32 | 5.2 / 20.7 / 33.0 | n/a | n/a | n/a |
| meta_tables | ADBC | 1 | 6.5 / 10.9 / 13.7 | n/a | n/a | n/a |
| meta_tables | ADBC | 8 | 6.7 / 16.9 / 22.2 | n/a | n/a | n/a |
| meta_tables | ADBC | 32 | 13.5 / 39.3 / 63.0 | n/a | n/a | n/a |
| meta_schemas | JDBC | 1 | 4.6 / 8.4 / 10.8 | n/a | n/a | n/a |
| meta_schemas | JDBC | 8 | 3.1 / 9.8 / 21.2 | n/a | n/a | n/a |
| meta_schemas | JDBC | 32 | 4.0 / 21.2 / 44.2 | n/a | n/a | n/a |
| meta_schemas | ADBC | 1 | 4.1 / 7.6 / 9.5 | n/a | n/a | n/a |
| meta_schemas | ADBC | 8 | 4.1 / 11.3 / 19.3 | n/a | n/a | n/a |
| meta_schemas | ADBC | 32 | 9.5 / 34.2 / 69.9 | n/a | n/a | n/a |

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
| CPU % p50 (200 = both cores) | 32 | n/a | n/a | n/a |
| CPU % max | 210 | n/a | n/a | n/a |
| memory peak (MiB, limit 6144) | 2256 | n/a | n/a | n/a |
| OOM-killed rounds | 0 / 9 | n/a | n/a | n/a |

