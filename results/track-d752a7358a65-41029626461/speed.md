# Server comparison - Report 1: SPEED (compare run 41029626461)

## Experiment setup

| item | value |
|---|---|
| runner | GitHub-hosted `ubuntu-latest`: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor; Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor; Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor; RAM 15983 MB; kernel 7.0.0-1017-azure; JDK Temurin 21 |
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
| JVM `d752a7358a65` `def` | `--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED -Darrowflight.plugins.dir=/app/plugins -Darrowflight.duckdb.extensionDir=/ext/duckdb-home/extensions -DduckDbAllowUnsignedExtensions=true -Ds3Endpoint=http://127.0.0.1:9000 -Ds3UrlStyle=path -Ds3Region=us-east-1 -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf10 -DresourceProfile=speed -cp --port --localhost --hosts` |
| JVM `up-native` `def` | `--add-modules --add-exports --add-opens --add-opens --add-opens=java.base/java.nio=ALL-UNNAMED --add-opens --add-opens -Dio.netty.tryReflectionSetAccessible=true -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf10 -cp --port --localhost --hosts` |

Times are warm medians in ms (median over rounds of the per-round warm median). **n/a** = not run, failed or wrong
answer (reason in the notes). Last column: same-runner ratio best-upstream / ours-new (> 1 = ours-new faster).

## local, setting `def`

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

### TPC-H SF1, ADBC

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

### TPC-H SF10, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | n/a | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | n/a | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | n/a | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | n/a | n/a | n/a | n/a | n/a |
| q05 | 6-way join | n/a | n/a | n/a | n/a | n/a |
| q06 | selective scan | n/a | n/a | 758 | n/a | n/a |
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
| **Score** | sum of the 1 queries every shown server answered | n/a | n/a | 758 | n/a | geomean n/a (0 q) |

- up-native: failed: repetition 1 of 2 Error while executing SQL "SELECT c_custkey, c_name, sum(l_extendedprice * (1 - l_discount)) AS revenue, c_acctbal, n_name, c_address, c_phone: q10; failed: repetition 1 of 2 Error while executing SQL "SELECT c_name, c_custkey, o_orderkey, o_orderdate, o_totalprice, sum(l_quantity) FROM tpch.customer, tpch.orders, t: q18; failed: repetition 1 of 2 Error while executing SQL "SELECT cntrycode, count(*) AS numcust, sum(c_acctbal) AS totacctbal FROM ( SELECT substring(c_phone FROM 1 FOR 2) A: q22; failed: repetition 1 of 2 Error while executing SQL "SELECT l_orderkey, sum(l_extendedprice * (1 - l_discount)) AS revenue, o_orderdate, o_shippriority FROM tpch.custom: q03; failed: repetition 1 of 2 Error while executing SQL "SELECT l_returnflag, l_linestatus, sum(l_quantity) AS sum_qty, sum(l_extendedprice) AS sum_base_price, sum(l_extend: q01; failed: repetition 1 of 2 Error while executing SQL "SELECT l_shipmode, sum( CASE WHEN o_orderpriority = '1-URGENT' OR o_orderpriority = '2-HIGH' THEN 1 ELSE 0 END) AS : q12; failed: repetition 1 of 2 Error while executing SQL "SELECT n_name, sum(l_extendedprice * (1 - l_discount)) AS revenue FROM tpch.customer, tpch.orders, tpch.lineitem, t: q05; failed: repetition 1 of 2 Error while executing SQL "SELECT nation, o_year, sum(amount) AS sum_profit FROM ( SELECT n_name AS nation, extract(year FROM o_orderdate) AS : q09; failed: repetition 1 of 2 Error while executing SQL "SELECT o_orderpriority, count(*) AS order_count FROM tpch.orders WHERE o_orderdate >= CAST('1993-07-01' AS date) AN: q04; failed: repetition 1 of 2 Error while executing SQL "SELECT o_year, sum( CASE WHEN nation = 'BRAZIL' THEN volume ELSE 0 END) / sum(volume) AS mkt_share FROM ( SELECT ex: q08; failed: repetition 1 of 2 Error while executing SQL "SELECT p_brand, p_type, p_size, count(DISTINCT ps_suppkey) AS supplier_cnt FROM tpch.partsupp, tpch.part WHERE p_pa: q16; failed: repetition 1 of 2 Error while executing SQL "SELECT ps_partkey, sum(ps_supplycost * ps_availqty) AS value FROM tpch.partsupp, tpch.supplier, tpch.nation WHERE p: q11; failed: repetition 1 of 2 Error while executing SQL "SELECT s_acctbal, s_name, n_name, p_partkey, p_mfgr, s_address, s_phone, s_comment FROM tpch.part, tpch.supplier, t: q02; failed: repetition 1 of 2 Error while executing SQL "SELECT s_name, count(*) AS numwait FROM tpch.supplier, tpch.lineitem l1, tpch.orders, tpch.nation WHERE s_suppkey =: q21; failed: repetition 1 of 2 Error while executing SQL "SELECT s_name, s_address FROM tpch.supplier, tpch.nation WHERE s_suppkey IN ( SELECT ps_suppkey FROM tpch.partsupp : q20; failed: repetition 1 of 2 Error while executing SQL "SELECT sum(l_extendedprice * (1 - l_discount)) AS revenue FROM tpch.lineitem, tpch.part WHERE (p_partkey = l_partke: q19; failed: repetition 1 of 2 Error while executing SQL "SELECT supp_nation, cust_nation, l_year, sum(volume) AS revenue FROM ( SELECT n1.n_name AS supp_nation, n2.n_name A: q07; failed: repetition 1 of 2 Error while executing SQL "WITH revenue AS ( SELECT l_suppkey AS supplier_no, sum(l_extendedprice * (1 - l_discount)) AS total_revenue FROM tp: q15; failed: the server's schema resolver rejects it (upstream: single-table parser, `Can only select from ONE table`; `AVG` unsupported on main): q13 q14 q17
- ours-new: not run: not in this setting's jobs
- ours-27f5: not run: not in this setting's jobs
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### TPC-H SF1, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | n/a | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | n/a | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | n/a | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | n/a | n/a | n/a | n/a | n/a |
| q05 | 6-way join | n/a | n/a | n/a | n/a | n/a |
| q06 | selective scan | n/a | n/a | 112 | n/a | n/a |
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
| **Score** | sum of the 1 queries every shown server answered | n/a | n/a | 112 | n/a | geomean n/a (0 q) |

- up-native: failed: repetition 1 of 3 Error while executing SQL "SELECT c_custkey, c_name, sum(l_extendedprice * (1 - l_discount)) AS revenue, c_acctbal, n_name, c_address, c_phone: q10; failed: repetition 1 of 3 Error while executing SQL "SELECT c_name, c_custkey, o_orderkey, o_orderdate, o_totalprice, sum(l_quantity) FROM tpch.customer, tpch.orders, t: q18; failed: repetition 1 of 3 Error while executing SQL "SELECT cntrycode, count(*) AS numcust, sum(c_acctbal) AS totacctbal FROM ( SELECT substring(c_phone FROM 1 FOR 2) A: q22; failed: repetition 1 of 3 Error while executing SQL "SELECT l_orderkey, sum(l_extendedprice * (1 - l_discount)) AS revenue, o_orderdate, o_shippriority FROM tpch.custom: q03; failed: repetition 1 of 3 Error while executing SQL "SELECT l_returnflag, l_linestatus, sum(l_quantity) AS sum_qty, sum(l_extendedprice) AS sum_base_price, sum(l_extend: q01; failed: repetition 1 of 3 Error while executing SQL "SELECT l_shipmode, sum( CASE WHEN o_orderpriority = '1-URGENT' OR o_orderpriority = '2-HIGH' THEN 1 ELSE 0 END) AS : q12; failed: repetition 1 of 3 Error while executing SQL "SELECT n_name, sum(l_extendedprice * (1 - l_discount)) AS revenue FROM tpch.customer, tpch.orders, tpch.lineitem, t: q05; failed: repetition 1 of 3 Error while executing SQL "SELECT nation, o_year, sum(amount) AS sum_profit FROM ( SELECT n_name AS nation, extract(year FROM o_orderdate) AS : q09; failed: repetition 1 of 3 Error while executing SQL "SELECT o_orderpriority, count(*) AS order_count FROM tpch.orders WHERE o_orderdate >= CAST('1993-07-01' AS date) AN: q04; failed: repetition 1 of 3 Error while executing SQL "SELECT o_year, sum( CASE WHEN nation = 'BRAZIL' THEN volume ELSE 0 END) / sum(volume) AS mkt_share FROM ( SELECT ex: q08; failed: repetition 1 of 3 Error while executing SQL "SELECT p_brand, p_type, p_size, count(DISTINCT ps_suppkey) AS supplier_cnt FROM tpch.partsupp, tpch.part WHERE p_pa: q16; failed: repetition 1 of 3 Error while executing SQL "SELECT ps_partkey, sum(ps_supplycost * ps_availqty) AS value FROM tpch.partsupp, tpch.supplier, tpch.nation WHERE p: q11; failed: repetition 1 of 3 Error while executing SQL "SELECT s_acctbal, s_name, n_name, p_partkey, p_mfgr, s_address, s_phone, s_comment FROM tpch.part, tpch.supplier, t: q02; failed: repetition 1 of 3 Error while executing SQL "SELECT s_name, count(*) AS numwait FROM tpch.supplier, tpch.lineitem l1, tpch.orders, tpch.nation WHERE s_suppkey =: q21; failed: repetition 1 of 3 Error while executing SQL "SELECT s_name, s_address FROM tpch.supplier, tpch.nation WHERE s_suppkey IN ( SELECT ps_suppkey FROM tpch.partsupp : q20; failed: repetition 1 of 3 Error while executing SQL "SELECT sum(l_extendedprice * (1 - l_discount)) AS revenue FROM tpch.lineitem, tpch.part WHERE (p_partkey = l_partke: q19; failed: repetition 1 of 3 Error while executing SQL "SELECT supp_nation, cust_nation, l_year, sum(volume) AS revenue FROM ( SELECT n1.n_name AS supp_nation, n2.n_name A: q07; failed: repetition 1 of 3 Error while executing SQL "WITH revenue AS ( SELECT l_suppkey AS supplier_no, sum(l_extendedprice * (1 - l_discount)) AS total_revenue FROM tp: q15; failed: the server's schema resolver rejects it (upstream: single-table parser, `Can only select from ONE table`; `AVG` unsupported on main): q13 q14 q17
- ours-new: not run: not in this setting's jobs
- ours-27f5: not run: not in this setting's jobs
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### Small queries (ms, p50 / p95 / p99 over all rounds)

| class | client | c | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|---|---|
| point_orders | JDBC | 1 | n/a | n/a | 24.6 / 36.3 / 41.5 | n/a |
| point_orders | JDBC | 8 | n/a | n/a | n/a | n/a |
| point_orders | JDBC | 32 | n/a | n/a | n/a (480 errors: t20 r-1: java.sql.SQLException: Error while executing SQL "SELECT o_orderkey, o) | n/a |
| point_orders | ADBC | 1 | n/a | n/a | n/a | n/a |
| point_orders | ADBC | 8 | n/a | n/a | n/a | n/a |
| point_orders | ADBC | 32 | n/a | n/a | n/a (480 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| point_lineitem | JDBC | 1 | n/a | n/a | 34.5 / 44.4 / 53.4 | n/a |
| point_lineitem | JDBC | 8 | n/a | n/a | n/a | n/a |
| point_lineitem | JDBC | 32 | n/a | n/a | n/a (480 errors: t20 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l) | n/a |
| point_lineitem | ADBC | 1 | n/a | n/a | n/a | n/a |
| point_lineitem | ADBC | 8 | n/a | n/a | n/a | n/a |
| point_lineitem | ADBC | 32 | n/a | n/a | n/a (480 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| count_filter | JDBC | 1 | n/a | n/a | 85.8 / 107.7 / 126.5 | n/a |
| count_filter | JDBC | 8 | n/a | n/a | n/a | n/a |
| count_filter | JDBC | 32 | n/a | n/a | n/a (480 errors: t15 r-1: java.sql.SQLException: Error while executing SQL "SELECT count(*) FROM) | n/a |
| count_filter | ADBC | 1 | n/a | n/a | n/a | n/a |
| count_filter | ADBC | 8 | n/a | n/a | n/a | n/a |
| count_filter | ADBC | 32 | n/a | n/a | n/a (480 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| limit10_ob | JDBC | 1 | n/a | n/a | 8034.8 / 8396.6 / 8503.2 | n/a |
| limit10_ob | JDBC | 8 | n/a | n/a | n/a | n/a |
| limit10_ob | JDBC | 32 | n/a | n/a | n/a (480 errors: t15 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l) | n/a |
| limit10_ob | ADBC | 1 | n/a | n/a | n/a | n/a |
| limit10_ob | ADBC | 8 | n/a | n/a | n/a | n/a |
| limit10_ob | ADBC | 32 | n/a | n/a | n/a (480 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| meta_tables | JDBC | 1 | n/a | n/a | 82.0 / 192.5 / 209.2 | n/a |
| meta_tables | JDBC | 8 | n/a | n/a | n/a | n/a |
| meta_tables | JDBC | 32 | n/a | n/a | n/a (480 errors: t20 r-1: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRunt) | n/a |
| meta_tables | ADBC | 1 | n/a | n/a | n/a | n/a |
| meta_tables | ADBC | 8 | n/a | n/a | n/a | n/a |
| meta_tables | ADBC | 32 | n/a | n/a | n/a (480 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| meta_schemas | JDBC | 1 | n/a | n/a | 7.8 / 12.1 / 13.3 | n/a |
| meta_schemas | JDBC | 8 | n/a | n/a | n/a | n/a |
| meta_schemas | JDBC | 32 | n/a | n/a | n/a (480 errors: t20 r-1: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRunt) | n/a |
| meta_schemas | ADBC | 1 | n/a | n/a | n/a | n/a |
| meta_schemas | ADBC | 8 | n/a | n/a | n/a | n/a |
| meta_schemas | ADBC | 32 | n/a | n/a | n/a (480 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |

Answers per class are compared across servers in the run summary (`summary.md`, correctness gate).

### Scans (`SELECT * FROM tpch.lineitem`, SF10, MB/s of Arrow buffers) and server peak RSS

| metric | ours-new | ours-27f5 | up-native | up-main | ours-new vs best upstream |
|---|---|---|---|---|---|
| raw Flight, 1 stream | n/a | n/a | 646 | n/a | n/a |
| raw Flight, 4 streams | n/a | n/a | 866 | n/a | n/a |
| raw Flight, 8 streams | n/a | n/a | 880 | n/a | n/a |
| full export over ADBC | n/a | n/a | 826 | n/a | n/a |
| server peak RSS (MB) | n/a | n/a | 3677 | n/a | - |

### Server container (docker stats every ~5 s, all workloads of this setting)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| CPU % p50 (200 = both cores) | n/a | n/a | 155 | n/a |
| CPU % max | n/a | n/a | 209 | n/a |
| memory peak (MiB, limit 6144) | n/a | n/a | 6130 | n/a |
| OOM-killed rounds | n/a | n/a | 3 / 15 | n/a |

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

### TPC-H SF1, ADBC

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

### TPC-H SF10, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | n/a | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | n/a | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | n/a | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | n/a | n/a | n/a | n/a | n/a |
| q05 | 6-way join | n/a | n/a | n/a | n/a | n/a |
| q06 | selective scan | n/a | n/a | 491 | n/a | n/a |
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
| **Score** | sum of the 1 queries every shown server answered | n/a | n/a | 491 | n/a | geomean n/a (0 q) |

- up-native: failed: repetition 1 of 2 Error while executing SQL "SELECT c_custkey, c_name, sum(l_extendedprice * (1 - l_discount)) AS revenue, c_acctbal, n_name, c_address, c_phone: q10; failed: repetition 1 of 2 Error while executing SQL "SELECT c_name, c_custkey, o_orderkey, o_orderdate, o_totalprice, sum(l_quantity) FROM tpch.customer, tpch.orders, t: q18; failed: repetition 1 of 2 Error while executing SQL "SELECT cntrycode, count(*) AS numcust, sum(c_acctbal) AS totacctbal FROM ( SELECT substring(c_phone FROM 1 FOR 2) A: q22; failed: repetition 1 of 2 Error while executing SQL "SELECT l_orderkey, sum(l_extendedprice * (1 - l_discount)) AS revenue, o_orderdate, o_shippriority FROM tpch.custom: q03; failed: repetition 1 of 2 Error while executing SQL "SELECT l_returnflag, l_linestatus, sum(l_quantity) AS sum_qty, sum(l_extendedprice) AS sum_base_price, sum(l_extend: q01; failed: repetition 1 of 2 Error while executing SQL "SELECT l_shipmode, sum( CASE WHEN o_orderpriority = '1-URGENT' OR o_orderpriority = '2-HIGH' THEN 1 ELSE 0 END) AS : q12; failed: repetition 1 of 2 Error while executing SQL "SELECT n_name, sum(l_extendedprice * (1 - l_discount)) AS revenue FROM tpch.customer, tpch.orders, tpch.lineitem, t: q05; failed: repetition 1 of 2 Error while executing SQL "SELECT nation, o_year, sum(amount) AS sum_profit FROM ( SELECT n_name AS nation, extract(year FROM o_orderdate) AS : q09; failed: repetition 1 of 2 Error while executing SQL "SELECT o_orderpriority, count(*) AS order_count FROM tpch.orders WHERE o_orderdate >= CAST('1993-07-01' AS date) AN: q04; failed: repetition 1 of 2 Error while executing SQL "SELECT o_year, sum( CASE WHEN nation = 'BRAZIL' THEN volume ELSE 0 END) / sum(volume) AS mkt_share FROM ( SELECT ex: q08; failed: repetition 1 of 2 Error while executing SQL "SELECT p_brand, p_type, p_size, count(DISTINCT ps_suppkey) AS supplier_cnt FROM tpch.partsupp, tpch.part WHERE p_pa: q16; failed: repetition 1 of 2 Error while executing SQL "SELECT ps_partkey, sum(ps_supplycost * ps_availqty) AS value FROM tpch.partsupp, tpch.supplier, tpch.nation WHERE p: q11; failed: repetition 1 of 2 Error while executing SQL "SELECT s_acctbal, s_name, n_name, p_partkey, p_mfgr, s_address, s_phone, s_comment FROM tpch.part, tpch.supplier, t: q02; failed: repetition 1 of 2 Error while executing SQL "SELECT s_name, count(*) AS numwait FROM tpch.supplier, tpch.lineitem l1, tpch.orders, tpch.nation WHERE s_suppkey =: q21; failed: repetition 1 of 2 Error while executing SQL "SELECT s_name, s_address FROM tpch.supplier, tpch.nation WHERE s_suppkey IN ( SELECT ps_suppkey FROM tpch.partsupp : q20; failed: repetition 1 of 2 Error while executing SQL "SELECT sum(l_extendedprice * (1 - l_discount)) AS revenue FROM tpch.lineitem, tpch.part WHERE (p_partkey = l_partke: q19; failed: repetition 1 of 2 Error while executing SQL "SELECT supp_nation, cust_nation, l_year, sum(volume) AS revenue FROM ( SELECT n1.n_name AS supp_nation, n2.n_name A: q07; failed: repetition 1 of 2 Error while executing SQL "WITH revenue AS ( SELECT l_suppkey AS supplier_no, sum(l_extendedprice * (1 - l_discount)) AS total_revenue FROM tp: q15; failed: the server's schema resolver rejects it (upstream: single-table parser, `Can only select from ONE table`; `AVG` unsupported on main): q13 q14 q17
- ours-new: not run: not in this setting's jobs
- ours-27f5: not run: not in this setting's jobs
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### TPC-H SF1, JDBC

| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |
|---|---|---|---|---|---|---|
| q01 | scan + aggregation | n/a | n/a | n/a | n/a | n/a |
| q02 | correlated subquery, joins | n/a | n/a | n/a | n/a | n/a |
| q03 | 3-way join, top-N | n/a | n/a | n/a | n/a | n/a |
| q04 | EXISTS semi-join | n/a | n/a | n/a | n/a | n/a |
| q05 | 6-way join | n/a | n/a | n/a | n/a | n/a |
| q06 | selective scan | n/a | n/a | 130 | n/a | n/a |
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
| **Score** | sum of the 1 queries every shown server answered | n/a | n/a | 130 | n/a | geomean n/a (0 q) |

- up-native: failed: repetition 1 of 3 Error while executing SQL "SELECT c_custkey, c_name, sum(l_extendedprice * (1 - l_discount)) AS revenue, c_acctbal, n_name, c_address, c_phone: q10; failed: repetition 1 of 3 Error while executing SQL "SELECT c_name, c_custkey, o_orderkey, o_orderdate, o_totalprice, sum(l_quantity) FROM tpch.customer, tpch.orders, t: q18; failed: repetition 1 of 3 Error while executing SQL "SELECT cntrycode, count(*) AS numcust, sum(c_acctbal) AS totacctbal FROM ( SELECT substring(c_phone FROM 1 FOR 2) A: q22; failed: repetition 1 of 3 Error while executing SQL "SELECT l_orderkey, sum(l_extendedprice * (1 - l_discount)) AS revenue, o_orderdate, o_shippriority FROM tpch.custom: q03; failed: repetition 1 of 3 Error while executing SQL "SELECT l_returnflag, l_linestatus, sum(l_quantity) AS sum_qty, sum(l_extendedprice) AS sum_base_price, sum(l_extend: q01; failed: repetition 1 of 3 Error while executing SQL "SELECT l_shipmode, sum( CASE WHEN o_orderpriority = '1-URGENT' OR o_orderpriority = '2-HIGH' THEN 1 ELSE 0 END) AS : q12; failed: repetition 1 of 3 Error while executing SQL "SELECT n_name, sum(l_extendedprice * (1 - l_discount)) AS revenue FROM tpch.customer, tpch.orders, tpch.lineitem, t: q05; failed: repetition 1 of 3 Error while executing SQL "SELECT nation, o_year, sum(amount) AS sum_profit FROM ( SELECT n_name AS nation, extract(year FROM o_orderdate) AS : q09; failed: repetition 1 of 3 Error while executing SQL "SELECT o_orderpriority, count(*) AS order_count FROM tpch.orders WHERE o_orderdate >= CAST('1993-07-01' AS date) AN: q04; failed: repetition 1 of 3 Error while executing SQL "SELECT o_year, sum( CASE WHEN nation = 'BRAZIL' THEN volume ELSE 0 END) / sum(volume) AS mkt_share FROM ( SELECT ex: q08; failed: repetition 1 of 3 Error while executing SQL "SELECT p_brand, p_type, p_size, count(DISTINCT ps_suppkey) AS supplier_cnt FROM tpch.partsupp, tpch.part WHERE p_pa: q16; failed: repetition 1 of 3 Error while executing SQL "SELECT ps_partkey, sum(ps_supplycost * ps_availqty) AS value FROM tpch.partsupp, tpch.supplier, tpch.nation WHERE p: q11; failed: repetition 1 of 3 Error while executing SQL "SELECT s_acctbal, s_name, n_name, p_partkey, p_mfgr, s_address, s_phone, s_comment FROM tpch.part, tpch.supplier, t: q02; failed: repetition 1 of 3 Error while executing SQL "SELECT s_name, count(*) AS numwait FROM tpch.supplier, tpch.lineitem l1, tpch.orders, tpch.nation WHERE s_suppkey =: q21; failed: repetition 1 of 3 Error while executing SQL "SELECT s_name, s_address FROM tpch.supplier, tpch.nation WHERE s_suppkey IN ( SELECT ps_suppkey FROM tpch.partsupp : q20; failed: repetition 1 of 3 Error while executing SQL "SELECT sum(l_extendedprice * (1 - l_discount)) AS revenue FROM tpch.lineitem, tpch.part WHERE (p_partkey = l_partke: q19; failed: repetition 1 of 3 Error while executing SQL "SELECT supp_nation, cust_nation, l_year, sum(volume) AS revenue FROM ( SELECT n1.n_name AS supp_nation, n2.n_name A: q07; failed: repetition 1 of 3 Error while executing SQL "WITH revenue AS ( SELECT l_suppkey AS supplier_no, sum(l_extendedprice * (1 - l_discount)) AS total_revenue FROM tp: q15; failed: the server's schema resolver rejects it (upstream: single-table parser, `Can only select from ONE table`; `AVG` unsupported on main): q13 q14 q17
- ours-new: not run: not in this setting's jobs
- ours-27f5: not run: not in this setting's jobs
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### Small queries (ms, p50 / p95 / p99 over all rounds)

| class | client | c | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|---|---|
| point_orders | JDBC | 1 | n/a | n/a | 35.4 / 49.3 / 63.3 | n/a |
| point_orders | JDBC | 8 | n/a | n/a | n/a (141 errors: t3 r5: java.sql.SQLException: Error while executing SQL "SELECT o_orderkey, o_c) | n/a |
| point_orders | JDBC | 32 | n/a | n/a | n/a | n/a |
| point_orders | ADBC | 1 | n/a | n/a | n/a | n/a |
| point_orders | ADBC | 8 | n/a | n/a | n/a (240 errors: t5 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| point_orders | ADBC | 32 | n/a | n/a | n/a (480 errors: t1 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| point_lineitem | JDBC | 1 | n/a | n/a | 35.1 / 54.9 / 845.0 | n/a |
| point_lineitem | JDBC | 8 | n/a | n/a | n/a (138 errors: t3 r6: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l_l) | n/a |
| point_lineitem | JDBC | 32 | n/a | n/a | n/a | n/a |
| point_lineitem | ADBC | 1 | n/a | n/a | n/a | n/a |
| point_lineitem | ADBC | 8 | n/a | n/a | n/a (240 errors: t5 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| point_lineitem | ADBC | 32 | n/a | n/a | n/a (480 errors: t1 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| count_filter | JDBC | 1 | n/a | n/a | 51.1 / 121.6 / 1162.8 | n/a |
| count_filter | JDBC | 8 | n/a | n/a | n/a (153 errors: t4 r4: java.sql.SQLException: Error while executing SQL "SELECT count(*) FROM t) | n/a |
| count_filter | JDBC | 32 | n/a | n/a | n/a | n/a |
| count_filter | ADBC | 1 | n/a | n/a | n/a | n/a |
| count_filter | ADBC | 8 | n/a | n/a | n/a (240 errors: t5 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| count_filter | ADBC | 32 | n/a | n/a | n/a (480 errors: t1 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| limit10_ob | JDBC | 1 | n/a | n/a | 5644.4 / 5928.0 / 7136.7 | n/a |
| limit10_ob | JDBC | 8 | n/a | n/a | n/a (158 errors: t0 r2: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRuntim) | n/a |
| limit10_ob | JDBC | 32 | n/a | n/a | n/a | n/a |
| limit10_ob | ADBC | 1 | n/a | n/a | n/a | n/a |
| limit10_ob | ADBC | 8 | n/a | n/a | n/a (240 errors: t5 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| limit10_ob | ADBC | 32 | n/a | n/a | n/a (480 errors: t1 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| meta_tables | JDBC | 1 | n/a | n/a | 10.5 / 325.5 / 936.2 | n/a |
| meta_tables | JDBC | 8 | n/a | n/a | n/a (147 errors: t4 r4: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRuntim) | n/a |
| meta_tables | JDBC | 32 | n/a | n/a | n/a | n/a |
| meta_tables | ADBC | 1 | n/a | n/a | n/a | n/a |
| meta_tables | ADBC | 8 | n/a | n/a | n/a (240 errors: t5 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| meta_tables | ADBC | 32 | n/a | n/a | n/a (480 errors: t1 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| meta_schemas | JDBC | 1 | n/a | n/a | 7.2 / 14.2 / 17.0 | n/a |
| meta_schemas | JDBC | 8 | n/a | n/a | n/a (144 errors: t4 r4: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRuntim) | n/a |
| meta_schemas | JDBC | 32 | n/a | n/a | n/a | n/a |
| meta_schemas | ADBC | 1 | n/a | n/a | n/a | n/a |
| meta_schemas | ADBC | 8 | n/a | n/a | n/a (240 errors: t5 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| meta_schemas | ADBC | 32 | n/a | n/a | n/a (480 errors: t1 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |

Answers per class are compared across servers in the run summary (`summary.md`, correctness gate).

### Scans (`SELECT * FROM tpch.lineitem`, SF10, MB/s of Arrow buffers) and server peak RSS

| metric | ours-new | ours-27f5 | up-native | up-main | ours-new vs best upstream |
|---|---|---|---|---|---|
| raw Flight, 1 stream | n/a | n/a | 300 | n/a | n/a |
| raw Flight, 4 streams | n/a | n/a | 688 | n/a | n/a |
| raw Flight, 8 streams | n/a | n/a | n/a | n/a | n/a |
| full export over ADBC | n/a | n/a | 650 | n/a | n/a |
| server peak RSS (MB) | n/a | n/a | 5885 | n/a | - |

### Server container (docker stats every ~5 s, all workloads of this setting)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| CPU % p50 (200 = both cores) | n/a | n/a | 138 | n/a |
| CPU % max | n/a | n/a | 205 | n/a |
| memory peak (MiB, limit 6144) | n/a | n/a | 6063 | n/a |
| OOM-killed rounds | n/a | n/a | 3 / 15 | n/a |

