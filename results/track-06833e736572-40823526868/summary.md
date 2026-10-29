# Wave track-06833e736572 (server comparison), run 40823526868

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

## Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| core-def-lat-local | ours-new `-` | 06833e736572 `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | 0.94 | 0.99 | 1.01 | 0.97 | n/a | n/a | n/a | 0.95 | none |
| core-def-lat-s3 | ours-new `-` | 06833e736572 `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | 0.99 | 0.99 | 1.06 | 1.02 | n/a | n/a | n/a | 0.99 | none |
| core-def-sf1-s3 | ours-new `-` | 06833e736572 `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 0.99 | n/a | n/a | n/a | none |
| core-def-sf10adbc-s3 | ours-new `-` | 06833e736572 `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | 0.65 | n/a | n/a | none |
| core-def-sf10jdbc-s3 | ours-new `-` | 06833e736572 `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | 1.03 | n/a | none |
| core-def-tpch-local | ours-new `-` | 06833e736572 `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 0.99 | 1.06 | 1.03 | n/a | none |

## Per job (absolute medians and ratios)

### core-def-lat-local: A = ours-new `-`, B = 06833e736572 `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 25.8 | 26.2 | 1.01 | 1.10 0.98 0.99 |
| small JDBC c1 p95 | ms | 50.7 | 52.8 | 1.04 | 1.07 1.00 1.00 |
| small JDBC c1 p99 | ms | 57.1 | 65.5 | 1.15 | 1.17 1.16 0.92 |
| small JDBC c8 p50 | ms | 129.7 | 124.9 | 0.96 | 0.96 1.01 0.98 |
| small JDBC c8 p95 | ms | 289.4 | 293.4 | 1.01 | 1.02 1.01 1.01 |
| small JDBC c8 p99 | ms | 409.9 | 363.4 | 0.89 | 0.72 0.95 0.89 |
| small JDBC c32 p50 | ms | 487.9 | 477.2 | 0.98 | 0.97 0.95 1.01 |
| small JDBC c32 p95 | ms | 1365.8 | 1319.9 | 0.97 | 0.96 0.97 0.97 |
| small JDBC c32 p99 | ms | 2007.3 | 1953.9 | 0.97 | 0.95 0.97 0.95 |
| small ADBC c1 p50 | ms | 18.2 | 17.0 | 0.94 | 0.92 0.92 0.99 |
| small ADBC c1 p95 | ms | 48.0 | 47.6 | 0.99 | 1.01 0.98 0.95 |
| small ADBC c1 p99 | ms | 55.0 | 61.2 | 1.11 | 1.11 0.99 1.20 |
| small ADBC c8 p50 | ms | 115.9 | 112.6 | 0.97 | 0.97 1.01 0.96 |
| small ADBC c8 p95 | ms | 280.3 | 279.7 | 1.00 | 0.99 1.03 0.98 |
| small ADBC c8 p99 | ms | 347.9 | 355.4 | 1.02 | 0.94 1.18 1.02 |
| small ADBC c32 p50 | ms | 440.8 | 441.3 | 1.00 | 1.00 0.99 1.03 |
| small ADBC c32 p95 | ms | 1319.9 | 1312.6 | 0.99 | 0.96 1.04 0.98 |
| small ADBC c32 p99 | ms | 1930.5 | 1967.7 | 1.02 | 1.04 1.05 0.95 |
| lineitem scan x1 | MB/s | 435.8 | 414.3 | 0.95 | 0.99 0.91 0.95 |
| lineitem scan x4 | MB/s | 459.6 | 456.7 | 0.99 | 1.00 0.98 1.00 |
| lineitem scan x8 | MB/s | 420.5 | 414.8 | 0.99 | 0.99 0.98 0.99 |
| lineitem export ADBC | MB/s | 532.4 | 520.8 | 0.98 | 1.00 0.99 0.96 |
| server RSS peak | MB | 1727.0 | 1739.0 | 1.01 | 1.01 1.04 0.98 |

### core-def-lat-s3: A = ours-new `-`, B = 06833e736572 `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `small scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 25.2 | 26.8 | 1.06 | 1.05 1.04 1.12 |
| small JDBC c1 p95 | ms | 680.3 | 688.7 | 1.01 | 0.97 1.02 0.98 |
| small JDBC c1 p99 | ms | 744.1 | 724.3 | 0.97 | 0.95 0.99 0.99 |
| small JDBC c8 p50 | ms | 257.0 | 268.4 | 1.04 | 0.99 1.04 1.34 |
| small JDBC c8 p95 | ms | 3767.9 | 3789.5 | 1.01 | 0.98 0.97 1.53 |
| small JDBC c8 p99 | ms | 4133.8 | 4132.7 | 1.00 | 0.99 0.99 1.59 |
| small JDBC c32 p50 | ms | 994.2 | 867.9 | 0.87 | 0.85 0.87 1.52 |
| small JDBC c32 p95 | ms | 13772.1 | 14090.0 | 1.02 | 1.06 1.02 1.49 |
| small JDBC c32 p99 | ms | 16998.3 | 31133.8 | 1.83 | 2.16 1.09 2.22 |
| small ADBC c1 p50 | ms | 20.5 | 20.3 | 0.99 | 0.94 0.91 1.14 |
| small ADBC c1 p95 | ms | 696.1 | 692.8 | 1.00 | 0.96 1.03 0.99 |
| small ADBC c1 p99 | ms | 746.9 | 752.2 | 1.01 | 1.58 1.02 0.97 |
| small ADBC c8 p50 | ms | 253.8 | 256.9 | 1.01 | 0.98 1.09 1.49 |
| small ADBC c8 p95 | ms | 3778.9 | 3772.0 | 1.00 | 0.99 1.00 1.62 |
| small ADBC c8 p99 | ms | 4136.1 | 4239.8 | 1.03 | 1.02 1.03 1.57 |
| small ADBC c32 p50 | ms | 897.4 | 980.6 | 1.09 | 1.01 1.09 1.65 |
| small ADBC c32 p95 | ms | 13071.4 | 12961.6 | 0.99 | 0.98 0.99 1.71 |
| small ADBC c32 p99 | ms | 14290.7 | 14630.4 | 1.02 | 1.03 0.95 2.23 |
| lineitem scan x1 | MB/s | 568.8 | 563.1 | 0.99 | 1.01 0.92 0.99 |
| lineitem scan x4 | MB/s | 641.3 | 642.1 | 1.00 | 1.00 0.85 1.01 |
| lineitem scan x8 | MB/s | 606.4 | 592.8 | 0.98 | 0.99 0.95 0.98 |
| lineitem export ADBC | MB/s | 532.9 | 570.2 | 1.07 | 1.07 0.94 1.03 |
| server RSS peak | MB | 2858.0 | 2771.0 | 0.97 | 1.02 0.93 0.97 |

### core-def-sf1-s3: A = ours-new `-`, B = 06833e736572 `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 27.8 | 27.6 | 0.99 | 1.01 0.99 1.00 |
| TPC-H SF1 JDBC (sum of medians) | s | 28.0 | 28.0 | 1.00 | 1.04 0.97 0.97 |
| server RSS peak | MB | 728.0 | 734.0 | 1.01 | 1.01 0.97 0.94 |

### core-def-sf10adbc-s3: A = ours-new `-`, B = 06833e736572 `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | 477.5 | 309.5 | 0.65 | 1.05 0.63 1.00 |
| server RSS peak | MB | 1657.0 | 1584.0 | 0.96 | 0.89 0.91 0.96 |

### core-def-sf10jdbc-s3: A = ours-new `-`, B = 06833e736572 `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `sf10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 JDBC (sum of medians) | s | 286.5 | 294.6 | 1.03 | 1.05 1.03 1.06 |
| server RSS peak | MB | 1649.0 | 1593.0 | 0.97 | 0.90 0.99 0.98 |

### core-def-tpch-local: A = ours-new `-`, B = 06833e736572 `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 4.1 | 4.1 | 0.99 | 0.99 1.01 0.99 |
| TPC-H SF10 ADBC (sum of medians) | s | 39.6 | 42.1 | 1.06 | 1.03 1.06 1.07 |
| TPC-H SF1 JDBC (sum of medians) | s | 4.2 | 4.2 | 0.99 | 1.01 0.99 0.99 |
| TPC-H SF10 JDBC (sum of medians) | s | 40.3 | 41.5 | 1.03 | 1.02 1.03 1.05 |
| server RSS peak | MB | 1733.0 | 1528.0 | 0.88 | 0.89 0.88 0.92 |
