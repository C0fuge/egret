# Fresh upstream three-way: `6f0aa5a026fa` speed vs balanced vs upstream native

Task: `ci/BUILD-TRACK-TASK.md`, "FRESH UPSTREAM TRACKING" (build `server-1.0.0-6f0aa5a026fa`: kestrel item 51, join
runtime filters sent with the Flight ticket (block `ARF1`) and applied to plain scans; tickets without the block are
unchanged). The harness sends no `ARF1` block, so this run checks that the change costs nothing on the local and S3
paths. No ACCEPT (item 51 is not an HDFS item). Compare run 43840086547, wave
[`fresh-up-6f0aa5a026fa`](../ci/waves/fresh-up-6f0aa5a026fa.json), 10 jobs, all green, 3 rounds each, alternating
order; per-step load via rereport (`load.md`).

- A = `6f0aa5a026fa` default (balanced)
- B = `6f0aa5a026fa -DresourceProfile=speed`
- C = upstream native **`28d6ea713b8eb6377704ba85807ed7e433ae4869`** (head of `feat/starrocks-native-integration` at
  dispatch 09:28 UTC; unchanged since `d2e27119fda4`)

Full tables: [run summary](fresh-up-6f0aa5a026fa-43840086547/summary.md),
[speed report](fresh-up-6f0aa5a026fa-43840086547/speed.md), [load.md](fresh-up-6f0aa5a026fa-43840086547/load.md).
Load q/s and the slow-link numbers come from each round's `result.txt` in the job logs (the client's own 60 s count).
All three servers of a job run on the same runner. Ratios: for times, < 1 = first faster; for MB/s and q/s, > 1 =
first faster.

## What item 51 touches here

Nothing the harness exercises: without an `ARF1` block in the ticket the scan path is meant to be unchanged. Within
each job (the measure the rule uses) speed/balanced is in line with `d2e27119fda4` everywhere except the local ADBC c1
p50 (below). Across runs:

- **S3 SF10 JDBC (7763 runner both times)**: speed 46.0 s (rounds 46.0 45.7 46.0) vs 38.5 s (38.2 38.5 44.0) on
  `d2e27119fda4`, +19 %; balanced 289.5 s vs 300.5 s (-4 %); speed/balanced 0.16 vs 0.13. **The unchanged upstream
  binary `28d6ea713b8e` is slower by about the same factor on the same job (its one answered query q06: 0.85-0.92 s vs
  0.73-0.75 s, +22 %)**, so this reads as a slower runner (S3 path), not as an item 51 cost. Not a regression by the
  rule (speed/balanced within the job 0.15-0.16 every round). Re-check in the next FRESH run.
- The `d2e27119fda4` open point (S3 SF10 ADBC speed +5 % across runs) cannot be re-checked: this time the ADBC job ran
  on a Xeon 6973P-C (30.1 s, speed/balanced 0.11), not a 7763.
- Local scans (9V45 both times): all three servers 5-6 % lower than last run (speed x8 860 vs 915, balanced 613 vs
  643, upstream x4 795 vs 846 MB/s), ratios unchanged - runner variance.

## Correctness

| workload | speed (B) | balanced (A) | upstream native (C) |
|---|---|---|---|
| TPC-H SF1 + SF10, ADBC + JDBC, local | 22/22 | 22/22 | **0/22 ADBC, 1/22 JDBC** (md5 `813b233c6193` / `50bb2801381f`, as before) |
| TPC-H SF1 + SF10, ADBC + JDBC, S3 | 22/22 | 22/22 | **0/22 ADBC, 1/22 JDBC** |
| small queries 1/8/32 clients, local + S3 | 0 errors | 0 errors | **errors at most steps, server died after small** |
| slow link TPC-H SF10 ADBC (ZSTD) | 22/22 (md5 `c9c83daae5eb`) | 22/22 | **0/22** (prepare fails: no `tpch` schema, decimal typing) |
| scans 1/4/8 + ADBC export, local | 0 errors | 0 errors | **x8 stream errors in 2 of 3 rounds (2 / 2)** |
| scans 1/4/8 + ADBC export, S3 | 0 errors | 0 errors | **x8 stream errors in 3 of 3 rounds (3 / 1 / 1)** |
| closed-loop load 1-128, local | 0 errors | 0 errors | 0 errors |

## Speed vs balanced vs upstream (medians over 3 rounds)

| area | metric | B speed | A balanced | C upstream | speed / balanced (rounds) | speed / upstream | balanced / upstream |
|---|---|---|---|---|---|---|---|
| TPC-H local (7763) | SF1 ADBC / JDBC (s) | 4.3 / 4.4 | 4.2 / 4.3 | n/a | 1.03 / 1.03 | n/a | n/a |
| TPC-H local (7763) | SF10 ADBC / JDBC (s) | 41.9 / 42.0 | 42.8 / 44.4 | n/a | 0.98 (1.03 1.00 0.89) / 0.95 (1.05 0.92 0.90) | n/a | n/a |
| TPC-H S3 (9V74) | SF1 ADBC / JDBC (s) | 3.3 / 3.4 | 25.3 / 24.4 | n/a | 0.13 / 0.14 | n/a | n/a |
| TPC-H S3 (6973P-C) | SF10 ADBC (s) | 30.1 | 276.1 | n/a | 0.11 (0.14 0.10 0.11) | n/a | n/a |
| TPC-H S3 (7763) | SF10 JDBC (s) | 46.0 | 289.5 | n/a | 0.16 (0.16 0.15 0.16) | n/a | n/a |
| small local (9V45) | ADBC c1 / c8 / c32 p50 (ms) | 13.1 / 62.4 / 244 | 10.4 / 64.3 / 278 | n/a | **1.26** (1.22 1.16 1.26) / 0.97 / 0.88 | n/a | n/a |
| small local | ADBC c1 / c8 / c32 p95 (ms) | 32.4 / 166 / 709 | 31.9 / 182 / 873 | n/a | 1.01 / 0.91 / 0.81 | n/a | n/a |
| small local | JDBC c1 / c8 / c32 p50 (ms) | 17.8 / 75.9 / 253 | 16.0 / 77.9 / 314 | n/a | 1.11 (1.12 1.01 1.05) / 0.97 / 0.80 | n/a | n/a |
| small local | JDBC c1 / c8 / c32 p95 (ms) | 32.9 / 174 / 710 | 33.1 / 199 / 892 | n/a | 0.99 / 0.87 / 0.80 | n/a | n/a |
| small S3 (9V74) | ADBC c1 / c8 / c32 p50 (ms) | 12.4 / 54.5 / 176 | 24.2 / 252 / 919 | n/a | 0.51 / 0.22 / 0.19 | n/a | n/a |
| small S3 | ADBC c1 / c8 / c32 p95 (ms) | 32.4 / 164 / 788 | 599 / 3439 / 12991 | n/a | **0.05 / 0.05 / 0.06** | n/a | n/a |
| small S3 | JDBC c1 / c8 / c32 p50 (ms) | 24.0 / 72.1 / 196 | 31.0 / 264 / 963 | n/a | 0.78 / 0.27 / 0.20 | n/a | n/a |
| small S3 | JDBC c1 / c8 / c32 p95 (ms) | 45.0 / 175 / 797 | 561 / 3507 / 12362 | n/a | 0.08 / 0.05 / 0.06 | n/a | n/a |
| scan local (9V45) | x1 / x4 / x8 (MB/s) | 636 / 847 / 860 | 655 / 682 / 613 | 618 / 795 / n/a (errors) | 0.97 / 1.24 / **1.40** | 1.03 / 1.06 / n/a | 1.06 / 0.86 / n/a |
| scan local | ADBC export (MB/s) | 790 | 767 | 773 | 1.03 | 1.02 | 0.99 |
| scan S3 (9V74) | x1 / x4 / x8 (MB/s) | 411 / 721 / 728 | 380 / 444 / 452 | 331 / 685 / n/a (errors) | 1.08 (1.67 1.03 0.78) / **1.62** / **1.61** | 1.24 / 1.05 / n/a | 1.15 / 0.65 / n/a |
| scan S3 | ADBC export (MB/s) | 659 | 381 | 652 | 1.73 (1.65 1.83 1.73) | 1.01 | 0.58 |
| load local (7763) | JDBC q/s at 1 / 8 / 32 / 64 / 128 clients | 40.2 / 50.6 / 51.7 / 52.5 / 50.4 | 41.1 / 45.0 / 42.5 / 39.9 / 37.7 | 37.3 / 51.1 / 53.6 / 53.5 / 52.3 | 0.98 / 1.12 / 1.22 / 1.32 / **1.34** (1.34 1.41 1.33) | 1.08 / 0.99 / 0.96 / 0.98 / 0.96 | 1.10 / 0.88 / 0.79 / 0.75 / 0.72 |
| load local (7763) | ADBC q/s at 1 / 8 / 32 / 64 / 128 clients | 43.0 / 51.2 / 51.7 / 52.1 / 51.0 | 42.5 / 44.6 / 41.0 / 39.5 / 36.1 | 43.2 / 54.7 / 54.5 / 54.0 / 53.6 | 1.01 / 1.15 / 1.26 / 1.32 / **1.41** (1.41 1.44 1.39) | 1.00 / 0.94 / 0.95 / 0.96 / 0.95 | 0.98 / 0.82 / 0.75 / 0.73 / 0.67 |
| load local | saturation (best median q/s) | 52.5 (JDBC c64) | 45.0 (JDBC c8) | 54.7 (ADBC c8) | 1.17 | 0.96 | 0.82 |
| slow link (10 ms, 1 Gbit), ZSTD (7763) | ADBC export (MB/s) | 256.7 | 253.9 | 260.8 | 1.01 (1.04 0.97 0.99) | 0.98 | 0.97 |
| slow link (10 ms, 1 Gbit), ZSTD | TPC-H SF10 ADBC (s, median sum) | 39.6 | 41.9 | n/a (0/22) | 0.95 (0.95 0.95 0.96) | n/a | n/a |

Load ran on a 7763 (`d2e27119fda4`: 9V74), so absolute q/s are ~25 % lower for all three servers, as on
`2c169a53db3b` (7763: +39 % JDBC / +42 % ADBC at 128 clients; now +34 % / +41 %). Balanced memory under load grows to
~4.6 GB at 128 clients, speed stays under 0.9 GB like upstream. Slow link ran on a 7763 (`d2e27119fda4`: 6973P-C,
329-345 MB/s), so all three export slower (254-261 MB/s, the level of `2ff221447b5d` on a 7763); speed 0.98 of
upstream ZSTD. S3 scan x1 is noisy across rounds (speed/balanced 1.67 1.03 0.78); x4/x8 and the export are stable.

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
| `d2e27119fda4` | 9V45 | 1.12 (1.15 1.07 1.14) | 1.15 (1.13 1.15 1.27) |
| **`6f0aa5a026fa`** | **9V45** | 1.11 (1.12 1.01 1.05), not all rounds, 16.0 -> 17.8 ms | **1.26 (1.22 1.16 1.26)**, 10.4 -> 13.1 ms |

**ADBC is > 5 % slower at c1 p50 in all 3 rounds (regression by the rule, carried over, larger than on
`d2e27119fda4`: 1.26 vs 1.15 on the same CPU type)**: balanced got faster (10.6 -> 10.4 ms), speed slower (12.2 ->
13.1 ms). JDBC is 1.11 by the medians but round 2 is 1.01, so not by the rule this time. c1 p95 level (ADBC 1.01, JDBC
0.99), c1 p99 0.90-0.93, 8/32 clients 0.80-0.97, S3 c1 0.51 / 0.78.

## Memory (server RSS peak, MB, median over rounds)

| job | B speed | A balanced | C upstream | speed / balanced | speed / upstream | speed vs `d2e27119fda4` | balanced vs `d2e27119fda4` |
|---|---|---|---|---|---|---|---|
| TPC-H local | 1742 | 1564 | 358 (failed answers) | 1.11 | 4.87 | 1818 (-4 %, other CPU) | 1617 (-3 %) |
| TPC-H S3 SF1 | 1001 | 785 | 568 (failed answers) | 1.28 | 1.76 | 995 (+1 %) | 755 (+4 %) |
| TPC-H S3 SF10 ADBC | 3447 | 1642 | 1068 (failed answers) | 2.10 | 3.23 | 3380 (+2 %) | 1666 (-1 %) |
| TPC-H S3 SF10 JDBC | 3362 | 1601 | 1015 (failed answers) | 2.10 | 3.31 | 3375 (same) | 1618 (-1 %) |
| small local | 794 | 1513 | 252 (died) | 0.52 | 3.15 | 831 (-4 %) | 1503 (+1 %) |
| small S3 | 1515 | 2327 | 394 (died) | 0.65 | 3.85 | 1522 (same) | 2259 (+3 %) |
| scan local | 1184 | 1364 | 3692 | 0.87 | 0.32 | 1157 (+2 %) | 1230 (+11 %) |
| scan S3 | 3317 | 1741 | 5937 | 1.91 | 0.56 | 3316 (same) | 1779 (-2 %) |
| load local | 858 | 4554 | 932 | 0.19 | 0.92 | 866 (-1 %) | 4915 (-7 %, other CPU) |
| slow link | 1692 | 1525 | 608 (failed answers) | 1.11 | 2.78 | 1638 (+3 %) | 1554 (-2 %) |

No memory change from item 51: speed -4 .. +3 %, balanced -3 .. +4 % vs `d2e27119fda4` except balanced local scan
+11 % (1364 vs 1230 MB; per round speed/balanced 0.80 0.87 0.93, peak timing) and balanced load -7 % on another CPU type.

## Upstream native `28d6ea713b8e`

Unchanged since `d2e27119fda4`. Same gate failures: TPC-H 0/22 ADBC, 1/22 JDBC with the same md5 (no `tpch` schema,
decimal typing), small errors at most steps and the server dies after small, slow-link 0/22; x8 scan stream errors in
2 of 3 rounds local (as before) and 3 of 3 on S3 (before: 1 of 3). Speed is 0.95-0.98 of it under load from 32 clients,
1.03-1.06 on local x1/x4 scans, 1.05 on S3 x4, 1.01-1.02 on the ADBC export, 0.98 on the slow-link ZSTD export.

## Verdict

- **No wrong answers**: speed and balanced 22/22 on every TPC-H job (local, S3, slow link), 0 errors on small, scan and
  load.
- **Regression by the rule, carried over: local small ADBC c1 p50 speed/balanced 1.26 (1.22 1.16 1.26)** in all 3 rounds
  (9V45), larger than `d2e27119fda4` (1.15) on the same CPU type; JDBC c1 1.11 but not in all rounds (1.12 1.01 1.05);
  c1 p95 level, 8/32 clients faster.
- Item 51 (runtime filters only with an `ARF1` ticket block, which the harness does not send): no visible cost in any
  within-job ratio or in memory. S3 SF10 JDBC speed 46.0 s vs 38.5 s on `d2e27119fda4` (same CPU type, +19 %, all
  rounds) moves together with the unchanged upstream binary on the same job (+22 %), so it is read as runner variance;
  re-check next FRESH. The ADBC +5 % open point could not be re-checked (other CPU type).
- Speed otherwise as before: S3 TPC-H 0.11-0.16 of balanced, S3 small-query tails 0.05-0.08, load +34-41 % at 128
  clients (0.95-0.96 of upstream native) at 0.19 of balanced RSS, scans x4/x8 1.24-1.62 of balanced, S3 ADBC export
  1.73, slow-link ZSTD export 1.01 of balanced and 0.98 of upstream.
- A run with `ARF1` tickets (a client that sends join filters) would be needed to measure item 51 itself; the harness
  has none.
