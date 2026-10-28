# Build tracking: `4bb6441569be` vs baseline `7562a5bdb7b9`

- Build: `server-1.0.0-4bb6441569be` (S3: `duckDbThreads` default >= 4, aimed at the S3 small-query p95 regression of
  `d22cdaccb4e1`; contains `881b7c62b373` item 21 step 1 and `e9f0fd3` item 22 step 1 (opt-in, not enabled here)).
  Skipped as contained: `ba4139a2eb93` (item 20 (c)), `cadd1aca9c23` (item 20 (f)), `3fbf5b28b186` / `1f600b930eda`
  (plugins / test only).
- Run: compare 40638050743 (wave `track-load-4bb6441569be`, 9 of 9 jobs green). Full tables:
  [run summary](../track-load-4bb6441569be-40638050743/summary.md), [load report](../track-load-4bb6441569be-40638050743/load.md).
  Per-round load QPS below are from the job logs (`result.txt` of every round), because the artifacts are not readable
  from every environment.
- Pairs: A = baseline, B = candidate, same runner, 3 rounds (A B, B A, A B), containers as `COMPARE-TASK.md`.
  Ratio = B / A of the medians; times < 1 = candidate faster, MB/s and QPS > 1 = candidate faster.
- Correctness: TPC-H SF1 + SF10, ADBC + JDBC, local + S3: correctness gate passed in every job (22/22, no job
  disqualified); 0 errors in all load steps of both builds.

## Regression check (rule: > 5 % slower on a core metric in all 3 rounds)

- **The S3 p95 regression of `d22cdaccb4e1` is gone**: vs baseline S3 JDBC c32 p95 1.03 (rounds 0.99 1.06 0.97),
  JDBC c8 p95 1.06 (1.09 1.01 1.29, not all rounds), ADBC c8 p95 0.93, ADBC c32 p95 0.99. Directly vs `d22cdaccb4e1` on
  one runner: S3 c32 p95 0.58 (ADBC) / 0.65 (JDBC), c8 p95 0.85-0.87.
- The price on S3 is the p50 gain of `d22cdaccb4e1`: vs `d22cdaccb4e1` S3 c8 p50 1.46-1.50 and c1 p95 1.19-1.23 in all
  rounds. Against the baseline S3 c1/c8/c32 p50 is 0.89-1.08 (no round pattern), so S3 is back at baseline level, not
  worse than it.
- **Small regression, local disk, ADBC c8 tail: p95 1.07 (rounds 1.10 1.06 1.12), p99 1.15 (1.14 1.16 1.15)** while
  p50 at the same step is 0.75. Same shape as in `d22cdaccb4e1` on S3 (faster median, longer tail), much smaller;
  JDBC c8 p95 0.98 and both c32 p95 (0.96 / 0.97) are not affected.

## Core (default settings)

| metric | storage | A (baseline) | B (candidate) | B / A | per round |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC total s | local | 28.9 | 29.5 | 1.02 | 1.00 1.02 1.01 |
| TPC-H SF10 JDBC total s | local | 28.8 | 29.8 | 1.04 | 1.01 1.04 1.00 |
| TPC-H SF1 ADBC total s | local | 3.0 | 2.8 | 0.92 | 0.93 0.92 0.93 |
| TPC-H SF1 JDBC total s | local | 3.1 | 2.9 | 0.94 | 0.93 0.94 0.93 |
| TPC-H SF10 ADBC total s | S3 | 319.3 | 264.9 | 0.83 | 1.02 0.82 0.93 |
| TPC-H SF10 JDBC total s | S3 | 486.0 | 305.2 | 0.63 | 0.98 0.63 0.98 |
| TPC-H SF1 ADBC total s | S3 | 25.7 | 25.8 | 1.00 | 1.04 1.00 0.97 |
| TPC-H SF1 JDBC total s | S3 | 25.9 | 26.1 | 1.01 | 1.01 0.96 1.04 |
| small ADBC c1 p50 ms | local | 16.8 | 15.4 | 0.92 | 0.92 0.84 0.96 |
| small JDBC c1 p50 ms | local | 23.2 | 22.3 | 0.96 | 0.99 0.92 0.95 |
| small ADBC c8 p50 / p95 ms | local | 104 / 264 | 78 / 283 | 0.75 / **1.07** | p95: 1.10 1.06 1.12 |
| small JDBC c8 p50 / p95 ms | local | 117 / 285 | 93 / 279 | 0.79 / 0.98 | p95: 0.97 0.99 0.93 |
| small ADBC c32 p50 / p95 / p99 ms | local | 422 / 1194 / 1711 | 312 / 1158 / 1359 | 0.74 / 0.97 / 0.79 | p95: 0.98 0.98 0.93 |
| small JDBC c32 p50 / p95 / p99 ms | local | 466 / 1255 / 1810 | 374 / 1209 / 1528 | 0.80 / 0.96 / 0.84 | p95: 0.99 0.96 0.89 |
| small ADBC c1 p50 ms | S3 | 23.5 | 25.5 | 1.08 | 0.98 1.02 1.11 |
| small JDBC c1 p50 ms | S3 | 31.8 | 30.8 | 0.97 | 0.96 0.97 1.12 |
| small ADBC c32 p95 ms | S3 | 16589 | 16465 | 0.99 | 1.07 0.97 0.97 |
| small JDBC c32 p95 ms | S3 | 16234 | 16767 | 1.03 | 0.99 1.06 0.97 |
| scan 1 / 4 / 8 streams MB/s | local | 456 / 503 / 471 | 451 / 542 / 536 | 0.99 / 1.08 / **1.14** | x8: 1.13 1.14 1.14 |
| scan 1 / 4 / 8 streams MB/s | S3 | 408 / 481 / 459 | 406 / 486 / 467 | 1.00 / 1.01 / 1.02 | x8: 1.04 1.02 0.99 |
| lineitem export ADBC MB/s | local / S3 | 541 / 455 | 546 / 447 | 1.01 / 0.98 | |
| server peak RSS MB | all core jobs | 766-2807 | 785-2727 | 0.94-1.10 | TPC-H local 1.10 (1.20 1.11 1.04) |

S3 TPC-H totals vary a lot between rounds and runners (one slow baseline round each in SF10 ADBC / JDBC); the medians and
`d22cdaccb4e1` agree that the candidate is not slower on S3. Scan x8 local +14 % as in `d22cdaccb4e1`; on S3 the
`d22cdaccb4e1` gain (+10 %) is not seen here (1.02).

## Item 21: closed-loop load 1-128 clients, local Parquet (same runner, EPYC 7763)

QPS per step, median of 3 rounds (A = baseline, B = candidate):

| clients | JDBC A | JDBC B | B / A (per round) | ADBC A | ADBC B | B / A (per round) |
|---|---|---|---|---|---|---|
| 1 | 39.5 | 41.6 | 1.05 (1.06 1.05 1.08) | 41.5 | 43.7 | 1.05 (1.06 1.05 1.07) |
| 8 | 44.1 | 46.9 | 1.06 (1.03 1.06 1.04) | 45.0 | 47.5 | 1.06 (1.05 1.06 1.06) |
| 32 | 42.5 | 46.0 | 1.08 (1.11 1.08 1.08) | 41.3 | 45.1 | 1.09 (1.14 1.10 1.08) |
| 64 | 39.4 | 43.8 | 1.11 (1.13 1.10 1.11) | 38.5 | 43.2 | 1.12 (1.12 1.11 1.12) |
| 128 | 35.1 | 40.4 | **1.15** (1.15 1.19 1.12) | 34.4 | 40.8 | **1.19** (1.21 1.17 1.19) |
| peak | 44.1 (c8) | 46.9 (c8) | 1.06 (1.04 1.06 1.04) | 45.0 (c8) | 47.5 (c8) | 1.06 (1.05 1.06 1.06) |

Errors 0 in every step and round for both. Saturation by the rule "highest step with p95 < 100 ms" is c1 for both
(unchanged). The candidate keeps its throughput better past saturation (c128 -14 % from peak instead of -20 %).

Reference vs upstream native on another runner (Xeon 8573C; `load.md` medians): candidate peak ~53 q/s, upstream
native ~70 q/s (0.76x; native has errors=1 at ADBC c128 in 2 of 3 rounds). The gap to upstream (~84 q/s in Report 2)
remains the main open point of item 21.

## Verdict

**Better**: fixes the S3 small-query p95 regression of `d22cdaccb4e1` (S3 back to baseline tails), closed-loop load
+5-6 % at the peak and +15-19 % at 128 clients, local small-query p50 at 8/32 clients 20-26 % faster, local p99 at 32
clients 16-21 % faster, scan 8 streams local +14 %, TPC-H same or faster, 22/22 everywhere. Small flagged tail
regression: local ADBC c8 p95 1.07 / p99 1.15 in all rounds.
