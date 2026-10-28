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

ALL DONE 2026-10-27 (compare task: Reports 1-3, fix list, later addition published).

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
  - Final run ("Later addition"): **published** `results/COMPARE-CACHE-2026-10-27.md` (run 40569584228, wave `c10-cache`):
    S3 cache on (`4e77c6bda59a`, 1 GiB) makes repeated small queries faster (p50 1.4-4x, p95 8-20x) and SF1 ~2-3x, SF10 ~8 % slower, peak RSS
    ~5.7 GB of the 6 GB limit; cache off equals `ours-new`; `84fec772ec50` inconclusive (noisy rounds, no consistent regression).
  - Phase B (`ci/BUILD-TRACK-TASK.md`): build 1 = `d22cdaccb4e1` (item 20 (b) LZ4 streams; contains ZSTD streams 6ca7352,
    item 19 threads default, item 17 (b)-(d), Iceberg items; skipped as contained: 84fec772ec50 8625e28f08cd b28fedf9edbf
    752e272b3ab6 04e558056068 4e77c6bda59a b7be8d166498 85aaf4604d9a) vs `7562a5bdb7b9`. Compare run 40602868592
    (wave `track-load-d22cdaccb4e1`): 13 of 14 jobs complete, results in `results/track-load-d22cdaccb4e1-40602868592/`
    (`load.md` re-reported by 40621233483 with the new per-job netem pair table). `core-def-tpch-s3` hit the 170 min job
    limit (SF1/SF10 ADBC only 2 rounds; not usable for the regression rule), so it is split into `core-def-sf10jdbc-s3`,
    `core-def-sf10adbc-s3`, `core-def-sf1-s3`: compare run **40621069419** (started 2026-10-28 02:28 UTC,
    `merge-run=40602868592`, merge-prefix `core-,i20-`; its aggregate commits `results/track-load-d22cdaccb4e1-40621069419/`
    with all jobs). So far (B = d22cdaccb4e1 / A = baseline): local SF10 ADBC 0.98, JDBC 0.99, SF1 0.94; t4 ~1.00; small
    c1 p50 0.94 local / 0.88 S3, c32 p95 0.88 local / 0.82 S3 (JDBC S3 1.21); scan x8 1.15 local / 1.10 S3; netem export
    plain 1.00, CLZ4 2.51x (261 MB/s), CZSTD 3.46x (361 MB/s) vs 104 MB/s; up-native ZSTD 256-260 MB/s on the same runners;
    fast link: CZSTD export 0.47x, CLZ4 0.67x of plain; ours 22/22 everywhere (up-native 0/22 on netem TPC-H, upstream
    side); peak RSS within +-10 %.
    Next session: check 40621069419 (failed job: re-run it with `only=` + `merge-run=40621069419`), then write
    `results/track-d22cdaccb4e1/summary.md` and the first `results/BUILDS.md` row (ratios, 22/22, peak RSS, verdict;
    regression rule of the task), then the next untracked pre-release.
    Note: the aggregate job rebuilds README from `ci/README-status.md`: edit 'In progress' THERE, not only in README.
  - `results/c2-speed-40481152975` is only a "no-container reference". `ci/ignored-runs.txt` blocks the aggregates of
    40483119136 (wrong `ours-new`), 40478832460 (old `c1-servers`) and 40539031628 (diagnostic).

## Latest server comparison: [c10-cache-40569584228](results/c10-cache-40569584228/summary.md)

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

### Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cache-off-vs-on-s3 | ours-cache `-DduckDbThreads=4` | ours-cache `-DduckDbThreads=4 -Darrowflight.s3.cacheMegabytes=1024` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | 0.33 | 0.06 | 0.64 | 0.07 | 0.32 | 1.08 | n/a | n/a | none |
| new-vs-84fe-s3 | ours-new `-DduckDbThreads=4` | 84fec772ec50 `-DduckDbThreads=4` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | 1.23 | 1.58 | 0.99 | 1.51 | 1.45 | 0.83 | n/a | n/a | none |
| new-vs-cache-off-s3 | ours-new `-DduckDbThreads=4` | ours-cache `-DduckDbThreads=4` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | 1.09 | 1.02 | 0.88 | 1.02 | 1.00 | 1.01 | n/a | n/a | none |
| new-vs-cache-on-s3 | ours-new `-DduckDbThreads=4` | ours-cache `-DduckDbThreads=4 -Darrowflight.s3.cacheMegabytes=1024` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | 0.57 | 0.11 | 0.70 | 0.11 | 0.47 | 1.08 | n/a | n/a | none |

### Per job (absolute medians and ratios)

#### cache-off-vs-on-s3: A = ours-cache `-DduckDbThreads=4`, B = ours-cache `-DduckDbThreads=4 -Darrowflight.s3.cacheMegabytes=1024`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `adbc10 adbc1 small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 30.1 | 19.3 | 0.64 | 0.70 0.59 0.58 |
| small JDBC c1 p95 | ms | 986.1 | 82.1 | 0.08 | 0.12 0.08 0.09 |
| small JDBC c1 p99 | ms | 1019.2 | 102.5 | 0.10 | 0.13 0.10 0.10 |
| small JDBC c8 p50 | ms | 383.9 | 89.2 | 0.23 | 0.37 0.21 0.23 |
| small JDBC c8 p95 | ms | 5940.2 | 294.1 | 0.05 | 0.07 0.05 0.05 |
| small JDBC c8 p99 | ms | 6687.1 | 338.6 | 0.05 | 0.07 0.04 0.05 |
| small JDBC c32 p50 | ms | 1389.9 | 404.5 | 0.29 | 0.42 0.29 0.28 |
| small JDBC c32 p95 | ms | 20034.4 | 1350.4 | 0.07 | 0.11 0.06 0.07 |
| small JDBC c32 p99 | ms | 22775.5 | 1616.1 | 0.07 | 0.11 0.06 0.07 |
| small ADBC c1 p50 | ms | 33.4 | 11.2 | 0.33 | 0.54 0.32 0.32 |
| small ADBC c1 p95 | ms | 988.3 | 75.9 | 0.08 | 0.11 0.08 0.08 |
| small ADBC c1 p99 | ms | 1058.4 | 102.5 | 0.10 | 0.14 0.10 0.09 |
| small ADBC c8 p50 | ms | 312.5 | 68.6 | 0.22 | 0.30 0.17 0.22 |
| small ADBC c8 p95 | ms | 6047.9 | 302.8 | 0.05 | 0.08 0.05 0.05 |
| small ADBC c8 p99 | ms | 6900.9 | 348.5 | 0.05 | 0.08 0.05 0.03 |
| small ADBC c32 p50 | ms | 1373.9 | 328.4 | 0.24 | 0.37 0.25 0.22 |
| small ADBC c32 p95 | ms | 20900.7 | 1261.2 | 0.06 | 0.09 0.05 0.06 |
| small ADBC c32 p99 | ms | 25111.4 | 1462.5 | 0.06 | 0.06 0.05 0.06 |
| TPC-H SF1 ADBC (sum of medians) | s | 34.4 | 11.0 | 0.32 | 0.45 0.34 0.31 |
| TPC-H SF10 ADBC (sum of medians) | s | 350.7 | 380.0 | 1.08 | 1.22 1.08 1.22 |
| server RSS peak | MB | 2338.0 | 5725.0 | 2.45 | 2.33 2.63 2.47 |

#### new-vs-84fe-s3: A = ours-new `-DduckDbThreads=4`, B = 84fec772ec50 `-DduckDbThreads=4`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `adbc10 adbc1 small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 33.0 | 32.7 | 0.99 | 0.99 1.04 0.96 |
| small JDBC c1 p95 | ms | 744.9 | 735.1 | 0.99 | 0.98 1.08 0.99 |
| small JDBC c1 p99 | ms | 1236.8 | 794.9 | 0.64 | 0.59 1.55 0.95 |
| small JDBC c8 p50 | ms | 352.9 | 360.5 | 1.02 | 1.02 0.97 0.99 |
| small JDBC c8 p95 | ms | 5226.0 | 6114.8 | 1.17 | 1.22 0.97 1.01 |
| small JDBC c8 p99 | ms | 5621.7 | 7812.5 | 1.39 | 1.45 0.97 0.99 |
| small JDBC c32 p50 | ms | 1101.4 | 1654.9 | 1.50 | 1.81 0.95 1.13 |
| small JDBC c32 p95 | ms | 16373.8 | 24699.2 | 1.51 | 1.54 1.00 1.27 |
| small JDBC c32 p99 | ms | 18204.6 | 27091.2 | 1.49 | 1.83 1.00 1.41 |
| small ADBC c1 p50 | ms | 23.7 | 29.1 | 1.23 | 1.06 1.09 1.26 |
| small ADBC c1 p95 | ms | 780.0 | 730.6 | 0.94 | 0.91 1.01 0.98 |
| small ADBC c1 p99 | ms | 805.7 | 867.2 | 1.08 | 1.08 0.94 1.03 |
| small ADBC c8 p50 | ms | 338.3 | 454.0 | 1.34 | 1.37 0.92 0.96 |
| small ADBC c8 p95 | ms | 5300.6 | 7484.0 | 1.41 | 1.41 1.02 0.97 |
| small ADBC c8 p99 | ms | 5992.5 | 8189.4 | 1.37 | 1.42 1.11 0.92 |
| small ADBC c32 p50 | ms | 1084.7 | 1446.6 | 1.33 | 1.33 0.97 1.39 |
| small ADBC c32 p95 | ms | 16144.8 | 25498.1 | 1.58 | 1.61 1.06 1.58 |
| small ADBC c32 p99 | ms | 17999.0 | 49262.6 | 2.74 | 3.87 1.20 2.74 |
| TPC-H SF1 ADBC (sum of medians) | s | 26.0 | 37.7 | 1.45 | 1.45 0.97 1.50 |
| TPC-H SF10 ADBC (sum of medians) | s | 353.6 | 292.7 | 0.83 | 1.00 1.03 0.82 |
| server RSS peak | MB | 2327.0 | 2200.0 | 0.95 | 0.97 0.98 0.92 |

#### new-vs-cache-off-s3: A = ours-new `-DduckDbThreads=4`, B = ours-cache `-DduckDbThreads=4`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `adbc10 adbc1 small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 33.3 | 29.2 | 0.88 | 0.87 0.87 1.09 |
| small JDBC c1 p95 | ms | 938.9 | 946.0 | 1.01 | 1.01 1.00 1.01 |
| small JDBC c1 p99 | ms | 994.9 | 1046.5 | 1.05 | 1.03 1.06 0.98 |
| small JDBC c8 p50 | ms | 357.5 | 343.7 | 0.96 | 1.05 1.07 0.92 |
| small JDBC c8 p95 | ms | 6030.4 | 6179.9 | 1.02 | 0.99 1.02 1.04 |
| small JDBC c8 p99 | ms | 12674.3 | 13878.0 | 1.09 | 0.93 0.94 1.71 |
| small JDBC c32 p50 | ms | 1462.3 | 1447.3 | 0.99 | 0.97 0.98 0.99 |
| small JDBC c32 p95 | ms | 20678.8 | 21037.1 | 1.02 | 0.99 1.02 0.99 |
| small JDBC c32 p99 | ms | 23508.4 | 37791.8 | 1.61 | 0.98 1.78 1.16 |
| small ADBC c1 p50 | ms | 30.8 | 33.5 | 1.09 | 1.33 1.11 0.97 |
| small ADBC c1 p95 | ms | 958.6 | 947.7 | 0.99 | 1.03 0.96 1.00 |
| small ADBC c1 p99 | ms | 1058.6 | 1018.0 | 0.96 | 1.16 0.96 0.98 |
| small ADBC c8 p50 | ms | 393.5 | 395.4 | 1.00 | 0.97 0.98 1.04 |
| small ADBC c8 p95 | ms | 5783.8 | 5753.0 | 0.99 | 1.01 1.04 0.99 |
| small ADBC c8 p99 | ms | 6192.5 | 6423.9 | 1.04 | 0.97 1.05 1.03 |
| small ADBC c32 p50 | ms | 1434.8 | 1517.5 | 1.06 | 1.76 0.98 1.06 |
| small ADBC c32 p95 | ms | 20184.1 | 20529.9 | 1.02 | 1.48 1.02 1.04 |
| small ADBC c32 p99 | ms | 23026.9 | 23300.3 | 1.01 | 1.31 1.00 1.02 |
| TPC-H SF1 ADBC (sum of medians) | s | 33.7 | 33.7 | 1.00 | 1.40 0.97 1.00 |
| TPC-H SF10 ADBC (sum of medians) | s | 385.1 | 387.7 | 1.01 | 1.01 1.00 1.02 |
| server RSS peak | MB | 2324.0 | 2309.0 | 0.99 | 0.97 0.95 1.04 |

#### new-vs-cache-on-s3: A = ours-new `-DduckDbThreads=4`, B = ours-cache `-DduckDbThreads=4 -Darrowflight.s3.cacheMegabytes=1024`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `adbc10 adbc1 small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 33.5 | 23.5 | 0.70 | 0.70 0.52 0.79 |
| small JDBC c1 p95 | ms | 811.5 | 100.9 | 0.12 | 0.12 0.08 0.13 |
| small JDBC c1 p99 | ms | 1685.7 | 113.9 | 0.07 | 0.06 0.07 0.13 |
| small JDBC c8 p50 | ms | 345.9 | 125.7 | 0.36 | 0.38 0.25 0.36 |
| small JDBC c8 p95 | ms | 5656.2 | 413.8 | 0.07 | 0.08 0.06 0.07 |
| small JDBC c8 p99 | ms | 7054.0 | 472.5 | 0.07 | 0.08 0.06 0.07 |
| small JDBC c32 p50 | ms | 1071.1 | 540.9 | 0.51 | 0.53 0.34 0.49 |
| small JDBC c32 p95 | ms | 16580.3 | 1835.4 | 0.11 | 0.11 0.07 0.12 |
| small JDBC c32 p99 | ms | 27540.0 | 2231.8 | 0.08 | 0.04 0.08 0.11 |
| small ADBC c1 p50 | ms | 25.7 | 14.6 | 0.57 | 0.66 0.37 0.57 |
| small ADBC c1 p95 | ms | 780.8 | 94.0 | 0.12 | 0.12 0.09 0.12 |
| small ADBC c1 p99 | ms | 860.1 | 110.0 | 0.13 | 0.13 0.10 0.13 |
| small ADBC c8 p50 | ms | 352.7 | 98.0 | 0.28 | 0.28 0.21 0.30 |
| small ADBC c8 p95 | ms | 5503.0 | 418.4 | 0.08 | 0.08 0.06 0.08 |
| small ADBC c8 p99 | ms | 6089.1 | 494.0 | 0.08 | 0.34 0.06 0.08 |
| small ADBC c32 p50 | ms | 1094.9 | 443.4 | 0.40 | 0.40 0.29 0.46 |
| small ADBC c32 p95 | ms | 16677.5 | 1789.2 | 0.11 | 0.11 0.07 0.12 |
| small ADBC c32 p99 | ms | 37918.8 | 2863.7 | 0.08 | 0.18 0.05 0.08 |
| TPC-H SF1 ADBC (sum of medians) | s | 26.9 | 12.6 | 0.47 | 0.49 0.32 0.48 |
| TPC-H SF10 ADBC (sum of medians) | s | 389.1 | 419.2 | 1.08 | 1.45 1.32 1.03 |
| server RSS peak | MB | 2219.0 | 5709.0 | 2.57 | 2.46 2.60 2.55 |

## Results

- [track-load-d22cdaccb4e1-40621069419](results/track-load-d22cdaccb4e1-40621069419/summary.md) (latest of its wave)
- [track-load-d22cdaccb4e1-40602868592](results/track-load-d22cdaccb4e1-40602868592/summary.md)
- [c10-cache-40569584228](results/c10-cache-40569584228/summary.md) (latest of its wave)
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
