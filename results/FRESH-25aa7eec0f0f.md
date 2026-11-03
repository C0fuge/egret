# Fresh upstream three-way: `25aa7eec0f0f` speed vs balanced vs upstream native

Task: `ci/BUILD-TRACK-TASK.md`, "FRESH UPSTREAM TRACKING". Pre-release `server-1.0.0-25aa7eec0f0f` (STATUS: item 26 done,
hadoopfs short-circuit from LIBHDFS3_CONF / hdfs-site.xml). Compare run 41584018828, wave
[`fresh-up-25aa7eec0f0f`](../ci/waves/fresh-up-25aa7eec0f0f.json), 10 jobs, all green, 3 rounds each, alternating order.

- A = `25aa7eec0f0f` default (balanced)
- B = `25aa7eec0f0f -DresourceProfile=speed` (file cache is part of the profile since `57e054887f7a`)
- C = upstream native **`6e264c10f4031edcc7c021cd86dc807c8fff9bc6`** (head of `feat/starrocks-native-integration` at
  dispatch; the same commit as in the `fresh-up-f06b5834e76e` run, so upstream has not moved)

Full tables: [run summary](fresh-up-25aa7eec0f0f-41584018828/summary.md),
[speed report](fresh-up-25aa7eec0f0f-41584018828/speed.md). Load and slow-link numbers are from the job logs (the wave
name does not trigger `load_report.py`; artifacts are not downloadable from the session). All three servers of a job run
on the same runner, so A/C is taken from the A and C medians of the same job. Ratios: times < 1 = first faster; MB/s and
q/s > 1 = first faster.

## Correctness

| workload | speed (B) | balanced (A) | upstream native (C) |
|---|---|---|---|
| TPC-H SF1 + SF10, ADBC + JDBC, local | 22/22 | 22/22 | **0/22 ADBC, 1/22 JDBC** |
| TPC-H SF1 + SF10, ADBC + JDBC, S3 | 22/22 | 22/22 | **0/22 ADBC, 1/22 JDBC** |
| small queries 1/8/32 clients, local + S3 | 0 errors | 0 errors | **errors at every step, server died after small** |
| slow link TPC-H SF10 ADBC (ZSTD) | 22/22 | 22/22 | **0/22** |
| scans 1/4/8 + ADBC export, local + S3 | 0 errors | 0 errors | 0 errors |
| closed-loop load 1-128, local | 0 errors | 0 errors | 0 errors |

Upstream native at `6e264c10f403` still cannot run the harness's TPC-H and small-query sets: `Catalog Error: ... schema
"tpch" does not exist`, `endpoint 0 returned inconsistent schema` (float64 vs decimal(38,4) on q06), `Can only select from
ONE table`, `Unknown function: version()`. This is the same as in the `fresh-up-f06b5834e76e` run; it is an interface gap
of that branch (no `tpch` schema, decimal typing), not a server crash under load. Upstream ratios are therefore only given
for scans, load and memory.

## Speed vs balanced vs upstream (medians over 3 rounds)

| area | metric | B speed | A balanced | C upstream | speed / balanced (rounds) | speed / upstream | balanced / upstream |
|---|---|---|---|---|---|---|---|
| TPC-H local | SF1 ADBC (s) | 3.2 | 3.2 | n/a | 1.02 (1.02 1.04 0.99) | n/a | n/a |
| TPC-H local | SF10 ADBC (s) | 32.9 | 34.2 | n/a | 0.96 (0.97 0.99 0.95) | n/a | n/a |
| TPC-H local | SF10 JDBC (s) | 33.2 | 34.1 | n/a | 0.97 (0.96 0.97 0.97) | n/a | n/a |
| TPC-H S3 | SF1 ADBC (s) | 4.2 | 26.3 | n/a | **0.16** (0.16 0.16 0.15) | n/a | n/a |
| TPC-H S3 | SF10 ADBC (s) | 59.5 | 305.2 | n/a | **0.19** (0.18 0.19 0.20) | n/a | n/a |
| TPC-H S3 | SF10 JDBC (s) | 54.2 | 306.5 | n/a | **0.18** (0.17 0.18 0.18) | n/a | n/a |
| small local | ADBC c1 / c8 / c32 p50 (ms) | 15.7 / 71.9 / 251 | 15.5 / 97.2 / 420 | n/a | 1.01 / 0.74 / 0.60 | n/a | n/a |
| small local | ADBC c32 p95 / p99 (ms) | 1062 / 1296 | 1130 / 1466 | n/a | 0.94 / 0.88 | n/a | n/a |
| small local | JDBC c1 / c8 / c32 p50 (ms) | 21.7 / 82.8 / 259 | 22.6 / 113 / 429 | n/a | 0.96 / 0.73 / 0.60 | n/a | n/a |
| small local | JDBC c32 p95 / p99 (ms) | 1056 / 1228 | 1185 / 1602 | n/a | 0.89 / 0.77 | n/a | n/a |
| small S3 | ADBC c1 / c8 / c32 p50 (ms) | 10.6 / 48.0 / 145 | 21.4 / 266 / 956 | n/a | 0.50 / 0.18 / 0.15 | n/a | n/a |
| small S3 | ADBC c1 / c8 / c32 p95 (ms) | 30.9 / 152 / 773 | 686 / 3696 / 13293 | n/a | **0.05 / 0.04 / 0.06** | n/a | n/a |
| small S3 | JDBC c1 / c8 / c32 p50 (ms) | 21.8 / 61.1 / 165 | 28.5 / 268 / 967 | n/a | 0.77 / 0.23 / 0.17 | n/a | n/a |
| small S3 | JDBC c1 / c8 / c32 p95 (ms) | 42.9 / 161 / 800 | 694 / 3648 / 12694 | n/a | **0.06 / 0.04 / 0.06** | n/a | n/a |
| scan local | x1 / x4 / x8 (MB/s) | 461 / 511 / 531 | 455 / 475 / 424 | 439 / 580 / 603 | 1.01 / 1.07 / 1.25 | 1.05 / 0.88 / 0.88 | 1.04 / 0.82 / 0.70 |
| scan local | ADBC export (MB/s) | 557 | 527 | 562 | 1.06 | 0.99 | 0.94 |
| scan S3 | x1 / x4 / x8 (MB/s) | 394 / 525 / 545 | 386 / 447 / 434 | 386 / 605 / 614 | 1.02 / 1.17 / 1.26 | 1.02 / 0.87 / 0.89 | 1.00 / 0.74 / 0.71 |
| scan S3 | ADBC export (MB/s) | 490 | 409 | 562 | 1.20 | 0.87 | 0.73 |
| load local | JDBC q/s at 1 / 8 / 32 / 128 clients | 44.1 / 54.1 / 59.6 / 55.5 | 43.5 / 48.5 / 46.1 / 36.5 | 40.9 / 58.6 / 61.4 / 60.1 | 1.01 / 1.12 / 1.29 / **1.52** | 1.08 / 0.92 / 0.97 / 0.92 | 1.06 / 0.83 / 0.75 / 0.61 |
| load local | ADBC q/s at 1 / 8 / 32 / 128 clients | 47.0 / 55.9 / 57.0 / 53.9 | 45.5 / 49.0 / 43.5 / 36.0 | 48.9 / 61.5 / 62.1 / 61.3 | 1.03 / 1.14 / 1.31 / **1.50** | 0.96 / 0.91 / 0.92 / 0.88 | 0.93 / 0.80 / 0.70 / 0.59 |
| load local | saturation (best median q/s) | 59.6 (JDBC c32) | 49.0 (ADBC c8) | 62.2 (ADBC c64) | 1.22 | 0.96 | 0.79 |
| slow link (10 ms, 1 Gbit), ZSTD | ADBC export (MB/s) | 428 | 369 | 403 | 1.16 (1.19 1.16 0.97) | 1.06 | 0.92 |
| slow link (10 ms, 1 Gbit), ZSTD | TPC-H SF10 ADBC (s) | 27.3 | 27.7 | n/a | 0.99 | n/a | n/a |

Load per round, speed / balanced at 128 clients: JDBC 1.42 1.39 1.64, ADBC 1.50 1.43 1.58 (all rounds > 1.39).

## Memory (server RSS peak, MB, median over rounds)

| job | B speed | A balanced | C upstream | speed / balanced | speed / upstream | balanced / upstream |
|---|---|---|---|---|---|---|
| TPC-H local | 1823 | 1530 | 354 (failed answers) | 1.19 | 5.15 | 4.32 |
| TPC-H S3 SF1 | 916 | 724 | 630 (failed answers) | 1.27 | 1.45 | 1.15 |
| TPC-H S3 SF10 ADBC | 3054 | 1578 | 984 (failed answers) | 1.94 | 3.10 | 1.60 |
| TPC-H S3 SF10 JDBC | 3047 | 1548 | 1003 (failed answers) | 1.97 | 3.04 | 1.54 |
| small local | 729 | 1477 | 253 (died) | 0.49 | 2.88 | 5.84 |
| small S3 | 1351 | 2226 | 383 (died) | 0.61 | 3.53 | 5.81 |
| scan local | 1123 | 1135 | 3610 | 0.99 | 0.31 | 0.31 |
| scan S3 | 3215 | 1685 | 5832 | 1.91 | 0.55 | 0.29 |
| load local | 874 | 4664 | 945 | 0.19 | 0.92 | 4.94 |
| slow link | 1742 | 1617 | 596 (failed answers) | 1.08 | 2.92 | 2.71 |

Upstream RSS in jobs where it fails its answers is not comparable (it does little work). The speed profile's file cache
costs ~1.9x balanced RSS on S3 TPC-H SF10 and S3 scans (about 3.0-3.2 GB of the 6 GB limit), and saves memory on small
queries and under load (0.19-0.61).

## Verdict

- **Speed is better than balanced everywhere measured, with no regression by the rule** (no core metric > 5 % slower in
  all 3 rounds; the worst is local SF1 ADBC 1.02, rounds 1.02 1.04 0.99). S3 TPC-H 5-6x faster and S3 small-query tails
  16-25x lower (file cache); load +50-52 % at 128 clients; scans x8 +25 %; slow-link ZSTD export +16 %.
- **The `f06b5834e76e` flag (S3 small c32 p95 1.50-1.59 of balanced) is gone with the file cache in the profile:** S3 c32
  p95 is 0.06 of balanced (773-800 ms vs 12.7-13.3 s), 0 errors at every step.
- vs upstream native (scans and load only, where it answers): speed is at 0.87-0.89 on S3 x4/x8 and 0.88 on local
  x4/x8, 0.88-0.97 under load, ahead on single-stream scans (1.02-1.05) and on the slow link (1.06), at 0.31-0.55 of its
  scan RSS and 0.92 of its load RSS.
- Upstream native at `6e264c10f403` is unchanged since the last fresh run and still fails the TPC-H and small-query
  correctness gate (no `tpch` schema, decimal vs float64 on q06).
