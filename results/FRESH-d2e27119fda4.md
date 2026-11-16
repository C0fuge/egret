# Fresh upstream three-way: `d2e27119fda4` speed vs balanced vs upstream native

Task: `ci/BUILD-TRACK-TASK.md`, "FRESH UPSTREAM TRACKING" (build `server-1.0.0-d2e27119fda4`: kestrel item 49
(upstream server changes since `cec626bbb54a`: (a) read-only SqlInfo DDL, (b) opt-in `streamTimingLog`, (c) metadata
cache caps, (d) parallel cold footers, `fileInventoryRefreshSeconds`) and item 50 (distributed-complete small scans and
unfiltered count(*) computed on the planning node)). It contains `7ab48cd6675c` (item 49 only), skipped as contained.
HDFS acceptance: [ACCEPT-7ab48cd6675c](ACCEPT-7ab48cd6675c.md) and [ACCEPT-d2e27119fda4](ACCEPT-d2e27119fda4.md)
(both SHIP). Compare run 43798340706, wave [`fresh-up-d2e27119fda4`](../ci/waves/fresh-up-d2e27119fda4.json), 10 jobs,
all green, 3 rounds each, alternating order; per-step load via rereport 43811945061.

- A = `d2e27119fda4` default (balanced)
- B = `d2e27119fda4 -DresourceProfile=speed`
- C = upstream native **`28d6ea713b8eb6377704ba85807ed7e433ae4869`** (head of `feat/starrocks-native-integration` at
  dispatch 03:27 UTC; new since `cfaa929746cb`)

Full tables: [run summary](fresh-up-d2e27119fda4-43798340706/summary.md),
[speed report](fresh-up-d2e27119fda4-43798340706/speed.md), [load.md](fresh-up-d2e27119fda4-43798340706/load.md).
Load q/s and the slow-link numbers come from each round's `result.txt` in the job logs (the client's own 60 s count).
All three servers of a job run on the same runner. Ratios: for times, < 1 = first faster; for MB/s and q/s, > 1 =
first faster.

## What the new items touch here

Item 50 is on the distributed-complete path (not in these single-server waves; ACCEPT checks 3 and 5 pass). Item 49
(c)/(d) (metadata cache caps, parallel cold footers) are on the local and S3 paths of this wave:

- **Local TPC-H**: on the same CPU type as `2ff221447b5d` (EPYC 9V45) speed SF10 is 24.4 / 23.9 s ADBC / JDBC
  (2ff: 24.0 / 24.2) - unchanged; speed/balanced 0.96 / 0.98, SF1 1.02 / 0.98. The `2c169a53db3b` SF10 numbers
  (34.2 s) were on a 9V74 and are not comparable.
- **S3 TPC-H**: on the same CPU type as `2c169a53db3b` (EPYC 7763) S3 SF10 ADBC speed 39.8 s (2c16: 37.8, +5 % across
  runs), balanced 276.2 s (288.7, -4 %); within the job speed/balanced 0.14 (2c16: 0.13). Not a regression by the rule
  (the rule compares within a job); one run, so the +5 % is not attributable to item 49 (d) from this data.
- Cold-file effects of (d) are not isolated by this wave (TPC-H totals are sums of warm medians).

## Correctness

| workload | speed (B) | balanced (A) | upstream native (C) |
|---|---|---|---|
| TPC-H SF1 + SF10, ADBC + JDBC, local | 22/22 | 22/22 | **0/22 ADBC, 1/22 JDBC** (md5 `813b233c6193` / `50bb2801381f`, as before) |
| TPC-H SF1 + SF10, ADBC + JDBC, S3 | 22/22 | 22/22 | **0/22 ADBC, 1/22 JDBC** |
| small queries 1/8/32 clients, local + S3 | 0 errors | 0 errors | **errors at most steps, server died after small** |
| slow link TPC-H SF10 ADBC (ZSTD) | 22/22 (md5 `c9c83daae5eb`) | 22/22 | **0/22** (prepare fails: no `tpch` schema, decimal typing) |
| scans 1/4/8 + ADBC export, local | 0 errors | 0 errors | **x8 stream errors in 2 of 3 rounds (2 / 1)** |
| scans 1/4/8 + ADBC export, S3 | 0 errors | 0 errors | **x8 stream errors in 1 of 3 rounds (2)** |
| closed-loop load 1-128, local | 0 errors | 0 errors | 0 errors |

## Speed vs balanced vs upstream (medians over 3 rounds)

| area | metric | B speed | A balanced | C upstream | speed / balanced (rounds) | speed / upstream | balanced / upstream |
|---|---|---|---|---|---|---|---|
| TPC-H local (9V45) | SF1 ADBC / JDBC (s) | 2.4 / 2.5 | 2.4 / 2.6 | n/a | 1.02 / 0.98 | n/a | n/a |
| TPC-H local (9V45) | SF10 ADBC / JDBC (s) | 24.4 / 23.9 | 25.3 / 24.5 | n/a | 0.96 (0.96 0.97 0.97) / 0.98 | n/a | n/a |
| TPC-H S3 (7763) | SF1 ADBC / JDBC (s) | 4.2 / 4.2 | 26.5 / 26.4 | n/a | 0.16 / 0.16 | n/a | n/a |
| TPC-H S3 (7763) | SF10 ADBC (s) | 39.8 | 276.2 | n/a | 0.14 (0.14 0.15 0.14) | n/a | n/a |
| TPC-H S3 (7763) | SF10 JDBC (s) | 38.5 | 300.5 | n/a | 0.13 (0.13 0.13 0.15) | n/a | n/a |
| small local (9V45) | ADBC c1 / c8 / c32 p50 (ms) | 12.2 / 62.4 / 225 | 10.6 / 61.8 / 259 | n/a | **1.15** (1.13 1.15 1.27) / 1.01 / 0.87 | n/a | n/a |
| small local | ADBC c1 / c8 / c32 p95 (ms) | 30.0 / 168 / 674 | 31.1 / 170 / 781 | n/a | 0.96 / 0.99 / 0.86 | n/a | n/a |
| small local | JDBC c1 / c8 / c32 p50 (ms) | 16.7 / 69.3 / 253 | 14.9 / 69.2 / 270 | n/a | **1.12** (1.15 1.07 1.14) / 1.00 / 0.94 | n/a | n/a |
| small local | JDBC c1 / c8 / c32 p95 (ms) | 30.7 / 170 / 687 | 30.2 / 185 / 808 | n/a | 1.02 / 0.92 / 0.85 | n/a | n/a |
| small S3 (9V74) | ADBC c1 / c8 / c32 p50 (ms) | 12.5 / 53.3 / 170 | 25.4 / 256 / 945 | n/a | 0.49 / 0.21 / 0.18 | n/a | n/a |
| small S3 | ADBC c1 / c8 / c32 p95 (ms) | 34.5 / 165 / 781 | 596 / 3604 / 12351 | n/a | **0.06 / 0.05 / 0.06** | n/a | n/a |
| small S3 | JDBC c1 / c8 / c32 p50 (ms) | 25.8 / 68.2 / 198 | 40.9 / 259 / 979 | n/a | 0.63 / 0.26 / 0.20 | n/a | n/a |
| small S3 | JDBC c1 / c8 / c32 p95 (ms) | 66.1 / 179 / 779 | 712 / 3660 / 12686 | n/a | 0.09 / 0.05 / 0.06 | n/a | n/a |
| scan local (9V45) | x1 / x4 / x8 (MB/s) | 697 / 902 / 915 | 713 / 745 / 643 | 643 / 846 / n/a (errors) | 0.98 / 1.21 / **1.42** | 1.08 / 1.07 / n/a | 1.11 / 0.88 / n/a |
| scan local | ADBC export (MB/s) | 835 | 832 | 819 | 1.00 | 1.02 | 1.02 |
| scan S3 (9V45) | x1 / x4 / x8 (MB/s) | 577 / 913 / 929 | 558 / 655 / 617 | 536 / 837 / n/a (errors) | 1.03 / **1.39** / **1.51** | 1.08 / 1.09 / n/a | 1.04 / 0.78 / n/a |
| scan S3 | ADBC export (MB/s) | 857 | 666 | 828 | 1.29 (1.28 1.29 1.24) | 1.03 | 0.80 |
| load local (9V74) | JDBC q/s at 1 / 8 / 32 / 64 / 128 clients | 54.4 / 66.1 / 66.7 / 66.2 / 65.6 | 54.4 / 57.7 / 53.2 / 50.3 / 45.9 | 49.4 / 66.4 / 68.5 / 68.8 / 68.0 | 1.00 / 1.15 / 1.25 / 1.32 / **1.43** (1.45 1.41 1.41) | 1.10 / 1.00 / 0.97 / 0.96 / 0.96 | 1.10 / 0.87 / 0.78 / 0.73 / 0.67 |
| load local (9V74) | ADBC q/s at 1 / 8 / 32 / 64 / 128 clients | 56.0 / 67.5 / 66.5 / 66.0 / 65.2 | 55.9 / 56.7 / 51.5 / 48.4 / 45.9 | 57.2 / 70.8 / 70.0 / 70.0 / 67.9 | 1.00 / 1.19 / 1.29 / 1.36 / **1.42** (1.42 1.41 1.41) | 0.98 / 0.95 / 0.95 / 0.94 / 0.96 | 0.98 / 0.80 / 0.74 / 0.69 / 0.68 |
| load local | saturation (best median q/s) | 67.5 (ADBC c8) | 57.7 (JDBC c8) | 70.8 (ADBC c8) | 1.17 | 0.95 | 0.81 |
| slow link (10 ms, 1 Gbit), ZSTD (6973P-C) | ADBC export (MB/s) | 345.2 | 329.0 | 332.7 | 1.05 (1.01 1.07 1.03) | 1.04 | 0.99 |
| slow link (10 ms, 1 Gbit), ZSTD | TPC-H SF10 ADBC (s, median sum) | 30.9 | 31.6 | n/a (0/22) | 0.98 | n/a | n/a |

Load ran on a 9V74 (`2c169a53db3b`: 7763), so absolute q/s are ~25 % higher for all three servers; the ratios are in
line (`2c169a53db3b`: +39 % JDBC / +42 % ADBC at 128 clients, now +43 % / +42 %; `29f1267b995f` on a 9V74: +41 % /
+48 %). Saturation (p95 < 100 ms) is 1 client for all three. **`load.md` (rereport 43811945061) again shows balanced q/s
above the client's own count (55-62 vs 46-58 q/s); speed and upstream agree within 1-2 q/s - ratios use the client
count** (same open point as `FRESH-deafc861cce3`). Balanced memory under load grows to ~4.9 GB at 128 clients, speed
stays under 0.9 GB like upstream.

Slow link ran on a Xeon 6973P-C (new CPU type for this job; `2c169a53db3b`: 9V74, 318-322 MB/s), so all three servers
export faster (329-345 MB/s); speed 1.04 of upstream ZSTD.

## Local small c1 speed / balanced (regression by the rule, carried over)

| build | runner | JDBC c1 p50 (rounds) | ADBC c1 p50 (rounds) |
|---|---|---|---|
| `deafc861cce3` | 9V45 | 1.10 (in all rounds) | 1.08 (not all rounds) |
| `894afb9b48c4` | 9V45 | 1.19 (1.28 1.12 1.19) | 1.28 (1.34 1.20 1.36) |
| `37bf9401d77c` | 9V45 | 1.14 (1.15 1.14 1.13) | 1.32 (1.08 1.33 1.26) |
| `2ff221447b5d` | 9V74 | 1.07 (1.10 1.09 0.97) | 1.11 (1.19 1.09 1.11) |
| `29f1267b995f` | 9V74 | 1.19 (1.12 1.09 1.19) | 1.16 (1.14 1.17 1.16) |
| `74464701e372` | 8573C | 1.12 (1.08 1.12 1.15) | 1.23 (1.23 1.33 1.20) |
| `2c169a53db3b` | 9V45 | 1.09 (1.19 1.09 1.13) | 1.14 (1.26 1.14 1.13) |
| **`d2e27119fda4`** | **9V45** | **1.12 (1.15 1.07 1.14)**, 14.9 -> 16.7 ms | **1.15 (1.13 1.15 1.27)**, 10.6 -> 12.2 ms |

**Both clients are > 5 % slower at c1 p50 in all 3 rounds again (regression by the rule, carried over)**, at the
same size as `2c169a53db3b` on the same CPU type (1.09 / 1.14); c1 p95 level (ADBC 0.96, JDBC 1.02), c1 p99 0.90,
8/32 clients 0.85-1.01, S3 c1 0.49 / 0.63.

## Memory (server RSS peak, MB, median over rounds)

| job | B speed | A balanced | C upstream | speed / balanced | speed / upstream | speed vs `2c169a53db3b` | balanced vs `2c169a53db3b` |
|---|---|---|---|---|---|---|---|
| TPC-H local | 1818 | 1617 | 361 (failed answers) | 1.12 | 5.04 | 1827 (same) | 1624 (same) |
| TPC-H S3 SF1 | 995 | 755 | 582 (failed answers) | 1.32 | 1.71 | 984 (+1 %) | 771 (-2 %) |
| TPC-H S3 SF10 ADBC | 3380 | 1666 | 1007 (failed answers) | 2.03 | 3.36 | 3404 (-1 %) | 1654 (+1 %) |
| TPC-H S3 SF10 JDBC | 3375 | 1618 | 1023 (failed answers) | 2.09 | 3.30 | 3451 (-2 %) | 1595 (+1 %) |
| small local | 831 | 1503 | 253 (died) | 0.55 | 3.28 | 837 (same) | 1505 (same) |
| small S3 | 1522 | 2259 | 390 (died) | 0.67 | 3.90 | 1523 (same) | 2307 (-2 %) |
| scan local | 1157 | 1230 | 3714 | 0.94 | 0.31 | 1150 (+1 %) | 1208 (+2 %) |
| scan S3 | 3316 | 1779 | 5926 | 1.86 | 0.56 | 3326 (same) | 1717 (+4 %) |
| load local | 866 | 4915 | 975 | 0.18 | 0.89 | 902 (-4 %) | 4557 (+8 %, other CPU) |
| slow link | 1638 | 1554 | 610 (failed answers) | 1.05 | 2.69 | 1730 (-5 %) | 1532 (+1 %) |

No memory change from item 49 (c) metadata cache caps at this data size: speed -5 .. +1 %, balanced -2 .. +4 % vs
`2c169a53db3b` (the load difference is a different CPU type and peak timing).

## Upstream native `28d6ea713b8e`

New since `cfaa929746cb`. Same gate failures as before: TPC-H 0/22 ADBC, 1/22 JDBC with the same md5 (no `tpch`
schema, decimal typing), small errors at most steps and the server dies after small, slow-link 0/22; x8 scan stream
errors in 2 of 3 rounds local, 1 of 3 on S3 (`cfaa929746cb`: 3 of 3 local, 2 of 3 S3). Speed is 0.94-0.96 of it under
load from 32 clients (`cfaa929746cb`: 0.95-0.97, other CPU), 1.07-1.09 on x1/x4 scans (1.05-1.12), 1.02-1.03 on the
ADBC export, 1.04 on the slow-link ZSTD export (1.01); upstream RSS on these jobs within a few % of `cfaa929746cb`
except load 975 MB (929).

## Verdict

- **No wrong answers**: speed and balanced 22/22 on every TPC-H job (local, S3, slow link), 0 errors on small, scan and
  load.
- **Regression by the rule, carried over: local small c1 p50 speed/balanced 1.12 JDBC (1.15 1.07 1.14) and 1.15 ADBC
  (1.13 1.15 1.27)** in all 3 rounds (9V45), the same size as `2c169a53db3b`; c1 p95 level, 8/32 clients faster.
- Item 49 (c)/(d): no visible effect on local TPC-H (speed SF10 24.4 / 23.9 s = `2ff221447b5d` on the same CPU type)
  or memory; S3 SF10 ADBC speed 39.8 s vs 37.8 s on `2c169a53db3b` (same CPU type, +5 % across runs, one run;
  speed/balanced 0.14 vs 0.13) - re-check in the next FRESH run before reading it as an item 49 effect.
- Speed otherwise as before: S3 TPC-H 0.13-0.16 of balanced, S3 small-query tails 0.05-0.09, load +42-43 % at 128
  clients (0.96 of upstream native) at 0.18 of balanced RSS, scans x4/x8 1.21-1.51 of balanced, S3 ADBC export 1.29,
  slow-link ZSTD export 1.05 of balanced and 1.04 of upstream.
- Upstream native moved to `28d6ea713b8e`: same gate failures, fewer x8 scan stream errors, otherwise level.
