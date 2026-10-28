# Build tracking: `d22cdaccb4e1` vs baseline `7562a5bdb7b9`

- Build: `server-1.0.0-d22cdaccb4e1` (item 20 (b) LZ4 Flight streams; contains ZSTD streams, item 19 threads default,
  item 17 (b)-(d), Iceberg items). Skipped as contained: `84fec772ec50` `8625e28f08cd` `b28fedf9edbf` `752e272b3ab6`
  `04e558056068` `4e77c6bda59a` `b7be8d166498` `85aaf4604d9a`.
- Runs: compare 40602868592 (wave `track-load-d22cdaccb4e1`, 13 of 14 jobs) + 40621069419 (the S3 TPC-H job split in
  three after it hit the 170 min limit). Full tables: [run 40621069419](../track-load-d22cdaccb4e1-40621069419/summary.md)
  (all jobs merged), [load / netem report](../track-load-d22cdaccb4e1-40602868592/load.md).
- Pairs: A = baseline, B = candidate, same runner, 3 rounds (A B, B A, A B), containers as `COMPARE-TASK.md`.
  Ratio = B / A of the medians; times < 1 = candidate faster, MB/s > 1 = candidate faster.
- Correctness: TPC-H SF1 + SF10, ADBC + JDBC, local + S3: **22/22 in every round** for both builds; no job disqualified.

## Regression (rule: > 5 % slower on a core metric in all 3 rounds)

**S3, small queries, tail latency under concurrency: JDBC c32 p95 1.21 (rounds 1.13 1.27 1.13), JDBC c8 p95 1.12
(1.18 1.12 1.36), ADBC c8 p95 1.20 (1.20 1.19 1.31).** The p50 at the same steps is clearly faster (JDBC c32 p50 0.67,
ADBC c8 p50 0.65), so the candidate answers most small S3 queries sooner but lets a slower tail build up. Local disk shows no
such tail (c8/c32 p95 0.86-1.05). Not seen in any other core metric.

## Core (default settings)

| metric | storage | A (baseline) | B (candidate) | B / A | per round |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC total s | local | 39.3 | 38.6 | 0.98 | 0.98 0.98 0.98 |
| TPC-H SF10 JDBC total s | local | 38.8 | 38.5 | 0.99 | 0.99 0.98 0.99 |
| TPC-H SF1 ADBC total s | local | 4.0 | 3.7 | 0.94 | 0.94 0.94 0.94 |
| TPC-H SF10 ADBC total s | S3 (split job) | 316.7 | 266.6 | 0.84 | 1.03 0.83 0.91 |
| TPC-H SF10 JDBC total s | S3 (split job) | 451.9 | 269.3 | 0.60 | 0.86 0.60 0.83 |
| TPC-H SF1 ADBC total s | S3 (split job) | 24.2 | 25.3 | 1.04 | 1.08 0.99 1.04 |
| TPC-H SF1 JDBC total s | S3 (split job) | 23.9 | 24.6 | 1.03 | 1.02 1.03 1.03 |
| small ADBC c1 p50 ms | local | 17.8 | 16.7 | 0.94 | 0.84 1.00 0.91 |
| small ADBC c32 p95 ms | local | 1341.5 | 1175.8 | 0.88 | 0.89 0.91 0.82 |
| small JDBC c32 p95 ms | local | 1408.4 | 1217.4 | 0.86 | 0.90 0.92 0.86 |
| small ADBC c1 p50 ms | S3 | 24.2 | 21.2 | 0.88 | 0.86 0.95 0.79 |
| small ADBC c32 p95 ms | S3 | 24285 | 19816 | 0.82 | 1.22 0.81 1.11 |
| small JDBC c32 p95 ms | S3 | 16787 | 20322 | **1.21** | 1.13 1.27 1.13 |
| scan 1 / 4 / 8 streams MB/s | local | 444 / 495 / 458 | 442 / 530 / 528 | 1.00 / 1.07 / **1.15** | x8: 1.15 1.15 1.12 |
| scan 1 / 4 / 8 streams MB/s | S3 | 414 / 483 / 462 | 416 / 494 / 508 | 1.01 / 1.02 / **1.10** | x8: 1.10 1.09 1.10 |
| server peak RSS MB | all core jobs | 801-2814 | 877-2572 | 0.91-1.14 | |

S3 TPC-H totals are noisy between runners (baseline SF10 JDBC 452 s on one runner, 490 s on another); the split jobs and the
original S3 job (SF10 ADBC 0.89, JDBC 0.82) agree that the candidate is not slower on S3. With `-DduckDbThreads=4` on both
sides (the candidate's new default is the baseline's explicit setting) everything is 0.96-1.05: no change.

## Item 20: slow link (netem 10 ms RTT, 1 Gbit/s), full lineitem export over ADBC

| pair (A vs B) | export MB/s A | B | B / A | per round | TPC-H SF10 ADBC B / A | answers A / B |
|---|---|---|---|---|---|---|
| baseline plain vs candidate plain | 104 | 104 | 1.00 | 1.00 1.00 1.00 | 1.00 | 22 / 22 |
| baseline plain vs candidate CLZ4 | 104 | 261 | **2.51** | 2.51 2.51 2.51 | 1.00 | 22 / 22 |
| baseline plain vs candidate CZSTD | 104 | 361 | **3.46** | 3.43 3.47 3.47 | 1.02 | 22 / 22 |
| candidate CZSTD vs candidate CLZ4 | 345 | 261 | 0.76 | 0.73 0.76 0.76 | 0.97 | 22 / 22 |
| candidate CZSTD vs upstream native ZSTD | 223 | 260 | 1.16 | 1.15 1.17 1.15 | n/a | 22 / 0 |
| candidate CLZ4 vs upstream native ZSTD | 260 | 256 | 0.99 | 0.99 0.97 0.99 | n/a | 22 / 0 |

Upstream native answers 0/22 TPC-H queries on this path (upstream side, as in Report 1); its export reference is 256-260
MB/s (264 in Report 2). The candidate's ZSTD speed depends on the runner CPU (compression runs on the server's 2 cores):
361 and 345 MB/s on EPYC 9V45 runners, 223 MB/s on an EPYC 7763 runner, where upstream native ZSTD is 1.16x faster.

Fast local link (no netem): asking for compression costs throughput - lineitem export CZSTD 0.47x, CLZ4 0.67x of plain;
TPC-H SF10 ADBC unchanged (1.00 / 0.98). Compression is only requested by the client, so the default path is unaffected.

## Verdict

**Better, with one flagged regression**: slow-link export 2.5x (LZ4) / 3.5x (ZSTD) when the client asks for compression,
scan 8 streams +10-15 %, small-query p50 6-12 % faster, TPC-H same or faster, 22/22 everywhere, peak RSS within
-9 % / +14 %. Regression: S3 small-query p95 at 8 and 32 clients 12-21 % slower in all rounds (see above).
