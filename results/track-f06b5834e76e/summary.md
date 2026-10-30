# Build `f06b5834e76e`: `resourceProfile=speed` vs balanced vs upstream native (item 23b follow-up)

Task: `ci/BUILD-TRACK-TASK.md` Phase B (newest untracked pre-release `server-1.0.0-f06b5834e76e`, published 2026-10-30
16:03 UTC). Runtime change since `843e4ad5b610`: `resourceProfile=speed` only, `duckDbThreads` = all cores but at least
balanced's 4 per query, aimed at the ITEM 23b flag (S3 small p95 at 8/32 clients 1.33-1.54). No other runtime change
(STATUS, CI workflow and lock commits only). Run **41132125972** (wave `track-f06b5834e76e`, the ITEM 23b set: 3
three-way jobs + aggregate, all green; `upstream-ref` pinned to `9fb08d9dd24d`). Full tables:
[run summary](../track-f06b5834e76e-41132125972/summary.md), [load](../track-f06b5834e76e-41132125972/load.md).
Wall times and error counts per round are from the job logs (the run artifacts are not downloadable from the session
environment).

## Setup

- As ITEM 23b: A = `f06b5834e76e` default (balanced), B = `f06b5834e76e` `-DresourceProfile=speed`, C = upstream
  native `9fb08d9dd24d`; rounds A B C / C B A / A B C; containers as `COMPARE-TASK.md` (2 CPUs pinned, 6 GB, `-Xmx3g`,
  direct 2g; clients and S3 on the other cores).
- Jobs: `i23b-small` on S3 and on local disk (control), `i23b-load` on local disk. All 3 jobs on AMD EPYC 7763
  runners, as the `843e4ad5b610` run, so the ratios are directly comparable with [ITEM23b](../ITEM23b-843e4ad5b610.md).
- Ratios are medians over 3 rounds (per round in brackets): times < 1 = speed faster, QPS > 1 = speed faster.

## Correctness

| workload | speed (B) | balanced (A) | upstream native (C) |
|---|---|---|---|
| small queries S3, 1 / 8 / 32 clients | 0 errors every round, answers equal | 0 | JDBC c1 21, c8 549-602, ADBC c8 640, c32 all errors; OOM-killed (exit 137) every round |
| small queries local, 1 / 8 / 32 | 0 every round | 0 | JDBC c1 20, c32 all errors; OOM-killed every round |
| closed-loop load 1-128, local | 0 | 0 | 0 |

The ITEM 23b result holds: speed has 0 errors at every step, S3 and local, in all 3 rounds. No OOM or restart for
either profile of `f06b5834e76e`.

## S3 small queries: speed vs balanced, compared with the `843e4ad5b610` flag

| metric | balanced | speed | speed/balanced f06b (rounds) | 843e (ITEM 23b) |
|---|---|---|---|---|
| c1 p50 ADBC / JDBC ms | 24.9 / 34.4 | 22.7 / 33.7 | 0.91 (1.30 0.89 0.86) / 0.98 (0.91 1.18 0.95) | 0.91 / 1.04 |
| c8 p50 ADBC / JDBC | 336 / 339 | 199 / 199 | 0.59 / 0.59 | 0.50 / 0.50 |
| c8 p95 ADBC / JDBC | 5514 / 5521 | 6053 / 5297 | 1.10 (1.10 0.98 1.08) / 0.96 (0.96 1.10 0.93) | **1.33 / 1.36** |
| c8 p99 ADBC / JDBC | 6024 / 8982 | 9503 / 9039 | **1.58 (1.58 1.55 1.54)** / 1.01 (1.55 0.87 0.91) | 1.06 / 1.37 |
| c32 p50 ADBC / JDBC | 1101 / 1119 | 554 / 592 | 0.50 (0.50 0.49 0.76) / 0.53 (0.54 0.53 0.72) | 0.52 / 0.50 |
| c32 p95 ADBC / JDBC | 17609 / 17005 | 26346 / 26976 | **1.50 (1.59 1.49 1.90) / 1.59 (1.45 1.59 2.08)** | **1.46 / 1.54** |
| c32 p99 ADBC / JDBC | 20087 / 20013 | 27993 / 29597 | 1.39 (1.39 1.39 0.89) / **1.48 (1.16 1.49 1.92)** | 1.15 / 1.40 |
| c8 wall s (640 q) ADBC / JDBC | 77.0 / 89.4 | 77.3 / 74.4 | 1.00 / 0.83 | - |
| c32 wall s (1280 q) ADBC / JDBC | 125.2 / 124.5 | 139.3 / 155.3 | **1.11 (1.11 1.10 1.21) / 1.25 (1.02 1.26 1.56)** | 1.05 / 1.15 |
| peak RSS MB | 2221 | 832 | 0.37 | 0.39 |

Round 3 of speed was slow on the 32-client step (c32 p50 0.72-0.76 vs ~0.50 in rounds 1-2, wall 194-198 s), but
rounds 1-2 alone show the same c32 p95 (1.45-1.59).

## Local small queries (control): speed vs balanced

| metric | balanced | speed | speed/balanced (rounds) | 843e |
|---|---|---|---|---|
| c1 p50 ADBC / JDBC ms | 15.7 / 23.3 | 15.1 / 22.5 | 0.97 / 0.97 | 0.98 / 0.97 |
| c1 p99 ADBC / JDBC | 52.1 / 58.5 | 55.7 / 57.2 | 1.07 (1.15 1.07 1.09) / 0.98 | 1.05 / 0.97 |
| c8 p50 ADBC / JDBC | 105.4 / 119.4 | 74.3 / 82.9 | 0.70 / 0.69 | 0.63 / 0.62 |
| c8 p95 ADBC / JDBC | 281.9 / 286.1 | 291.0 / 284.5 | 1.03 (1.06 1.03 1.03) / 0.99 | **1.13** / 1.02 |
| c8 p99 ADBC / JDBC | 356.6 / 356.4 | 398.7 / 353.2 | 1.12 (1.13 1.02 1.12) / 0.99 | 1.00 / 0.98 |
| c32 p50 ADBC / JDBC | 426.8 / 450.1 | 244.3 / 259.1 | 0.57 / 0.58 | 0.56 / 0.55 |
| c32 p95 ADBC / JDBC | 1239.5 / 1292.7 | 1147.9 / 1135.7 | 0.93 / 0.88 | 0.93 / 0.86 |
| c32 p99 ADBC / JDBC | 1686.5 / 1674.8 | 1308.0 / 1296.9 | 0.78 / 0.77 | 0.70 / 0.73 |
| peak RSS MB | 1458 | 705 | 0.48 | 0.47 |

## Closed-loop load, local (QPS / p95 ms)

| clients | balanced JDBC | speed JDBC | upstream JDBC | balanced ADBC | speed ADBC | upstream ADBC |
|---|---|---|---|---|---|---|
| 1 | 40 / 42.8 | 40 / 42.3 | 38 / 46.5 | 41 / 38.5 | 42 / 38.3 | 43 / 36.8 |
| 8 | 46 / 316.7 | 50 / 350.6 | 51 / 318.2 | 47 / 313.3 | 50 / 344.0 | 54 / 300.0 |
| 32 | 45 / 1298 | 51 / 1233 | 52 / 1182 | 46 / 1295 | 52 / 1228 | 54 / 1163 |
| 64 | 45 / 2720 | 51 / 2420 | 53 / 2355 | 45 / 2705 | 51 / 2395 | 53 / 2377 |
| 128 | 42 / 5974 | 49 / 5167 | 52 / 5093 | 42 / 5806 | 50 / 5191 | 53 / 5030 |

Speed/balanced QPS at 128 clients: JDBC 1.17, ADBC 1.19 (843e: 1.19 / 1.22); speed/upstream 0.94 / 0.94 (843e: 0.96 /
0.94). p95 at 128 clients 0.86 / 0.89 of balanced. At 8 clients speed p95 is 1.10-1.11 of balanced (QPS +7-9 %).
Peak RSS in the load job: speed 823 MB, balanced 4577 MB (0.18), upstream 4322 MB (0.19); server memory at 128 clients
speed 755-899 MiB vs balanced 4016-4688 and upstream 3637-4796. Errors 0 for all three.

## Verdict

- **Correct**, as `843e4ad5b610`: 0 errors for speed everywhere, S3 c32 included.
- **The fix does not remove the S3 c32 tail it targets:** S3 small c32 p95 is still 1.50 / 1.59 of balanced (rounds
  1.45-2.08; ~26-27 s vs ~17 s), unchanged from 843e (1.46 / 1.54), and the S3 c32 wall time for 1280 queries is now
  11-25 % longer (843e: 5-15 %). **New: S3 ADBC c8 p99 1.58 in all 3 rounds** (843e 1.06).
- Better than 843e: S3 c8 p95 down from 1.33-1.36 to 0.96-1.10 (not in all rounds above 1.05), and the local ADBC c8
  p95 flag of 843e is gone (1.03). Small: local ADBC c1 p99 1.07 (all rounds >= 1.07, ~3.6 ms) and local ADBC c8 p99
  1.12 (not all rounds).
- Unchanged: concurrent small-query p50 at 8/32 clients 0.50-0.70, load +17-19 % at 128 clients (0.94 of upstream
  native) at 0.18 of balanced's peak RSS.
- Next for item 23b: the S3 tail at 32 clients needs a different fix than the thread floor (per-query latency samples
  are in run artifact `ab-i23b-small-s3`, B/r*/small-*32*).
