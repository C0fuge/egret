# FINAL build `1e7b43a4e0c7` vs baseline `7562a5bdb7b9` vs upstream native

Task: `ci/BUILD-TRACK-TASK.md` "FINAL". Build `server-1.0.0-1e7b43a4e0c7` (finish mode; contains every item since
`7562a5bdb7b9`). Run 40876778493 (wave `track-1e7b43a4e0c7`, 8 three-way jobs + aggregate, all green; the earlier
attempt 40875293905 failed at Assets before measuring). Full tables: [run summary](track-1e7b43a4e0c7-40876778493/summary.md),
[speed](track-1e7b43a4e0c7-40876778493/speed.md), [load / slow link](track-1e7b43a4e0c7-40876778493/load.md).

## Key builds (copied from [BUILDS.md](BUILDS.md))

- `d22cdaccb4e1` (item 20 LZ4/ZSTD Flight streams): on a 1 Gbit/s 10 ms link, the full lineitem export over ADBC rises from 104 MB/s
  to 261 MB/s (LZ4, 2.5x) or 361 MB/s (ZSTD, 3.5x) when the client asks for compression, matching or beating upstream's
  native ZSTD (256-260 MB/s); scan with 8 streams +10-15 %.
- `4bb6441569be` (S3 threads default, item 21 step 1): removes the S3 small-query tail regression of `d22cdaccb4e1`;
  closed-loop load +5-6 % at the peak and +15-19 % at 128 clients (35 -> 40 q/s), local small-query p50 at 8/32 clients
  20-26 % faster. Still ~0.76x of upstream native's load throughput.
- `e70d80bb7995` (item 22 (c)/(d), item 17 (e)): opt-in `flightZeroCopyWrites` scans +4-7 % and on par with upstream
  native (equal at 4 streams, 854 MB/s at 8, a third of native's RSS); S3 cache-on peak RSS -8 % at equal speed;
  local small-query p50 13-26 % faster, scan 8 streams +22 % vs baseline.
- `94ad61021d93` (item 19b threads + memory by host size, item 18 step 3): closed-loop load +6-7 % at the peak and
  +18-23 % at 128 clients (48 -> 59 q/s JDBC), sized DuckDB memory cuts peak RSS 12 % for a 2-3 % SF10 cost; 3-node
  cluster answers 22/22 with a node stopped or killed mid-query in both `distributedComplete` modes (on is not faster).
- `881bbf73e946` (item 22 shared DuckDB, opt-in `duckDbSharedDatabase=true`): scans with 8 streams +39 % and 4 streams
  +15 % in every round, closed-loop load +16 % at the peak and +37-41 % at 128 clients (35 -> 48 q/s) with 14 % less
  RSS under load; reaches upstream native's scan speed (x4 0.98, x1 1.04, ~900 MB/s at 8) at 38 % of its RSS.

## Setup

- Three servers per job on one runner: A = `7562a5bdb7b9`, B = final `1e7b43a4e0c7`, C = upstream native
  `9fb08d9dd24d` (the upstream build of Reports 1-3); rounds A B C / C B A / A B C. Containers as `COMPARE-TASK.md`
  (2 CPUs pinned, 6 GB, `-Xmx3g`, direct 2g; clients and S3 on the other cores). Default settings on all servers
  (opt-ins such as `duckDbSharedDatabase` and `flightZeroCopyWrites` off), except the slow link: final with client-side
  ZSTD (`CZSTD`), baseline plain (it has no Flight compression), upstream native with `-DflightCompression=zstd`.
- Ratios are medians over 3 rounds: times < 1 = final faster, MB/s > 1 = final faster. "final/7562" and
  "final/upstream" columns; **n/a** = upstream failed that workload's correctness gate (never ranked).

## Correctness

| workload | final | 7562 | upstream native |
|---|---|---|---|
| TPC-H SF1 + SF10, ADBC + JDBC, local | 22/22 every round | 22/22 every round | ADBC 0/22 (every query fails), JDBC 1/22 |
| TPC-H SF1 + SF10, ADBC + JDBC, S3 | 22/22 every round | 22/22 every round | ADBC 0/22, JDBC 1/22 |
| TPC-H SF10 ADBC over the slow link | 22/22 | 22/22 | 0/22 |
| small queries (8 classes), local + S3, 1/8/32 clients | 0 errors, answers equal | 0 errors, answers equal | JDBC c1 20/160 errors; c8/c32 mostly or all errors; server died after the small set |
| lineitem scans 1/4/8 streams, export | all rows | all rows | x8 one stream error (local and S3); x1, x4, export ok |

Same picture as Report 1 for upstream (multi-table prepare rejected, DECIMAL vs float64); our two builds never failed
an answer and were never OOM-killed.

## TPC-H (sum of warm medians, s)

| storage / protocol | 7562 | final | final/7562 | per-round | final/upstream |
|---|---|---|---|---|---|
| local SF1 ADBC | 3.3 | 3.3 | 0.99 | 0.99 0.98 1.00 | n/a |
| local SF1 JDBC | 3.4 | 3.4 | 0.99 | 0.97 0.99 1.00 | n/a |
| local SF10 ADBC | 33.7 | 35.1 | 1.04 | 1.07 1.06 1.03 | n/a |
| local SF10 JDBC | 33.7 | 34.2 | 1.02 | 1.02 1.02 1.00 | n/a |
| S3 SF1 ADBC | 26.3 | 26.4 | 1.00 | 1.01 1.03 0.98 | n/a |
| S3 SF1 JDBC | 25.7 | 25.9 | 1.01 | 1.01 0.99 1.01 | n/a |
| S3 SF10 ADBC | 455.2 | 297.1 | 0.65 (noisy: one slow baseline round; level otherwise) | 1.01 0.65 1.02 | n/a |
| S3 SF10 JDBC | 256.9 | 260.6 | 1.01 | 1.01 1.05 1.06 | n/a |

## Small queries (ms; 8 point / count / limit / metadata classes)

| metric | local 7562 | local final | local final/7562 | S3 7562 | S3 final | S3 final/7562 (rounds) | final/upstream |
|---|---|---|---|---|---|---|---|
| ADBC c1 p50 | 17.6 | 17.6 | 1.00 | 24.6 | 26.7 | 1.08 (1.17 0.99 1.09) | n/a |
| ADBC c8 p95 | 282.9 | 281.6 | 1.00 | 5574.9 | 5730.8 | 1.03 (1.16 0.97 1.03) | n/a |
| ADBC c32 p95 | 1339.6 | 1328.6 | 0.99 | 18079.9 | 17979.3 | 0.99 (1.02 0.99 1.54) | n/a |
| ADBC c32 p99 | 1858.4 | 1822.8 | 0.98 | 21232.2 | 24504.0 | 1.15 (1.00 1.15 1.27) | n/a |
| JDBC c1 p50 | 26.4 | 26.4 | 1.00 | 38.8 | 40.3 | 1.04 (1.23 1.02 1.05) | n/a |
| JDBC c8 p50 | 127.2 | 124.1 | 0.98 | 306.0 | 334.1 | 1.09 (0.98 0.98 1.17) | n/a |
| JDBC c32 p95 | 1395.0 | 1358.5 | 0.97 | 17232.4 | 18287.4 | 1.06 (1.03 1.01 1.44) | n/a |
| JDBC c32 p99 | 2051.6 | 1916.6 | 0.93 | 20306.4 | 22398.4 | 1.10 (0.94 1.02 1.32) | n/a |

Local: every step 0.93-1.02 except ADBC c1 p99 1.10 (rounds 0.98 1.23 1.10). S3: round 3 was slow for the final build
at c32 (1.23-1.62 on every c32 metric); no S3 metric is > 5 % slower in all 3 rounds. Upstream: n/a (errors at every
concurrency, see Correctness).

## Scans and export (MB/s, lineitem SF10)

| metric | 7562 | final | final/7562 (rounds) | upstream | final/upstream (rounds) |
|---|---|---|---|---|---|
| local scan x1 | 416.1 | 408.4 | 0.98 (0.92 1.03 1.00) | 419.4 | 0.97 (1.02 0.92 0.98) |
| local scan x4 | 446.9 | 450.7 | 1.01 (0.99 1.06 1.02) | 565.1 | 0.80 (0.84 0.83 0.78) |
| local scan x8 | 414.3 | 416.5 | 1.01 (0.99 1.02 1.03) | error | n/a |
| local export ADBC | 513.9 | 449.5 | 0.87 (0.82 1.01 1.05) | 544.2 | 0.83 (0.81 0.96 0.83) |
| S3 scan x1 | 535.7 | 481.2 | 0.90 (1.03 0.88 0.90) | 515.0 | 0.93 (1.07 0.92 0.85) |
| S3 scan x4 | 634.8 | 616.2 | 0.97 (0.90 1.01 1.00) | 825.3 | 0.75 (0.73 0.75 0.74) |
| S3 scan x8 | 588.9 | 610.2 | 1.04 (0.92 1.05 1.07) | error | n/a |
| S3 export ADBC | 620.8 | 615.1 | 0.99 (0.97 1.00 0.97) | 778.5 | 0.79 (0.85 0.80 0.71) |

With default settings the final build scans like the baseline; the +15-22 % scan x8 of builds 1-4 is not seen any more
(builds 6-9 were also 0.99-1.02). Upstream native stays 20-25 % faster at 4 streams at 2-3x the RSS. The opt-in shared
DuckDB (`881bbf73e946`: ~upstream scan speed at 38 % of its RSS) was not part of this default-settings run.

## Slow link (netem 10 ms RTT, 1 Gbit/s, local SF10)

| metric | 7562 plain | final CZSTD | final/7562 (rounds) | upstream ZSTD | final/upstream (rounds) |
|---|---|---|---|---|---|
| lineitem export ADBC, MB/s | 104 | 250 | **2.40** (2.54 2.40 2.37) | 260 | 0.96 (1.03 0.96 0.95) |
| TPC-H SF10 ADBC, s | 40.6 (22/22) | 42.6 (22/22) | 1.05 | n/a (0/22) | n/a |

## Peak RSS (MB, median over rounds)

| job | 7562 | final | final/7562 | upstream | final/upstream |
|---|---|---|---|---|---|
| local TPC-H SF1 + SF10 | 1710 | 1610 | 0.94 | 362 (all TPC-H failed) | n/a |
| local small + scans | 1720 | 1717 | 1.00 | 3638 | 0.47 |
| S3 SF1 | 728 | 742 | 1.02 | 576 (failed) | n/a |
| S3 SF10 ADBC | 1727 | 1572 | 0.91 | 1022 (failed) | n/a |
| S3 SF10 JDBC | 1769 | 1598 | 0.90 | 1013 (failed) | n/a |
| S3 small | 2175 | 2117 | 0.97 | 393 (died) | n/a |
| S3 scans | 1762 | 1728 | 0.98 | 5806 | 0.30 |
| slow link | 1686 | 1478 | 0.88 | 597 (TPC-H failed) | n/a |

Upstream RSS is only comparable where it answered (scans): there the final build uses 30-47 % of upstream's memory.

## Verdict

- **vs baseline `7562a5bdb7b9`: same on the default path, better on the slow link, no regression.** No core metric is
  > 5 % slower in all 3 rounds (closest: local SF10 ADBC 1.04, rounds 1.07 1.06 1.03; S3 small ADBC c1 p50 1.08,
  rounds 1.17 0.99 1.09). 22/22 everywhere, peak RSS 0.88-1.02. Client-requested ZSTD lifts the slow-link export
  2.40x (104 -> 250 MB/s). The gains of builds 2-4 on local small-query p50 and scan x8 are not visible in this run
  (level with the baseline); the larger gains of the opt-ins (`duckDbSharedDatabase`, `flightZeroCopyWrites`, S3 cache)
  stay as measured in their builds above.
- **vs upstream native `9fb08d9dd24d`: correct where upstream is not**, at 30-47 % of its memory on scans. Upstream fails
  every TPC-H query over ADBC and 21/22 over JDBC, errors on small queries from 1 client and dies under concurrency,
  and fails 8-stream scans. Where both answer, upstream is faster on parallel scans (final 0.75-0.80 at 4 streams,
  0.79-0.83 on export) and level on single-stream scans (0.93-0.97) and the slow link with ZSTD (0.96).
