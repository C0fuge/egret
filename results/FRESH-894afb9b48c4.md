# Fresh upstream three-way: `894afb9b48c4` speed vs balanced vs upstream native

Task: `ci/BUILD-TRACK-TASK.md`, "FRESH UPSTREAM TRACKING". Pre-release `server-1.0.0-894afb9b48c4` (kestrel item 39:
hadoopfs afc4 / `hdfsMetadataCacheTtlMs`, (b) cgroup-aware sizing, (c) file-stats pruning; the last two touch the
local/S3 path; its HDFS acceptance is [ACCEPT-894afb9b48c4](ACCEPT-894afb9b48c4.md), SHIP). Compare run 42775953599,
wave [`fresh-up-894afb9b48c4`](../ci/waves/fresh-up-894afb9b48c4.json), 10 jobs, all green, 3 rounds each, alternating
order.

- A = `894afb9b48c4` default (balanced)
- B = `894afb9b48c4 -DresourceProfile=speed`
- C = upstream native **`cec626bbb54aabb64d9e4a12beca40b7fbfa3fa6`** (head of `feat/starrocks-native-integration` at
  dispatch; **new**: `FRESH-deafc861cce3` measured `9e4787906b07`)

Full tables: [run summary](fresh-up-894afb9b48c4-42775953599/summary.md),
[speed report](fresh-up-894afb9b48c4-42775953599/speed.md). Load q/s and the slow-link numbers are not in the run
summary; they come from each round's `result.txt` as printed in the job logs (the client's own 60 s count, as in
`FRESH-deafc861cce3`). All three servers of a job run on the same runner. Ratios: for times, < 1 = first faster; for
MB/s and q/s, > 1 = first faster.

## Correctness

| workload | speed (B) | balanced (A) | upstream native (C) |
|---|---|---|---|
| TPC-H SF1 + SF10, ADBC + JDBC, local | 22/22 | 22/22 | **0/22 ADBC, 1/22 JDBC** (same md5 as `9e4787906b07`) |
| TPC-H SF1 + SF10, ADBC + JDBC, S3 | 22/22 | 22/22 | **0/22 ADBC, 1/22 JDBC** |
| small queries 1/8/32 clients, local + S3 | 0 errors | 0 errors | **errors at most steps, server died after small** (OOM-killed in 3 of 15 rounds per storage) |
| slow link TPC-H SF10 ADBC (ZSTD) | 22/22 | 22/22 | **0/22** (`schema "tpch" does not exist`, decimal typing) |
| scans 1/4/8 + ADBC export, local + S3 | 0 errors | 0 errors | **x8 stream errors in every round, local (5, 3, 2) and S3 (2, 2, 1)** |
| closed-loop load 1-128, local | 0 errors | 0 errors | 1 error (ADBC c128, round 1) |

## Speed vs balanced vs upstream (medians over 3 rounds)

| area | metric | B speed | A balanced | C upstream | speed / balanced (rounds) | speed / upstream | balanced / upstream |
|---|---|---|---|---|---|---|---|
| TPC-H local | SF1 ADBC / JDBC (s) | 4.1 / 4.2 | 4.1 / 4.1 | n/a | 0.99 / 1.01 | n/a | n/a |
| TPC-H local | SF10 ADBC (s) | 39.4 | 40.3 | n/a | 0.98 (0.98 0.98 0.98) | n/a | n/a |
| TPC-H local | SF10 JDBC (s) | 39.5 | 40.8 | n/a | 0.97 (0.97 0.97 0.96) | n/a | n/a |
| TPC-H S3 | SF1 ADBC / JDBC (s) | 4.2 / 4.2 | 26.2 / 26.0 | n/a | **0.16 / 0.16** | n/a | n/a |
| TPC-H S3 | SF10 ADBC (s) | 45.9 | 264.5 | n/a | **0.17** (0.17 0.17 0.18) | n/a | n/a |
| TPC-H S3 | SF10 JDBC (s) | 54.0 | 288.4 | n/a | **0.19** (0.18 0.20 0.19) | n/a | n/a |
| small local | ADBC c1 / c8 / c32 p50 (ms) | 13.2 / 62.7 / 231 | 10.3 / 65.1 / 272 | n/a | **1.28** (1.34 1.20 1.36) / 0.96 / 0.85 | n/a | n/a |
| small local | ADBC c1 / c8 / c32 p95 (ms) | 31.0 / 173 / 696 | 30.2 / 176 / 854 | n/a | 1.03 / 0.98 / 0.81 | n/a | n/a |
| small local | ADBC c8 / c32 p99 (ms) | 215 / 827 | 225 / 1140 | n/a | 0.96 / 0.73 | n/a | n/a |
| small local | JDBC c1 / c8 / c32 p50 (ms) | 18.4 / 75.2 / 256 | 15.4 / 76.6 / 291 | n/a | **1.19** (1.28 1.12 1.19) / 0.98 / 0.88 | n/a | n/a |
| small local | JDBC c1 / c8 / c32 p95 (ms) | 31.9 / 183 / 718 | 31.2 / 187 / 829 | n/a | 1.02 / 0.98 / 0.87 | n/a | n/a |
| small S3 | ADBC c1 / c8 / c32 p50 (ms) | 13.0 / 54.6 / 181 | 24.5 / 253 / 898 | n/a | 0.53 / 0.22 / 0.20 | n/a | n/a |
| small S3 | ADBC c1 / c8 / c32 p95 (ms) | 33.9 / 167 / 794 | 579 / 3529 / 12100 | n/a | **0.06 / 0.05 / 0.07** | n/a | n/a |
| small S3 | JDBC c1 / c8 / c32 p50 (ms) | 27.1 / 76.2 / 217 | 33.0 / 260 / 956 | n/a | 0.82 / 0.29 / 0.23 | n/a | n/a |
| small S3 | JDBC c1 / c8 / c32 p95 (ms) | 74.4 / 188 / 793 | 582 / 3560 / 12810 | n/a | **0.13 / 0.05 / 0.06** | n/a | n/a |
| scan local | x1 / x4 / x8 (MB/s) | 552 / 734 / 740 | 552 / 566 / 488 | 536 / 684 / n/a (errors) | 1.00 / 1.30 / **1.52** | 1.03 / 1.07 / n/a | 1.03 / 0.83 / n/a |
| scan local | ADBC export (MB/s) | 658 | 650 | 662 | 1.01 | 0.99 | 0.98 |
| scan S3 | x1 / x4 / x8 (MB/s) | 367 / 719 / 692 | 327 / 390 / 421 | 310 / 669 / n/a (errors) | 1.12 / **1.84** / **1.64** | 1.18 / 1.07 / n/a | 1.05 / 0.58 / n/a |
| scan S3 | ADBC export (MB/s) | 401 | 301 | 647 | 1.33 (2.00 1.04 1.33) | **0.62** (0.92 0.62 0.61) | 0.46 |
| load local | JDBC q/s at 1 / 8 / 32 / 64 / 128 clients | 65.0 / 84.2 / 84.2 / 84.4 / 80.6 | 63.5 / 69.2 / 64.1 / 59.0 / 54.1 | 64.5 / 86.9 / 89.0 / 90.9 / 85.4 | 1.02 / 1.22 / 1.31 / 1.43 / **1.49** | 1.01 / 0.97 / 0.95 / 0.93 / 0.94 | 0.98 / 0.80 / 0.72 / 0.65 / 0.63 |
| load local | ADBC q/s at 1 / 8 / 32 / 64 / 128 clients | 71.0 / 86.5 / 85.2 / 83.7 / 82.6 | 66.4 / 72.0 / 60.4 / 58.1 / 54.6 | 75.0 / 89.2 / 90.7 / 91.1 / 85.3 | 1.07 / 1.20 / 1.41 / 1.44 / **1.51** | 0.95 / 0.97 / 0.94 / 0.92 / 0.97 | 0.89 / 0.81 / 0.67 / 0.64 / 0.64 |
| load local | saturation (best median q/s) | 86.5 (ADBC c8) | 72.0 (ADBC c8) | 91.1 (ADBC c64) | 1.20 | 0.95 | 0.79 |
| slow link (10 ms, 1 Gbit), ZSTD | ADBC export (MB/s) | 254.3 | 252.2 | 258.0 | 1.01 (1.01 1.08 0.94) | 0.99 | 0.98 |
| slow link (10 ms, 1 Gbit), ZSTD | TPC-H SF10 ADBC (s, median sum) | 41.9 | 43.0 | n/a | 0.97 (0.98 0.99 0.96) | n/a | n/a |

Load per round, speed / balanced at 128 clients: JDBC 1.56 1.50 1.40, ADBC 1.51 1.46 1.50. The load job ran on an EPYC
9V45 runner (deafc861cce3: 7763), so absolute q/s are ~60 % higher than in `FRESH-deafc861cce3`; the same-job ratios
are the comparison. Upstream ratios on scans x1/x4, export, load and memory only; TPC-H and small queries fail its
gate, and its x8 scans now have stream errors on local and S3.

## Load per step (`ci/load_report.py`, rereport 42793745922: [load.md](fresh-up-894afb9b48c4-42775953599/load.md))

p50 / p95 ms, server CPU % and server memory MiB (docker stats max in the step), medians over rounds.

| clients | JDBC speed | JDBC balanced | JDBC upstream | ADBC speed | ADBC balanced | ADBC upstream |
|---|---|---|---|---|---|---|
| 1 | 12.9 / 26.3, 167 %, 476 | 13.0 / 26.3, 167 %, 482 | 13.0 / 27.2, 161 %, 420 | 12.2 / 22.6, 165 %, 452 | 12.3 / 23.1, 165 %, 478 | 11.1 / 21.6, 167 %, 399 |
| 8 | 91.5 / 190, 188 %, 561 | 103 / 186, 183 %, 858 | 84.2 / 183, 187 %, 520 | 89.2 / 186, 198 %, 547 | 103 / 185, 200 %, 971 | 81.2 / 179, 202 %, 509 |
| 32 | 336 / 745, 202 %, 670 | 403 / 813, 197 %, 1862 | 312 / 706, 203 %, 639 | 342 / 728, 201 %, 655 | 411 / 847, 199 %, 1933 | 307 / 706, 201 %, 663 |
| 64 | 691 / 1538, 200 %, 758 | 840 / 1739, 199 %, 2917 | 625 / 1454, 198 %, 824 | 707 / 1538, 195 %, 797 | 860 / 1802, 200 %, 3239 | 630 / 1466, 204 %, 881 |
| 128 | 1426 / 3475, 186 %, 978 | 1715 / 3909, 188 %, 4605 | 1335 / 3289, 193 %, 960 | 1370 / 3474, 198 %, 982 | 1762 / 3915, 195 %, 5341 | 1324 / 3316, 203 %, 970 |

All three run at the 2-CPU limit from 8 clients on. Speed p50 is 0.78-0.89 of balanced from 8 clients on and its p95
0.89-1.02; balanced's memory grows to 4.6-5.3 GB at 128 clients, speed stays under 1 GB like upstream. Saturation
(p95 < 100 ms) is 1 client for all three. The `FRESH-deafc861cce3` open point repeats: `load.md` q/s for balanced
(67-77 from 8 clients) is above the client's own 60 s count (54-72); speed and upstream agree within 1-3 q/s. The main
table uses the client count. The c1 load mix (point lookups and count_filter, 0 errors) shows no speed penalty at 1
client (p50 0.99-1.00), unlike the small-query set: the c1 regression is in classes outside the load mix.

## Memory (server RSS peak, MB, median over rounds)

| job | B speed | A balanced | C upstream | speed / balanced | speed / upstream | balanced / upstream |
|---|---|---|---|---|---|---|
| TPC-H local | 1891 | 1650 | 351 (failed answers) | 1.15 | 5.39 | 4.70 |
| TPC-H S3 SF1 | 1002 | 776 | 626 (failed answers) | 1.29 | 1.60 | 1.24 |
| TPC-H S3 SF10 ADBC | 3043 | 1614 | 978 (failed answers) | 1.89 | 3.11 | 1.65 |
| TPC-H S3 SF10 JDBC | 3179 | 1649 | 982 (failed answers) | 1.93 | 3.24 | 1.68 |
| small local | 794 | 1552 | 254 (died) | 0.51 | 3.13 | 6.11 |
| small S3 | 1448 | 2270 | 401 (died) | 0.64 | 3.61 | 5.66 |
| scan local | 1180 | 1234 | 3680 | 0.96 | 0.32 | 0.34 |
| scan S3 | 3064 | 1703 | 5950 | 1.80 | 0.51 | 0.29 |
| load local | 1053 | 5335 | 1031 | 0.20 | 1.02 | 5.17 |
| slow link | 1782 | 1613 | 640 (failed answers) | 1.10 | 2.78 | 2.52 |

Within +-10 % of `deafc861cce3` in every job except balanced load (5335 vs 4491 MB, higher q/s on the faster runner)
and TPC-H local speed (1891 vs 1733 MB, +9 %). Upstream's S3 scan RSS is back at 5950 MB (`9e4787906b07`: 4009); its
container hit the 6 GiB limit (OOM-killed in 3 of 15 rounds on local and on S3, all in the small-query set).

## Upstream native `cec626bbb54a` vs `9e4787906b07`

`9e4787906b07` was measured in `fresh-up-deafc861cce3` (run 42223833724). Different runs; "same CPU" marks jobs on the
same CPU type in both runs. "balanced / upstream" uses our balanced build in the same job as the yardstick.

| metric | `9e4787906b07` (42223833724) | `cec626bbb54a` (42775953599) | balanced / upstream then -> now | same CPU |
|---|---|---|---|---|
| TPC-H SF1/SF10 ADBC + JDBC, local + S3 | 0/22 ADBC, 1/22 JDBC | 0/22 ADBC, 1/22 JDBC (same md5 `813b233c6193` / `50bb2801381f`) | n/a | - |
| small queries 1/8/32 | errors at every step, server died | errors, server died (OOM-killed 3/15 rounds) | n/a | local yes (9V45) |
| slow-link TPC-H SF10 (ZSTD) | 0/22 | 0/22 | n/a | yes (7763) |
| scan local x1 / x4 (MB/s) | 528 / 673 | 536 / 684 | 1.04 / 0.82 -> 1.03 / 0.83 | yes (9V74) |
| scan local x8 | stream errors in 2 rounds (3, 2) | stream errors in 3 rounds (5, 3, 2) | n/a | yes |
| scan local ADBC export (MB/s) | 650 | 662 | 0.97 -> 0.98 | yes |
| scan S3 x1 / x4 / x8 (MB/s) | 396 / 640 / 633, 0 errors | 310 / 669 / **stream errors in 3 rounds (2, 2, 1)** | 1.02 / 0.75 / 0.72 -> 1.05 / 0.58 / n/a | no (8573C -> 9V74) |
| scan S3 ADBC export (MB/s) | 622 | 647 | 0.68 -> 0.46 | no |
| load JDBC q/s at 1 / 8 / 128 | 39.2 / 52.8 / 54.4 | 64.5 / 86.9 / 85.4 | 0.67 at 128 -> 0.63 | no (7763 -> 9V45) |
| load ADBC q/s at 1 / 8 / 128 | 45.5 / 55.7 / 54.9 | 75.0 / 89.2 / 85.3 | 0.65 at 128 -> 0.64 | no |
| slow-link ZSTD export (MB/s) | 262.8 | 258.0 | 0.97 -> 0.98 | yes |
| peak RSS: scan local / scan S3 / load (MB) | 3666 / 4009 / 923 | 3680 / 5950 / 1031 | - | - |
| peak RSS: TPC-H local / S3 SF10 ADBC / small S3 (MB) | 357 / 988 / 402 | 351 / 978 / 401 | - | - |

The correctness gate is unchanged (same failed answers, server dies after small). Against our balanced build, local
scans, export, load and slow link are unchanged. The one change that shows is on S3: the x8 stream errors are back (as
with `6e264c10f403`), and so is the ~5.9 GB scan RSS. The S3 runner changed CPU type, so this may be partly the runner.

## vs `deafc861cce3` (previous fresh run)

Cross-run numbers come from different runners and are indicative only; the same-job ratios are the comparison.

| metric | `deafc861cce3` | `894afb9b48c4` | change |
|---|---|---|---|
| local small c1 p50 speed / balanced, JDBC / ADBC (both 9V45) | **1.10** / 1.08 | **1.19 / 1.28** | **larger again, both > 5 % in all 3 rounds** |
| local small c1 p50 absolute, speed JDBC / ADBC (ms) | 17.1 / 11.9 | 18.4 / 13.2 | speed slower; balanced 15.5 / 11.1 -> 15.4 / 10.3 |
| local small c32 p95 speed / balanced, JDBC / ADBC | 0.84 / 0.78 | 0.87 / 0.81 | same |
| scan local speed / balanced x4 / x8 | 1.30 / 1.53 | 1.30 / 1.52 | same |
| scan S3 speed / balanced x4 / x8 | 1.49 / 1.58 | 1.84 / 1.64 | higher (balanced lower on this runner: 390 vs 482 at x4) |
| S3 ADBC export speed / balanced, speed / upstream | 1.35, 0.91 | 1.33, 0.62 | same, upstream higher on this runner |
| load at 128 clients speed / balanced, JDBC / ADBC | 1.42 / 1.45 | 1.49 / 1.51 | +0.07 / +0.06 |
| load speed / upstream at 128 clients, JDBC / ADBC | 0.95 / 0.94 | 0.94 / 0.97 | same |
| S3 TPC-H speed / balanced | 0.15-0.18 | 0.16-0.19 | same |
| S3 small p95 speed / balanced | 0.03-0.06 | 0.05-0.13 | same at 8/32 clients; c1 JDBC 0.13 (was 0.06) |
| slow-link ZSTD export speed / balanced, speed / upstream | 1.00, 0.97 | 1.01, 0.99 | same |

## Verdict

- **Regression by the rule (>5 % slower in all 3 rounds), larger than in `deafc861cce3`: local small queries at 1
  client, speed p50 1.19 of balanced over JDBC (rounds 1.28 1.12 1.19; 15.4 -> 18.4 ms) and 1.28 over ADBC (1.34 1.20
  1.36; 10.3 -> 13.2 ms).** Both runs are on the same CPU type (EPYC 9V45); `deafc861cce3` had 1.10 / 1.08. c1 p95 /
  p99 are 0.94-1.03, local 8/32 clients are 0.73-0.98 and S3 c1 is 0.53 / 0.82, so this is a fixed per-query cost of
  speed on local data at low concurrency. Item 39 (b) (cgroup-aware sizing) is the likely cause (the runtime change on this path
  named in the Log since `deafc861cce3`; not bisected). Balanced c1 got a bit faster (11.1 -> 10.3 ms ADBC), speed slower (11.9 -> 13.2).
- Everything else as before or better: S3 TPC-H 5-6x faster (0.16-0.19), S3 small-query tails at 8/32 clients 14-20x
  lower (0.05-0.07), load +49-51 % at 128 clients (0.94-0.97 of upstream native) at 0.20 of balanced RSS, local SF10
  0.97-0.98, scans x4/x8 1.30-1.84 of balanced (S3 x1 / x4 above upstream native at 1.18 / 1.07), slow-link ZSTD
  export 1.01 of balanced and 0.99 of upstream; 22/22 and 0 errors everywhere. The memory cost of speed is unchanged
  (S3 SF10/scan ~3.0-3.2 GB, 1.8-1.9x balanced).
- S3 ADBC export under speed is 0.62 of upstream native (was 0.91): upstream reached 647 MB/s on this runner, our
  builds 301 (balanced) / 401 (speed); speed / balanced 1.33 as before. Noisy (speed / balanced rounds 2.00 1.04 1.33).
- Upstream native moved to `cec626bbb54a`: same gate failures (TPC-H, small, server dies, OOM-killed in 3 of 15 rounds);
  its x8 scans now have stream errors on S3 too (every round), and its S3 scan RSS is back at ~5.9 GB.
