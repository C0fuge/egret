# Tracked server builds (vs baseline `7562a5bdb7b9`)

Task: `ci/BUILD-TRACK-TASK.md`. Ratios are candidate / baseline on the same runner, medians over 3 rounds (times < 1 =
candidate faster; MB/s > 1 = candidate faster). Core numbers on local Parquet unless marked S3.

**Regression `d22cdaccb4e1`: S3 small queries, p95 at 8 and 32 clients 12-21 % slower in all 3 rounds (JDBC c32 p95 1.21,
JDBC c8 p95 1.12, ADBC c8 p95 1.20) while p50 is 0.65-0.91. Local disk not affected. Details:
[track-d22cdaccb4e1](track-d22cdaccb4e1/summary.md).** Fixed in `4bb6441569be` (S3 c32 p95 back to 0.99-1.03 of baseline).

**Regression `4bb6441569be` (small): local ADBC small queries at 8 clients, p95 1.07 (rounds 1.10 1.06 1.12), p99 1.15
(1.14 1.16 1.15) while p50 is 0.75; JDBC and 32 clients not affected. Details: [track-4bb6441569be](track-4bb6441569be/summary.md).**

## Key builds

- `d22cdaccb4e1` (item 20 LZ4/ZSTD Flight streams): on a 1 Gbit/s 10 ms link, the full lineitem export over ADBC rises from 104 MB/s
  to 261 MB/s (LZ4, 2.5x) or 361 MB/s (ZSTD, 3.5x) when the client asks for compression, matching or beating upstream's
  native ZSTD (256-260 MB/s); scan with 8 streams +10-15 %.
- `4bb6441569be` (S3 threads default, item 21 step 1): removes the S3 small-query tail regression of `d22cdaccb4e1`;
  closed-loop load +5-6 % at the peak and +15-19 % at 128 clients (35 -> 40 q/s), local small-query p50 at 8/32 clients
  20-26 % faster. Still ~0.76x of upstream native's load throughput.

## Builds

| date | build | items | SF10 ADBC | SF10 JDBC | small c1 p50 | small c32 p95 | QPS sat. | scan x8 MB/s | slow-link MB/s | correct | peak RSS | verdict | details |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-10-28 | `d22cdaccb4e1` | 20 (b) LZ4 + ZSTD streams; contains 19 (threads default), 17 (b)-(d), Iceberg | 0.98 (S3 0.84) | 0.99 (S3 0.60) | ADBC 0.94 (S3 0.88), JDBC 0.95 (S3 0.91) | ADBC 0.88 (S3 0.82), JDBC 0.86 (**S3 1.21**) | not run | 1.15 (S3 1.10) | plain 1.00; CLZ4 2.51 (261); CZSTD 3.46 (361) vs 104 | 22/22 | 0.91-1.14 | better; **S3 p95 regression at c8/c32** | [summary](track-d22cdaccb4e1/summary.md), runs 40602868592 + 40621069419 |
| 2026-10-28 | `4bb6441569be` | S3 threads default >= 4; contains 21 step 1, 22 step 1 (opt-in) | 1.02 (S3 0.83) | 1.04 (S3 0.63) | ADBC 0.92 (S3 1.08), JDBC 0.96 (S3 0.97) | ADBC 0.97 (S3 0.99), JDBC 0.96 (S3 1.03) | peak 1.06 (JDBC 1.06, ADBC 1.06); c128 1.15-1.19; sat. c1 both; vs up-native 0.76 | 1.14 (S3 1.02) | not run | 22/22 | 0.94-1.10 | better; S3 regression of d22 fixed; **local ADBC c8 p95 1.07** | [summary](track-4bb6441569be/summary.md), run 40638050743 |

Skipped as contained in `d22cdaccb4e1`: `84fec772ec50` `8625e28f08cd` `b28fedf9edbf` `752e272b3ab6` `04e558056068`
`4e77c6bda59a` `b7be8d166498` `85aaf4604d9a`.

Skipped as contained in `4bb6441569be`: `881b7c62b373` `e9f0fd3` `ba4139a2eb93` `cadd1aca9c23` `3fbf5b28b186` `1f600b930eda`.
