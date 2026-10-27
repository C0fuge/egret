# Server comparison - Report 1: SPEED (compare run 40537018532)

## Experiment setup

| item | value |
|---|---|
| runner | GitHub-hosted `ubuntu-latest`: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor; Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor; Linux ubuntu24 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C; RAM 15982 MB; kernel 7.0.0-1017-azure; JDK Temurin 21 |
| containers | every server: `eclipse-temurin:21-jre`, `--cpus=2 --cpuset-cpus=0,1 --memory=6g --memory-swap=6g`, JVM `-Xmx3g -XX:MaxDirectMemorySize=2g`, `MALLOC_ARENA_MAX=4`, host network; clients (JDBC/ADBC/Flight runners, jcmd sampling) and the S3 server in their own containers on cpus 2,3 |
| servers | ours-new = `7562a5bdb7b9` (DuckDB v1.5.6); ours-27f5 = `27f583adccd7` (DuckDB v1.5.6); up-native = `9fb08d9dd24df3cb838a3172f9375560bb6dc70a` (DuckDB ?); up-main = `dbacd8d585bce2ef2a449c821fe3a53cc6060b57` (DuckDB ?) |
| data | TPC-H SF1 and SF10, DuckDB dbgen, Parquet, 8 files per big table, 122880-row row groups, one data dir `tpch.*` per SF |
| storage | local disk (`file://`, page-cached) and S3 (`rclone serve s3` on the same runner, path style) |
| pairs | every job: ours-new (side A) vs one other server (side B) on the same runner, rounds A B / B A / A B (3), 1 cold run (warm-up) + warm runs per query (SF1 2 warm, SF10 1 warm per round) |
| settings | `def` = each server's default (`duckDbThreads` ours 4, upstream 2); `t8` = `-DduckDbThreads=8` on both |
| batch size | server defaults (not overridden) |
| clients | TPC-H: Python ADBC Flight SQL 1.12.0 (pyarrow 26), Flight SQL JDBC 18.0.0; small queries: same; scans: raw Flight (Arrow Java), ADBC export |
| correctness | TPC-H over ADBC: rows + checksum per query equal to in-process DuckDB on the same files; over JDBC: the result rows compared numerically with the same reference (numbers within a relative 1.5e-9, i.e. two 10-digit roundings; the JDBC runner prints DECIMAL as an exact plain BigDecimal, the reference as %.10g) |
| upstream on S3 | up-native: `s3a://` data dir (Hadoop S3A from its `docker/hadoop-aws` recipe for listing, DuckDB httpfs for scans, `FLIGHT_S3_*` settings); up-main: **n/a**, main at the fork point has no S3 settings (no `FLIGHT_S3_*`, no S3A dependencies) |
| SF30 | not run: SF1+SF10 already fill most of the repo's 10 GB Actions cache, SF30 Parquet (~11 GB) does not fit; generating it per job costs ~20 min of each 4-vCPU runner |
| JVM `45fc0a9e6e02` `def` | `--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED -Darrowflight.plugins.dir=/app/plugins -Darrowflight.duckdb.extensionDir=/ext/duckdb-home/extensions -DduckDbAllowUnsignedExtensions=true -Ds3Endpoint=http://127.0.0.1:9000 -Ds3UrlStyle=path -Ds3Region=us-east-1 -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf10 -cp --port --localhost --hosts` |
| JVM `6acc9cce0b26` `def` | `--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED -Darrowflight.plugins.dir=/app/plugins -Darrowflight.duckdb.extensionDir=/ext/duckdb-home/extensions -DduckDbAllowUnsignedExtensions=true -Ds3Endpoint=http://127.0.0.1:9000 -Ds3UrlStyle=path -Ds3Region=us-east-1 -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf10 -cp --port --localhost --hosts` |
| JVM `e46f28dfdf09` `def` | `--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED -Darrowflight.plugins.dir=/app/plugins -Darrowflight.duckdb.extensionDir=/ext/duckdb-home/extensions -DduckDbAllowUnsignedExtensions=true -Ds3Endpoint=http://127.0.0.1:9000 -Ds3UrlStyle=path -Ds3Region=us-east-1 -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf10 -cp --port --localhost --hosts` |
| JVM `ours-27f5` `def` | `--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED -Darrowflight.plugins.dir=/app/plugins -Darrowflight.duckdb.extensionDir=/ext/duckdb-home/extensions -DduckDbAllowUnsignedExtensions=true -Ds3Endpoint=http://127.0.0.1:9000 -Ds3UrlStyle=path -Ds3Region=us-east-1 -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf10 -cp --port --localhost --hosts` |
| JVM `ours-new` `def` | `--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED -Darrowflight.plugins.dir=/app/plugins -Darrowflight.duckdb.extensionDir=/ext/duckdb-home/extensions -DduckDbAllowUnsignedExtensions=true -Ds3Endpoint=http://127.0.0.1:9000 -Ds3UrlStyle=path -Ds3Region=us-east-1 -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf10 -cp --port --localhost --hosts` |

Times are warm medians in ms (median over rounds of the per-round warm median). **n/a** = not run, failed or wrong
answer (reason in the notes). Last column: same-runner ratio best-upstream / ours-new (> 1 = ours-new faster).

## local, setting `def`

### TPC-H SF10, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 1659 | 2105 | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 271 | 341 | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1085 | 1259 | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 673 | 833 | n/a | n/a | n/a |
| q05 | 6-way join | 1173 | 1448 | n/a | n/a | n/a |
| q06 | selective scan | 517 | 646 | n/a | n/a | n/a |
| q07 | joins, group by | 1154 | 1419 | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 1446 | 1776 | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 3034 | 3473 | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1273 | 1516 | n/a | n/a | n/a |
| q11 | HAVING subquery | 236 | 305 | n/a | n/a | n/a |
| q12 | join, CASE agg | 662 | 846 | n/a | n/a | n/a |
| q13 | outer join, LIKE | 2019 | 2388 | n/a | n/a | n/a |
| q14 | join, CASE | 814 | 1006 | n/a | n/a | n/a |
| q15 | view / CTE, max | 727 | 932 | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 373 | 478 | n/a | n/a | n/a |
| q17 | correlated avg | 1122 | 1424 | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 2108 | 2512 | n/a | n/a | n/a |
| q19 | OR predicates | 1140 | 1417 | n/a | n/a | n/a |
| q20 | nested IN | 946 | 1196 | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 4388 | 4713 | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 419 | 504 | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 27239 | 32539 | n/a | n/a | geomean n/a (0 q) |

- up-native: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### Small queries (ms, p50 / p95 / p99 over all rounds)

| class | client | c | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|---|---|
| point_orders | JDBC | 1 | 18.4 / 29.0 / 33.7 | 24.2 / 35.1 / 42.9 | n/a | n/a |
| point_orders | JDBC | 8 | 81.0 / 133.8 / 272.0 | 110.3 / 174.4 / 220.1 | n/a | n/a |
| point_orders | JDBC | 32 | 304.5 / 647.4 / 933.2 | 437.1 / 767.3 / 959.7 | n/a | n/a |
| point_orders | ADBC | 1 | 11.0 / 18.0 / 22.8 | 17.8 / 28.7 / 64.7 | n/a | n/a |
| point_orders | ADBC | 8 | 65.9 / 111.9 / 133.9 | 102.3 / 165.4 / 213.2 | n/a | n/a |
| point_orders | ADBC | 32 | 254.9 / 579.2 / 898.9 | 381.5 / 747.0 / 1001.9 | n/a | n/a |
| point_lineitem | JDBC | 1 | 25.3 / 37.4 / 44.5 | 31.1 / 43.6 / 55.7 | n/a | n/a |
| point_lineitem | JDBC | 8 | 133.0 / 201.6 / 313.2 | 168.7 / 254.2 / 322.2 | n/a | n/a |
| point_lineitem | JDBC | 32 | 527.1 / 886.8 / 1199.9 | 697.0 / 1148.2 / 1451.0 | n/a | n/a |
| point_lineitem | ADBC | 1 | 16.6 / 27.3 / 35.4 | 23.2 / 35.4 / 43.0 | n/a | n/a |
| point_lineitem | ADBC | 8 | 118.0 / 176.0 / 214.0 | 160.4 / 248.1 / 305.3 | n/a | n/a |
| point_lineitem | ADBC | 32 | 491.1 / 861.1 / 1135.6 | 645.8 / 1115.5 / 1375.9 | n/a | n/a |
| count_filter | JDBC | 1 | 34.1 / 44.7 / 49.7 | 45.1 / 65.6 / 74.1 | n/a | n/a |
| count_filter | JDBC | 8 | 145.9 / 195.9 / 260.8 | 192.6 / 285.7 / 323.7 | n/a | n/a |
| count_filter | JDBC | 32 | 574.4 / 903.0 / 1096.2 | 759.4 / 1224.8 / 1488.7 | n/a | n/a |
| count_filter | ADBC | 1 | 26.1 / 36.1 / 38.9 | 38.8 / 51.8 / 58.4 | n/a | n/a |
| count_filter | ADBC | 8 | 139.0 / 192.8 / 215.2 | 188.9 / 272.5 / 322.2 | n/a | n/a |
| count_filter | ADBC | 32 | 561.1 / 1013.5 / 1614.7 | 766.3 / 1266.1 / 1577.6 | n/a | n/a |
| limit10_ob | JDBC | 1 | 32.8 / 51.0 / 58.5 | 43.2 / 64.4 / 72.0 | n/a | n/a |
| limit10_ob | JDBC | 8 | 187.7 / 260.1 / 317.3 | 233.9 / 346.2 / 408.9 | n/a | n/a |
| limit10_ob | JDBC | 32 | 761.0 / 1187.6 / 1384.8 | 960.8 / 1505.4 / 1887.6 | n/a | n/a |
| limit10_ob | ADBC | 1 | 25.3 / 39.2 / 53.2 | 36.0 / 55.5 / 70.6 | n/a | n/a |
| limit10_ob | ADBC | 8 | 175.9 / 246.3 / 276.7 | 228.1 / 331.2 / 397.4 | n/a | n/a |
| limit10_ob | ADBC | 32 | 746.7 / 1190.3 / 1696.6 | 970.3 / 1554.0 / 1859.1 | n/a | n/a |
| meta_tables | JDBC | 1 | 5.8 / 9.9 / 11.4 | 6.8 / 10.6 / 13.3 | n/a | n/a |
| meta_tables | JDBC | 8 | 11.7 / 26.2 / 29.6 | 11.7 / 27.5 / 37.1 | n/a | n/a |
| meta_tables | JDBC | 32 | 25.7 / 144.4 / 879.3 | 27.3 / 81.1 / 170.7 | n/a | n/a |
| meta_tables | ADBC | 1 | 5.0 / 8.0 / 10.5 | 6.2 / 10.4 / 214.5 | n/a | n/a |
| meta_tables | ADBC | 8 | 24.4 / 48.8 / 66.9 | 29.0 / 55.2 / 77.3 | n/a | n/a |
| meta_tables | ADBC | 32 | 63.1 / 575.4 / 1491.2 | 88.5 / 1019.9 / 1876.5 | n/a | n/a |
| meta_schemas | JDBC | 1 | 4.4 / 8.4 / 12.0 | 5.0 / 8.6 / 12.6 | n/a | n/a |
| meta_schemas | JDBC | 8 | 10.2 / 23.2 / 30.7 | 10.2 / 26.4 / 37.1 | n/a | n/a |
| meta_schemas | JDBC | 32 | 20.9 / 62.4 / 159.6 | 23.0 / 74.4 / 124.7 | n/a | n/a |
| meta_schemas | ADBC | 1 | 3.2 / 5.5 / 7.2 | 4.1 / 7.3 / 9.5 | n/a | n/a |
| meta_schemas | ADBC | 8 | 16.4 / 39.6 / 48.8 | 18.5 / 40.1 / 51.9 | n/a | n/a |
| meta_schemas | ADBC | 32 | 37.6 / 91.8 / 179.5 | 46.5 / 113.0 / 185.5 | n/a | n/a |

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
| CPU % p50 (200 = both cores) | 199 | 200 | n/a | n/a |
| CPU % max | 204 | 206 | n/a | n/a |
| memory peak (MiB, limit 6144) | 1475 | 1618 | n/a | n/a |
| OOM-killed rounds | 0 / 5 | 0 / 20 | n/a | n/a |

