# Wave track-94ad61021d93 (server comparison), run 40699820075

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

## Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| core-def-lat-local | ours-new `-` | 94ad61021d93 `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | 0.97 | 0.87 | 0.90 | 0.90 | n/a | n/a | n/a | 0.91 | none |
| core-def-lat-s3 | ours-new `-` | 94ad61021d93 `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | 1.14 | 0.69 | 0.99 | 0.96 | n/a | n/a | n/a | 0.99 | none |
| core-def-sf1-s3 | ours-new `-` | 94ad61021d93 `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 1.05 | n/a | n/a | n/a | none |
| core-def-sf10adbc-s3 | ours-new `-` | 94ad61021d93 `-` | s3 | Linux ubuntu24 4 vCPU Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz | 3/3 | n/a | n/a | n/a | n/a | n/a | 0.64 | n/a | n/a | none |
| core-def-sf10jdbc-s3 | ours-new `-` | 94ad61021d93 `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | 0.66 | n/a | none |
| core-def-tpch-local | ours-new `-` | 94ad61021d93 `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 0.91 | 1.04 | 1.02 | n/a | none |
| i18-dc-off-vs-on-s3 | 94ad61021d93 `-DdistributedComplete=false` | 94ad61021d93 `-DdistributedComplete=true` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/2 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| i19b-load-local | ours-new `-` | 94ad61021d93 `-` | local | Linux ubuntu24 4 vCPU Intel(R) Xeon(R) 6973P-C | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| i19b-memnone-vs-sized-local | 94ad61021d93 `-DduckDbMemoryLimit=none` | 94ad61021d93 `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | 1.03 | n/a | n/a | none |

## Per job (absolute medians and ratios)

### core-def-lat-local: A = ours-new `-`, B = 94ad61021d93 `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 28.9 | 26.1 | 0.90 | 0.93 0.90 0.95 |
| small JDBC c1 p95 | ms | 54.7 | 50.6 | 0.92 | 0.95 0.92 0.97 |
| small JDBC c1 p99 | ms | 62.0 | 52.8 | 0.85 | 0.89 0.85 0.87 |
| small JDBC c8 p50 | ms | 131.2 | 101.5 | 0.77 | 0.77 0.74 0.83 |
| small JDBC c8 p95 | ms | 307.8 | 300.5 | 0.98 | 1.00 0.98 1.00 |
| small JDBC c8 p99 | ms | 482.0 | 344.5 | 0.71 | 0.77 0.63 0.86 |
| small JDBC c32 p50 | ms | 486.7 | 393.2 | 0.81 | 0.81 0.76 0.81 |
| small JDBC c32 p95 | ms | 1374.9 | 1243.3 | 0.90 | 0.89 0.90 0.92 |
| small JDBC c32 p99 | ms | 1870.2 | 1822.3 | 0.97 | 0.98 0.97 0.91 |
| small ADBC c1 p50 | ms | 19.0 | 18.4 | 0.97 | 0.88 0.98 0.95 |
| small ADBC c1 p95 | ms | 47.6 | 47.0 | 0.99 | 0.98 0.99 1.01 |
| small ADBC c1 p99 | ms | 57.3 | 55.7 | 0.97 | 0.94 1.10 0.92 |
| small ADBC c8 p50 | ms | 117.9 | 86.7 | 0.74 | 0.74 0.71 0.75 |
| small ADBC c8 p95 | ms | 293.2 | 290.3 | 0.99 | 1.05 0.93 1.03 |
| small ADBC c8 p99 | ms | 366.6 | 328.4 | 0.90 | 0.99 0.84 0.94 |
| small ADBC c32 p50 | ms | 449.6 | 362.8 | 0.81 | 0.78 0.81 0.81 |
| small ADBC c32 p95 | ms | 1360.2 | 1188.6 | 0.87 | 0.90 0.85 0.88 |
| small ADBC c32 p99 | ms | 1857.4 | 1427.3 | 0.77 | 0.85 0.75 0.81 |
| lineitem scan x1 | MB/s | 425.9 | 387.7 | 0.91 | 0.92 0.89 0.99 |
| lineitem scan x4 | MB/s | 436.5 | 468.4 | 1.07 | 1.07 1.08 1.07 |
| lineitem scan x8 | MB/s | 410.2 | 484.9 | 1.18 | 1.17 1.18 1.18 |
| lineitem export ADBC | MB/s | 504.9 | 516.3 | 1.02 | 1.00 1.03 1.01 |
| server RSS peak | MB | 1693.0 | 1589.0 | 0.94 | 0.94 0.92 0.94 |

### core-def-lat-s3: A = ours-new `-`, B = 94ad61021d93 `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `small scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 31.1 | 30.7 | 0.99 | 1.09 0.89 0.99 |
| small JDBC c1 p95 | ms | 787.5 | 794.1 | 1.01 | 1.05 1.05 0.97 |
| small JDBC c1 p99 | ms | 849.7 | 868.3 | 1.02 | 1.06 1.01 0.97 |
| small JDBC c8 p50 | ms | 363.7 | 356.0 | 0.98 | 0.85 1.16 1.04 |
| small JDBC c8 p95 | ms | 5840.3 | 6068.8 | 1.04 | 1.08 0.95 0.94 |
| small JDBC c8 p99 | ms | 10047.2 | 8413.0 | 0.84 | 1.62 0.56 0.84 |
| small JDBC c32 p50 | ms | 1133.7 | 1057.0 | 0.93 | 1.03 0.87 0.99 |
| small JDBC c32 p95 | ms | 17394.5 | 16711.3 | 0.96 | 0.96 0.97 0.98 |
| small JDBC c32 p99 | ms | 27082.7 | 26825.9 | 0.99 | 0.81 1.27 0.70 |
| small ADBC c1 p50 | ms | 22.7 | 25.9 | 1.14 | 1.61 1.14 0.80 |
| small ADBC c1 p95 | ms | 778.8 | 838.0 | 1.08 | 1.07 1.09 1.05 |
| small ADBC c1 p99 | ms | 831.3 | 904.0 | 1.09 | 1.19 1.09 1.06 |
| small ADBC c8 p50 | ms | 380.1 | 356.9 | 0.94 | 0.94 0.98 0.93 |
| small ADBC c8 p95 | ms | 5625.8 | 5654.3 | 1.01 | 0.97 1.01 1.02 |
| small ADBC c8 p99 | ms | 6143.4 | 6133.3 | 1.00 | 0.99 1.00 1.43 |
| small ADBC c32 p50 | ms | 1563.4 | 1111.5 | 0.71 | 1.00 0.65 1.00 |
| small ADBC c32 p95 | ms | 23721.4 | 16388.3 | 0.69 | 1.01 0.67 1.09 |
| small ADBC c32 p99 | ms | 27613.1 | 17860.3 | 0.65 | 0.96 0.65 1.31 |
| lineitem scan x1 | MB/s | 395.1 | 391.6 | 0.99 | 0.98 1.13 0.99 |
| lineitem scan x4 | MB/s | 445.1 | 457.0 | 1.03 | 1.03 1.06 1.02 |
| lineitem scan x8 | MB/s | 434.5 | 434.0 | 1.00 | 1.02 0.98 0.99 |
| lineitem export ADBC | MB/s | 444.8 | 442.0 | 0.99 | 0.98 1.19 0.99 |
| server RSS peak | MB | 2689.0 | 2765.0 | 1.03 | 0.95 1.03 1.08 |

### core-def-sf1-s3: A = ours-new `-`, B = 94ad61021d93 `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 23.9 | 25.2 | 1.05 | 1.05 1.07 0.94 |
| TPC-H SF1 JDBC (sum of medians) | s | 24.7 | 24.6 | 0.99 | 1.18 0.69 0.99 |
| server RSS peak | MB | 775.0 | 781.0 | 1.01 | 1.02 1.05 0.99 |

### core-def-sf10adbc-s3: A = ours-new `-`, B = 94ad61021d93 `-`, s3

Runner: Linux ubuntu24 4 vCPU Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | 485.3 | 308.3 | 0.64 | 1.03 0.63 0.98 |
| server RSS peak | MB | 1761.0 | 1540.0 | 0.87 | 0.90 0.86 0.83 |

### core-def-sf10jdbc-s3: A = ours-new `-`, B = 94ad61021d93 `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 JDBC (sum of medians) | s | 499.9 | 328.9 | 0.66 | 0.99 0.66 0.99 |
| server RSS peak | MB | 1685.0 | 1566.0 | 0.93 | 0.91 0.93 0.98 |

### core-def-tpch-local: A = ours-new `-`, B = 94ad61021d93 `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 3.9 | 3.6 | 0.91 | 0.92 0.92 0.89 |
| TPC-H SF10 ADBC (sum of medians) | s | 37.6 | 38.9 | 1.04 | 1.02 1.04 1.01 |
| TPC-H SF1 JDBC (sum of medians) | s | 4.0 | 3.6 | 0.90 | 0.90 0.91 0.91 |
| TPC-H SF10 JDBC (sum of medians) | s | 37.6 | 38.3 | 1.02 | 1.02 1.02 1.02 |
| server RSS peak | MB | 1774.0 | 1555.0 | 0.88 | 0.85 0.88 0.95 |

### i18-dc-off-vs-on-s3: A = 94ad61021d93 `-DdistributedComplete=false`, B = 94ad61021d93 `-DdistributedComplete=true`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `cluster`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 352.0 | 339.5 | 0.96 | 0.95 0.98 |

### i19b-load-local: A = ours-new `-`, B = 94ad61021d93 `-`, local

Runner: Linux ubuntu24 4 vCPU Intel(R) Xeon(R) 6973P-C. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 4855.0 | 5146.0 | 1.06 | 1.07 1.04 1.03 |

### i19b-memnone-vs-sized-local: A = 94ad61021d93 `-DduckDbMemoryLimit=none`, B = 94ad61021d93 `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `adbc10 heavy4a`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | 39.2 | 40.3 | 1.03 | 1.03 1.02 1.03 |
| server RSS peak | MB | 3126.0 | 2749.0 | 0.88 | 0.88 0.88 0.88 |
