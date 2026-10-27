# Server comparison - Report 1: SPEED (2026-10-27)

Tables below: compare run [40537011671](c2-speed-40537011671/speed.md) (upstream pairs, re-run after the fixes) merged with
the ours-new vs ours-27f5 pairs of run 40490378159. Every server in an identically limited container (2 CPUs on cpus 0,1,
6 GB, `-Xmx3g -XX:MaxDirectMemorySize=2g`); clients and S3 in their own containers on cpus 2,3. Every A/B pair on one
runner, alternating rounds, 3 rounds, 1 warm-up.

## Fix list (maintainer, 18:55) - results

1. **JDBC "wrong answer" q01/q05/q06/q07/q09/q15/q19 on both our builds**: harness, not servers. JDBC answers are now
   compared numerically with the DuckDB reference rows (decimal-aware, same rounding). Both our builds: 22/22 correct on
   JDBC and ADBC, SF1 and SF10, local and S3.
2. **up-main ADBC TPC-H "failed"**: the server's own errors, recorded per query (every upstream TPC-H query fails on both
   upstream builds, so the upstream TPC-H columns are n/a with these reasons, never ranked):
   - multi-table queries: upstream's schema resolver rejects them (`Can only select from ONE table`), on Prepare and on
     plain `CommandStatementQuery` alike (upstream runs TPC-H only behind Spark, which does the joins);
   - q04-style subqueries: the table inside the subquery is not rewritten, DuckDB answers `schema "tpch" does not exist`;
   - q06: the stream is DECIMAL(38,4) while the advertised schema says float64, which ADBC rejects;
   - up-main also has no `AVG` (`Column 'avg(l_quantity)' not found`); JDBC: no prepared statements at all.
   Through Trino and our connector (Report 3) both upstream builds answer TPC-H SF1 22/22 correctly, because Trino sends
   them single-table scans only.
3. **up-native jobs added** in `def` and `t8`, local and S3: it appears in every table (its upstream head moved during the
   day: `9fb08d9dd24d` here, `202b4cef8a39` in Report 3).
4. **ours-new 30-45 % slower than ours-27f5 on SF10 ADBC: not confirmed, no build regresses.** Dedicated same-runner job
   [c6-bisect 40537018532](c6-bisect-40537018532/summary.md), 5 rounds, each build vs ours-27f5 on one runner, ADBC SF10 sum of
   medians B / A: `45fc0a9e6e02` 1.00, `e46f28dfdf09` 0.98, `6acc9cce0b26` 1.00, `7562a5bdb7b9` 1.01; small ADBC c1 p50
   0.78-0.85 (the newer builds are 15-22 % faster there). The gap in the first speed report was an aggregation artifact: its
   ours-new column pooled jobs from other runners and CPU types, while ours-27f5 came only from its own pair job. Every TPC-H
   table now prints the same-runner ratio ours-27f5 / ours-new under it: 0.95-1.05 in 15 of 16 tables (one outlier, S3 `t8`
   SF10 JDBC 0.76, single pair job). Compare our two builds by that ratio, not by the columns.

## Summary

- **TPC-H (SF1 / SF10, ADBC and JDBC, local and S3)**: only our builds answer it; both upstream builds are n/a (item 2).
  ours-new and ours-27f5 are equal within noise on the same runner.
- **Small queries**: up-native answers point / count / LIMIT-with-ORDER-BY over JDBC at c1/c8 (up to ~25 % lower p50 than
  ours-new), but fails every class at c32, and its LIMIT 10 with ORDER BY takes ~5.8 s at c1 and fails at c8; over ADBC it
  has no small-query result (n/a: no answers recorded, the rounds where it was OOM-killed included). up-main fails every JDBC query (no prepared statements) and its ADBC c8/c32 connections fail.
  **Both upstream servers were OOM-killed inside the 6 GB limit in 3 of 6 rounds** (memory peak 6.1 GB); ours peaked at 1.7-3.2 GB
  and was never killed (0 / 18 rounds).
- **Scans** (`SELECT * FROM tpch.lineitem` SF10): up-native streams faster with 4-8 parallel raw Flight streams (local `def`
  807-823 vs ours 463-502 MB/s) at twice the memory (peak RSS 3.7-5.7 GB vs 1.7-2.7 GB); single stream and full ADBC export
  are close (ours 0.77-1.09x of up-native). up-main: no scan numbers (OOM-killed before the scan step).
- **SF30**: not run (the SF1+SF10 Parquet already fill most of the repo's 10 GB Actions cache; SF30 does not fit, and
  generating it per job costs ~20 min of each runner).


## Experiment setup

| item | value |
|---|---|
| runner | GitHub-hosted `ubuntu-latest`: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor; Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor; Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor; Linux ubuntu24 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C; RAM 15989 MB; kernel 6.17.0-1022-azure; JDK Temurin 21 |
| containers | every server: `eclipse-temurin:21-jre`, `--cpus=2 --cpuset-cpus=0,1 --memory=6g --memory-swap=6g`, JVM `-Xmx3g -XX:MaxDirectMemorySize=2g`, `MALLOC_ARENA_MAX=4`, host network; clients (JDBC/ADBC/Flight runners, jcmd sampling) and the S3 server in their own containers on cpus 2,3 |
| servers | ours-new = `7562a5bdb7b9` (DuckDB v1.5.6); ours-27f5 = `27f583adccd7` (DuckDB v1.5.6); up-native = `9fb08d9dd24df3cb838a3172f9375560bb6dc70a` (DuckDB error: INTERNAL: [FlightSQL] Failed to prepare Flight SQL statement (Internal; Prepare). Vendor code: 13); up-main = `dbacd8d585bce2ef2a449c821fe3a53cc6060b57` (DuckDB error: INTERNAL: [FlightSQL] Error getting Arrow schema for query (Internal; ExecuteQuery). Vendor code: 13) |
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

### TPC-H SF10, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 2115 | 1510 | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 320 | 251 | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1196 | 862 | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 796 | 615 | n/a | n/a | n/a |
| q05 | 6-way join | 1427 | 1076 | n/a | n/a | n/a |
| q06 | selective scan | 620 | 470 | n/a | n/a | n/a |
| q07 | joins, group by | 1368 | 996 | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 1726 | 1194 | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 3267 | 2508 | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1469 | 1115 | n/a | n/a | n/a |
| q11 | HAVING subquery | 289 | 212 | n/a | n/a | n/a |
| q12 | join, CASE agg | 803 | 598 | n/a | n/a | n/a |
| q13 | outer join, LIKE | 2275 | 1822 | n/a | n/a | n/a |
| q14 | join, CASE | 973 | 728 | n/a | n/a | n/a |
| q15 | view / CTE, max | 865 | 639 | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 446 | 326 | n/a | n/a | n/a |
| q17 | correlated avg | 1420 | 1024 | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 2425 | 1738 | n/a | n/a | n/a |
| q19 | OR predicates | 1329 | 1001 | n/a | n/a | n/a |
| q20 | nested IN | 1165 | 848 | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 4595 | 3723 | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 483 | 367 | n/a | n/a | n/a |
| **Score** | sum of the 0 queries every shown server answered | n/a | n/a | n/a | n/a | geomean n/a (0 q) |

- up-native: failed: advertised schema differs from the data (e.g. float64 vs decimal(38,4)): ADBC rejects the stream: q06; failed: subquery table not rewritten: DuckDB `schema "tpch" does not exist`: q04; failed: the server's schema resolver rejects it (upstream: single-table parser, `Can only select from ONE table`; `AVG` unsupported on main): q01 q02 q03 q05 q07 q08 q09 q10 q11 q12 q13 q14 q15 q16 q17 q18 q19 q20 q21 q22
- up-main: failed: advertised schema differs from the data (e.g. float64 vs decimal(38,4)): ADBC rejects the stream: q06; failed: subquery table not rewritten: DuckDB `schema "tpch" does not exist`: q04; failed: the server's schema resolver rejects it (upstream: single-table parser, `Can only select from ONE table`; `AVG` unsupported on main): q01 q02 q03 q05 q07 q08 q09 q10 q11 q12 q13 q14 q15 q16 q17 q18 q19 q20 q21 q22
- same runner: ours-27f5 / ours-new = 0.96 (sum of 22 warm medians, AMD EPYC 9V45 96-Core Processor)
- the ours-new column is the median over all its jobs of this storage and setting (other runners and CPU types), ours-27f5 comes only from its own pair job: compare the two by the same-runner ratio above, not by the columns

### TPC-H SF1, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 293 | 205 | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 53 | 47 | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 131 | 113 | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 95 | 70 | n/a | n/a | n/a |
| q05 | 6-way join | 139 | 105 | n/a | n/a | n/a |
| q06 | selective scan | 81 | 66 | n/a | n/a | n/a |
| q07 | joins, group by | 145 | 119 | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 175 | 128 | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 243 | 182 | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 187 | 131 | n/a | n/a | n/a |
| q11 | HAVING subquery | 43 | 37 | n/a | n/a | n/a |
| q12 | join, CASE agg | 94 | 76 | n/a | n/a | n/a |
| q13 | outer join, LIKE | 219 | 179 | n/a | n/a | n/a |
| q14 | join, CASE | 108 | 87 | n/a | n/a | n/a |
| q15 | view / CTE, max | 76 | 63 | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 66 | 51 | n/a | n/a | n/a |
| q17 | correlated avg | 133 | 109 | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 284 | 217 | n/a | n/a | n/a |
| q19 | OR predicates | 144 | 123 | n/a | n/a | n/a |
| q20 | nested IN | 118 | 101 | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 360 | 298 | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 55 | 47 | n/a | n/a | n/a |
| **Score** | sum of the 0 queries every shown server answered | n/a | n/a | n/a | n/a | geomean n/a (0 q) |

- up-native: failed: advertised schema differs from the data (e.g. float64 vs decimal(38,4)): ADBC rejects the stream: q06; failed: subquery table not rewritten: DuckDB `schema "tpch" does not exist`: q04; failed: the server's schema resolver rejects it (upstream: single-table parser, `Can only select from ONE table`; `AVG` unsupported on main): q01 q02 q03 q05 q07 q08 q09 q10 q11 q12 q13 q14 q15 q16 q17 q18 q19 q20 q21 q22
- up-main: failed: advertised schema differs from the data (e.g. float64 vs decimal(38,4)): ADBC rejects the stream: q06; failed: subquery table not rewritten: DuckDB `schema "tpch" does not exist`: q04; failed: the server's schema resolver rejects it (upstream: single-table parser, `Can only select from ONE table`; `AVG` unsupported on main): q01 q02 q03 q05 q07 q08 q09 q10 q11 q12 q13 q14 q15 q16 q17 q18 q19 q20 q21 q22
- same runner: ours-27f5 / ours-new = 1.01 (sum of 22 warm medians, AMD EPYC 9V45 96-Core Processor)
- the ours-new column is the median over all its jobs of this storage and setting (other runners and CPU types), ours-27f5 comes only from its own pair job: compare the two by the same-runner ratio above, not by the columns

### TPC-H SF10, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 1512 | 1553 | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 241 | 260 | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 861 | 917 | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 606 | 608 | n/a | n/a | n/a |
| q05 | 6-way join | 1104 | 1035 | n/a | n/a | n/a |
| q06 | selective scan | 505 | 488 | n/a | n/a | n/a |
| q07 | joins, group by | 1150 | 997 | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 1462 | 1291 | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 2591 | 2535 | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1135 | 1136 | n/a | n/a | n/a |
| q11 | HAVING subquery | 225 | 218 | n/a | n/a | n/a |
| q12 | join, CASE agg | 617 | 605 | n/a | n/a | n/a |
| q13 | outer join, LIKE | 1813 | 1812 | n/a | n/a | n/a |
| q14 | join, CASE | 748 | 741 | n/a | n/a | n/a |
| q15 | view / CTE, max | 648 | 650 | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 351 | 351 | n/a | n/a | n/a |
| q17 | correlated avg | 1045 | 1037 | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 1846 | 1796 | n/a | n/a | n/a |
| q19 | OR predicates | 1014 | 999 | n/a | n/a | n/a |
| q20 | nested IN | 870 | 858 | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 4293 | 3635 | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 373 | 352 | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 25010 | 23874 | n/a | n/a | geomean n/a (0 q) |

- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- same runner: ours-27f5 / ours-new = 0.95 (sum of 22 warm medians, AMD EPYC 9V45 96-Core Processor)
- the ours-new column is the median over all its jobs of this storage and setting (other runners and CPU types), ours-27f5 comes only from its own pair job: compare the two by the same-runner ratio above, not by the columns

### TPC-H SF1, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 209 | 223 | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 49 | 58 | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 109 | 107 | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 86 | 78 | n/a | n/a | n/a |
| q05 | 6-way join | 110 | 114 | n/a | n/a | n/a |
| q06 | selective scan | 67 | 67 | n/a | n/a | n/a |
| q07 | joins, group by | 116 | 120 | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 139 | 136 | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 205 | 186 | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 138 | 153 | n/a | n/a | n/a |
| q11 | HAVING subquery | 43 | 44 | n/a | n/a | n/a |
| q12 | join, CASE agg | 88 | 78 | n/a | n/a | n/a |
| q13 | outer join, LIKE | 177 | 193 | n/a | n/a | n/a |
| q14 | join, CASE | 88 | 86 | n/a | n/a | n/a |
| q15 | view / CTE, max | 73 | 63 | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 59 | 66 | n/a | n/a | n/a |
| q17 | correlated avg | 116 | 107 | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 221 | 220 | n/a | n/a | n/a |
| q19 | OR predicates | 122 | 119 | n/a | n/a | n/a |
| q20 | nested IN | 105 | 96 | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 294 | 271 | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 51 | 53 | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 2665 | 2638 | n/a | n/a | geomean n/a (0 q) |

- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- same runner: ours-27f5 / ours-new = 0.99 (sum of 22 warm medians, AMD EPYC 9V45 96-Core Processor)
- the ours-new column is the median over all its jobs of this storage and setting (other runners and CPU types), ours-27f5 comes only from its own pair job: compare the two by the same-runner ratio above, not by the columns

### Small queries (ms, p50 / p95 / p99 over all rounds)

| class | client | c | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|---|---|
| point_orders | JDBC | 1 | 25.3 / 36.5 / 44.6 | 28.1 / 38.3 / 43.5 | 23.4 / 35.4 / 53.2 | n/a (60 errors: t0 r-1: java.sql.SQLException: Error while executing SQL "SELECT o_orderkey, o_) |
| point_orders | JDBC | 8 | 114.4 / 193.9 / 361.7 | 130.3 / 190.9 / 226.1 | 89.6 / 185.9 / 374.2 | n/a (240 errors: t2 r-1: java.sql.SQLException: Error while executing SQL "SELECT o_orderkey, o_) |
| point_orders | JDBC | 32 | 465.7 / 914.2 / 1472.9 | 511.3 / 888.2 / 1005.4 | n/a (480 errors: t27 r-1: java.sql.SQLException: Error while executing SQL "SELECT o_orderkey, o) | n/a (480 errors: t8 r-1: java.sql.SQLException: Error while executing SQL "SELECT o_orderkey, o_) |
| point_orders | ADBC | 1 | 15.3 / 25.0 / 33.3 | 20.3 / 27.7 / 46.1 | n/a | n/a |
| point_orders | ADBC | 8 | 95.3 / 156.4 / 173.2 | 125.5 / 186.6 / 231.4 | n/a | n/a (240 errors: t4 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| point_orders | ADBC | 32 | 381.0 / 759.9 / 1002.2 | 429.1 / 743.8 / 893.1 | n/a (480 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a (480 errors: t1 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| point_lineitem | JDBC | 1 | 33.3 / 44.7 / 53.6 | 38.5 / 49.1 / 66.4 | 28.1 / 44.2 / 62.4 | n/a (60 errors: t0 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l_) |
| point_lineitem | JDBC | 8 | 178.8 / 279.6 / 401.5 | 202.1 / 301.4 / 432.2 | 136.2 / 238.8 / 423.3 | n/a (240 errors: t3 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l_) |
| point_lineitem | JDBC | 32 | 725.6 / 1261.6 / 1544.3 | 786.9 / 1247.2 / 1531.0 | n/a (480 errors: t28 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l) | n/a (480 errors: t27 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l) |
| point_lineitem | ADBC | 1 | 24.1 / 35.1 / 41.9 | 29.2 / 45.9 / 53.8 | n/a | n/a |
| point_lineitem | ADBC | 8 | 164.9 / 258.4 / 308.6 | 195.0 / 278.6 / 330.0 | n/a | n/a (240 errors: t4 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| point_lineitem | ADBC | 32 | 686.5 / 1180.1 / 1471.4 | 776.4 / 1177.3 / 1476.7 | n/a (480 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a (480 errors: t1 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| count_filter | JDBC | 1 | 47.3 / 58.6 / 64.3 | 52.0 / 64.7 / 73.3 | 36.8 / 48.1 / 59.9 | n/a (60 errors: t0 r-1: java.sql.SQLException: Error while executing SQL "SELECT count(*) FROM) |
| count_filter | JDBC | 8 | 215.1 / 290.0 / 316.3 | 244.7 / 321.9 / 389.7 | 171.8 / 288.2 / 322.7 | n/a (240 errors: t4 r-1: java.sql.SQLException: Error while executing SQL "SELECT count(*) FROM) |
| count_filter | JDBC | 32 | 793.3 / 1426.0 / 2061.1 | 955.5 / 1601.0 / 1905.0 | n/a (480 errors: t11 r-1: java.sql.SQLException: Error while executing SQL "SELECT count(*) FROM) | n/a (480 errors: t16 r-1: java.sql.SQLException: Error while executing SQL "SELECT count(*) FROM) |
| count_filter | ADBC | 1 | 40.1 / 53.6 / 77.0 | 46.7 / 70.9 / 81.4 | n/a | n/a |
| count_filter | ADBC | 8 | 213.0 / 301.1 / 337.3 | 239.8 / 297.3 / 325.4 | n/a | n/a (240 errors: t5 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| count_filter | ADBC | 32 | 806.7 / 1338.3 / 1603.4 | 962.9 / 1471.5 / 1716.0 | n/a (480 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a (480 errors: t1 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| limit10_ob | JDBC | 1 | 43.6 / 57.9 / 70.6 | 50.7 / 68.7 / 77.4 | 5775.5 / 6179.2 / 6360.9 | n/a (60 errors: t0 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l_) |
| limit10_ob | JDBC | 8 | 250.3 / 362.7 / 462.9 | 283.7 / 387.1 / 446.6 | n/a (114 errors: t6 r1: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRuntim) | n/a (240 errors: t3 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l_) |
| limit10_ob | JDBC | 32 | 972.4 / 1648.2 / 2106.3 | 1162.6 / 1761.6 / 2334.4 | n/a (480 errors: t30 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l) | n/a (480 errors: t23 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l) |
| limit10_ob | ADBC | 1 | 36.8 / 56.4 / 63.4 | 42.7 / 63.9 / 71.4 | n/a | n/a |
| limit10_ob | ADBC | 8 | 239.8 / 353.8 / 399.8 | 266.0 / 348.7 / 437.2 | n/a | n/a (240 errors: t5 r-1: OperationalError: IO: [FlightSQL] error reading from server: EOF (Unava) |
| limit10_ob | ADBC | 32 | 991.9 / 1582.0 / 1836.0 | 1185.1 / 1763.9 / 2066.8 | n/a (480 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a (480 errors: t1 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| meta_tables | JDBC | 1 | 8.4 / 14.7 / 22.0 | 8.0 / 12.4 / 13.7 | 10.7 / 207.3 / 218.2 | 14.4 / 23.6 / 26.4 |
| meta_tables | JDBC | 8 | 13.6 / 30.4 / 41.0 | 13.8 / 342.3 / 838.2 | 30.5 / 1043.9 / 1285.4 | 48.3 / 88.8 / 130.1 |
| meta_tables | JDBC | 32 | 28.4 / 1151.0 / 1962.8 | 31.1 / 1193.0 / 1840.1 | n/a (480 errors: t27 r-1: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRunt) | n/a (480 errors: t23 r-1: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRunt) |
| meta_tables | ADBC | 1 | 8.0 / 13.8 / 16.3 | 7.8 / 9.6 / 11.1 | n/a | n/a |
| meta_tables | ADBC | 8 | 31.6 / 64.2 / 525.7 | 31.1 / 58.1 / 70.9 | n/a | n/a (240 errors: t5 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| meta_tables | ADBC | 32 | 88.8 / 640.2 / 2206.1 | 96.4 / 1899.4 / 3081.7 | n/a (480 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a (480 errors: t1 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| meta_schemas | JDBC | 1 | 6.9 / 12.6 / 21.5 | 6.1 / 9.0 / 9.8 | 7.5 / 10.3 / 12.3 | 12.2 / 21.0 / 23.7 |
| meta_schemas | JDBC | 8 | 12.9 / 32.9 / 46.4 | 11.7 / 26.5 / 43.8 | 33.3 / 64.5 / 77.7 | 46.0 / 80.6 / 101.3 |
| meta_schemas | JDBC | 32 | 24.8 / 77.5 / 199.1 | 22.8 / 63.7 / 112.4 | n/a (480 errors: t27 r-1: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRunt) | n/a (480 errors: t23 r-1: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRunt) |
| meta_schemas | ADBC | 1 | 5.0 / 8.6 / 11.3 | 4.9 / 7.8 / 8.2 | n/a | n/a |
| meta_schemas | ADBC | 8 | 19.0 / 36.9 / 47.7 | 19.2 / 38.9 / 53.1 | n/a | n/a (240 errors: t5 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| meta_schemas | ADBC | 32 | 52.9 / 128.5 / 229.8 | 53.5 / 123.3 / 175.1 | n/a (480 errors: t1 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a (480 errors: t1 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |

Answers per class are compared across servers in the run summary (`summary.md`, correctness gate).

### Scans (`SELECT * FROM tpch.lineitem`, SF10, MB/s of Arrow buffers) and server peak RSS

| metric | ours-new | ours-27f5 | up-native | up-main | ours-new vs best upstream |
|---|---|---|---|---|---|
| raw Flight, 1 stream | 418 | 446 | 603 | n/a | 0.98x |
| raw Flight, 4 streams | 502 | 499 | 807 | n/a | 0.87x |
| raw Flight, 8 streams | 463 | 462 | 823 | n/a | 0.80x |
| full export over ADBC | 532 | 514 | 761 | n/a | 0.96x |
| server peak RSS (MB) | 1708 | 1764 | 3699 | 283 | - |

### Server container (docker stats every ~5 s, all workloads of this setting)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| CPU % p50 (200 = both cores) | 202 | 204 | 0 | 1 |
| CPU % max | 212 | 210 | 207 | 212 |
| memory peak (MiB, limit 6144) | 1751 | 1794 | 6128 | 6140 |
| OOM-killed rounds | 0 / 18 | 0 / 6 | 3 / 6 | 3 / 6 |

## local, setting `t8`

### TPC-H SF10, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 2750 | 2799 | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 406 | 409 | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1541 | 1518 | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 995 | 998 | n/a | n/a | n/a |
| q05 | 6-way join | 1748 | 1770 | n/a | n/a | n/a |
| q06 | selective scan | 753 | 757 | n/a | n/a | n/a |
| q07 | joins, group by | 1689 | 1714 | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 2056 | 2047 | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 4025 | 4161 | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1876 | 1842 | n/a | n/a | n/a |
| q11 | HAVING subquery | 371 | 396 | n/a | n/a | n/a |
| q12 | join, CASE agg | 1051 | 1039 | n/a | n/a | n/a |
| q13 | outer join, LIKE | 3015 | 3036 | n/a | n/a | n/a |
| q14 | join, CASE | 1209 | 1213 | n/a | n/a | n/a |
| q15 | view / CTE, max | 1103 | 1101 | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 572 | 596 | n/a | n/a | n/a |
| q17 | correlated avg | 1737 | 1744 | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 3209 | 3242 | n/a | n/a | n/a |
| q19 | OR predicates | 1660 | 1671 | n/a | n/a | n/a |
| q20 | nested IN | 1436 | 1446 | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 5437 | 5403 | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 589 | 590 | n/a | n/a | n/a |
| **Score** | sum of the 0 queries every shown server answered | n/a | n/a | n/a | n/a | geomean n/a (0 q) |

- up-native: failed: advertised schema differs from the data (e.g. float64 vs decimal(38,4)): ADBC rejects the stream: q06; failed: subquery table not rewritten: DuckDB `schema "tpch" does not exist`: q04; failed: the server's schema resolver rejects it (upstream: single-table parser, `Can only select from ONE table`; `AVG` unsupported on main): q01 q02 q03 q05 q07 q08 q09 q10 q11 q12 q13 q14 q15 q16 q17 q18 q19 q20 q21 q22
- up-main: failed: advertised schema differs from the data (e.g. float64 vs decimal(38,4)): ADBC rejects the stream: q06; failed: subquery table not rewritten: DuckDB `schema "tpch" does not exist`: q04; failed: the server's schema resolver rejects it (upstream: single-table parser, `Can only select from ONE table`; `AVG` unsupported on main): q01 q02 q03 q05 q07 q08 q09 q10 q11 q12 q13 q14 q15 q16 q17 q18 q19 q20 q21 q22
- same runner: ours-27f5 / ours-new = 0.99 (sum of 22 warm medians, AMD EPYC 7763 64-Core Processor)
- the ours-new column is the median over all its jobs of this storage and setting (other runners and CPU types), ours-27f5 comes only from its own pair job: compare the two by the same-runner ratio above, not by the columns

### TPC-H SF1, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 371 | 385 | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 63 | 79 | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 172 | 188 | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 125 | 122 | n/a | n/a | n/a |
| q05 | 6-way join | 174 | 180 | n/a | n/a | n/a |
| q06 | selective scan | 95 | 107 | n/a | n/a | n/a |
| q07 | joins, group by | 190 | 204 | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 218 | 225 | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 314 | 314 | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 212 | 229 | n/a | n/a | n/a |
| q11 | HAVING subquery | 48 | 59 | n/a | n/a | n/a |
| q12 | join, CASE agg | 123 | 138 | n/a | n/a | n/a |
| q13 | outer join, LIKE | 292 | 304 | n/a | n/a | n/a |
| q14 | join, CASE | 138 | 146 | n/a | n/a | n/a |
| q15 | view / CTE, max | 103 | 106 | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 78 | 89 | n/a | n/a | n/a |
| q17 | correlated avg | 168 | 177 | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 393 | 401 | n/a | n/a | n/a |
| q19 | OR predicates | 183 | 193 | n/a | n/a | n/a |
| q20 | nested IN | 150 | 178 | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 453 | 473 | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 75 | 82 | n/a | n/a | n/a |
| **Score** | sum of the 0 queries every shown server answered | n/a | n/a | n/a | n/a | geomean n/a (0 q) |

- up-native: failed: advertised schema differs from the data (e.g. float64 vs decimal(38,4)): ADBC rejects the stream: q06; failed: subquery table not rewritten: DuckDB `schema "tpch" does not exist`: q04; failed: the server's schema resolver rejects it (upstream: single-table parser, `Can only select from ONE table`; `AVG` unsupported on main): q01 q02 q03 q05 q07 q08 q09 q10 q11 q12 q13 q14 q15 q16 q17 q18 q19 q20 q21 q22
- up-main: failed: advertised schema differs from the data (e.g. float64 vs decimal(38,4)): ADBC rejects the stream: q06; failed: subquery table not rewritten: DuckDB `schema "tpch" does not exist`: q04; failed: the server's schema resolver rejects it (upstream: single-table parser, `Can only select from ONE table`; `AVG` unsupported on main): q01 q02 q03 q05 q07 q08 q09 q10 q11 q12 q13 q14 q15 q16 q17 q18 q19 q20 q21 q22
- same runner: ours-27f5 / ours-new = 1.05 (sum of 22 warm medians, AMD EPYC 7763 64-Core Processor)
- the ours-new column is the median over all its jobs of this storage and setting (other runners and CPU types), ours-27f5 comes only from its own pair job: compare the two by the same-runner ratio above, not by the columns

### TPC-H SF10, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 2753 | 2763 | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 420 | 430 | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1493 | 1484 | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 1003 | 994 | n/a | n/a | n/a |
| q05 | 6-way join | 1762 | 1761 | n/a | n/a | n/a |
| q06 | selective scan | 754 | 764 | n/a | n/a | n/a |
| q07 | joins, group by | 1683 | 1695 | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 2060 | 2083 | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 3992 | 4060 | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1844 | 1878 | n/a | n/a | n/a |
| q11 | HAVING subquery | 361 | 374 | n/a | n/a | n/a |
| q12 | join, CASE agg | 1035 | 1040 | n/a | n/a | n/a |
| q13 | outer join, LIKE | 3043 | 3024 | n/a | n/a | n/a |
| q14 | join, CASE | 1217 | 1215 | n/a | n/a | n/a |
| q15 | view / CTE, max | 1099 | 1104 | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 600 | 626 | n/a | n/a | n/a |
| q17 | correlated avg | 1744 | 1751 | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 3770 | 3783 | n/a | n/a | n/a |
| q19 | OR predicates | 1662 | 1690 | n/a | n/a | n/a |
| q20 | nested IN | 1432 | 1439 | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 5401 | 5452 | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 603 | 618 | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 39731 | 40028 | n/a | n/a | geomean n/a (0 q) |

- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- same runner: ours-27f5 / ours-new = 1.01 (sum of 22 warm medians, AMD EPYC 7763 64-Core Processor)
- the ours-new column is the median over all its jobs of this storage and setting (other runners and CPU types), ours-27f5 comes only from its own pair job: compare the two by the same-runner ratio above, not by the columns

### TPC-H SF1, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 387 | 402 | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 79 | 89 | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 186 | 196 | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 124 | 141 | n/a | n/a | n/a |
| q05 | 6-way join | 181 | 188 | n/a | n/a | n/a |
| q06 | selective scan | 102 | 108 | n/a | n/a | n/a |
| q07 | joins, group by | 184 | 194 | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 218 | 236 | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 305 | 332 | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 219 | 230 | n/a | n/a | n/a |
| q11 | HAVING subquery | 62 | 68 | n/a | n/a | n/a |
| q12 | join, CASE agg | 130 | 145 | n/a | n/a | n/a |
| q13 | outer join, LIKE | 297 | 292 | n/a | n/a | n/a |
| q14 | join, CASE | 144 | 144 | n/a | n/a | n/a |
| q15 | view / CTE, max | 103 | 110 | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 111 | 111 | n/a | n/a | n/a |
| q17 | correlated avg | 174 | 178 | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 402 | 406 | n/a | n/a | n/a |
| q19 | OR predicates | 193 | 190 | n/a | n/a | n/a |
| q20 | nested IN | 153 | 162 | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 446 | 447 | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 78 | 82 | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 4278 | 4451 | n/a | n/a | geomean n/a (0 q) |

- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- same runner: ours-27f5 / ours-new = 1.04 (sum of 22 warm medians, AMD EPYC 7763 64-Core Processor)
- the ours-new column is the median over all its jobs of this storage and setting (other runners and CPU types), ours-27f5 comes only from its own pair job: compare the two by the same-runner ratio above, not by the columns

### Small queries (ms, p50 / p95 / p99 over all rounds)

| class | client | c | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|---|---|
| point_orders | JDBC | 1 | 25.1 / 35.2 / 48.3 | 28.1 / 40.1 / 42.8 | 27.7 / 71.9 / 85.6 | n/a (60 errors: t0 r-1: java.sql.SQLException: Error while executing SQL "SELECT o_orderkey, o_) |
| point_orders | JDBC | 8 | 143.2 / 220.6 / 347.2 | 146.8 / 222.1 / 258.2 | 102.5 / 230.5 / 393.2 | n/a (240 errors: t2 r-1: java.sql.SQLException: Error while executing SQL "SELECT o_orderkey, o_) |
| point_orders | JDBC | 32 | 583.3 / 1108.0 / 1621.1 | 625.1 / 1068.7 / 1292.6 | n/a (480 errors: t3 r-1: java.sql.SQLException: Error while executing SQL "SELECT o_orderkey, o_) | n/a (480 errors: t14 r-1: java.sql.SQLException: Error while executing SQL "SELECT o_orderkey, o) |
| point_orders | ADBC | 1 | 17.1 / 25.1 / 47.2 | 20.9 / 30.5 / 31.9 | n/a | n/a |
| point_orders | ADBC | 8 | 107.8 / 188.4 / 215.5 | 139.7 / 213.0 / 262.5 | n/a | n/a (240 errors: t4 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| point_orders | ADBC | 32 | 490.9 / 868.8 / 1101.6 | 496.7 / 839.7 / 1088.5 | n/a (480 errors: t0 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a (480 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| point_lineitem | JDBC | 1 | 34.5 / 45.8 / 54.9 | 38.3 / 49.4 / 63.1 | 36.7 / 77.4 / 91.1 | n/a (60 errors: t0 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l_) |
| point_lineitem | JDBC | 8 | 199.8 / 303.7 / 539.7 | 205.4 / 289.5 / 433.3 | 151.7 / 284.8 / 420.2 | n/a (240 errors: t3 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l_) |
| point_lineitem | JDBC | 32 | 824.1 / 1391.1 / 1712.8 | 877.0 / 1290.2 / 1552.5 | n/a (480 errors: t10 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l) | n/a (480 errors: t21 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l) |
| point_lineitem | ADBC | 1 | 25.3 / 38.8 / 54.3 | 30.2 / 42.6 / 46.7 | n/a | n/a |
| point_lineitem | ADBC | 8 | 181.5 / 286.3 / 340.1 | 200.8 / 313.0 / 401.2 | n/a | n/a (240 errors: t4 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| point_lineitem | ADBC | 32 | 780.3 / 1243.6 / 1468.8 | 783.9 / 1198.4 / 1384.7 | n/a (480 errors: t0 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a (480 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| count_filter | JDBC | 1 | 50.3 / 62.2 / 84.2 | 54.3 / 65.8 / 70.7 | 52.1 / 64.8 / 68.3 | n/a (60 errors: t0 r-1: java.sql.SQLException: Error while executing SQL "SELECT count(*) FROM) |
| count_filter | JDBC | 8 | 205.2 / 276.2 / 316.7 | 220.7 / 296.9 / 306.1 | 171.2 / 412.8 / 477.4 | n/a (240 errors: t4 r-1: java.sql.SQLException: Error while executing SQL "SELECT count(*) FROM) |
| count_filter | JDBC | 32 | 816.7 / 1385.5 / 2074.6 | 913.1 / 1786.9 / 2216.3 | n/a (480 errors: t5 r-1: java.sql.SQLException: Error while executing SQL "SELECT count(*) FROM) | n/a (480 errors: t16 r-1: java.sql.SQLException: Error while executing SQL "SELECT count(*) FROM) |
| count_filter | ADBC | 1 | 42.9 / 56.4 / 66.5 | 47.3 / 58.6 / 59.6 | n/a | n/a |
| count_filter | ADBC | 8 | 203.2 / 292.4 / 340.3 | 220.4 / 292.2 / 331.3 | n/a | n/a (240 errors: t5 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| count_filter | ADBC | 32 | 826.6 / 1291.8 / 1552.1 | 950.9 / 1504.6 / 1742.4 | n/a (480 errors: t0 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a (480 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| limit10_ob | JDBC | 1 | 47.0 / 61.0 / 67.7 | 54.2 / 70.1 / 88.3 | 10632.9 / 11184.6 / 11523.8 | n/a (60 errors: t0 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l_) |
| limit10_ob | JDBC | 8 | 275.9 / 412.0 / 457.2 | 291.3 / 399.9 / 449.9 | n/a (101 errors: t7 r2: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRuntim) | n/a (240 errors: t5 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l_) |
| limit10_ob | JDBC | 32 | 1134.6 / 1774.7 / 2064.9 | 1191.8 / 1865.9 / 2393.3 | n/a (480 errors: t13 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l) | n/a (480 errors: t23 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l) |
| limit10_ob | ADBC | 1 | 40.4 / 57.9 / 65.9 | 44.2 / 66.7 / 71.6 | n/a | n/a |
| limit10_ob | ADBC | 8 | 269.0 / 408.4 / 473.8 | 289.6 / 397.0 / 457.9 | n/a | n/a (240 errors: t2 r-1: OperationalError: IO: [FlightSQL] error reading from server: EOF (Unava) |
| limit10_ob | ADBC | 32 | 1159.1 / 1754.1 / 2019.6 | 1278.5 / 1934.5 / 2285.5 | n/a (480 errors: t0 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a (480 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| meta_tables | JDBC | 1 | 8.5 / 13.1 / 19.6 | 8.1 / 12.8 / 16.4 | 11.3 / 275.7 / 294.0 | 13.5 / 22.9 / 31.4 |
| meta_tables | JDBC | 8 | 13.9 / 35.6 / 53.3 | 13.8 / 437.0 / 917.1 | 32.0 / 1325.1 / 1907.6 | 42.1 / 76.1 / 87.3 |
| meta_tables | JDBC | 32 | 37.0 / 1183.2 / 2086.3 | 36.0 / 490.4 / 1816.7 | n/a (480 errors: t13 r-1: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRunt) | n/a (480 errors: t23 r-1: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRunt) |
| meta_tables | ADBC | 1 | 8.8 / 13.3 / 16.6 | 7.4 / 10.4 / 12.5 | n/a | n/a |
| meta_tables | ADBC | 8 | 34.0 / 313.7 / 580.3 | 33.3 / 64.0 / 77.8 | n/a | n/a (240 errors: t7 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| meta_tables | ADBC | 32 | 110.8 / 672.9 / 2461.4 | 112.0 / 1613.1 / 3300.5 | n/a (480 errors: t0 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a (480 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| meta_schemas | JDBC | 1 | 6.6 / 10.3 / 12.6 | 5.8 / 8.9 / 10.3 | 7.9 / 12.0 / 13.7 | 12.1 / 19.1 / 22.0 |
| meta_schemas | JDBC | 8 | 14.3 / 37.7 / 51.5 | 11.9 / 27.3 / 45.8 | 35.6 / 79.8 / 107.9 | 39.3 / 69.9 / 80.0 |
| meta_schemas | JDBC | 32 | 27.6 / 84.3 / 135.6 | 25.6 / 76.8 / 133.9 | n/a (480 errors: t3 r-1: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRunti) | n/a (480 errors: t23 r-1: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRunt) |
| meta_schemas | ADBC | 1 | 5.3 / 8.0 / 11.5 | 4.8 / 7.6 / 8.1 | n/a | n/a |
| meta_schemas | ADBC | 8 | 20.6 / 44.3 / 61.4 | 20.8 / 54.5 / 68.9 | n/a | n/a (240 errors: t3 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |
| meta_schemas | ADBC | 32 | 58.8 / 147.8 / 229.4 | 55.9 / 119.7 / 185.2 | n/a (480 errors: t0 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a (480 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) |

Answers per class are compared across servers in the run summary (`summary.md`, correctness gate).

### Scans (`SELECT * FROM tpch.lineitem`, SF10, MB/s of Arrow buffers) and server peak RSS

| metric | ours-new | ours-27f5 | up-native | up-main | ours-new vs best upstream |
|---|---|---|---|---|---|
| raw Flight, 1 stream | 425 | 422 | 399 | n/a | 1.09x |
| raw Flight, 4 streams | 455 | 428 | 558 | n/a | 0.84x |
| raw Flight, 8 streams | 405 | 381 | 593 | n/a | 0.68x |
| full export over ADBC | 501 | 485 | 518 | n/a | 1.01x |
| server peak RSS (MB) | 1864 | 1922 | 3920 | 283 | - |

### Server container (docker stats every ~5 s, all workloads of this setting)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| CPU % p50 (200 = both cores) | 201 | 201 | 1 | 0 |
| CPU % max | 210 | 204 | 215 | 200 |
| memory peak (MiB, limit 6144) | 1917 | 1924 | 6139 | 6133 |
| OOM-killed rounds | 0 / 18 | 0 / 6 | 3 / 6 | 3 / 6 |

## s3, setting `def`

### TPC-H SF10, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 8855 | 10617 | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 3906 | 4490 | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 15946 | 18699 | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 10037 | 11527 | n/a | n/a | n/a |
| q05 | 6-way join | 18028 | 21690 | n/a | n/a | n/a |
| q06 | selective scan | 15323 | 18257 | n/a | n/a | n/a |
| q07 | joins, group by | 20660 | 24513 | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 23548 | 28259 | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 24293 | 28960 | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 14786 | 17536 | n/a | n/a | n/a |
| q11 | HAVING subquery | 3154 | 3747 | n/a | n/a | n/a |
| q12 | join, CASE agg | 17277 | 20340 | n/a | n/a | n/a |
| q13 | outer join, LIKE | 4659 | 5518 | n/a | n/a | n/a |
| q14 | join, CASE | 15394 | 19489 | n/a | n/a | n/a |
| q15 | view / CTE, max | 15911 | 17445 | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 1416 | 1665 | n/a | n/a | n/a |
| q17 | correlated avg | 19771 | 26397 | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 15490 | 18244 | n/a | n/a | n/a |
| q19 | OR predicates | 15955 | 18759 | n/a | n/a | n/a |
| q20 | nested IN | 18398 | 22303 | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 41116 | 52387 | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 2168 | 2566 | n/a | n/a | n/a |
| **Score** | sum of the 0 queries every shown server answered | n/a | n/a | n/a | n/a | geomean n/a (0 q) |

- up-native: failed: advertised schema differs from the data (e.g. float64 vs decimal(38,4)): ADBC rejects the stream: q06; failed: subquery table not rewritten: DuckDB `schema "tpch" does not exist`: q04; failed: the server's schema resolver rejects it (upstream: single-table parser, `Can only select from ONE table`; `AVG` unsupported on main): q01 q02 q03 q05 q07 q08 q09 q10 q11 q12 q13 q14 q15 q16 q17 q18 q19 q20 q21 q22
- up-main: not run: not in this setting's jobs
- same runner: ours-27f5 / ours-new = 1.01 (sum of 22 warm medians, AMD EPYC 9V45 96-Core Processor)
- the ours-new column is the median over all its jobs of this storage and setting (other runners and CPU types), ours-27f5 comes only from its own pair job: compare the two by the same-runner ratio above, not by the columns

### TPC-H SF1, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 758 | 912 | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 442 | 513 | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1530 | 1821 | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 942 | 1131 | n/a | n/a | n/a |
| q05 | 6-way join | 1577 | 1840 | n/a | n/a | n/a |
| q06 | selective scan | 1338 | 1631 | n/a | n/a | n/a |
| q07 | joins, group by | 1764 | 2095 | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 2047 | 2394 | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 2138 | 2469 | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1482 | 1702 | n/a | n/a | n/a |
| q11 | HAVING subquery | 344 | 387 | n/a | n/a | n/a |
| q12 | join, CASE agg | 1678 | 1899 | n/a | n/a | n/a |
| q13 | outer join, LIKE | 371 | 462 | n/a | n/a | n/a |
| q14 | join, CASE | 1400 | 1703 | n/a | n/a | n/a |
| q15 | view / CTE, max | 1178 | 1407 | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 154 | 173 | n/a | n/a | n/a |
| q17 | correlated avg | 1904 | 2295 | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 1614 | 1800 | n/a | n/a | n/a |
| q19 | OR predicates | 1602 | 1770 | n/a | n/a | n/a |
| q20 | nested IN | 1538 | 1839 | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 2949 | 3496 | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 212 | 248 | n/a | n/a | n/a |
| **Score** | sum of the 0 queries every shown server answered | n/a | n/a | n/a | n/a | geomean n/a (0 q) |

- up-native: failed: advertised schema differs from the data (e.g. float64 vs decimal(38,4)): ADBC rejects the stream: q06; failed: subquery table not rewritten: DuckDB `schema "tpch" does not exist`: q04; failed: the server's schema resolver rejects it (upstream: single-table parser, `Can only select from ONE table`; `AVG` unsupported on main): q01 q02 q03 q05 q07 q08 q09 q10 q11 q12 q13 q14 q15 q16 q17 q18 q19 q20 q21 q22
- up-main: not run: not in this setting's jobs
- same runner: ours-27f5 / ours-new = 1.01 (sum of 22 warm medians, AMD EPYC 9V45 96-Core Processor)
- the ours-new column is the median over all its jobs of this storage and setting (other runners and CPU types), ours-27f5 comes only from its own pair job: compare the two by the same-runner ratio above, not by the columns

### TPC-H SF10, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 7521 | 7464 | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 4549 | 4606 | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 20050 | 18889 | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 11407 | 11497 | n/a | n/a | n/a |
| q05 | 6-way join | 21327 | 21094 | n/a | n/a | n/a |
| q06 | selective scan | 16234 | 16222 | n/a | n/a | n/a |
| q07 | joins, group by | 24155 | 24547 | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 28140 | 28118 | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 34146 | 37404 | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 17368 | 16985 | n/a | n/a | n/a |
| q11 | HAVING subquery | 3761 | 3697 | n/a | n/a | n/a |
| q12 | join, CASE agg | 19600 | 19355 | n/a | n/a | n/a |
| q13 | outer join, LIKE | 5612 | 5440 | n/a | n/a | n/a |
| q14 | join, CASE | 17527 | 17752 | n/a | n/a | n/a |
| q15 | view / CTE, max | 17256 | 17329 | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 1574 | 1474 | n/a | n/a | n/a |
| q17 | correlated avg | 23402 | 23505 | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 17745 | 17807 | n/a | n/a | n/a |
| q19 | OR predicates | 23578 | 26659 | n/a | n/a | n/a |
| q20 | nested IN | 22256 | 22344 | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 43746 | 42841 | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 2534 | 2500 | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 383488 | 387529 | n/a | n/a | geomean n/a (0 q) |

- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- same runner: ours-27f5 / ours-new = 1.01 (sum of 22 warm medians, AMD EPYC 9V45 96-Core Processor)
- the ours-new column is the median over all its jobs of this storage and setting (other runners and CPU types), ours-27f5 comes only from its own pair job: compare the two by the same-runner ratio above, not by the columns

### TPC-H SF1, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 695 | 692 | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 371 | 413 | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1292 | 1261 | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 1099 | 1167 | n/a | n/a | n/a |
| q05 | 6-way join | 1855 | 1809 | n/a | n/a | n/a |
| q06 | selective scan | 1510 | 1508 | n/a | n/a | n/a |
| q07 | joins, group by | 2074 | 2083 | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 2446 | 2662 | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 2447 | 2411 | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1609 | 1661 | n/a | n/a | n/a |
| q11 | HAVING subquery | 358 | 344 | n/a | n/a | n/a |
| q12 | join, CASE agg | 1843 | 1953 | n/a | n/a | n/a |
| q13 | outer join, LIKE | 436 | 466 | n/a | n/a | n/a |
| q14 | join, CASE | 1694 | 1700 | n/a | n/a | n/a |
| q15 | view / CTE, max | 1357 | 1359 | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 183 | 181 | n/a | n/a | n/a |
| q17 | correlated avg | 2247 | 2260 | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 1737 | 1839 | n/a | n/a | n/a |
| q19 | OR predicates | 1752 | 1752 | n/a | n/a | n/a |
| q20 | nested IN | 1744 | 1847 | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 3448 | 3410 | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 246 | 251 | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 32443 | 33029 | n/a | n/a | geomean n/a (0 q) |

- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- same runner: ours-27f5 / ours-new = 1.02 (sum of 22 warm medians, AMD EPYC 9V45 96-Core Processor)
- the ours-new column is the median over all its jobs of this storage and setting (other runners and CPU types), ours-27f5 comes only from its own pair job: compare the two by the same-runner ratio above, not by the columns

### Small queries (ms, p50 / p95 / p99 over all rounds)

| class | client | c | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|---|---|
| point_orders | JDBC | 1 | 33.6 / 43.4 / 55.4 | 38.7 / 52.5 / 60.8 | 46.2 / 87.4 / 1163.5 | n/a |
| point_orders | JDBC | 8 | 412.4 / 637.5 / 794.5 | 425.7 / 685.7 / 1130.4 | n/a (76 errors: t7 r5: java.sql.SQLException: Error while executing SQL "SELECT o_orderkey, o_c) | n/a |
| point_orders | JDBC | 32 | 1450.2 / 3109.5 / 9076.0 | 1522.0 / 2819.4 / 4026.9 | n/a (480 errors: t30 r-1: java.sql.SQLException: Error while executing SQL "SELECT o_orderkey, o) | n/a |
| point_orders | ADBC | 1 | 23.9 / 37.3 / 47.4 | 28.2 / 46.4 / 148.6 | n/a | n/a |
| point_orders | ADBC | 8 | 394.1 / 633.3 / 789.4 | 447.0 / 794.8 / 946.1 | n/a (240 errors: t6 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "error readi) | n/a |
| point_orders | ADBC | 32 | 1425.0 / 2727.4 / 4581.5 | 1601.8 / 3333.9 / 8736.3 | n/a (480 errors: t0 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| point_lineitem | JDBC | 1 | 29.1 / 46.8 / 49.5 | 34.8 / 55.5 / 132.2 | 45.3 / 118.4 / 2954.3 | n/a |
| point_lineitem | JDBC | 8 | 251.4 / 400.9 / 524.6 | 263.3 / 4242.3 / 7517.9 | n/a (74 errors: t7 r5: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l_l) | n/a |
| point_lineitem | JDBC | 32 | 851.1 / 3012.9 / 26287.6 | 866.8 / 8914.6 / 20416.5 | n/a (480 errors: t3 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l_) | n/a |
| point_lineitem | ADBC | 1 | 20.2 / 37.2 / 40.8 | 25.2 / 41.5 / 47.8 | n/a | n/a |
| point_lineitem | ADBC | 8 | 253.8 / 553.4 / 5521.3 | 261.7 / 462.0 / 555.2 | n/a (240 errors: t6 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "error readi) | n/a |
| point_lineitem | ADBC | 32 | 844.5 / 11678.3 / 22162.7 | 949.1 / 10278.9 / 19062.1 | n/a (480 errors: t0 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| count_filter | JDBC | 1 | 639.0 / 739.6 / 755.5 | 640.2 / 725.3 / 760.5 | 52.9 / 74.6 / 88.0 | n/a |
| count_filter | JDBC | 8 | 5337.2 / 6302.1 / 9688.8 | 4996.6 / 5693.6 / 8761.6 | n/a (72 errors: t7 r5: java.sql.SQLException: Error while executing SQL "SELECT count(*) FROM t) | n/a |
| count_filter | JDBC | 32 | 16943.1 / 32277.0 / 45735.5 | 16679.9 / 26980.3 / 29454.1 | n/a (480 errors: t28 r-1: java.sql.SQLException: Error while executing SQL "SELECT count(*) FROM) | n/a |
| count_filter | ADBC | 1 | 648.5 / 734.6 / 756.3 | 675.9 / 753.9 / 801.3 | n/a | n/a |
| count_filter | ADBC | 8 | 5288.1 / 6060.0 / 6297.4 | 5326.4 / 7987.1 / 8183.7 | n/a (240 errors: t6 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "error readi) | n/a |
| count_filter | ADBC | 32 | 16744.5 / 27464.8 / 36763.3 | 16337.1 / 46134.3 / 55985.2 | n/a (480 errors: t0 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| limit10_ob | JDBC | 1 | 130.3 / 185.1 / 211.2 | 112.8 / 139.2 / 178.3 | 8002.2 / 8438.1 / 9864.6 | n/a |
| limit10_ob | JDBC | 8 | 809.8 / 1102.2 / 1240.1 | 786.5 / 1455.5 / 7198.0 | n/a (126 errors: t2 r3: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRuntim) | n/a |
| limit10_ob | JDBC | 32 | 2715.9 / 17685.8 / 52021.4 | 2741.9 / 5697.1 / 33658.3 | n/a (480 errors: t21 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l) | n/a |
| limit10_ob | ADBC | 1 | 128.4 / 179.4 / 193.9 | 110.6 / 140.8 / 152.4 | n/a | n/a |
| limit10_ob | ADBC | 8 | 811.7 / 1222.3 / 5345.3 | 837.1 / 1335.4 / 1608.3 | n/a (240 errors: t5 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "error readi) | n/a |
| limit10_ob | ADBC | 32 | 2716.5 / 17887.8 / 34754.2 | 2850.5 / 5683.0 / 28653.6 | n/a (480 errors: t0 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| meta_tables | JDBC | 1 | 9.1 / 13.4 / 14.5 | 8.6 / 13.4 / 14.7 | 10.5 / 105.3 / 121.7 | n/a |
| meta_tables | JDBC | 8 | 5.6 / 15.2 / 21.7 | 5.4 / 12.6 / 18.6 | n/a (82 errors: t7 r4: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRuntim) | n/a |
| meta_tables | JDBC | 32 | 6.6 / 23.7 / 54.4 | 7.3 / 27.5 / 40.0 | n/a (480 errors: t18 r-1: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRunt) | n/a |
| meta_tables | ADBC | 1 | 8.6 / 14.4 / 18.6 | 7.8 / 13.3 / 17.2 | n/a | n/a |
| meta_tables | ADBC | 8 | 9.1 / 21.2 / 30.0 | 8.1 / 20.2 / 37.6 | n/a (240 errors: t6 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "error readi) | n/a |
| meta_tables | ADBC | 32 | 19.9 / 51.8 / 76.5 | 17.8 / 51.3 / 84.2 | n/a (480 errors: t0 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| meta_schemas | JDBC | 1 | 6.8 / 11.1 / 13.4 | 6.5 / 11.3 / 14.7 | 7.7 / 12.0 / 12.5 | n/a |
| meta_schemas | JDBC | 8 | 4.8 / 15.8 / 29.5 | 4.4 / 12.8 / 20.6 | n/a (78 errors: t7 r5: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRuntim) | n/a |
| meta_schemas | JDBC | 32 | 6.5 / 32.0 / 62.8 | 5.7 / 29.1 / 44.2 | n/a (480 errors: t18 r-1: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRunt) | n/a |
| meta_schemas | ADBC | 1 | 5.3 / 8.7 / 11.6 | 5.0 / 7.5 / 9.3 | n/a | n/a |
| meta_schemas | ADBC | 8 | 6.1 / 16.5 / 26.5 | 5.6 / 14.1 / 19.7 | n/a (240 errors: t6 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "error readi) | n/a |
| meta_schemas | ADBC | 32 | 12.6 / 48.9 / 84.5 | 11.6 / 43.4 / 118.8 | n/a (480 errors: t0 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |

Answers per class are compared across servers in the run summary (`summary.md`, correctness gate).

### Scans (`SELECT * FROM tpch.lineitem`, SF10, MB/s of Arrow buffers) and server peak RSS

| metric | ours-new | ours-27f5 | up-native | up-main | ours-new vs best upstream |
|---|---|---|---|---|---|
| raw Flight, 1 stream | 396 | 409 | 375 | n/a | 1.06x |
| raw Flight, 4 streams | 479 | 486 | 588 | n/a | 0.82x |
| raw Flight, 8 streams | 457 | 461 | 613 | n/a | 0.75x |
| full export over ADBC | 431 | 418 | 552 | n/a | 0.77x |
| server peak RSS (MB) | 2696 | 2601 | 5745 | n/a | - |

### Server container (docker stats every ~5 s, all workloads of this setting)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| CPU % p50 (200 = both cores) | 29 | 20 | 154 | n/a |
| CPU % max | 211 | 210 | 215 | n/a |
| memory peak (MiB, limit 6144) | 2772 | 2553 | 6077 | n/a |
| OOM-killed rounds | 0 / 12 | 0 / 6 | 3 / 6 | n/a |

## s3, setting `t8`

### TPC-H SF10, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 10120 | 10350 | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 4330 | 4474 | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 16824 | 24798 | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 10685 | 11043 | n/a | n/a | n/a |
| q05 | 6-way join | 23185 | 23243 | n/a | n/a | n/a |
| q06 | selective scan | 14718 | 11003 | n/a | n/a | n/a |
| q07 | joins, group by | 22996 | 24327 | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 25381 | 28550 | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 27049 | 28736 | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 18362 | 16896 | n/a | n/a | n/a |
| q11 | HAVING subquery | 3367 | 3601 | n/a | n/a | n/a |
| q12 | join, CASE agg | 17810 | 25858 | n/a | n/a | n/a |
| q13 | outer join, LIKE | 4620 | 5854 | n/a | n/a | n/a |
| q14 | join, CASE | 16703 | 17797 | n/a | n/a | n/a |
| q15 | view / CTE, max | 16439 | 12730 | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 1434 | 1181 | n/a | n/a | n/a |
| q17 | correlated avg | 21981 | 19117 | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 16882 | 17918 | n/a | n/a | n/a |
| q19 | OR predicates | 17616 | 18023 | n/a | n/a | n/a |
| q20 | nested IN | 24788 | 21912 | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 37895 | 43137 | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 2322 | 2826 | n/a | n/a | n/a |
| **Score** | sum of the 0 queries every shown server answered | n/a | n/a | n/a | n/a | geomean n/a (0 q) |

- up-native: failed: advertised schema differs from the data (e.g. float64 vs decimal(38,4)): ADBC rejects the stream: q06; failed: subquery table not rewritten: DuckDB `schema "tpch" does not exist`: q04; failed: the server's schema resolver rejects it (upstream: single-table parser, `Can only select from ONE table`; `AVG` unsupported on main): q01 q02 q03 q05 q07 q08 q09 q10 q11 q12 q13 q14 q15 q16 q17 q18 q19 q20 q21 q22
- up-main: not run: not in this setting's jobs
- same runner: ours-27f5 / ours-new = 1.03 (sum of 22 warm medians, AMD EPYC 9V74 80-Core Processor)
- the ours-new column is the median over all its jobs of this storage and setting (other runners and CPU types), ours-27f5 comes only from its own pair job: compare the two by the same-runner ratio above, not by the columns

### TPC-H SF1, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 728 | 724 | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 447 | 534 | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1580 | 1548 | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 1013 | 1042 | n/a | n/a | n/a |
| q05 | 6-way join | 1616 | 1653 | n/a | n/a | n/a |
| q06 | selective scan | 1370 | 1096 | n/a | n/a | n/a |
| q07 | joins, group by | 1838 | 1914 | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 2214 | 2085 | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 2308 | 2460 | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1538 | 1964 | n/a | n/a | n/a |
| q11 | HAVING subquery | 361 | 381 | n/a | n/a | n/a |
| q12 | join, CASE agg | 1584 | 1842 | n/a | n/a | n/a |
| q13 | outer join, LIKE | 438 | 433 | n/a | n/a | n/a |
| q14 | join, CASE | 1534 | 1659 | n/a | n/a | n/a |
| q15 | view / CTE, max | 1240 | 1468 | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 146 | 145 | n/a | n/a | n/a |
| q17 | correlated avg | 1974 | 2200 | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 1530 | 1628 | n/a | n/a | n/a |
| q19 | OR predicates | 1424 | 1575 | n/a | n/a | n/a |
| q20 | nested IN | 1318 | 1770 | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 2969 | 3159 | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 222 | 238 | n/a | n/a | n/a |
| **Score** | sum of the 0 queries every shown server answered | n/a | n/a | n/a | n/a | geomean n/a (0 q) |

- up-native: failed: advertised schema differs from the data (e.g. float64 vs decimal(38,4)): ADBC rejects the stream: q06; failed: subquery table not rewritten: DuckDB `schema "tpch" does not exist`: q04; failed: the server's schema resolver rejects it (upstream: single-table parser, `Can only select from ONE table`; `AVG` unsupported on main): q01 q02 q03 q05 q07 q08 q09 q10 q11 q12 q13 q14 q15 q16 q17 q18 q19 q20 q21 q22
- up-main: not run: not in this setting's jobs
- same runner: ours-27f5 / ours-new = 1.00 (sum of 22 warm medians, AMD EPYC 9V74 80-Core Processor)
- the ours-new column is the median over all its jobs of this storage and setting (other runners and CPU types), ours-27f5 comes only from its own pair job: compare the two by the same-runner ratio above, not by the columns

### TPC-H SF10, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 9217 | 8286 | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 3760 | 3046 | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 18109 | 13023 | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 11202 | 9293 | n/a | n/a | n/a |
| q05 | 6-way join | 21725 | 21378 | n/a | n/a | n/a |
| q06 | selective scan | 15310 | 13648 | n/a | n/a | n/a |
| q07 | joins, group by | 23912 | 19296 | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 28486 | 20411 | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 47783 | 20016 | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 16980 | 11644 | n/a | n/a | n/a |
| q11 | HAVING subquery | 3887 | 3687 | n/a | n/a | n/a |
| q12 | join, CASE agg | 18639 | 17856 | n/a | n/a | n/a |
| q13 | outer join, LIKE | 5616 | 4526 | n/a | n/a | n/a |
| q14 | join, CASE | 18125 | 14686 | n/a | n/a | n/a |
| q15 | view / CTE, max | 17600 | 12784 | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 1817 | 1476 | n/a | n/a | n/a |
| q17 | correlated avg | 23942 | 16212 | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 17573 | 12098 | n/a | n/a | n/a |
| q19 | OR predicates | 19796 | 12055 | n/a | n/a | n/a |
| q20 | nested IN | 22512 | 14667 | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 43809 | 47534 | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 2874 | 2135 | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 392674 | 299757 | n/a | n/a | geomean n/a (0 q) |

- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- same runner: ours-27f5 / ours-new = 0.76 (sum of 22 warm medians, AMD EPYC 9V74 80-Core Processor)
- the ours-new column is the median over all its jobs of this storage and setting (other runners and CPU types), ours-27f5 comes only from its own pair job: compare the two by the same-runner ratio above, not by the columns

### TPC-H SF1, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 903 | 706 | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 521 | 361 | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1147 | 1454 | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 693 | 796 | n/a | n/a | n/a |
| q05 | 6-way join | 1318 | 2802 | n/a | n/a | n/a |
| q06 | selective scan | 1460 | 1468 | n/a | n/a | n/a |
| q07 | joins, group by | 1980 | 2321 | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 2700 | 2500 | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 2565 | 2407 | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1564 | 1623 | n/a | n/a | n/a |
| q11 | HAVING subquery | 255 | 331 | n/a | n/a | n/a |
| q12 | join, CASE agg | 1708 | 1556 | n/a | n/a | n/a |
| q13 | outer join, LIKE | 353 | 425 | n/a | n/a | n/a |
| q14 | join, CASE | 1722 | 1526 | n/a | n/a | n/a |
| q15 | view / CTE, max | 1443 | 1531 | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 266 | 446 | n/a | n/a | n/a |
| q17 | correlated avg | 2313 | 1576 | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 1607 | 1917 | n/a | n/a | n/a |
| q19 | OR predicates | 1628 | 1662 | n/a | n/a | n/a |
| q20 | nested IN | 1735 | 2366 | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 3114 | 4454 | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 181 | 173 | n/a | n/a | n/a |
| **Score** | sum of the 22 queries every shown server answered | 31176 | 34401 | n/a | n/a | geomean n/a (0 q) |

- up-native: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)
- same runner: ours-27f5 / ours-new = 1.10 (sum of 22 warm medians, AMD EPYC 9V74 80-Core Processor)
- the ours-new column is the median over all its jobs of this storage and setting (other runners and CPU types), ours-27f5 comes only from its own pair job: compare the two by the same-runner ratio above, not by the columns

### Small queries (ms, p50 / p95 / p99 over all rounds)

| class | client | c | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|---|---|
| point_orders | JDBC | 1 | 33.9 / 141.4 / 184.5 | 35.1 / 119.9 / 200.0 | 63.3 / 506.2 / 1931.1 | n/a |
| point_orders | JDBC | 8 | 483.4 / 1003.8 / 1347.8 | 525.4 / 997.2 / 1368.9 | n/a (40 errors: t2 r5: java.sql.SQLException: Error while executing SQL "SELECT o_orderkey, o_c) | n/a |
| point_orders | JDBC | 32 | 1800.0 / 3224.2 / 4270.2 | 1985.2 / 3766.5 / 12173.7 | n/a (480 errors: t2 r-1: java.sql.SQLException: Error while executing SQL "SELECT o_orderkey, o_) | n/a |
| point_orders | ADBC | 1 | 24.5 / 210.6 / 349.7 | 26.8 / 70.5 / 84.3 | n/a | n/a |
| point_orders | ADBC | 8 | 519.4 / 955.6 / 1160.3 | 540.3 / 948.7 / 1151.7 | n/a (80 errors: t5 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| point_orders | ADBC | 32 | 2052.7 / 5160.8 / 21432.5 | 2095.7 / 3941.6 / 16184.7 | n/a (480 errors: t4 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| point_lineitem | JDBC | 1 | 27.6 / 106.0 / 514.4 | 29.5 / 224.5 / 351.8 | 49.0 / 393.5 / 7210.0 | n/a |
| point_lineitem | JDBC | 8 | 262.6 / 628.2 / 5242.6 | 267.3 / 554.6 / 912.1 | n/a (39 errors: t2 r5: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l_l) | n/a |
| point_lineitem | JDBC | 32 | 887.1 / 1683.3 / 2464.5 | 954.5 / 13197.5 / 21295.2 | n/a (480 errors: t27 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l) | n/a |
| point_lineitem | ADBC | 1 | 19.1 / 106.0 / 316.5 | 22.2 / 139.8 / 198.2 | n/a | n/a |
| point_lineitem | ADBC | 8 | 262.7 / 514.7 / 673.4 | 295.5 / 520.5 / 5984.1 | n/a (80 errors: t5 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| point_lineitem | ADBC | 32 | 950.5 / 4659.3 / 43064.4 | 969.2 / 1675.2 / 12950.9 | n/a (480 errors: t4 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| count_filter | JDBC | 1 | 633.5 / 1038.0 / 1572.4 | 631.9 / 1093.1 / 1170.0 | 44.7 / 54.7 / 60.1 | n/a |
| count_filter | JDBC | 8 | 3229.3 / 4268.2 / 8858.7 | 2984.0 / 6701.9 / 10803.4 | n/a (38 errors: t2 r5: java.sql.SQLException: Error while executing SQL "SELECT count(*) FROM t) | n/a |
| count_filter | JDBC | 32 | 10712.6 / 14513.6 / 28371.4 | 8331.6 / 12357.5 / 25240.8 | n/a (480 errors: t22 r-1: java.sql.SQLException: Error while executing SQL "SELECT count(*) FROM) | n/a |
| count_filter | ADBC | 1 | 653.3 / 1368.8 / 1681.5 | 630.3 / 810.6 / 871.2 | n/a | n/a |
| count_filter | ADBC | 8 | 3097.1 / 3803.3 / 4061.9 | 2694.7 / 3287.7 / 3486.2 | n/a (80 errors: t4 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| count_filter | ADBC | 32 | 10604.8 / 22748.2 / 28868.6 | 9125.1 / 23830.7 / 27309.9 | n/a (480 errors: t4 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| limit10_ob | JDBC | 1 | 156.8 / 439.1 / 3899.5 | 145.8 / 388.8 / 525.5 | 10300.5 / 11166.9 / 13251.2 | n/a |
| limit10_ob | JDBC | 8 | 1018.3 / 1693.0 / 2579.0 | 970.3 / 1610.4 / 2060.9 | n/a (132 errors: t1 r2: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRuntim) | n/a |
| limit10_ob | JDBC | 32 | 3753.6 / 5683.1 / 8616.3 | 3774.0 / 17478.2 / 33883.8 | n/a (480 errors: t17 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l) | n/a |
| limit10_ob | ADBC | 1 | 157.6 / 472.8 / 709.6 | 136.2 / 298.1 / 322.0 | n/a | n/a |
| limit10_ob | ADBC | 8 | 1054.6 / 1683.0 / 1962.9 | 989.4 / 1605.0 / 5301.5 | n/a (80 errors: t4 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| limit10_ob | ADBC | 32 | 4054.6 / 12041.9 / 131032.7 | 3845.6 / 6325.0 / 16187.9 | n/a (480 errors: t4 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| meta_tables | JDBC | 1 | 7.7 / 13.8 / 14.9 | 7.1 / 12.0 / 14.0 | 10.5 / 91.1 / 106.1 | n/a |
| meta_tables | JDBC | 8 | 6.1 / 14.8 / 22.8 | 6.1 / 15.1 / 21.0 | n/a (43 errors: t2 r4: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRuntim) | n/a |
| meta_tables | JDBC | 32 | 8.3 / 29.8 / 54.6 | 10.7 / 30.0 / 44.9 | n/a (480 errors: t24 r-1: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRunt) | n/a |
| meta_tables | ADBC | 1 | 7.4 / 13.2 / 16.5 | 6.7 / 10.7 / 17.5 | n/a | n/a |
| meta_tables | ADBC | 8 | 9.1 / 20.0 / 26.9 | 8.8 / 22.2 / 32.7 | n/a (80 errors: t5 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| meta_tables | ADBC | 32 | 23.4 / 52.9 / 77.1 | 27.5 / 67.1 / 109.7 | n/a (480 errors: t4 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| meta_schemas | JDBC | 1 | 5.8 / 9.5 / 11.1 | 5.1 / 9.4 / 13.5 | 7.0 / 11.3 / 12.4 | n/a |
| meta_schemas | JDBC | 8 | 5.4 / 16.2 / 22.9 | 4.9 / 11.7 / 21.4 | n/a (41 errors: t2 r4: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRuntim) | n/a |
| meta_schemas | JDBC | 32 | 8.1 / 36.0 / 62.3 | 7.8 / 32.5 / 65.2 | n/a (480 errors: t1 r-1: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRunti) | n/a |
| meta_schemas | ADBC | 1 | 4.4 / 7.8 / 9.4 | 4.1 / 9.1 / 10.2 | n/a | n/a |
| meta_schemas | ADBC | 8 | 6.0 / 14.8 / 20.8 | 6.1 / 17.4 / 24.0 | n/a (80 errors: t5 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| meta_schemas | ADBC | 32 | 14.0 / 43.3 / 89.7 | 15.8 / 50.2 / 89.1 | n/a (480 errors: t4 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |

Answers per class are compared across servers in the run summary (`summary.md`, correctness gate).

### Scans (`SELECT * FROM tpch.lineitem`, SF10, MB/s of Arrow buffers) and server peak RSS

| metric | ours-new | ours-27f5 | up-native | up-main | ours-new vs best upstream |
|---|---|---|---|---|---|
| raw Flight, 1 stream | 347 | 411 | 346 | n/a | 0.78x |
| raw Flight, 4 streams | 451 | 495 | 650 | n/a | 0.65x |
| raw Flight, 8 streams | 416 | 452 | n/a | n/a | n/a |
| full export over ADBC | 354 | 484 | 378 | n/a | 0.84x |
| server peak RSS (MB) | 3111 | 3152 | 3292 | n/a | - |

### Server container (docker stats every ~5 s, all workloads of this setting)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| CPU % p50 (200 = both cores) | 34 | 29 | 1 | n/a |
| CPU % max | 216 | 206 | 205 | n/a |
| memory peak (MiB, limit 6144) | 3166 | 2962 | 6117 | n/a |
| OOM-killed rounds | 0 / 12 | 0 / 6 | 3 / 6 | n/a |

