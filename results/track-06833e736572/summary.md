# Build tracking: `06833e736572` vs baseline `7562a5bdb7b9`

- Build: `server-1.0.0-06833e736572` (contains `fd6084f` item 18 D6: a peer lost after the first batch of a
  distributed complete answer fails as UNAVAILABLE; Ranger Hive policies P6 steps 1-3a (custom auth providers only);
  C4 step 3 Hive insert-only tables through the server). Skipped as contained: `01884e287668`.
- Runs: core compare 40823526868 (wave `track-06833e736572`, 6 jobs, 3 rounds, all green); item-18 cluster compare
  40823529991 (wave `track-06833e736572-cluster`, `distributedComplete` off vs on, `rounds=2` in its own wave, job
  green, both rounds complete). Full tables: [run summary](../track-06833e736572-40823526868/summary.md),
  [speed](../track-06833e736572-40823526868/speed.md),
  [cluster](../track-06833e736572-cluster-40823529991/robust.md).
- Pairs: A = baseline, B = candidate, same runner, 3 rounds (A B, B A, A B), containers as `COMPARE-TASK.md`.
  Ratio = B / A of the medians; times < 1 = candidate faster, MB/s > 1 = candidate faster.
- Correctness: TPC-H SF1 + SF10, ADBC + JDBC, local + S3: 22/22 for both sides in every round, no job disqualified,
  no OOM. 3-node cluster: 22/22 in every check, both modes.

## Regression check (rule: > 5 % slower on a core metric in all 3 rounds)

- No core metric is > 5 % slower in all 3 rounds.
- Local TPC-H SF10 ADBC 1.06 (rounds 1.03 1.06 1.07), JDBC 1.03 (1.02 1.03 1.05): under the rule, slightly up from
  1.03-1.04 in build 7. Watch in the next build.
- The build-7 flag **S3 small JDBC c8 p50 1.10 is not confirmed**: 1.04 (0.99 1.04 1.34); ADBC c8 p50 1.01
  (0.98 1.09 1.49). Round 3 of the S3 latency job was slow for the candidate at every step from 8 clients on
  (1.34-2.23), so its per-round values are noise.
- S3 small JDBC c1 p50 1.06 (1.05 1.04 1.12; 25.2 -> 26.8 ms): not in all rounds above 5 %, p95 / p99 1.01 / 0.97.
- S3 small JDBC c32 p99 1.83 (2.16 1.09 2.22): p99 of the noisy job, p50 0.87 and p95 1.02 at the same step.
- S3 TPC-H SF10 ADBC 0.65 (1.05 0.63 1.00): a slow baseline round 2, not a gain.

## Core (default settings)

| metric | storage | A (baseline) | B (candidate) | B / A | per round |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC total s | local | 39.6 | 42.1 | 1.06 | 1.03 1.06 1.07 |
| TPC-H SF10 JDBC total s | local | 40.3 | 41.5 | 1.03 | 1.02 1.03 1.05 |
| TPC-H SF1 ADBC total s | local | 4.1 | 4.1 | 0.99 | 0.99 1.01 0.99 |
| TPC-H SF1 JDBC total s | local | 4.2 | 4.2 | 0.99 | 1.01 0.99 0.99 |
| TPC-H SF10 ADBC total s | S3 | 477.5 | 309.5 | 0.65 | 1.05 0.63 1.00 (noisy) |
| TPC-H SF10 JDBC total s | S3 | 286.5 | 294.6 | 1.03 | 1.05 1.03 1.06 |
| TPC-H SF1 ADBC total s | S3 | 27.8 | 27.6 | 0.99 | 1.01 0.99 1.00 |
| TPC-H SF1 JDBC total s | S3 | 28.0 | 28.0 | 1.00 | 1.04 0.97 0.97 |
| small ADBC c1 p50 / p95 / p99 ms | local | 18.2 / 48.0 / 55.0 | 17.0 / 47.6 / 61.2 | 0.94 / 0.99 / 1.11 | p99: 1.11 0.99 1.20 |
| small JDBC c1 p50 / p95 / p99 ms | local | 25.8 / 50.7 / 57.1 | 26.2 / 52.8 / 65.5 | 1.01 / 1.04 / 1.15 | p99: 1.17 1.16 0.92 |
| small ADBC c8 p50 / p95 / p99 ms | local | 116 / 280 / 348 | 113 / 280 / 355 | 0.97 / 1.00 / 1.02 | p95: 0.99 1.03 0.98 |
| small JDBC c8 p50 / p95 / p99 ms | local | 130 / 289 / 410 | 125 / 293 / 363 | 0.96 / 1.01 / 0.89 | p95: 1.02 1.01 1.01 |
| small ADBC c32 p50 / p95 / p99 ms | local | 441 / 1320 / 1931 | 441 / 1313 / 1968 | 1.00 / 0.99 / 1.02 | p95: 0.96 1.04 0.98 |
| small JDBC c32 p50 / p95 / p99 ms | local | 488 / 1366 / 2007 | 477 / 1320 / 1954 | 0.98 / 0.97 / 0.97 | p95: 0.96 0.97 0.97 |
| small ADBC c1 p50 / p95 / p99 ms | S3 | 20.5 / 696 / 747 | 20.3 / 693 / 752 | 0.99 / 1.00 / 1.01 | p50: 0.94 0.91 1.14 |
| small JDBC c1 p50 / p95 / p99 ms | S3 | 25.2 / 680 / 744 | 26.8 / 689 / 724 | 1.06 / 1.01 / 0.97 | p50: 1.05 1.04 1.12 |
| small ADBC c8 p50 / p95 / p99 ms | S3 | 254 / 3779 / 4136 | 257 / 3772 / 4240 | 1.01 / 1.00 / 1.03 | p50: 0.98 1.09 1.49 |
| small JDBC c8 p50 / p95 / p99 ms | S3 | 257 / 3768 / 4134 | 268 / 3790 / 4133 | 1.04 / 1.01 / 1.00 | p50: 0.99 1.04 1.34 |
| small ADBC c32 p50 / p95 / p99 ms | S3 | 897 / 13071 / 14291 | 981 / 12962 / 14630 | 1.09 / 0.99 / 1.02 | p95: 0.98 0.99 1.71 |
| small JDBC c32 p50 / p95 / p99 ms | S3 | 994 / 13772 / 16998 | 868 / 14090 / 31134 | 0.87 / 1.02 / 1.83 | p99: 2.16 1.09 2.22 (noisy) |
| scan 1 / 4 / 8 streams MB/s | local | 436 / 460 / 421 | 414 / 457 / 415 | 0.95 / 0.99 / 0.99 | x8: 0.99 0.98 0.99 |
| scan 1 / 4 / 8 streams MB/s | S3 | 569 / 641 / 606 | 563 / 642 / 593 | 0.99 / 1.00 / 0.98 | x8: 0.99 0.95 0.98 |
| lineitem export ADBC MB/s | local / S3 | 532 / 533 | 521 / 570 | 0.98 / 1.07 | S3: 1.07 0.94 1.03 |
| server peak RSS MB | core jobs | 728-2858 | 734-2771 | 0.88-1.01 | TPC-H local 0.88, S3 SF10 0.96-0.97 |

The default path is level with the baseline, as in builds 6 and 7: small queries 0.94-1.01 at p50 and p95 locally,
scans 0.95-0.99. Peak RSS is 12 % lower in the local TPC-H job (1733 -> 1528 MB, 0.88-0.92 in every round).

## Item 18: 3-node cluster on S3, `distributedComplete` off (A) vs on (B), same build

| check (SF10 ADBC through node 1) | off: wall s (r1 r2) | on: wall s (r1 r2) | on / off | answers |
|---|---|---|---|---|
| all 3 nodes up | 320 459 (390) | 351 478 (414) | 1.06 (1.10 1.04) | 22/22 both |
| node 3 stopped | 314 327 (321) | 505 502 (504) | 1.57 (1.61 1.53) | 22/22 both |
| node 3 back | 318 319 (318) | 489 489 (489) | 1.54 (1.54 1.53) | 22/22 both |
| node 2 killed mid-query, dead | 311 314 (313) | 507 502 (505) | 1.61 (1.63 1.60) | 22/22 both |
| node 2 back | 309 313 (311) | 489 502 (496) | 1.59 (1.58 1.60) | 22/22 both |
| kill node 2 during q18 / q21 | ok / ok | ok / ok | | |
| first correct q06 after the kill, s | 59, 59 | 90, 103 | | |
| cluster start / node rejoin s | 20-21 / 6 | 20-21 / 5-6 | | |

22/22 in every check in both modes and q18 / q21 survive the kill mid-query; the D6 change (peer lost after the first
batch fails as UNAVAILABLE) shows no wrong or partial answer. With all nodes up, on is 6 % slower than off in both
rounds (1.10 1.04; build 7: 1.01, build 6: 1.03). After any node change the on side settles at ~490-505 s in both
rounds while off now stays at ~310-330 s in both rounds (build 7: off ~300 s r1 / ~475 s r2), so the on / off gap is
1.54-1.61 here. Recovery with on after the kill is 90-103 s (build 7: 96 s; off 59 s). `distributedComplete=true` is
still not faster on this setup (2 CPUs per node, one runner).

## Verdict

**Same.** Default path level with the baseline, 22/22 everywhere incl. the 3-node cluster with node loss (dc on and
off), no core metric > 5 % slower in all 3 rounds, peak RSS 0.88-1.01 (local TPC-H -12 %). The build-7 flag S3 small
JDBC c8 p50 1.10 is not confirmed (1.04, rounds 0.99 1.04 1.34). Local TPC-H SF10 ADBC 1.06 (1.03 1.06 1.07) is under
the rule but the highest since build 5; watch in the next build. Cluster: `distributedComplete=true` 1.06 of off with
all nodes up and 1.54-1.61 after node changes; recovery 90-103 s vs 59 s; still not faster.
