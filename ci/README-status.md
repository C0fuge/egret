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
  - Phase B (`ci/BUILD-TRACK-TASK.md`): tracked builds in [`results/BUILDS.md`](results/BUILDS.md).
    - Build 1 `d22cdaccb4e1` (item 20 (b) LZ4 + ZSTD streams; contains item 19, 17 (b)-(d), Iceberg): **done**,
      [`results/track-d22cdaccb4e1/summary.md`](results/track-d22cdaccb4e1/summary.md) (runs 40602868592 + 40621069419).
      Better (slow-link export CLZ4 2.51x, CZSTD 3.46x; scan x8 +10-15 %; 22/22 everywhere), but **regression: S3 small
      queries p95 at 8/32 clients 12-21 % slower in all 3 rounds (JDBC c32 p95 1.21; p50 faster); local not affected.**
    - Build 2 `4bb6441569be` (S3 duckDbThreads default >= 4, aimed at the build-1 S3 p95 regression; contains
      `881b7c62b373` item 21 step 1, `e9f0fd3` item 22 step 1 (opt-in); skipped as contained: `ba4139a2eb93` item 20 (c),
      `cadd1aca9c23` item 20 (f), `3fbf5b28b186` / `1f600b930eda` plugins/test only): **running** compare run 40638050743,
      wave `track-load-4bb6441569be` (core local + S3 split, item 21 load 1-128 vs baseline and vs up-native, S3 small vs
      `d22cdaccb4e1`). Next step: when it finishes, write `results/track-4bb6441569be/summary.md` + BUILDS.md row
      (check whether the S3 c8/c32 p95 regression is gone), fix/re-run failed jobs with `only=`.
    Note: the aggregate job rebuilds README from `ci/README-status.md`: edit 'In progress' THERE, not only in README.
  - `results/c2-speed-40481152975` is only a "no-container reference". `ci/ignored-runs.txt` blocks the aggregates of
    40483119136 (wrong `ours-new`), 40478832460 (old `c1-servers`) and 40539031628 (diagnostic).
