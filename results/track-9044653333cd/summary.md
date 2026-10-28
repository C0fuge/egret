# Build tracking: `9044653333cd` vs baseline `7562a5bdb7b9`

- Build: `server-1.0.0-9044653333cd` (contains `936b2d7` item 21 `duckDbThreadsUnderLoad` fix, `a110a22` / `aef0a7a` /
  `9044653` item 18 D3 steps 1-2b (no wait for a crashed cluster member), `9efe670` item 19b thread floor 4, Hive
  views, Iceberg time travel via Hive). Skipped as contained: `a110a2279437`, `0f8eb5e5f65c` (catalog CI probe only),
  `936b2d7c366c`.
- Runs: core compare 40772221252 (wave `track-9044653333cd`, 8 jobs incl. `i19b-memnone-vs-sized` and `i21-load`,
  3 rounds, all green); item-18 cluster compare 40772225000 (wave `track-9044653333cd-cluster`, `distributedComplete`
  off vs on, `rounds=2` in its own wave, job green, both rounds complete). Full core tables:
  [run summary](../track-9044653333cd-40772221252/summary.md), [speed](../track-9044653333cd-40772221252/speed.md),
  [load](../track-9044653333cd-40772221252/load.md), [cluster](../track-9044653333cd-cluster-40772225000/robust.md).
- Pairs: A = baseline (or the named reference), B = candidate, same runner, 3 rounds (A B, B A, A B), containers as
  `COMPARE-TASK.md`. Ratio = B / A of the medians; times < 1 = candidate faster, MB/s and q/s > 1 = candidate faster.
- Correctness: TPC-H SF1 + SF10, ADBC + JDBC, local + S3: 22/22 for both sides in every round, no job disqualified,
  no OOM; S3 SF10 ADBC result checksum identical in all 6 side-rounds (`c9c83daae5eb`). 3-node cluster: 22/22 in
  every check, both modes.

## Regression check (rule: > 5 % slower on a core metric in all 3 rounds)

- **S3 TPC-H SF10 ADBC total 1.10 (rounds 1.06 1.10 1.21; 260.5 -> 285.7 s, sum of warm medians).** Per side-round
  (job log): A 258.4 / 260.5 / 318.2 s, B 274.0 / 285.7 / 386.3 s; round 2 ran B first, so it is not the run order.
  Round 3 is slow for both sides (runner drift), B more. Cold sums are mixed (B 265.9 / 295.0 / 393.7 vs A 282.0 /
  261.7 / 326.4: round 1 B faster). S3 SF10 JDBC in the same build on the same runner type is 0.97 (0.97 1.00 1.03)
  and S3 SF1 ADBC 0.99, so it is limited to SF10 over ADBC on S3. Earlier builds had one slow *baseline* round per
  S3 SF10 job; here all three rounds lean against the candidate, so it counts under the rule. Small; re-check in the
  next build's S3 SF10 ADBC job.
- The build-5 flag **S3 TPC-H SF1 JDBC 1.14 is gone**: 0.97 (0.99 1.00 0.95).
- Local TPC-H SF10 is back down: ADBC 1.04 (1.04 1.05 1.04), JDBC 1.04 (1.03 1.05 1.06), from 1.10 / 1.07 in build 5
  (19b thread floor `9efe670`). Under the rule.
- **Item 21: the load gain of builds 2 and 4 is not seen.** Closed-loop load is equal to the baseline (JDBC peak 42 vs
  43 q/s, c128 35 vs 34; ADBC peak 43 vs 43, c128 32 vs 33). Builds 2 and 4 had +5-7 % at the peak and +15-23 % at 128
  clients on the same job. Not slower than the baseline, so no regression under the rule, but the
  `duckDbThreadsUnderLoad` change does not add throughput here, and the earlier gain is lost.

## Core (default settings)

| metric | storage | A (baseline) | B (candidate) | B / A | per round |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC total s | local | 40.2 | 41.7 | 1.04 | 1.04 1.05 1.04 |
| TPC-H SF10 JDBC total s | local | 40.9 | 42.4 | 1.04 | 1.03 1.05 1.06 |
| TPC-H SF1 ADBC total s | local | 4.2 | 4.1 | 0.98 | 0.99 0.98 0.96 |
| TPC-H SF1 JDBC total s | local | 4.2 | 4.2 | 0.98 | 1.01 1.00 0.96 |
| TPC-H SF10 ADBC total s | S3 | 260.5 | 285.7 | **1.10** | **1.06 1.10 1.21** |
| TPC-H SF10 JDBC total s | S3 | 309.9 | 302.2 | 0.97 | 0.97 1.00 1.03 |
| TPC-H SF1 ADBC total s | S3 | 24.1 | 23.9 | 0.99 | 1.03 0.96 0.99 |
| TPC-H SF1 JDBC total s | S3 | 24.6 | 23.9 | 0.97 | 0.99 1.00 0.95 |
| small ADBC c1 p50 / p95 / p99 ms | local | 11.8 / 30.9 / 37.9 | 10.8 / 28.5 / 39.8 | 0.92 / 0.92 / 1.05 | p50: 0.74 0.97 0.95 |
| small JDBC c1 p50 / p95 ms | local | 17.9 / 35.0 | 15.2 / 31.8 | 0.85 / 0.91 | p50: 0.72 1.16 0.85 |
| small ADBC c8 p50 / p95 / p99 ms | local | 75 / 187 / 233 | 69 / 187 / 226 | 0.92 / 1.00 / 0.97 | p95: 0.87 1.04 1.00 |
| small JDBC c8 p50 / p95 ms | local | 85 / 194 | 78 / 200 | 0.91 / 1.03 | p95: 0.89 1.11 1.03 |
| small ADBC c32 p50 / p95 / p99 ms | local | 312 / 929 / 1303 | 285 / 915 / 1256 | 0.91 / 0.98 / 0.96 | p95: 0.88 1.05 0.98 |
| small JDBC c32 p50 / p95 / p99 ms | local | 319 / 910 / 1190 | 305 / 857 / 1218 | 0.96 / 0.94 / 1.02 | p95: 0.94 0.94 0.94 |
| small ADBC c1 p50 / p95 / p99 ms | S3 | 28.3 / 687 / 1145 | 26.0 / 667 / 715 | 0.92 / 0.97 / 0.62 | p95: 0.96 0.98 0.94 |
| small JDBC c1 p50 / p95 ms | S3 | 36.2 / 681 | 34.4 / 697 | 0.95 / 1.02 | p95: 1.02 1.02 1.01 |
| small ADBC c8 p50 / p95 ms | S3 | 301 / 5553 | 328 / 5531 | 1.09 / 1.00 | p50: 1.21 1.00 1.22 |
| small JDBC c8 p50 / p95 / p99 ms | S3 | 315 / 5593 / 6636 | 307 / 5362 / 6018 | 0.97 / 0.96 / 0.91 | p95: 0.91 0.94 1.05 |
| small ADBC c32 p95 ms | S3 | 17670 | 17104 | 0.97 | 1.00 0.97 1.00 |
| small JDBC c32 p95 / p99 ms | S3 | 17861 / 24292 | 18352 / 27971 | 1.03 / 1.15 | p99: 0.83 1.40 0.85 (noisy) |
| scan 1 / 4 / 8 streams MB/s | local | 639 / 667 / 617 | 668 / 729 / 629 | 1.05 / 1.09 / 1.02 | x8: 1.04 1.00 1.04 |
| scan 1 / 4 / 8 streams MB/s | S3 | 399 / 442 / 438 | 385 / 435 / 421 | 0.96 / 0.98 / 0.96 | x8: 1.00 0.96 0.95 |
| lineitem export ADBC MB/s | local / S3 | 777 / 439 | 756 / 440 | 0.97 / 1.00 | |
| server peak RSS MB | core jobs | 751-2781 | 747-2699 | 0.89-0.99 | TPC-H local 0.91, S3 SF10 JDBC 0.89 |

The local latency job ran on a faster runner type than in builds 1-5 (absolute times lower for both sides). Its round
2 is slow for B at every step (p50 c1 JDBC 1.16), so the local small-query picture is "same-or-better" rather than
the 20-28 % p50 gain at 8/32 clients of builds 2-5 (here 4-9 %). S3 small ADBC c8 p50 1.09 (1.21 1.00 1.22) is not in
all 3 rounds; p95 is 1.00.

## Item 21: closed-loop load, local SF10 (baseline A vs candidate B)

| clients | JDBC q/s A / B | JDBC p95 ms A / B | ADBC q/s A / B | ADBC p95 ms A / B |
|---|---|---|---|---|
| 1 | 38 / 38 | 44.9 / 43.8 | 41 / 40 | 39.6 / 39.7 |
| 8 | 43 / 42 | 282 / 287 | 43 / 43 | 278 / 282 |
| 32 | 40 / 40 | 1340 / 1329 | 39 / 39 | 1358 / 1398 |
| 64 | 38 / 38 | 2999 / 3032 | 36 / 37 | 3048 / 3176 |
| 128 | 34 / 35 | 6850 / 7074 | 33 / 32 | 6403 / 6615 |

Saturation (p95 < 100 ms, 0 errors): 1 client on both sides. 0 errors at every step. Peak RSS 4512 vs 4458 MB (0.99).
Builds 2 and 4 measured +5-7 % at the peak and +15-23 % at 128 clients on the same job; with the `duckDbThreadsUnderLoad`
fix the candidate is level with the baseline.

## Item 19b: sized DuckDB memory limit (B, default) vs `-DduckDbMemoryLimit=none` (A), same build

| metric | none (A) | sized (B) | B / A | per round |
|---|---|---|---|---|
| TPC-H SF10 ADBC total s, local | 39.3 | 41.4 | 1.05 | 1.04 1.06 1.06 |
| server peak RSS MB (incl. 4 heavy at once) | 2768 | 2846 | 1.03 | 1.01 1.05 1.03 |
| 4 heavy SF10 at once (sized): slowest s / failures | | 17.8 / 0 | | |

In build 4 the sized limit cut peak RSS by 12 % for 2-3 % SF10. With the thread floor of 4 (`9efe670`) it no longer
lowers peak RSS here (1.03) and still costs 5 % on SF10.

## Item 18: 3-node cluster on S3, `distributedComplete` off (A) vs on (B), same build

| check (SF10 ADBC through node 1) | off: wall s (r1 r2) | on: wall s (r1 r2) | on / off | answers |
|---|---|---|---|---|
| all 3 nodes up | 291 430 (361) | 298 445 (372) | 1.03 (1.02 1.04) | 22/22 both |
| node 3 stopped | 286 451 (368) | 399 463 (431) | 1.17 (1.39 1.03) | 22/22 both |
| node 3 back | 281 455 (368) | 467 473 (470) | 1.28 (1.66 1.04) | 22/22 both |
| node 2 killed mid-query, dead | 291 463 (377) | 460 468 (464) | 1.23 (1.58 1.01) | 22/22 both |
| node 2 back | 295 452 (374) | 464 461 (462) | 1.24 (1.57 1.02) | 22/22 both |
| kill node 2 during q18 / q21 | ok / ok | ok / ok | | |
| first correct q06 after the kill, s | 65, 89 | 96, 90 | | |
| cluster start / node rejoin s | 23-24 / 6 | 21 / 6-7 | | |

Both modes answer 22/22 in every check, also with a node stopped or killed mid-query, and q18 / q21 survive the kill.
With all nodes up, on is now level with off (1.03; build 5: 1.13). After any node change the on side settles at
~460-470 s in both rounds while off stays at ~290 s (r1) / ~455 s (r2), so on is still not faster on this setup (2 CPUs
per node, one runner). Recovery with on after the kill is 90-96 s (build 5: 104-109 s; off 65-89 s): the D3 "no wait
for a crashed member" steps shorten it, but it is still not below off.

## Verdict

**Same overall, with one small S3 point.** 22/22 everywhere, peak RSS 1-11 % lower, local SF10 back to 1.04 from
1.07-1.10, the build-5 S3 SF1 JDBC flag gone, local scan x4 +9 %. **Small regression: S3 TPC-H SF10 ADBC total 1.10
in all 3 rounds (1.06 1.10 1.21); JDBC on S3 not affected (0.97).** The item-21 change does not raise closed-loop load
(level with the baseline; the +5-7 % peak gain of builds 2 and 4 is not seen), and the item-19b sized memory limit no
longer saves memory with the new thread floor. Cluster: 22/22 with node loss in both modes; `distributedComplete=true`
level with off when all nodes are up and recovers faster than in build 5, but is still not faster than off.
