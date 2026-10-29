# Build tracking: `b3bbcce19996` vs baseline `7562a5bdb7b9`

- Build: `server-1.0.0-b3bbcce19996` (contains `16edbb7` item 18 D9 node-load leak fix under concurrent identical
  queries, `d4a136f` D11 `shutdownDrainSeconds` default 20 s, `ab8cc3d` D10 distributed complete merges plain `avg`,
  `b3bbcce` subquery / CTE / UNION tables checked under authorization providers (no change without a provider),
  `786782219b1a` LZ4 codec module for Java Flight clients (separate jar, our clients do not load it: no slow-link
  pair)). Skipped as contained: `85a790826156`, `7b988c720821`, `2a2b8e08191f`, `786782219b1a`.
- Runs: core compare 40849716676 (wave `track-b3bbcce19996`, 6 jobs, 3 rounds, all green); item-18 cluster compare
  40849719732 (wave `track-b3bbcce19996-cluster`, `distributedComplete` off vs on, `rounds=2` in its own wave, job
  green, both rounds complete). Full tables: [run summary](../track-b3bbcce19996-40849716676/summary.md),
  [speed](../track-b3bbcce19996-40849716676/speed.md),
  [cluster](../track-b3bbcce19996-cluster-40849719732/robust.md).
- Pairs: A = baseline, B = candidate, same runner, 3 rounds (A B, B A, A B), containers as `COMPARE-TASK.md`.
  Ratio = B / A of the medians; times < 1 = candidate faster, MB/s > 1 = candidate faster.
- Correctness: TPC-H SF1 + SF10, ADBC + JDBC, local + S3: 22/22 for both sides in every round, no job disqualified,
  no OOM. 3-node cluster: 22/22 in every check, both modes.

## Regression check (rule: > 5 % slower on a core metric in all 3 rounds)

- No core metric is > 5 % slower in all 3 rounds.
- The build-8 watch item **local TPC-H SF10 ADBC is 1.03** (rounds 1.11 1.03 1.00; build 8: 1.06). Local SF10 JDBC
  1.06 (1.11 1.01 1.08): round 1 was slow for the candidate on both protocols, round 2 is level; under the rule.
- Local small JDBC c8 p95 / p99 1.07 / 1.10 (p95 rounds 1.09 1.09 1.03, p99 1.12 1.07 1.02): tail only, p50 0.93 at
  the same step; ADBC c8 p95 1.03. Under the rule; watch.
- Local small ADBC c32 p95 1.05 (1.07 1.08 0.98), JDBC c32 p99 1.05 (1.02 1.05 1.05): under the rule.
- S3 small JDBC c8 p50 1.09 (0.96 1.22 1.24; p95 0.98): not in all rounds (build-7 flag was 1.10, build 8 1.04).
- S3 small ADBC c32 0.67-0.69 and S3 SF10 JDBC 0.85: single slow baseline rounds (round 2), not gains.

## Core (default settings)

| metric | storage | A (baseline) | B (candidate) | B / A | per round |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC total s | local | 26.6 | 27.4 | 1.03 | 1.11 1.03 1.00 |
| TPC-H SF10 JDBC total s | local | 26.1 | 27.6 | 1.06 | 1.11 1.01 1.08 |
| TPC-H SF1 ADBC total s | local | 2.7 | 2.6 | 0.99 | 1.01 0.97 1.01 |
| TPC-H SF1 JDBC total s | local | 2.8 | 2.8 | 0.99 | 1.00 0.99 0.99 |
| TPC-H SF10 ADBC total s | S3 | 312.4 | 320.1 | 1.02 | 1.11 0.94 1.06 |
| TPC-H SF10 JDBC total s | S3 | 314.0 | 267.3 | 0.85 | 1.03 0.85 1.00 (noisy) |
| TPC-H SF1 ADBC total s | S3 | 26.8 | 26.7 | 1.00 | 0.99 1.02 0.99 |
| TPC-H SF1 JDBC total s | S3 | 26.6 | 26.5 | 1.00 | 1.00 0.99 1.01 |
| small ADBC c1 p50 / p95 / p99 ms | local | 13.0 / 36.3 / 43.3 | 11.6 / 34.7 / 44.9 | 0.89 / 0.96 / 1.04 | p50: 0.84 0.95 0.81 |
| small JDBC c1 p50 / p95 / p99 ms | local | 18.4 / 38.8 / 50.5 | 17.1 / 37.9 / 45.2 | 0.93 / 0.98 / 0.90 | p50: 0.93 0.93 0.99 |
| small ADBC c8 p50 / p95 / p99 ms | local | 85 / 242 / 336 | 79 / 249 / 348 | 0.93 / 1.03 / 1.04 | p95: 0.94 1.11 1.05 |
| small JDBC c8 p50 / p95 / p99 ms | local | 96 / 227 / 289 | 89 / 242 / 318 | 0.93 / 1.07 / 1.10 | p95: 1.09 1.09 1.03 |
| small ADBC c32 p50 / p95 / p99 ms | local | 348 / 1056 / 1441 | 335 / 1107 / 1486 | 0.97 / 1.05 / 1.03 | p95: 1.07 1.08 0.98 |
| small JDBC c32 p50 / p95 / p99 ms | local | 367 / 1027 / 1338 | 355 / 1036 / 1400 | 0.97 / 1.01 / 1.05 | p99: 1.02 1.05 1.05 |
| small ADBC c1 p50 / p95 / p99 ms | S3 | 27.6 / 871 / 911 | 23.4 / 839 / 910 | 0.85 / 0.96 / 1.00 | p50: 0.98 0.86 0.65 |
| small JDBC c1 p50 / p95 / p99 ms | S3 | 32.8 / 849 / 897 | 34.2 / 842 / 885 | 1.04 / 0.99 / 0.99 | p50: 0.92 1.05 1.07 |
| small ADBC c8 p50 / p95 / p99 ms | S3 | 382 / 6134 / 6587 | 351 / 6372 / 6918 | 0.92 / 1.04 / 1.05 | p95: 1.00 1.10 0.99 |
| small JDBC c8 p50 / p95 / p99 ms | S3 | 338 / 6546 / 6985 | 370 / 6387 / 6907 | 1.09 / 0.98 / 0.99 | p50: 0.96 1.22 1.24 |
| small ADBC c32 p50 / p95 / p99 ms | S3 | 1666 / 26626 / 31398 | 1122 / 18371 / 20580 | 0.67 / 0.69 / 0.66 | p95: 1.04 0.67 1.02 (noisy) |
| small JDBC c32 p50 / p95 / p99 ms | S3 | 1150 / 17923 / 28633 | 1118 / 19000 / 30466 | 0.97 / 1.06 / 1.06 | p95: 1.06 1.01 1.04 |
| scan 1 / 4 / 8 streams MB/s | local | 533 / 565 / 505 | 511 / 564 / 506 | 0.96 / 1.00 / 1.00 | x8: 1.00 0.98 1.01 |
| scan 1 / 4 / 8 streams MB/s | S3 | 386 / 421 / 400 | 383 / 434 / 402 | 0.99 / 1.03 / 1.01 | x8: 1.01 1.02 0.99 |
| lineitem export ADBC MB/s | local / S3 | 638 / 429 | 645 / 404 | 1.01 / 0.94 | S3: 1.00 0.93 1.00 |
| server peak RSS MB | core jobs | 710-2640 | 747-2632 | 0.90-1.05 | TPC-H local 0.90, S3 SF10 0.90-0.94, S3 SF1 1.05 |

The default path is level with the baseline, as in builds 6-8: small-query p50 0.85-0.97 except S3 JDBC c8, scans
0.96-1.03, TPC-H 0.99-1.06. Peak RSS 6-10 % lower in the SF10 jobs (local 1762 -> 1585 MB, S3 ADBC 1674 -> 1580,
S3 JDBC 1764 -> 1589); S3 SF1 +5 % (710 -> 747 MB, rounds 1.00 1.06 1.09).

## Item 18: 3-node cluster on S3, `distributedComplete` off (A) vs on (B), same build

| check (SF10 ADBC through node 1) | off: wall s (r1 r2) | on: wall s (r1 r2) | on / off | answers |
|---|---|---|---|---|
| all 3 nodes up | 297 441 (369) | 309 460 (385) | 1.04 (1.04 1.04) | 22/22 both |
| node 3 stopped | 298 461 (380) | 437 494 (466) | 1.23 (1.46 1.07) | 22/22 both |
| node 3 back | 299 467 (383) | 482 483 (483) | 1.26 (1.61 1.04) | 22/22 both |
| node 2 killed mid-query, dead | 298 476 (387) | 494 475 (485) | 1.25 (1.66 1.00) | 22/22 both |
| node 2 back | 297 402 (350) | 476 481 (479) | 1.37 (1.60 1.20) | 22/22 both |
| kill node 2 during q18 / q21 | ok / ok | ok / ok | | |
| first correct q06 after the kill, s | 59, 93 | 91, 104 | | |
| cluster start / node rejoin s | 20-22 / 5-7 | 19-20 / 6 | | |
| `docker stop` of node 3, s | 0.8-0.9 | 1.1 | | |

22/22 in every check in both modes and q18 / q21 survive the kill mid-query. With D10 (distributed complete merges
plain `avg`) the on side answers the `avg` queries (q01, q17, q22 among them) correctly in every check. With all nodes
up, on is 4 % slower than off in both rounds (build 8: 1.06, build 7: 1.01). After node changes on settles at
~475-495 s in both rounds; off is ~300 s in r1 but ~400-475 s in r2 (a slower second round for both sides, as in
build 7), so on / off is 1.46-1.66 in r1 and 1.00-1.20 in r2 (build 8: 1.54-1.61 in both). Recovery with on after the
kill is 91-104 s (build 8: 90-103 s; off 59-93 s). D11 (`shutdownDrainSeconds` default 20 s): `docker stop` of an
idle node takes ~1 s, so the drain does not delay a stop without queries in flight. `distributedComplete=true` is
still not faster on this setup (2 CPUs per node, one runner).

## Verdict

**Same.** Default path level with the baseline, 22/22 everywhere incl. the 3-node cluster with node loss (dc on and
off), no core metric > 5 % slower in all 3 rounds, peak RSS 0.90-1.05 (SF10 jobs -6-10 %). The build-8 watch item
local TPC-H SF10 ADBC is back to 1.03 (rounds 1.11 1.03 1.00). Watch: local small JDBC c8 p95 / p99 1.07 / 1.10
(p95 rounds 1.09 1.09 1.03; p50 0.93). Cluster: `distributedComplete=true` 1.04 of off with all nodes up, 1.23-1.37
after node changes (r2 1.00-1.20), recovery 91-104 s vs 59-93 s; still not faster.
