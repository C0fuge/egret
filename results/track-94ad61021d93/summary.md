# Build tracking: `94ad61021d93` vs baseline `7562a5bdb7b9`

- Build: `server-1.0.0-94ad61021d93` (contains `a9e43ca5e296` item 19b step 1 DuckDB threads + memory limit by host
  size, `fd9f62f` item 19b step 2 opt-in `duckDbThreadsWhenIdle`, `ffcbabf` / `c7e436e` item 18 step 3 off-vs-on
  counters and backup fail-over, `ea55a4f` item 17 (a) opt-in S3 cache disk tier). Skipped as contained:
  `a9e43ca5e296`, `177dfe3e5716`, `f73de96b8773`, `c258adf27dc9`, `1b3a7bbad4bc` (plugins / auth).
- Run: compare 40699820075 (wave `track-94ad61021d93`), 8 of 9 jobs green; `i18-dc-off-vs-on` hit the 170-min job
  limit in round 3 (each cluster side-round takes 28-45 min), its 2 complete rounds (A B, B A) are reported.
  Load and cluster tables via re-report 40728485498. Full tables: [run summary](../track-94ad61021d93-40699820075/summary.md),
  [speed](../track-94ad61021d93-40699820075/speed.md), [load](../track-94ad61021d93-40699820075/load.md),
  [cluster](../track-94ad61021d93-40699820075/robust.md).
- Pairs: A = baseline (or the named reference), B = candidate, same runner, 3 rounds (A B, B A, A B), containers as
  `COMPARE-TASK.md`. Ratio = B / A of the medians; times < 1 = candidate faster, MB/s and q/s > 1 = candidate faster.
- Correctness: TPC-H SF1 + SF10, ADBC + JDBC, local + S3, and the 3-node cluster in every check: 22/22, no job
  disqualified, no OOM.

## Regression check (rule: > 5 % slower on a core metric in all 3 rounds)

- **S3 small queries, ADBC c1 tail: p95 1.08 (rounds 1.07 1.09 1.05; 779 -> 838 ms), p99 1.09 (1.19 1.09 1.06).**
  JDBC c1 p95 1.01 (1.05 1.05 0.97), and c8 / c32 tails are 0.69-1.04, so it is limited to ADBC at one client. Small.
- The build-3 flag (S3 ADBC c1 p50 1.25) is not confirmed: p50 1.14 with rounds 1.61 1.14 0.80 (no consistent
  direction); JDBC c1 p50 0.99.
- Local TPC-H SF10 is slightly slower in every round but under the rule: ADBC 1.04 (1.02 1.04 1.01), JDBC 1.02
  (1.02 1.02 1.02). The item 19b memory limit costs part of it (see below).

## Core (default settings)

| metric | storage | A (baseline) | B (candidate) | B / A | per round |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC total s | local | 37.6 | 38.9 | 1.04 | 1.02 1.04 1.01 |
| TPC-H SF10 JDBC total s | local | 37.6 | 38.3 | 1.02 | 1.02 1.02 1.02 |
| TPC-H SF1 ADBC total s | local | 3.9 | 3.6 | 0.91 | 0.92 0.92 0.89 |
| TPC-H SF1 JDBC total s | local | 4.0 | 3.6 | 0.90 | 0.90 0.91 0.91 |
| TPC-H SF10 ADBC total s | S3 | 485.3 | 308.3 | 0.64 | 1.03 0.63 0.98 |
| TPC-H SF10 JDBC total s | S3 | 499.9 | 328.9 | 0.66 | 0.99 0.66 0.99 |
| TPC-H SF1 ADBC total s | S3 | 23.9 | 25.2 | 1.05 | 1.05 1.07 0.94 |
| TPC-H SF1 JDBC total s | S3 | 24.7 | 24.6 | 0.99 | 1.18 0.69 0.99 |
| small ADBC c1 p50 / p95 ms | local | 19.0 / 47.6 | 18.4 / 47.0 | 0.97 / 0.99 | p50: 0.88 0.98 0.95 |
| small JDBC c1 p50 ms | local | 28.9 | 26.1 | 0.90 | 0.93 0.90 0.95 |
| small ADBC c8 p50 / p95 / p99 ms | local | 118 / 293 / 367 | 87 / 290 / 328 | 0.74 / 0.99 / 0.90 | p95: 1.05 0.93 1.03 |
| small JDBC c8 p50 / p95 ms | local | 131 / 308 | 102 / 301 | 0.77 / 0.98 | p95: 1.00 0.98 1.00 |
| small ADBC c32 p50 / p95 / p99 ms | local | 450 / 1360 / 1857 | 363 / 1189 / 1427 | 0.81 / 0.87 / 0.77 | p95: 0.90 0.85 0.88 |
| small JDBC c32 p50 / p95 / p99 ms | local | 487 / 1375 / 1870 | 393 / 1243 / 1822 | 0.81 / 0.90 / 0.97 | p95: 0.89 0.90 0.92 |
| small ADBC c1 p50 / p95 / p99 ms | S3 | 22.7 / 779 / 831 | 25.9 / 838 / 904 | 1.14 / **1.08** / **1.09** | p95: **1.07 1.09 1.05** |
| small JDBC c1 p50 / p95 ms | S3 | 31.1 / 788 | 30.7 / 794 | 0.99 / 1.01 | p95: 1.05 1.05 0.97 |
| small ADBC c32 p95 ms | S3 | 23721 | 16388 | 0.69 | 1.01 0.67 1.09 |
| small JDBC c32 p95 ms | S3 | 17395 | 16711 | 0.96 | 0.96 0.97 0.98 |
| scan 1 / 4 / 8 streams MB/s | local | 426 / 437 / 410 | 388 / 468 / 485 | 0.91 / 1.07 / **1.18** | x8: 1.17 1.18 1.18 |
| scan 1 / 4 / 8 streams MB/s | S3 | 395 / 445 / 435 | 392 / 457 / 434 | 0.99 / 1.03 / 1.00 | x8: 1.02 0.98 0.99 |
| lineitem export ADBC MB/s | local / S3 | 505 / 445 | 516 / 442 | 1.02 / 0.99 | |
| server peak RSS MB | core jobs | 775-2689 | 781-2765 | 0.87-1.03 | TPC-H local 0.88, S3 SF10 0.87-0.93 |

S3 SF10 again has one slow baseline round per job (as in builds 1-3); the other rounds are 0.98-1.03, so S3 SF10 is
"same". Local scan x1 0.91 (0.92 0.89 0.99) is not in the rule (> 5 % in all rounds fails in round 3).

## Item 19b: DuckDB threads + memory limit by host size

| pair (same runner) | metric | A | B | B / A | per round |
|---|---|---|---|---|---|
| `duckDbMemoryLimit=none` (A) vs sized default (B) | TPC-H SF10 ADBC total s | 39.2 | 40.3 | 1.03 | 1.03 1.02 1.03 |
| same | server peak RSS MB | 3126 | 2749 | **0.88** | 0.88 0.88 0.88 |
| same | 4 heavy SF10 at once, slowest query s | | 18.1 (both sides pooled) | q09 ~1.07 (job log) | 0 failed |
| baseline (A) vs candidate (B), closed-loop load JDBC | peak q/s (c8) | 67 | 72 | **1.07** | |
| same, ADBC | peak q/s (c8) | 67 | 71 | **1.06** | |
| same, JDBC / ADBC | q/s at 128 clients | 48 / 49 | 59 / 58 | **1.23 / 1.18** | |
| same, JDBC / ADBC | p95 ms at 32 clients | 899 / 975 | 832 / 885 | 0.93 / 0.91 | |
| same | load peak RSS MB | 4855 | 5146 | 1.06 | 1.07 1.04 1.03 |

The sized memory limit caps peak RSS 12 % lower for a 2-3 % SF10 cost; load +6-7 % at the peak and +18-23 % at 128
clients against the baseline (saturation point unchanged at 1 client, p95 < 100 ms rule), 0 errors.

## Item 18: 3-node cluster on S3, `distributedComplete` off (A) vs on (B), same build, 2 complete rounds

| check (SF10 ADBC through node 1) | off: wall s (r1 r2) | on: wall s (r1 r2) | on / off | answers |
|---|---|---|---|---|
| all 3 nodes up | 314 488 (401) | 369 478 (424) | 1.06 (1.18 0.98) | 22/22 both |
| node 3 stopped | 317 503 (410) | 522 526 (524) | 1.28 (1.65 1.05) | 22/22 both |
| node 3 back | 316 500 (408) | 521 521 (521) | 1.28 | 22/22 both |
| node 2 killed mid-query, dead | 314 519 (416) | 526 535 (530) | 1.27 | 22/22 both |
| node 2 back | 318 513 (416) | 527 518 (522) | 1.26 | 22/22 both |
| kill node 2 during q18 / q21 | ok / ok | ok / ok | | |
| first correct q06 after the kill, s | 63, 100 | 103, 104 | | |

Both modes answer 22/22 in every check, also with a node stopped or killed mid-query (backup fail-over of item 18
step 3 works). With distributed complete on, the cluster is not faster on SF10 here (2 CPUs per node, one runner)
and is ~520 s with any node change versus 315-500 s off; the off side varies a lot between rounds (r1 ~315 s, r2
~500 s), so only 2 noisy rounds: on is equal-or-slower, not faster. The job needs a longer limit or fewer checks for
3 rounds (see README).

## Verdict

**Better, with one small S3 tail point.** Load +6-7 % at the peak and +18-23 % at 128 clients (item 19b), local small
p50 at 8/32 clients 19-26 % faster and c32 p95/p99 10-23 % better, SF1 9-10 % faster, scan 8 streams +18 %, peak RSS
up to 12-13 % lower; 22/22 everywhere including the 3-node cluster with node loss. Local SF10 1.02-1.04 (under the
rule, partly the memory-limit cost). **Small regression: S3 small ADBC c1 p95 1.08 / p99 1.09 in all 3 rounds; JDBC
and c8/c32 not affected.** The build-3 S3 ADBC c1 p50 flag is not confirmed. `distributedComplete=true` is
correct but not faster than off on this setup.
