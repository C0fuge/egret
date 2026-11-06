# Fresh upstream three-way: `deafc861cce3` speed vs balanced vs upstream native

Task: `ci/BUILD-TRACK-TASK.md`, "FRESH UPSTREAM TRACKING". Pre-release `server-1.0.0-deafc861cce3` (kestrel item 34; its
HDFS acceptance is [ACCEPT-deafc861cce3](ACCEPT-deafc861cce3.md), SHIP). Compare run 42223833724, wave
[`fresh-up-deafc861cce3`](../ci/waves/fresh-up-deafc861cce3.json), 10 jobs, all green, 3 rounds each, alternating order.

- A = `deafc861cce3` default (balanced)
- B = `deafc861cce3 -DresourceProfile=speed`
- C = upstream native **`9e4787906b07b6ecee80167ad3a0a2f0022d0ff3`** (head of `feat/starrocks-native-integration` at
  dispatch; **new**: the three previous fresh runs measured `6e264c10f403`)

Full tables: [run summary](fresh-up-deafc861cce3-42223833724/summary.md),
[speed report](fresh-up-deafc861cce3-42223833724/speed.md), [load report](fresh-up-deafc861cce3-42223833724/load.md)
(`ci/load_report.py`, via `rereport` run 42244896618 with the new `load` input, which also splits side C as the compare
aggregate does). The q/s in the main table come from each round's `result.txt` (the client's own 60 s count, as in
`FRESH-413485ba80fd`); latency, CPU and memory per step from `load.md`, see "Load per step" below. All three servers of a job run on the same runner, so A/C comes from the A
and C medians of the same job. Ratios: for times, < 1 = first faster; for MB/s and q/s, > 1 = first faster.

## Correctness

| workload | speed (B) | balanced (A) | upstream native (C) |
|---|---|---|---|
| TPC-H SF1 + SF10, ADBC + JDBC, local | 22/22 | 22/22 | **0/22 ADBC, 1/22 JDBC** |
| TPC-H SF1 + SF10, ADBC + JDBC, S3 | 22/22 | 22/22 | **0/22 ADBC, 1/22 JDBC** |
| small queries 1/8/32 clients, local + S3 | 0 errors | 0 errors | **errors at every step, server died after small** |
| slow link TPC-H SF10 ADBC (ZSTD) | 22/22 | 22/22 | **0/22** (`schema "tpch" does not exist`) |
| scans 1/4/8 + ADBC export, local + S3 | 0 errors | 0 errors | **local scan x8: stream errors in 2 rounds (3 and 2)**; S3 0 errors |
| closed-loop load 1-128, local | 0 errors | 0 errors | 0 errors |

The new upstream commit `9e4787906b07` behaves like `6e264c10f403` on the gate: it still cannot run the harness's TPC-H
and small-query sets (no `tpch` schema, the same answer differences), and the server dies after the small-query set.

## Speed vs balanced vs upstream (medians over 3 rounds)

| area | metric | B speed | A balanced | C upstream | speed / balanced (rounds) | speed / upstream | balanced / upstream |
|---|---|---|---|---|---|---|---|
| TPC-H local | SF1 ADBC (s) | 4.0 | 4.0 | n/a | 1.01 (1.01 1.01 0.99) | n/a | n/a |
| TPC-H local | SF10 ADBC (s) | 39.1 | 40.3 | n/a | 0.97 (0.96 0.96 0.98) | n/a | n/a |
| TPC-H local | SF10 JDBC (s) | 38.3 | 40.3 | n/a | 0.95 (0.95 0.95 0.95) | n/a | n/a |
| TPC-H S3 | SF1 ADBC / JDBC (s) | 4.5 / 4.5 | 25.8 / 25.8 | n/a | **0.18 / 0.18** | n/a | n/a |
| TPC-H S3 | SF10 ADBC (s) | 41.6 | 264.5 | n/a | **0.16** (0.21 0.16 0.14) | n/a | n/a |
| TPC-H S3 | SF10 JDBC (s) | 64.2 | 421.4 | n/a | **0.15** (0.14 0.15 0.15) | n/a | n/a |
| small local | ADBC c1 / c8 / c32 p50 (ms) | 11.9 / 62.1 / 243 | 11.1 / 66.8 / 273 | n/a | 1.08 (1.17 1.08 1.02) / 0.93 / 0.89 | n/a | n/a |
| small local | ADBC c8 p95 / p99 (ms) | 172 / 213 | 171 / 211 | n/a | 1.00 / 1.01 | n/a | n/a |
| small local | ADBC c32 p95 / p99 (ms) | 702 / 816 | 903 / 1214 | n/a | 0.78 / 0.67 | n/a | n/a |
| small local | JDBC c1 / c8 / c32 p50 (ms) | 17.1 / 73.4 / 249 | 15.5 / 74.7 / 298 | n/a | **1.10** (1.18 1.10 1.12) / 0.98 / 0.83 | n/a | n/a |
| small local | JDBC c32 p95 / p99 (ms) | 694 / 836 | 830 / 1059 | n/a | 0.84 / 0.79 | n/a | n/a |
| small S3 | ADBC c1 / c8 / c32 p50 (ms) | 11.3 / 46.7 / 150 | 19.1 / 258 / 955 | n/a | 0.59 / 0.18 / 0.16 | n/a | n/a |
| small S3 | ADBC c1 / c8 / c32 p95 (ms) | 28.1 / 129 / 622 | 696 / 3846 / 13195 | n/a | **0.04 / 0.03 / 0.05** | n/a | n/a |
| small S3 | JDBC c1 / c8 / c32 p50 (ms) | 24.5 / 65.9 / 179 | 27.0 / 244 / 946 | n/a | 0.91 / 0.27 / 0.19 | n/a | n/a |
| small S3 | JDBC c1 / c8 / c32 p95 (ms) | 39.3 / 140 / 638 | 698 / 3888 / 13000 | n/a | **0.06 / 0.04 / 0.05** | n/a | n/a |
| scan local | x1 / x4 / x8 (MB/s) | 537 / 714 / 730 | 548 / 550 / 477 | 528 / 673 / n/a (errors) | 0.98 / 1.30 / **1.53** | 1.02 / 1.06 / n/a | 1.04 / 0.82 / n/a |
| scan local | ADBC export (MB/s) | 646 | 630 | 650 | 1.03 | 0.99 | 0.97 |
| scan S3 | x1 / x4 / x8 (MB/s) | 438 / 720 / 726 | 404 / 482 / 459 | 396 / 640 / 633 | 1.08 / 1.49 / **1.58** | 1.10 / **1.13 / 1.15** | 1.02 / 0.75 / 0.72 |
| scan S3 | ADBC export (MB/s) | 567 | 421 | 622 | 1.35 (1.30 1.36 1.35) | 0.91 | 0.68 |
| load local | JDBC q/s at 1 / 8 / 32 / 64 / 128 clients | 41.8 / 49.7 / 51.5 / 51.1 / 51.5 | 38.4 / 43.4 / 40.8 / 38.6 / 36.3 | 39.2 / 52.8 / 53.9 / 54.0 / 54.4 | 1.09 / 1.15 / 1.26 / 1.32 / **1.42** | 1.07 / 0.94 / 0.96 / 0.95 / 0.95 | 0.98 / 0.82 / 0.76 / 0.71 / 0.67 |
| load local | ADBC q/s at 1 / 8 / 32 / 64 / 128 clients | 42.9 / 49.9 / 51.0 / 51.6 / 51.5 | 41.3 / 42.9 / 40.5 / 37.2 / 35.5 | 45.5 / 55.7 / 55.6 / 55.6 / 54.9 | 1.04 / 1.16 / 1.26 / 1.39 / **1.45** | 0.94 / 0.90 / 0.92 / 0.93 / 0.94 | 0.91 / 0.77 / 0.73 / 0.67 / 0.65 |
| load local | saturation (best median q/s) | 51.6 (ADBC c64) | 43.4 (JDBC c8) | 55.7 (ADBC c8) | 1.19 | 0.93 | 0.78 |
| slow link (10 ms, 1 Gbit), ZSTD | ADBC export (MB/s) | 255.0 | 253.9 | 262.8 | 1.00 (0.99 1.02 1.00) | 0.97 | 0.97 |
| slow link (10 ms, 1 Gbit), ZSTD | TPC-H SF10 ADBC (s) | 39.5 | 41.5 | n/a | 0.95 (0.95 0.93 0.96) | n/a | n/a |

Load per round, speed / balanced at 128 clients: JDBC 1.38 1.46 1.42, ADBC 1.42 1.54 1.47. Upstream ratios on scans
(S3 x8 included, no errors there this time), export, load and memory only; TPC-H and small queries fail its gate.

## Load per step (`ci/load_report.py`, medians over rounds)

p50 / p95 ms, server CPU % and server memory MiB (docker stats max in the step); 0 errors in every step for all three.

| clients | JDBC speed | JDBC balanced | JDBC upstream | ADBC speed | ADBC balanced | ADBC upstream |
|---|---|---|---|---|---|---|
| 1 | 19.6 / 40.8, 169 %, 390 | 19.9 / 42.1, 167 %, 397 | 21.2 / 46.2, 163 %, 437 | 19.3 / 37.5, 162 %, 418 | 19.7 / 38.3, 163 %, 418 | 17.8 / 35.8, 165 %, 412 |
| 8 | 153 / 345, 200 %, 479 | 171 / 312, 198 %, 770 | 138 / 306, 199 %, 447 | 155 / 339, 191 %, 534 | 171 / 315, 191 %, 800 | 130 / 294, 197 %, 444 |
| 32 | 544 / 1239, 197 %, 588 | 652 / 1280, 196 %, 1617 | 518 / 1144, 191 %, 550 | 560 / 1235, 193 %, 597 | 660 / 1288, 193 %, 1686 | 505 / 1126, 203 %, 603 |
| 64 | 1175 / 2406, 193 %, 720 | 1352 / 2694, 188 %, 2503 | 1072 / 2336, 192 %, 691 | 1140 / 2402, 202 %, 747 | 1341 / 2657, 196 %, 2875 | 1053 / 2280, 200 %, 743 |
| 128 | 2282 / 5174, 186 %, 886 | 2712 / 5838, 188 %, 3949 | 2158 / 4806, 193 %, 917 | 2281 / 5033, 201 %, 922 | 2778 / 5773, 195 %, 4477 | 2167 / 4764, 193 %, 1004 |

All three servers run at the 2-CPU limit from 8 clients on, so q/s is CPU-bound; balanced's memory grows to 3.9-4.5 GB
at 128 clients, speed stays under 1 GB like upstream. Speed p50 is 0.82-0.91 of balanced from 8 clients on; its c8 p95
is 1.08-1.11 of balanced (345 vs 312 ms JDBC, 339 vs 315 ADBC), at 16 % more q/s. Saturation (p95 < 100 ms) is 1 client
for all three.

**Open point, `load_report.py` q/s for balanced:** `load.md` gives balanced 41-47 q/s (JDBC c128 43, ADBC c128 43),
while the balanced `result.txt` rounds have 35.3-44.1 (c128 35.3-36.5). For speed (51-52) and upstream (54-56)
`load.md` and `result.txt` agree. `load.md` counts latency-CSV rows / 60 s; balanced's CSVs seem to hold more rows than
its 60 s window (the warm-up, when it is faster before its memory grows, is the likely cause). The artifacts are not
readable from this session, so not checked here; the main table uses `result.txt`, so speed/balanced at 128 clients
is 1.42 / 1.45 there and would be ~1.21 / 1.21 from `load.md`.

## Memory (server RSS peak, MB, median over rounds)

| job | B speed | A balanced | C upstream | speed / balanced | speed / upstream | balanced / upstream |
|---|---|---|---|---|---|---|
| TPC-H local | 1733 | 1591 | 357 (failed answers) | 1.09 | 4.85 | 4.46 |
| TPC-H S3 SF1 | 912 | 738 | 608 (failed answers) | 1.24 | 1.50 | 1.21 |
| TPC-H S3 SF10 ADBC | 3040 | 1589 | 988 (failed answers) | 1.91 | 3.08 | 1.61 |
| TPC-H S3 SF10 JDBC | 3066 | 1563 | 975 (failed answers) | 1.96 | 3.14 | 1.60 |
| small local | 757 | 1484 | 252 (died) | 0.51 | 3.00 | 5.89 |
| small S3 | 1388 | 2227 | 402 (died) | 0.62 | 3.45 | 5.54 |
| scan local | 1140 | 1236 | 3666 | 0.92 | 0.31 | 0.34 |
| scan S3 | 2967 | 1714 | 4009 | 1.73 | 0.74 | 0.43 |
| load local | 961 | 4491 | 923 | 0.21 | 1.04 | 4.87 |
| slow link | 1720 | 1549 | 607 (failed answers) | 1.11 | 2.83 | 2.55 |

Memory is within ±10 % of `413485ba80fd` in every job (load speed 961 vs 905 MB). Upstream's S3 scan RSS fell from 5946 to
4009 MB with the new commit.

## Upstream native `9e4787906b07` vs `6e264c10f403`

`6e264c10f403` was measured in `fresh-up-f06b5834e76e`, `fresh-up-25aa7eec0f0f` and `fresh-up-413485ba80fd` (run
41604206524, the numbers below). Different runs, so absolute values are indicative; same CPU type in both runs where
marked. The "ours balanced / upstream" column uses our balanced build in the same job as the yardstick (`413485ba80fd`
then, `deafc861cce3` now).

| metric | `6e264c10f403` (41604206524) | `9e4787906b07` (42223833724) | balanced / upstream then -> now | same CPU |
|---|---|---|---|---|
| TPC-H SF1/SF10 ADBC + JDBC, local + S3 | 0/22 ADBC, 1/22 JDBC | 0/22 ADBC, 1/22 JDBC (same md5) | n/a | - |
| small queries 1/8/32 | errors at every step, server died | errors at every step, server died | n/a | yes (9V45) |
| slow-link TPC-H SF10 (ZSTD) | 0/22 | 0/22 (`schema "tpch" does not exist`) | n/a | yes (7763) |
| scan local x1 / x4 (MB/s) | 417 / 545 | 528 / 673 | 1.04 / 0.80 -> 1.04 / 0.82 | yes (9V74) |
| scan local x8 | stream errors (2-3 per round, all rounds) | stream errors (3 and 2, in 2 rounds) | n/a | yes |
| scan local ADBC export (MB/s) | 521 | 650 | 0.98 -> 0.97 | yes |
| scan S3 x1 / x4 / x8 (MB/s) | 363 / 578 / errors in 1 round | 396 / 640 / 633, 0 errors | 1.02 / 0.75 -> 1.02 / 0.75 / 0.72 | no (7763 -> Xeon 8573C) |
| scan S3 ADBC export (MB/s) | 546 | 622 | 0.73 -> 0.68 | no |
| load JDBC q/s at 1 / 8 / 128 | 38.5 / 52.2 / 54.0 | 39.2 / 52.8 / 54.4 | 0.67 at 128 -> 0.67 | yes (7763) |
| load ADBC q/s at 1 / 8 / 128 | 45.4 / 55.7 / 55.5 | 45.5 / 55.7 / 54.9 | 0.62 at 128 -> 0.65 | yes |
| slow-link ZSTD export (MB/s) | 256.9 | 262.8 | 0.96 -> 0.97 | yes |
| peak RSS: scan local / scan S3 / load (MB) | 3746 / 5946 / 985 | 3666 / 4009 / 923 | - | - |
| peak RSS: TPC-H local / S3 SF10 ADBC / small S3 (MB) | 350 / 1027 / 357 | 357 / 988 / 402 | - | - |

On the same CPU type, local scans are 23-27 % faster in absolute terms, but our balanced build moved with it (same
balanced/upstream ratio), so that is the runner, not the upstream commit. Load and slow link are unchanged. The one
upstream change that shows is S3 scans: no x8 stream errors and 33 % less RSS (5946 -> 4009 MB). The correctness gate is
the same as before: the same answers fail, and the server still dies after small queries.

## vs `413485ba80fd` (previous fresh run)

Cross-run numbers come from different runners and are indicative only; the same-job ratios are the comparison.

| metric | `413485ba80fd` | `deafc861cce3` | change |
|---|---|---|---|
| local small c1 p50 speed / balanced, JDBC / ADBC | **1.18 / 1.19** | **1.10** / 1.08 | smaller, JDBC still > 5 % in all 3 rounds |
| local ADBC c8 p99 speed / balanced | **1.14** | 1.01 | gone |
| scan local speed / balanced x4 / x8 | 1.30 / 1.46 | 1.30 / 1.53 | same / +0.07 |
| scan S3 speed / balanced x4 / x8 | 1.33 / 1.41 | 1.49 / 1.58 | +0.16 / +0.17 |
| scan speed / upstream x4, S3 / local | 1.00 / 1.04 | 1.13 / 1.06 | above upstream native (new upstream commit) |
| S3 ADBC export speed / balanced, speed / upstream | 1.26, 0.92 | 1.35, 0.91 | +0.09, same |
| load at 128 clients speed / balanced, JDBC / ADBC | 1.41 / 1.48 | 1.42 / 1.45 | same |
| load speed / upstream at 128 clients, JDBC / ADBC | 0.94 / 0.92 | 0.95 / 0.94 | same |
| S3 TPC-H speed / balanced | 0.14-0.19 | 0.15-0.18 | same |
| S3 small p95 speed / balanced | 0.04-0.07 | 0.03-0.06 | same |
| slow-link ZSTD export speed / balanced, speed / upstream | 1.06, 1.02 | 1.00, 0.97 | -0.06, -0.05 |

## Verdict

- **Regression by the rule (>5 % slower in all 3 rounds), carried over from `413485ba80fd` but smaller: local small JDBC
  queries at 1 client, speed p50 1.10 of balanced (rounds 1.18 1.10 1.12; 15.5 -> 17.1 ms).** ADBC c1 p50 1.08 is no
  longer above 5 % in every round (1.17 1.08 1.02); c1 p95 / p99 are 0.74-0.98, and the `413485ba80fd` local ADBC c8 p99
  flag is gone (1.01). S3 c1 and local 8/32 clients are not affected (p50 0.83-0.98, c32 tails 0.67-0.84).
- Multi-stream scans under speed are a bit higher than in `413485ba80fd`: S3 x4/x8 1.49/1.58 of balanced, local
  1.30/1.53, in every round; speed is above upstream native `9e4787906b07` on S3 scans at every stream count
  (1.10-1.15) at 0.74 of its RSS, and level with it locally (x1 1.02, x4 1.06). S3 ADBC export 1.35 of balanced, 0.91 of
  upstream.
- Everything else as before: S3 TPC-H 5.5-7x faster (0.15-0.18), S3 small-query tails 17-33x lower, load +42-45 % at 128
  clients (0.94-0.95 of upstream native) at 0.21 of balanced RSS, local SF10 0.95-0.97, slow-link ZSTD export level with
  balanced (1.00) and 0.97 of upstream; 22/22 and 0 errors everywhere. The memory cost of speed is unchanged
  (S3 SF10/scan ~3.0 GB, 1.7-2.0x balanced).
- Load per step (`load.md`): speed's closed-loop c8 p95 is 1.08-1.11 of balanced at 16 % more q/s (p50 0.82-0.91 from 8
  clients on); `load.md` q/s for balanced disagrees with the client's own count (see "Open point"), the ratios here use
  the client count.
- Upstream native moved to `9e4787906b07` and still fails the TPC-H and small-query gate (its server dies after small);
  its local 8-stream scan still has stream errors, while its S3 x8 scan ran clean this time at 33 % less RSS; scans, load
  and slow link are otherwise unchanged against our balanced build (see the upstream section).
