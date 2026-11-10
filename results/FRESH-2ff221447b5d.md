# Fresh upstream three-way: `2ff221447b5d` speed vs balanced vs upstream native

Task: `ci/BUILD-TRACK-TASK.md`, "FRESH UPSTREAM TRACKING" and the maintainer note of 2026-11-10 22:35 (real-cluster
build `server-1.0.0-2ff221447b5d`: items 40(a), 40(b), 41, 42, 43). Its HDFS acceptance is
[ACCEPT-2ff221447b5d](ACCEPT-2ff221447b5d.md) (SHIP, run 42865242528). Compare run 42865250390, wave
[`fresh-up-2ff221447b5d`](../ci/waves/fresh-up-2ff221447b5d.json), 10 jobs, all green, 3 rounds each, alternating
order; per-step load via rereport 42889159832.

- A = `2ff221447b5d` default (balanced)
- B = `2ff221447b5d -DresourceProfile=speed`
- C = upstream native **`0ecca4f9b01e47c5be13e0add79afe4f77b3776f`** (head of `feat/starrocks-native-integration` at
  dispatch, and still the head at 19:35 UTC; `FRESH-37bf9401d77c` measured `b7d32cf3b3f0`)

Full tables: [run summary](fresh-up-2ff221447b5d-42865250390/summary.md),
[speed report](fresh-up-2ff221447b5d-42865250390/speed.md), [load.md](fresh-up-2ff221447b5d-42865250390/load.md).
Load q/s and the slow-link numbers come from each round's `result.txt` in the job logs (the client's own 60 s count).
All three servers of a job run on the same runner. Ratios: for times, < 1 = first faster; for MB/s and q/s, > 1 =
first faster. Speed vs gizmo (S3 SF10, small-query mix) is in `FRESH-gizmo-2ff221447b5d.md` (run 42888240521).

## WRONG ANSWERS: the default (balanced) profile fails TPC-H with DuckDB Out of Memory at 128 MiB

New in this build (balanced was 22/22 everywhere in `37bf9401d77c`). Every failure is a server error, not a silently
wrong result: `INTERNAL: Query execution failed: SQLException: Out of Memory Error: could not allocate block of size
256.0 KiB (127.8 MiB/128.0 MiB used)`. The DuckDB `memory_limit` in balanced mode is 128 MiB on these TPC-H jobs (the
server was started the same way as in every earlier FRESH run: 2 CPUs, 6 GB container, `-Xmx3g`, direct 2g).

| job (runner) | balanced failed queries per round | speed |
|---|---|---|
| TPC-H local SF10 ADBC + JDBC (9V45) | q09 q10 q13 in all 3 rounds (19/22) | 22/22 |
| TPC-H local SF1 ADBC + JDBC | 22/22 | 22/22 |
| TPC-H S3 SF1 ADBC (7763) | q08 q09 q10 q13 q21 / q09 q10 q13 q21 / q09 q13 q21 | 22/22 |
| TPC-H S3 SF1 JDBC | 21/22, 20/22 (OOM) | 22/22 |
| TPC-H S3 SF10 ADBC (9V74) | q08 q09 q10 q13 q16 q18 q21 q22 / q08 q09 q10 q13 q18 (two distinct lists over 3 rounds) | 22/22 |
| TPC-H S3 SF10 JDBC | 14/22, 17/22, 17/22 | 22/22 |
| slow link TPC-H SF10 ADBC, ZSTD (7763) | q09 q10 q13 in all 3 rounds (19/22) | 22/22 |

Balanced peak RSS on these jobs fell to 640-727 MB (`37bf9401d77c`: 1614-1667 MB), consistent with the small DuckDB
limit. Small queries, scans, export and load under balanced: 0 errors (balanced RSS there 1.3-4.6 GB, as before).
Because of the gate, no balanced TPC-H time is ranked in this run (SF1 local only: speed 0.96 / 0.94 of balanced).

## Correctness

| workload | speed (B) | balanced (A) | upstream native (C) |
|---|---|---|---|
| TPC-H SF1 + SF10, ADBC + JDBC, local | 22/22 | **SF10 19/22 (OOM q09 q10 q13)**, SF1 22/22 | **0/22 ADBC, 1/22 JDBC** (same md5 `813b233c6193` / `50bb2801381f`) |
| TPC-H SF1 + SF10, ADBC + JDBC, S3 | 22/22 | **14-21/22 (OOM)** | **0/22 ADBC, 1/22 JDBC** |
| small queries 1/8/32 clients, local + S3 | 0 errors | 0 errors | **errors at most steps, server died after small** |
| slow link TPC-H SF10 ADBC (ZSTD) | 22/22 | **19/22 (OOM)** | **0/22** |
| scans 1/4/8 + ADBC export, local | 0 errors | 0 errors | **x8 stream errors in 2 rounds (3, 2)** |
| scans 1/4/8 + ADBC export, S3 | 0 errors | 0 errors | **x8 stream errors in 2 rounds (1, 1)** |
| closed-loop load 1-128, local | 0 errors | 0 errors | 0 errors |

## Speed vs balanced vs upstream (medians over 3 rounds)

| area | metric | B speed | A balanced | C upstream | speed / balanced (rounds) | speed / upstream | balanced / upstream |
|---|---|---|---|---|---|---|---|
| TPC-H local | SF1 ADBC / JDBC (s) | 2.5 / 2.5 | 2.6 / 2.7 | n/a | 0.96 / 0.94 | n/a | n/a |
| TPC-H local | SF10 ADBC / JDBC (s) | 24.0 / 24.2 | n/a (OOM) | n/a | n/a | n/a | n/a |
| TPC-H S3 | SF1 ADBC / JDBC (s) | 4.1 / 4.2 | n/a (OOM) | n/a | n/a | n/a | n/a |
| TPC-H S3 | SF10 ADBC / JDBC (s) | 40.9 / 33.7 | n/a (OOM) | n/a | n/a | n/a | n/a |
| small local | ADBC c1 / c8 / c32 p50 (ms) | 15.8 / 84.0 / 309 | 14.2 / 88.0 / 362 | n/a | **1.11** (1.19 1.09 1.11) / 0.96 / 0.85 | n/a | n/a |
| small local | ADBC c1 / c8 / c32 p95 (ms) | 36.8 / 233 / 938 | 38.9 / 258 / 1032 | n/a | 0.95 / 0.90 / 0.91 | n/a | n/a |
| small local | JDBC c1 / c8 / c32 p50 (ms) | 22.9 / 90.4 / 308 | 21.3 / 99.0 / 377 | n/a | 1.07 (1.10 1.09 0.97) / 0.91 / 0.82 | n/a | n/a |
| small local | JDBC c1 / c8 / c32 p95 (ms) | 44.4 / 226 / 932 | 45.2 / 246 / 1050 | n/a | 0.98 / 0.92 / 0.89 | n/a | n/a |
| small local | JDBC c1 p99 (ms) | 56.1 | 50.8 | n/a | 1.11 (1.11 1.08 1.03) | n/a | n/a |
| small S3 | ADBC c1 / c8 / c32 p50 (ms) | 15.0 / 66.0 / 213 | 24.6 / 355 / 1132 | n/a | 0.61 / 0.19 / 0.19 | n/a | n/a |
| small S3 | ADBC c1 / c8 / c32 p95 (ms) | 43.3 / 211 / 1015 | 843 / 5925 / 17113 | n/a | **0.05 / 0.04 / 0.06** | n/a | n/a |
| small S3 | JDBC c1 / c8 / c32 p50 (ms) | 28.8 / 86.4 / 246 | 32.1 / 377 / 1166 | n/a | 0.90 / 0.23 / 0.21 | n/a | n/a |
| small S3 | JDBC c1 / c8 / c32 p95 (ms) | 51.8 / 221 / 1017 | 847 / 6114 / 17565 | n/a | **0.06 / 0.04 / 0.06** | n/a | n/a |
| scan local | x1 / x4 / x8 (MB/s) | 692 / 928 / 924 | 664 / 708 / 645 | 659 / 854 / n/a (errors) | 1.04 / 1.31 / **1.43** | 1.05 / 1.09 / n/a | 1.01 / 0.83 / n/a |
| scan local | ADBC export (MB/s) | 844 | 820 | 798 | 1.03 | 1.06 | 1.03 |
| scan S3 | x1 / x4 / x8 (MB/s) | 384 / 592 / 599 | 367 / 439 / 414 | 368 / 561 / n/a (errors) | 1.05 / **1.35** / **1.45** | 1.04 / 1.06 / n/a | 1.00 / 0.78 / n/a |
| scan S3 | ADBC export (MB/s) | 550 | 439 | 537 | 1.25 (1.39 1.23 1.24) | 1.02 | 0.82 |
| load local | JDBC q/s at 1 / 8 / 32 / 64 / 128 clients | 40.6 / 51.1 / 52.4 / 52.6 / 51.3 | 40.4 / 44.2 / 42.2 / 39.9 / 37.6 | 37.9 / 50.8 / 53.2 / 54.1 / 53.0 | 1.00 / 1.16 / 1.24 / 1.32 / **1.36** | 1.07 / 1.01 / 0.98 / 0.97 / 0.97 | 1.07 / 0.87 / 0.79 / 0.74 / 0.71 |
| load local | ADBC q/s at 1 / 8 / 32 / 64 / 128 clients | 42.9 / 52.0 / 52.5 / 52.5 / 51.2 | 41.6 / 44.4 / 40.4 / 39.0 / 35.6 | 43.5 / 54.9 / 54.5 / 54.9 / 54.2 | 1.03 / 1.17 / 1.30 / 1.35 / **1.44** | 0.99 / 0.95 / 0.96 / 0.96 / 0.94 | 0.96 / 0.81 / 0.74 / 0.71 / 0.66 |
| load local | saturation (best median q/s) | 52.6 (JDBC c64) | 44.4 (ADBC c8) | 54.9 (ADBC c8/c64) | 1.18 | 0.96 | 0.81 |
| slow link (10 ms, 1 Gbit), ZSTD | ADBC export (MB/s) | 258.7 | 254.6 | 261.8 | 1.02 (1.04 1.02 0.98) | 0.99 | 0.97 |
| slow link (10 ms, 1 Gbit), ZSTD | TPC-H SF10 ADBC (s, median sum) | 40.7 | n/a (OOM, 19/22) | n/a (0/22) | n/a | n/a | n/a |

Load per round, speed / balanced at 128 clients: JDBC 1.38 1.39 1.35, ADBC 1.44 1.43 1.41. The load job ran on an
EPYC 7763 runner (`37bf9401d77c`: Xeon 8573C). `load.md` q/s agree with the client counts within 1-4 q/s; saturation
(p95 < 100 ms) is 1 client for all three. Balanced memory under load grows to 4.0-4.6 GB at 128 clients, speed stays
under 0.9 GB like upstream.

## Local small c1 speed / balanced (40(b) claims the `894afb9b48c4` regression is gone)

| build | runner | JDBC c1 p50 (rounds) | ADBC c1 p50 (rounds) |
|---|---|---|---|
| `deafc861cce3` | 9V45 | 1.10 (in all rounds) | 1.08 (not all rounds) |
| `894afb9b48c4` | 9V45 | 1.19 (1.28 1.12 1.19) | 1.28 (1.34 1.20 1.36) |
| `37bf9401d77c` | 9V45 | 1.14 (1.15 1.14 1.13) | 1.32 (1.08 1.33 1.26) |
| **`2ff221447b5d`** | **9V74** | **1.07 (1.10 1.09 0.97)**, 21.3 -> 22.9 ms | **1.11 (1.19 1.09 1.11)**, 14.2 -> 15.8 ms |

Item 40(b) cuts the penalty to about a third (JDBC 1.14 -> 1.07, ADBC 1.32 -> 1.11), but it is **not gone: ADBC c1
p50 is still > 5 % slower in all 3 rounds (regression by the rule)**; JDBC is under the rule (round 3 0.97). JDBC c1
p99 1.11 (1.11 1.08 1.03). Caveat: this job ran on an EPYC 9V74, the last three on 9V45. c1 p95 0.95-0.98, 8/32
clients 0.82-0.96, S3 c1 0.61 / 0.90.

## Memory (server RSS peak, MB, median over rounds)

| job | B speed | A balanced | C upstream | speed / balanced | speed / upstream | speed vs `37bf9401d77c` |
|---|---|---|---|---|---|---|
| TPC-H local | 1872 | **727 (OOM)** | 365 (failed answers) | 2.57 | 5.13 | 1882 (same) |
| TPC-H S3 SF1 | 1013 | **640 (OOM)** | 611 (failed answers) | 1.58 | 1.66 | 994 (same) |
| TPC-H S3 SF10 ADBC | 3571 | **674 (OOM)** | 1042 (failed answers) | 5.30 | 3.43 | 3472 (+3 %) |
| TPC-H S3 SF10 JDBC | 3393 | **643 (OOM)** | 1051 (failed answers) | 5.28 | 3.23 | 3378 (same) |
| small local | 895 | 1547 | 257 (died) | 0.58 | 3.48 | 840 (+7 %) |
| small S3 | 1507 | 2211 | 388 (died) | 0.68 | 3.88 | 1523 (same) |
| scan local | 1170 | 1286 | 3745 | 0.91 | 0.31 | 1168 (same) |
| scan S3 | 3304 | 1705 | 5940 | 1.94 | 0.56 | 3305 (same) |
| load local | 909 | 4596 | 963 | 0.20 | 0.94 | 936 (same) |
| slow link | 1775 | **708 (OOM)** | 604 (failed answers) | 2.51 | 2.94 | 1798 (same) |

Speed memory is unchanged vs `37bf9401d77c` (within +-7 %). Balanced memory is unchanged on small/scan/load but
40-60 % lower on every TPC-H job, where it fails.

## Upstream native `0ecca4f9b01e` vs `b7d32cf3b3f0`

Same gate failures (TPC-H 0/22 ADBC, 1/22 JDBC with the same md5; small errors, server dies after small; slow-link
0/22). Local x8 scans have stream errors again in 2 of 3 rounds (`b7d32cf3b3f0` was clean) and the local scan RSS is
back at 3745 MB (was 1800); S3 x8 errors in 2 of 3 rounds as before, S3 scan RSS 5940 MB. Load at 128 clients 53-54
q/s, speed 0.94-0.97 of it (different runner type than last time). Against our speed build in the same job nothing
else moved beyond runner noise.

## Verdict

- **Wrong answers (gate fail) in the default profile: balanced `2ff221447b5d` fails TPC-H heavy queries with DuckDB
  Out of Memory at a 128 MiB `memory_limit`** - local SF10 q09/q10/q13 in every round (ADBC, JDBC, slow link), S3 SF1
  3-5 queries, S3 SF10 5-8 queries; balanced TPC-H RSS 640-727 MB (was ~1.6 GB). New in this build (items 40(b) / 42 /
  43 are the candidates; `37bf9401d77c` balanced was 22/22). Speed is 22/22 everywhere. Small queries, scans, load: 0
  errors in both profiles. **For the real cluster: run with `-DresourceProfile=speed` or wait for a fix of the
  balanced DuckDB memory sizing.**
- **Regression by the rule, smaller: local small ADBC c1 p50 speed/balanced 1.11 (1.19 1.09 1.11; 14.2 -> 15.8 ms),
  JDBC 1.07 (not all rounds).** Item 40(b) cuts the `37bf9401d77c` penalty (1.14 / 1.32) by about two thirds but does
  not remove it (different CPU type, 9V74).
- Speed otherwise as before: S3 small-query tails 0.04-0.06 of balanced, load +36-44 % at 128 clients (0.94-0.97 of
  upstream native) at 0.20 of balanced RSS, scans x4/x8 1.31-1.45 of balanced (local x4 1.09 of upstream), slow-link
  ZSTD export 1.02 of balanced and 0.99 of upstream; speed RSS unchanged.
- Upstream native moved to `0ecca4f9b01e`: same gate failures; local x8 scan errors and 3.7 GB local scan RSS are back.
