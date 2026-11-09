# GizmoSQL as a fourth server: `deafc861cce3` speed vs balanced vs GizmoSQL v1.42.2

Task: `ci/BUILD-TRACK-TASK.md`, "GIZMOSQL AS A FOURTH SERVER". Compare run 42632367579, wave
[`fresh-gizmo-deafc861cce3`](../ci/waves/fresh-gizmo-deafc861cce3.json), 10 jobs, all green, 3 rounds each, alternating
order (smoke run 42629228261 before it, 1 round). Raw Flight scans of gizmo: rerun 42684180966 (`only` the two scan jobs)
after a harness fix, see "Raw Flight scans" below.

- A = `deafc861cce3` default (balanced)
- B = `deafc861cce3 -DresourceProfile=speed`
- C = **GizmoSQL v1.42.2** release build (`gizmosql_cli_linux_amd64.zip`, sha256 `c94adef7f7a1...0a46a9` pinned in
  `ci/setup-compare.sh`), **DuckDB v1.5.6** backend, in-memory database; schema `tpch` = init-SQL views over the job's
  Parquet files (local: `/data/...`, S3: `s3://...` via httpfs 1.5.6 + a secret for the local S3 endpoint); login
  user/password (GizmoSQL always requires one: JDBC `user`/`password`, ADBC `username`/`password`); TLS off like the
  others; same container limits as every server (2 CPUs on cpus 0,1, 6 GB), clients on cpus 2,3.

Full tables: [run summary](fresh-gizmo-deafc861cce3-42632367579/summary.md),
[load report](fresh-gizmo-deafc861cce3-42632367579/load.md) (`ci/load_report.py`, rereport run 42683525682 with
`load=true`). Artifacts are not readable from this session; values not in the summary (load q/s, small-query step
times, netem lines, TPC-H md5) come from the `result.txt` copies in the job logs. All three servers of a job run on the
same runner. Ratios: for times, < 1 = first faster; for MB/s and q/s, > 1 = first faster.

## Correctness

| workload | speed (B) | balanced (A) | GizmoSQL (C) |
|---|---|---|---|
| TPC-H SF1 + SF10, ADBC + JDBC, local | 22/22 | 22/22 | **22/22** (same md5 as A/B and the DuckDB reference, every round) |
| TPC-H SF1 + SF10, ADBC + JDBC, S3 | 22/22 | 22/22 | **22/22** (same md5) |
| small queries 1/8/32 clients, local + S3 | 0 errors | 0 errors | 0 errors, **gate fail: `meta_schemas` answer differs** (all 6 steps, both storages); all other classes equal |
| slow link TPC-H SF10 ADBC | 22/22 (ZSTD) | 22/22 (ZSTD) | 22/22 (uncompressed, see below) |
| scans: ADBC export, local + S3 | 0 errors | 0 errors | 0 errors, full row count |
| scans: raw Flight 1/4/8 streams | 0 errors | 0 errors | run 42632367579: every stream failed at once (harness login, not gizmo); see "Raw Flight scans" |
| closed-loop load 1-128, local | 0 errors | 0 errors | 0 errors |

GizmoSQL is the first non-fork server that passes the TPC-H gate of this harness unchanged (upstream native still has
no `tpch` schema and different decimal typing, see `FRESH-deafc861cce3`).

## Flight SQL features (task: note what gizmo lacks instead of working around it)

| feature the harness uses | GizmoSQL v1.42.2 | evidence |
|---|---|---|
| statements (JDBC, ADBC) | yes | TPC-H 22/22, small/load 0 errors |
| prepared statements with parameters (`prep_point`, JDBC + ADBC) | yes | small-query class `prep_point`: 0 errors, answers equal |
| metadata `GetObjects` / `getTables` at table depth (`meta_tables`, filter `tpch`) | yes, same answer | not in the gate failures |
| metadata at schema depth (`meta_schemas`) | answers, **but a different schema count** | the only gate failure of the small set; GizmoSQL lists the schemas of DuckDB's own catalogs next to `tpch` (the count itself is in the artifact `small-*.csv`, not readable here) - a catalog-content difference, not a missing call; reported as a gate fail as the rule says, not worked around |
| result compression (`arrow-compression` call header, ZSTD/LZ4) | **no** | the slow-link job runs gizmo uncompressed (its export: 106 MB/s vs 420 with ZSTD on speed) |
| result mode header `x-flight-result-mode` (partial/complete) | ignored (single node) | n/a for one server |
| login | **required** (Basic handshake -> bearer token) | the raw Flight scan client sent Basic on every call; fixed in 76e7dfb (handshake, then the bearer token) |
| cancel (`CancelFlightInfo`) | **not tested** | the cancel client runs only in the robustness waves, not in this wave |
| batch size | ~2048 rows per batch (DuckDB vector) | ADBC export 29291 batches vs 916 for the fork, same MB/s locally |

## Speed vs balanced vs GizmoSQL (medians over 3 rounds)

| area | metric | B speed | A balanced | C gizmo | speed / balanced (rounds) | speed / gizmo (rounds) | balanced / gizmo |
|---|---|---|---|---|---|---|---|
| TPC-H local | SF1 ADBC / JDBC (s) | 3.2 / 3.3 | 3.2 / 3.3 | 3.1 / 3.1 | 0.99 / 1.00 | 1.05 (1.10 1.03 1.05) / 1.07 (1.09 1.00 1.07) | 1.03 / 1.06 |
| TPC-H local | SF10 ADBC (s) | 32.6 | 34.1 | 32.4 | 0.96 (0.97 0.96 0.94) | 1.01 (1.04 0.99 1.00) | 1.05 |
| TPC-H local | SF10 JDBC (s) | 33.3 | 34.1 | 32.5 | 0.98 (0.98 1.00 0.96) | 1.02 (1.04 1.05 1.01) | 1.05 |
| TPC-H S3 | SF1 ADBC / JDBC (s) | 4.4 / 4.5 | 25.5 / 25.5 | 4.2 / 4.3 | **0.17 / 0.18** | 1.07 (1.04 1.06 1.10) / 1.03 (0.98 1.03 1.08) | 6.1 / 5.9 |
| TPC-H S3 | SF10 ADBC (s) | 50.4 | 298.9 | 33.5 | **0.17** (0.18 0.16 0.18) | **1.51** (1.60 1.46 1.49) | 8.9 |
| TPC-H S3 | SF10 JDBC (s) | 51.5 | 351.4 | 34.7 | **0.15** (0.13 0.15 0.16) | **1.48** (1.18 1.57 1.80) | 10.1 |
| small local | ADBC c1 / c8 / c32 p50 (ms) | 15.7 / 81.8 / 349 | 13.3 / 82.2 / 337 | gate | **1.18** (1.27 1.18 1.19) / 0.99 / 1.03 | gate | gate |
| small local | JDBC c1 / c8 / c32 p50 (ms) | 23.2 / 92.8 / 320 | 19.9 / 95.8 / 371 | gate | **1.16** (1.13 1.20 1.15) / 0.97 / 0.86 | gate | gate |
| small local | ADBC / JDBC c32 p95 (ms) | 894 / 922 | 1057 / 1053 | gate | 0.85 / 0.88 | gate | gate |
| small S3 | ADBC c1 / c8 / c32 p95 (ms) | 39.0 / 204 / 997 | 658 / 5348 / 17866 | gate | **0.06 / 0.04 / 0.06** | gate | gate |
| small S3 | JDBC c1 / c8 / c32 p95 (ms) | 46.9 / 216 / 1048 | 685 / 5255 / 17948 | gate | **0.07 / 0.04 / 0.06** | gate | gate |
| small, whole mix (info) | local step time ADBC c1 / c8 / c32 (s) | 2.83 / 8.27 / 15.71 | 2.71 / 8.63 / 17.17 | 2.08 / 6.50 / 13.18 | 1.04 / 0.96 / 0.91 | 1.36 / 1.27 / 1.19 | 1.30 / 1.33 / 1.30 |
| small, whole mix (info) | local step time JDBC c1 / c8 / c32 (s) | 3.60 / 8.18 / 15.18 | 3.46 / 8.74 / 17.37 | 2.55 / 6.33 / 12.66 | 1.04 / 0.94 / 0.87 | 1.41 / 1.29 / 1.20 | 1.36 / 1.38 / 1.37 |
| small, whole mix (info) | S3 step time ADBC c1 / c8 / c32 (s) | 3.00 / 6.94 / 12.69 | 20.27 / 74.19 / 126.84 | 2.66 / 8.14 / 16.74 | 0.15 / 0.09 / 0.10 | 1.13 / **0.85 / 0.76** | 7.6 / 9.1 / 7.6 |
| small, whole mix (info) | S3 step time JDBC c1 / c8 / c32 (s) | 4.20 / 7.52 / 12.93 | 18.62 / 72.51 / 169.50 | 3.75 / 8.08 / 16.19 | 0.23 / 0.10 / 0.08 | 1.12 / **0.93 / 0.80** | 5.0 / 9.0 / 10.5 |
| scan local | ADBC export (MB/s) | 497 | 474 | 490 | 1.05 | 1.02 (1.01 1.03 1.00) | 0.97 |
| scan S3 | ADBC export (MB/s) | 799 | 713 | 672 | 1.12 | **1.19** (1.24 1.19 1.00) | 1.06 |
| scan local | raw Flight x1 / x4 / x8 (MB/s) | 428 / 539 / 556 | 400 / 421 / 384 | RAWSCAN_LOCAL | 1.07 / 1.28 / **1.45** | RAWSCAN_LOCAL_R | RAWSCAN_LOCAL_A |
| scan S3 | raw Flight x1 / x4 / x8 (MB/s) | 629 / 959 / 956 | 597 / 676 / 671 | RAWSCAN_S3 | 1.05 / 1.42 / **1.43** | RAWSCAN_S3_R | RAWSCAN_S3_A |
| load local | JDBC q/s at 1 / 8 / 32 / 64 / 128 | 42.4 / 52.0 / 52.8 / 53.4 / 51.8 | 40.2 / 43.8 / 42.1 / 39.7 / 37.1 | 49.7 / 55.3 / 54.7 / 54.0 / 51.8 | 1.05 / 1.19 / 1.25 / 1.35 / **1.40** | **0.85** / 0.94 / 0.97 / 0.99 / 1.00 | 0.81 / 0.79 / 0.77 / 0.74 / 0.72 |
| load local | ADBC q/s at 1 / 8 / 32 / 64 / 128 | 44.5 / 53.4 / 53.0 / 52.7 / 51.8 | 41.9 / 44.1 / 40.7 / 38.7 / 35.7 | 49.1 / 55.0 / 54.3 / 53.6 / 52.2 | 1.06 / 1.21 / 1.30 / 1.36 / **1.45** | **0.91** / 0.97 / 0.98 / 0.98 / 0.99 | 0.85 / 0.80 / 0.75 / 0.72 / 0.68 |
| slow link (10 ms, 1 Gbit) | ADBC export (MB/s) | 420 (ZSTD) | 392 (ZSTD) | 106 (no compression) | 1.07 | 3.95 (3.95 3.81 4.03) | 3.69 |
| slow link (10 ms, 1 Gbit) | TPC-H SF10 ADBC (s) | 25.6 (ZSTD) | 26.8 (ZSTD) | 26.4 | 0.96 | 0.97 | 1.02 |

"gate" = GizmoSQL failed the small-query gate (`meta_schemas`), so its per-class latencies are not ranked; the "whole
mix" rows are informational only: the time of each fixed-size step (160 / 640 / 1280 queries of all 8 classes, including
`meta_schemas`), from `result.txt`. Load q/s are the client's own 60 s counts (`result.txt`), as in `FRESH-deafc861cce3`;
the load mix (`point_orders`, `point_lineitem`, `count_filter`) has no metadata class, so gizmo is in the gate there.
Load per round, speed / gizmo at 1 client: JDBC 0.86 0.84 0.87, ADBC 0.91 0.90 0.93.

## Load per step (`load.md`, medians over rounds)

p50 / p95 ms, server CPU %, server memory MiB; 0 errors in every step for all three.

| clients | JDBC speed | JDBC balanced | JDBC gizmo | ADBC speed | ADBC balanced | ADBC gizmo |
|---|---|---|---|---|---|---|
| 1 | 19.2 / 40.3, 171 %, 382 | 19.9 / 41.6, 169 %, 400 | 16.8 / 33.9, 159 %, 79 | 18.5 / 36.6, 163 %, 406 | 19.1 / 37.4, 163 %, 406 | 17.1 / 33.9, 169 %, 78 |
| 8 | 145 / 339, 200 %, 468 | 169 / 307, 199 %, 759 | 129 / 295, 190 %, 149 | 142 / 336, 191 %, 473 | 164 / 307, 191 %, 786 | 130 / 296, 196 %, 149 |
| 32 | 527 / 1218, 194 %, 531 | 638 / 1278, 195 %, 1665 | 505 / 1101, 191 %, 231 | 528 / 1218, 203 %, 547 | 634 / 1279, 200 %, 1744 | 506 / 1103, 202 %, 243 |
| 64 | 1110 / 2353, 192 %, 622 | 1308 / 2622, 192 %, 2516 | 1022 / 2296, 191 %, 321 | 1120 / 2412, 203 %, 635 | 1364 / 2687, 200 %, 2909 | 998 / 2324, 200 %, 334 |
| 128 | 2265 / 5005, 193 %, 837 | 2680 / 5882, 193 %, 3970 | 2184 / 4806, 187 %, 469 | 2291 / 5039, 198 %, 831 | 2743 / 5771, 196 %, 4584 | 2210 / 4696, 201 %, 491 |

All three are CPU-bound at the 2-CPU limit from 8 clients on. GizmoSQL has the lowest latency at every step (speed p50
1.04-1.14 of gizmo, p95 1.02-1.19) and by far the smallest memory (79-491 MiB vs 382-837 speed, 400-4584 balanced).
Saturation (p95 < 100 ms) is 1 client for all three. The `load.md` open point of `FRESH-deafc861cce3` shows again:
balanced 41-48 q/s in `load.md` vs 35.7-46.2 in `result.txt`; speed and gizmo agree in both.

## Memory (server RSS peak, MB, median over rounds)

| job | B speed | A balanced | C gizmo | speed / balanced | speed / gizmo | balanced / gizmo |
|---|---|---|---|---|---|---|
| TPC-H local | 1957 | 1609 | 1537 | 1.22 | 1.27 | 1.05 |
| TPC-H S3 SF1 | 938 | 738 | 568 | 1.27 | 1.65 | 1.30 |
| TPC-H S3 SF10 ADBC | 3047 | 1617 | 3820 | 1.88 | **0.80** | 0.42 |
| TPC-H S3 SF10 JDBC | 3006 | 1585 | 3860 | 1.90 | **0.78** | 0.41 |
| small local | 788 | 1470 | 425 | 0.54 | 1.85 | 3.46 |
| small S3 | 1408 | 2216 | 1015 | 0.64 | 1.39 | 2.18 |
| scan local | 1103 | 1110 | 230 (export only in 42632367579) | 0.99 | 4.80 | 4.83 |
| scan S3 | 3092 | 1743 | 2348 (export only in 42632367579) | 1.77 | 1.32 | 0.74 |
| load local | 904 | 4537 | 565 | 0.20 | 1.60 | 8.03 |
| slow link | 1635 | 1644 | 1478 | 0.99 | 1.11 | 1.11 |

## Raw Flight scans

RAWSCAN_SECTION

## Speed vs balanced: repeat of `FRESH-deafc861cce3` (same build, other runners)

| metric | run 42223833724 | run 42632367579 (A/B jobs) |
|---|---|---|
| local small c1 p50 speed / balanced, JDBC / ADBC | 1.10 (1.18 1.10 1.12) / 1.08 (1.17 1.08 1.02) | **1.16 (1.13 1.20 1.15) / 1.18 (1.27 1.18 1.19)** |
| scan local speed / balanced x4 / x8 | 1.30 / 1.53 | 1.28 / 1.45 |
| scan S3 speed / balanced x4 / x8 | 1.49 / 1.58 | 1.42 / 1.43 |
| S3 TPC-H speed / balanced | 0.15-0.18 | 0.15-0.18 |
| S3 small p95 speed / balanced | 0.03-0.06 | 0.04-0.07 |
| load at 128 clients speed / balanced, JDBC / ADBC | 1.42 / 1.45 | 1.40 / 1.45 |
| slow-link ZSTD export speed / balanced | 1.00 | 1.07 |

The local small-query c1 p50 regression of speed (> 5 % in all 3 rounds) is confirmed and now holds for ADBC too
(both 1.16-1.18; 19.9 -> 23.2 ms JDBC, 13.3 -> 15.7 ms ADBC); c1 p95/p99 0.84-1.05, 8/32 clients and S3 not affected.

## Verdict

- **GizmoSQL v1.42.2 passes the TPC-H gate unchanged** (22/22, SF1 + SF10, ADBC + JDBC, local + S3, the reference md5)
  and runs every workload with 0 errors. Its only gate failure is the small set's `meta_schemas` class (a different
  schema count at `GetObjects` schema depth; table-depth metadata and prepared statements match). It has no Flight
  result compression and requires a login; cancel was not tested.
- **Local disk: GizmoSQL is level with or ahead of our speed profile at a fraction of the memory**: TPC-H 1.01-1.07
  (speed / gizmo), ADBC export 1.02, load 0.85-0.91 at 1 client and 0.94-1.00 from 8 clients, lowest p50/p95 at every
  load step, small-query mix steps take speed 1.19-1.41x gizmo's time (informational), at 0.2-0.8 of speed's RSS (load 565 vs 904 MB).
  Our balanced build is behind it everywhere locally (load 0.68-0.85, TPC-H 1.03-1.06 slower).
- **S3: mixed.** GizmoSQL is clearly faster on S3 TPC-H SF10 (speed 1.48-1.51 of its time, in every round; ~34 s vs
  ~51 s) but at 1.25x speed's memory (3.8 vs 3.0 GB); SF1 level (1.03-1.07). Speed is ahead on concurrent small queries
  over S3 (whole-mix step time 0.76-0.93 at 8/32 clients) and on the S3 ADBC export (1.19). Balanced is 6-10x slower
  than gizmo on S3 TPC-H.
- Slow link: without compression gizmo's export is 3.7-4x slower than ours with ZSTD; TPC-H answers are small, so the
  slow-link TPC-H time is level (0.97).
- Speed vs balanced repeats `FRESH-deafc861cce3`; **the local small c1 p50 regression is confirmed (1.16 JDBC / 1.18
  ADBC, all rounds)**.
