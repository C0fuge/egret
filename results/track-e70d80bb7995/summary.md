# Build tracking: `e70d80bb7995` vs baseline `7562a5bdb7b9`

- Build: `server-1.0.0-e70d80bb7995` (auth-provider groups for Ranger, no change for the built-in providers; contains
  `9506620bb170` item 22 (c) opt-in `duckDbProducingStreams`, `99113c98c1c3` item 17 (e) S3 cache memory + opt-in
  `cacheAdmission=reuse`, `7f308a6cdb4d` item 22 (d) opt-in `flightZeroCopyWrites`). Skipped as contained: those three
  and `36b2177d51b4` (plugins only).
- Run: compare 40664667021 (wave `track-e70d80bb7995`, 13 of 13 jobs green). Full tables:
  [run summary](../track-e70d80bb7995-40664667021/summary.md), [speed report](../track-e70d80bb7995-40664667021/speed.md).
- Pairs: A = baseline (or the named reference), B = candidate, same runner, 3 rounds (A B, B A, A B), containers as
  `COMPARE-TASK.md`. Ratio = B / A of the medians; times < 1 = candidate faster, MB/s > 1 = candidate faster.
- Correctness: TPC-H SF1 + SF10, ADBC + JDBC, local + S3: correctness gate passed in every job of the candidate (22/22,
  no job disqualified). Only upstream native failed a gate (scan 8 streams, errors=3 in 2 rounds, see item 22).

## Regression check (rule: > 5 % slower on a core metric in all 3 rounds)

- **S3 small queries, ADBC c1 p50 1.25 (rounds 1.31 1.18 1.36; 18.1 -> 22.7 ms).** JDBC c1 p50 1.13 (0.98 1.17 1.11)
  and ADBC c32 p50 1.08 (1.08 1.08 1.00) point the same way but not in all rounds; p95/p99 at c1 and c32 are 0.94-1.04
  (JDBC c32 p99 1.49 is one long outlier in 2 rounds). Round 3 of this job was slow for the candidate at every step
  (1.3-1.9x), so it is a noisy job; rounds 1 and 2 alone still show ADBC c1 p50 1.31 / 1.18. Build 2 had S3 ADBC c1
  p50 1.08 (0.98 1.02 1.11), so this is a new or grown effect. Local disk is not affected (ADBC c1 p50 0.87).
- The local ADBC c8 tail regression of `4bb6441569be` is gone: vs baseline ADBC c8 p95 0.94 (0.97 0.92 0.94), p99 0.93;
  directly vs `4bb6441569be` on one runner p95 1.02 (0.95 1.04 1.04), p99 0.96, i.e. both builds are equal at that step
  and the build-2 tail is not reproduced against the baseline here.

## Core (default settings)

| metric | storage | A (baseline) | B (candidate) | B / A | per round |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC total s | local | 37.5 | 37.0 | 0.99 | 0.99 0.98 0.99 |
| TPC-H SF10 JDBC total s | local | 37.6 | 37.1 | 0.99 | 1.00 0.99 0.98 |
| TPC-H SF1 ADBC total s | local | 4.0 | 3.7 | 0.93 | 0.93 0.92 0.93 |
| TPC-H SF1 JDBC total s | local | 4.1 | 3.8 | 0.93 | 0.95 0.92 0.91 |
| TPC-H SF10 ADBC total s | S3 | 459.4 | 305.8 | 0.67 | 1.03 0.65 0.97 |
| TPC-H SF10 JDBC total s | S3 | 497.5 | 334.0 | 0.67 | 1.00 0.66 1.02 |
| TPC-H SF1 ADBC total s | S3 | 26.6 | 26.6 | 1.00 | 1.00 0.99 1.01 |
| TPC-H SF1 JDBC total s | S3 | 26.5 | 26.8 | 1.01 | 1.01 0.97 1.03 |
| small ADBC c1 p50 ms | local | 14.9 | 12.9 | 0.87 | 0.79 0.86 0.91 |
| small JDBC c1 p50 ms | local | 20.2 | 19.5 | 0.96 | 0.92 0.95 0.96 |
| small ADBC c8 p50 / p95 ms | local | 88 / 250 | 68 / 234 | 0.77 / 0.94 | p95: 0.97 0.92 0.94 |
| small JDBC c8 p50 / p95 ms | local | 97 / 246 | 78 / 229 | 0.81 / 0.93 | p95: 0.91 0.93 0.93 |
| small ADBC c32 p50 / p95 / p99 ms | local | 362 / 1010 / 1323 | 286 / 996 / 1335 | 0.79 / 0.99 / 1.01 | p95: 0.96 0.99 0.96 |
| small JDBC c32 p50 / p95 / p99 ms | local | 387 / 1084 / 1361 | 288 / 985 / 1224 | 0.74 / 0.91 / 0.90 | p95: 0.91 0.91 0.92 |
| small ADBC c1 p50 ms | S3 | 18.1 | 22.7 | **1.25** | **1.31 1.18 1.36** |
| small JDBC c1 p50 ms | S3 | 25.6 | 28.8 | 1.13 | 0.98 1.17 1.11 |
| small ADBC c32 p95 ms | S3 | 13048 | 13242 | 1.01 | 1.05 1.01 0.98 |
| small JDBC c32 p95 ms | S3 | 13400 | 13873 | 1.04 | 1.05 1.04 1.56 |
| scan 1 / 4 / 8 streams MB/s | local | 548 / 556 / 494 | 548 / 603 / 601 | 1.00 / 1.08 / **1.22** | x8: 1.22 1.21 1.24 |
| scan 1 / 4 / 8 streams MB/s | S3 | 560 / 707 / 686 | 566 / 689 / 655 | 1.01 / 0.97 / 0.95 | x8: 0.93 1.03 0.95 |
| lineitem export ADBC MB/s | local / S3 | 632 / 611 | 635 / 596 | 1.01 / 0.98 | |
| server peak RSS MB | all core jobs | 757-2890 | 769-2896 | 0.94-1.07 | TPC-H local 1.07 (1.02 1.04 1.11) |

S3 SF10 totals again have one slow baseline round per job (as in builds 1 and 2); the other rounds are 0.97-1.03, so
S3 SF10 is "same", not 33 % faster. Scan x8 local +22 % (build 2: +14 %). Not run for this build: closed-loop load
(item 21, no change since build 2) and slow link (item 20, no change since build 1).

## Item 22: multi-stream scan, local Parquet (opt-in flags of this build)

| pair (same runner) | x1 MB/s | x4 MB/s | x8 MB/s | export ADBC MB/s | peak RSS MB |
|---|---|---|---|---|---|
| default -> `flightZeroCopyWrites=true` | 567 -> 591 (1.04) | 649 -> 694 (1.07) | 663 -> 699 (**1.06**, rounds 1.06 1.05 1.07) | 664 -> 689 (1.04) | 1415 -> 1393 (0.98) |
| default -> `duckDbProducingStreams=2` | 442 -> 438 (0.99) | 499 -> 504 (1.01) | 499 -> 517 (1.04, rounds 1.03 1.04 1.03) | 498 -> 511 (1.03) | 922 -> 854 (0.93) |
| zero-copy (A) vs upstream native (B) | 711 vs 667 (0.94) | 866 vs 867 (1.00) | 854 vs n/a (native: errors=3 in 2 rounds) | 840 vs 821 (0.98) | 1299 vs 3732 (2.87) |

Zero-copy writes give a small, consistent gain (+4-7 % in every round, all stream counts); producing streams = 2 adds
+3-4 % at 8 streams only. With zero-copy the candidate reaches upstream native on that runner: equal at 4 streams,
ahead at 1 stream, 854 MB/s at 8 streams where native failed the gate (reference 807-823 MB/s in Report 2), at a third
of native's peak RSS.

## Item 17: S3 cache (1 GiB, `duckDbThreads=4` on both sides)

| pair (same runner) | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c32 p95 | SF1 ADBC | SF10 ADBC | peak RSS MB |
|---|---|---|---|---|---|---|
| cache off -> on (this build) | 0.43 | 0.07 | 0.07 | 0.35 | **1.34** (1.45 1.34 1.30) | 2289 -> 5149 |
| `4e77c6bda59a` on -> this build on | 1.04 | 0.99 | 0.92 | 1.01 | 0.99 | 5702 -> 5263 (**0.92**, rounds 0.91 0.92 0.93) |
| admission always -> `reuse` (this build) | 0.99 | 1.02 | 0.98 | 1.04 | 0.92 (0.92 1.02 1.03) | 5179 -> 5569 (1.08) |

- Item 17 (e) cache memory: peak RSS with the cache on is 8 % lower than `4e77c6bda59a` in every round (5.3 GB of the
  6 GB limit instead of 5.7 GB), with the same speed (small queries, SF1, SF10 0.92-1.04).
- The cache's SF10 cost is larger on this runner than in `c10-cache` (cache on / off 1.34 here, 1.08 there); since the
  cache-on speed equals `4e77c6bda59a`, the difference comes from the faster cache-off side of this build/runner, not
  from a cache slowdown. Opt-in, not a core metric.
- `cacheAdmission=reuse` shows no measurable effect in this workload (all metrics 0.92-1.07, no round pattern) and
  peaks 8 % higher in RSS.

## Verdict

**Better, with one flagged S3 small-query point.** Local: small-query p50 13-26 % faster at every client count, p95
equal or better (the build-2 ADBC c8 tail flag is gone), TPC-H SF1 7 % faster, scan 8 streams +22 %. Opt-in item 22
zero-copy writes +4-7 % on scans and on par with upstream native at a third of its memory; item 17 (e) cuts cache-on
peak RSS by 8 % at equal speed. 22/22 everywhere. **Flag: S3 small ADBC c1 p50 1.25 (1.31 1.18 1.36) in a noisy job;
re-check in the next build's S3 core job.**
