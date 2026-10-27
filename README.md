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


## Server comparison reports (2026-10-27)

- **Report 1 SPEED** - [results/COMPARE-SPEED-2026-10-27.md](results/COMPARE-SPEED-2026-10-27.md): TPC-H SF1/SF10 (ADBC, JDBC,
  local, S3) is answered only by our builds; both upstream builds fail every TPC-H query for server-side reasons (single-table
  schema resolver, unrewritten subquery tables, DECIMAL vs float64 schema, no `AVG` / no prepared statements on up-main), so
  their columns are n/a with the reason. ours-new = ours-27f5 within noise on the same runner (bisect of 4 intermediate
  builds: no regression; the earlier 30-45 % gap was an aggregation artifact). Small queries: up-native has ~25 % lower JDBC
  p50 at c1/c8 but fails at c32; both upstream servers were OOM-killed inside the 6 GB limit in 3 of 6 rounds, ours never
  (peak 1.7-3.2 GB). Parallel raw Flight scans: up-native faster (4-8 streams, up to ~1.8x) at twice the memory.

- **Report 2 LOAD** - [results/COMPARE-LOAD-2026-10-27.md](results/COMPARE-LOAD-2026-10-27.md): on 2 server cores every
  server saturates at 1 client (p95 < 100 ms); throughput at saturation for point / count queries: up-native ~84 QPS, ours-new
  ~50, ours-27f5 ~45, up-main ~48 over ADBC (up-main fails every JDBC query). Only ours runs the heavy parts (mixed, 4 heavy at
  once: 0 failures, peak RSS 4.3 GB). Slow link (10 ms RTT, 1 Gbit/s): up-native with ZSTD exports `lineitem` at 264 MB/s vs
  104 MB/s plain (ours has no Flight compression). TLS + token on ours: latency and closed-loop QPS unchanged (1-128 clients), SF10 TPC-H 1.01x, export -11 %.

- **Report 3 ROBUSTNESS** - [results/COMPARE-ROBUSTNESS-2026-10-27.md](results/COMPARE-ROBUSTNESS-2026-10-27.md): 30-min
  soak without deaths or errors for ours (RSS settles ~2 GB); ours stops work at once on cancel, upstream keeps computing
  6.7-10.6 s; 3-node cluster on S3 answers TPC-H SF10 22/22 correctly with a node stopped or SIGKILLed mid-query, rejoin
  4-5 s; Trino + our connector 22/22 on all four servers; 2 DuckDB threads best for many small queries on 2 cores.

## In progress

- Server comparison task `ci/COMPARE-TASK.md` (4 servers). `ours-new` is pinned to `7562a5bdb7b9`, the build of the
  first comparison run (workflow input default). Newer pre-releases (`84fec772ec50` and any later one) are
  collected and tested only in a final run after Reports 1-3 (including the S3 read-cache pair). Every server runs in an identically limited
  container (`eclipse-temurin:21-jre`, 2 CPUs on cpus 0,1, 6 GB), clients (now also limited to 6 GB) and S3 in their own
  container on cpus 2,3.
  - Report 1 SPEED: **published** `results/COMPARE-SPEED-2026-10-27.md` (run 40537011671 merged with the ours pairs of
    40490378159; fix list items 1-4 at its top, bisect 40537018532: no build regresses).
  - Report 2 LOAD: **published** `results/COMPARE-LOAD-2026-10-27.md` (TLS closed-loop load split per side added, re-report run
    40569304541 of 40550942695 via the new `rereport` workflow).
  - Report 3 ROBUSTNESS: **published** `results/COMPARE-ROBUSTNESS-2026-10-27.md` (soak 40550552130, cold start + cancel
    40551848571, threads 40550556746, Trino 40551575311, cluster on S3 40553385813; the local-disk cluster attempt 40551320307
    showed that a cluster refuses complete answers without shared storage).
  - Next: final run of the task's "Later addition": compare run **40569584228** (wave `c10-cache`, dispatched 2026-10-27
    19:40 UTC, S3 only, `-DduckDbThreads=4` on both sides): `ours-cache` = newest pre-release `4e77c6bda59a` with
    `-Darrowflight.s3.cacheMegabytes=1024` (key `arrowflight.s3.cacheMegabytes`, MiB, 0 = off, at most half the heap) vs the
    same build with the cache off, both vs `ours-new`, and `84fec772ec50` vs `ours-new`; workloads TPC-H SF1/SF10 ADBC +
    small queries. When it finishes: check for failures, write a short `results/COMPARE-CACHE-2026-10-27.md` (cache on/off
    ratios, new builds vs ours-new), link it here, then write `ALL DONE <date>` at the top of this section.
  - `results/c2-speed-40481152975` is only a "no-container reference". `ci/ignored-runs.txt` blocks the aggregates of
    40483119136 (wrong `ours-new`), 40478832460 (old `c1-servers`) and 40539031628 (diagnostic).

## Latest server comparison: [c7-load-tls-40553901245](results/c7-load-tls-40553901245/summary.md)

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

### Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| new-plain-vs-tls-lat-local | ours-new `-` | ours-new `TLS` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | 0.96 | 1.01 | 1.08 | 1.09 | n/a | 1.01 | n/a | n/a | none |

### Per job (absolute medians and ratios)

#### new-plain-vs-tls-lat-local: A = ours-new `-`, B = ours-new `TLS`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small adbcscan adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 25.5 | 27.5 | 1.08 | 1.09 1.10 0.95 |
| small JDBC c1 p95 | ms | 53.3 | 54.3 | 1.02 | 1.02 1.08 0.97 |
| small JDBC c1 p99 | ms | 58.9 | 61.6 | 1.05 | 1.05 1.05 0.96 |
| small JDBC c8 p50 | ms | 124.2 | 122.7 | 0.99 | 0.93 1.00 1.01 |
| small JDBC c8 p95 | ms | 277.6 | 298.6 | 1.08 | 0.98 1.12 1.01 |
| small JDBC c8 p99 | ms | 340.6 | 406.7 | 1.19 | 0.93 1.20 1.23 |
| small JDBC c32 p50 | ms | 469.5 | 448.1 | 0.95 | 1.01 0.92 1.01 |
| small JDBC c32 p95 | ms | 1274.1 | 1385.5 | 1.09 | 0.98 1.11 1.04 |
| small JDBC c32 p99 | ms | 1788.4 | 1853.5 | 1.04 | 1.08 1.04 1.00 |
| small ADBC c1 p50 | ms | 17.7 | 17.0 | 0.96 | 1.03 0.95 0.91 |
| small ADBC c1 p95 | ms | 46.3 | 44.3 | 0.96 | 0.88 0.96 1.02 |
| small ADBC c1 p99 | ms | 61.4 | 54.4 | 0.89 | 0.85 0.87 0.95 |
| small ADBC c8 p50 | ms | 114.4 | 110.8 | 0.97 | 0.96 0.89 1.02 |
| small ADBC c8 p95 | ms | 268.0 | 280.2 | 1.05 | 0.96 1.05 1.08 |
| small ADBC c8 p99 | ms | 344.6 | 324.6 | 0.94 | 0.98 0.92 1.00 |
| small ADBC c32 p50 | ms | 436.5 | 435.0 | 1.00 | 0.99 1.01 0.98 |
| small ADBC c32 p95 | ms | 1244.7 | 1262.3 | 1.01 | 0.90 1.01 1.02 |
| small ADBC c32 p99 | ms | 1787.1 | 1700.0 | 0.95 | 0.85 0.95 1.05 |
| TPC-H SF10 ADBC (sum of medians) | s | 39.4 | 39.8 | 1.01 | 1.01 0.99 1.04 |
| lineitem export ADBC | MB/s | 481.2 | 426.5 | 0.89 | 0.92 0.92 0.86 |
| server RSS peak | MB | 2587.0 | 2699.0 | 1.04 | 0.99 1.00 1.05 |

## Results

- [c7-load-tls-40553901245](results/c7-load-tls-40553901245/summary.md) (latest of its wave)
- [c8-robust-cluster-40553385813](results/c8-robust-cluster-40553385813/summary.md) (latest of its wave)
- [c4-robust-40551848571](results/c4-robust-40551848571/summary.md) (latest of its wave)
- [c9-robust-trino-40551575311](results/c9-robust-trino-40551575311/summary.md) (latest of its wave)
- [c8-robust-cluster-40551320307](results/c8-robust-cluster-40551320307/summary.md)
- [c7-load-tls-40550942695](results/c7-load-tls-40550942695/summary.md)
- [c5-threads-40550556746](results/c5-threads-40550556746/summary.md) (latest of its wave)
- [c4-robust-40550552130](results/c4-robust-40550552130/summary.md)
- [c3-load-40540885908](results/c3-load-40540885908/summary.md) (latest of its wave)
- [c6-bisect-40537018532](results/c6-bisect-40537018532/summary.md) (latest of its wave)
- [c2-speed-40537011671](results/c2-speed-40537011671/summary.md) (latest of its wave)
- [c3-load-40490387806](results/c3-load-40490387806/summary.md)
- [c2-speed-40490378159](results/c2-speed-40490378159/summary.md)
- [c2-speed-40481152975](results/c2-speed-40481152975/summary.md)
- [w3-combos-c3b2-40232144198](results/w3-combos-c3b2-40232144198/summary.md) (latest of its wave)
- [w2-s3-and-layout-40211085777](results/w2-s3-and-layout-40211085777/summary.md) (latest of its wave)
- [w1-knobs-local-40211079235](results/w1-knobs-local-40211079235/summary.md) (latest of its wave)
- [w0-smoke-40210310231](results/w0-smoke-40210310231/summary.md) (latest of its wave)
