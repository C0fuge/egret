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

EGRET FINAL DONE 2026-10-29 (final build `1e7b43a4e0c7`: [results/FINAL-1e7b43a4e0c7.md](results/FINAL-1e7b43a4e0c7.md); no further builds).

EGRET ITEM 23 DONE 2026-10-30 (build `d752a7358a65`, `-DresourceProfile=speed` vs balanced vs upstream native, run 41029626461: [results/ITEM23-d752a7358a65.md](results/ITEM23-d752a7358a65.md); BUILDS.md row added). Speed is faster where correct (load +11-22 %, scan x8 +36-43 %, small p50 at 8/32 clients 37-50 % lower; near upstream native on load 0.90-0.96 and above it on local scans at 24 % of its RSS) but **fails the correctness gate on S3 small queries at 32 clients in all 3 rounds** (ADBC 702-753, JDBC 66-91 of 1280 errors; balanced 0) and has S3 c8 p95 1.42-1.44. Nothing running. Next: none until a newer pre-release with a fix for the speed-profile S3 c32 errors; then re-run `i23-small` on S3 + local.

ITEM 23b (`ci/BUILD-TRACK-TASK.md` "ITEM 23b"): build `843e4ad5b610` (STATUS: item 23b done, shared DuckDB node-wide budget for cached prepared statements; contains `eb1f15d`). Wave `track-843e4ad5b610` (3 three-way jobs: i23b-small S3 + local, i23b-load local; A = 843e balanced, B = 843e `-DresourceProfile=speed`, C = upstream native `9fb08d9dd24d`; 3 rounds). Run **41082368785** (dispatched 2026-10-30 15:37 UTC). Next: when green, write `results/ITEM23b-843e4ad5b610.md` (errors per concurrency, speed must have 0 at S3 c32; speed/balanced, speed/upstream, peak RSS), BUILDS.md row, then "EGRET ITEM 23b DONE".

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
  - Phase B (`ci/BUILD-TRACK-TASK.md`): tracked builds in [`results/BUILDS.md`](results/BUILDS.md).
    - Build 1 `d22cdaccb4e1` (item 20 (b) LZ4 + ZSTD streams; contains item 19, 17 (b)-(d), Iceberg): **done**,
      [`results/track-d22cdaccb4e1/summary.md`](results/track-d22cdaccb4e1/summary.md) (runs 40602868592 + 40621069419).
      Better (slow-link export CLZ4 2.51x, CZSTD 3.46x; scan x8 +10-15 %; 22/22 everywhere), but **regression: S3 small
      queries p95 at 8/32 clients 12-21 % slower in all 3 rounds (JDBC c32 p95 1.21; p50 faster); local not affected.**
    - Build 2 `4bb6441569be` (S3 duckDbThreads default >= 4, aimed at the build-1 S3 p95 regression; contains
      `881b7c62b373` item 21 step 1, `e9f0fd3` item 22 step 1 (opt-in); skipped as contained: `ba4139a2eb93` item 20 (c),
      `cadd1aca9c23` item 20 (f), `3fbf5b28b186` / `1f600b930eda` plugins/test only): **done**,
      [`results/track-4bb6441569be/summary.md`](results/track-4bb6441569be/summary.md) (run 40638050743, 9/9 jobs green).
      Better: build-1 S3 p95 regression gone (S3 c32 p95 0.99-1.03 of baseline), load +5-6 % at peak and +15-19 % at
      128 clients (still 0.76x upstream native), local small p50 c8/c32 20-26 % faster, 22/22 everywhere.
      **Small regression: local ADBC c8 p95 1.07 / p99 1.15 in all 3 rounds (p50 0.75); JDBC and c32 not affected.**
    - Build 3 `e70d80bb7995` (contains `9506620bb170` item 22 (c) opt-in `duckDbProducingStreams`,
      `99113c98c1c3` item 17 (e) S3 cache memory + opt-in `cacheAdmission=reuse`, `7f308a6cdb4d` item 22 (d) opt-in
      `flightZeroCopyWrites`; skipped as contained: those three and `36b2177d51b4` (plugins only); `e70d80bb7995` itself adds
      auth-provider groups for Ranger, no change for built-in providers): **done**,
      [`results/track-e70d80bb7995/summary.md`](results/track-e70d80bb7995/summary.md) (run 40664667021, 13/13 jobs green).
      Better: local small p50 13-26 % faster, scan x8 +22 %, opt-in zero-copy writes scans +4-7 % (on par with upstream
      native at a third of its RSS), cache-on peak RSS -8 % vs `4e77c6bda59a` at equal speed, 22/22 everywhere; build-2
      local ADBC c8 tail not seen (p95 0.94). **Flag: S3 small ADBC c1 p50 1.25 (rounds 1.31 1.18 1.36) in a noisy job;
      re-check in the next build's S3 core job.**
    - Build 4 `94ad61021d93` (contains `a9e43ca5e296` item 19b step 1 DuckDB threads + memory limit by host size,
      `fd9f62f` item 19b step 2 opt-in `duckDbThreadsWhenIdle`, `ffcbabf`/`c7e436e` item 18 step 3 off-vs-on counters and
      backup fail-over, `ea55a4f` item 17 (a) opt-in S3 cache disk tier; skipped as contained: `a9e43ca5e296`,
      `177dfe3e5716`, `f73de96b8773`, `c258adf27dc9`, `1b3a7bbad4bc`): **done**,
      [`results/track-94ad61021d93/summary.md`](results/track-94ad61021d93/summary.md) (run 40699820075, 8/9 green;
      load + cluster tables via re-report 40728485498). Better: load +6-7 % at peak and +18-23 % at 128 clients,
      local small p50 c8/c32 19-26 % faster, scan x8 +18 %, sized DuckDB memory -12 % peak RSS for 2-3 % SF10, 22/22
      everywhere incl. the 3-node cluster with node loss (dc on and off; on not faster). Local SF10 1.02-1.04 (under the
      rule). **Small regression: S3 small ADBC c1 p95 1.08 / p99 1.09 in all 3 rounds (JDBC, c8/c32 not affected); the
      build-3 S3 ADBC c1 p50 flag is not confirmed (1.14, rounds 1.61 1.14 0.80).**
      The `i18-dc-off-vs-on` job hit the 170-min job limit in round 3 (cluster side-round 28-45 min): only 2 rounds.
      For the next item-18 build: give the cluster job its own wave with `rounds=2`, or split the 5 checks over two jobs.
    - Build 5 `2cfa23eb62f9` (contains `eb82020` item 18 / D2 (c) part 1 two-process distributed complete with TLS +
      token auth, opt-in `dataDirShared`; `3042102` item 13 (c) external file cache bound line; `411e804` item 3 (c)
      Iceberg time travel; Hive Avro plugin; still has the 19b thread defaults, the fix `9efe670` is not released yet):
      **done**, [`results/track-2cfa23eb62f9/summary.md`](results/track-2cfa23eb62f9/summary.md) (core 40736482953,
      6/6 green; cluster 40736487295, `rounds=2` in its own wave, green). Better locally (small p50 c8/c32 22-28 %
      faster, scan x8 +15 %), 22/22 everywhere incl. the 3-node cluster with node loss (dc on and off; on still not
      faster, slower recovery 104-109 s vs 62-98 s). **Small regression: S3 TPC-H SF1 JDBC total 1.14 in all 3 rounds
      (1.21 1.05 1.14; warm medians only, cold sums and ADBC not affected).** Local SF10 1.07-1.10 (under the rule,
      up from 1.02-1.04 in build 4). Build-4 S3 ADBC c1 p95 flag not seen (1.01).
    - Build 6 `9044653333cd` (contains `936b2d7` item 21 `duckDbThreadsUnderLoad` fix, `a110a22` / `aef0a7a` /
      `9044653` item 18 D3 steps 1-2b (no wait for a crashed cluster member), `9efe670` 19b thread floor 4, Hive views,
      Iceberg time travel via Hive; skipped as contained: `a110a2279437`, `0f8eb5e5f65c` (catalog CI probe only),
      `936b2d7c366c`): **done**, [`results/track-9044653333cd/summary.md`](results/track-9044653333cd/summary.md)
      (core 40772221252, 8/8 green; cluster 40772225000, `rounds=2`, green). 22/22 everywhere incl. the 3-node cluster
      with node loss (dc on and off; on level with off when all up, 1.03, recovery 90-96 s vs 104-109 s in build 5,
      still not faster). Local SF10 back to 1.04, build-5 S3 SF1 JDBC flag gone (0.97). **Small regression: S3 TPC-H
      SF10 ADBC total 1.10 in all 3 rounds (1.06 1.10 1.21); S3 SF10 JDBC 0.97.** Item 21 load level with the
      baseline (the +5-7 % peak gain of builds 2/4 is not seen); 19b sized memory no longer lowers peak RSS (1.03).
    - Build 7 `881bbf73e946` (item 22 shared DuckDB step (c) `duckDbStreamingBufferSize` in shared mode; contains
      `e75119218df7` item 22 (a) one describe DuckDB per node, `80aa61a15557` D3 step 3 local-disk plans + item 22 step 1
      opt-in `duckDbSharedDatabase`, Hive P4 (d), opt-in `plainFlightCommands` (P5), Hive insert-only tables (C4);
      skipped as contained: `e75119218df7`, `80aa61a15557`): **done**,
      [`results/track-881bbf73e946/summary.md`](results/track-881bbf73e946/summary.md) (core 40800578035, 11/11 green;
      cluster 40800581040, `rounds=2`, green). 22/22 everywhere incl. the 3-node cluster with node loss (dc on level with
      off all-up, 1.01; still not faster after node changes, recovery 96 s). Build-6 S3 SF10 ADBC flag gone (0.96).
      Opt-in shared DuckDB: scans x8 +39 % / x4 +15 % in every round, load +16 % at the peak and +37-41 % at 128
      clients with 14 % less RSS under load, upstream native's scan speed at 38 % of its RSS (+17-19 % RSS on scans /
      SF10). Item 21 load level with the baseline. **Small regression: S3 small JDBC c8 p50 1.10 in all 3 rounds
      (1.07 1.11 1.10; p95 0.94); re-check in the next build's S3 latency job.**
    - Build 8 `06833e736572` (contains `fd6084f` item 18 D6: peer lost after the first batch of a distributed complete
      answer fails as UNAVAILABLE; Ranger Hive policies P6 steps 1-3a (custom auth providers only), C4 step 3 Hive
      insert-only tables through the server; skipped as contained: `01884e287668`): **done**,
      [`results/track-06833e736572/summary.md`](results/track-06833e736572/summary.md) (core 40823526868, 6/6 green;
      cluster 40823529991, `rounds=2`, green). Same: default path level with the baseline, 22/22 everywhere incl. the
      3-node cluster with node loss (dc on and off), no regression by the rule, peak RSS 0.88-1.01. Build-7 S3 JDBC c8
      p50 flag not confirmed (1.04). Local SF10 ADBC 1.06 (rounds 1.03 1.06 1.07, under the rule; watch). Cluster: dc on
      1.06 of off all-up, 1.54-1.61 after node changes, recovery 90-103 s vs 59 s; still not faster.
    - Build 9 `b3bbcce19996` (contains `16edbb7` item 18 D9 node-load leak fix under concurrent identical queries,
      `d4a136f` D11 `shutdownDrainSeconds` default 20 s, `ab8cc3d` D10 distributed complete merges plain `avg`,
      `b3bbcce` subquery/CTE/UNION tables checked under authorization providers (no change without a provider),
      `786782219b1a` LZ4 codec module for Java Flight clients (separate jar, our clients do not load it: no slow-link
      pair); skipped as contained: `85a790826156`, `7b988c720821`, `2a2b8e08191f`, `786782219b1a`): **done**,
      [`results/track-b3bbcce19996/summary.md`](results/track-b3bbcce19996/summary.md) (core 40849716676, 6/6 green;
      cluster 40849719732, `rounds=2`, green). Same: default path level with the baseline, 22/22 everywhere incl. the
      3-node cluster with node loss (dc on and off), no regression by the rule, peak RSS 0.90-1.05. Build-8 local SF10
      ADBC watch back to 1.03. Watch: local small JDBC c8 p95 / p99 1.07 / 1.10 (p95 rounds 1.09 1.09 1.03, p50 0.93).
      Cluster: dc on 1.04 of off all-up, 1.23-1.37 after node changes, recovery 91-104 s vs 59-93 s; still not faster.
    - FINAL build `1e7b43a4e0c7` (finish mode; `ci/BUILD-TRACK-TASK.md` "FINAL"): **done**,
      [`results/FINAL-1e7b43a4e0c7.md`](results/FINAL-1e7b43a4e0c7.md) (run 40876778493, three-way on one runner per job:
      `7562a5bdb7b9` / final / upstream native `9fb08d9dd24d`, 8/8 jobs green). Vs baseline: same on the default path,
      no regression by the rule (closest local SF10 ADBC 1.04, S3 small ADBC c1 p50 1.08, neither in all rounds), 22/22
      everywhere, peak RSS 0.88-1.02, slow-link export with client ZSTD 2.40x (104 -> 250 MB/s). Vs upstream native:
      upstream 0-1/22 on TPC-H, small-query errors and a server death, 8-stream scan error; where it answers it scans
      20-25 % faster at 4 streams at 2-3x our RSS, single stream and slow link with ZSTD level (0.93-0.97).
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

- [track-d752a7358a65-41029626461](results/track-d752a7358a65-41029626461/summary.md) (latest of its wave)
- [track-1e7b43a4e0c7-40876778493](results/track-1e7b43a4e0c7-40876778493/summary.md) (latest of its wave)
- [track-b3bbcce19996-cluster-40849719732](results/track-b3bbcce19996-cluster-40849719732/summary.md) (latest of its wave)
- [track-b3bbcce19996-40849716676](results/track-b3bbcce19996-40849716676/summary.md) (latest of its wave)
- [track-06833e736572-cluster-40823529991](results/track-06833e736572-cluster-40823529991/summary.md) (latest of its wave)
- [track-06833e736572-40823526868](results/track-06833e736572-40823526868/summary.md) (latest of its wave)
- [track-881bbf73e946-cluster-40800581040](results/track-881bbf73e946-cluster-40800581040/summary.md) (latest of its wave)
- [track-881bbf73e946-40800578035](results/track-881bbf73e946-40800578035/summary.md) (latest of its wave)
- [track-9044653333cd-cluster-40772225000](results/track-9044653333cd-cluster-40772225000/summary.md) (latest of its wave)
- [track-9044653333cd-40772221252](results/track-9044653333cd-40772221252/summary.md) (latest of its wave)
- [track-2cfa23eb62f9-cluster-40736487295](results/track-2cfa23eb62f9-cluster-40736487295/summary.md) (latest of its wave)
- [track-2cfa23eb62f9-40736482953](results/track-2cfa23eb62f9-40736482953/summary.md) (latest of its wave)
- [track-94ad61021d93-40699820075](results/track-94ad61021d93-40699820075/summary.md) (latest of its wave)
- [track-e70d80bb7995-40664667021](results/track-e70d80bb7995-40664667021/summary.md) (latest of its wave)
- [track-load-4bb6441569be-40638050743](results/track-load-4bb6441569be-40638050743/summary.md) (latest of its wave)
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
- [track-881bbf73e946](results/track-881bbf73e946/summary.md) (latest of its wave)
- [track-06833e736572](results/track-06833e736572/summary.md)
- [track-94ad61021d93](results/track-94ad61021d93/summary.md)
- [track-4bb6441569be](results/track-4bb6441569be/summary.md)
- [track-b3bbcce19996](results/track-b3bbcce19996/summary.md)
- [track-d22cdaccb4e1](results/track-d22cdaccb4e1/summary.md)
- [track-2cfa23eb62f9](results/track-2cfa23eb62f9/summary.md)
- [track-e70d80bb7995](results/track-e70d80bb7995/summary.md)
- [track-9044653333cd](results/track-9044653333cd/summary.md)
