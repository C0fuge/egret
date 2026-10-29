# Build tracking: `881bbf73e946` vs baseline `7562a5bdb7b9`

- Build: `server-1.0.0-881bbf73e946` (item 22 shared DuckDB step (c): `duckDbStreamingBufferSize` in shared mode;
  contains `e75119218df7` item 22 (a) one describe DuckDB per node, `80aa61a15557` item 18 D3 step 3 local-disk plans +
  item 22 step 1 opt-in `duckDbSharedDatabase`, Hive P4 (d), opt-in `plainFlightCommands` (P5), Hive insert-only
  tables (C4)). Skipped as contained: `e75119218df7`, `80aa61a15557`.
- Runs: core compare 40800578035 (wave `track-881bbf73e946`, 11 jobs: core, item 22 shared DuckDB off vs on for scans,
  SF10 and load, shared vs upstream native, item-21 load; 3 rounds, all green); item-18 cluster compare 40800581040
  (wave `track-881bbf73e946-cluster`, `distributedComplete` off vs on, `rounds=2` in its own wave). Full core tables:
  [run summary](../track-881bbf73e946-40800578035/summary.md), [speed](../track-881bbf73e946-40800578035/speed.md),
  [load](../track-881bbf73e946-40800578035/load.md).
- Pairs: A = baseline (or the named reference), B = candidate, same runner, 3 rounds (A B, B A, A B), containers as
  `COMPARE-TASK.md`. Ratio = B / A of the medians; times < 1 = candidate faster, MB/s and q/s > 1 = candidate faster.
- Correctness: TPC-H SF1 + SF10, ADBC + JDBC, local + S3: 22/22 for both sides in every round, no candidate job
  disqualified, no OOM, also with `duckDbSharedDatabase=true` (SF10 ADBC + JDBC). Only upstream native failed a gate
  (scan with 8 streams, 2 errors, in `i22-shared-vs-native`); it is the reference there, not a tracked build.

## Regression check (rule: > 5 % slower on a core metric in all 3 rounds)

- **S3 small JDBC c8 p50 1.10 (rounds 1.07 1.11 1.10; 244.5 -> 268.2 ms).** The tail at the same step is faster
  (p95 0.94, p99 0.95) and ADBC c8 p50 is 1.12 but not in all rounds (1.03 0.99 1.12). Build 6 had S3 ADBC c8 p50 1.09
  (1.21 1.00 1.22) in the same job, also not in all rounds, so this is a recurring small S3 c8 median point rather than
  new in this build. Local c8 not affected (JDBC p50 0.99, ADBC 0.93). Small; re-check in the next build.
- The build-6 flag **S3 TPC-H SF10 ADBC 1.10 is gone**: 0.96 (1.03 0.83 0.94). S3 SF10 JDBC 0.83 (1.03 0.83 0.92), a
  slow baseline round 2, so not a clear gain either.
- Local TPC-H SF10 ADBC 1.04 (1.04 1.01 1.05), JDBC 1.03 (1.04 0.99 1.03): level with build 6, under the rule.
- S3 small ADBC c1 p99 1.38 (1.28 0.92 1.41) and JDBC c32 p99 1.15 (1.63 1.10 0.93): not in all rounds (p99 of a noisy
  S3 job), p50 and p95 at those steps 0.96-1.01.

## Core (default settings)

| metric | storage | A (baseline) | B (candidate) | B / A | per round |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC total s | local | 39.5 | 41.0 | 1.04 | 1.04 1.01 1.05 |
| TPC-H SF10 JDBC total s | local | 39.6 | 40.7 | 1.03 | 1.04 0.99 1.03 |
| TPC-H SF1 ADBC total s | local | 4.1 | 4.0 | 0.97 | 0.96 0.99 1.00 |
| TPC-H SF1 JDBC total s | local | 4.1 | 4.1 | 1.00 | 0.97 0.99 1.02 |
| TPC-H SF10 ADBC total s | S3 | 275.9 | 263.6 | 0.96 | 1.03 0.83 0.94 |
| TPC-H SF10 JDBC total s | S3 | 317.8 | 265.1 | 0.83 | 1.03 0.83 0.92 |
| TPC-H SF1 ADBC total s | S3 | 34.7 | 34.5 | 0.99 | 1.00 1.01 0.99 |
| TPC-H SF1 JDBC total s | S3 | 35.4 | 35.8 | 1.01 | 0.98 1.03 1.03 |
| small ADBC c1 p50 / p95 / p99 ms | local | 14.6 / 37.4 / 44.3 | 12.5 / 34.6 / 40.7 | 0.86 / 0.93 / 0.92 | p50: 0.87 0.82 0.85 |
| small JDBC c1 p50 / p95 / p99 ms | local | 21.0 / 41.3 / 49.6 | 19.4 / 40.1 / 44.6 | 0.92 / 0.97 / 0.90 | p50: 0.95 0.78 0.87 |
| small ADBC c8 p50 / p95 / p99 ms | local | 88.4 / 249 / 365 | 82.6 / 249 / 366 | 0.93 / 1.00 / 1.00 | p95: 1.04 1.00 0.93 |
| small JDBC c8 p50 / p95 / p99 ms | local | 102 / 244 / 317 | 101 / 252 / 301 | 0.99 / 1.03 / 0.95 | p95: 0.95 1.03 1.08 |
| small ADBC c32 p50 / p95 / p99 ms | local | 376 / 1051 / 1309 | 361 / 1062 / 1345 | 0.96 / 1.01 / 1.03 | p95: 1.12 0.99 0.99 |
| small JDBC c32 p50 / p95 / p99 ms | local | 385 / 1070 / 1403 | 383 / 1039 / 1371 | 0.99 / 0.97 / 0.98 | p95: 0.98 0.93 0.96 |
| small ADBC c1 p50 / p95 / p99 ms | S3 | 24.3 / 726 / 853 | 24.1 / 694 / 1174 | 0.99 / 0.96 / 1.38 | p99: 1.28 0.92 1.41 |
| small JDBC c1 p50 / p95 / p99 ms | S3 | 29.6 / 671 / 738 | 28.2 / 696 / 790 | 0.95 / 1.04 / 1.07 | p95: 1.29 1.04 1.01 |
| small ADBC c8 p50 / p95 / p99 ms | S3 | 240 / 3919 / 4415 | 269 / 3752 / 4321 | 1.12 / 0.96 / 0.98 | p50: 1.03 0.99 1.12 |
| small JDBC c8 p50 / p95 / p99 ms | S3 | 245 / 4004 / 4348 | 268 / 3774 / 4113 | **1.10** / 0.94 / 0.95 | p50: **1.07 1.11 1.10** |
| small ADBC c32 p50 / p95 / p99 ms | S3 | 954 / 12866 / 14646 | 955 / 12976 / 14406 | 1.00 / 1.01 / 0.98 | p95: 1.01 1.00 1.04 |
| small JDBC c32 p50 / p95 / p99 ms | S3 | 930 / 14024 / 21311 | 955 / 13741 / 24528 | 1.03 / 0.98 / 1.15 | p99: 1.63 1.10 0.93 (noisy) |
| scan 1 / 4 / 8 streams MB/s | local | 544 / 547 / 486 | 526 / 557 / 490 | 0.97 / 1.02 / 1.01 | x8: 1.00 1.01 1.01 |
| scan 1 / 4 / 8 streams MB/s | S3 | 361 / 494 / 457 | 345 / 462 / 461 | 0.96 / 0.94 / 1.01 | x8: 0.97 1.02 0.95 |
| lineitem export ADBC MB/s | local / S3 | 623 / 353 | 595 / 330 | 0.96 / 0.93 | S3: 0.83 1.61 0.88 (noisy) |
| server peak RSS MB | core jobs | 729-2732 | 735-2798 | 0.90-1.02 | TPC-H local 0.90, S3 SF10 ADBC 0.94 |

The latency jobs ran on a slower runner type than build 6 (absolute times higher for both sides). Local small-query
p50 at c1 is 8-14 % faster in all rounds (ADBC 0.86, rounds 0.87 0.82 0.85); at 8/32 clients the candidate is level
(0.93-0.99), not the 19-28 % p50 gain of builds 2-5. Default scans are level with the baseline (x8 1.01), as in build 6 (1.02);
the +15-22 % x8 gain of builds 1-5 is not seen on the default path (shared DuckDB off).

## Item 21: closed-loop load, local SF10 (baseline A vs candidate B)

| clients | JDBC q/s A / B | JDBC p95 ms A / B | ADBC q/s A / B | ADBC p95 ms A / B |
|---|---|---|---|---|
| 1 | 38 / 40 | 44.8 / 42.5 | 41 / 42 | 39.5 / 38.4 |
| 8 | 44 / 44 | 280 / 282 | 44 / 44 | 281 / 279 |
| 32 | 41 / 41 | 1327 / 1318 | 39 / 40 | 1393 / 1393 |
| 64 | 38 / 38 | 3029 / 2989 | 37 / 37 | 3124 / 3183 |
| 128 | 35 / 35 | 6926 / 6924 | 34 / 34 | 6921 / 6957 |

Saturation (p95 < 100 ms, 0 errors): 1 client on both sides. 0 errors at every step. Peak RSS 4504 vs 4458 MB (0.99).
Level with the baseline as in build 6; the +5-7 % peak gain of builds 2 and 4 is still not seen.

## Item 22: shared DuckDB (`-DduckDbSharedDatabase=true`, B) vs default (A), same build, local

| metric | off (A) | on (B) | B / A | per round |
|---|---|---|---|---|
| scan 1 stream MB/s | 447 | 447 | 1.00 | 0.98 1.00 1.06 |
| scan 4 streams MB/s | 465 | 537 | **1.15** | 1.11 1.15 1.19 |
| scan 8 streams MB/s | 409 | 567 | **1.39** | 1.37 1.41 1.38 |
| lineitem export ADBC MB/s | 522 | 527 | 1.01 | 0.99 1.03 1.01 |
| server peak RSS MB (scan job) | 1137 | 1353 | 1.19 | 1.17 1.21 1.19 |
| TPC-H SF10 ADBC total s | 33.7 | 33.0 | 0.98 | 0.99 0.98 0.98 |
| TPC-H SF10 JDBC total s | 33.4 | 32.9 | 0.99 | 0.99 0.98 0.99 |
| server peak RSS MB (SF10 job) | 1639 | 1915 | 1.17 | 1.18 1.17 0.96 |
| load JDBC q/s peak / c128 | 44 / 35 | 51 / 48 | **1.16 / 1.37** | |
| load ADBC q/s peak / c128 | 44 / 34 | 51 / 48 | **1.16 / 1.41** | |
| load JDBC p50 / p95 ms at c32 | 752 / 1318 | 560 / 1195 | 0.74 / 0.91 | |
| load JDBC p95 ms at c8 | 282 | 319 | 1.13 | p50 0.79 |
| server peak RSS MB (load job) | 4468 | 3847 | 0.86 | 0.86 0.84 0.89 |

Shared DuckDB on is the clearest single gain since build 1: scans with 8 streams +39 % in every round (x4 +15 %),
closed-loop load +16 % at the peak and +37-41 % at 128 clients (35 -> 48 q/s JDBC, 0 errors) with 14 % less peak RSS
under load, SF10 level (0.98-0.99), 22/22. Costs: +17-19 % peak RSS on scans and SF10, and p95 at 8 load clients
+13 % (p50 -21 %). It is opt-in; the default is unchanged.

### Shared DuckDB on (A) vs upstream native (B), local scans

| metric | ours shared (A) | up-native (B) | ours / native |
|---|---|---|---|
| scan 1 stream MB/s | 712 | 683 | 1.04 |
| scan 4 streams MB/s | 854 | 876 | 0.98 |
| scan 8 streams MB/s | 900 | n/a (2 errors, failed gate) | - (Report 2 native: 807-823) |
| lineitem export ADBC MB/s | 859 | 858 | 1.00 |
| server peak RSS MB | 1467 | 3845 | 0.38 |

With shared DuckDB, our server reaches upstream native's scan speed (x4 0.98, x1 1.04, export equal; x8 900 MB/s
where native failed its gate in this job and measured 807-823 MB/s in Report 2) at 38 % of its peak RSS.

## Item 18: 3-node cluster on S3, `distributedComplete` off (A) vs on (B), same build

Pending: cluster run 40800581040 still running.

## Verdict

Pending until the cluster run is in.
