# Fresh upstream three-way: `f4feb0d5e404` speed vs balanced vs upstream native

Task: `ci/BUILD-TRACK-TASK.md`, "FRESH UPSTREAM TRACKING" (build `server-1.0.0-f4feb0d5e404`: kestrel item 52(a)
`memoryBudgetBytes` / `FLIGHT_MEMORY_BUDGET` overrides memory detection; **item 53: `resourceProfile=balanced` now
supplies `duckDbSharedDatabase=true`** (one shared DuckDB instead of one per connection; `-DduckDbSharedDatabase=false`
restores the old mode); item 55(b) opt-in `distributedAggregateMinBytes`, default 0 = off). ACCEPT on the same build:
[ACCEPT-f4feb0d5e404](ACCEPT-f4feb0d5e404.md), SHIP. Compare run 44158872708, wave
[`fresh-up-f4feb0d5e404`](../ci/waves/fresh-up-f4feb0d5e404.json), 10 jobs, all green, 3 rounds each, alternating
order; per-step load via rereport 44183288832 (`load.md`).

- A = `f4feb0d5e404` default (balanced, now on the shared DuckDB)
- B = `f4feb0d5e404 -DresourceProfile=speed`
- C = upstream native **`d05bf9c521294a6a91c5da44800aa420ab92a523`** (head of `feat/starrocks-native-integration` at
  dispatch 19:28 UTC; new, before `28d6ea713b8e`)

Full tables: [run summary](fresh-up-f4feb0d5e404-44158872708/summary.md),
[speed report](fresh-up-f4feb0d5e404-44158872708/speed.md), [load.md](fresh-up-f4feb0d5e404-44158872708/load.md).
Load q/s come from each round's `result.txt` in the job log (the client's own 60 s count). All three servers of a job
run on the same runner. Ratios: for times, < 1 = first faster; for MB/s and q/s, > 1 = first faster.

## What this build changes here

- **Item 53 is the visible change, and it is all on the balanced side.** Balanced now behaves like speed under
  concurrency: closed-loop load 52-54 q/s at 8-128 clients (was 36-45), speed/balanced **0.99-1.00** at 128 clients (was
  1.34 / 1.41); balanced memory under load 887 MB peak (was 4554 MB); local small c8/c32 p50 29-42 % lower (ADBC c32
  278 -> 165 ms, same 9V45 CPU), S3 small c8/c32 p50 61-65 % lower (other CPU type). Balanced RSS is lower on every
  small/scan/load job (0.19-0.69 of `6f0aa5a026fa`).
- Speed itself is unchanged within runner noise (RSS -5 .. +11 %, the +11 % on another CPU type; load, scans, TPC-H as
  before on the same CPU types).
- Item 52(a): the harness sets no `memoryBudgetBytes`, so the servers keep detecting the 6 GB container (no
  `memoryBudget=unset` WARN expected, the host is not > 64 GiB). Item 55(b) is off by default and needs a cluster; not
  exercised by these single-server waves.
- Because balanced got faster, several speed/balanced ratios moved without speed changing; read the speed/balanced
  columns below with that in mind.

## Correctness

| workload | speed (B) | balanced (A) | upstream native (C) |
|---|---|---|---|
| TPC-H SF1 + SF10, ADBC + JDBC, local | 22/22 | 22/22 | **0/22 ADBC, 1/22 JDBC** (md5 `813b233c6193` / `50bb2801381f`, as before) |
| TPC-H SF1 + SF10, ADBC + JDBC, S3 | 22/22 | 22/22 | **0/22 ADBC, 1/22 JDBC** |
| small queries 1/8/32 clients, local + S3 | 0 errors | 0 errors | **errors at most steps, server died after small** |
| slow link TPC-H SF10 ADBC (ZSTD) | 22/22 (md5 `c9c83daae5eb`) | 22/22 | **0/22** (prepare fails: no `tpch` schema, decimal typing) |
| scans 1/4/8 + ADBC export, local | 0 errors | 0 errors | 0 errors (x8 stream errors gone this run) |
| scans 1/4/8 + ADBC export, S3 | 0 errors | 0 errors | 0 errors (x8 stream errors gone this run) |
| closed-loop load 1-128, local | 0 errors | 0 errors | 0 errors |

## Speed vs balanced vs upstream (medians over 3 rounds)

| area | metric | B speed | A balanced | C upstream | speed / balanced (rounds) | speed / upstream | balanced / upstream |
|---|---|---|---|---|---|---|---|
| TPC-H local (6975P-C) | SF1 ADBC / JDBC (s) | 2.5 / 2.6 | 2.3 / 2.5 | n/a | **1.10 (1.11 1.11 1.10) / 1.08 (1.09 1.07 1.08)** | n/a | n/a |
| TPC-H local (6975P-C) | SF10 ADBC / JDBC (s) | 23.1 / 23.0 | 23.2 / 23.0 | n/a | 1.00 (0.98 1.00 1.00) / 1.00 (0.97 0.99 1.01) | n/a | n/a |
| TPC-H S3 (9V74) | SF1 ADBC / JDBC (s) | 3.3 / 3.4 | 30.1 / 28.8 | n/a | 0.11 / 0.12 | n/a | n/a |
| TPC-H S3 (9V74) | SF10 ADBC (s) | 32.3 | 266.3 | n/a | 0.12 (0.12 0.12 0.11) | n/a | n/a |
| TPC-H S3 (7763) | SF10 JDBC (s) | 38.2 | 273.9 | n/a | 0.14 (0.14 0.14 0.14) | n/a | n/a |
| small local (9V45) | ADBC c1 / c8 / c32 p50 (ms) | 13.3 / 70.3 / 255 | 11.2 / 45.3 / 165 | n/a | **1.19** (1.06 1.21 1.10) / **1.55** (1.48 1.55 1.55) / **1.55** (1.50 1.64 1.51) | n/a | n/a |
| small local | ADBC c1 / c8 / c32 p95 (ms) | 31.8 / 182 / 741 | 31.0 / 187 / 740 | n/a | 1.03 / 0.98 / 1.00 | n/a | n/a |
| small local | JDBC c1 / c8 / c32 p50 (ms) | 18.8 / 74.5 / 271 | 16.3 / 55.5 / 183 | n/a | 1.15 (1.00 1.15 1.13) / **1.34** (1.24 1.34 1.39) / **1.48** (1.40 1.55 1.39) | n/a | n/a |
| small local | JDBC c1 / c8 / c32 p95 (ms) | 34.5 / 188 / 747 | 32.7 / 193 / 741 | n/a | 1.05 / 0.98 / 1.01 | n/a | n/a |
| small S3 (6975P-C) | ADBC c1 / c8 / c32 p50 (ms) | 9.6 / 41.1 / 126 | 14.5 / 98.5 / 347 | n/a | 0.66 / 0.42 / 0.36 | n/a | n/a |
| small S3 | ADBC c1 / c8 / c32 p95 (ms) | 21.4 / 107 / 452 | 614 / 3822 / 13837 | n/a | **0.03 / 0.03 / 0.03** | n/a | n/a |
| small S3 | JDBC c1 / c8 / c32 p50 (ms) | 19.1 / 57.2 / 156 | 21.5 / 101 / 337 | n/a | 0.89 / 0.57 / 0.46 | n/a | n/a |
| small S3 | JDBC c1 / c8 / c32 p95 (ms) | 30.6 / 119 / 516 | 603 / 3807 / 13324 | n/a | 0.05 / 0.03 / 0.04 | n/a | n/a |
| scan local (8573C) | x1 / x4 / x8 (MB/s) | 463 / 620 / 627 | 446 / 548 / 567 | 423 / 568 / 586 | 1.04 / 1.13 / 1.10 | 1.09 / 1.09 / 1.07 | 1.05 / 0.96 / 0.97 |
| scan local | ADBC export (MB/s) | 552 | 515 | 515 | 1.07 | 1.07 | 1.00 |
| scan S3 (6975P-C) | x1 / x4 / x8 (MB/s) | 518 / 870 / 886 | 463 / 691 / 718 | 462 / 811 / 810 | 1.12 / 1.26 / 1.23 | 1.12 / 1.07 / 1.09 | 1.00 / 0.85 / 0.89 |
| scan S3 | ADBC export (MB/s) | 754 | 551 | 641 | 1.37 (1.27 1.42 1.37) | 1.18 | 0.86 |
| load local (7763) | JDBC q/s at 1 / 8 / 32 / 64 / 128 clients | 42.7 / 52.6 / 53.5 / 53.5 / 52.5 | 44.5 / 53.8 / 54.2 / 53.9 / 52.4 | 39.1 / 52.4 / 55.0 / 55.7 / 54.3 | 0.96 / 0.98 / 0.99 / 0.99 / **1.00** (1.01 1.01 1.00) | 1.09 / 1.00 / 0.97 / 0.96 / 0.97 | 1.14 / 1.03 / 0.99 / 0.97 / 0.97 |
| load local (7763) | ADBC q/s at 1 / 8 / 32 / 64 / 128 clients | 44.6 / 53.3 / 53.4 / 53.1 / 52.4 | 45.8 / 54.1 / 54.0 / 53.4 / 53.0 | 45.0 / 56.1 / 56.4 / 56.1 / 55.1 | 0.97 / 0.99 / 0.99 / 0.99 / **0.99** (1.00 0.97 0.99) | 0.99 / 0.95 / 0.95 / 0.95 / 0.95 | 1.02 / 0.96 / 0.96 / 0.95 / 0.96 |
| load local | saturation (best median q/s) | 53.5 (JDBC c32/c64) | 54.2 (JDBC c32) | 56.4 (ADBC c32) | 0.99 | 0.95 | 0.96 |
| slow link (10 ms, 1 Gbit), ZSTD (8573C) | ADBC export (MB/s) | 250 | 248 | 255 | 1.01 (1.00 1.01 1.01) | 0.98 | 0.97 |
| slow link (10 ms, 1 Gbit), ZSTD | TPC-H SF10 ADBC (s, median sum) | 40.1 | 41.1 | n/a (0/22) | 0.98 (0.98 0.97 0.98) | n/a | n/a |

Load ran on a 7763 as on `6f0aa5a026fa`. Speed is where it was (128 clients 52.5 / 52.4 q/s vs 50.4 / 51.0); balanced
rose from 37.7 / 36.1 to 52.4 / 53.0 q/s (+39 % / +47 %). Saturation (p95 < 100 ms) is 1 client for all three.
**`load.md` (rereport 44183288832) now agrees with the client's own count for balanced (43-54 q/s, the client 44-54)**:
the open point from `FRESH-deafc861cce3` (balanced q/s in `load.md` above the client count) was a per-connection-DuckDB
effect and is gone with item 53. In `load.md` the per-step server memory of balanced and speed is the same at every
step (JDBC 404-824 MiB, ADBC 437-843 MiB); the RSS peak is 887 / 885 MB. Upstream native leads by 3-5 % from 8 clients.

## Local small queries (regressions by the rule)

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
| `6f0aa5a026fa` | 9V45 | 1.11 (1.12 1.01 1.05) | 1.26 (1.22 1.16 1.26) |
| **`f4feb0d5e404`** | **9V45** | 1.15 (1.00 1.15 1.13), not all rounds, 16.3 -> 18.8 ms | **1.19 (1.06 1.21 1.10)**, 11.2 -> 13.3 ms |

- **c1: ADBC is > 5 % slower in all 3 rounds (regression by the rule, carried over; 1.19 vs 1.26 on `6f0aa5a026fa`)**;
  JDBC 1.15 by the medians but round 1 is 1.00, so not by the rule. c1 p95 level (1.03 / 1.05).
- **New by the rule: c8 and c32 p50 speed/balanced 1.34-1.55 in all rounds, ADBC and JDBC.** This is balanced getting
  faster (item 53: ADBC c8 64.3 -> 45.3 ms, c32 278 -> 165 ms; JDBC c8 77.9 -> 55.5, c32 314 -> 183, same CPU type),
  not speed getting slower: speed c8/c32 p50 moved -2 .. +13 % across runs (ADBC c8 62.4 -> 70.3, c32 244 -> 255; JDBC
  c8 75.9 -> 74.5, c32 253 -> 271). p95/p99 at 8/32 clients are level (0.98-1.02), so the tails are the same; balanced
  now has the lower median at concurrency on local disk. On S3 speed stays far ahead (p50 0.36-0.57, p95 0.03-0.04).
- **TPC-H local SF1 speed/balanced 1.10 ADBC / 1.08 JDBC in all rounds** (2.5 vs 2.3 s; `6f0aa5a026fa` 1.03 / 1.03 on a
  7763). SF10 is level (1.00 / 1.00). Small absolute gap (0.2 s on 2.3 s), on another CPU type; also counted by the rule.

## Memory (server RSS peak, MB, median over rounds)

| job | B speed | A balanced | C upstream | speed / balanced | speed / upstream | speed vs `6f0aa5a026fa` | balanced vs `6f0aa5a026fa` |
|---|---|---|---|---|---|---|---|
| TPC-H local | 1934 | 1717 | 353 (failed answers) | 1.13 | 5.48 | 1742 (+11 %, other CPU) | 1564 (+10 %, other CPU) |
| TPC-H S3 SF1 | 974 | 734 | 593 (failed answers) | 1.33 | 1.64 | 1001 (-3 %) | 785 (-6 %) |
| TPC-H S3 SF10 ADBC | 3436 | 1591 | 1039 (failed answers) | 2.16 | 3.31 | 3447 (same) | 1642 (-3 %) |
| TPC-H S3 SF10 JDBC | 3358 | 1475 | 1016 (failed answers) | 2.28 | 3.31 | 3362 (same) | 1601 (-8 %) |
| small local | 796 | **711** | 252 (died) | 1.12 | 3.16 | 794 (same) | 1513 (**-53 %**) |
| small S3 | 1534 | **793** | 396 (died) | 1.93 | 3.87 | 1515 (+1 %) | 2327 (**-66 %**) |
| scan local | 1129 | **908** | 1816 | 1.24 | 0.62 | 1184 (-5 %) | 1364 (**-33 %**) |
| scan S3 | 3306 | **1199** | 4206 | 2.76 | 0.79 | 3317 (same) | 1741 (**-31 %**) |
| load local | 885 | **887** | 988 | 1.00 | 0.90 | 858 (+3 %) | 4554 (**-81 %**) |
| slow link | 1685 | 1448 | 617 (failed answers) | 1.16 | 2.73 | 1692 (same) | 1525 (-5 %) |

Item 53 removes balanced's memory growth with connections: load 4554 -> 887 MB, small 1513 / 2327 -> 711 / 793 MB.
Speed/balanced memory is now > 1 on every job except load (1.00); before, balanced was the larger one on small, local
scan and load. The server repo's item 54 note (balanced OOM-killed at 6 GiB on 4 concurrent HDFS SF5 scans) is not
reproduced here: no job hit the 6 GB limit, balanced peaked at 1.7 GB.

## Upstream native `d05bf9c52129`

New head (was `28d6ea713b8e`). Same gate failures: TPC-H 0/22 ADBC, 1/22 JDBC with the same md5 (no `tpch` schema,
decimal typing), small errors at most steps and the server dies after small, slow-link 0/22. **No x8 scan stream errors
this time** (before: 2 of 3 rounds local, 3 of 3 S3), so x8 is ranked again: speed is 1.07 (local) / 1.09 (S3) of it.
Upstream scan RSS is lower (local 1816 vs 3692 MB, S3 4206 vs 5937 MB; different CPU types). Speed is 0.95-0.97 of it
under load from 32 clients, 1.07-1.12 on scans, 1.07 / 1.18 on the ADBC export local / S3, 0.98 on the slow-link ZSTD
export.

## Open points from `6f0aa5a026fa`

- S3 SF10 JDBC speed +19 % across runs (46.0 vs 38.5 s, 7763): now 38.2 s on a 7763 again, back to the `d2e27119fda4`
  level. Confirms runner variance; closed.
- S3 SF10 ADBC speed +5 % across runs (`d2e27119fda4`): 32.3 s on a 9V74 this time; no same-CPU earlier value, still
  not re-checked.

## Verdict

- **No wrong answers**: speed and balanced 22/22 on every TPC-H job (local, S3, slow link), 0 errors on small, scan and
  load.
- **Item 53 makes balanced much better under concurrency**: load +39-47 % at 128 clients (now = speed, 0.96-0.97 of
  upstream native), memory under load -81 % (887 MB), local small c8/c32 p50 -29 .. -42 %, balanced RSS -31 .. -66 % on
  small and scans. S3 small tails of balanced are unchanged (p95 3.8 s at 8 clients, 13.3-13.8 s at 32).
- **Regressions by the rule (speed/balanced, all 3 rounds):** local small ADBC c1 p50 1.19 (carried over, 1.26 before);
  new: local small c8/c32 p50 1.34-1.55 (ADBC and JDBC) and local TPC-H SF1 1.08-1.10. The c8/c32 one comes from balanced
  getting faster, not from speed (speed -2 .. +13 % across runs, p95/p99 level); SF1 is 0.2 s on another CPU type.
- Speed otherwise as before: S3 TPC-H 0.11-0.14 of balanced, S3 small tails 0.03-0.05, scans x4/x8 1.10-1.26 of
  balanced (smaller than before because balanced is faster), S3 ADBC export 1.37, slow-link ZSTD export 1.01 of balanced
  and 0.98 of upstream; vs upstream native 1.07-1.12 on scans, 0.95-0.97 under load.
- Items 52(a) and 55(b) are not exercised (no budget setting; 55(b) is opt-in and needs a cluster).
