# egret: A/B screening of Arrow Flight SQL server settings in CI

Each job of the `screen` workflow runs on one GitHub-hosted runner (4 vCPU, 16 GB) and compares the server's default
configuration (side A) with one variant (side B: server flags, JVM flags or a data layout) on that same runner, in
alternating rounds (A B, B A, A B), so runner-to-runner noise cancels out. Results are **ratios variant / default**;
absolute numbers from shared 4-vCPU runners are not comparable with a real deployment.

- Server: the public release `server-1.0.0-<id>` of C0fuge/kestrel (jar + runtime libs + plugins), DuckDB v1.4.5
  httpfs extension from extensions.duckdb.org, server in an `eclipse-temurin:21-jre` container limited to 2 CPUs (cpus 0,1) and 6 GB (`-Xmx3g -XX:MaxDirectMemorySize=2g`), clients in their own container on cpus 2,3.
- Data: TPC-H SF1 and SF10 generated with DuckDB `dbgen` (cached), 8 files per big table, 122880-row row groups;
  layout variants rewrite `lineitem` and `orders` (row group size, file size, one file).
- Storage: local disk (`file://`) or S3 served by `rclone serve s3`.
- Workloads (`clients/`): small queries (metadata, point lookups on orders/lineitem, `LIMIT 10`, filtered count,
  a reused prepared statement) at 1/8/32 concurrent clients through the Flight SQL JDBC driver 18.0.0 and Python
  ADBC; TPC-H SF1 and SF10 (22 queries, JDBC, complete mode, warm medians); full `lineitem` scans over raw Flight
  at 1 and 4 concurrent scans (MB/s of Arrow buffers); 4 heavy queries at once (q01 q09 q18 q21).
- Correctness gate per job: TPC-H answers (md5 of query/status/rows/answer checksum) equal the reference on both
  sides, small-query answers equal, no errors; a variant that fails the gate is reported, not ranked.

Run: Actions → screen → wave (file in `ci/waves/`), rounds, workloads. The `aggregate` job writes
`results/<wave>-<run id>/summary.md` / `summary.csv` and this index.

## Server comparison (`compare` workflow)

Each job of the `compare` workflow runs two different servers on one runner in alternating rounds (A B, B A, A B):
kestrel pre-releases `server-1.0.0-<id>` with the DuckDB 1.5.6 extension set (release `ci-assets`), and the upstream
reference server built in the same run from the public upstream repository (read-only checkout; shaded jar plus its
`provided` Hadoop dependencies; DuckDB 1.5.6 bundled, official httpfs 1.5.6; JVM options of its docker entrypoint).
All servers get the same TPC-H-only data dir and the same schema-qualified queries (`queries/tpch-schema`); TPC-H over
ADBC (`clients/tpch_adbc.py`) is checked per query against in-process DuckDB on the same files, and a server with wrong
or failed answers is marked n/a for that workload (never ranked). Upstream has no JDBC prepared statements (the Flight
SQL JDBC driver prepares every query) and answers `LIMIT` without `ORDER BY` with the whole table, so its pair runs only
point lookups, filtered count and metadata as small queries, and TPC-H over ADBC. Wave `c1-servers`:
45fc0a9e6e02 vs 27f583adccd7 at `duckDbThreads` 4 and 8 (local Parquet and S3), and upstream at its default
`duckDbThreads=2` (its `arrowflight.properties`; its docs give no other recommendation) vs 45fc0a9e6e02 at its default 4.
