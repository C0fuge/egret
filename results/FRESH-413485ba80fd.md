# Fresh upstream three-way: `413485ba80fd` speed vs balanced vs upstream native

Task: `ci/BUILD-TRACK-TASK.md`, "FRESH UPSTREAM TRACKING". Pre-release `server-1.0.0-413485ba80fd` (STATUS: item 27 done,
the speed profile sets `duckDbPreserveInsertionOrder=false`). Compare run 41604206524, wave
[`fresh-up-413485ba80fd`](../ci/waves/fresh-up-413485ba80fd.json), 10 jobs, all green, 3 rounds each, alternating order.

- A = `413485ba80fd` default (balanced)
- B = `413485ba80fd -DresourceProfile=speed` (file cache and, new, `duckDbPreserveInsertionOrder=false` in the profile)
- C = upstream native **`6e264c10f4031edcc7c021cd86dc807c8fff9bc6`** (head of `feat/starrocks-native-integration` at
  dispatch; the same commit as in the `fresh-up-f06b5834e76e` and `fresh-up-25aa7eec0f0f` runs, upstream has not moved)

Full tables: [run summary](fresh-up-413485ba80fd-41604206524/summary.md),
[speed report](fresh-up-413485ba80fd-41604206524/speed.md). Load and slow-link numbers are from the job logs (the wave
name does not trigger `load_report.py`). All three servers of a job run on the same runner, so A/C is taken from the A
and C medians of the same job. Ratios: times < 1 = first faster; MB/s and q/s > 1 = first faster.

## Correctness

| workload | speed (B) | balanced (A) | upstream native (C) |
|---|---|---|---|
| TPC-H SF1 + SF10, ADBC + JDBC, local | 22/22 | 22/22 | **0/22 ADBC, 1/22 JDBC** |
| TPC-H SF1 + SF10, ADBC + JDBC, S3 | 22/22 | 22/22 | **0/22 ADBC, 1/22 JDBC** |
| small queries 1/8/32 clients, local + S3 | 0 errors | 0 errors | **errors at every step, server died after small** |
| slow link TPC-H SF10 ADBC (ZSTD) | 22/22 | 22/22 | **0/22** |
| scans 1/4/8 + ADBC export, local + S3 | 0 errors | 0 errors | **scan x8 errors: local 2-3 per round (all 3 rounds), S3 1 in one round** (x1/x4/export 0) |
| closed-loop load 1-128, local | 0 errors | 0 errors | 0 errors |

Upstream native at `6e264c10f403` still cannot run the harness's TPC-H and small-query sets (`schema "tpch" does not
exist`, float64 vs decimal(38,4) on q06, `Can only select from ONE table`, `Unknown function: version()`), as in the two
previous fresh runs. New in this run: its 8-stream scan reports stream errors (it had none on the same commit before),
so its x8 MB/s is not ranked; upstream ratios are given for scan x1/x4, export, load and memory.

**Row order under speed (item 27).** The harness's answer checks are order-insensitive by design (TPC-H checksums are
taken over sorted, normalised rows; small-query answers are compared per class, `limit10` without ORDER BY is not
compared). Speed passes all of them: every TPC-H query returns the same row set as balanced and the in-process reference. Whether `duckDbPreserveInsertionOrder=false` changes the row order of queries *without* ORDER BY is therefore
not measured here; clients that rely on file order without ORDER BY should not use the speed profile.

## Speed vs balanced vs upstream (medians over 3 rounds)

| area | metric | B speed | A balanced | C upstream | speed / balanced (rounds) | speed / upstream | balanced / upstream |
|---|---|---|---|---|---|---|---|
| TPC-H local | SF1 ADBC (s) | 2.8 | 2.7 | n/a | 1.03 (1.06 1.01 1.00) | n/a | n/a |
| TPC-H local | SF10 ADBC (s) | 27.5 | 29.2 | n/a | 0.94 (0.94 0.93 0.98) | n/a | n/a |
| TPC-H local | SF10 JDBC (s) | 27.4 | 29.0 | n/a | 0.95 (0.95 0.98 0.96) | n/a | n/a |
| TPC-H S3 | SF1 ADBC (s) | 3.9 | 26.7 | n/a | **0.15** (0.15 0.15 0.14) | n/a | n/a |
| TPC-H S3 | SF10 ADBC (s) | 57.0 | 304.4 | n/a | **0.19** (0.19 0.19 0.19) | n/a | n/a |
| TPC-H S3 | SF10 JDBC (s) | 37.7 | 261.1 | n/a | **0.14** (0.15 0.15 0.14) | n/a | n/a |
| small local | ADBC c1 / c8 / c32 p50 (ms) | 20.4 / 102 / 374 | 17.1 / 113 / 445 | n/a | **1.19** (1.28 1.13 1.07) / 0.91 / 0.84 | n/a | n/a |
| small local | ADBC c8 p95 / p99 (ms) | 291 / 379 | 275 / 333 | n/a | 1.06 (1.09 1.05 1.04) / **1.14** (1.15 1.15 1.06) | n/a | n/a |
| small local | ADBC c32 p95 / p99 (ms) | 1151 / 1324 | 1287 / 1772 | n/a | 0.89 / 0.75 | n/a | n/a |
| small local | JDBC c1 / c8 / c32 p50 (ms) | 27.7 / 112 / 421 | 23.5 / 121 / 466 | n/a | **1.18** (1.17 1.17 1.18) / 0.93 / 0.90 | n/a | n/a |
| small local | JDBC c32 p95 / p99 (ms) | 1188 / 1444 | 1356 / 1926 | n/a | 0.88 / 0.75 | n/a | n/a |
| small S3 | ADBC c1 / c8 / c32 p50 (ms) | 16.4 / 72.8 / 236 | 25.9 / 307 / 1119 | n/a | 0.63 / 0.24 / 0.21 | n/a | n/a |
| small S3 | ADBC c1 / c8 / c32 p95 (ms) | 42.1 / 216 / 1027 | 683 / 5340 / 17314 | n/a | **0.06 / 0.04 / 0.06** | n/a | n/a |
| small S3 | JDBC c1 / c8 / c32 p50 (ms) | 31.4 / 92.4 / 259 | 37.1 / 348 / 1087 | n/a | 0.85 / 0.27 / 0.24 | n/a | n/a |
| small S3 | JDBC c1 / c8 / c32 p95 (ms) | 51.7 / 216 / 1108 | 708 / 5075 / 18177 | n/a | **0.07 / 0.04 / 0.06** | n/a | n/a |
| scan local | x1 / x4 / x8 (MB/s) | 432 / 568 / 574 | 433 / 437 / 393 | 417 / 545 / n/a (errors) | 1.00 / 1.30 / **1.46** | 1.04 / 1.04 / n/a | 1.04 / 0.80 / n/a |
| scan local | ADBC export (MB/s) | 512 | 510 | 521 | 1.01 | 0.98 | 0.98 |
| scan S3 | x1 / x4 / x8 (MB/s) | 371 / 578 / 606 | 371 / 435 / 429 | 363 / 578 / n/a (errors) | 1.00 / 1.33 / **1.41** | 1.02 / 1.00 / n/a | 1.02 / 0.75 / n/a |
| scan S3 | ADBC export (MB/s) | 500 | 397 | 546 | 1.26 (1.35 1.12 1.15) | 0.92 | 0.73 |
| load local | JDBC q/s at 1 / 8 / 32 / 64 / 128 clients | 41.3 / 51.4 / 51.8 / 52.5 / 50.6 | 41.4 / 44.6 / 41.8 / 39.2 / 36.0 | 38.5 / 52.2 / 53.4 / 54.6 / 54.0 | 1.00 / 1.15 / 1.24 / 1.34 / **1.41** | 1.07 / 0.98 / 0.97 / 0.96 / 0.94 | 1.08 / 0.85 / 0.78 / 0.72 / 0.67 |
| load local | ADBC q/s at 1 / 8 / 32 / 64 / 128 clients | 42.7 / 52.4 / 52.3 / 52.0 / 51.2 | 42.5 / 44.5 / 40.5 / 38.5 / 34.5 | 45.4 / 55.7 / 54.9 / 54.8 / 55.5 | 1.00 / 1.18 / 1.29 / 1.35 / **1.48** | 0.94 / 0.94 / 0.95 / 0.95 / 0.92 | 0.94 / 0.80 / 0.74 / 0.70 / 0.62 |
| load local | saturation (best median q/s) | 52.5 (JDBC c64) | 44.6 (JDBC c8) | 55.7 (ADBC c8) | 1.18 | 0.94 | 0.80 |
| slow link (10 ms, 1 Gbit), ZSTD | ADBC export (MB/s) | 261.5 | 247.5 | 256.9 | 1.06 (1.05 1.06 1.04) | 1.02 | 0.96 |
| slow link (10 ms, 1 Gbit), ZSTD | TPC-H SF10 ADBC (s) | 41.9 | 42.4 | n/a | 0.99 (0.97 0.98 0.99) | n/a | n/a |

Load per round, speed / balanced at 128 clients: JDBC 1.42 1.40 1.38, ADBC 1.48 1.48 1.49 (all rounds > 1.38).
Slow-link absolute MB/s are ~40 % lower than in the `25aa7eec0f0f` run for all three servers (upstream native too: 257
vs 403 MB/s on the same commit), so that is the runner/link, not the build; only the same-job ratios compare.

## Memory (server RSS peak, MB, median over rounds)

| job | B speed | A balanced | C upstream | speed / balanced | speed / upstream | balanced / upstream |
|---|---|---|---|---|---|---|
| TPC-H local | 1924 | 1600 | 350 (failed answers) | 1.20 | 5.50 | 4.57 |
| TPC-H S3 SF1 | 971 | 739 | 612 (failed answers) | 1.31 | 1.59 | 1.21 |
| TPC-H S3 SF10 ADBC | 3079 | 1568 | 1027 (failed answers) | 1.96 | 3.00 | 1.53 |
| TPC-H S3 SF10 JDBC | 3096 | 1560 | 1015 (failed answers) | 1.98 | 3.05 | 1.54 |
| small local | 759 | 1531 | 247 (died) | 0.50 | 3.07 | 6.20 |
| small S3 | 1385 | 2204 | 357 (died) | 0.63 | 3.88 | 6.17 |
| scan local | 1137 | 1171 | 3746 | 0.97 | 0.30 | 0.31 |
| scan S3 | 2988 | 1695 | 5946 | 1.76 | 0.50 | 0.29 |
| load local | 905 | 4522 | 985 | 0.20 | 0.92 | 4.59 |
| slow link | 1711 | 1518 | 613 (failed answers) | 1.13 | 2.79 | 2.48 |

Memory is essentially unchanged from `25aa7eec0f0f` (S3 scan speed RSS 2988 vs 3215 MB, the rest within ±5 %).

## Item 27 vs `25aa7eec0f0f` (previous fresh run)

Cross-run numbers come from different runners and are indicative only; the same-job ratios are the comparison.

| metric | `25aa7eec0f0f` | `413485ba80fd` | change |
|---|---|---|---|
| S3 scan x1 / x4 / x8, speed (MB/s) | 394 / 525 / 545 | 371 / 578 / 606 | -6 % / +10 % / +11 % |
| S3 scan speed / balanced x4 / x8 | 1.17 / 1.26 | 1.33 / 1.41 | +0.16 / +0.15 |
| S3 scan speed / upstream x4 | 0.87 | 1.00 | reaches upstream native |
| S3 ADBC export speed (MB/s), speed / balanced, speed / upstream | 490, 1.20, 0.87 | 500, 1.26, 0.92 | +2 % |
| local scan speed / balanced x4 / x8 | 1.07 / 1.25 | 1.30 / 1.46 | +0.23 / +0.21 |
| local scan speed / upstream x4 | 0.88 | 1.04 | passes upstream native |
| local ADBC export speed / balanced | 1.06 | 1.01 | -0.05 |
| local small c1 p50 speed / balanced, ADBC / JDBC | 1.01 / 0.96 | **1.19 / 1.18** | new c1 penalty |
| load at 128 clients speed / balanced, JDBC / ADBC | 1.52 / 1.50 | 1.41 / 1.48 | about the same |
| S3 TPC-H speed / balanced | 0.16-0.19 | 0.14-0.19 | same |
| S3 small p95 speed / balanced | 0.04-0.06 | 0.04-0.07 | same |

## Verdict

- **Item 27 lifts multi-stream scans under speed:** x4/x8 at 1.30-1.46 of balanced (was 1.07-1.26), on S3 and local in
  every round; speed now equals upstream native at 4 streams on S3 (1.00) and passes it locally (1.04), at 0.30-0.50 of
  its scan RSS. S3 ADBC export 1.26 of balanced, 0.92 of upstream. Single-stream scans and local export unchanged.
- **Regression by the rule (>5 % slower in all 3 rounds): local small queries at 1 client, speed p50 1.18 JDBC (rounds
  1.17 1.17 1.18; 23.5 -> 27.7 ms) and 1.19 ADBC (1.28 1.13 1.07; 17.1 -> 20.4 ms) of balanced, and local ADBC c8 p99 1.14
  (1.15 1.15 1.06).** In `25aa7eec0f0f` local c1 p50 was 1.01 / 0.96. S3 c1 is not affected (0.63 / 0.85), and local
  8/32 clients stay faster (p50 0.84-0.93, c32 p95/p99 0.75-0.89). Possibly a cost of the insertion-order setting on tiny
  single-client queries (not isolated in this wave); worth a check by the maintainer.
- Everything else as in `25aa7eec0f0f`: S3 TPC-H 5-7x faster, S3 small-query tails 14-25x lower, load +41-48 % at 128
  clients (0.92-0.94 of upstream native) at 0.20 of balanced RSS, local SF10 0.94-0.95, slow-link ZSTD export 1.06 of
  balanced and 1.02 of upstream; 22/22 and 0 errors everywhere.
- Upstream native at `6e264c10f403` (unchanged) still fails the TPC-H and small-query gate, and in this run also shows
  stream errors at 8 scan streams.
