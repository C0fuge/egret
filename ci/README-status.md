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
    - FINAL build `1e7b43a4e0c7` (finish mode; `ci/BUILD-TRACK-TASK.md` "FINAL"): **running**, wave
      `track-1e7b43a4e0c7`, three-way on one runner per job (side A `7562a5bdb7b9`, B final, C upstream native; rounds
      A B C / C B A / A B C): core local + S3 (S3 latency split into small / scan jobs for the 170-min limit) and the
      slow link with ZSTD (final CZSTD vs baseline plain vs native ZSTD). Run 40875293905 (upstream native pinned to Report 1's `9fb08d9dd24d`).
    - Next step (next session): when the run is done, write `results/FINAL-1e7b43a4e0c7.md` (Key builds list at the
      top, one table per area with final/7562 and final/upstream ratios, correctness, peak RSS, verdict), add the
      BUILDS.md row, then write "EGRET FINAL DONE" here and stop; no further builds.
    Note: the aggregate job rebuilds README from `ci/README-status.md`: edit 'In progress' THERE, not only in README.
  - `results/c2-speed-40481152975` is only a "no-container reference". `ci/ignored-runs.txt` blocks the aggregates of
    40483119136 (wrong `ours-new`), 40478832460 (old `c1-servers`) and 40539031628 (diagnostic).
