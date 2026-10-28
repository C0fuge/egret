# Build tracking: `2cfa23eb62f9` vs baseline `7562a5bdb7b9`

- Build: `server-1.0.0-2cfa23eb62f9` (contains `eb82020` item 18 / D2 (c) part 1 two-process distributed complete with
  TLS + token auth, opt-in `dataDirShared`; `3042102` item 13 (c) external file cache bound line; `411e804` item 3 (c)
  Iceberg time travel; Hive Avro plugin). Still has the item 19b thread defaults (the fix `9efe670` is not released yet).
- Runs: core compare 40736482953 (wave `track-2cfa23eb62f9`, 6 jobs, 3 rounds, all green); item-18 cluster compare
  40736487295 (wave `track-2cfa23eb62f9-cluster`, `distributedComplete` off vs on, `rounds=2` because of the 170-min
  job limit). Full core tables: [run summary](../track-2cfa23eb62f9-40736482953/summary.md),
  [speed](../track-2cfa23eb62f9-40736482953/speed.md).
- Pairs: A = baseline, B = candidate, same runner, 3 rounds (A B, B A, A B), containers as `COMPARE-TASK.md`.
  Ratio = B / A of the medians; times < 1 = candidate faster, MB/s > 1 = candidate faster.
- Correctness: TPC-H SF1 + SF10, ADBC + JDBC, local + S3: 22/22 for both sides in every round, result checksums of
  A and B identical (S3 SF1: JDBC `de713f9eea2f`, ADBC `090124efed2e` in all 6 side-rounds); no job disqualified, no OOM.

## Regression check (rule: > 5 % slower on a core metric in all 3 rounds)

- **S3 TPC-H SF1 JDBC total 1.14 (rounds 1.21 1.05 1.14; 26.9 -> 30.5 s, sum of warm medians).** The cold sums are
  not slower (B 24.4 / 27.7 / 26.0 s vs A 25.4 / 28.3 / 25.9 s), SF1 ADBC on the same runner is 1.04 (1.05 0.76 1.08)
  and S3 SF10 JDBC is 0.82 (1.01 0.82 1.01), so it is limited to warm repeats of the short SF1 queries over JDBC on
  S3. Small; per-query split only in the raw artifact (the speed report has no column for the candidate).
- Local TPC-H SF10 is slower than in build 4 but still under the rule: ADBC 1.10 (1.06 1.10 1.04), JDBC 1.07
  (1.09 1.07 1.02); build 4 had 1.04 / 1.02. Still has the 19b thread defaults; re-check with the `9efe670` build.
- The build-4 flag S3 small ADBC c1 p95 1.08 is **not seen** here: p95 1.01 (1.01 1.06 0.99), p99 0.98.

## Core (default settings)

| metric | storage | A (baseline) | B (candidate) | B / A | per round |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC total s | local | 31.8 | 34.9 | 1.10 | 1.06 1.10 1.04 |
| TPC-H SF10 JDBC total s | local | 32.2 | 34.5 | 1.07 | 1.09 1.07 1.02 |
| TPC-H SF1 ADBC total s | local | 3.4 | 3.2 | 0.95 | 0.99 0.96 0.91 |
| TPC-H SF1 JDBC total s | local | 3.4 | 3.3 | 0.96 | 1.02 0.96 0.89 |
| TPC-H SF10 ADBC total s | S3 | 314.4 | 276.0 | 0.88 | 1.00 0.88 0.99 |
| TPC-H SF10 JDBC total s | S3 | 335.9 | 277.1 | 0.82 | 1.01 0.82 1.01 |
| TPC-H SF1 ADBC total s | S3 | 26.8 | 28.0 | 1.04 | 1.05 0.76 1.08 |
| TPC-H SF1 JDBC total s | S3 | 26.9 | 30.5 | **1.14** | **1.21 1.05 1.14** |
| small ADBC c1 p50 / p95 / p99 ms | local | 16.1 / 41.6 / 54.7 | 14.8 / 41.1 / 52.1 | 0.92 / 0.99 / 0.95 | p50: 0.89 0.93 0.91 |
| small JDBC c1 p50 / p95 ms | local | 22.1 / 45.1 | 20.6 / 41.3 | 0.93 / 0.92 | p50: 0.96 0.90 0.95 |
| small ADBC c8 p50 / p95 / p99 ms | local | 98 / 263 / 383 | 77 / 257 / 307 | 0.78 / 0.98 / 0.80 | p95: 0.99 0.98 0.95 |
| small JDBC c8 p50 / p95 ms | local | 111 / 252 | 85 / 250 | 0.76 / 0.99 | p95: 0.95 0.99 1.01 |
| small ADBC c32 p50 / p95 / p99 ms | local | 412 / 1090 / 1379 | 297 / 997 / 1225 | 0.72 / 0.91 / 0.89 | p95: 0.91 0.94 0.96 |
| small JDBC c32 p50 / p95 / p99 ms | local | 415 / 1178 / 1538 | 325 / 1031 / 1233 | 0.78 / 0.88 / 0.80 | p95: 0.88 0.87 0.90 |
| small ADBC c1 p50 / p95 / p99 ms | S3 | 22.6 / 776 / 834 | 23.4 / 786 / 821 | 1.03 / 1.01 / 0.98 | p95: 1.01 1.06 0.99 |
| small JDBC c1 p50 / p95 ms | S3 | 32.5 / 786 | 32.4 / 787 | 1.00 / 1.00 | p95: 0.97 0.99 1.00 |
| small ADBC c8 p50 / p95 ms | S3 | 353 / 5648 | 343 / 5698 | 0.97 / 1.01 | p95: 0.99 1.01 1.09 |
| small JDBC c8 p50 / p95 / p99 ms | S3 | 341 / 5687 / 6341 | 360 / 5535 / 7821 | 1.06 / 0.97 / 1.23 | p99: 1.29 1.65 0.73 (noisy) |
| small ADBC c32 p95 ms | S3 | 18219 | 18503 | 1.02 | 1.03 0.94 1.02 |
| small JDBC c32 p95 ms | S3 | 21144 | 19616 | 0.93 | 0.93 0.92 0.95 |
| scan 1 / 4 / 8 streams MB/s | local | 454 / 489 / 445 | 428 / 520 / 513 | 0.94 / 1.06 / **1.15** | x8: 1.16 1.16 1.13 |
| scan 1 / 4 / 8 streams MB/s | S3 | 392 / 451 / 423 | 394 / 445 / 420 | 1.01 / 0.99 / 0.99 | x8: 0.97 0.99 0.99 |
| lineitem export ADBC MB/s | local / S3 | 490 / 412 | 476 / 412 | 0.97 / 1.00 | |
| server peak RSS MB | core jobs | 739-2630 | 751-2698 | 0.92-1.03 | TPC-H local 0.94, S3 SF10 0.92 |

S3 SF10 again has one slow baseline round per job (as in builds 1-4); the other rounds are 0.99-1.01, so S3 SF10 is
"same". Local scan x1 0.94 (0.92 0.93 1.00) is not in the rule (round 3).

## Item 18: 3-node cluster on S3, `distributedComplete` off (A) vs on (B), same build

Pending: run 40736487295 still running at 19:45 UTC; table added when it ends.

## Verdict

Pending the cluster run. Core so far: **better on local small queries and scans, with one small S3 point** (S3 TPC-H SF1 JDBC 1.14 in all 3 rounds), local SF10 1.07-1.10 under the rule, 22/22 everywhere.
