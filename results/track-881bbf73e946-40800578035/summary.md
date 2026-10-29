# Wave track-881bbf73e946 (server comparison), run 40800578035

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

## Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| core-def-lat-local | ours-new `-` | 881bbf73e946 `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | 0.86 | 1.01 | 0.92 | 0.97 | n/a | n/a | n/a | 0.97 | none |
| core-def-lat-s3 | ours-new `-` | 881bbf73e946 `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | 0.99 | 1.01 | 0.95 | 0.98 | n/a | n/a | n/a | 0.96 | none |
| core-def-sf1-s3 | ours-new `-` | 881bbf73e946 `-` | s3 | Linux ubuntu24 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C | 3/3 | n/a | n/a | n/a | n/a | 0.99 | n/a | n/a | n/a | none |
| core-def-sf10adbc-s3 | ours-new `-` | 881bbf73e946 `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | 0.96 | n/a | n/a | none |
| core-def-sf10jdbc-s3 | ours-new `-` | 881bbf73e946 `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | 0.83 | n/a | none |
| core-def-tpch-local | ours-new `-` | 881bbf73e946 `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 0.97 | 1.04 | 1.03 | n/a | none |
| i21-load-local | ours-new `-` | 881bbf73e946 `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| i22-shared-off-vs-on-load-local | 881bbf73e946 `-` | 881bbf73e946 `-DduckDbSharedDatabase=true` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| i22-shared-off-vs-on-local | 881bbf73e946 `-` | 881bbf73e946 `-DduckDbSharedDatabase=true` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.00 | none |
| i22-shared-off-vs-on-sf10-local | 881bbf73e946 `-` | 881bbf73e946 `-DduckDbSharedDatabase=true` | local | Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | 0.98 | 0.99 | n/a | none |
| i22-shared-vs-native-local | 881bbf73e946 `-DduckDbSharedDatabase=true` | up-native `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 0.96 | B: scan8 (rows=382657304 errors=2) |

## Per job (absolute medians and ratios)

### core-def-lat-local: A = ours-new `-`, B = 881bbf73e946 `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `small scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 21.0 | 19.4 | 0.92 | 0.95 0.78 0.87 |
| small JDBC c1 p95 | ms | 41.3 | 40.1 | 0.97 | 0.98 0.88 0.98 |
| small JDBC c1 p99 | ms | 49.6 | 44.6 | 0.90 | 1.01 0.88 0.98 |
| small JDBC c8 p50 | ms | 101.9 | 100.5 | 0.99 | 1.05 0.94 0.93 |
| small JDBC c8 p95 | ms | 243.7 | 251.6 | 1.03 | 0.95 1.03 1.08 |
| small JDBC c8 p99 | ms | 316.8 | 300.5 | 0.95 | 0.95 0.95 0.94 |
| small JDBC c32 p50 | ms | 385.3 | 382.5 | 0.99 | 0.96 0.90 0.99 |
| small JDBC c32 p95 | ms | 1069.6 | 1039.3 | 0.97 | 0.98 0.93 0.96 |
| small JDBC c32 p99 | ms | 1403.2 | 1371.2 | 0.98 | 0.96 0.97 0.99 |
| small ADBC c1 p50 | ms | 14.6 | 12.5 | 0.86 | 0.87 0.82 0.85 |
| small ADBC c1 p95 | ms | 37.4 | 34.6 | 0.93 | 0.95 0.98 0.90 |
| small ADBC c1 p99 | ms | 44.3 | 40.7 | 0.92 | 0.92 0.99 0.82 |
| small ADBC c8 p50 | ms | 88.4 | 82.6 | 0.93 | 1.01 0.92 0.89 |
| small ADBC c8 p95 | ms | 249.2 | 249.3 | 1.00 | 1.04 1.00 0.93 |
| small ADBC c8 p99 | ms | 364.9 | 366.3 | 1.00 | 0.99 1.12 1.03 |
| small ADBC c32 p50 | ms | 375.9 | 361.3 | 0.96 | 1.01 0.88 0.95 |
| small ADBC c32 p95 | ms | 1051.0 | 1061.7 | 1.01 | 1.12 0.99 0.99 |
| small ADBC c32 p99 | ms | 1308.6 | 1345.4 | 1.03 | 1.10 1.00 0.99 |
| lineitem scan x1 | MB/s | 543.8 | 526.2 | 0.97 | 0.97 1.17 0.95 |
| lineitem scan x4 | MB/s | 547.2 | 556.5 | 1.02 | 0.96 1.06 1.03 |
| lineitem scan x8 | MB/s | 486.2 | 490.4 | 1.01 | 1.00 1.01 1.01 |
| lineitem export ADBC | MB/s | 622.8 | 594.8 | 0.96 | 0.99 0.94 0.96 |
| server RSS peak | MB | 1699.0 | 1714.0 | 1.01 | 1.01 1.02 0.99 |

### core-def-lat-s3: A = ours-new `-`, B = 881bbf73e946 `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `small scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 29.6 | 28.2 | 0.95 | 1.13 0.95 0.87 |
| small JDBC c1 p95 | ms | 670.8 | 696.3 | 1.04 | 1.29 1.04 1.01 |
| small JDBC c1 p99 | ms | 737.5 | 789.8 | 1.07 | 1.95 1.02 1.02 |
| small JDBC c8 p50 | ms | 244.5 | 268.2 | 1.10 | 1.07 1.11 1.10 |
| small JDBC c8 p95 | ms | 4003.6 | 3773.5 | 0.94 | 0.98 0.93 0.95 |
| small JDBC c8 p99 | ms | 4348.2 | 4112.5 | 0.95 | 0.99 0.94 0.96 |
| small JDBC c32 p50 | ms | 929.5 | 955.2 | 1.03 | 0.97 1.03 1.08 |
| small JDBC c32 p95 | ms | 14024.2 | 13741.1 | 0.98 | 1.05 1.01 0.93 |
| small JDBC c32 p99 | ms | 21311.4 | 24527.9 | 1.15 | 1.63 1.10 0.93 |
| small ADBC c1 p50 | ms | 24.3 | 24.1 | 0.99 | 0.83 0.99 1.03 |
| small ADBC c1 p95 | ms | 725.7 | 693.8 | 0.96 | 1.03 0.96 1.00 |
| small ADBC c1 p99 | ms | 853.0 | 1174.3 | 1.38 | 1.28 0.92 1.41 |
| small ADBC c8 p50 | ms | 239.7 | 268.7 | 1.12 | 1.03 0.99 1.12 |
| small ADBC c8 p95 | ms | 3919.1 | 3751.5 | 0.96 | 1.00 0.98 0.94 |
| small ADBC c8 p99 | ms | 4414.9 | 4321.4 | 0.98 | 1.00 0.89 0.98 |
| small ADBC c32 p50 | ms | 954.4 | 954.5 | 1.00 | 1.05 0.97 0.98 |
| small ADBC c32 p95 | ms | 12865.5 | 12975.6 | 1.01 | 1.01 1.00 1.04 |
| small ADBC c32 p99 | ms | 14646.1 | 14405.9 | 0.98 | 1.00 0.98 1.01 |
| lineitem scan x1 | MB/s | 360.5 | 344.8 | 0.96 | 0.66 0.97 0.99 |
| lineitem scan x4 | MB/s | 493.5 | 462.2 | 0.94 | 0.88 0.94 0.88 |
| lineitem scan x8 | MB/s | 456.7 | 461.2 | 1.01 | 0.97 1.02 0.95 |
| lineitem export ADBC | MB/s | 353.2 | 329.8 | 0.93 | 0.83 1.61 0.88 |
| server RSS peak | MB | 2732.0 | 2798.0 | 1.02 | 1.01 1.02 1.05 |

### core-def-sf1-s3: A = ours-new `-`, B = 881bbf73e946 `-`, s3

Runner: Linux ubuntu24 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 34.7 | 34.5 | 0.99 | 1.00 1.01 0.99 |
| TPC-H SF1 JDBC (sum of medians) | s | 35.4 | 35.8 | 1.01 | 0.98 1.03 1.03 |
| server RSS peak | MB | 729.0 | 735.0 | 1.01 | 0.97 0.98 1.12 |

### core-def-sf10adbc-s3: A = ours-new `-`, B = 881bbf73e946 `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | 275.9 | 263.6 | 0.96 | 1.03 0.83 0.94 |
| server RSS peak | MB | 1681.0 | 1587.0 | 0.94 | 0.95 0.87 0.91 |

### core-def-sf10jdbc-s3: A = ours-new `-`, B = 881bbf73e946 `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `sf10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 JDBC (sum of medians) | s | 317.8 | 265.1 | 0.83 | 1.03 0.83 0.92 |
| server RSS peak | MB | 1649.0 | 1618.0 | 0.98 | 1.00 0.98 0.91 |

### core-def-tpch-local: A = ours-new `-`, B = 881bbf73e946 `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 4.1 | 4.0 | 0.97 | 0.96 0.99 1.00 |
| TPC-H SF10 ADBC (sum of medians) | s | 39.5 | 41.0 | 1.04 | 1.04 1.01 1.05 |
| TPC-H SF1 JDBC (sum of medians) | s | 4.1 | 4.1 | 1.00 | 0.97 0.99 1.02 |
| TPC-H SF10 JDBC (sum of medians) | s | 39.6 | 40.7 | 1.03 | 1.04 0.99 1.03 |
| server RSS peak | MB | 1741.0 | 1567.0 | 0.90 | 0.88 1.00 0.90 |

### i21-load-local: A = ours-new `-`, B = 881bbf73e946 `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 4504.0 | 4458.0 | 0.99 | 0.99 0.99 1.00 |

### i22-shared-off-vs-on-load-local: A = 881bbf73e946 `-`, B = 881bbf73e946 `-DduckDbSharedDatabase=true`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 4468.0 | 3847.0 | 0.86 | 0.86 0.84 0.89 |

### i22-shared-off-vs-on-local: A = 881bbf73e946 `-`, B = 881bbf73e946 `-DduckDbSharedDatabase=true`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 447.2 | 447.4 | 1.00 | 0.98 1.00 1.06 |
| lineitem scan x4 | MB/s | 464.8 | 536.7 | 1.15 | 1.11 1.15 1.19 |
| lineitem scan x8 | MB/s | 408.6 | 567.2 | 1.39 | 1.37 1.41 1.38 |
| lineitem export ADBC | MB/s | 521.8 | 527.0 | 1.01 | 0.99 1.03 1.01 |
| server RSS peak | MB | 1137.0 | 1353.0 | 1.19 | 1.17 1.21 1.19 |

### i22-shared-off-vs-on-sf10-local: A = 881bbf73e946 `-`, B = 881bbf73e946 `-DduckDbSharedDatabase=true`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `sf10 adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | 33.7 | 33.0 | 0.98 | 0.99 0.98 0.98 |
| TPC-H SF10 JDBC (sum of medians) | s | 33.4 | 32.9 | 0.99 | 0.99 0.98 0.99 |
| server RSS peak | MB | 1639.0 | 1915.0 | 1.17 | 1.18 1.17 0.96 |

### i22-shared-vs-native-local: A = 881bbf73e946 `-DduckDbSharedDatabase=true`, B = up-native `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 712.4 | 683.3 | 0.96 | 0.96 0.98 0.94 |
| lineitem scan x4 | MB/s | 854.0 | 875.6 | 1.03 | 1.01 1.07 1.01 |
| lineitem scan x8 | MB/s | 899.7 | n/a | n/a | - |
| lineitem export ADBC | MB/s | 859.0 | 857.7 | 1.00 | 1.00 0.99 1.00 |
| server RSS peak | MB | 1467.0 | 3845.0 | 2.62 | 2.68 2.48 2.67 |

Correctness gate: B: scan8 (rows=382657304 errors=2).
