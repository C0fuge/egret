# Tracked server builds (vs baseline `7562a5bdb7b9`)

Task: `ci/BUILD-TRACK-TASK.md`. Ratios are candidate / baseline on the same runner, medians over 3 rounds (times < 1 =
candidate faster; MB/s > 1 = candidate faster). Core numbers on local Parquet unless marked S3.

**Regression `d22cdaccb4e1`: S3 small queries, p95 at 8 and 32 clients 12-21 % slower in all 3 rounds (JDBC c32 p95 1.21,
JDBC c8 p95 1.12, ADBC c8 p95 1.20) while p50 is 0.65-0.91. Local disk not affected. Details:
[track-d22cdaccb4e1](track-d22cdaccb4e1/summary.md).** Fixed in `4bb6441569be` (S3 c32 p95 back to 0.99-1.03 of baseline).

**Regression `4bb6441569be` (small): local ADBC small queries at 8 clients, p95 1.07 (rounds 1.10 1.06 1.12), p99 1.15
(1.14 1.16 1.15) while p50 is 0.75; JDBC and 32 clients not affected. Details: [track-4bb6441569be](track-4bb6441569be/summary.md).**

**Flag `e70d80bb7995`: S3 small queries, ADBC c1 p50 1.25 (rounds 1.31 1.18 1.36; 18.1 -> 22.7 ms) in a noisy job (round 3
slow at every step); JDBC c1 p50 1.13 not in all rounds; S3 tails and local not affected. Re-check in the next build.
Details: [track-e70d80bb7995](track-e70d80bb7995/summary.md).** The local ADBC c8 tail of `4bb6441569be` is not seen
against the baseline in this run (p95 0.94).

## Key builds

- `d22cdaccb4e1` (item 20 LZ4/ZSTD Flight streams): on a 1 Gbit/s 10 ms link, the full lineitem export over ADBC rises from 104 MB/s
  to 261 MB/s (LZ4, 2.5x) or 361 MB/s (ZSTD, 3.5x) when the client asks for compression, matching or beating upstream's
  native ZSTD (256-260 MB/s); scan with 8 streams +10-15 %.
- `4bb6441569be` (S3 threads default, item 21 step 1): removes the S3 small-query tail regression of `d22cdaccb4e1`;
  closed-loop load +5-6 % at the peak and +15-19 % at 128 clients (35 -> 40 q/s), local small-query p50 at 8/32 clients
  20-26 % faster. Still ~0.76x of upstream native's load throughput.
- `e70d80bb7995` (item 22 (c)/(d), item 17 (e)): opt-in `flightZeroCopyWrites` scans +4-7 % and on par with upstream
  native (equal at 4 streams, 854 MB/s at 8, a third of native's RSS); S3 cache-on peak RSS -8 % at equal speed;
  local small-query p50 13-26 % faster, scan 8 streams +22 % vs baseline.

## Builds

| date | build | items | SF10 ADBC | SF10 JDBC | small c1 p50 | small c32 p95 | QPS sat. | scan x8 MB/s | slow-link MB/s | correct | peak RSS | verdict | details |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-10-28 | `d22cdaccb4e1` | 20 (b) LZ4 + ZSTD streams; contains 19 (threads default), 17 (b)-(d), Iceberg | 0.98 (S3 0.84) | 0.99 (S3 0.60) | ADBC 0.94 (S3 0.88), JDBC 0.95 (S3 0.91) | ADBC 0.88 (S3 0.82), JDBC 0.86 (**S3 1.21**) | not run | 1.15 (S3 1.10) | plain 1.00; CLZ4 2.51 (261); CZSTD 3.46 (361) vs 104 | 22/22 | 0.91-1.14 | better; **S3 p95 regression at c8/c32** | [summary](track-d22cdaccb4e1/summary.md), runs 40602868592 + 40621069419 |
| 2026-10-28 | `4bb6441569be` | S3 threads default >= 4; contains 21 step 1, 22 step 1 (opt-in) | 1.02 (S3 0.83) | 1.04 (S3 0.63) | ADBC 0.92 (S3 1.08), JDBC 0.96 (S3 0.97) | ADBC 0.97 (S3 0.99), JDBC 0.96 (S3 1.03) | peak 1.06 (JDBC 1.06, ADBC 1.06); c128 1.15-1.19; sat. c1 both; vs up-native 0.76 | 1.14 (S3 1.02) | not run | 22/22 | 0.94-1.10 | better; S3 regression of d22 fixed; **local ADBC c8 p95 1.07** | [summary](track-4bb6441569be/summary.md), run 40638050743 |
| 2026-10-28 | `e70d80bb7995` | 22 (c) producing streams + 22 (d) zero-copy (opt-in), 17 (e) cache memory + reuse admission (opt-in); Ranger groups | 0.99 (S3 0.67, noisy) | 0.99 (S3 0.67, noisy) | ADBC 0.87 (**S3 1.25**), JDBC 0.96 (S3 1.13) | ADBC 0.99 (S3 1.01), JDBC 0.91 (S3 1.04) | not run | 1.22 (S3 0.95); zero-copy 1.06, prodstreams=2 1.04; zero-copy vs up-native x4 1.00 | not run | 22/22 | 0.94-1.07; cache on 0.92 vs 4e77 | better; **S3 ADBC c1 p50 1.25 (noisy job)** | [summary](track-e70d80bb7995/summary.md), run 40664667021 |

Skipped as contained in `d22cdaccb4e1`: `84fec772ec50` `8625e28f08cd` `b28fedf9edbf` `752e272b3ab6` `04e558056068`
`4e77c6bda59a` `b7be8d166498` `85aaf4604d9a`.

Skipped as contained in `4bb6441569be`: `881b7c62b373` `e9f0fd3` `ba4139a2eb93` `cadd1aca9c23` `3fbf5b28b186` `1f600b930eda`.

Skipped as contained in `e70d80bb7995`: `9506620bb170` `99113c98c1c3` `7f308a6cdb4d` `36b2177d51b4`.
