# Server comparison - Report 1: SPEED (compare run 40876778493)

## Experiment setup

| item | value |
|---|---|
| runner | GitHub-hosted `ubuntu-latest`: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor; Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor; Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor; RAM 15983 MB; kernel 7.0.0-1017-azure; JDK Temurin 21 |
| containers | **no-container reference run**: server in `eclipse-temurin:21-jdk` with an 8 GB memory limit and no CPU limit, clients on the runner host; not the reported numbers |
| servers | ours-new = `7562a5bdb7b9` (DuckDB v1.5.6); ours-27f5 = `27f583adccd7` (DuckDB ?); up-native = `9fb08d9dd24df3cb838a3172f9375560bb6dc70a` (DuckDB error: INTERNAL: [FlightSQL] Failed to prepare Flight SQL statement (Internal; Prepare). Vendor code: 13); up-main = `dbacd8d585bce2ef2a449c821fe3a53cc6060b57` (DuckDB ?) |
| data | TPC-H SF1 and SF10, DuckDB dbgen, Parquet, 8 files per big table, 122880-row row groups, one data dir `tpch.*` per SF |
| storage | local disk (`file://`, page-cached) and S3 (`rclone serve s3` on the same runner, path style) |
| pairs | every job: ours-new (side A) vs one other server (side B) on the same runner, rounds A B / B A / A B (3), 1 cold run (warm-up) + warm runs per query (SF1 2 warm, SF10 1 warm per round) |
| settings | `def` = each server's default (`duckDbThreads` ours 4, upstream 2); `t8` = `-DduckDbThreads=8` on both |
| batch size | server defaults (not overridden) |
| clients | TPC-H: Python ADBC Flight SQL 1.12.0 (pyarrow 26), Flight SQL JDBC 18.0.0; small queries: same; scans: raw Flight (Arrow Java), ADBC export |
| correctness | TPC-H over ADBC: rows + checksum per query equal to in-process DuckDB on the same files; over JDBC: the result rows compared numerically with the same reference (numbers within a relative 1.5e-9, i.e. two 10-digit roundings; the JDBC runner prints DECIMAL as an exact plain BigDecimal, the reference as %.10g) |
| upstream on S3 | up-native: `s3a://` data dir (Hadoop S3A from its `docker/hadoop-aws` recipe for listing, DuckDB httpfs for scans, `FLIGHT_S3_*` settings); up-main: **n/a**, main at the fork point has no S3 settings (no `FLIGHT_S3_*`, no S3A dependencies) |
| SF30 | not run: SF1+SF10 already fill most of the repo's 10 GB Actions cache, SF30 Parquet (~11 GB) does not fit; generating it per job costs ~20 min of each 4-vCPU runner |
| JVM `1e7b43a4e0c7` `def` | `--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED -Darrowflight.plugins.dir=/app/plugins -Darrowflight.duckdb.extensionDir=/ext/duckdb-home/extensions -DduckDbAllowUnsignedExtensions=true -Ds3Endpoint=http://127.0.0.1:9000 -Ds3UrlStyle=path -Ds3Region=us-east-1 -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf10 -cp --port --localhost --hosts` |
| JVM `ours-new` `def` | `--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED -Darrowflight.plugins.dir=/app/plugins -Darrowflight.duckdb.extensionDir=/ext/duckdb-home/extensions -DduckDbAllowUnsignedExtensions=true -Ds3Endpoint=http://127.0.0.1:9000 -Ds3UrlStyle=path -Ds3Region=us-east-1 -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf10 -cp --port --localhost --hosts` |
| JVM `up-native` `def` | `--add-modules --add-exports --add-opens --add-opens --add-opens=java.base/java.nio=ALL-UNNAMED --add-opens --add-opens -Dio.netty.tryReflectionSetAccessible=true -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf10 -cp --port --localhost --hosts` |

Times are warm medians in ms (median over rounds of the per-round warm median). **n/a** = not run, failed or wrong
answer (reason in the notes). Last column: same-runner ratio best-upstream / ours-new (> 1 = ours-new faster).

## local, setting `def`

### TPC-H SF10, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 2134 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 324 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1307 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 828 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 1490 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 619 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 1417 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 1813 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 3635 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1548 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 293 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 836 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 2398 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 1020 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 932 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 454 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 1428 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 2737 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 1378 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 1187 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 4978 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 493 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 0 queries every shown server answered | n/a | n/a | n/a | n/a | geomean n/a (0 q) |

- up-native: failed: advertised schema differs from the data (e.g. float64 vs decimal(38,4)): ADBC rejects the stream: q06; failed: subquery table not rewritten: DuckDB `schema "tpch" does not exist`: q04; failed: the server's schema resolver rejects it (upstream: single-table parser, `Can only select from ONE table`; `AVG` unsupported on main): q01 q02 q03 q05 q07 q08 q09 q10 q11 q12 q13 q14 q15 q16 q17 q18 q19 q20 q21 q22
- ours-27f5: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF1, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 272 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 49 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 131 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 93 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 135 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 78 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 147 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 171 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 260 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 185 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 37 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 95 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 239 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 115 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 78 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 62 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 138 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 285 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 154 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 117 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 397 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 59 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 0 queries every shown server answered | n/a | n/a | n/a | n/a | geomean n/a (0 q) |

- up-native: failed: advertised schema differs from the data (e.g. float64 vs decimal(38,4)): ADBC rejects the stream: q06; failed: subquery table not rewritten: DuckDB `schema "tpch" does not exist`: q04; failed: the server's schema resolver rejects it (upstream: single-table parser, `Can only select from ONE table`; `AVG` unsupported on main): q01 q02 q03 q05 q07 q08 q09 q10 q11 q12 q13 q14 q15 q16 q17 q18 q19 q20 q21 q22
- ours-27f5: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF10, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 2144 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 342 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1283 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 829 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 1465 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 626 | n/a | 618 | n/a | n/a |
| q07 | joins, group by | 1410 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 1771 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 3654 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1563 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 299 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 827 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 2380 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 1023 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 892 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 479 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 1440 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 2658 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 1371 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 1215 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 5322 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 502 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 1 queries every shown server answered | 626 | n/a | 618 | n/a | geomean n/a (0 q) |

- up-native: failed: repetition 1 of 2 Error while executing SQL "SELECT c_custkey, c_name, sum(l_extendedprice * (1 - l_discount)) AS revenue, c_acctbal, n_name, c_address, c_phone: q10; failed: repetition 1 of 2 Error while executing SQL "SELECT c_name, c_custkey, o_orderkey, o_orderdate, o_totalprice, sum(l_quantity) FROM tpch.customer, tpch.orders, t: q18; failed: repetition 1 of 2 Error while executing SQL "SELECT cntrycode, count(*) AS numcust, sum(c_acctbal) AS totacctbal FROM ( SELECT substring(c_phone FROM 1 FOR 2) A: q22; failed: repetition 1 of 2 Error while executing SQL "SELECT l_orderkey, sum(l_extendedprice * (1 - l_discount)) AS revenue, o_orderdate, o_shippriority FROM tpch.custom: q03; failed: repetition 1 of 2 Error while executing SQL "SELECT l_returnflag, l_linestatus, sum(l_quantity) AS sum_qty, sum(l_extendedprice) AS sum_base_price, sum(l_extend: q01; failed: repetition 1 of 2 Error while executing SQL "SELECT l_shipmode, sum( CASE WHEN o_orderpriority = '1-URGENT' OR o_orderpriority = '2-HIGH' THEN 1 ELSE 0 END) AS : q12; failed: repetition 1 of 2 Error while executing SQL "SELECT n_name, sum(l_extendedprice * (1 - l_discount)) AS revenue FROM tpch.customer, tpch.orders, tpch.lineitem, t: q05; failed: repetition 1 of 2 Error while executing SQL "SELECT nation, o_year, sum(amount) AS sum_profit FROM ( SELECT n_name AS nation, extract(year FROM o_orderdate) AS : q09; failed: repetition 1 of 2 Error while executing SQL "SELECT o_orderpriority, count(*) AS order_count FROM tpch.orders WHERE o_orderdate >= CAST('1993-07-01' AS date) AN: q04; failed: repetition 1 of 2 Error while executing SQL "SELECT o_year, sum( CASE WHEN nation = 'BRAZIL' THEN volume ELSE 0 END) / sum(volume) AS mkt_share FROM ( SELECT ex: q08; failed: repetition 1 of 2 Error while executing SQL "SELECT p_brand, p_type, p_size, count(DISTINCT ps_suppkey) AS supplier_cnt FROM tpch.partsupp, tpch.part WHERE p_pa: q16; failed: repetition 1 of 2 Error while executing SQL "SELECT ps_partkey, sum(ps_supplycost * ps_availqty) AS value FROM tpch.partsupp, tpch.supplier, tpch.nation WHERE p: q11; failed: repetition 1 of 2 Error while executing SQL "SELECT s_acctbal, s_name, n_name, p_partkey, p_mfgr, s_address, s_phone, s_comment FROM tpch.part, tpch.supplier, t: q02; failed: repetition 1 of 2 Error while executing SQL "SELECT s_name, count(*) AS numwait FROM tpch.supplier, tpch.lineitem l1, tpch.orders, tpch.nation WHERE s_suppkey =: q21; failed: repetition 1 of 2 Error while executing SQL "SELECT s_name, s_address FROM tpch.supplier, tpch.nation WHERE s_suppkey IN ( SELECT ps_suppkey FROM tpch.partsupp : q20; failed: repetition 1 of 2 Error while executing SQL "SELECT sum(l_extendedprice * (1 - l_discount)) AS revenue FROM tpch.lineitem, tpch.part WHERE (p_partkey = l_partke: q19; failed: repetition 1 of 2 Error while executing SQL "SELECT supp_nation, cust_nation, l_year, sum(volume) AS revenue FROM ( SELECT n1.n_name AS supp_nation, n2.n_name A: q07; failed: repetition 1 of 2 Error while executing SQL "WITH revenue AS ( SELECT l_suppkey AS supplier_no, sum(l_extendedprice * (1 - l_discount)) AS total_revenue FROM tp: q15; failed: the server's schema resolver rejects it (upstream: single-table parser, `Can only select from ONE table`; `AVG` unsupported on main): q13 q14 q17
- ours-27f5: not run: not in this setting's jobs
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### TPC-H SF1, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 279 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 61 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 131 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 107 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 137 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 82 | n/a | 86 | n/a | n/a |
| q07 | joins, group by | 154 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 176 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 257 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 181 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 45 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 104 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 238 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 112 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 80 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 74 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 136 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 294 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 148 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 119 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 382 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 63 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 1 queries every shown server answered | 82 | n/a | 86 | n/a | geomean n/a (0 q) |

- up-native: failed: repetition 1 of 3 Error while executing SQL "SELECT c_custkey, c_name, sum(l_extendedprice * (1 - l_discount)) AS revenue, c_acctbal, n_name, c_address, c_phone: q10; failed: repetition 1 of 3 Error while executing SQL "SELECT c_name, c_custkey, o_orderkey, o_orderdate, o_totalprice, sum(l_quantity) FROM tpch.customer, tpch.orders, t: q18; failed: repetition 1 of 3 Error while executing SQL "SELECT cntrycode, count(*) AS numcust, sum(c_acctbal) AS totacctbal FROM ( SELECT substring(c_phone FROM 1 FOR 2) A: q22; failed: repetition 1 of 3 Error while executing SQL "SELECT l_orderkey, sum(l_extendedprice * (1 - l_discount)) AS revenue, o_orderdate, o_shippriority FROM tpch.custom: q03; failed: repetition 1 of 3 Error while executing SQL "SELECT l_returnflag, l_linestatus, sum(l_quantity) AS sum_qty, sum(l_extendedprice) AS sum_base_price, sum(l_extend: q01; failed: repetition 1 of 3 Error while executing SQL "SELECT l_shipmode, sum( CASE WHEN o_orderpriority = '1-URGENT' OR o_orderpriority = '2-HIGH' THEN 1 ELSE 0 END) AS : q12; failed: repetition 1 of 3 Error while executing SQL "SELECT n_name, sum(l_extendedprice * (1 - l_discount)) AS revenue FROM tpch.customer, tpch.orders, tpch.lineitem, t: q05; failed: repetition 1 of 3 Error while executing SQL "SELECT nation, o_year, sum(amount) AS sum_profit FROM ( SELECT n_name AS nation, extract(year FROM o_orderdate) AS : q09; failed: repetition 1 of 3 Error while executing SQL "SELECT o_orderpriority, count(*) AS order_count FROM tpch.orders WHERE o_orderdate >= CAST('1993-07-01' AS date) AN: q04; failed: repetition 1 of 3 Error while executing SQL "SELECT o_year, sum( CASE WHEN nation = 'BRAZIL' THEN volume ELSE 0 END) / sum(volume) AS mkt_share FROM ( SELECT ex: q08; failed: repetition 1 of 3 Error while executing SQL "SELECT p_brand, p_type, p_size, count(DISTINCT ps_suppkey) AS supplier_cnt FROM tpch.partsupp, tpch.part WHERE p_pa: q16; failed: repetition 1 of 3 Error while executing SQL "SELECT ps_partkey, sum(ps_supplycost * ps_availqty) AS value FROM tpch.partsupp, tpch.supplier, tpch.nation WHERE p: q11; failed: repetition 1 of 3 Error while executing SQL "SELECT s_acctbal, s_name, n_name, p_partkey, p_mfgr, s_address, s_phone, s_comment FROM tpch.part, tpch.supplier, t: q02; failed: repetition 1 of 3 Error while executing SQL "SELECT s_name, count(*) AS numwait FROM tpch.supplier, tpch.lineitem l1, tpch.orders, tpch.nation WHERE s_suppkey =: q21; failed: repetition 1 of 3 Error while executing SQL "SELECT s_name, s_address FROM tpch.supplier, tpch.nation WHERE s_suppkey IN ( SELECT ps_suppkey FROM tpch.partsupp : q20; failed: repetition 1 of 3 Error while executing SQL "SELECT sum(l_extendedprice * (1 - l_discount)) AS revenue FROM tpch.lineitem, tpch.part WHERE (p_partkey = l_partke: q19; failed: repetition 1 of 3 Error while executing SQL "SELECT supp_nation, cust_nation, l_year, sum(volume) AS revenue FROM ( SELECT n1.n_name AS supp_nation, n2.n_name A: q07; failed: repetition 1 of 3 Error while executing SQL "WITH revenue AS ( SELECT l_suppkey AS supplier_no, sum(l_extendedprice * (1 - l_discount)) AS total_revenue FROM tp: q15; failed: the server's schema resolver rejects it (upstream: single-table parser, `Can only select from ONE table`; `AVG` unsupported on main): q13 q14 q17
- ours-27f5: not run: not in this setting's jobs
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### Small queries (ms, p50 / p95 / p99 over all rounds)

| class | client | c | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|---|---|
| point_orders | JDBC | 1 | 25.6 / 44.1 / 56.5 | n/a | 24.8 / 41.1 / 43.2 | n/a |
| point_orders | JDBC | 8 | 123.8 / 179.5 / 195.9 | n/a | n/a | n/a |
| point_orders | JDBC | 32 | 457.7 / 885.9 / 1229.6 | n/a | n/a (480 errors: t27 r-1: java.sql.SQLException: Error while executing SQL "SELECT o_orderkey, o) | n/a |
| point_orders | ADBC | 1 | 16.1 / 22.4 / 24.4 | n/a | n/a | n/a |
| point_orders | ADBC | 8 | 101.5 / 163.5 / 225.3 | n/a | n/a | n/a |
| point_orders | ADBC | 32 | 386.9 / 715.0 / 854.3 | n/a | n/a (480 errors: t0 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| point_lineitem | JDBC | 1 | 35.8 / 49.2 / 61.1 | n/a | 34.2 / 52.6 / 57.8 | n/a |
| point_lineitem | JDBC | 8 | 197.0 / 270.1 / 400.3 | n/a | n/a | n/a |
| point_lineitem | JDBC | 32 | 768.4 / 1261.8 / 1580.4 | n/a | n/a (480 errors: t20 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l) | n/a |
| point_lineitem | ADBC | 1 | 25.5 / 41.6 / 47.2 | n/a | n/a | n/a |
| point_lineitem | ADBC | 8 | 174.2 / 266.7 / 318.6 | n/a | n/a | n/a |
| point_lineitem | ADBC | 32 | 730.2 / 1165.7 / 1387.4 | n/a | n/a (480 errors: t0 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| count_filter | JDBC | 1 | 49.5 / 64.3 / 72.2 | n/a | 90.7 / 112.2 / 120.7 | n/a |
| count_filter | JDBC | 8 | 224.8 / 285.2 / 308.4 | n/a | n/a | n/a |
| count_filter | JDBC | 32 | 903.9 / 1469.7 / 2087.6 | n/a | n/a (480 errors: t24 r-1: java.sql.SQLException: Error while executing SQL "SELECT count(*) FROM) | n/a |
| count_filter | ADBC | 1 | 42.5 / 54.3 / 60.4 | n/a | n/a | n/a |
| count_filter | ADBC | 8 | 225.9 / 291.2 / 310.1 | n/a | n/a | n/a |
| count_filter | ADBC | 32 | 855.3 / 1373.1 / 1568.1 | n/a | n/a (480 errors: t0 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| limit10_ob | JDBC | 1 | 45.8 / 56.3 / 58.8 | n/a | 8136.5 / 8457.0 / 8506.9 | n/a |
| limit10_ob | JDBC | 8 | 260.9 / 332.9 / 399.7 | n/a | n/a | n/a |
| limit10_ob | JDBC | 32 | 1082.6 / 1726.0 / 2109.7 | n/a | n/a (480 errors: t25 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l) | n/a |
| limit10_ob | ADBC | 1 | 38.7 / 54.1 / 57.2 | n/a | n/a | n/a |
| limit10_ob | ADBC | 8 | 253.9 / 361.1 / 420.0 | n/a | n/a | n/a |
| limit10_ob | ADBC | 32 | 1064.3 / 1757.7 / 1986.6 | n/a | n/a (480 errors: t0 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| meta_tables | JDBC | 1 | 8.4 / 13.3 / 14.5 | n/a | 87.3 / 182.2 / 211.6 | n/a |
| meta_tables | JDBC | 8 | 16.1 / 356.2 / 652.7 | n/a | n/a | n/a |
| meta_tables | JDBC | 32 | 36.0 / 1491.8 / 2449.7 | n/a | n/a (480 errors: t9 r-1: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRunti) | n/a |
| meta_tables | ADBC | 1 | 8.0 / 11.1 / 14.3 | n/a | n/a | n/a |
| meta_tables | ADBC | 8 | 32.9 / 62.0 / 78.9 | n/a | n/a | n/a |
| meta_tables | ADBC | 32 | 113.4 / 1715.3 / 2554.8 | n/a | n/a (480 errors: t0 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| meta_schemas | JDBC | 1 | 6.9 / 10.8 / 14.0 | n/a | 7.5 / 12.6 / 14.7 | n/a |
| meta_schemas | JDBC | 8 | 14.5 / 26.5 / 44.5 | n/a | n/a | n/a |
| meta_schemas | JDBC | 32 | 26.1 / 71.2 / 193.1 | n/a | n/a (480 errors: t27 r-1: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRunt) | n/a |
| meta_schemas | ADBC | 1 | 5.1 / 7.3 / 9.6 | n/a | n/a | n/a |
| meta_schemas | ADBC | 8 | 21.6 / 40.9 / 49.1 | n/a | n/a | n/a |
| meta_schemas | ADBC | 32 | 62.0 / 118.7 / 149.6 | n/a | n/a (480 errors: t0 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |

Answers per class are compared across servers in the run summary (`summary.md`, correctness gate).

### Scans (`SELECT * FROM tpch.lineitem`, SF10, MB/s of Arrow buffers) and server peak RSS

| metric | ours-new | ours-27f5 | up-native | up-main | ours-new vs best upstream |
|---|---|---|---|---|---|
| raw Flight, 1 stream | 416 | n/a | 419 | n/a | n/a |
| raw Flight, 4 streams | 447 | n/a | 565 | n/a | n/a |
| raw Flight, 8 streams | 414 | n/a | 588 | n/a | n/a |
| full export over ADBC | 514 | n/a | 544 | n/a | n/a |
| server peak RSS (MB) | 1720 | n/a | 3638 | n/a | - |

### Server container (docker stats every ~5 s, all workloads of this setting)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| CPU % p50 (200 = both cores) | 200 | n/a | 146 | n/a |
| CPU % max | 205 | n/a | 208 | n/a |
| memory peak (MiB, limit 6144) | 1624 | n/a | 6125 | n/a |
| OOM-killed rounds | 0 / 9 | n/a | 3 / 9 | n/a |

## s3, setting `def`

### TPC-H SF10, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 8344 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 3753 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 14648 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 8809 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 18646 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 18995 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 28606 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 33005 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 34168 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 21220 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 4378 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 23199 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 6902 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 21041 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 20675 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 1891 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 28008 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 21754 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 22745 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 26393 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 50995 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 2889 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 0 queries every shown server answered | n/a | n/a | n/a | n/a | geomean n/a (0 q) |

- up-native: failed: advertised schema differs from the data (e.g. float64 vs decimal(38,4)): ADBC rejects the stream: q06; failed: subquery table not rewritten: DuckDB `schema "tpch" does not exist`: q04; failed: the server's schema resolver rejects it (upstream: single-table parser, `Can only select from ONE table`; `AVG` unsupported on main): q01 q02 q03 q05 q07 q08 q09 q10 q11 q12 q13 q14 q15 q16 q17 q18 q19 q20 q21 q22
- ours-27f5: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF1, ADBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 805 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 393 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1380 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 860 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 1351 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 1249 | n/a | n/a | n/a | n/a |
| q07 | joins, group by | 1591 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 1855 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 1955 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1289 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 334 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 1380 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 372 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 1208 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 1037 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 120 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 1699 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 1448 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 1342 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 1409 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 2601 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 195 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 0 queries every shown server answered | n/a | n/a | n/a | n/a | geomean n/a (0 q) |

- up-native: failed: advertised schema differs from the data (e.g. float64 vs decimal(38,4)): ADBC rejects the stream: q06; failed: subquery table not rewritten: DuckDB `schema "tpch" does not exist`: q04; failed: the server's schema resolver rejects it (upstream: single-table parser, `Can only select from ONE table`; `AVG` unsupported on main): q01 q02 q03 q05 q07 q08 q09 q10 q11 q12 q13 q14 q15 q16 q17 q18 q19 q20 q21 q22
- ours-27f5: not run: not in this setting's jobs
- up-main: not run: not in this setting's jobs

### TPC-H SF10, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 6696 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 2997 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 13069 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 7393 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 13939 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 11625 | n/a | 613 | n/a | n/a |
| q07 | joins, group by | 17053 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 21944 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 18571 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 11084 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 2313 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 12584 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 3616 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 16842 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 11725 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 1285 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 14883 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 15815 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 13699 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 15731 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 30499 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 1656 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 1 queries every shown server answered | 11625 | n/a | 613 | n/a | geomean n/a (0 q) |

- up-native: failed: repetition 1 of 2 Error while executing SQL "SELECT c_custkey, c_name, sum(l_extendedprice * (1 - l_discount)) AS revenue, c_acctbal, n_name, c_address, c_phone: q10; failed: repetition 1 of 2 Error while executing SQL "SELECT c_name, c_custkey, o_orderkey, o_orderdate, o_totalprice, sum(l_quantity) FROM tpch.customer, tpch.orders, t: q18; failed: repetition 1 of 2 Error while executing SQL "SELECT cntrycode, count(*) AS numcust, sum(c_acctbal) AS totacctbal FROM ( SELECT substring(c_phone FROM 1 FOR 2) A: q22; failed: repetition 1 of 2 Error while executing SQL "SELECT l_orderkey, sum(l_extendedprice * (1 - l_discount)) AS revenue, o_orderdate, o_shippriority FROM tpch.custom: q03; failed: repetition 1 of 2 Error while executing SQL "SELECT l_returnflag, l_linestatus, sum(l_quantity) AS sum_qty, sum(l_extendedprice) AS sum_base_price, sum(l_extend: q01; failed: repetition 1 of 2 Error while executing SQL "SELECT l_shipmode, sum( CASE WHEN o_orderpriority = '1-URGENT' OR o_orderpriority = '2-HIGH' THEN 1 ELSE 0 END) AS : q12; failed: repetition 1 of 2 Error while executing SQL "SELECT n_name, sum(l_extendedprice * (1 - l_discount)) AS revenue FROM tpch.customer, tpch.orders, tpch.lineitem, t: q05; failed: repetition 1 of 2 Error while executing SQL "SELECT nation, o_year, sum(amount) AS sum_profit FROM ( SELECT n_name AS nation, extract(year FROM o_orderdate) AS : q09; failed: repetition 1 of 2 Error while executing SQL "SELECT o_orderpriority, count(*) AS order_count FROM tpch.orders WHERE o_orderdate >= CAST('1993-07-01' AS date) AN: q04; failed: repetition 1 of 2 Error while executing SQL "SELECT o_year, sum( CASE WHEN nation = 'BRAZIL' THEN volume ELSE 0 END) / sum(volume) AS mkt_share FROM ( SELECT ex: q08; failed: repetition 1 of 2 Error while executing SQL "SELECT p_brand, p_type, p_size, count(DISTINCT ps_suppkey) AS supplier_cnt FROM tpch.partsupp, tpch.part WHERE p_pa: q16; failed: repetition 1 of 2 Error while executing SQL "SELECT ps_partkey, sum(ps_supplycost * ps_availqty) AS value FROM tpch.partsupp, tpch.supplier, tpch.nation WHERE p: q11; failed: repetition 1 of 2 Error while executing SQL "SELECT s_acctbal, s_name, n_name, p_partkey, p_mfgr, s_address, s_phone, s_comment FROM tpch.part, tpch.supplier, t: q02; failed: repetition 1 of 2 Error while executing SQL "SELECT s_name, count(*) AS numwait FROM tpch.supplier, tpch.lineitem l1, tpch.orders, tpch.nation WHERE s_suppkey =: q21; failed: repetition 1 of 2 Error while executing SQL "SELECT s_name, s_address FROM tpch.supplier, tpch.nation WHERE s_suppkey IN ( SELECT ps_suppkey FROM tpch.partsupp : q20; failed: repetition 1 of 2 Error while executing SQL "SELECT sum(l_extendedprice * (1 - l_discount)) AS revenue FROM tpch.lineitem, tpch.part WHERE (p_partkey = l_partke: q19; failed: repetition 1 of 2 Error while executing SQL "SELECT supp_nation, cust_nation, l_year, sum(volume) AS revenue FROM ( SELECT n1.n_name AS supp_nation, n2.n_name A: q07; failed: repetition 1 of 2 Error while executing SQL "WITH revenue AS ( SELECT l_suppkey AS supplier_no, sum(l_extendedprice * (1 - l_discount)) AS total_revenue FROM tp: q15; failed: the server's schema resolver rejects it (upstream: single-table parser, `Can only select from ONE table`; `AVG` unsupported on main): q13 q14 q17
- ours-27f5: not run: not in this setting's jobs
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### TPC-H SF1, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | 701 | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | 400 | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | 1398 | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | 896 | n/a | n/a | n/a | n/a |
| q05 | 6-way join | 1355 | n/a | n/a | n/a | n/a |
| q06 | selective scan | 1154 | n/a | 110 | n/a | n/a |
| q07 | joins, group by | 1557 | n/a | n/a | n/a | n/a |
| q08 | 8-way join, CASE | 1846 | n/a | n/a | n/a | n/a |
| q09 | joins, LIKE, heavy | 1938 | n/a | n/a | n/a | n/a |
| q10 | 4-way join, top-N | 1300 | n/a | n/a | n/a | n/a |
| q11 | HAVING subquery | 332 | n/a | n/a | n/a | n/a |
| q12 | join, CASE agg | 1429 | n/a | n/a | n/a | n/a |
| q13 | outer join, LIKE | 404 | n/a | n/a | n/a | n/a |
| q14 | join, CASE | 1242 | n/a | n/a | n/a | n/a |
| q15 | view / CTE, max | 1031 | n/a | n/a | n/a | n/a |
| q16 | NOT IN, distinct | 135 | n/a | n/a | n/a | n/a |
| q17 | correlated avg | 1667 | n/a | n/a | n/a | n/a |
| q18 | IN subquery, big group by | 1400 | n/a | n/a | n/a | n/a |
| q19 | OR predicates | 1361 | n/a | n/a | n/a | n/a |
| q20 | nested IN | 1361 | n/a | n/a | n/a | n/a |
| q21 | EXISTS / NOT EXISTS | 2648 | n/a | n/a | n/a | n/a |
| q22 | substring, NOT EXISTS | 197 | n/a | n/a | n/a | n/a |
| **Score** | sum of the 1 queries every shown server answered | 1154 | n/a | 110 | n/a | geomean n/a (0 q) |

- up-native: failed: repetition 1 of 3 Error while executing SQL "SELECT c_custkey, c_name, sum(l_extendedprice * (1 - l_discount)) AS revenue, c_acctbal, n_name, c_address, c_phone: q10; failed: repetition 1 of 3 Error while executing SQL "SELECT c_name, c_custkey, o_orderkey, o_orderdate, o_totalprice, sum(l_quantity) FROM tpch.customer, tpch.orders, t: q18; failed: repetition 1 of 3 Error while executing SQL "SELECT cntrycode, count(*) AS numcust, sum(c_acctbal) AS totacctbal FROM ( SELECT substring(c_phone FROM 1 FOR 2) A: q22; failed: repetition 1 of 3 Error while executing SQL "SELECT l_orderkey, sum(l_extendedprice * (1 - l_discount)) AS revenue, o_orderdate, o_shippriority FROM tpch.custom: q03; failed: repetition 1 of 3 Error while executing SQL "SELECT l_returnflag, l_linestatus, sum(l_quantity) AS sum_qty, sum(l_extendedprice) AS sum_base_price, sum(l_extend: q01; failed: repetition 1 of 3 Error while executing SQL "SELECT l_shipmode, sum( CASE WHEN o_orderpriority = '1-URGENT' OR o_orderpriority = '2-HIGH' THEN 1 ELSE 0 END) AS : q12; failed: repetition 1 of 3 Error while executing SQL "SELECT n_name, sum(l_extendedprice * (1 - l_discount)) AS revenue FROM tpch.customer, tpch.orders, tpch.lineitem, t: q05; failed: repetition 1 of 3 Error while executing SQL "SELECT nation, o_year, sum(amount) AS sum_profit FROM ( SELECT n_name AS nation, extract(year FROM o_orderdate) AS : q09; failed: repetition 1 of 3 Error while executing SQL "SELECT o_orderpriority, count(*) AS order_count FROM tpch.orders WHERE o_orderdate >= CAST('1993-07-01' AS date) AN: q04; failed: repetition 1 of 3 Error while executing SQL "SELECT o_year, sum( CASE WHEN nation = 'BRAZIL' THEN volume ELSE 0 END) / sum(volume) AS mkt_share FROM ( SELECT ex: q08; failed: repetition 1 of 3 Error while executing SQL "SELECT p_brand, p_type, p_size, count(DISTINCT ps_suppkey) AS supplier_cnt FROM tpch.partsupp, tpch.part WHERE p_pa: q16; failed: repetition 1 of 3 Error while executing SQL "SELECT ps_partkey, sum(ps_supplycost * ps_availqty) AS value FROM tpch.partsupp, tpch.supplier, tpch.nation WHERE p: q11; failed: repetition 1 of 3 Error while executing SQL "SELECT s_acctbal, s_name, n_name, p_partkey, p_mfgr, s_address, s_phone, s_comment FROM tpch.part, tpch.supplier, t: q02; failed: repetition 1 of 3 Error while executing SQL "SELECT s_name, count(*) AS numwait FROM tpch.supplier, tpch.lineitem l1, tpch.orders, tpch.nation WHERE s_suppkey =: q21; failed: repetition 1 of 3 Error while executing SQL "SELECT s_name, s_address FROM tpch.supplier, tpch.nation WHERE s_suppkey IN ( SELECT ps_suppkey FROM tpch.partsupp : q20; failed: repetition 1 of 3 Error while executing SQL "SELECT sum(l_extendedprice * (1 - l_discount)) AS revenue FROM tpch.lineitem, tpch.part WHERE (p_partkey = l_partke: q19; failed: repetition 1 of 3 Error while executing SQL "SELECT supp_nation, cust_nation, l_year, sum(volume) AS revenue FROM ( SELECT n1.n_name AS supp_nation, n2.n_name A: q07; failed: repetition 1 of 3 Error while executing SQL "WITH revenue AS ( SELECT l_suppkey AS supplier_no, sum(l_extendedprice * (1 - l_discount)) AS total_revenue FROM tp: q15; failed: the server's schema resolver rejects it (upstream: single-table parser, `Can only select from ONE table`; `AVG` unsupported on main): q13 q14 q17
- ours-27f5: not run: not in this setting's jobs
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### Small queries (ms, p50 / p95 / p99 over all rounds)

| class | client | c | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|---|---|
| point_orders | JDBC | 1 | 34.6 / 44.2 / 47.3 | n/a | 39.9 / 52.4 / 56.1 | n/a |
| point_orders | JDBC | 8 | 398.9 / 641.3 / 745.7 | n/a | n/a (199 errors: t2 r2: java.sql.SQLException: Error while executing SQL "SELECT o_orderkey, o_c) | n/a |
| point_orders | JDBC | 32 | 1464.3 / 2422.1 / 4189.0 | n/a | n/a | n/a |
| point_orders | ADBC | 1 | 23.2 / 34.5 / 37.0 | n/a | n/a | n/a |
| point_orders | ADBC | 8 | 437.8 / 641.3 / 785.4 | n/a | n/a (240 errors: t0 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| point_orders | ADBC | 32 | 1422.4 / 2520.2 / 9053.7 | n/a | n/a (480 errors: t0 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| point_lineitem | JDBC | 1 | 30.4 / 48.7 / 53.0 | n/a | 44.6 / 94.7 / 118.9 | n/a |
| point_lineitem | JDBC | 8 | 246.0 / 407.3 / 558.5 | n/a | n/a (196 errors: t2 r2: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l_l) | n/a |
| point_lineitem | JDBC | 32 | 822.7 / 6129.1 / 23600.1 | n/a | n/a | n/a |
| point_lineitem | ADBC | 1 | 19.8 / 35.3 / 37.3 | n/a | n/a | n/a |
| point_lineitem | ADBC | 8 | 253.9 / 466.2 / 7091.0 | n/a | n/a (240 errors: t3 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| point_lineitem | ADBC | 32 | 824.1 / 11814.8 / 20241.8 | n/a | n/a (480 errors: t0 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| count_filter | JDBC | 1 | 764.6 / 888.5 / 904.2 | n/a | 76.6 / 1100.4 / 1209.4 | n/a |
| count_filter | JDBC | 8 | 5479.9 / 6188.4 / 6353.3 | n/a | n/a (211 errors: t2 r1: java.sql.SQLException: Error while executing SQL "SELECT count(*) FROM t) | n/a |
| count_filter | JDBC | 32 | 16334.5 / 20731.2 / 24085.5 | n/a | n/a | n/a |
| count_filter | ADBC | 1 | 771.4 / 887.4 / 916.1 | n/a | n/a | n/a |
| count_filter | ADBC | 8 | 5382.0 / 6173.8 / 12163.6 | n/a | n/a (240 errors: t3 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| count_filter | ADBC | 32 | 16893.9 / 22883.5 / 28594.2 | n/a | n/a (480 errors: t0 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| limit10_ob | JDBC | 1 | 117.3 / 160.4 / 180.1 | n/a | 7928.0 / 8732.0 / 9094.7 | n/a |
| limit10_ob | JDBC | 8 | 789.3 / 1170.9 / 1270.0 | n/a | n/a (217 errors: t7 r-1: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRunti) | n/a |
| limit10_ob | JDBC | 32 | 2770.1 / 3833.8 / 19021.3 | n/a | n/a | n/a |
| limit10_ob | ADBC | 1 | 125.5 / 173.9 / 184.8 | n/a | n/a | n/a |
| limit10_ob | ADBC | 8 | 844.0 / 1170.0 / 2239.3 | n/a | n/a (240 errors: t3 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| limit10_ob | ADBC | 32 | 2767.4 / 4097.5 / 11316.7 | n/a | n/a (480 errors: t0 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| meta_tables | JDBC | 1 | 9.7 / 15.3 / 15.9 | n/a | 33.4 / 1036.9 / 5284.3 | n/a |
| meta_tables | JDBC | 8 | 6.3 / 14.3 / 26.7 | n/a | n/a (205 errors: t2 r1: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRuntim) | n/a |
| meta_tables | JDBC | 32 | 7.3 / 25.9 / 61.6 | n/a | n/a | n/a |
| meta_tables | ADBC | 1 | 8.6 / 12.0 / 18.8 | n/a | n/a | n/a |
| meta_tables | ADBC | 8 | 9.3 / 30.0 / 34.9 | n/a | n/a (240 errors: t0 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| meta_tables | ADBC | 32 | 22.0 / 57.6 / 100.3 | n/a | n/a (480 errors: t0 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| meta_schemas | JDBC | 1 | 7.9 / 13.1 / 16.0 | n/a | 8.0 / 13.2 / 14.5 | n/a |
| meta_schemas | JDBC | 8 | 5.3 / 16.0 / 24.7 | n/a | n/a (202 errors: t2 r1: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRuntim) | n/a |
| meta_schemas | JDBC | 32 | 6.1 / 27.7 / 60.6 | n/a | n/a | n/a |
| meta_schemas | ADBC | 1 | 6.3 / 11.2 / 13.1 | n/a | n/a | n/a |
| meta_schemas | ADBC | 8 | 6.3 / 18.3 / 23.4 | n/a | n/a (240 errors: t0 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| meta_schemas | ADBC | 32 | 13.9 / 41.3 / 70.7 | n/a | n/a (480 errors: t0 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |

Answers per class are compared across servers in the run summary (`summary.md`, correctness gate).

### Scans (`SELECT * FROM tpch.lineitem`, SF10, MB/s of Arrow buffers) and server peak RSS

| metric | ours-new | ours-27f5 | up-native | up-main | ours-new vs best upstream |
|---|---|---|---|---|---|
| raw Flight, 1 stream | 536 | n/a | 515 | n/a | n/a |
| raw Flight, 4 streams | 635 | n/a | 825 | n/a | n/a |
| raw Flight, 8 streams | 589 | n/a | 839 | n/a | n/a |
| full export over ADBC | 621 | n/a | 778 | n/a | n/a |
| server peak RSS (MB) | 1762 | n/a | 5806 | n/a | - |

### Server container (docker stats every ~5 s, all workloads of this setting)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| CPU % p50 (200 = both cores) | 30 | n/a | 147 | n/a |
| CPU % max | 206 | n/a | 205 | n/a |
| memory peak (MiB, limit 6144) | 2006 | n/a | 6094 | n/a |
| OOM-killed rounds | 0 / 15 | n/a | 3 / 15 | n/a |

