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
    small queries. Still running at 21:07 UTC (4 ab jobs in progress after 1 h 38 min, job timeout 170 min;
    if a job times out, rerun it alone with `only=<job id>` and fewer workloads, e.g. without `adbc1`). When it finishes: check for failures, write a short `results/COMPARE-CACHE-2026-10-27.md` (cache on/off
    ratios, new builds vs ours-new), link it here, then write `ALL DONE <date>` at the top of this section.
  - `results/c2-speed-40481152975` is only a "no-container reference". `ci/ignored-runs.txt` blocks the aggregates of
    40483119136 (wrong `ours-new`), 40478832460 (old `c1-servers`) and 40539031628 (diagnostic).
