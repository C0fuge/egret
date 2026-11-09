# Wave fresh-gizmo-deafc861cce3 (server comparison), run 42632367579

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

## Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| fu-load-local | deafc861cce3 `-` | deafc861cce3 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-load-local-vs-gizmo | gizmo `-` | deafc861cce3 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-scan-local | deafc861cce3 `-` | deafc861cce3 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.07 | none |
| fu-scan-local-vs-gizmo | gizmo `-` | deafc861cce3 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: scan1 (rows=0 errors=1), scan4 (rows=0 errors=4), scan8 (rows=0 errors=8) |
| fu-scan-s3 | deafc861cce3 `-` | deafc861cce3 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.05 | none |
| fu-scan-s3-vs-gizmo | gizmo `-` | deafc861cce3 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: scan1 (rows=0 errors=1), scan4 (rows=0 errors=4), scan8 (rows=0 errors=8) |
| fu-sf1-s3 | deafc861cce3 `-` | deafc861cce3 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz | 3/3 | n/a | n/a | n/a | n/a | 0.17 | n/a | n/a | n/a | none |
| fu-sf1-s3-vs-gizmo | gizmo `-` | deafc861cce3 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz | 3/3 | n/a | n/a | n/a | n/a | 1.07 | n/a | n/a | n/a | none |
| fu-sf10adbc-s3 | deafc861cce3 `-` | deafc861cce3 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | 0.17 | n/a | n/a | none |
| fu-sf10adbc-s3-vs-gizmo | gizmo `-` | deafc861cce3 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | 1.51 | n/a | n/a | none |
| fu-sf10jdbc-s3 | deafc861cce3 `-` | deafc861cce3 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | 0.15 | n/a | none |
| fu-sf10jdbc-s3-vs-gizmo | gizmo `-` | deafc861cce3 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | 1.48 | n/a | none |
| fu-small-local | deafc861cce3 `-` | deafc861cce3 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | 1.18 | 0.85 | 1.16 | 0.88 | n/a | n/a | n/a | n/a | none |
| fu-small-local-vs-gizmo | gizmo `-` | deafc861cce3 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: small-adbc1 (answers differ: meta_schemas), small-adbc32 (answers differ: meta_schemas), small-adbc8 (answers differ: meta_schemas), small-jdbc1 (answers differ: meta_schemas), small-jdbc32 (answers differ: meta_schemas), small-jdbc8 (answers differ: meta_schemas) |
| fu-small-s3 | deafc861cce3 `-` | deafc861cce3 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | 0.60 | 0.06 | 0.84 | 0.06 | n/a | n/a | n/a | n/a | none |
| fu-small-s3-vs-gizmo | gizmo `-` | deafc861cce3 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: small-adbc1 (answers differ: meta_schemas), small-adbc32 (answers differ: meta_schemas), small-adbc8 (answers differ: meta_schemas), small-jdbc1 (answers differ: meta_schemas), small-jdbc32 (answers differ: meta_schemas), small-jdbc8 (answers differ: meta_schemas) |
| fu-tpch-local | deafc861cce3 `-` | deafc861cce3 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 0.99 | 0.96 | 0.98 | n/a | none |
| fu-tpch-local-vs-gizmo | gizmo `-` | deafc861cce3 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 1.05 | 1.01 | 1.02 | n/a | none |
| fu-zstd-netem-local | deafc861cce3 `CZSTD` | deafc861cce3 `-DresourceProfile=speed CZSTD` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-zstd-netem-local-vs-gizmo | gizmo `-` | deafc861cce3 `-DresourceProfile=speed CZSTD` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |

## Per job (absolute medians and ratios)

### fu-load-local: A = deafc861cce3 `-`, B = deafc861cce3 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 4537.0 | 904.0 | 0.20 | 0.19 0.20 0.19 |

### fu-load-local-vs-gizmo: A = gizmo `-`, B = deafc861cce3 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 565.0 | 904.0 | 1.60 | 1.46 1.68 1.60 |

### fu-scan-local: A = deafc861cce3 `-`, B = deafc861cce3 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 400.0 | 427.7 | 1.07 | 1.03 1.11 1.03 |
| lineitem scan x4 | MB/s | 421.3 | 538.8 | 1.28 | 1.26 1.26 1.29 |
| lineitem scan x8 | MB/s | 383.8 | 556.1 | 1.45 | 1.40 1.45 1.47 |
| lineitem export ADBC | MB/s | 473.7 | 497.3 | 1.05 | 1.05 1.07 1.01 |
| server RSS peak | MB | 1110.0 | 1103.0 | 0.99 | 1.02 0.99 0.98 |

### fu-scan-local-vs-gizmo: A = gizmo `-`, B = deafc861cce3 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | n/a | 427.7 | n/a | - |
| lineitem scan x4 | MB/s | n/a | 538.8 | n/a | - |
| lineitem scan x8 | MB/s | n/a | 556.1 | n/a | - |
| lineitem export ADBC | MB/s | 489.8 | 497.3 | 1.02 | 1.01 1.03 1.00 |
| server RSS peak | MB | 230.0 | 1103.0 | 4.80 | 4.63 4.80 4.83 |

Correctness gate: A: scan1 (rows=0 errors=1), scan4 (rows=0 errors=4), scan8 (rows=0 errors=8).

### fu-scan-s3: A = deafc861cce3 `-`, B = deafc861cce3 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 596.8 | 629.3 | 1.05 | 1.21 1.05 1.03 |
| lineitem scan x4 | MB/s | 676.3 | 959.4 | 1.42 | 1.41 1.39 1.45 |
| lineitem scan x8 | MB/s | 670.8 | 956.2 | 1.43 | 1.44 1.43 1.45 |
| lineitem export ADBC | MB/s | 712.9 | 799.0 | 1.12 | 1.23 1.12 0.95 |
| server RSS peak | MB | 1743.0 | 3092.0 | 1.77 | 1.80 1.78 1.68 |

### fu-scan-s3-vs-gizmo: A = gizmo `-`, B = deafc861cce3 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | n/a | 629.3 | n/a | - |
| lineitem scan x4 | MB/s | n/a | 959.4 | n/a | - |
| lineitem scan x8 | MB/s | n/a | 956.2 | n/a | - |
| lineitem export ADBC | MB/s | 672.0 | 799.0 | 1.19 | 1.24 1.19 1.00 |
| server RSS peak | MB | 2348.0 | 3092.0 | 1.32 | 1.31 1.32 1.26 |

Correctness gate: A: scan1 (rows=0 errors=1), scan4 (rows=0 errors=4), scan8 (rows=0 errors=8).

### fu-sf1-s3: A = deafc861cce3 `-`, B = deafc861cce3 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 25.5 | 4.4 | 0.17 | 0.17 0.17 0.18 |
| TPC-H SF1 JDBC (sum of medians) | s | 25.5 | 4.5 | 0.18 | 0.17 0.18 0.17 |
| server RSS peak | MB | 738.0 | 938.0 | 1.27 | 1.31 1.27 1.27 |

### fu-sf1-s3-vs-gizmo: A = gizmo `-`, B = deafc861cce3 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 4.2 | 4.4 | 1.07 | 1.04 1.06 1.10 |
| TPC-H SF1 JDBC (sum of medians) | s | 4.3 | 4.5 | 1.03 | 0.98 1.03 1.08 |
| server RSS peak | MB | 568.0 | 938.0 | 1.65 | 1.67 1.65 1.64 |

### fu-sf10adbc-s3: A = deafc861cce3 `-`, B = deafc861cce3 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | 298.9 | 50.4 | 0.17 | 0.18 0.16 0.18 |
| server RSS peak | MB | 1617.0 | 3047.0 | 1.88 | 1.89 1.86 1.96 |

### fu-sf10adbc-s3-vs-gizmo: A = gizmo `-`, B = deafc861cce3 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | 33.5 | 50.4 | 1.51 | 1.60 1.46 1.49 |
| server RSS peak | MB | 3820.0 | 3047.0 | 0.80 | 0.79 0.80 0.78 |

### fu-sf10jdbc-s3: A = deafc861cce3 `-`, B = deafc861cce3 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `sf10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 JDBC (sum of medians) | s | 351.4 | 51.5 | 0.15 | 0.13 0.15 0.16 |
| server RSS peak | MB | 1585.0 | 3006.0 | 1.90 | 1.86 1.89 2.00 |

### fu-sf10jdbc-s3-vs-gizmo: A = gizmo `-`, B = deafc861cce3 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `sf10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 JDBC (sum of medians) | s | 34.7 | 51.5 | 1.48 | 1.18 1.57 1.80 |
| server RSS peak | MB | 3860.0 | 3006.0 | 0.78 | 0.78 0.77 0.86 |

### fu-small-local: A = deafc861cce3 `-`, B = deafc861cce3 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 19.9 | 23.2 | 1.16 | 1.13 1.20 1.15 |
| small JDBC c1 p95 | ms | 40.6 | 40.1 | 0.99 | 0.98 1.03 0.97 |
| small JDBC c1 p99 | ms | 48.9 | 44.6 | 0.91 | 0.86 0.92 0.92 |
| small JDBC c8 p50 | ms | 95.8 | 92.8 | 0.97 | 0.97 0.96 0.90 |
| small JDBC c8 p95 | ms | 241.8 | 227.1 | 0.94 | 0.95 0.90 0.93 |
| small JDBC c8 p99 | ms | 307.0 | 289.2 | 0.94 | 0.98 0.93 0.87 |
| small JDBC c32 p50 | ms | 370.6 | 320.3 | 0.86 | 0.87 0.86 0.88 |
| small JDBC c32 p95 | ms | 1052.6 | 921.9 | 0.88 | 0.88 0.88 0.85 |
| small JDBC c32 p99 | ms | 1399.4 | 1080.8 | 0.77 | 0.76 0.76 0.85 |
| small ADBC c1 p50 | ms | 13.3 | 15.7 | 1.18 | 1.27 1.18 1.19 |
| small ADBC c1 p95 | ms | 34.1 | 35.7 | 1.05 | 0.96 0.99 1.05 |
| small ADBC c1 p99 | ms | 46.7 | 45.0 | 0.96 | 0.98 0.84 0.98 |
| small ADBC c8 p50 | ms | 82.2 | 81.8 | 0.99 | 1.01 0.92 1.01 |
| small ADBC c8 p95 | ms | 235.5 | 229.0 | 0.97 | 0.99 0.98 0.95 |
| small ADBC c8 p99 | ms | 345.8 | 310.4 | 0.90 | 0.72 0.90 0.97 |
| small ADBC c32 p50 | ms | 336.9 | 348.7 | 1.03 | 0.95 1.03 1.07 |
| small ADBC c32 p95 | ms | 1056.6 | 894.2 | 0.85 | 0.85 0.89 0.82 |
| small ADBC c32 p99 | ms | 1345.9 | 1174.2 | 0.87 | 0.92 0.87 0.74 |
| server RSS peak | MB | 1470.0 | 788.0 | 0.54 | 0.52 0.54 0.55 |

### fu-small-local-vs-gizmo: A = gizmo `-`, B = deafc861cce3 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | n/a | 23.2 | n/a | - |
| small JDBC c1 p95 | ms | n/a | 40.1 | n/a | - |
| small JDBC c1 p99 | ms | n/a | 44.6 | n/a | - |
| small JDBC c8 p50 | ms | n/a | 92.8 | n/a | - |
| small JDBC c8 p95 | ms | n/a | 227.1 | n/a | - |
| small JDBC c8 p99 | ms | n/a | 289.2 | n/a | - |
| small JDBC c32 p50 | ms | n/a | 320.3 | n/a | - |
| small JDBC c32 p95 | ms | n/a | 921.9 | n/a | - |
| small JDBC c32 p99 | ms | n/a | 1080.8 | n/a | - |
| small ADBC c1 p50 | ms | n/a | 15.7 | n/a | - |
| small ADBC c1 p95 | ms | n/a | 35.7 | n/a | - |
| small ADBC c1 p99 | ms | n/a | 45.0 | n/a | - |
| small ADBC c8 p50 | ms | n/a | 81.8 | n/a | - |
| small ADBC c8 p95 | ms | n/a | 229.0 | n/a | - |
| small ADBC c8 p99 | ms | n/a | 310.4 | n/a | - |
| small ADBC c32 p50 | ms | n/a | 348.7 | n/a | - |
| small ADBC c32 p95 | ms | n/a | 894.2 | n/a | - |
| small ADBC c32 p99 | ms | n/a | 1174.2 | n/a | - |
| server RSS peak | MB | 425.0 | 788.0 | 1.85 | 1.66 1.90 1.88 |

Correctness gate: A: small-adbc1 (answers differ: meta_schemas), small-adbc32 (answers differ: meta_schemas), small-adbc8 (answers differ: meta_schemas), small-jdbc1 (answers differ: meta_schemas), small-jdbc32 (answers differ: meta_schemas), small-jdbc8 (answers differ: meta_schemas).

### fu-small-s3: A = deafc861cce3 `-`, B = deafc861cce3 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 33.2 | 27.8 | 0.84 | 0.81 0.84 0.85 |
| small JDBC c1 p95 | ms | 684.5 | 46.9 | 0.07 | 0.08 0.07 0.07 |
| small JDBC c1 p99 | ms | 733.6 | 52.8 | 0.07 | 0.08 0.06 0.07 |
| small JDBC c8 p50 | ms | 315.8 | 83.6 | 0.26 | 0.27 0.25 0.26 |
| small JDBC c8 p95 | ms | 5254.6 | 216.1 | 0.04 | 0.04 0.04 0.04 |
| small JDBC c8 p99 | ms | 5561.7 | 301.1 | 0.05 | 0.05 0.06 0.05 |
| small JDBC c32 p50 | ms | 1073.0 | 237.8 | 0.22 | 0.22 0.22 0.22 |
| small JDBC c32 p95 | ms | 17947.6 | 1048.1 | 0.06 | 0.06 0.06 0.06 |
| small JDBC c32 p99 | ms | 48490.5 | 1185.2 | 0.02 | 0.06 0.02 0.02 |
| small ADBC c1 p50 | ms | 24.2 | 14.6 | 0.60 | 0.58 0.62 0.57 |
| small ADBC c1 p95 | ms | 657.9 | 39.0 | 0.06 | 0.06 0.06 0.06 |
| small ADBC c1 p99 | ms | 714.9 | 48.7 | 0.07 | 0.07 0.07 0.07 |
| small ADBC c8 p50 | ms | 316.9 | 65.2 | 0.21 | 0.21 0.22 0.20 |
| small ADBC c8 p95 | ms | 5348.2 | 204.3 | 0.04 | 0.04 0.04 0.04 |
| small ADBC c8 p99 | ms | 5723.4 | 287.9 | 0.05 | 0.05 0.05 0.05 |
| small ADBC c32 p50 | ms | 1069.0 | 212.5 | 0.20 | 0.20 0.18 0.20 |
| small ADBC c32 p95 | ms | 17865.9 | 996.9 | 0.06 | 0.06 0.06 0.06 |
| small ADBC c32 p99 | ms | 20202.4 | 1142.1 | 0.06 | 0.06 0.06 0.05 |
| server RSS peak | MB | 2216.0 | 1408.0 | 0.64 | 0.63 0.64 0.65 |

### fu-small-s3-vs-gizmo: A = gizmo `-`, B = deafc861cce3 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | n/a | 27.8 | n/a | - |
| small JDBC c1 p95 | ms | n/a | 46.9 | n/a | - |
| small JDBC c1 p99 | ms | n/a | 52.8 | n/a | - |
| small JDBC c8 p50 | ms | n/a | 83.6 | n/a | - |
| small JDBC c8 p95 | ms | n/a | 216.1 | n/a | - |
| small JDBC c8 p99 | ms | n/a | 301.1 | n/a | - |
| small JDBC c32 p50 | ms | n/a | 237.8 | n/a | - |
| small JDBC c32 p95 | ms | n/a | 1048.1 | n/a | - |
| small JDBC c32 p99 | ms | n/a | 1185.2 | n/a | - |
| small ADBC c1 p50 | ms | n/a | 14.6 | n/a | - |
| small ADBC c1 p95 | ms | n/a | 39.0 | n/a | - |
| small ADBC c1 p99 | ms | n/a | 48.7 | n/a | - |
| small ADBC c8 p50 | ms | n/a | 65.2 | n/a | - |
| small ADBC c8 p95 | ms | n/a | 204.3 | n/a | - |
| small ADBC c8 p99 | ms | n/a | 287.9 | n/a | - |
| small ADBC c32 p50 | ms | n/a | 212.5 | n/a | - |
| small ADBC c32 p95 | ms | n/a | 996.9 | n/a | - |
| small ADBC c32 p99 | ms | n/a | 1142.1 | n/a | - |
| server RSS peak | MB | 1015.0 | 1408.0 | 1.39 | 1.34 1.39 1.41 |

Correctness gate: A: small-adbc1 (answers differ: meta_schemas), small-adbc32 (answers differ: meta_schemas), small-adbc8 (answers differ: meta_schemas), small-jdbc1 (answers differ: meta_schemas), small-jdbc32 (answers differ: meta_schemas), small-jdbc8 (answers differ: meta_schemas).

### fu-tpch-local: A = deafc861cce3 `-`, B = deafc861cce3 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 3.2 | 3.2 | 0.99 | 1.00 0.98 0.99 |
| TPC-H SF10 ADBC (sum of medians) | s | 34.1 | 32.6 | 0.96 | 0.97 0.96 0.94 |
| TPC-H SF1 JDBC (sum of medians) | s | 3.3 | 3.3 | 1.00 | 0.98 0.99 1.01 |
| TPC-H SF10 JDBC (sum of medians) | s | 34.1 | 33.3 | 0.98 | 0.98 1.00 0.96 |
| server RSS peak | MB | 1609.0 | 1957.0 | 1.22 | 1.09 1.21 1.25 |

### fu-tpch-local-vs-gizmo: A = gizmo `-`, B = deafc861cce3 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 3.1 | 3.2 | 1.05 | 1.10 1.03 1.05 |
| TPC-H SF10 ADBC (sum of medians) | s | 32.4 | 32.6 | 1.01 | 1.04 0.99 1.00 |
| TPC-H SF1 JDBC (sum of medians) | s | 3.1 | 3.3 | 1.07 | 1.09 1.00 1.07 |
| TPC-H SF10 JDBC (sum of medians) | s | 32.5 | 33.3 | 1.02 | 1.04 1.05 1.01 |
| server RSS peak | MB | 1537.0 | 1957.0 | 1.27 | 1.14 1.23 1.31 |

### fu-zstd-netem-local: A = deafc861cce3 `CZSTD`, B = deafc861cce3 `-DresourceProfile=speed CZSTD`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 1644.0 | 1635.0 | 0.99 | 1.08 0.96 1.07 |

### fu-zstd-netem-local-vs-gizmo: A = gizmo `-`, B = deafc861cce3 `-DresourceProfile=speed CZSTD`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 1478.0 | 1635.0 | 1.11 | 1.06 1.07 1.22 |
