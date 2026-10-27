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
  - Fix list item 4 done, run 40537018532 (`results/c6-bisect-40537018532/summary.md`, 5 rounds, each build vs
    ours-27f5 on one runner): ADBC SF10 sum of medians B / A = 45fc0a9e6e02 1.00, e46f28dfdf09 0.98, 6acc9cce0b26
    1.00, 7562a5bdb7b9 1.01; small ADBC c1 p50 0.90-1.01 (newer builds equal or faster). **No build regresses.** The
    30-45 % gap of the first speed report was an aggregation artifact (its ours-new column pooled jobs from other runners
    and CPU types, ours-27f5 came from its own pair job only); the speed report now prints the same-runner
    ours-27f5 / ours-new ratio under each TPC-H table. Put this at the top of Report 1.
  - up-main small/scan (`-lat` jobs of 40537011671): JDBC point / count / LIMIT queries fail at once (no prepared
    statements), metadata answers, and the server is OOM-killed (exit 137) inside its 6 GB limit during the ADBC c1
    small queries in every round, so its scans are n/a too (a result, limit not raised).
  - Report 2 LOAD: ZSTD run 40540885908 finished (`results/c3-load-40540885908/load.md`, merged with 40490387806):
    netem 10 ms / 1 Gbit/s full lineitem export over ADBC: up-native with ZSTD 264 MB/s vs ours-new plain 104 MB/s.
    Publish it as `results/COMPARE-LOAD-2026-10-27.md` after Report 1. Earlier: run 40490387806 finished (`results/c3-load-40490387806/load.md`); usable for ours and for upstream
    small-query load over ADBC (upstream TPC-H in heavy x4 / mixed / netem fails for the reasons above; up-main fails
    every JDBC load query). TLS + token: run 40550942695 below.
  - Report 3 ROBUSTNESS (all dispatched 17:26-17:33 UTC): `c4-robust` run **40550552130** (rounds 1: 30-min soak, cold
    starts, cancel; all 3 pairs), `c5-threads` run **40550556746** (rounds 3: ours-new duckDbThreads 1/2/4/8, SF1/SF10 ADBC +
    small), `c8-robust-cluster` run **40551320307** (new `cluster` workload: 3 kestrel nodes on one runner, 4 GB / 2 CPUs
    each on cpus 0,1 since 3 x 6 GB does not fit; node 3 stopped before SF10 TPC-H, node 2 SIGKILLed during q18/q21, time until
    node 1 answers q06 correctly again, rejoin times, every check vs the reference answers), `c9-robust-trino` run
    **40551575311** (new `trino` workload: TPC-H SF1 through Trino 455 + the C0fuge/heron connector built read-only by the
    new `trino-plugin` job, answers vs heron's reference via its compare.py; upstream pairs record their failure text).
    The stock Flight SQL JDBC driver TPC-H is the JDBC tables of Report 1 (upstream fails there). Next: when they have
    committed, check `robust.md` / `summary.md` and the job logs (cluster / trino lines are in result.txt), fix failures,
    then write `results/COMPARE-ROBUSTNESS-2026-10-27.md`.
  - Report 2 TLS: `c7-load-tls` run **40550942695** (ours-new plain vs TLS + bearer token; new flag word `TLS` in ab.sh:
    self-signed cert, `FLIGHT_TLS_CERT/KEY` + `FLIGHT_BEARER_TOKEN`, clients `grpc+tls://` / `useEncryption=true&token&tlsRootCerts`).
  - `results/c2-speed-40481152975` is only a "no-container reference". `ci/ignored-runs.txt` blocks the aggregates of
    40483119136 (wrong `ours-new`), 40478832460 (old `c1-servers`) and 40539031628 (diagnostic).

## Latest server comparison: [c9-robust-trino-40551575311](results/c9-robust-trino-40551575311/summary.md)

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

### Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| new-vs-27f5-trino-local | ours-new `-` | ours-27f5 `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor | 1/1 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| new-vs-main-trino-local | ours-new `-` | up-main `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 1/1 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| new-vs-native-trino-local | ours-new `-` | up-native `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 1/1 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |

### Per job (absolute medians and ratios)

#### new-vs-27f5-trino-local: A = ours-new `-`, B = ours-27f5 `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `trino`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 954.0 | 806.0 | 0.84 | 0.84 |

#### new-vs-main-trino-local: A = ours-new `-`, B = up-main `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `trino`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 970.0 | 1359.0 | 1.40 | 1.40 |

#### new-vs-native-trino-local: A = ours-new `-`, B = up-native `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `trino`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 825.0 | 1123.0 | 1.36 | 1.36 |

## Results

- [c9-robust-trino-40551575311](results/c9-robust-trino-40551575311/summary.md) (latest of its wave)
- [c8-robust-cluster-40551320307](results/c8-robust-cluster-40551320307/summary.md) (latest of its wave)
- [c5-threads-40550556746](results/c5-threads-40550556746/summary.md) (latest of its wave)
- [c3-load-40540885908](results/c3-load-40540885908/summary.md) (latest of its wave)
- [c6-bisect-40537018532](results/c6-bisect-40537018532/summary.md) (latest of its wave)
- [c3-load-40490387806](results/c3-load-40490387806/summary.md)
- [c2-speed-40490378159](results/c2-speed-40490378159/summary.md) (latest of its wave)
- [c2-speed-40481152975](results/c2-speed-40481152975/summary.md)
- [w3-combos-c3b2-40232144198](results/w3-combos-c3b2-40232144198/summary.md) (latest of its wave)
- [w2-s3-and-layout-40211085777](results/w2-s3-and-layout-40211085777/summary.md) (latest of its wave)
- [w1-knobs-local-40211079235](results/w1-knobs-local-40211079235/summary.md) (latest of its wave)
- [w0-smoke-40210310231](results/w0-smoke-40210310231/summary.md) (latest of its wave)
