# egret: A/B screening of Arrow Flight SQL server settings in CI

Each job of the `screen` workflow runs on one GitHub-hosted runner (4 vCPU, 16 GB) and compares the server's default
configuration (side A) with one variant (side B: server flags, JVM flags or a data layout) on that same runner, in
alternating rounds (A B, B A, A B), so runner-to-runner noise cancels out. Results are **ratios variant / default**;
absolute numbers from shared 4-vCPU runners are not comparable with a real deployment.

- Server: the public release `server-1.0.0-<id>` of C0fuge/kestrel (jar + runtime libs + plugins), DuckDB v1.4.5
  httpfs extension from extensions.duckdb.org, 8 GB server container (`-Xmx3g -XX:MaxDirectMemorySize=2g`).
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


## Results

- [w2-s3-and-layout-40211085777](results/w2-s3-and-layout-40211085777/summary.md) (latest of its wave)
- [w1-knobs-local-40211079235](results/w1-knobs-local-40211079235/summary.md) (latest of its wave)
- [w0-smoke-40210310231](results/w0-smoke-40210310231/summary.md) (latest of its wave)
