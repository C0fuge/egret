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


## In progress

- Server comparison task `ci/COMPARE-TASK.md` (4 servers). `ours-new` is pinned to `7562a5bdb7b9`, the build of the
  first comparison run (workflow input default). Newer pre-releases (`84fec772ec50` and any later one) are
  collected and tested only in a final run after Reports 1-3 (including the S3 read-cache pair). Every server runs in an identically limited
  container (`eclipse-temurin:21-jre`, 2 CPUs on cpus 0,1, 6 GB), clients (now also limited to 6 GB) and S3 in their own
  container on cpus 2,3.
  - Report 1 SPEED: first run 40490378159 finished; its ours-new vs ours-27f5 jobs are kept, its upstream jobs were
    unusable (every upstream S3 start failed: up-main has no S3 support, up-native needs its hadoop-aws jars and `s3a://`;
    up-main was OOM-killed inside the 6 GB limit after its point queries errored; both up-native local jobs died with
    "runner received a shutdown signal"). Fixed in 5ff4701 / 96c79b5 / 3802b4c / 14899cd (also the maintainer fix list
    items 1-3: JDBC answers compared numerically with the DuckDB rows, every failed query with its error text in the job
    log and in the report notes, up-native jobs in def and t8, upstream pairs split into `-tpch` and `-lat` jobs).
    Rerun of only the upstream pairs: run **40537011671** (dispatched 16:02 UTC, up-native = head `9fb08d9dd24d`,
    `merge-run=40490378159`, so its `speed.md` contains the ours pairs of the first run too; S3 and `-lat` jobs take
    ~1.5-3 h). Its aggregate commits `results/c2-speed-40537011671/`.
  - Upstream TPC-H over ADBC (fix list item 2, from the local `-tpch` jobs of 40537011671 and the 1-round diagnostic
    40539031628): every query fails on both upstream builds, for server-side reasons, so they are n/a with the reason:
    multi-table queries are rejected by upstream's schema resolver (`Can only select from ONE table`, on Prepare and on
    plain ExecuteQuery alike: upstream runs TPC-H only behind Spark, which does the joins); q04-style subqueries reach
    DuckDB with the table not rewritten (`schema "tpch" does not exist`); q06 returns DECIMAL(38,4) where the advertised
    schema says float64, which ADBC rejects; up-main also has no `AVG` (`Column 'avg(l_quantity)' not found`).
  - Next: when 40537011671 has committed its results, check `speed.md` (up-native small/scan local and S3, up-main
    small/scan local), copy it to `results/COMPARE-SPEED-2026-10-27.md` with the bisect result (below) and the upstream
    TPC-H reasons at the top, add a README summary, own commit. If an up-native `-lat` local job dies again with a runner
    shutdown, its log now shows the last workload and the host's free memory before it.
  - Fix list item 4, first look (job 27f5-vs-7562 of the bisect run, 5 rounds on one runner): ADBC SF10 sum of warm
    medians per round ours-27f5 25.9-27.4 s vs 7562a5bdb7b9 26.3-28.6 s, i.e. about 1 % apart, not 30-45 %. The gap in
    the first speed report is an aggregation artifact: its ours-new column pooled all ours-new jobs of a storage/setting
    (upstream pairs on other runners and CPU types included) while ours-27f5 came from its own pair job only. The speed
    report now prints the same-runner ours-27f5 / ours-new ratio under each TPC-H table ; in the first
    run's own pair job the ADBC SF10 ratio was 0.97 (summary.md).
  - Fix list item 4 (ours-new 30-45 % slower than ours-27f5 on ADBC SF10): wave `c6-bisect`, run **40537018532**
    (dispatched 16:02 UTC, 5 rounds, ADBC SF10 + small, ours-27f5 vs 45fc0a9e6e02 / e46f28dfdf09 / 6acc9cce0b26 /
    7562a5bdb7b9, each pair on one runner); its `results/c6-bisect-40537018532/summary.md` B/A ratios give the first slow
    build.
  - Report 2 LOAD: run 40490387806 finished (`results/c3-load-40490387806/load.md`); usable for ours and for upstream
    small-query load over ADBC (upstream TPC-H in heavy x4 / mixed / netem fails for the reasons above; up-main fails
    every JDBC load query). Running: `c3-load` run **40540885908** with `only=new-vs-native-zstd-netem` (up-native
    `-DflightCompression=zstd` on the netem path; its lineitem export is the comparable number) and
    `merge-run=40490387806`, `merge-prefix=new-vs-`, so its `load.md` covers both runs: publish that as
    `results/COMPARE-LOAD-2026-10-27.md` after Report 1. TLS + token for ours still to build: the
    server takes `FLIGHT_TLS_CERT` / `FLIGHT_TLS_KEY` (PEM files) and `FLIGHT_BEARER_TOKEN` (without
    `FLIGHT_ALLOW_INSECURE`); clients then need `grpc+tls://` with the self-signed CA (ADBC) and
    `useEncryption=true&token=...` (JDBC); ab.sh hardcodes the client URIs today.
  - Report 3 ROBUSTNESS: waves `c4-robust` (dispatch with rounds = 1: 30-min soak, cold starts, cancel) and `c5-threads`
    (rounds = 3) are committed, not yet dispatched; still to build: 3-node cluster and Trino plugin runs (ours only).
  - `results/c2-speed-40481152975` is only a "no-container reference". `ci/ignored-runs.txt` blocks the aggregates of
    40483119136 (wrong `ours-new`), 40478832460 (old `c1-servers`) and 40539031628 (diagnostic).

## Latest server comparison: [c6-bisect-40537018532](results/c6-bisect-40537018532/summary.md)

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

### Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 27f5-vs-45fc-local | ours-27f5 `-` | 45fc0a9e6e02 `-` | local | Linux ubuntu24 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C | 5/5 | 0.85 | 1.01 | 0.90 | 0.92 | n/a | 1.00 | n/a | n/a | none |
| 27f5-vs-6acc-local | ours-27f5 `-` | 6acc9cce0b26 `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 5/5 | 0.84 | 0.92 | 0.86 | 0.99 | n/a | 1.00 | n/a | n/a | none |
| 27f5-vs-7562-local | ours-27f5 `-` | ours-new `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor | 5/5 | 0.78 | 0.90 | 0.95 | 1.02 | n/a | 1.01 | n/a | n/a | none |
| 27f5-vs-e46f-local | ours-27f5 `-` | e46f28dfdf09 `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor | 5/5 | 0.79 | 0.90 | 0.88 | 0.89 | n/a | 0.98 | n/a | n/a | none |

### Per job (absolute medians and ratios)

#### 27f5-vs-45fc-local: A = ours-27f5 `-`, B = 45fc0a9e6e02 `-`, local

Runner: Linux ubuntu24 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C. Workloads: `adbc10 small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 27.1 | 24.4 | 0.90 | 0.93 0.86 0.93 0.89 0.87 |
| small JDBC c1 p95 | ms | 58.3 | 52.0 | 0.89 | 0.92 0.96 0.89 0.89 0.81 |
| small JDBC c1 p99 | ms | 69.4 | 63.8 | 0.92 | 1.04 1.04 0.85 0.95 0.82 |
| small JDBC c8 p50 | ms | 133.1 | 121.5 | 0.91 | 0.89 0.91 0.86 0.92 0.93 |
| small JDBC c8 p95 | ms | 286.4 | 274.0 | 0.96 | 1.04 0.91 0.96 0.92 0.98 |
| small JDBC c8 p99 | ms | 359.5 | 333.9 | 0.93 | 1.00 0.95 0.89 0.86 0.97 |
| small JDBC c32 p50 | ms | 510.6 | 482.8 | 0.95 | 0.96 0.88 0.95 0.92 0.95 |
| small JDBC c32 p95 | ms | 1190.7 | 1093.9 | 0.92 | 0.92 0.92 0.86 0.89 1.00 |
| small JDBC c32 p99 | ms | 1467.7 | 1402.5 | 0.96 | 0.96 0.97 0.86 0.93 1.00 |
| small ADBC c1 p50 | ms | 20.1 | 17.1 | 0.85 | 0.84 0.86 0.79 0.80 0.87 |
| small ADBC c1 p95 | ms | 46.0 | 44.6 | 0.97 | 0.91 0.90 1.02 0.97 0.97 |
| small ADBC c1 p99 | ms | 65.4 | 63.9 | 0.98 | 0.88 1.13 0.86 0.90 0.93 |
| small ADBC c8 p50 | ms | 131.2 | 114.1 | 0.87 | 0.91 0.86 0.87 0.84 0.86 |
| small ADBC c8 p95 | ms | 285.1 | 258.1 | 0.91 | 0.92 0.85 0.95 0.89 0.96 |
| small ADBC c8 p99 | ms | 342.8 | 321.6 | 0.94 | 0.99 0.88 1.03 0.88 0.88 |
| small ADBC c32 p50 | ms | 509.4 | 410.1 | 0.81 | 0.78 0.81 0.86 0.79 0.88 |
| small ADBC c32 p95 | ms | 1191.8 | 1206.6 | 1.01 | 1.02 1.00 1.04 0.98 1.02 |
| small ADBC c32 p99 | ms | 1463.9 | 1733.3 | 1.18 | 1.20 1.28 1.17 1.20 1.11 |
| TPC-H SF10 ADBC (sum of medians) | s | 40.3 | 40.1 | 1.00 | 0.99 0.99 1.00 1.00 0.99 |
| server RSS peak | MB | 1566.0 | 1546.0 | 0.99 | 0.98 1.00 0.99 0.97 1.01 |

#### 27f5-vs-6acc-local: A = ours-27f5 `-`, B = 6acc9cce0b26 `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `adbc10 small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 26.7 | 23.0 | 0.86 | 0.83 0.92 0.83 0.86 0.90 |
| small JDBC c1 p95 | ms | 58.8 | 52.4 | 0.89 | 0.83 1.00 0.89 0.86 0.95 |
| small JDBC c1 p99 | ms | 66.5 | 63.1 | 0.95 | 0.90 1.04 0.85 0.82 0.89 |
| small JDBC c8 p50 | ms | 135.8 | 114.9 | 0.85 | 0.86 0.85 0.87 0.82 0.94 |
| small JDBC c8 p95 | ms | 307.9 | 286.4 | 0.93 | 0.90 0.97 0.96 0.93 0.91 |
| small JDBC c8 p99 | ms | 386.3 | 383.0 | 0.99 | 0.86 1.05 1.08 0.94 0.87 |
| small JDBC c32 p50 | ms | 507.7 | 435.7 | 0.86 | 0.83 0.90 0.82 0.85 0.96 |
| small JDBC c32 p95 | ms | 1270.2 | 1258.1 | 0.99 | 0.89 0.96 1.02 0.98 1.00 |
| small JDBC c32 p99 | ms | 1634.1 | 1677.0 | 1.03 | 0.71 0.95 1.08 1.08 1.03 |
| small ADBC c1 p50 | ms | 19.9 | 16.7 | 0.84 | 0.89 0.81 0.82 0.84 0.81 |
| small ADBC c1 p95 | ms | 47.3 | 45.8 | 0.97 | 1.05 0.97 0.81 1.05 0.87 |
| small ADBC c1 p99 | ms | 64.2 | 53.3 | 0.83 | 0.93 0.80 0.73 1.00 0.80 |
| small ADBC c8 p50 | ms | 123.3 | 107.8 | 0.87 | 0.86 0.83 0.86 0.87 0.88 |
| small ADBC c8 p95 | ms | 288.8 | 269.4 | 0.93 | 0.86 0.93 0.97 0.90 0.97 |
| small ADBC c8 p99 | ms | 347.9 | 329.5 | 0.95 | 0.53 1.00 0.91 0.95 1.12 |
| small ADBC c32 p50 | ms | 460.6 | 405.9 | 0.88 | 0.74 0.85 0.89 0.87 0.94 |
| small ADBC c32 p95 | ms | 1382.9 | 1269.6 | 0.92 | 0.89 0.92 0.89 0.95 0.97 |
| small ADBC c32 p99 | ms | 1773.6 | 1831.6 | 1.03 | 1.10 1.03 0.98 0.82 1.06 |
| TPC-H SF10 ADBC (sum of medians) | s | 37.9 | 37.7 | 1.00 | 1.00 0.99 1.00 0.98 1.02 |
| server RSS peak | MB | 1610.0 | 1640.0 | 1.02 | 1.00 0.95 1.06 1.02 1.02 |

#### 27f5-vs-7562-local: A = ours-27f5 `-`, B = ours-new `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `adbc10 small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 19.9 | 19.0 | 0.95 | 1.07 0.89 0.86 0.84 0.87 |
| small JDBC c1 p95 | ms | 41.7 | 39.3 | 0.94 | 1.02 0.99 0.87 0.86 0.93 |
| small JDBC c1 p99 | ms | 56.2 | 51.1 | 0.91 | 0.84 1.09 0.95 0.91 1.01 |
| small JDBC c8 p50 | ms | 97.1 | 86.1 | 0.89 | 0.90 0.89 0.83 0.99 0.86 |
| small JDBC c8 p95 | ms | 218.8 | 210.3 | 0.96 | 0.94 0.96 1.00 0.99 1.00 |
| small JDBC c8 p99 | ms | 272.3 | 260.7 | 0.96 | 0.96 0.91 1.22 1.11 1.02 |
| small JDBC c32 p50 | ms | 352.3 | 340.2 | 0.97 | 0.93 0.84 0.91 1.01 0.86 |
| small JDBC c32 p95 | ms | 900.9 | 915.1 | 1.02 | 0.92 0.93 0.98 1.02 0.97 |
| small JDBC c32 p99 | ms | 1227.8 | 1217.8 | 0.99 | 0.99 0.97 0.99 1.00 0.96 |
| small ADBC c1 p50 | ms | 15.2 | 11.9 | 0.78 | 0.87 0.75 0.75 0.81 0.76 |
| small ADBC c1 p95 | ms | 31.5 | 30.5 | 0.97 | 0.94 0.74 1.01 1.02 1.02 |
| small ADBC c1 p99 | ms | 47.5 | 39.6 | 0.83 | 0.83 0.69 1.03 0.85 0.87 |
| small ADBC c8 p50 | ms | 92.0 | 74.6 | 0.81 | 0.87 0.77 0.81 0.87 0.83 |
| small ADBC c8 p95 | ms | 210.9 | 190.7 | 0.90 | 0.98 0.84 0.88 0.95 0.99 |
| small ADBC c8 p99 | ms | 260.9 | 237.3 | 0.91 | 0.96 0.93 0.94 0.86 0.86 |
| small ADBC c32 p50 | ms | 341.4 | 314.5 | 0.92 | 0.80 0.89 0.89 1.00 0.86 |
| small ADBC c32 p95 | ms | 1038.0 | 930.2 | 0.90 | 0.87 0.89 0.88 0.92 0.87 |
| small ADBC c32 p99 | ms | 1427.1 | 1432.1 | 1.00 | 0.94 1.07 1.01 1.06 0.73 |
| TPC-H SF10 ADBC (sum of medians) | s | 27.0 | 27.3 | 1.01 | 1.06 0.97 1.01 0.99 1.02 |
| server RSS peak | MB | 1734.0 | 1561.0 | 0.90 | 0.89 0.90 0.99 1.08 0.88 |

#### 27f5-vs-e46f-local: A = ours-27f5 `-`, B = e46f28dfdf09 `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `adbc10 small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 22.8 | 20.1 | 0.88 | 0.92 0.72 0.99 0.76 1.01 |
| small JDBC c1 p95 | ms | 44.0 | 41.0 | 0.93 | 0.87 0.93 0.96 0.90 0.97 |
| small JDBC c1 p99 | ms | 58.0 | 50.5 | 0.87 | 0.70 1.08 1.06 0.87 1.10 |
| small JDBC c8 p50 | ms | 104.4 | 92.4 | 0.88 | 0.94 0.82 0.94 0.89 0.88 |
| small JDBC c8 p95 | ms | 223.2 | 214.6 | 0.96 | 0.97 0.93 0.92 0.92 0.99 |
| small JDBC c8 p99 | ms | 274.5 | 279.3 | 1.02 | 1.03 1.11 0.89 1.03 0.96 |
| small JDBC c32 p50 | ms | 411.6 | 338.7 | 0.82 | 0.87 0.81 0.88 0.87 0.81 |
| small JDBC c32 p95 | ms | 1030.3 | 912.2 | 0.89 | 0.97 0.84 0.88 0.96 0.90 |
| small JDBC c32 p99 | ms | 1287.2 | 1194.4 | 0.93 | 1.02 0.89 0.92 0.95 0.96 |
| small ADBC c1 p50 | ms | 15.9 | 12.6 | 0.79 | 0.76 0.88 0.77 0.75 0.79 |
| small ADBC c1 p95 | ms | 36.0 | 33.5 | 0.93 | 0.94 1.01 0.87 0.82 0.91 |
| small ADBC c1 p99 | ms | 45.6 | 49.0 | 1.08 | 1.08 1.20 1.08 0.81 0.92 |
| small ADBC c8 p50 | ms | 97.8 | 78.8 | 0.81 | 0.88 0.71 0.84 0.85 0.80 |
| small ADBC c8 p95 | ms | 220.1 | 194.7 | 0.88 | 0.94 0.88 0.98 0.91 0.85 |
| small ADBC c8 p99 | ms | 277.8 | 246.9 | 0.89 | 0.91 0.87 1.01 0.93 0.83 |
| small ADBC c32 p50 | ms | 363.4 | 325.6 | 0.90 | 0.92 0.91 0.90 0.86 0.89 |
| small ADBC c32 p95 | ms | 1066.5 | 963.1 | 0.90 | 0.93 0.86 0.89 0.96 0.88 |
| small ADBC c32 p99 | ms | 1413.0 | 1368.8 | 0.97 | 0.90 0.97 0.92 0.91 1.27 |
| TPC-H SF10 ADBC (sum of medians) | s | 27.7 | 27.2 | 0.98 | 0.99 0.97 1.00 0.98 0.99 |
| server RSS peak | MB | 1723.0 | 1621.0 | 0.94 | 1.09 0.90 1.02 1.01 0.93 |

## Results

- [c6-bisect-40537018532](results/c6-bisect-40537018532/summary.md) (latest of its wave)
- [c3-load-40490387806](results/c3-load-40490387806/summary.md) (latest of its wave)
- [c2-speed-40490378159](results/c2-speed-40490378159/summary.md) (latest of its wave)
- [c2-speed-40481152975](results/c2-speed-40481152975/summary.md)
- [w3-combos-c3b2-40232144198](results/w3-combos-c3b2-40232144198/summary.md) (latest of its wave)
- [w2-s3-and-layout-40211085777](results/w2-s3-and-layout-40211085777/summary.md) (latest of its wave)
- [w1-knobs-local-40211079235](results/w1-knobs-local-40211079235/summary.md) (latest of its wave)
- [w0-smoke-40210310231](results/w0-smoke-40210310231/summary.md) (latest of its wave)
