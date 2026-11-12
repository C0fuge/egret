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

**Regression `94ad61021d93` (small): S3 small queries, ADBC c1 p95 1.08 (rounds 1.07 1.09 1.05), p99 1.09 (1.19 1.09 1.06);
JDBC and 8/32 clients not affected. The `e70d80bb7995` S3 ADBC c1 p50 flag is not confirmed (1.14, rounds 1.61 1.14
0.80). Details: [track-94ad61021d93](track-94ad61021d93/summary.md).**

**Regression `2cfa23eb62f9` (small): S3 TPC-H SF1 JDBC total 1.14 (rounds 1.21 1.05 1.14; 26.9 -> 30.5 s, warm medians);
cold sums, SF1 ADBC (1.04) and S3 SF10 JDBC (0.82) not affected. Local SF10 1.07-1.10, under the rule but up from
1.02-1.04 in `94ad61021d93`. The `94ad61021d93` S3 ADBC c1 p95 flag is not seen (1.01). Details:
[track-2cfa23eb62f9](track-2cfa23eb62f9/summary.md).**

**Regression `9044653333cd` (small): S3 TPC-H SF10 ADBC total 1.10 (rounds 1.06 1.10 1.21; 260.5 -> 285.7 s, warm medians);
S3 SF10 JDBC (0.97) and S3 SF1 not affected. The `2cfa23eb62f9` S3 SF1 JDBC flag is gone (0.97); local SF10 back to
1.04. Details: [track-9044653333cd](track-9044653333cd/summary.md).**

**Regression `881bbf73e946` (small): S3 small JDBC queries at 8 clients, p50 1.10 (rounds 1.07 1.11 1.10; 245 -> 268 ms)
while p95 / p99 are 0.94 / 0.95; ADBC c8 p50 1.12 not in all rounds (as in `9044653333cd`); local not affected. The
`9044653333cd` S3 SF10 ADBC flag is gone (0.96). Details: [track-881bbf73e946](track-881bbf73e946/summary.md).** Not
confirmed in `06833e736572` (S3 JDBC c8 p50 1.04, rounds 0.99 1.04 1.34).

**Flag `843e4ad5b610` ITEM 23b (`resourceProfile=speed` vs balanced): the ITEM 23 S3 c32 errors are fixed (0 in all 3
rounds), but S3 small-query tails at 8/32 clients stay longer: p95 1.33-1.54 in every round (c32 p95 ~26 s vs ~17-18 s),
JDBC p99 1.37-1.40, total S3 c32 wall time 5-15 % longer, while p50 is 0.50. Local ADBC c8 p95 1.13. Details:
[ITEM23b](ITEM23b-843e4ad5b610.md).**

**Flag `f06b5834e76e` (`resourceProfile=speed` vs balanced, item 23b follow-up): the speed thread floor does not remove
the S3 c32 tail: S3 small c32 p95 1.50 ADBC / 1.59 JDBC in every round (1.45-2.08; 843e 1.46 / 1.54), S3 c32 wall time
11-25 % longer, and S3 ADBC c8 p99 1.58 in all 3 rounds (new; 843e 1.06). S3 c8 p95 improved (0.96-1.10, was 1.33-1.36);
0 errors everywhere. Details: [track-f06b5834e76e](track-f06b5834e76e/summary.md).** Gone in `25aa7eec0f0f` with the file cache in the speed profile (S3 c32 p95 0.06 of balanced, 0 errors; [FRESH-25aa7eec0f0f](FRESH-25aa7eec0f0f.md)).

**Regression `413485ba80fd` FRESH (`resourceProfile=speed` vs balanced, item 27): local small queries at 1 client, speed p50
1.18 JDBC (rounds 1.17 1.17 1.18; 23.5 -> 27.7 ms) and 1.19 ADBC (1.28 1.13 1.07), local ADBC c8 p99 1.14 (1.15 1.15 1.06);
`25aa7eec0f0f` had c1 p50 1.01 / 0.96. S3 c1 and local 8/32 clients not affected; 22/22 and 0 errors everywhere. Details:
[FRESH-413485ba80fd](FRESH-413485ba80fd.md).**

**Regression `deafc861cce3` FRESH (`resourceProfile=speed` vs balanced, item 34): the `413485ba80fd` local c1 penalty is
smaller but not gone: local small JDBC c1 p50 1.10 (rounds 1.18 1.10 1.12; 15.5 -> 17.1 ms); ADBC c1 p50 1.08 not in all
rounds (1.17 1.08 1.02), local ADBC c8 p99 flag gone (1.01). S3 and local 8/32 clients not affected; 22/22 and 0 errors
everywhere. Details: [FRESH-deafc861cce3](FRESH-deafc861cce3.md).**

**Regression `894afb9b48c4` FRESH (`resourceProfile=speed` vs balanced, item 39): the local c1 penalty is larger again:
local small c1 p50 1.19 JDBC (rounds 1.28 1.12 1.19; 15.4 -> 18.4 ms) and 1.28 ADBC (1.34 1.20 1.36; 10.3 -> 13.2 ms),
same CPU type as `deafc861cce3` (1.10 / 1.08). c1 p95/p99, local 8/32 clients and S3 not affected; 22/22 and 0 errors
everywhere. Details: [FRESH-894afb9b48c4](FRESH-894afb9b48c4.md).**

**Regression `37bf9401d77c` FRESH (`resourceProfile=speed` vs balanced, items 40(a), 41): the local c1 penalty stays:
local small c1 p50 1.14 JDBC (rounds 1.15 1.14 1.13; 16.6 -> 18.9 ms) and 1.32 ADBC (1.08 1.33 1.26; 10.9 -> 14.3 ms),
same CPU type as the last two runs. Item 40(a) raises speed's S3 RSS by 6-14 % (3.3-3.5 GB). c1 tails, local 8/32 clients
and S3 not affected; 22/22 and 0 errors everywhere. Details: [FRESH-37bf9401d77c](FRESH-37bf9401d77c.md).**

**WRONG ANSWERS `2ff221447b5d` FRESH (real-cluster build, items 40(a), 40(b), 41, 42, 43): the default (balanced)
profile fails TPC-H heavy queries with DuckDB Out of Memory at a 128 MiB `memory_limit` - local SF10 q09/q10/q13 in
every round (ADBC, JDBC, slow link), S3 SF1 3-5 and S3 SF10 5-8 queries per round; balanced TPC-H RSS 640-727 MB (was
~1.6 GB in `37bf9401d77c`, 22/22). Speed is 22/22 everywhere; small/scan/load 0 errors in both profiles. Also
(regression by the rule, smaller): local small ADBC c1 p50 speed/balanced 1.11 (rounds 1.19 1.09 1.11), JDBC 1.07 not
in all rounds - item 40(b) cuts the `37bf9401d77c` 1.14 / 1.32 but does not remove it (9V74 runner). Details:
[FRESH-2ff221447b5d](FRESH-2ff221447b5d.md).**

**Fixed + regression `29f1267b995f` FRESH (item 44 (1)(3) balanced DuckDB cap, floor 512 MiB; 44 (2), 45): the
`2ff221447b5d` balanced TPC-H OOM is gone - balanced 22/22 on every TPC-H job (local, S3, slow link), balanced TPC-H RSS
0.76-1.64 GB. Regression by the rule, larger again: local small c1 p50 speed/balanced 1.19 JDBC (rounds 1.12 1.09 1.19;
19.0 -> 22.7 ms) and 1.16 ADBC (1.14 1.17 1.16; 13.0 -> 15.1 ms) in all rounds, same 9V74 CPU type as `2ff221447b5d`
(1.07 / 1.11); speed's own c1 latency unchanged, balanced faster. Details: [FRESH-29f1267b995f](FRESH-29f1267b995f.md).**

**Regression `74464701e372` FRESH (item 46 DuckDB per-connection limit in one reserved budget): no wrong answers, balanced
unchanged at the 2-CPU harness size. Regression by the rule carried over: local small c1 p50 speed/balanced 1.12 JDBC
(rounds 1.08 1.12 1.15; 19.2 -> 21.6 ms) and 1.23 ADBC (1.23 1.33 1.20; 12.8 -> 15.7 ms) in all rounds, on a new CPU type
(Xeon 8573C); c1 p95 level, 8/32 clients faster. Details: [FRESH-74464701e372](FRESH-74464701e372.md).**

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
- `94ad61021d93` (item 19b threads + memory by host size, item 18 step 3): closed-loop load +6-7 % at the peak and
  +18-23 % at 128 clients (48 -> 59 q/s JDBC), sized DuckDB memory cuts peak RSS 12 % for a 2-3 % SF10 cost; 3-node
  cluster answers 22/22 with a node stopped or killed mid-query in both `distributedComplete` modes (on is not faster).
- `881bbf73e946` (item 22 shared DuckDB, opt-in `duckDbSharedDatabase=true`): scans with 8 streams +39 % and 4 streams
  +15 % in every round, closed-loop load +16 % at the peak and +37-41 % at 128 clients (35 -> 48 q/s) with 14 % less
  RSS under load; reaches upstream native's scan speed (x4 0.98, x1 1.04, ~900 MB/s at 8) at 38 % of its RSS.
- `843e4ad5b610` (item 23b, with `-DresourceProfile=speed`): passes the correctness gate on S3 at 32 clients; closed-loop
  load +19-22 % at 128 clients over balanced (within 4-6 % of upstream native) at 823 MB peak RSS vs 4432 balanced and
  4928 upstream; concurrent small-query p50 halved (S3 tails at 8/32 clients still 1.33-1.54x).
- `413485ba80fd` (item 27, `-DresourceProfile=speed`, FRESH three-way): scans with 4/8 streams 1.30-1.46x of balanced on
  local and S3 (was 1.07-1.26 in `25aa7eec0f0f`), reaching upstream native at 4 streams (S3 1.00, local 1.04) at 0.30-0.50 of
  its RSS; local single-client small-query p50 1.18-1.19x slower.

## Builds

| date | build | items | SF10 ADBC | SF10 JDBC | small c1 p50 | small c32 p95 | QPS sat. | scan x8 MB/s | slow-link MB/s | correct | peak RSS | verdict | details |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-10-28 | `d22cdaccb4e1` | 20 (b) LZ4 + ZSTD streams; contains 19 (threads default), 17 (b)-(d), Iceberg | 0.98 (S3 0.84) | 0.99 (S3 0.60) | ADBC 0.94 (S3 0.88), JDBC 0.95 (S3 0.91) | ADBC 0.88 (S3 0.82), JDBC 0.86 (**S3 1.21**) | not run | 1.15 (S3 1.10) | plain 1.00; CLZ4 2.51 (261); CZSTD 3.46 (361) vs 104 | 22/22 | 0.91-1.14 | better; **S3 p95 regression at c8/c32** | [summary](track-d22cdaccb4e1/summary.md), runs 40602868592 + 40621069419 |
| 2026-10-28 | `4bb6441569be` | S3 threads default >= 4; contains 21 step 1, 22 step 1 (opt-in) | 1.02 (S3 0.83) | 1.04 (S3 0.63) | ADBC 0.92 (S3 1.08), JDBC 0.96 (S3 0.97) | ADBC 0.97 (S3 0.99), JDBC 0.96 (S3 1.03) | peak 1.06 (JDBC 1.06, ADBC 1.06); c128 1.15-1.19; sat. c1 both; vs up-native 0.76 | 1.14 (S3 1.02) | not run | 22/22 | 0.94-1.10 | better; S3 regression of d22 fixed; **local ADBC c8 p95 1.07** | [summary](track-4bb6441569be/summary.md), run 40638050743 |
| 2026-10-28 | `e70d80bb7995` | 22 (c) producing streams + 22 (d) zero-copy (opt-in), 17 (e) cache memory + reuse admission (opt-in); Ranger groups | 0.99 (S3 0.67, noisy) | 0.99 (S3 0.67, noisy) | ADBC 0.87 (**S3 1.25**), JDBC 0.96 (S3 1.13) | ADBC 0.99 (S3 1.01), JDBC 0.91 (S3 1.04) | not run | 1.22 (S3 0.95); zero-copy 1.06, prodstreams=2 1.04; zero-copy vs up-native x4 1.00 | not run | 22/22 | 0.94-1.07; cache on 0.92 vs 4e77 | better; **S3 ADBC c1 p50 1.25 (noisy job)** | [summary](track-e70d80bb7995/summary.md), run 40664667021 |
| 2026-10-28 | `94ad61021d93` | 19b threads + memory limit by host size (+ opt-in idle threads), 18 step 3 counters + backup fail-over, 17 (a) opt-in disk tier | 1.04 (S3 0.64, noisy) | 1.02 (S3 0.66, noisy) | ADBC 0.97 (S3 1.14 noisy; **S3 p95 1.08**), JDBC 0.90 (S3 0.99) | ADBC 0.87 (S3 0.69), JDBC 0.90 (S3 0.96) | peak 1.07 JDBC / 1.06 ADBC; c128 1.18-1.23; sat. c1 both | 1.18 (S3 1.00) | not run | 22/22 (cluster 22/22 with node loss, dc on and off) | 0.87-1.06; memnone vs sized 0.88 | better; **S3 ADBC c1 p95 1.08**; dc on not faster | [summary](track-94ad61021d93/summary.md), run 40699820075 (cluster 2 of 3 rounds) |
| 2026-10-28 | `2cfa23eb62f9` | 18 / D2 (c) part 1 two-process distributed complete (TLS + token, opt-in `dataDirShared`), 13 (c) file cache bound, 3 (c) Iceberg time travel, Hive Avro | 1.10 (S3 0.88, noisy) | 1.07 (S3 0.82, noisy) | ADBC 0.92 (S3 1.03), JDBC 0.93 (S3 1.00) | ADBC 0.91 (S3 1.02), JDBC 0.88 (S3 0.93) | not run | 1.15 (S3 0.99) | not run | 22/22 (cluster 22/22 with node loss, dc on and off) | 0.92-1.03 | better locally; **S3 SF1 JDBC 1.14**; local SF10 1.07-1.10 (under rule); dc on not faster | [summary](track-2cfa23eb62f9/summary.md), runs 40736482953 + 40736487295 (cluster 2 rounds) |
| 2026-10-28 | `9044653333cd` | 21 `duckDbThreadsUnderLoad` fix, 18 D3 steps 1-2b (no wait for a crashed member), 19b thread floor 4, Hive views | 1.04 (**S3 1.10**) | 1.04 (S3 0.97) | ADBC 0.92 (S3 0.92), JDBC 0.85 (S3 0.95) | ADBC 0.98 (S3 0.97), JDBC 0.94 (S3 1.03) | peak 0.98 JDBC / 1.00 ADBC; c128 1.03 / 0.97; sat. c1 both | 1.02 (S3 0.96) | not run | 22/22 (cluster 22/22 with node loss, dc on and off) | 0.89-0.99; sized vs none 1.03 | same; **S3 SF10 ADBC 1.10**; load gain of builds 2/4 not seen; dc on all-up 1.03, recovery 90-96 s (was 104-109) | [summary](track-9044653333cd/summary.md), runs 40772221252 + 40772225000 (cluster 2 rounds) |
| 2026-10-29 | `881bbf73e946` | 22 shared DuckDB (c) streaming buffer, 22 (a) one describe DuckDB per node, 18 D3 step 3 local-disk plans, 22 step 1 opt-in `duckDbSharedDatabase`, Hive P4 (d) / C4, opt-in `plainFlightCommands` | 1.04 (S3 0.96) | 1.03 (S3 0.83, noisy) | ADBC 0.86 (S3 0.99), JDBC 0.92 (S3 0.95) | ADBC 1.01 (S3 1.01), JDBC 0.97 (S3 0.98) | peak 1.00 JDBC / 1.00 ADBC; c128 1.00; sat. c1 both; shared on: peak 1.16, c128 1.37-1.41 | 1.01 (S3 1.01); shared on 1.39; shared vs up-native x4 0.98 | not run | 22/22 (cluster 22/22 with node loss, dc on and off) | 0.90-1.02; shared on +17-19 % scans/SF10, -14 % load | better (opt-in shared DuckDB); default same; **S3 JDBC c8 p50 1.10**; dc on all-up 1.01, still not faster | [summary](track-881bbf73e946/summary.md), runs 40800578035 + 40800581040 (cluster 2 rounds) |
| 2026-10-29 | `06833e736572` | 18 D6 peer lost after first batch fails as UNAVAILABLE, Ranger Hive policies P6 steps 1-3a, C4 step 3 Hive insert-only tables | 1.06 (S3 0.65, noisy) | 1.03 (S3 1.03) | ADBC 0.94 (S3 0.99), JDBC 1.01 (S3 1.06) | ADBC 0.99 (S3 0.99), JDBC 0.97 (S3 1.02) | not run | 0.99 (S3 0.98) | not run | 22/22 (cluster 22/22 with node loss, dc on and off) | 0.88-1.01 | same; build-7 S3 JDBC c8 p50 flag not confirmed (1.04); local SF10 ADBC 1.06 (under rule); dc on all-up 1.06, after node changes 1.54-1.61 | [summary](track-06833e736572/summary.md), runs 40823526868 + 40823529991 (cluster 2 rounds) |
| 2026-10-29 | `b3bbcce19996` | 18 D9 node-load leak fix, D10 distributed complete merges plain `avg`, D11 `shutdownDrainSeconds` default 20 s; subquery/CTE/UNION tables under auth providers; LZ4 codec module for Java clients | 1.03 (S3 1.02) | 1.06 (S3 0.85, noisy) | ADBC 0.89 (S3 0.85), JDBC 0.93 (S3 1.04) | ADBC 1.05 (S3 0.69, noisy), JDBC 1.01 (S3 1.06) | not run | 1.00 (S3 1.01) | not run | 22/22 (cluster 22/22 with node loss, dc on and off) | 0.90-1.05 | same; build-8 local SF10 ADBC watch back to 1.03; local JDBC c8 p95 1.07 / p99 1.10 (watch); dc on all-up 1.04, after node changes 1.23-1.37, recovery 91-104 s | [summary](track-b3bbcce19996/summary.md), runs 40849716676 + 40849719732 (cluster 2 rounds) |
| 2026-10-29 | `1e7b43a4e0c7` FINAL | finish mode, all items since `7562a5bdb7b9`; three-way with upstream native | 1.04 (S3 0.65, noisy) | 1.02 (S3 1.01) | ADBC 1.00 (S3 1.08), JDBC 1.00 (S3 1.04) | ADBC 0.99 (S3 0.99), JDBC 0.97 (S3 1.06) | not run | 1.01 (S3 1.04); vs up-native x4 0.80 (S3 0.75) | CZSTD 2.40 (250) vs 104; vs up-native ZSTD 0.96 | 22/22 (up-native 0-1/22) | 0.88-1.02; vs up-native scans 0.30-0.47 | same on default path, better on slow link, no regression by the rule | [FINAL](FINAL-1e7b43a4e0c7.md), run 40876778493 |
| 2026-10-30 | `d752a7358a65` ITEM 23 | 23 (a)-(d) `resourceProfile=speed`; ratios here are **speed / balanced on the same build** (three-way with upstream native) | 0.97 (S3 0.81, noisy) | 0.98 (S3 0.81, noisy) | ADBC 1.06 (S3 0.97), JDBC 1.13 (S3 1.07) | ADBC 0.91 (**S3 errors**), JDBC 0.87 (**S3 errors**) | QPS at 128 clients +22 % JDBC, +16 % ADBC; vs up-native 0.96 / 0.90 | 1.43 (S3 1.36); vs up-native x4 1.06 (S3 0.70) | CZSTD 1.00 (260); vs up-native ZSTD 1.01 | 22/22; **S3 small c32 ADBC 702-753 / JDBC 66-91 of 1280 errors, all rounds** (up-native 0-1/22) | 0.67-1.25 (+20-25 % on SF10); vs up-native scans 0.19-0.24 | faster where correct; **correctness failure S3 c32, S3 c8 p95 1.42-1.44** | [ITEM23](ITEM23-d752a7358a65.md), run 41029626461 |
| 2026-10-30 | `843e4ad5b610` ITEM 23b | 23b node-wide budget for cached prepared statements; ratios here are **speed / balanced on the same build** (three-way with upstream native; small S3 + local, load only) | not run | not run | ADBC 0.98 (S3 0.91), JDBC 0.97 (S3 1.04) | ADBC 0.93 (**S3 1.46**), JDBC 0.86 (**S3 1.54**) | QPS at 128 clients +19 % JDBC, +22 % ADBC; vs up-native 0.96 / 0.94 | not run | not run | small + load 0 errors everywhere incl. **S3 c32 (ITEM 23 failure fixed)**; up-native OOM-killed on small every round | load 0.19 (823 vs 4432 MB; vs up-native 0.17), small 0.39-0.47 | correct now, faster p50 and load, far less memory; **S3 c8/c32 p95 1.33-1.54 every round** | [ITEM23b](ITEM23b-843e4ad5b610.md), run 41082368785 |
| 2026-10-30 | `f06b5834e76e` | 23b follow-up: speed `duckDbThreads` = all cores, at least 4; ratios here are **speed / balanced on the same build** (three-way with upstream native; small S3 + local, load only) | not run | not run | ADBC 0.97 (S3 0.91), JDBC 0.97 (S3 0.98) | ADBC 0.93 (**S3 1.50**), JDBC 0.88 (**S3 1.59**) | QPS at 128 clients +17 % JDBC, +19 % ADBC; vs up-native 0.94 / 0.94 | not run | not run | small + load 0 errors everywhere incl. S3 c32; up-native OOM-killed on small every round | load 0.18 (823 vs 4577 MB; vs up-native 0.19), small 0.37-0.48 | same as 843e; S3 c8 p95 better (0.96-1.10); **S3 c32 p95 1.50-1.59 unchanged, S3 ADBC c8 p99 1.58** | [summary](track-f06b5834e76e/summary.md), run 41132125972 |
| 2026-11-03 | `25aa7eec0f0f` FRESH | item 26 hadoopfs short-circuit; fresh three-way, ratios here are **speed (file cache in profile) / balanced on the same build**, upstream native `6e264c10f403` | 0.96 (S3 0.19) | 0.97 (S3 0.18) | ADBC 1.01 (S3 0.50), JDBC 0.96 (S3 0.77) | ADBC 0.94 (S3 0.06), JDBC 0.89 (S3 0.06) | QPS at 128 clients +52 % JDBC, +50 % ADBC; saturation 1.22; vs up-native 0.92 / 0.88 | 1.25 (S3 1.26); vs up-native x8 0.88 (S3 0.89) | ZSTD export 1.16 (428 MB/s); vs up-native ZSTD 1.06 | 22/22, small/load 0 errors (up-native 0-1/22 TPC-H, small errors: no `tpch` schema, decimal typing) | load 0.19, small 0.49-0.61, S3 TPC-H/scan 1.91-1.97 (~3.0-3.2 GB); vs up-native scans 0.31-0.55 | better, no regression by the rule; `f06b5834e76e` S3 c32 tail flag gone | [FRESH](FRESH-25aa7eec0f0f.md), run 41584018828 |
| 2026-11-03 | `413485ba80fd` FRESH | item 27 speed profile `duckDbPreserveInsertionOrder=false`; fresh three-way, ratios here are **speed / balanced on the same build**, upstream native `6e264c10f403` | 0.94 (S3 0.19) | 0.95 (S3 0.14) | ADBC **1.19** (S3 0.63), JDBC **1.18** (S3 0.85) | ADBC 0.89 (S3 0.06), JDBC 0.88 (S3 0.06) | QPS at 128 clients +41 % JDBC, +48 % ADBC; saturation 1.18; vs up-native 0.94 / 0.92 | 1.46 (S3 1.41); vs up-native x4 1.04 (S3 1.00), x8 n/a (up-native stream errors) | ZSTD export 1.06 (262 MB/s, slow runner link); vs up-native ZSTD 1.02 | 22/22, small/load/scan 0 errors (up-native 0-1/22 TPC-H, small errors, x8 scan errors) | load 0.20, small 0.50-0.63, S3 TPC-H/scan 1.76-1.98 (~3.0-3.1 GB); vs up-native scans 0.30-0.50 | better on scans x4/x8 (item 27); **local c1 p50 regression 1.18-1.19** | [FRESH](FRESH-413485ba80fd.md), run 41604206524 |
| 2026-11-06 | `deafc861cce3` FRESH | item 34 (HDFS copy room; [ACCEPT](ACCEPT-deafc861cce3.md) SHIP); fresh three-way, ratios here are **speed / balanced on the same build**, upstream native `9e4787906b07` (new) | 0.97 (S3 0.16) | 0.95 (S3 0.15) | ADBC 1.08 (S3 0.59), JDBC **1.10** (S3 0.91) | ADBC 0.78 (S3 0.05), JDBC 0.84 (S3 0.05) | QPS at 128 clients +42 % JDBC, +45 % ADBC; saturation 1.19; vs up-native 0.95 / 0.94 | 1.53 (S3 1.58); vs up-native x4 1.06 (S3 1.13), S3 x8 1.15, local x8 n/a (up-native stream errors) | ZSTD export 1.00 (255 MB/s); vs up-native ZSTD 0.97 | 22/22, small/load/scan 0 errors (up-native 0-1/22 TPC-H, small errors + died, local x8 scan errors) | load 0.21, small 0.51-0.62, S3 TPC-H/scan 1.73-1.96 (~3.0 GB); vs up-native scans 0.31-0.74 | same as `413485ba80fd`, S3 scans x4/x8 higher; **local JDBC c1 p50 regression 1.10** (smaller) | [FRESH](FRESH-deafc861cce3.md), run 42223833724 |
| 2026-11-10 | `894afb9b48c4` FRESH | item 39 (hadoopfs afc4, (b) cgroup sizing, (c) file-stats pruning; [ACCEPT](ACCEPT-894afb9b48c4.md) SHIP); fresh three-way, ratios here are **speed / balanced on the same build**, upstream native `cec626bbb54a` (new) | 0.98 (S3 0.17) | 0.97 (S3 0.19) | ADBC **1.28** (S3 0.53), JDBC **1.19** (S3 0.82) | ADBC 0.81 (S3 0.07), JDBC 0.87 (S3 0.06) | QPS at 128 clients +49 % JDBC, +51 % ADBC; saturation 1.20; vs up-native 0.94 / 0.97 | 1.52 (S3 1.64); vs up-native x4 1.07 (S3 1.07), x8 n/a (up-native stream errors local and S3) | ZSTD export 1.01 (254 MB/s); vs up-native ZSTD 0.99 | 22/22, small/load/scan 0 errors (up-native 0-1/22 TPC-H, small errors + died, x8 scan errors) | load 0.20, small 0.51-0.64, S3 TPC-H/scan 1.80-1.93 (~3.0-3.2 GB); vs up-native scans 0.32-0.51 | same as `deafc861cce3` elsewhere; **local c1 p50 regression 1.19 JDBC / 1.28 ADBC** (larger) | [FRESH](FRESH-894afb9b48c4.md) |
| 2026-11-10 | `37bf9401d77c` FRESH | item 40(a) speed DuckDB memory sizing, item 41 hadoopfs afc6 + `hdfsSaslDataTransfer=auto` ([ACCEPT](ACCEPT-37bf9401d77c.md) checks 1-5 pass, check 6 maintainer decision); fresh three-way, ratios here are **speed / balanced on the same build**, upstream native `b7d32cf3b3f0` (new) | 0.97 (S3 0.14) | 0.99 (S3 0.16) | ADBC **1.32** (S3 0.56), JDBC **1.14** (S3 0.78) | ADBC 0.82 (S3 0.06), JDBC 0.89 (S3 0.05) | QPS at 128 clients +38 % JDBC, +40 % ADBC (8573C runner); saturation 1.17; vs up-native 0.93 / 0.94 | 1.52 (S3 1.43); vs up-native x4 1.10 / x8 1.10 (S3 x4 1.02, x8 n/a: up-native stream errors) | ZSTD export 0.99 (323 MB/s); vs up-native ZSTD 1.01 | 22/22, small/load/scan 0 errors (up-native 0-1/22 TPC-H, small errors + died, S3 x8 scan errors) | load 0.19, small 0.54-0.67, S3 TPC-H/scan 1.88-2.09 (~3.3-3.5 GB, +6-14 % vs `894afb9b48c4`); vs up-native scans 0.56-0.65 | same as `894afb9b48c4`; speed S3 RSS up (item 40(a)); **local c1 p50 regression 1.14 JDBC / 1.32 ADBC** | [FRESH](FRESH-37bf9401d77c.md), run 42791002963 |
| 2026-11-10 | `2ff221447b5d` FRESH | real-cluster build: 40(a), 40(b) speed small-query path, 41 follow-up, 42, 43 ([ACCEPT](ACCEPT-2ff221447b5d.md) SHIP); fresh three-way, ratios here are **speed / balanced on the same build**, upstream native `0ecca4f9b01e` (new) | n/a: **balanced OOM** (speed 24.0 s local, 40.9 s S3) | n/a: **balanced OOM** (speed 24.2 s local, 33.7 s S3) | ADBC **1.11** (S3 0.61), JDBC 1.07 (S3 0.90) | ADBC 0.91 (S3 0.06), JDBC 0.89 (S3 0.06) | QPS at 128 clients +36 % JDBC, +44 % ADBC (7763 runner); saturation 1.18; vs up-native 0.97 / 0.94 | 1.43 (S3 1.45); vs up-native x4 1.09 (S3 1.06), x8 n/a: up-native stream errors | ZSTD export 1.02 (259 MB/s); vs up-native ZSTD 0.99 | **balanced 14-21/22 TPC-H (DuckDB OOM at 128 MiB)**, speed 22/22; small/load/scan 0 errors (up-native 0-1/22 TPC-H, small errors + died, x8 scan errors local + S3) | load 0.20, small 0.58-0.68, S3 TPC-H/scan 1.58-5.30 (balanced 640-727 MB on TPC-H); speed RSS same as `37bf9401d77c` | **wrong answers (balanced OOM)**; speed same as `37bf9401d77c`, local c1 penalty smaller (**ADBC 1.11**) | [FRESH](FRESH-2ff221447b5d.md), run 42865250390 |
| 2026-11-11 | `29f1267b995f` FRESH | item 44 (1)(3) balanced DuckDB cap from the 40(a) reservation (floor 512 MiB), 44 (2) `hdfsAccessRecheckMs`, 45 DC typed literals, hadoopfs afc8 ([ACCEPT](ACCEPT-29f1267b995f.md) SHIP); fresh three-way, ratios here are **speed / balanced on the same build**, upstream native `46d565e93c19` (new) | 1.01 / SF10 0.96 (S3 0.16 / SF10 0.12) | 0.98 / SF10 0.96 (S3 0.16 / SF10 0.13) | ADBC **1.16** (S3 0.48), JDBC **1.19** (S3 0.57) | ADBC 0.88 (S3 0.06), JDBC 0.89 (S3 0.07) | QPS at 128 clients +41 % JDBC, +48 % ADBC (9V74 runner); saturation 1.16; vs up-native 0.96 / 0.94 | 1.46 (S3 1.45); vs up-native x4 1.03 (S3 1.02), x8 n/a: up-native stream errors | ZSTD export 0.99 (310 MB/s); vs up-native ZSTD 0.98 | **22/22 both profiles (2ff balanced OOM fixed)**; small/load/scan 0 errors (up-native 0-1/22 TPC-H, small errors + died, x8 scan errors local + S3) | load 0.21, small 0.58-0.65, S3 TPC-H/scan 1.29-2.17 (balanced TPC-H 0.76-1.64 GB again); speed RSS same as `2ff221447b5d` | **balanced OOM fixed**; **local c1 p50 regression 1.19 JDBC / 1.16 ADBC** (larger again) | [FRESH](FRESH-29f1267b995f.md), run 42965886044 |
| 2026-11-12 | `74464701e372` FRESH | item 46 DuckDB per-connection limit within one reserved budget, qid on denial WARNs, SASL QOP in the start line ([ACCEPT](ACCEPT-74464701e372.md) SHIP); fresh three-way, ratios here are **speed / balanced on the same build**, upstream native `cfaa929746cb` (new) | 1.01 / SF10 0.96 (S3 0.18 / SF10 0.12) | 1.00 / SF10 0.97 (S3 0.19 / SF10 0.09) | ADBC **1.23** (S3 0.55), JDBC **1.12** (S3 0.84) (8573C runner) | ADBC 0.86 (S3 0.06), JDBC 0.90 (S3 0.06) | QPS at 128 clients +44 % JDBC, +47 % ADBC (9V74 runner); saturation 1.17; vs up-native 0.96 / 0.95 | 1.46 (S3 1.45); vs up-native x4 1.06 (S3 1.03), x8 n/a: up-native stream errors every round | ZSTD export 1.02 (265 MB/s, 8573C); vs up-native ZSTD 0.98 | 22/22 both profiles; small/load/scan 0 errors (up-native 0-1/22 TPC-H, small errors + died, x8 scan errors local + S3) | load 0.18, small 0.58-0.66, S3 TPC-H/scan 1.31-2.19; speed and balanced RSS same as `29f1267b995f` | same; balanced unchanged by item 46; **local c1 p50 regression 1.12 JDBC / 1.23 ADBC** (carried over) | [FRESH](FRESH-74464701e372.md), run 43148390757 |

Skipped as contained in `d22cdaccb4e1`: `84fec772ec50` `8625e28f08cd` `b28fedf9edbf` `752e272b3ab6` `04e558056068`
`4e77c6bda59a` `b7be8d166498` `85aaf4604d9a`.

Skipped as contained in `4bb6441569be`: `881b7c62b373` `e9f0fd3` `ba4139a2eb93` `cadd1aca9c23` `3fbf5b28b186` `1f600b930eda`.

Skipped as contained in `e70d80bb7995`: `9506620bb170` `99113c98c1c3` `7f308a6cdb4d` `36b2177d51b4`.

Skipped as contained in `94ad61021d93`: `a9e43ca5e296` `177dfe3e5716` `f73de96b8773` `c258adf27dc9` `1b3a7bbad4bc`.

Skipped as contained in `9044653333cd`: `a110a2279437` `0f8eb5e5f65c` `936b2d7c366c`.

Skipped as contained in `881bbf73e946`: `e75119218df7` `80aa61a15557`.

Skipped as contained in `d752a7358a65`: `1a25c7e13802` `0e457de30f25`.

Skipped as contained in `06833e736572`: `01884e287668`.

Skipped as contained in `b3bbcce19996`: `85a790826156` `7b988c720821` `2a2b8e08191f` `786782219b1a`.
