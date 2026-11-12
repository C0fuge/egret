# Server comparison - Report 1: SPEED (compare run 43175544843)

## Experiment setup

| item | value |
|---|---|
| runner | GitHub-hosted `ubuntu-latest`: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor; Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor; Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor; Linux ubuntu26 4 vCPU Intel(R) Xeon(R) 6973P-C; Linux ubuntu26 4 vCPU Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz; RAM 15983 MB; kernel 7.0.0-1019-azure; JDK Temurin 21 |
| containers | **no-container reference run**: server in `eclipse-temurin:21-jdk` with an 8 GB memory limit and no CPU limit, clients on the runner host; not the reported numbers |
| servers | ours-new = `7562a5bdb7b9` (DuckDB ?); ours-27f5 = `27f583adccd7` (DuckDB ?); up-native = `cfaa929746cbf9ba9f6134cbf0c5a9683b2c1e92` (DuckDB error: INTERNAL: [FlightSQL] Failed to prepare Flight SQL statement (Internal; Prepare). Vendor code: 13 duckdb_threads/memory_limit=n/a); up-main = `dbacd8d585bce2ef2a449c821fe3a53cc6060b57` (DuckDB ?) |
| data | TPC-H SF1 and SF10, DuckDB dbgen, Parquet, 8 files per big table, 122880-row row groups, one data dir `tpch.*` per SF |
| storage | local disk (`file://`, page-cached) and S3 (`rclone serve s3` on the same runner, path style) |
| pairs | every job: ours-new (side A) vs one other server (side B) on the same runner, rounds A B / B A / A B (3), 1 cold run (warm-up) + warm runs per query (SF1 2 warm, SF10 1 warm per round) |
| settings | `def` = each server's default (`duckDbThreads` ours 4, upstream 2); `t8` = `-DduckDbThreads=8` on both |
| batch size | server defaults (not overridden) |
| clients | TPC-H: Python ADBC Flight SQL 1.12.0 (pyarrow 26), Flight SQL JDBC 18.0.0; small queries: same; scans: raw Flight (Arrow Java), ADBC export |
| correctness | TPC-H over ADBC: rows + checksum per query equal to in-process DuckDB on the same files; over JDBC: the result rows compared numerically with the same reference (numbers within a relative 1.5e-9, i.e. two 10-digit roundings; the JDBC runner prints DECIMAL as an exact plain BigDecimal, the reference as %.10g) |
| upstream on S3 | up-native: `s3a://` data dir (Hadoop S3A from its `docker/hadoop-aws` recipe for listing, DuckDB httpfs for scans, `FLIGHT_S3_*` settings); up-main: **n/a**, main at the fork point has no S3 settings (no `FLIGHT_S3_*`, no S3A dependencies) |
| SF30 | not run: SF1+SF10 already fill most of the repo's 10 GB Actions cache, SF30 Parquet (~11 GB) does not fit; generating it per job costs ~20 min of each 4-vCPU runner |
| JVM `2c169a53db3b` `def` | `--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED -Darrowflight.plugins.dir=/app/plugins -Darrowflight.duckdb.extensionDir=/ext/duckdb-home/extensions -DduckDbAllowUnsignedExtensions=true -Ds3Endpoint=http://127.0.0.1:9000 -Ds3UrlStyle=path -Ds3Region=us-east-1 -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir=file:///data/default/sf10 -DresourceProfile=speed -cp --port --localhost --hosts` |
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
| q06 | selective scan | n/a | n/a | 626 | n/a | n/a |
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
| **Score** | sum of the 1 queries every shown server answered | n/a | n/a | 626 | n/a | geomean n/a (0 q) |

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
| q06 | selective scan | n/a | n/a | 91 | n/a | n/a |
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
| **Score** | sum of the 1 queries every shown server answered | n/a | n/a | 91 | n/a | geomean n/a (0 q) |

- up-native: failed: repetition 1 of 3 Error while executing SQL "SELECT c_custkey, c_name, sum(l_extendedprice * (1 - l_discount)) AS revenue, c_acctbal, n_name, c_address, c_phone: q10; failed: repetition 1 of 3 Error while executing SQL "SELECT c_name, c_custkey, o_orderkey, o_orderdate, o_totalprice, sum(l_quantity) FROM tpch.customer, tpch.orders, t: q18; failed: repetition 1 of 3 Error while executing SQL "SELECT cntrycode, count(*) AS numcust, sum(c_acctbal) AS totacctbal FROM ( SELECT substring(c_phone FROM 1 FOR 2) A: q22; failed: repetition 1 of 3 Error while executing SQL "SELECT l_orderkey, sum(l_extendedprice * (1 - l_discount)) AS revenue, o_orderdate, o_shippriority FROM tpch.custom: q03; failed: repetition 1 of 3 Error while executing SQL "SELECT l_returnflag, l_linestatus, sum(l_quantity) AS sum_qty, sum(l_extendedprice) AS sum_base_price, sum(l_extend: q01; failed: repetition 1 of 3 Error while executing SQL "SELECT l_shipmode, sum( CASE WHEN o_orderpriority = '1-URGENT' OR o_orderpriority = '2-HIGH' THEN 1 ELSE 0 END) AS : q12; failed: repetition 1 of 3 Error while executing SQL "SELECT n_name, sum(l_extendedprice * (1 - l_discount)) AS revenue FROM tpch.customer, tpch.orders, tpch.lineitem, t: q05; failed: repetition 1 of 3 Error while executing SQL "SELECT nation, o_year, sum(amount) AS sum_profit FROM ( SELECT n_name AS nation, extract(year FROM o_orderdate) AS : q09; failed: repetition 1 of 3 Error while executing SQL "SELECT o_orderpriority, count(*) AS order_count FROM tpch.orders WHERE o_orderdate >= CAST('1993-07-01' AS date) AN: q04; failed: repetition 1 of 3 Error while executing SQL "SELECT o_year, sum( CASE WHEN nation = 'BRAZIL' THEN volume ELSE 0 END) / sum(volume) AS mkt_share FROM ( SELECT ex: q08; failed: repetition 1 of 3 Error while executing SQL "SELECT p_brand, p_type, p_size, count(DISTINCT ps_suppkey) AS supplier_cnt FROM tpch.partsupp, tpch.part WHERE p_pa: q16; failed: repetition 1 of 3 Error while executing SQL "SELECT ps_partkey, sum(ps_supplycost * ps_availqty) AS value FROM tpch.partsupp, tpch.supplier, tpch.nation WHERE p: q11; failed: repetition 1 of 3 Error while executing SQL "SELECT s_acctbal, s_name, n_name, p_partkey, p_mfgr, s_address, s_phone, s_comment FROM tpch.part, tpch.supplier, t: q02; failed: repetition 1 of 3 Error while executing SQL "SELECT s_name, count(*) AS numwait FROM tpch.supplier, tpch.lineitem l1, tpch.orders, tpch.nation WHERE s_suppkey =: q21; failed: repetition 1 of 3 Error while executing SQL "SELECT s_name, s_address FROM tpch.supplier, tpch.nation WHERE s_suppkey IN ( SELECT ps_suppkey FROM tpch.partsupp : q20; failed: repetition 1 of 3 Error while executing SQL "SELECT sum(l_extendedprice * (1 - l_discount)) AS revenue FROM tpch.lineitem, tpch.part WHERE (p_partkey = l_partke: q19; failed: repetition 1 of 3 Error while executing SQL "SELECT supp_nation, cust_nation, l_year, sum(volume) AS revenue FROM ( SELECT n1.n_name AS supp_nation, n2.n_name A: q07; failed: repetition 1 of 3 Error while executing SQL "WITH revenue AS ( SELECT l_suppkey AS supplier_no, sum(l_extendedprice * (1 - l_discount)) AS total_revenue FROM tp: q15; failed: the server's schema resolver rejects it (upstream: single-table parser, `Can only select from ONE table`; `AVG` unsupported on main): q13 q14 q17
- ours-new: not run: not in this setting's jobs
- ours-27f5: not run: not in this setting's jobs
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### Small queries (ms, p50 / p95 / p99 over all rounds)

| class | client | c | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|---|---|
| point_orders | JDBC | 1 | n/a | n/a | 17.6 / 29.4 / 35.1 | n/a |
| point_orders | JDBC | 8 | n/a | n/a | n/a | n/a |
| point_orders | JDBC | 32 | n/a | n/a | n/a (480 errors: t11 r-1: java.sql.SQLException: Error while executing SQL "SELECT o_orderkey, o) | n/a |
| point_orders | ADBC | 1 | n/a | n/a | n/a | n/a |
| point_orders | ADBC | 8 | n/a | n/a | n/a | n/a |
| point_orders | ADBC | 32 | n/a | n/a | n/a (480 errors: t3 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| point_lineitem | JDBC | 1 | n/a | n/a | 22.7 / 30.8 / 40.1 | n/a |
| point_lineitem | JDBC | 8 | n/a | n/a | n/a | n/a |
| point_lineitem | JDBC | 32 | n/a | n/a | n/a (480 errors: t20 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l) | n/a |
| point_lineitem | ADBC | 1 | n/a | n/a | n/a | n/a |
| point_lineitem | ADBC | 8 | n/a | n/a | n/a | n/a |
| point_lineitem | ADBC | 32 | n/a | n/a | n/a (480 errors: t3 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| count_filter | JDBC | 1 | n/a | n/a | 38.7 / 81.5 / 92.8 | n/a |
| count_filter | JDBC | 8 | n/a | n/a | n/a | n/a |
| count_filter | JDBC | 32 | n/a | n/a | n/a (480 errors: t24 r-1: java.sql.SQLException: Error while executing SQL "SELECT count(*) FROM) | n/a |
| count_filter | ADBC | 1 | n/a | n/a | n/a | n/a |
| count_filter | ADBC | 8 | n/a | n/a | n/a | n/a |
| count_filter | ADBC | 32 | n/a | n/a | n/a (480 errors: t3 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| limit10_ob | JDBC | 1 | n/a | n/a | 5242.8 / 5754.0 / 5949.9 | n/a |
| limit10_ob | JDBC | 8 | n/a | n/a | n/a | n/a |
| limit10_ob | JDBC | 32 | n/a | n/a | n/a (480 errors: t24 r-1: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l) | n/a |
| limit10_ob | ADBC | 1 | n/a | n/a | n/a | n/a |
| limit10_ob | ADBC | 8 | n/a | n/a | n/a | n/a |
| limit10_ob | ADBC | 32 | n/a | n/a | n/a (480 errors: t3 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| meta_tables | JDBC | 1 | n/a | n/a | 8.7 / 156.2 / 169.2 | n/a |
| meta_tables | JDBC | 8 | n/a | n/a | n/a | n/a |
| meta_tables | JDBC | 32 | n/a | n/a | n/a (480 errors: t11 r-1: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRunt) | n/a |
| meta_tables | ADBC | 1 | n/a | n/a | n/a | n/a |
| meta_tables | ADBC | 8 | n/a | n/a | n/a | n/a |
| meta_tables | ADBC | 32 | n/a | n/a | n/a (480 errors: t3 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| meta_schemas | JDBC | 1 | n/a | n/a | 5.1 / 8.9 / 11.5 | n/a |
| meta_schemas | JDBC | 8 | n/a | n/a | n/a | n/a |
| meta_schemas | JDBC | 32 | n/a | n/a | n/a (480 errors: t11 r-1: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRunt) | n/a |
| meta_schemas | ADBC | 1 | n/a | n/a | n/a | n/a |
| meta_schemas | ADBC | 8 | n/a | n/a | n/a | n/a |
| meta_schemas | ADBC | 32 | n/a | n/a | n/a (480 errors: t3 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |

Answers per class are compared across servers in the run summary (`summary.md`, correctness gate).

### Scans (`SELECT * FROM tpch.lineitem`, SF10, MB/s of Arrow buffers) and server peak RSS

| metric | ours-new | ours-27f5 | up-native | up-main | ours-new vs best upstream |
|---|---|---|---|---|---|
| raw Flight, 1 stream | n/a | n/a | 528 | n/a | n/a |
| raw Flight, 4 streams | n/a | n/a | 680 | n/a | n/a |
| raw Flight, 8 streams | n/a | n/a | n/a | n/a | n/a |
| full export over ADBC | n/a | n/a | 653 | n/a | n/a |
| server peak RSS (MB) | n/a | n/a | 3731 | n/a | - |

### Server container (docker stats every ~5 s, all workloads of this setting)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| CPU % p50 (200 = both cores) | n/a | n/a | 160 | n/a |
| CPU % max | n/a | n/a | 206 | n/a |
| memory peak (MiB, limit 6144) | n/a | n/a | 4896 | n/a |
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
| q06 | selective scan | n/a | n/a | 893 | n/a | n/a |
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
| **Score** | sum of the 1 queries every shown server answered | n/a | n/a | 893 | n/a | geomean n/a (0 q) |

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
| q06 | selective scan | n/a | n/a | 123 | n/a | n/a |
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
| **Score** | sum of the 1 queries every shown server answered | n/a | n/a | 123 | n/a | geomean n/a (0 q) |

- up-native: failed: repetition 1 of 3 Error while executing SQL "SELECT c_custkey, c_name, sum(l_extendedprice * (1 - l_discount)) AS revenue, c_acctbal, n_name, c_address, c_phone: q10; failed: repetition 1 of 3 Error while executing SQL "SELECT c_name, c_custkey, o_orderkey, o_orderdate, o_totalprice, sum(l_quantity) FROM tpch.customer, tpch.orders, t: q18; failed: repetition 1 of 3 Error while executing SQL "SELECT cntrycode, count(*) AS numcust, sum(c_acctbal) AS totacctbal FROM ( SELECT substring(c_phone FROM 1 FOR 2) A: q22; failed: repetition 1 of 3 Error while executing SQL "SELECT l_orderkey, sum(l_extendedprice * (1 - l_discount)) AS revenue, o_orderdate, o_shippriority FROM tpch.custom: q03; failed: repetition 1 of 3 Error while executing SQL "SELECT l_returnflag, l_linestatus, sum(l_quantity) AS sum_qty, sum(l_extendedprice) AS sum_base_price, sum(l_extend: q01; failed: repetition 1 of 3 Error while executing SQL "SELECT l_shipmode, sum( CASE WHEN o_orderpriority = '1-URGENT' OR o_orderpriority = '2-HIGH' THEN 1 ELSE 0 END) AS : q12; failed: repetition 1 of 3 Error while executing SQL "SELECT n_name, sum(l_extendedprice * (1 - l_discount)) AS revenue FROM tpch.customer, tpch.orders, tpch.lineitem, t: q05; failed: repetition 1 of 3 Error while executing SQL "SELECT nation, o_year, sum(amount) AS sum_profit FROM ( SELECT n_name AS nation, extract(year FROM o_orderdate) AS : q09; failed: repetition 1 of 3 Error while executing SQL "SELECT o_orderpriority, count(*) AS order_count FROM tpch.orders WHERE o_orderdate >= CAST('1993-07-01' AS date) AN: q04; failed: repetition 1 of 3 Error while executing SQL "SELECT o_year, sum( CASE WHEN nation = 'BRAZIL' THEN volume ELSE 0 END) / sum(volume) AS mkt_share FROM ( SELECT ex: q08; failed: repetition 1 of 3 Error while executing SQL "SELECT p_brand, p_type, p_size, count(DISTINCT ps_suppkey) AS supplier_cnt FROM tpch.partsupp, tpch.part WHERE p_pa: q16; failed: repetition 1 of 3 Error while executing SQL "SELECT ps_partkey, sum(ps_supplycost * ps_availqty) AS value FROM tpch.partsupp, tpch.supplier, tpch.nation WHERE p: q11; failed: repetition 1 of 3 Error while executing SQL "SELECT s_acctbal, s_name, n_name, p_partkey, p_mfgr, s_address, s_phone, s_comment FROM tpch.part, tpch.supplier, t: q02; failed: repetition 1 of 3 Error while executing SQL "SELECT s_name, count(*) AS numwait FROM tpch.supplier, tpch.lineitem l1, tpch.orders, tpch.nation WHERE s_suppkey =: q21; failed: repetition 1 of 3 Error while executing SQL "SELECT s_name, s_address FROM tpch.supplier, tpch.nation WHERE s_suppkey IN ( SELECT ps_suppkey FROM tpch.partsupp : q20; failed: repetition 1 of 3 Error while executing SQL "SELECT sum(l_extendedprice * (1 - l_discount)) AS revenue FROM tpch.lineitem, tpch.part WHERE (p_partkey = l_partke: q19; failed: repetition 1 of 3 Error while executing SQL "SELECT supp_nation, cust_nation, l_year, sum(volume) AS revenue FROM ( SELECT n1.n_name AS supp_nation, n2.n_name A: q07; failed: repetition 1 of 3 Error while executing SQL "WITH revenue AS ( SELECT l_suppkey AS supplier_no, sum(l_extendedprice * (1 - l_discount)) AS total_revenue FROM tp: q15; failed: the server's schema resolver rejects it (upstream: single-table parser, `Can only select from ONE table`; `AVG` unsupported on main): q13 q14 q17
- ours-new: not run: not in this setting's jobs
- ours-27f5: not run: not in this setting's jobs
- up-main: not run: upstream has no JDBC prepared statements (the Flight SQL JDBC driver prepares every query)

### Small queries (ms, p50 / p95 / p99 over all rounds)

| class | client | c | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|---|---|
| point_orders | JDBC | 1 | n/a | n/a | 36.0 / 44.9 / 54.9 | n/a |
| point_orders | JDBC | 8 | n/a | n/a | n/a (137 errors: t0 r6: java.sql.SQLException: Error while executing SQL "SELECT o_orderkey, o_c) | n/a |
| point_orders | JDBC | 32 | n/a | n/a | n/a | n/a |
| point_orders | ADBC | 1 | n/a | n/a | n/a | n/a |
| point_orders | ADBC | 8 | n/a | n/a | n/a (240 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| point_orders | ADBC | 32 | n/a | n/a | n/a (480 errors: t1 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| point_lineitem | JDBC | 1 | n/a | n/a | 38.9 / 59.5 / 2583.4 | n/a |
| point_lineitem | JDBC | 8 | n/a | n/a | n/a (134 errors: t0 r6: java.sql.SQLException: Error while executing SQL "SELECT l_orderkey, l_l) | n/a |
| point_lineitem | JDBC | 32 | n/a | n/a | n/a | n/a |
| point_lineitem | ADBC | 1 | n/a | n/a | n/a | n/a |
| point_lineitem | ADBC | 8 | n/a | n/a | n/a (240 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| point_lineitem | ADBC | 32 | n/a | n/a | n/a (480 errors: t1 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| count_filter | JDBC | 1 | n/a | n/a | 46.6 / 172.7 / 1184.0 | n/a |
| count_filter | JDBC | 8 | n/a | n/a | n/a (149 errors: t6 r6: java.sql.SQLException: Error while executing SQL "SELECT count(*) FROM t) | n/a |
| count_filter | JDBC | 32 | n/a | n/a | n/a | n/a |
| count_filter | ADBC | 1 | n/a | n/a | n/a | n/a |
| count_filter | ADBC | 8 | n/a | n/a | n/a (240 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| count_filter | ADBC | 32 | n/a | n/a | n/a (480 errors: t1 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| limit10_ob | JDBC | 1 | n/a | n/a | 5756.4 / 6133.7 / 8260.8 | n/a |
| limit10_ob | JDBC | 8 | n/a | n/a | n/a (155 errors: t0 r0: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRuntim) | n/a |
| limit10_ob | JDBC | 32 | n/a | n/a | n/a | n/a |
| limit10_ob | ADBC | 1 | n/a | n/a | n/a | n/a |
| limit10_ob | ADBC | 8 | n/a | n/a | n/a (240 errors: t2 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| limit10_ob | ADBC | 32 | n/a | n/a | n/a (480 errors: t1 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| meta_tables | JDBC | 1 | n/a | n/a | 11.8 / 256.8 / 860.4 | n/a |
| meta_tables | JDBC | 8 | n/a | n/a | n/a (143 errors: t6 r6: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRuntim) | n/a |
| meta_tables | JDBC | 32 | n/a | n/a | n/a | n/a |
| meta_tables | ADBC | 1 | n/a | n/a | n/a | n/a |
| meta_tables | ADBC | 8 | n/a | n/a | n/a (240 errors: t7 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| meta_tables | ADBC | 32 | n/a | n/a | n/a (480 errors: t1 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| meta_schemas | JDBC | 1 | n/a | n/a | 7.5 / 11.8 / 13.9 | n/a |
| meta_schemas | JDBC | 8 | n/a | n/a | n/a (140 errors: t7 r6: org.apache.arrow.driver.jdbc.shaded.org.apache.arrow.flight.FlightRuntim) | n/a |
| meta_schemas | JDBC | 32 | n/a | n/a | n/a | n/a |
| meta_schemas | ADBC | 1 | n/a | n/a | n/a | n/a |
| meta_schemas | ADBC | 8 | n/a | n/a | n/a (240 errors: t7 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |
| meta_schemas | ADBC | 32 | n/a | n/a | n/a (480 errors: t1 r-1: OperationalError: IO: [FlightSQL] connection error: desc = "transport) | n/a |

Answers per class are compared across servers in the run summary (`summary.md`, correctness gate).

### Scans (`SELECT * FROM tpch.lineitem`, SF10, MB/s of Arrow buffers) and server peak RSS

| metric | ours-new | ours-27f5 | up-native | up-main | ours-new vs best upstream |
|---|---|---|---|---|---|
| raw Flight, 1 stream | n/a | n/a | 361 | n/a | n/a |
| raw Flight, 4 streams | n/a | n/a | 678 | n/a | n/a |
| raw Flight, 8 streams | n/a | n/a | 705 | n/a | n/a |
| full export over ADBC | n/a | n/a | 654 | n/a | n/a |
| server peak RSS (MB) | n/a | n/a | 5907 | n/a | - |

### Server container (docker stats every ~5 s, all workloads of this setting)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| CPU % p50 (200 = both cores) | n/a | n/a | 138 | n/a |
| CPU % max | n/a | n/a | 205 | n/a |
| memory peak (MiB, limit 6144) | n/a | n/a | 6143 | n/a |
| OOM-killed rounds | n/a | n/a | 2 / 15 | n/a |

