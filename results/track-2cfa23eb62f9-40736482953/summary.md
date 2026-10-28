# Wave track-2cfa23eb62f9 (server comparison), run 40736482953

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

## Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| core-def-lat-local | ours-new `-` | 2cfa23eb62f9 `-` | local | Linux ubuntu24 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C | 3/3 | 0.92 | 0.91 | 0.93 | 0.88 | n/a | n/a | n/a | 0.94 | none |
| core-def-lat-s3 | ours-new `-` | 2cfa23eb62f9 `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | 1.03 | 1.02 | 1.00 | 0.93 | n/a | n/a | n/a | 1.01 | none |
| core-def-sf1-s3 | ours-new `-` | 2cfa23eb62f9 `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 1.04 | n/a | n/a | n/a | none |
| core-def-sf10adbc-s3 | ours-new `-` | 2cfa23eb62f9 `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | 0.88 | n/a | n/a | none |
| core-def-sf10jdbc-s3 | ours-new `-` | 2cfa23eb62f9 `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | 0.82 | n/a | none |
| core-def-tpch-local | ours-new `-` | 2cfa23eb62f9 `-` | local | Linux ubuntu24 4 vCPU Intel(R) Xeon(R) 6973P-C | 3/3 | n/a | n/a | n/a | n/a | 0.95 | 1.10 | 1.07 | n/a | none |

## Per job (absolute medians and ratios)

### core-def-lat-local: A = ours-new `-`, B = 2cfa23eb62f9 `-`, local

Runner: Linux ubuntu24 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C. Workloads: `small scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 22.1 | 20.6 | 0.93 | 0.96 0.90 0.95 |
| small JDBC c1 p95 | ms | 45.1 | 41.3 | 0.92 | 0.93 0.92 0.91 |
| small JDBC c1 p99 | ms | 54.4 | 48.7 | 0.90 | 0.93 1.12 0.86 |
| small JDBC c8 p50 | ms | 111.0 | 84.8 | 0.76 | 0.74 0.85 0.76 |
| small JDBC c8 p95 | ms | 252.0 | 249.9 | 0.99 | 0.95 0.99 1.01 |
| small JDBC c8 p99 | ms | 318.2 | 296.2 | 0.93 | 0.95 0.93 0.92 |
| small JDBC c32 p50 | ms | 414.5 | 324.6 | 0.78 | 0.81 0.72 0.77 |
| small JDBC c32 p95 | ms | 1178.1 | 1031.0 | 0.88 | 0.88 0.87 0.90 |
| small JDBC c32 p99 | ms | 1538.4 | 1232.5 | 0.80 | 0.76 0.83 0.84 |
| small ADBC c1 p50 | ms | 16.1 | 14.8 | 0.92 | 0.89 0.93 0.91 |
| small ADBC c1 p95 | ms | 41.6 | 41.1 | 0.99 | 1.00 1.00 0.91 |
| small ADBC c1 p99 | ms | 54.7 | 52.1 | 0.95 | 1.09 0.94 0.99 |
| small ADBC c8 p50 | ms | 97.9 | 76.7 | 0.78 | 0.76 0.77 0.82 |
| small ADBC c8 p95 | ms | 263.0 | 256.5 | 0.98 | 0.99 0.98 0.95 |
| small ADBC c8 p99 | ms | 383.0 | 306.9 | 0.80 | 0.91 0.86 0.76 |
| small ADBC c32 p50 | ms | 412.0 | 296.6 | 0.72 | 0.72 0.72 0.72 |
| small ADBC c32 p95 | ms | 1089.6 | 996.5 | 0.91 | 0.91 0.94 0.96 |
| small ADBC c32 p99 | ms | 1379.3 | 1225.2 | 0.89 | 0.89 0.88 0.93 |
| lineitem scan x1 | MB/s | 453.9 | 428.4 | 0.94 | 0.92 0.93 1.00 |
| lineitem scan x4 | MB/s | 488.6 | 519.6 | 1.06 | 1.07 1.06 1.06 |
| lineitem scan x8 | MB/s | 445.0 | 512.6 | 1.15 | 1.16 1.16 1.13 |
| lineitem export ADBC | MB/s | 489.9 | 475.8 | 0.97 | 0.97 1.11 0.86 |
| server RSS peak | MB | 1708.0 | 1593.0 | 0.93 | 0.96 0.92 0.91 |

### core-def-lat-s3: A = ours-new `-`, B = 2cfa23eb62f9 `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 32.5 | 32.4 | 1.00 | 1.02 1.05 0.96 |
| small JDBC c1 p95 | ms | 785.8 | 786.6 | 1.00 | 0.97 0.99 1.00 |
| small JDBC c1 p99 | ms | 847.6 | 854.6 | 1.01 | 1.00 0.98 1.06 |
| small JDBC c8 p50 | ms | 341.4 | 360.2 | 1.06 | 0.89 1.06 1.15 |
| small JDBC c8 p95 | ms | 5686.9 | 5534.7 | 0.97 | 1.11 0.93 0.93 |
| small JDBC c8 p99 | ms | 6340.8 | 7820.6 | 1.23 | 1.29 1.65 0.73 |
| small JDBC c32 p50 | ms | 1103.5 | 1127.5 | 1.02 | 0.99 1.02 1.04 |
| small JDBC c32 p95 | ms | 21143.7 | 19615.9 | 0.93 | 0.93 0.92 0.95 |
| small JDBC c32 p99 | ms | 30932.3 | 30049.3 | 0.97 | 1.35 0.97 0.80 |
| small ADBC c1 p50 | ms | 22.6 | 23.4 | 1.03 | 1.19 0.91 1.03 |
| small ADBC c1 p95 | ms | 775.8 | 786.0 | 1.01 | 1.01 1.06 0.99 |
| small ADBC c1 p99 | ms | 834.3 | 820.7 | 0.98 | 0.98 1.02 0.96 |
| small ADBC c8 p50 | ms | 353.2 | 342.9 | 0.97 | 0.97 0.98 0.97 |
| small ADBC c8 p95 | ms | 5647.9 | 5697.9 | 1.01 | 0.99 1.01 1.09 |
| small ADBC c8 p99 | ms | 6169.3 | 6333.4 | 1.03 | 0.97 1.03 1.06 |
| small ADBC c32 p50 | ms | 1198.8 | 1140.6 | 0.95 | 1.00 0.95 0.98 |
| small ADBC c32 p95 | ms | 18219.1 | 18502.6 | 1.02 | 1.03 0.94 1.02 |
| small ADBC c32 p99 | ms | 22723.7 | 22376.7 | 0.98 | 1.13 0.94 1.15 |
| lineitem scan x1 | MB/s | 391.5 | 393.6 | 1.01 | 0.87 1.01 1.01 |
| lineitem scan x4 | MB/s | 450.6 | 445.0 | 0.99 | 1.06 0.98 0.95 |
| lineitem scan x8 | MB/s | 422.9 | 420.0 | 0.99 | 0.97 0.99 0.99 |
| lineitem export ADBC | MB/s | 411.5 | 411.6 | 1.00 | 0.93 1.00 1.08 |
| server RSS peak | MB | 2630.0 | 2698.0 | 1.03 | 1.03 0.98 1.02 |

### core-def-sf1-s3: A = ours-new `-`, B = 2cfa23eb62f9 `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 26.8 | 28.0 | 1.04 | 1.05 0.76 1.08 |
| TPC-H SF1 JDBC (sum of medians) | s | 26.9 | 30.5 | 1.14 | 1.21 1.05 1.14 |
| server RSS peak | MB | 739.0 | 751.0 | 1.02 | 1.02 1.00 1.05 |

### core-def-sf10adbc-s3: A = ours-new `-`, B = 2cfa23eb62f9 `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | 314.4 | 276.0 | 0.88 | 1.00 0.88 0.99 |
| server RSS peak | MB | 1682.0 | 1551.0 | 0.92 | 0.90 0.88 0.92 |

### core-def-sf10jdbc-s3: A = ours-new `-`, B = 2cfa23eb62f9 `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `sf10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 JDBC (sum of medians) | s | 335.9 | 277.1 | 0.82 | 1.01 0.82 1.01 |
| server RSS peak | MB | 1723.0 | 1593.0 | 0.92 | 0.92 0.89 0.92 |

### core-def-tpch-local: A = ours-new `-`, B = 2cfa23eb62f9 `-`, local

Runner: Linux ubuntu24 4 vCPU Intel(R) Xeon(R) 6973P-C. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 3.4 | 3.2 | 0.95 | 0.99 0.96 0.91 |
| TPC-H SF10 ADBC (sum of medians) | s | 31.8 | 34.9 | 1.10 | 1.06 1.10 1.04 |
| TPC-H SF1 JDBC (sum of medians) | s | 3.4 | 3.3 | 0.96 | 1.02 0.96 0.89 |
| TPC-H SF10 JDBC (sum of medians) | s | 32.2 | 34.5 | 1.07 | 1.09 1.07 1.02 |
| server RSS peak | MB | 1739.0 | 1629.0 | 0.94 | 0.88 0.94 1.07 |
