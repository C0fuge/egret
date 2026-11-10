# Fresh upstream three-way: `37bf9401d77c` speed vs balanced vs upstream native

Task: `ci/BUILD-TRACK-TASK.md`, "FRESH UPSTREAM TRACKING". Pre-release `server-1.0.0-37bf9401d77c` (kestrel item 41:
hadoopfs afc6 + `hdfsSaslDataTransfer=auto`, HDFS only; item 40(a): `resourceProfile=speed` sizes the shared DuckDB
memory limit from a smaller JVM reservation, which touches the local/S3 path; balanced unchanged). Its HDFS acceptance
is [ACCEPT-37bf9401d77c](ACCEPT-37bf9401d77c.md) (checks 1-5 pass, check 6 needs a maintainer decision). Compare run
42791002963, wave [`fresh-up-37bf9401d77c`](../ci/waves/fresh-up-37bf9401d77c.json), 10 jobs, all green, 3 rounds
each, alternating order.

- A = `37bf9401d77c` default (balanced)
- B = `37bf9401d77c -DresourceProfile=speed`
- C = upstream native **`b7d32cf3b3f0ba71f79a7d3f425bbc0241eb6036`** (head of `feat/starrocks-native-integration` at
  dispatch; **new**: `FRESH-894afb9b48c4` measured `cec626bbb54a`)

Full tables: [run summary](fresh-up-37bf9401d77c-42791002963/summary.md),
[speed report](fresh-up-37bf9401d77c-42791002963/speed.md), per-step load
[load.md](fresh-up-37bf9401d77c-42791002963/load.md) (rereport 42810212730). Load q/s and the slow-link numbers come
from each round's `result.txt` as printed in the job logs (the client's own 60 s count). All three servers of a job run
on the same runner. Ratios: for times, < 1 = first faster; for MB/s and q/s, > 1 = first faster.

## Correctness

| workload | speed (B) | balanced (A) | upstream native (C) |
|---|---|---|---|
| TPC-H SF1 + SF10, ADBC + JDBC, local | 22/22 | 22/22 | **0/22 ADBC, 1/22 JDBC** (same md5 `813b233c6193` / `50bb2801381f` as `cec626bbb54a`) |
| TPC-H SF1 + SF10, ADBC + JDBC, S3 | 22/22 | 22/22 | **0/22 ADBC, 1/22 JDBC** |
| small queries 1/8/32 clients, local + S3 | 0 errors | 0 errors | **errors at most steps, server died after small** |
| slow link TPC-H SF10 ADBC (ZSTD) | 22/22 | 22/22 | **0/22** (`schema "tpch" does not exist`, decimal typing) |
| scans 1/4/8 + ADBC export, local | 0 errors | 0 errors | 0 errors (**new**: `cec626bbb54a` had x8 errors in every round) |
| scans 1/4/8 + ADBC export, S3 | 0 errors | 0 errors | **x8 stream errors in 2 rounds (2, 1)** |
| closed-loop load 1-128, local | 0 errors | 0 errors | 1 error (ADBC c128, connect) |

## Speed vs balanced vs upstream (medians over 3 rounds)

| area | metric | B speed | A balanced | C upstream | speed / balanced (rounds) | speed / upstream | balanced / upstream |
|---|---|---|---|---|---|---|---|
| TPC-H local | SF1 ADBC / JDBC (s) | 4.1 / 4.2 | 4.3 / 4.3 | n/a | 0.97 / 0.98 | n/a | n/a |
| TPC-H local | SF10 ADBC (s) | 40.4 | 41.6 | n/a | 0.97 (0.97 0.98 0.93) | n/a | n/a |
| TPC-H local | SF10 JDBC (s) | 40.8 | 41.3 | n/a | 0.99 (1.00 1.01 0.96) | n/a | n/a |
| TPC-H S3 | SF1 ADBC / JDBC (s) | 4.3 / 4.3 | 21.6 / 21.7 | n/a | **0.20 / 0.20** | n/a | n/a |
| TPC-H S3 | SF10 ADBC (s) | 41.6 | 294.4 | n/a | **0.14** (0.14 0.14 0.14) | n/a | n/a |
| TPC-H S3 | SF10 JDBC (s) | 36.8 | 233.8 | n/a | **0.16** (0.16 0.16 0.16) | n/a | n/a |
| small local | ADBC c1 / c8 / c32 p50 (ms) | 14.3 / 67.5 / 242 | 10.9 / 66.4 / 273 | n/a | **1.32** (1.08 1.33 1.26) / 1.02 / 0.89 | n/a | n/a |
| small local | ADBC c1 / c8 / c32 p95 (ms) | 28.8 / 178 / 706 | 31.1 / 182 / 859 | n/a | 0.93 / 0.98 / 0.82 | n/a | n/a |
| small local | ADBC c8 / c32 p99 (ms) | 214 / 857 | 231 / 1278 | n/a | 0.93 / 0.67 | n/a | n/a |
| small local | JDBC c1 / c8 / c32 p50 (ms) | 18.9 / 79.6 / 266 | 16.6 / 85.6 / 291 | n/a | **1.14** (1.15 1.14 1.13) / 0.93 / 0.91 | n/a | n/a |
| small local | JDBC c1 / c8 / c32 p95 (ms) | 34.5 / 181 / 762 | 33.7 / 193 / 857 | n/a | 1.02 / 0.94 / 0.89 | n/a | n/a |
| small S3 | ADBC c1 / c8 / c32 p50 (ms) | 15.1 / 65.3 / 214 | 26.9 / 352 / 1168 | n/a | 0.56 / 0.19 / 0.18 | n/a | n/a |
| small S3 | ADBC c1 / c8 / c32 p95 (ms) | 42.1 / 208 / 995 | 856 / 5865 / 17132 | n/a | **0.05 / 0.04 / 0.06** | n/a | n/a |
| small S3 | JDBC c1 / c8 / c32 p50 (ms) | 27.0 / 76.5 / 240 | 34.8 / 355 / 1064 | n/a | 0.78 / 0.22 / 0.23 | n/a | n/a |
| small S3 | JDBC c1 / c8 / c32 p95 (ms) | 47.7 / 233 / 1020 | 867 / 5833 / 18952 | n/a | **0.06 / 0.04 / 0.05** | n/a | n/a |
| scan local | x1 / x4 / x8 (MB/s) | 518 / 707 / 722 | 501 / 547 / 475 | 506 / 645 / 656 | 1.03 / 1.29 / **1.52** | 1.02 / 1.10 / 1.10 | 0.99 / 0.85 / 0.72 |
| scan local | ADBC export (MB/s) | 626 | 607 | 617 | 1.03 | 1.02 | 0.98 |
| scan S3 | x1 / x4 / x8 (MB/s) | 400 / 598 / 604 | 366 / 452 / 423 | 370 / 587 / n/a (errors) | 1.09 / **1.32** / **1.43** | 1.08 / 1.02 / n/a | 0.99 / 0.77 / n/a |
| scan S3 | ADBC export (MB/s) | 560 | 437 | 548 | 1.28 (1.41 1.28 1.28) | 1.02 | 0.80 |
| load local | JDBC q/s at 1 / 8 / 32 / 64 / 128 clients | 42.7 / 55.7 / 57.0 / 56.7 / 55.6 | 43.2 / 49.0 / 46.1 / 42.9 / 40.3 | 42.0 / 57.2 / 59.6 / 60.2 / 59.6 | 0.99 / 1.14 / 1.24 / 1.32 / **1.38** | 1.02 / 0.97 / 0.96 / 0.94 / 0.93 | 1.03 / 0.86 / 0.77 / 0.71 / 0.68 |
| load local | ADBC q/s at 1 / 8 / 32 / 64 / 128 clients | 45.1 / 56.5 / 57.4 / 56.7 / 55.6 | 46.2 / 48.9 / 44.4 / 42.4 / 39.6 | 48.6 / 61.8 / 61.1 / 60.2 / 59.4 | 0.98 / 1.16 / 1.29 / 1.34 / **1.40** | 0.93 / 0.91 / 0.94 / 0.94 / 0.94 | 0.95 / 0.79 / 0.73 / 0.70 / 0.67 |
| load local | saturation (best median q/s) | 57.4 (ADBC c32) | 49.0 (JDBC c8) | 61.8 (ADBC c8) | 1.17 | 0.93 | 0.79 |
| slow link (10 ms, 1 Gbit), ZSTD | ADBC export (MB/s) | 322.6 | 326.0 | 320.8 | 0.99 (0.99 0.94 1.02) | 1.01 | 1.02 |
| slow link (10 ms, 1 Gbit), ZSTD | TPC-H SF10 ADBC (s, median sum) | 33.1 | 34.3 | n/a | 0.96 (0.99 0.96 0.95) | n/a | n/a |

Load per round, speed / balanced at 128 clients: JDBC 1.40 1.38 1.34, ADBC 1.45 1.40 1.38. The load job ran on a Xeon
8573C runner (`894afb9b48c4`: EPYC 9V45), so absolute q/s are ~35 % lower than there; the same-job ratios are the
comparison. The slow-link job ran on an EPYC 9V74 runner and reached 320-326 MB/s on all three servers (254-258 in
`894afb9b48c4`). Upstream ratios on scans, export, load, slow-link export and memory only; TPC-H and small queries fail
its gate. S3 small JDBC c8 p99 under speed is 2427 ms (rounds 0.38 0.05 0.43 of balanced; ADBC c8 p99 305 ms): a
tail spike in 2 of 3 rounds, still below balanced.

## Load per step (`ci/load_report.py`, [load.md](fresh-up-37bf9401d77c-42791002963/load.md))

QPS / p50 / p95 ms / server CPU % / server memory MiB (docker stats max in the step), medians over rounds.

| clients | JDBC speed | JDBC balanced | JDBC upstream | ADBC speed | ADBC balanced | ADBC upstream |
|---|---|---|---|---|---|---|
| 1 | 43 / 19.2 / 40.9, 167 %, 484 | 43 / 19.2 / 40.9, 166 %, 555 | 42 / 19.7 / 42.6, 158 %, 413 | 45 / 18.4 / 35.6, 164 %, 470 | 46 / 18.3 / 35.1, 164 %, 477 | 49 / 16.8 / 32.5, 164 %, 394 |
| 8 | 56 / 136 / 311, 200 %, 581 | 52 / 149 / 283, 200 %, 834 | 57 / 125 / 288, 200 %, 440 | 57 / 135 / 299, 195 %, 595 | 52 / 150 / 276, 196 %, 870 | 62 / 115 / 267, 192 %, 439 |
| 32 | 57 / 490 / 1137, 193 %, 690 | 51 / 576 / 1137, 195 %, 1726 | 60 / 455 / 1050, 202 %, 592 | 57 / 486 / 1129, 201 %, 686 | 51 / 587 / 1158, 200 %, 1880 | 61 / 444 / 1038, 194 %, 649 |
| 64 | 57 / 1072 / 2229, 190 %, 799 | 50 / 1237 / 2399, 191 %, 2597 | 60 / 968 / 2145, 182 %, 799 | 57 / 1082 / 2202, 201 %, 815 | 49 / 1240 / 2381, 200 %, 3034 | 60 / 967 / 2161, 191 %, 809 |
| 128 | 56 / 2097 / 4841, 192 %, 920 | 47 / 2501 / 5238, 191 %, 4255 | 60 / 1952 / 4558, 201 %, 943 | 56 / 2096 / 4813, 201 %, 984 | 47 / 2521 / 5248, 199 %, 4919 | 59 / 1916 / 4586, 189 %, 993 |

All three run at the 2-CPU limit from 8 clients on. Speed p50 is 0.83-0.92 of balanced from 8 clients on; balanced's
memory grows to 4.3-4.9 GB at 128 clients, speed stays under 1 GB like upstream. Saturation (p95 < 100 ms) is 1 client
for all three. The `FRESH-deafc861cce3` open point does not show this time: `load.md` q/s for balanced (47-52 from 8
clients) is within 1-6 q/s of the client's own count (40-49), speed and upstream agree within 1 q/s. The main table
uses the client count. As in `894afb9b48c4`, the c1 load mix (point lookups, count_filter) has no speed penalty at 1
client (q/s 0.98-0.99, p50 equal): the c1 regression is in small-query classes outside the load mix.

## Memory (server RSS peak, MB, median over rounds)

| job | B speed | A balanced | C upstream | speed / balanced | speed / upstream | balanced / upstream | speed vs `894afb9b48c4` |
|---|---|---|---|---|---|---|---|
| TPC-H local | 1882 | 1617 | 348 (failed answers) | 1.16 | 5.41 | 4.65 | 1891 (same) |
| TPC-H S3 SF1 | 994 | 769 | 609 (failed answers) | 1.29 | 1.63 | 1.26 | 1002 (same) |
| TPC-H S3 SF10 ADBC | 3472 | 1667 | 1030 (failed answers) | 2.08 | 3.37 | 1.62 | 3043 (**+14 %**) |
| TPC-H S3 SF10 JDBC | 3378 | 1614 | 996 (failed answers) | 2.09 | 3.39 | 1.62 | 3179 (+6 %) |
| small local | 840 | 1555 | 252 (died) | 0.54 | 3.33 | 6.17 | 794 (+6 %) |
| small S3 | 1523 | 2270 | 394 (died) | 0.67 | 3.87 | 5.76 | 1448 (+5 %) |
| scan local | 1168 | 1128 | 1800 | 1.04 | 0.65 | 0.63 | 1180 (same) |
| scan S3 | 3305 | 1762 | 5892 | 1.88 | 0.56 | 0.30 | 3064 (+8 %) |
| load local | 936 | 4926 | 945 | 0.19 | 0.99 | 5.21 | 1053 (-11 %) |
| slow link | 1798 | 1545 | 605 (failed answers) | 1.16 | 2.97 | 2.55 | 1782 (same) |

Item 40(a) shows on S3 only: speed's RSS on S3 SF10 and S3 scans is 6-14 % higher than in `894afb9b48c4` (2.08-2.09x
balanced, was 1.89-1.93x), with S3 SF10 ADBC 0.14 of balanced (was 0.17) and S3 scans x4/x8 1.32/1.43 (was 1.84/1.64,
different runner: balanced 452 vs 390 MB/s at x4 there). Balanced memory is within 10 % of `894afb9b48c4` in every
job. No job came near the 6 GiB limit for our builds; upstream's S3 scan reached 5892 MB.

## Upstream native `b7d32cf3b3f0` vs `cec626bbb54a`

`cec626bbb54a` was measured in `fresh-up-894afb9b48c4` (run 42775953599). Different runs; "same CPU" marks jobs on the
same CPU type in both runs. "balanced / upstream" uses our balanced build in the same job as the yardstick.

| metric | `cec626bbb54a` (42775953599) | `b7d32cf3b3f0` (42791002963) | balanced / upstream then -> now | same CPU |
|---|---|---|---|---|
| TPC-H SF1/SF10 ADBC + JDBC, local + S3 | 0/22 ADBC, 1/22 JDBC | 0/22 ADBC, 1/22 JDBC (same md5) | n/a | - |
| small queries 1/8/32 | errors, server died | errors, server died | n/a | local yes (9V45) |
| slow-link TPC-H SF10 (ZSTD) | 0/22 | 0/22 | n/a | no (7763 -> 9V74) |
| scan local x1 / x4 / x8 (MB/s) | 536 / 684 / errors in 3 rounds | 506 / 645 / **656, 0 errors** | 1.03 / 0.83 / n/a -> 0.99 / 0.85 / 0.72 | no (9V74 -> 8573C) |
| scan local ADBC export (MB/s) | 662 | 617 | 0.98 -> 0.98 | no |
| scan S3 x1 / x4 / x8 (MB/s) | 310 / 669 / errors in 3 rounds | 370 / 587 / errors in 2 rounds (2, 1) | 1.05 / 0.58 / n/a -> 0.99 / 0.77 / n/a | no (9V74 -> 7763) |
| scan S3 ADBC export (MB/s) | 647 | 548 | 0.46 -> 0.80 | no |
| load JDBC / ADBC q/s at 128 | 85.4 / 85.3 | 59.6 / 59.4 | 0.63 / 0.64 -> 0.68 / 0.67 | no (9V45 -> 8573C) |
| slow-link ZSTD export (MB/s) | 258.0 | 320.8 | 0.98 -> 1.02 | no |
| peak RSS: scan local / scan S3 / load (MB) | 3680 / 5950 / 1031 | **1800** / 5892 / 945 | - | - |
| peak RSS: TPC-H local / S3 SF10 ADBC / small S3 (MB) | 351 / 978 / 401 | 348 / 1030 / 394 | - | - |

Same gate failures. Two changes show: local x8 scans no longer have stream errors (S3 still in 2 of 3 rounds), and the
local scan RSS halved (3680 -> 1800 MB). Every other job is on a different CPU type than in the last run, so the
absolute numbers are not comparable; against our balanced build in the same job nothing moved beyond the runner noise.

## vs `894afb9b48c4` (previous fresh run)

Cross-run numbers come from different runners and are indicative only; the same-job ratios are the comparison.

| metric | `894afb9b48c4` | `37bf9401d77c` | change |
|---|---|---|---|
| local small c1 p50 speed / balanced, JDBC / ADBC (both 9V45) | **1.19 / 1.28** | **1.14 / 1.32** | still > 5 % in all 3 rounds; JDBC a bit lower, ADBC a bit higher |
| local small c1 p50 absolute, speed JDBC / ADBC (ms) | 18.4 / 13.2 | 18.9 / 14.3 | speed slower; balanced 15.4 / 10.3 -> 16.6 / 10.9 |
| local small c32 p95 speed / balanced, JDBC / ADBC | 0.87 / 0.81 | 0.89 / 0.82 | same |
| scan local speed / balanced x4 / x8 | 1.30 / 1.52 | 1.29 / 1.52 | same |
| scan S3 speed / balanced x4 / x8 | 1.84 / 1.64 | 1.32 / 1.43 | lower (runner change; balanced higher here) |
| S3 ADBC export speed / balanced, speed / upstream | 1.33, 0.62 | 1.28, 1.02 | same / upstream lower on this runner |
| load at 128 clients speed / balanced, JDBC / ADBC | 1.49 / 1.51 | 1.38 / 1.40 | lower (runner change: 8573C vs 9V45) |
| load speed / upstream at 128 clients, JDBC / ADBC | 0.94 / 0.97 | 0.93 / 0.94 | same |
| S3 TPC-H speed / balanced | 0.16-0.19 | 0.14-0.20 | same |
| S3 small p95 speed / balanced | 0.05-0.13 | 0.04-0.06 | same or lower |
| slow-link ZSTD export speed / balanced, speed / upstream | 1.01, 0.99 | 0.99, 1.01 | same |
| speed RSS S3 SF10 / S3 scans (MB) | 3043-3179 / 3064 | 3378-3472 / 3305 | **+6-14 %** (item 40(a)) |

## Verdict

- **Regression by the rule (>5 % slower in all 3 rounds), carried over from `894afb9b48c4`: local small queries at 1
  client, speed p50 1.14 of balanced over JDBC (rounds 1.15 1.14 1.13; 16.6 -> 18.9 ms) and 1.32 over ADBC (1.08 1.33
  1.26; 10.9 -> 14.3 ms),** same CPU type (EPYC 9V45) as the last two runs (`deafc861cce3` 1.10 / 1.08,
  `894afb9b48c4` 1.19 / 1.28). c1 p95/p99 0.93-1.05, local 8/32 clients 0.67-1.02, S3 c1 0.56 / 0.78. Item 40(a)
  does not fix it; it is a fixed per-query cost of speed on local data at low concurrency.
- Item 40(a) (speed DuckDB memory sizing): speed's RSS on S3 SF10 and S3 scans is 6-14 % higher than in
  `894afb9b48c4` (3.3-3.5 GB, 2.1x balanced, still well under the 6 GiB limit); S3 SF10 ADBC 0.14 of balanced (was
  0.17). Other jobs within +-6 % (load -11 %).
- Everything else as before: S3 TPC-H 5-7x faster (0.14-0.20), S3 small-query tails at 1/8/32 clients 16-25x lower
  (0.04-0.06), load +38-40 % at 128 clients (0.93-0.94 of upstream native) at 0.19 of balanced RSS, local TPC-H
  0.97-0.99, scans x4/x8 1.29-1.52 of balanced (local x4/x8 1.10 of upstream native), slow-link ZSTD export 0.99 of
  balanced and 1.01 of upstream; 22/22 and 0 errors everywhere.
- Upstream native moved to `b7d32cf3b3f0`: same gate failures (TPC-H, small, server dies after small); local x8 scans
  are clean again and its local scan RSS halved (1800 MB); S3 x8 still has stream errors in 2 of 3 rounds.
