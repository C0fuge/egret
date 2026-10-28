# Wave track-load-4bb6441569be (server comparison), run 40638050743

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

## Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| core-def-lat-local | ours-new `-` | 4bb6441569be `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | 0.92 | 0.97 | 0.96 | 0.96 | n/a | n/a | n/a | 0.99 | none |
| core-def-lat-s3 | ours-new `-` | 4bb6441569be `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | 1.08 | 0.99 | 0.97 | 1.03 | n/a | n/a | n/a | 1.00 | none |
| core-def-sf1-s3 | ours-new `-` | 4bb6441569be `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 1.00 | n/a | n/a | n/a | none |
| core-def-sf10adbc-s3 | ours-new `-` | 4bb6441569be `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | 0.83 | n/a | n/a | none |
| core-def-sf10jdbc-s3 | ours-new `-` | 4bb6441569be `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | 0.63 | n/a | none |
| core-def-tpch-local | ours-new `-` | 4bb6441569be `-` | local | Linux ubuntu24 4 vCPU Intel(R) Xeon(R) 6973P-C | 3/3 | n/a | n/a | n/a | n/a | 0.92 | 1.02 | 1.04 | n/a | none |
| i21-load-local | ours-new `-` | 4bb6441569be `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| i21-load-vs-native-local | 4bb6441569be `-` | up-native `-` | local | Linux ubuntu24 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| s3fix-lat-vs-d22-s3 | d22cdaccb4e1 `-` | 4bb6441569be `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | 1.06 | 0.58 | 1.03 | 0.65 | n/a | n/a | n/a | n/a | none |

## Per job (absolute medians and ratios)

### core-def-lat-local: A = ours-new `-`, B = 4bb6441569be `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 23.2 | 22.3 | 0.96 | 0.99 0.92 0.95 |
| small JDBC c1 p95 | ms | 49.3 | 47.0 | 0.95 | 0.94 0.96 0.96 |
| small JDBC c1 p99 | ms | 56.7 | 53.4 | 0.94 | 0.91 0.89 1.07 |
| small JDBC c8 p50 | ms | 117.3 | 92.7 | 0.79 | 0.79 0.81 0.77 |
| small JDBC c8 p95 | ms | 285.3 | 278.5 | 0.98 | 0.97 0.99 0.93 |
| small JDBC c8 p99 | ms | 357.8 | 320.7 | 0.90 | 0.82 0.91 0.95 |
| small JDBC c32 p50 | ms | 466.1 | 373.9 | 0.80 | 0.78 0.84 0.77 |
| small JDBC c32 p95 | ms | 1254.7 | 1209.0 | 0.96 | 0.99 0.96 0.89 |
| small JDBC c32 p99 | ms | 1810.3 | 1527.9 | 0.84 | 0.90 0.82 0.82 |
| small ADBC c1 p50 | ms | 16.8 | 15.4 | 0.92 | 0.92 0.84 0.96 |
| small ADBC c1 p95 | ms | 44.5 | 45.4 | 1.02 | 0.92 1.05 1.07 |
| small ADBC c1 p99 | ms | 54.5 | 60.6 | 1.11 | 0.96 1.24 1.06 |
| small ADBC c8 p50 | ms | 104.3 | 78.1 | 0.75 | 0.75 0.76 0.66 |
| small ADBC c8 p95 | ms | 264.0 | 282.9 | 1.07 | 1.10 1.06 1.12 |
| small ADBC c8 p99 | ms | 310.5 | 355.6 | 1.15 | 1.14 1.16 1.15 |
| small ADBC c32 p50 | ms | 421.8 | 312.0 | 0.74 | 0.76 0.73 0.74 |
| small ADBC c32 p95 | ms | 1193.5 | 1157.9 | 0.97 | 0.98 0.98 0.93 |
| small ADBC c32 p99 | ms | 1710.7 | 1359.3 | 0.79 | 0.81 0.84 0.75 |
| lineitem scan x1 | MB/s | 455.5 | 450.6 | 0.99 | 0.99 1.00 1.00 |
| lineitem scan x4 | MB/s | 503.2 | 542.1 | 1.08 | 1.02 1.08 1.10 |
| lineitem scan x8 | MB/s | 470.7 | 536.2 | 1.14 | 1.13 1.14 1.14 |
| lineitem export ADBC | MB/s | 540.9 | 545.8 | 1.01 | 1.00 1.01 1.01 |
| server RSS peak | MB | 1743.0 | 1637.0 | 0.94 | 0.95 0.91 0.96 |

### core-def-lat-s3: A = ours-new `-`, B = 4bb6441569be `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 31.8 | 30.8 | 0.97 | 0.96 0.97 1.12 |
| small JDBC c1 p95 | ms | 754.7 | 754.0 | 1.00 | 1.00 1.07 1.10 |
| small JDBC c1 p99 | ms | 795.9 | 837.6 | 1.05 | 0.99 1.05 1.60 |
| small JDBC c8 p50 | ms | 347.6 | 341.2 | 0.98 | 0.87 0.98 1.08 |
| small JDBC c8 p95 | ms | 5257.3 | 5577.9 | 1.06 | 1.09 1.01 1.29 |
| small JDBC c8 p99 | ms | 5606.5 | 7538.0 | 1.34 | 1.34 0.91 1.55 |
| small JDBC c32 p50 | ms | 1112.4 | 1107.3 | 1.00 | 1.02 0.94 0.98 |
| small JDBC c32 p95 | ms | 16233.5 | 16767.3 | 1.03 | 0.99 1.06 0.97 |
| small JDBC c32 p99 | ms | 19902.3 | 27734.4 | 1.39 | 0.92 1.59 1.23 |
| small ADBC c1 p50 | ms | 23.5 | 25.5 | 1.08 | 0.98 1.02 1.11 |
| small ADBC c1 p95 | ms | 773.2 | 772.7 | 1.00 | 0.95 1.05 0.99 |
| small ADBC c1 p99 | ms | 842.8 | 842.7 | 1.00 | 0.96 1.04 1.00 |
| small ADBC c8 p50 | ms | 353.5 | 315.8 | 0.89 | 1.08 0.89 1.01 |
| small ADBC c8 p95 | ms | 5733.3 | 5325.3 | 0.93 | 0.92 1.06 1.04 |
| small ADBC c8 p99 | ms | 6056.3 | 5804.5 | 0.96 | 0.94 1.00 1.01 |
| small ADBC c32 p50 | ms | 1102.1 | 1060.4 | 0.96 | 0.96 1.02 0.99 |
| small ADBC c32 p95 | ms | 16589.3 | 16464.5 | 0.99 | 1.07 0.97 0.97 |
| small ADBC c32 p99 | ms | 43900.6 | 18341.9 | 0.42 | 1.03 0.36 1.54 |
| lineitem scan x1 | MB/s | 408.2 | 406.3 | 1.00 | 1.00 0.99 1.00 |
| lineitem scan x4 | MB/s | 481.2 | 486.3 | 1.01 | 1.01 0.99 1.08 |
| lineitem scan x8 | MB/s | 459.2 | 466.7 | 1.02 | 1.04 1.02 0.99 |
| lineitem export ADBC | MB/s | 454.9 | 447.1 | 0.98 | 0.98 1.02 1.00 |
| server RSS peak | MB | 2807.0 | 2727.0 | 0.97 | 0.99 0.98 0.96 |

### core-def-sf1-s3: A = ours-new `-`, B = 4bb6441569be `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 25.7 | 25.8 | 1.00 | 1.04 1.00 0.97 |
| TPC-H SF1 JDBC (sum of medians) | s | 25.9 | 26.1 | 1.01 | 1.01 0.96 1.04 |
| server RSS peak | MB | 766.0 | 785.0 | 1.02 | 1.01 1.07 0.98 |

### core-def-sf10adbc-s3: A = ours-new `-`, B = 4bb6441569be `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | 319.3 | 264.9 | 0.83 | 1.02 0.82 0.93 |
| server RSS peak | MB | 1682.0 | 1657.0 | 0.99 | 0.99 1.01 0.92 |

### core-def-sf10jdbc-s3: A = ours-new `-`, B = 4bb6441569be `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 JDBC (sum of medians) | s | 486.0 | 305.2 | 0.63 | 0.98 0.63 0.98 |
| server RSS peak | MB | 1752.0 | 1716.0 | 0.98 | 0.99 1.05 0.93 |

### core-def-tpch-local: A = ours-new `-`, B = 4bb6441569be `-`, local

Runner: Linux ubuntu24 4 vCPU Intel(R) Xeon(R) 6973P-C. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 3.0 | 2.8 | 0.92 | 0.93 0.92 0.93 |
| TPC-H SF10 ADBC (sum of medians) | s | 28.9 | 29.5 | 1.02 | 1.00 1.02 1.01 |
| TPC-H SF1 JDBC (sum of medians) | s | 3.1 | 2.9 | 0.94 | 0.93 0.94 0.93 |
| TPC-H SF10 JDBC (sum of medians) | s | 28.8 | 29.8 | 1.04 | 1.01 1.04 1.00 |
| server RSS peak | MB | 1756.0 | 1938.0 | 1.10 | 1.20 1.11 1.04 |

### i21-load-local: A = ours-new `-`, B = 4bb6441569be `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 4693.0 | 4706.0 | 1.00 | 1.04 1.00 1.03 |

### i21-load-vs-native-local: A = 4bb6441569be `-`, B = up-native `-`, local

Runner: Linux ubuntu24 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 4910.0 | 5033.0 | 1.03 | 1.04 0.94 1.03 |

### s3fix-lat-vs-d22-s3: A = d22cdaccb4e1 `-`, B = 4bb6441569be `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 31.5 | 32.6 | 1.03 | 1.01 1.18 0.90 |
| small JDBC c1 p95 | ms | 597.7 | 734.6 | 1.23 | 1.23 1.22 1.26 |
| small JDBC c1 p99 | ms | 665.3 | 807.3 | 1.21 | 1.21 1.23 1.19 |
| small JDBC c8 p50 | ms | 244.3 | 355.8 | 1.46 | 1.46 1.43 1.05 |
| small JDBC c8 p95 | ms | 6934.8 | 5889.6 | 0.85 | 0.83 0.85 0.88 |
| small JDBC c8 p99 | ms | 7473.0 | 8446.9 | 1.13 | 0.86 1.13 1.22 |
| small JDBC c32 p50 | ms | 870.6 | 1119.0 | 1.29 | 1.38 1.29 1.43 |
| small JDBC c32 p95 | ms | 26634.5 | 17219.4 | 0.65 | 0.84 0.61 0.85 |
| small JDBC c32 p99 | ms | 30882.0 | 20924.5 | 0.68 | 0.83 0.59 0.59 |
| small ADBC c1 p50 | ms | 24.4 | 25.8 | 1.06 | 1.01 1.27 1.10 |
| small ADBC c1 p95 | ms | 626.7 | 747.0 | 1.19 | 1.24 1.17 1.17 |
| small ADBC c1 p99 | ms | 661.8 | 1190.2 | 1.80 | 2.10 1.20 1.13 |
| small ADBC c8 p50 | ms | 245.4 | 369.2 | 1.50 | 1.40 1.50 1.43 |
| small ADBC c8 p95 | ms | 6737.6 | 5853.9 | 0.87 | 0.90 0.82 0.78 |
| small ADBC c8 p99 | ms | 7083.3 | 6272.3 | 0.89 | 0.91 0.85 0.79 |
| small ADBC c32 p50 | ms | 1003.7 | 1117.9 | 1.11 | 1.63 1.01 1.68 |
| small ADBC c32 p95 | ms | 28839.2 | 16598.2 | 0.58 | 0.80 0.56 0.85 |
| small ADBC c32 p99 | ms | 30919.2 | 18189.5 | 0.59 | 0.82 0.59 0.73 |
| server RSS peak | MB | 2197.0 | 2215.0 | 1.01 | 1.02 1.01 1.00 |
