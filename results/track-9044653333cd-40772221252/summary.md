# Wave track-9044653333cd (server comparison), run 40772221252

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

## Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| core-def-lat-local | ours-new `-` | 9044653333cd `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | 0.92 | 0.98 | 0.85 | 0.94 | n/a | n/a | n/a | 1.05 | none |
| core-def-lat-s3 | ours-new `-` | 9044653333cd `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | 0.92 | 0.97 | 0.95 | 1.03 | n/a | n/a | n/a | 0.96 | none |
| core-def-sf1-s3 | ours-new `-` | 9044653333cd `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 0.99 | n/a | n/a | n/a | none |
| core-def-sf10adbc-s3 | ours-new `-` | 9044653333cd `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | 1.10 | n/a | n/a | none |
| core-def-sf10jdbc-s3 | ours-new `-` | 9044653333cd `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | 0.97 | n/a | none |
| core-def-tpch-local | ours-new `-` | 9044653333cd `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 0.98 | 1.04 | 1.04 | n/a | none |
| i19b-memnone-vs-sized-local | 9044653333cd `-DduckDbMemoryLimit=none` | 9044653333cd `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | 1.05 | n/a | n/a | none |
| i21-load-local | ours-new `-` | 9044653333cd `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |

## Per job (absolute medians and ratios)

### core-def-lat-local: A = ours-new `-`, B = 9044653333cd `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `small scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 17.9 | 15.2 | 0.85 | 0.72 1.16 0.85 |
| small JDBC c1 p95 | ms | 35.0 | 31.8 | 0.91 | 0.79 1.03 0.93 |
| small JDBC c1 p99 | ms | 45.9 | 43.7 | 0.95 | 1.01 0.86 1.05 |
| small JDBC c8 p50 | ms | 85.0 | 77.7 | 0.91 | 0.85 1.09 0.90 |
| small JDBC c8 p95 | ms | 193.7 | 200.4 | 1.03 | 0.89 1.11 1.03 |
| small JDBC c8 p99 | ms | 253.8 | 261.8 | 1.03 | 0.86 1.16 1.03 |
| small JDBC c32 p50 | ms | 318.6 | 304.8 | 0.96 | 0.86 1.01 0.97 |
| small JDBC c32 p95 | ms | 910.2 | 857.0 | 0.94 | 0.94 0.94 0.94 |
| small JDBC c32 p99 | ms | 1189.5 | 1217.5 | 1.02 | 0.96 1.02 1.05 |
| small ADBC c1 p50 | ms | 11.8 | 10.8 | 0.92 | 0.74 0.97 0.95 |
| small ADBC c1 p95 | ms | 30.9 | 28.5 | 0.92 | 0.70 0.98 0.99 |
| small ADBC c1 p99 | ms | 37.9 | 39.8 | 1.05 | 0.82 1.20 0.96 |
| small ADBC c8 p50 | ms | 75.3 | 69.0 | 0.92 | 0.92 0.90 0.92 |
| small ADBC c8 p95 | ms | 187.2 | 186.9 | 1.00 | 0.87 1.04 1.00 |
| small ADBC c8 p99 | ms | 233.1 | 226.1 | 0.97 | 0.53 1.02 0.94 |
| small ADBC c32 p50 | ms | 311.9 | 284.8 | 0.91 | 0.88 0.99 0.86 |
| small ADBC c32 p95 | ms | 928.9 | 914.7 | 0.98 | 0.88 1.05 0.98 |
| small ADBC c32 p99 | ms | 1303.3 | 1255.9 | 0.96 | 0.82 1.05 0.96 |
| lineitem scan x1 | MB/s | 638.5 | 668.1 | 1.05 | 0.98 1.01 1.06 |
| lineitem scan x4 | MB/s | 667.2 | 729.1 | 1.09 | 1.10 1.00 1.10 |
| lineitem scan x8 | MB/s | 617.3 | 628.5 | 1.02 | 1.04 1.00 1.04 |
| lineitem export ADBC | MB/s | 776.5 | 755.5 | 0.97 | 0.97 0.94 0.99 |
| server RSS peak | MB | 1737.0 | 1712.0 | 0.99 | 1.03 0.95 0.99 |

### core-def-lat-s3: A = ours-new `-`, B = 9044653333cd `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 36.2 | 34.4 | 0.95 | 0.98 0.89 0.93 |
| small JDBC c1 p95 | ms | 681.4 | 697.0 | 1.02 | 1.02 1.02 1.01 |
| small JDBC c1 p99 | ms | 743.3 | 773.1 | 1.04 | 1.06 0.98 1.02 |
| small JDBC c8 p50 | ms | 315.2 | 307.0 | 0.97 | 1.17 1.08 0.97 |
| small JDBC c8 p95 | ms | 5592.9 | 5361.6 | 0.96 | 0.91 0.94 1.05 |
| small JDBC c8 p99 | ms | 6635.9 | 6018.4 | 0.91 | 1.09 0.64 1.05 |
| small JDBC c32 p50 | ms | 1136.8 | 1048.8 | 0.92 | 0.91 0.96 1.39 |
| small JDBC c32 p95 | ms | 17860.7 | 18352.1 | 1.03 | 1.03 1.01 1.38 |
| small JDBC c32 p99 | ms | 24292.1 | 27970.9 | 1.15 | 0.83 1.40 0.85 |
| small ADBC c1 p50 | ms | 28.3 | 26.0 | 0.92 | 1.03 0.76 0.86 |
| small ADBC c1 p95 | ms | 687.2 | 667.1 | 0.97 | 0.96 0.98 0.94 |
| small ADBC c1 p99 | ms | 1145.0 | 715.1 | 0.62 | 0.94 0.62 0.58 |
| small ADBC c8 p50 | ms | 301.3 | 327.6 | 1.09 | 1.21 1.00 1.22 |
| small ADBC c8 p95 | ms | 5552.9 | 5531.1 | 1.00 | 1.00 0.99 1.35 |
| small ADBC c8 p99 | ms | 6035.6 | 6017.8 | 1.00 | 0.86 1.02 1.42 |
| small ADBC c32 p50 | ms | 1201.3 | 1193.5 | 0.99 | 0.99 1.07 1.06 |
| small ADBC c32 p95 | ms | 17670.1 | 17103.5 | 0.97 | 1.00 0.97 1.00 |
| small ADBC c32 p99 | ms | 20859.5 | 20340.3 | 0.98 | 1.03 0.96 0.85 |
| lineitem scan x1 | MB/s | 398.8 | 384.5 | 0.96 | 0.97 0.96 0.96 |
| lineitem scan x4 | MB/s | 442.4 | 435.2 | 0.98 | 0.98 1.00 0.93 |
| lineitem scan x8 | MB/s | 437.7 | 421.1 | 0.96 | 1.00 0.96 0.95 |
| lineitem export ADBC | MB/s | 439.4 | 440.2 | 1.00 | 0.98 1.01 1.06 |
| server RSS peak | MB | 2781.0 | 2699.0 | 0.97 | 0.97 0.99 0.96 |

### core-def-sf1-s3: A = ours-new `-`, B = 9044653333cd `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 24.1 | 23.9 | 0.99 | 1.03 0.96 0.99 |
| TPC-H SF1 JDBC (sum of medians) | s | 24.6 | 23.9 | 0.97 | 0.99 1.00 0.95 |
| server RSS peak | MB | 751.0 | 747.0 | 0.99 | 0.98 0.96 1.01 |

### core-def-sf10adbc-s3: A = ours-new `-`, B = 9044653333cd `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | 260.5 | 285.7 | 1.10 | 1.06 1.10 1.21 |
| server RSS peak | MB | 1676.0 | 1589.0 | 0.95 | 0.90 0.97 0.90 |

### core-def-sf10jdbc-s3: A = ours-new `-`, B = 9044653333cd `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `sf10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 JDBC (sum of medians) | s | 309.9 | 302.2 | 0.97 | 0.97 1.00 1.03 |
| server RSS peak | MB | 1762.0 | 1562.0 | 0.89 | 0.91 0.89 0.87 |

### core-def-tpch-local: A = ours-new `-`, B = 9044653333cd `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 4.2 | 4.1 | 0.98 | 0.99 0.98 0.96 |
| TPC-H SF10 ADBC (sum of medians) | s | 40.2 | 41.7 | 1.04 | 1.04 1.05 1.04 |
| TPC-H SF1 JDBC (sum of medians) | s | 4.2 | 4.2 | 0.98 | 1.01 1.00 0.96 |
| TPC-H SF10 JDBC (sum of medians) | s | 40.9 | 42.4 | 1.04 | 1.03 1.05 1.06 |
| server RSS peak | MB | 1741.0 | 1579.0 | 0.91 | 0.87 1.00 0.90 |

### i19b-memnone-vs-sized-local: A = 9044653333cd `-DduckDbMemoryLimit=none`, B = 9044653333cd `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `adbc10 heavy4a`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | 39.3 | 41.4 | 1.05 | 1.04 1.06 1.06 |
| server RSS peak | MB | 2768.0 | 2846.0 | 1.03 | 1.01 1.05 1.03 |

### i21-load-local: A = ours-new `-`, B = 9044653333cd `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 4512.0 | 4458.0 | 0.99 | 1.00 0.98 1.01 |
