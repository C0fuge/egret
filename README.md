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

- Server comparison task `ci/COMPARE-TASK.md` (4 servers: ours-new, ours-27f5, up-native, up-main). Report 1 SPEED:
  `compare` wave `c2-speed` with every server in an identically limited container (2 CPUs, 6 GB), clients pinned to the
  other cores: run id in the next commit. Run 40481152975 (same wave, dispatched before the container rule) is kept only
  as a no-container reference. Earlier `c1-servers` runs were superseded and cancelled (40478832460 cancelled 09:33 UTC).

## Latest server comparison: [c3-load-40482405265](results/c3-load-40482405265/summary.md)

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

### Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| new-vs-27f5-def-load-local | ours-new `-` | ours-27f5 `-` | local | Linux ubuntu24 4 vCPU Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz | 0/0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| new-vs-27f5-def-mix-local | ours-new `-` | ours-27f5 `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 0/0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| new-vs-27f5-t8-load-local | ours-new `-DduckDbThreads=8` | ours-27f5 `-DduckDbThreads=8` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 0/0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| new-vs-27f5-t8-mix-local | ours-new `-DduckDbThreads=8` | ours-27f5 `-DduckDbThreads=8` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 0/0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| new-vs-main-def-load-local | ours-new `-` | up-main `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 0/0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| new-vs-main-def-mix-local | ours-new `-` | up-main `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 0/0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| new-vs-main-t8-load-local | ours-new `-DduckDbThreads=8` | up-main `-DduckDbThreads=8` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 0/0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| new-vs-main-t8-mix-local | ours-new `-DduckDbThreads=8` | up-main `-DduckDbThreads=8` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 0/0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| new-vs-native-def-load-local | ours-new `-` | up-native `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 0/0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| new-vs-native-def-mix-local | ours-new `-` | up-native `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 0/0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| new-vs-native-t8-load-local | ours-new `-DduckDbThreads=8` | up-native `-DduckDbThreads=8` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 0/0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| new-vs-native-t8-mix-local | ours-new `-DduckDbThreads=8` | up-native `-DduckDbThreads=8` | local | Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor | 0/0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |

### Per job (absolute medians and ratios)

#### new-vs-27f5-def-load-local: A = ours-new `-`, B = ours-27f5 `-`, local

Runner: Linux ubuntu24 4 vCPU Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|

#### new-vs-27f5-def-mix-local: A = ours-new `-`, B = ours-27f5 `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `mixed heavy4a netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|

#### new-vs-27f5-t8-load-local: A = ours-new `-DduckDbThreads=8`, B = ours-27f5 `-DduckDbThreads=8`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|

#### new-vs-27f5-t8-mix-local: A = ours-new `-DduckDbThreads=8`, B = ours-27f5 `-DduckDbThreads=8`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `mixed heavy4a netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|

#### new-vs-main-def-load-local: A = ours-new `-`, B = up-main `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|

#### new-vs-main-def-mix-local: A = ours-new `-`, B = up-main `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `mixed heavy4a netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|

#### new-vs-main-t8-load-local: A = ours-new `-DduckDbThreads=8`, B = up-main `-DduckDbThreads=8`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|

#### new-vs-main-t8-mix-local: A = ours-new `-DduckDbThreads=8`, B = up-main `-DduckDbThreads=8`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `mixed heavy4a netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|

#### new-vs-native-def-load-local: A = ours-new `-`, B = up-native `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|

#### new-vs-native-def-mix-local: A = ours-new `-`, B = up-native `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `mixed heavy4a netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|

#### new-vs-native-t8-load-local: A = ours-new `-DduckDbThreads=8`, B = up-native `-DduckDbThreads=8`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|

#### new-vs-native-t8-mix-local: A = ours-new `-DduckDbThreads=8`, B = up-native `-DduckDbThreads=8`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `mixed heavy4a netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|

## Results

- [c3-load-40482405265](results/c3-load-40482405265/summary.md) (latest of its wave)
- [c2-speed-40481883941](results/c2-speed-40481883941/summary.md) (latest of its wave)
- [w3-combos-c3b2-40232144198](results/w3-combos-c3b2-40232144198/summary.md) (latest of its wave)
- [w2-s3-and-layout-40211085777](results/w2-s3-and-layout-40211085777/summary.md) (latest of its wave)
- [w1-knobs-local-40211079235](results/w1-knobs-local-40211079235/summary.md) (latest of its wave)
- [w0-smoke-40210310231](results/w0-smoke-40210310231/summary.md) (latest of its wave)
