# GizmoSQL three-way on the real-cluster build: `2ff221447b5d` speed vs balanced vs GizmoSQL v1.42.2

Task: `ci/BUILD-TRACK-TASK.md`, maintainer note 2026-11-10 22:35 (real-cluster build `server-1.0.0-2ff221447b5d`,
items 40(a), 40(b), 41, 42, 43), part (2): the gizmo wave like `fresh-gizmo-deafc861cce3` on this build. Compare run
42888240521, wave [`fresh-gizmo-2ff221447b5d`](../ci/waves/fresh-gizmo-2ff221447b5d.json), 10 jobs, all green, 3 rounds
each, alternating order; per-step load via rereport 42911042138 (`load=true`). The upstream three-way of the same build
is [FRESH-2ff221447b5d](FRESH-2ff221447b5d.md) (run 42865250390), its HDFS acceptance
[ACCEPT-2ff221447b5d](ACCEPT-2ff221447b5d.md) (SHIP).

- A = `2ff221447b5d` default (balanced)
- B = `2ff221447b5d -DresourceProfile=speed`
- C = GizmoSQL v1.42.2 (DuckDB v1.5.6), the same pinned release build and setup as in
  [FRESH-gizmo-deafc861cce3](FRESH-gizmo-deafc861cce3.md) (schema `tpch` as init-SQL views, login, TLS off, same
  container limits); harness unchanged since 76e7dfb (raw scan login fix), so the raw scans ran in the main run.

Full tables: [run summary](fresh-gizmo-2ff221447b5d-42888240521/summary.md),
[speed report](fresh-gizmo-2ff221447b5d-42888240521/speed.md),
[load.md](fresh-gizmo-2ff221447b5d-42888240521/load.md). Load q/s, slow-link numbers, TPC-H md5 and the small-query
step times come from each round's `result.txt` in the job logs. All three servers of a job run on the same runner.
Ratios: for times, < 1 = first faster; for MB/s and q/s, > 1 = first faster.

## Correctness

| workload | speed (B) | balanced (A) | GizmoSQL (C) |
|---|---|---|---|
| TPC-H SF1 + SF10, ADBC + JDBC, local | 22/22 | **SF10 19/22: DuckDB OOM q09 q10 q13 every round**, SF1 22/22 | 22/22 (same md5 as speed and the reference) |
| TPC-H SF1, ADBC + JDBC, S3 | 22/22 | **17-21/22 (OOM; ADBC q08 q09 q10 q13 q21 / q09 q13 q21 / q13 q21)** | 22/22 (same md5) |
| TPC-H SF10, ADBC + JDBC, S3 | 22/22 | **ADBC 14-17/22, JDBC 16-17/22 (OOM)** | 22/22 (same md5) |
| slow link TPC-H SF10 ADBC | 22/22 (ZSTD) | **19/22 (OOM q09 q10 q13, ZSTD)** | 22/22 (uncompressed) |
| small queries 1/8/32 clients, local + S3 | 0 errors | 0 errors | 0 errors, **gate fail `meta_schemas` only** (all 6 steps, both storages; as in deafc861cce3) |
| scans raw 1/4/8 + ADBC export, local + S3 | 0 errors | 0 errors | 0 errors, full row count |
| closed-loop load 1-128, local | 0 errors | 0 errors | 0 errors |

The balanced TPC-H failure of `FRESH-2ff221447b5d` repeats on four other runners (EPYC 9V74 / 7763 / 9V45): every
failure is a server error `Out of Memory Error: ... (12x.x MiB/128.0 MiB used)`, never a silently wrong md5 on an `ok`
query. Same query sets as in run 42865250390. GizmoSQL Flight SQL features as in `FRESH-gizmo-deafc861cce3`
(no result compression, login required, cancel not tested, `meta_schemas` schema count differs).

## Speed vs balanced vs GizmoSQL (medians over 3 rounds)

| area | metric | B speed | A balanced | C gizmo | speed / balanced (rounds) | speed / gizmo (rounds) | balanced / gizmo |
|---|---|---|---|---|---|---|---|
| TPC-H local (9V74) | SF1 ADBC / JDBC (s) | 3.3 / 3.4 | 3.4 / 3.5 | 3.0 / 3.1 | 0.99 / 0.97 | 1.12 (1.11 1.14 1.11) / 1.10 (1.11 1.10 1.10) | 1.13 / 1.14 |
| TPC-H local | SF10 ADBC / JDBC (s) | 32.7 / 32.5 | n/a (OOM) | 32.3 / 32.3 | n/a | 1.01 (1.02 1.00 1.01) / 1.01 (1.01 1.02 1.01) | n/a |
| TPC-H S3 (7763) | SF1 ADBC / JDBC (s) | 4.1 / 4.2 | n/a (OOM) | 3.7 / 3.8 | n/a | 1.10 (1.17 1.10 1.10) / 1.09 (1.09 1.09 1.09) | n/a |
| **TPC-H S3 (40(a))** | SF10 ADBC (s), 7763 | 46.0 | n/a (OOM) | 37.8 | n/a | **1.22** (1.19 1.43 1.16) | n/a |
| **TPC-H S3 (40(a))** | SF10 JDBC (s), 9V45 | 27.2 | n/a (OOM) | 27.5 | n/a | **0.99** (1.00 0.99 0.86) | n/a |
| small local (9V74) | ADBC c1 / c8 / c32 p50 (ms) | 15.8 / 83.0 / 308 | 12.0 / 82.8 / 354 | gate | **1.32** (1.44 1.23 1.18) / 1.00 / 0.87 | gate | gate |
| small local | JDBC c1 / c8 / c32 p50 (ms) | 21.8 / 91.3 / 300 | 18.6 / 96.1 / 375 | gate | **1.17** (1.13 1.17 1.23) / 0.95 / 0.80 | gate | gate |
| small local | ADBC / JDBC c32 p95 (ms) | 923 / 914 | 1016 / 1057 | gate | 0.91 / 0.86 | gate | gate |
| small S3 (8573C) | ADBC c1 / c8 / c32 p95 (ms) | 32.5 / 170 / 789 | 698 / 3939 / 13738 | gate | **0.05 / 0.04 / 0.06** | gate | gate |
| small S3 | JDBC c1 / c8 / c32 p95 (ms) | 40.5 / 181 / 800 | 699 / 3877 / 12983 | gate | **0.06 / 0.05 / 0.06** | gate | gate |
| **small, whole mix (40(b), info)** | local step time ADBC c1 / c8 / c32 (s) | 2.91 / 8.17 / 15.67 | 2.58 / 8.52 / 17.19 | 2.09 / 6.54 / 13.40 | 1.13 / 0.96 / 0.91 | **1.39 / 1.25 / 1.17** | 1.23 / 1.30 / 1.28 |
| **small, whole mix (40(b), info)** | local step time JDBC c1 / c8 / c32 (s) | 3.59 / 8.17 / 14.87 | 3.29 / 8.61 / 17.54 | 2.56 / 6.29 / 12.79 | 1.09 / 0.95 / 0.85 | **1.40 / 1.30 / 1.16** | 1.29 / 1.37 / 1.37 |
| **small, whole mix (40(b), info)** | S3 step time ADBC c1 / c8 / c32 (s) | 2.46 / 5.87 / 10.59 | 18.80 / 57.09 / 102.36 | 2.20 / 6.68 / 13.40 | 0.13 / 0.10 / 0.10 | 1.12 / **0.88 / 0.79** | 8.5 / 8.5 / 7.6 |
| **small, whole mix (40(b), info)** | S3 step time JDBC c1 / c8 / c32 (s) | 3.64 / 6.18 / 10.83 | 18.92 / 55.81 / 99.56 | 3.25 / 6.46 / 13.03 | 0.19 / 0.11 / 0.11 | 1.12 / **0.96 / 0.83** | 5.8 / 8.6 / 7.6 |
| scan local (8370C) | raw x1 / x4 / x8 (MB/s) | 416 / 546 / 558 | 412 / 421 / 389 | 461 / 559 / 562 | 1.01 / 1.30 / **1.43** | **0.90** (0.91 0.90 0.91) / 0.98 / 0.99 | 0.89 / 0.75 / 0.69 |
| scan local | ADBC export (MB/s) | 500 | 480 | 496 | 1.04 | 1.01 (1.00 1.01 1.01) | 0.97 |
| scan S3 (7763) | raw x1 / x4 / x8 (MB/s) | 402 / 614 / 616 | 380 / 453 / 429 | 383 / 619 / 634 | 1.06 / 1.35 / **1.44** | 1.05 / 0.99 / 0.97 (0.98 0.97 0.96) | 0.99 / 0.73 / 0.68 |
| scan S3 | ADBC export (MB/s) | 574 | 446 | 504 | 1.29 | 1.14 (1.14 1.13 1.41) | 0.88 |
| load local (8573C) | JDBC q/s at 1 / 8 / 32 / 64 / 128 | 46.9 / 58.8 / 60.1 / 59.5 / 58.6 | 46.8 / 51.8 / 48.6 / 45.3 / 41.9 | 53.8 / 61.0 / 60.1 / 59.2 / 58.2 | 1.00 / 1.14 / 1.24 / 1.31 / **1.40** | **0.87** (0.89 0.87 0.89) / 0.96 / 1.00 / 1.01 / 1.01 | 0.87 / 0.85 / 0.81 / 0.77 / 0.72 |
| load local | ADBC q/s at 1 / 8 / 32 / 64 / 128 | 49.0 / 59.6 / 60.1 / 59.6 / 58.9 | 48.9 / 51.6 / 46.9 / 44.0 / 41.5 | 52.9 / 60.5 / 60.1 / 59.2 / 58.5 | 1.00 / 1.16 / 1.28 / 1.35 / **1.42** | **0.93** (0.94 0.92 0.94) / 0.99 / 1.00 / 1.01 / 1.01 | 0.92 / 0.85 / 0.78 / 0.74 / 0.71 |
| slow link (10 ms, 1 Gbit) | ADBC export (MB/s) | 311 (ZSTD) | 321 (ZSTD) | 106 (no compression) | 0.97 | 2.92 (2.90 2.97 2.92) | 3.02 |
| slow link (10 ms, 1 Gbit) | TPC-H SF10 ADBC (s) | 33.7 (ZSTD) | n/a (OOM, 19/22) | 33.1 | n/a | 1.02 (1.01 1.04 1.02) | n/a |

"gate" = GizmoSQL failed the small-query gate (`meta_schemas`), so its per-class latencies are not ranked; the "whole
mix" rows are informational only (time of each fixed-size step of 160 / 640 / 1280 queries of all 8 classes, from
`result.txt`), as in `FRESH-gizmo-deafc861cce3`. The load mix has no metadata class, so gizmo is in the gate there.

## The three call-outs of the maintainer note

| point | `deafc861cce3` (run 42632367579) | `2ff221447b5d` (run 42888240521) | read |
|---|---|---|---|
| local small c1 p50 speed / balanced, JDBC / ADBC | 1.16 (1.13 1.20 1.15) / 1.18 (1.27 1.18 1.19) | **1.17 (1.13 1.17 1.23) / 1.32 (1.44 1.23 1.18)** | **not gone: > 5 % in all 3 rounds on both clients (regression by the rule)**; 18.6 -> 21.8 ms JDBC, 12.0 -> 15.8 ms ADBC. Same 9V74 runner type as run 42865250390 (1.07 / 1.11 there), so the size of the penalty varies by run; c1 p95/p99 0.88-1.15, 8/32 clients 0.80-1.00 |
| S3 TPC-H SF10 speed / gizmo, ADBC / JDBC (40(a)) | 1.51 (1.60 1.46 1.49) / 1.48 (1.18 1.57 1.80) | **1.22 (1.19 1.43 1.16) / 0.99 (1.00 0.99 0.86)** | **40(a) closes most of the gap**: JDBC level with gizmo, ADBC still 16-43 % slower (one noisy round, 54 s); speed RSS now 0.88-0.93 of gizmo's (3.4-3.5 vs 3.8 GB; was 0.78-0.80) |
| small-query mix speed / gizmo (40(b)), step time | local 1.36 / 1.27 / 1.19 (ADBC), 1.41 / 1.29 / 1.20 (JDBC); S3 8/32 clients 0.76-0.93 | local **1.39 / 1.25 / 1.17** (ADBC), **1.40 / 1.30 / 1.16** (JDBC); S3 8/32 clients **0.79-0.96**, c1 1.12 | **unchanged**: gizmo still 1.16-1.40x faster locally, speed still ahead on S3 at 8/32 clients |

## Load per step (`load.md`)

See [load.md](fresh-gizmo-2ff221447b5d-42888240521/load.md) (rereport 42911042138) for p50 / p95, CPU and memory per
step. 0 errors in every step for all three. Server RSS peak under load: speed 902 MB, balanced 4723 MB, gizmo 558 MB.
From 32 clients speed and gizmo are level (1.00-1.01 in every round); gizmo leads at 1 client (speed 0.87 JDBC / 0.93
ADBC) as in `deafc861cce3` (0.85 / 0.91). Latency: gizmo has the lowest p50 at 1-64 clients and the lowest p95 from 32
clients (128 clients JDBC p95: speed 4605 ms, gizmo 4321, balanced 4973); speed p50 is level with gizmo at 128 clients
(1977 vs 2026 ms JDBC, 1971 vs 1969 ADBC). Server memory per step: gizmo 78-496 MiB, speed 434-907, balanced 472-4688.
Saturation (p95 < 100 ms) is 1 client for all three. The `load.md` open point of `FRESH-deafc861cce3` shows again for
balanced only: 50-56 q/s in `load.md` vs 41.5-51.8 in `result.txt` (speed and gizmo agree within 1 q/s); the table above
uses the client counts.

## Memory (server RSS peak, MB, median over rounds)

| job | B speed | A balanced | C gizmo | speed / balanced | speed / gizmo | balanced / gizmo |
|---|---|---|---|---|---|---|
| TPC-H local | 1851 | **720 (OOM)** | 1593 | 2.57 | 1.16 | 0.45 |
| TPC-H S3 SF1 | 995 | **660 (OOM)** | 578 | 1.51 | 1.72 | 1.14 |
| TPC-H S3 SF10 ADBC | 3540 | **661 (OOM)** | 3805 | 5.36 | **0.93** | 0.17 |
| TPC-H S3 SF10 JDBC | 3369 | **650 (OOM)** | 3834 | 5.18 | **0.88** | 0.17 |
| small local | 908 | 1522 | 429 | 0.60 | 2.12 | 3.55 |
| small S3 | 1530 | 2284 | 1017 | 0.67 | 1.50 | 2.25 |
| scan local | 1133 | 1138 | 453 | 1.00 | 2.50 | 2.51 |
| scan S3 | 3305 | 1729 | 2536 | 1.91 | 1.30 | 0.68 |
| load local | 902 | 4723 | 558 | 0.19 | 1.62 | 8.46 |
| slow link | 1638 | **774 (OOM)** | 1475 | 2.12 | 1.11 | 0.52 |

## Verdict

- **Balanced `2ff221447b5d` fails the TPC-H gate again (DuckDB Out of Memory at the 128 MiB `memory_limit`)** on every
  TPC-H job of this run, on runners other than run 42865250390: local SF10 q09/q10/q13 every round, S3 SF1 1-5 and S3
  SF10 5-8 queries per round, slow link 19/22. Speed and GizmoSQL are 22/22 everywhere with the reference md5. The
  balanced finding of `FRESH-2ff221447b5d` is confirmed, not a runner effect.
- **40(a): speed vs gizmo on S3 TPC-H SF10 improved from 1.48-1.51 to 1.22 (ADBC) / 0.99 (JDBC)** at less memory than
  gizmo (0.88-0.93 of its RSS); SF1 on S3 still 1.09-1.10.
- **40(b): the local small c1 p50 penalty of speed vs balanced is not gone in this run: 1.17 JDBC / 1.32 ADBC, > 5 % in
  all 3 rounds (regression by the rule)**; in run 42865250390 it was 1.07 / 1.11 on the same CPU type. The whole
  small-query mix vs gizmo is unchanged (local 1.16-1.40x gizmo's time; S3 speed ahead at 8/32 clients, 0.79-0.96).
- Otherwise as in `FRESH-gizmo-deafc861cce3`: local TPC-H SF10 level with gizmo (1.01), SF1 1.10-1.12; raw scans level at
  4/8 streams (0.97-0.99, local x1 0.90), ADBC export 1.01 local / 1.14 S3; load level from 32 clients, gizmo ahead at
  1 client (0.87 / 0.93); gizmo 2.9x slower on the slow-link export without compression; GizmoSQL's only gate failure
  is still `meta_schemas`.
