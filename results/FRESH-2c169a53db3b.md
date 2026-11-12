# Fresh upstream three-way: `2c169a53db3b` speed vs balanced vs upstream native

Task: `ci/BUILD-TRACK-TASK.md`, "FRESH UPSTREAM TRACKING" (build `server-1.0.0-2c169a53db3b`: kestrel item 47
(catalogs), item 48 (distributed-complete filtered one-row aggregates over <= 4 pruned files computed locally), Q3
(default `arrowAllocatorLimitBytes` = 75 % of direct memory, at least 256 MiB) and Q-40b-1 (file pruning off by default
for a local dataDir)). Its HDFS acceptance is [ACCEPT-2c169a53db3b](ACCEPT-2c169a53db3b.md) (SHIP, run 43175547634).
Compare run 43175544843, wave [`fresh-up-2c169a53db3b`](../ci/waves/fresh-up-2c169a53db3b.json), 10 jobs, all green,
3 rounds each, alternating order; per-step load via rereport 43194955428.

- A = `2c169a53db3b` default (balanced)
- B = `2c169a53db3b -DresourceProfile=speed`
- C = upstream native **`cfaa929746cbf9ba9f6134cbf0c5a9683b2c1e92`** (head of `feat/starrocks-native-integration` at
  dispatch 07:28 UTC; the same commit as `FRESH-74464701e372`)

Full tables: [run summary](fresh-up-2c169a53db3b-43175544843/summary.md),
[speed report](fresh-up-2c169a53db3b-43175544843/speed.md), [load.md](fresh-up-2c169a53db3b-43175544843/load.md).
Load q/s and the slow-link numbers come from each round's `result.txt` in the job logs (the client's own 60 s count).
All three servers of a job run on the same runner. Ratios: for times, < 1 = first faster; for MB/s and q/s, > 1 =
first faster.

## What the new items touch here

Items 48 and Q3 are on the distributed-complete / direct-memory paths (covered by ACCEPT checks 3 and 5, both pass);
item 47 is catalogs. Q-40b-1 is the one change on this wave's local path: file pruning is off by default for a local
dataDir. On the same CPU type as `74464701e372` (EPYC 9V74) local TPC-H answers are 22/22 for both profiles;
balanced SF10 34.6 / 34.8 s ADBC / JDBC (74464701e372: 34.3 / 33.8), speed 34.2 / 34.3 s (32.7 / 32.8, **+5 % across
runs**), SF1 unchanged (3.4 s). Within this job speed/balanced is 0.99 / 0.99 (was 0.96 / 0.97); not a regression by
the rule (the rule compares within a job, and speed is not slower than balanced here), but the speed SF10 local time
is up across runs and is consistent with pruning being off. No per-query local times for our builds are in
`speed-queries.csv` (only up-native rows), so it cannot be pinned to single queries from this run.

## Correctness

| workload | speed (B) | balanced (A) | upstream native (C) |
|---|---|---|---|
| TPC-H SF1 + SF10, ADBC + JDBC, local | 22/22 | 22/22 | **0/22 ADBC, 1/22 JDBC** (md5 `813b233c6193` / `50bb2801381f`, as before) |
| TPC-H SF1 + SF10, ADBC + JDBC, S3 | 22/22 | 22/22 | **0/22 ADBC, 1/22 JDBC** |
| small queries 1/8/32 clients, local + S3 | 0 errors | 0 errors | **errors at most steps, server died after small** |
| slow link TPC-H SF10 ADBC (ZSTD) | 22/22 (md5 `c9c83daae5eb`) | 22/22 | **0/22** (prepare fails: no `tpch` schema, decimal typing) |
| scans 1/4/8 + ADBC export, local | 0 errors | 0 errors | **x8 stream errors in all 3 rounds (2 / 2 / 2)** |
| scans 1/4/8 + ADBC export, S3 | 0 errors | 0 errors | **x8 stream errors in 2 of 3 rounds (1 / 1)** |
| closed-loop load 1-128, local | 0 errors | 0 errors | 0 errors |

## Speed vs balanced vs upstream (medians over 3 rounds)

| area | metric | B speed | A balanced | C upstream | speed / balanced (rounds) | speed / upstream | balanced / upstream |
|---|---|---|---|---|---|---|---|
| TPC-H local (9V74) | SF1 ADBC / JDBC (s) | 3.4 / 3.4 | 3.4 / 3.5 | n/a | 1.01 / 0.97 | n/a | n/a |
| TPC-H local (9V74) | SF10 ADBC / JDBC (s) | 34.2 / 34.3 | 34.6 / 34.8 | n/a | 0.99 / 0.99 | n/a | n/a |
| TPC-H S3 (6973P-C) | SF1 ADBC / JDBC (s) | 3.6 / 3.7 | 25.1 / 24.7 | n/a | 0.14 / 0.15 | n/a | n/a |
| TPC-H S3 (7763) | SF10 ADBC (s) | 37.8 | 288.7 | n/a | 0.13 (0.13 0.16 0.13) | n/a | n/a |
| TPC-H S3 (8370C) | SF10 JDBC (s) | 45.3 | 284.6 | n/a | 0.16 (0.16 0.16 0.16) | n/a | n/a |
| small local (9V45) | ADBC c1 / c8 / c32 p50 (ms) | 12.3 / 63.7 / 242 | 10.8 / 62.1 / 271 | n/a | **1.14** (1.26 1.14 1.13) / 1.03 (0.99 0.99 1.04) / 0.89 | n/a | n/a |
| small local | ADBC c1 / c8 / c32 p95 (ms) | 31.4 / 171 / 695 | 32.8 / 179 / 795 | n/a | 0.96 / 0.95 / 0.87 | n/a | n/a |
| small local | JDBC c1 / c8 / c32 p50 (ms) | 17.0 / 68.2 / 257 | 15.6 / 73.7 / 280 | n/a | **1.09** (1.19 1.09 1.13) / 0.93 / 0.92 | n/a | n/a |
| small local | JDBC c1 / c8 / c32 p95 (ms) | 30.9 / 174 / 709 | 31.0 / 186 / 840 | n/a | 1.00 / 0.93 / 0.84 | n/a | n/a |
| small S3 (9V45) | ADBC c1 / c8 / c32 p50 (ms) | 9.9 / 50.8 / 157 | 20.8 / 251 / 1007 | n/a | 0.47 / 0.20 / 0.16 | n/a | n/a |
| small S3 | ADBC c1 / c8 / c32 p95 (ms) | 28.2 / 131 / 629 | 706 / 3805 / 12802 | n/a | **0.04 / 0.03 / 0.05** | n/a | n/a |
| small S3 | JDBC c1 / c8 / c32 p50 (ms) | 22.8 / 63.3 / 177 | 28.0 / 268 / 954 | n/a | 0.81 / 0.24 / 0.19 | n/a | n/a |
| small S3 | JDBC c1 / c8 / c32 p95 (ms) | 42.5 / 141 / 662 | 692 / 3755 / 13161 | n/a | 0.06 / 0.04 / 0.05 | n/a | n/a |
| scan local (9V74) | x1 / x4 / x8 (MB/s) | 556 / 720 / 735 | 551 / 565 / 485 | 528 / 681 / n/a (errors) | 1.01 / 1.27 / **1.52** | 1.05 / 1.06 / n/a | 1.04 / 0.83 / n/a |
| scan local | ADBC export (MB/s) | 648 | 639 | 653 | 1.01 | 0.99 | 0.98 |
| scan S3 (9V74) | x1 / x4 / x8 (MB/s) | 405 / 736 / 740 | 383 / 513 / 473 | 361 / 678 / n/a (errors) | 1.06 / **1.44** / **1.57** | 1.12 / 1.09 / n/a | 1.06 / 0.76 / n/a |
| scan S3 | ADBC export (MB/s) | 669 | 360 | 655 | 1.86 (1.69 1.85 2.02) | 1.02 | 0.55 |
| load local (7763) | JDBC q/s at 1 / 8 / 32 / 64 / 128 clients | 41.9 / 51.8 / 52.3 / 53.0 / 51.8 | 40.5 / 44.0 / 42.4 / 39.8 / 37.4 | 38.1 / 51.4 / 54.1 / 53.7 / 53.6 | 1.03 / 1.18 / 1.23 / 1.33 / **1.39** (1.39 1.32 1.39) | 1.10 / 1.01 / 0.97 / 0.99 / 0.97 | 1.06 / 0.86 / 0.78 / 0.74 / 0.70 |
| load local (7763) | ADBC q/s at 1 / 8 / 32 / 64 / 128 clients | 43.0 / 52.2 / 52.4 / 52.5 / 52.5 | 41.4 / 44.9 / 41.6 / 39.4 / 37.0 | 44.5 / 55.5 / 55.0 / 54.6 / 53.9 | 1.04 / 1.16 / 1.26 / 1.33 / **1.42** (1.39 1.37 1.42) | 0.97 / 0.94 / 0.95 / 0.96 / 0.97 | 0.93 / 0.81 / 0.76 / 0.72 / 0.69 |
| load local | saturation (best median q/s) | 53.0 (JDBC c64) | 44.9 (ADBC c8) | 55.5 (ADBC c8) | 1.18 | 0.95 | 0.81 |
| slow link (10 ms, 1 Gbit), ZSTD (9V74) | ADBC export (MB/s) | 321.4 | 321.6 | 317.6 | 1.00 (1.00 1.07 0.95) | 1.01 | 1.01 |
| slow link (10 ms, 1 Gbit), ZSTD | TPC-H SF10 ADBC (s, median sum) | 34.3 | 35.2 | n/a (0/22) | 0.98 | n/a | n/a |

Load ran on an EPYC 7763 (`74464701e372`: 9V74), so absolute q/s are ~20 % lower for all three servers; the ratios
are in line (`2ff221447b5d` on the same 7763: +36 % JDBC / +44 % ADBC at 128 clients, now +39 % / +42 %). Saturation
(p95 < 100 ms) is 1 client for all three. **`load.md` (rereport 43194955428) again shows balanced q/s above the
client's own count (44-48 vs 37-45 q/s); speed and upstream agree within 1-2 q/s - ratios use the client count**
(same open point as `FRESH-deafc861cce3`). Balanced memory under load grows to ~4.6 GB at 128 clients, speed stays
under 0.9 GB like upstream.

Slow link ran on a 9V74 (`74464701e372`: 8573C, 255-270 MB/s), so all three servers export faster (318-322 MB/s);
speed 1.01 of upstream ZSTD.

## Local small c1 speed / balanced (regression by the rule, carried over)

| build | runner | JDBC c1 p50 (rounds) | ADBC c1 p50 (rounds) |
|---|---|---|---|
| `deafc861cce3` | 9V45 | 1.10 (in all rounds) | 1.08 (not all rounds) |
| `894afb9b48c4` | 9V45 | 1.19 (1.28 1.12 1.19) | 1.28 (1.34 1.20 1.36) |
| `37bf9401d77c` | 9V45 | 1.14 (1.15 1.14 1.13) | 1.32 (1.08 1.33 1.26) |
| `2ff221447b5d` | 9V74 | 1.07 (1.10 1.09 0.97) | 1.11 (1.19 1.09 1.11) |
| `29f1267b995f` | 9V74 | 1.19 (1.12 1.09 1.19) | 1.16 (1.14 1.17 1.16) |
| `74464701e372` | 8573C | 1.12 (1.08 1.12 1.15) | 1.23 (1.23 1.33 1.20) |
| **`2c169a53db3b`** | **9V45** | **1.09 (1.19 1.09 1.13)**, 15.6 -> 17.0 ms | **1.14 (1.26 1.14 1.13)**, 10.8 -> 12.3 ms |

**Both clients are > 5 % slower at c1 p50 in all 3 rounds again (regression by the rule, carried over).** On the
9V45 CPU type it is smaller than on `894afb9b48c4` / `37bf9401d77c` (1.19 / 1.28, 1.14 / 1.32) and close to
`deafc861cce3`; c1 p95 is level (ADBC 0.96, JDBC 1.00), 8/32 clients 0.84-1.03, S3 c1 0.47 / 0.81.

## Memory (server RSS peak, MB, median over rounds)

| job | B speed | A balanced | C upstream | speed / balanced | speed / upstream | speed vs `74464701e372` | balanced vs `74464701e372` |
|---|---|---|---|---|---|---|---|
| TPC-H local | 1827 | 1624 | 368 (failed answers) | 1.12 | 4.96 | 1829 (same) | 1649 (-2 %) |
| TPC-H S3 SF1 | 984 | 771 | 597 (failed answers) | 1.28 | 1.65 | 979 (same) | 750 (+3 %) |
| TPC-H S3 SF10 ADBC | 3404 | 1654 | 1031 (failed answers) | 2.06 | 3.30 | 3521 (-3 %) | 1606 (+3 %) |
| TPC-H S3 SF10 JDBC | 3451 | 1595 | 1040 (failed answers) | 2.16 | 3.32 | 3382 (+2 %) | 1620 (-2 %) |
| small local | 837 | 1505 | 251 (died) | 0.56 | 3.33 | 904 (-7 %) | 1554 (-3 %) |
| small S3 | 1523 | 2307 | 396 (died) | 0.66 | 3.85 | 1523 (same) | 2303 (same) |
| scan local | 1150 | 1208 | 3731 | 0.95 | 0.31 | 1188 (-3 %) | 1279 (-6 %) |
| scan S3 | 3326 | 1717 | 5907 | 1.94 | 0.56 | 3311 (same) | 1717 (same) |
| load local | 902 | 4557 | 929 | 0.20 | 0.97 | 890 (+1 %) | 5038 (-10 %, other CPU) |
| slow link | 1730 | 1532 | 602 (failed answers) | 1.13 | 2.87 | 1782 (-3 %) | 1604 (-4 %) |

No memory change from Q3 (allocator limit default) on these paths: speed -7 .. +2 %, balanced -10 .. +3 % vs
`74464701e372` (the load difference is a different CPU type and peak timing).

## Upstream native `cfaa929746cb`

Unchanged since `FRESH-74464701e372` (same commit, still the head at dispatch). Same gate failures (TPC-H 0/22 ADBC,
1/22 JDBC with the same md5; small errors, server dies after small; slow-link 0/22); x8 scan stream errors in all 3
rounds local, 2 of 3 on S3. Speed is 0.95-0.97 of it under load from 8 clients, 1.05-1.12 on x1/x4 scans, 1.01 on
the slow-link ZSTD export.

## Verdict

- **No wrong answers**: speed and balanced 22/22 on every TPC-H job (local, S3, slow link), 0 errors on small, scan and
  load.
- **Regression by the rule, carried over: local small c1 p50 speed/balanced 1.09 JDBC (1.19 1.09 1.13) and 1.14 ADBC
  (1.26 1.14 1.13)** in all 3 rounds (9V45); smaller than on the earlier 9V45 runs of `894afb9b48c4` / `37bf9401d77c`;
  c1 p95 level, 8/32 clients faster.
- Q-40b-1 (pruning off for a local dataDir): answers right; speed local TPC-H SF10 34.2 / 34.3 s vs 32.7 / 32.8 s on
  `74464701e372` (same CPU type, +5 % across runs, speed/balanced 0.99 instead of 0.96-0.97); worth a look if pruning
  should stay on for speed.
- Speed otherwise as before: S3 TPC-H 0.13-0.16 of balanced, S3 small-query tails 0.03-0.06, load +39-42 % at 128
  clients (0.97 of upstream native) at 0.20 of balanced RSS, scans x4/x8 1.27-1.57 of balanced, slow-link ZSTD export
  1.00 of balanced and 1.01 of upstream; RSS unchanged.
- Upstream native unchanged at `cfaa929746cb`; same gate failures.
