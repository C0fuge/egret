# Wave fresh-gizmo-2ff221447b5d (server comparison), run 42888240521

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

## Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| fu-load-local | 2ff221447b5d `-` | 2ff221447b5d `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-load-local-vs-gizmo | gizmo `-` | 2ff221447b5d `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-scan-local | 2ff221447b5d `-` | 2ff221447b5d `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.01 | none |
| fu-scan-local-vs-gizmo | gizmo `-` | 2ff221447b5d `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 0.90 | none |
| fu-scan-s3 | 2ff221447b5d `-` | 2ff221447b5d `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.06 | none |
| fu-scan-s3-vs-gizmo | gizmo `-` | 2ff221447b5d `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.05 | none |
| fu-sf1-s3 | 2ff221447b5d `-` | 2ff221447b5d `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc1 (failed q08,q09,q10,q13,q21; failed q09,q13,q21; failed q13,q21), jdbc1 (md5 5c660ea0c384 (21/22 ok); md5 64ff22581be0 (21/22 ok); md5 7754a7b2f986 (20/22 ok)) |
| fu-sf1-s3-vs-gizmo | gizmo `-` | 2ff221447b5d `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 1.10 | n/a | n/a | n/a | none |
| fu-sf10adbc-s3 | 2ff221447b5d `-` | 2ff221447b5d `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc10 (failed q08,q09,q10,q13,q16,q18; failed q08,q09,q10,q13,q16,q18,q21,q22; failed q08,q09,q10,q13,q18) |
| fu-sf10adbc-s3-vs-gizmo | gizmo `-` | 2ff221447b5d `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | 1.22 | n/a | n/a | none |
| fu-sf10jdbc-s3 | 2ff221447b5d `-` | 2ff221447b5d `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: jdbc10 (md5 d5efdf8bc372 (16/22 ok); md5 fe761fa99f4b (17/22 ok)) |
| fu-sf10jdbc-s3-vs-gizmo | gizmo `-` | 2ff221447b5d `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | 0.99 | n/a | none |
| fu-small-local | 2ff221447b5d `-` | 2ff221447b5d `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | 1.32 | 0.91 | 1.17 | 0.86 | n/a | n/a | n/a | n/a | none |
| fu-small-local-vs-gizmo | gizmo `-` | 2ff221447b5d `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: small-adbc1 (answers differ: meta_schemas), small-adbc32 (answers differ: meta_schemas), small-adbc8 (answers differ: meta_schemas), small-jdbc1 (answers differ: meta_schemas), small-jdbc32 (answers differ: meta_schemas), small-jdbc8 (answers differ: meta_schemas) |
| fu-small-s3 | 2ff221447b5d `-` | 2ff221447b5d `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C | 3/3 | 0.55 | 0.06 | 0.84 | 0.06 | n/a | n/a | n/a | n/a | none |
| fu-small-s3-vs-gizmo | gizmo `-` | 2ff221447b5d `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: small-adbc1 (answers differ: meta_schemas), small-adbc32 (answers differ: meta_schemas), small-adbc8 (answers differ: meta_schemas), small-jdbc1 (answers differ: meta_schemas), small-jdbc32 (answers differ: meta_schemas), small-jdbc8 (answers differ: meta_schemas) |
| fu-tpch-local | 2ff221447b5d `-` | 2ff221447b5d `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 0.99 | n/a | n/a | n/a | A: adbc10 (failed q09,q10,q13), jdbc10 (md5 73517ed6356d (19/22 ok)) |
| fu-tpch-local-vs-gizmo | gizmo `-` | 2ff221447b5d `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 1.12 | 1.01 | 1.01 | n/a | none |
| fu-zstd-netem-local | 2ff221447b5d `CZSTD` | 2ff221447b5d `-DresourceProfile=speed CZSTD` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-zstd-netem-local-vs-gizmo | gizmo `-` | 2ff221447b5d `-DresourceProfile=speed CZSTD` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |

## Per job (absolute medians and ratios)

### fu-load-local: A = 2ff221447b5d `-`, B = 2ff221447b5d `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 4723.0 | 902.0 | 0.19 | 0.19 0.19 0.21 |

### fu-load-local-vs-gizmo: A = gizmo `-`, B = 2ff221447b5d `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 558.0 | 902.0 | 1.62 | 1.50 1.62 1.76 |

### fu-scan-local: A = 2ff221447b5d `-`, B = 2ff221447b5d `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 412.4 | 416.3 | 1.01 | 1.04 1.01 0.99 |
| lineitem scan x4 | MB/s | 421.1 | 546.3 | 1.30 | 1.29 1.30 1.29 |
| lineitem scan x8 | MB/s | 389.3 | 558.4 | 1.43 | 1.43 1.44 1.43 |
| lineitem export ADBC | MB/s | 480.0 | 500.4 | 1.04 | 1.04 1.03 1.05 |
| server RSS peak | MB | 1138.0 | 1133.0 | 1.00 | 0.98 1.00 1.01 |

### fu-scan-local-vs-gizmo: A = gizmo `-`, B = 2ff221447b5d `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 460.8 | 416.3 | 0.90 | 0.91 0.90 0.91 |
| lineitem scan x4 | MB/s | 558.6 | 546.3 | 0.98 | 0.99 0.97 0.96 |
| lineitem scan x8 | MB/s | 562.2 | 558.4 | 0.99 | 1.00 0.98 0.98 |
| lineitem export ADBC | MB/s | 495.7 | 500.4 | 1.01 | 1.00 1.01 1.01 |
| server RSS peak | MB | 453.0 | 1133.0 | 2.50 | 2.06 2.52 2.51 |

### fu-scan-s3: A = 2ff221447b5d `-`, B = 2ff221447b5d `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 380.0 | 401.6 | 1.06 | 1.03 1.06 1.06 |
| lineitem scan x4 | MB/s | 453.1 | 613.9 | 1.35 | 1.36 1.35 1.35 |
| lineitem scan x8 | MB/s | 428.6 | 616.0 | 1.44 | 1.45 1.44 1.44 |
| lineitem export ADBC | MB/s | 445.7 | 573.6 | 1.29 | 1.44 1.27 1.29 |
| server RSS peak | MB | 1729.0 | 3305.0 | 1.91 | 1.83 1.91 1.97 |

### fu-scan-s3-vs-gizmo: A = gizmo `-`, B = 2ff221447b5d `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 382.9 | 401.6 | 1.05 | 1.02 1.13 1.06 |
| lineitem scan x4 | MB/s | 618.6 | 613.9 | 0.99 | 1.00 1.03 0.97 |
| lineitem scan x8 | MB/s | 634.0 | 616.0 | 0.97 | 0.98 0.97 0.96 |
| lineitem export ADBC | MB/s | 503.9 | 573.6 | 1.14 | 1.14 1.13 1.41 |
| server RSS peak | MB | 2536.0 | 3305.0 | 1.30 | 1.26 1.30 1.32 |

### fu-sf1-s3: A = 2ff221447b5d `-`, B = 2ff221447b5d `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | n/a | 4.1 | n/a | - |
| TPC-H SF1 JDBC (sum of medians) | s | n/a | 4.2 | n/a | - |
| server RSS peak | MB | 660.0 | 995.0 | 1.51 | 1.51 1.50 1.60 |

Correctness gate: A: adbc1 (failed q08,q09,q10,q13,q21; failed q09,q13,q21; failed q13,q21), jdbc1 (md5 5c660ea0c384 (21/22 ok); md5 64ff22581be0 (21/22 ok); md5 7754a7b2f986 (20/22 ok)).

### fu-sf1-s3-vs-gizmo: A = gizmo `-`, B = 2ff221447b5d `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 3.7 | 4.1 | 1.10 | 1.17 1.10 1.10 |
| TPC-H SF1 JDBC (sum of medians) | s | 3.8 | 4.2 | 1.09 | 1.09 1.09 1.09 |
| server RSS peak | MB | 578.0 | 995.0 | 1.72 | 1.82 1.71 1.70 |

### fu-sf10adbc-s3: A = 2ff221447b5d `-`, B = 2ff221447b5d `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | n/a | 46.0 | n/a | - |
| server RSS peak | MB | 661.0 | 3540.0 | 5.36 | 5.18 5.29 5.41 |

Correctness gate: A: adbc10 (failed q08,q09,q10,q13,q16,q18; failed q08,q09,q10,q13,q16,q18,q21,q22; failed q08,q09,q10,q13,q18).

### fu-sf10adbc-s3-vs-gizmo: A = gizmo `-`, B = 2ff221447b5d `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | 37.8 | 46.0 | 1.22 | 1.19 1.43 1.16 |
| server RSS peak | MB | 3805.0 | 3540.0 | 0.93 | 0.89 0.95 0.91 |

### fu-sf10jdbc-s3: A = 2ff221447b5d `-`, B = 2ff221447b5d `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `sf10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 JDBC (sum of medians) | s | n/a | 27.2 | n/a | - |
| server RSS peak | MB | 650.0 | 3369.0 | 5.18 | 5.19 5.18 5.23 |

Correctness gate: A: jdbc10 (md5 d5efdf8bc372 (16/22 ok); md5 fe761fa99f4b (17/22 ok)).

### fu-sf10jdbc-s3-vs-gizmo: A = gizmo `-`, B = 2ff221447b5d `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `sf10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 JDBC (sum of medians) | s | 27.5 | 27.2 | 0.99 | 1.00 0.99 0.86 |
| server RSS peak | MB | 3834.0 | 3369.0 | 0.88 | 0.91 0.88 0.89 |

### fu-small-local: A = 2ff221447b5d `-`, B = 2ff221447b5d `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 18.6 | 21.8 | 1.17 | 1.13 1.17 1.23 |
| small JDBC c1 p95 | ms | 41.4 | 42.6 | 1.03 | 0.97 0.96 1.03 |
| small JDBC c1 p99 | ms | 52.2 | 52.3 | 1.00 | 0.94 0.89 1.15 |
| small JDBC c8 p50 | ms | 96.1 | 91.3 | 0.95 | 0.95 0.94 1.02 |
| small JDBC c8 p95 | ms | 242.2 | 218.4 | 0.90 | 0.95 0.89 0.86 |
| small JDBC c8 p99 | ms | 308.5 | 263.9 | 0.86 | 0.87 0.85 0.78 |
| small JDBC c32 p50 | ms | 375.2 | 300.1 | 0.80 | 0.82 0.80 0.78 |
| small JDBC c32 p95 | ms | 1057.4 | 914.3 | 0.86 | 0.87 0.86 0.90 |
| small JDBC c32 p99 | ms | 1372.3 | 1057.4 | 0.77 | 0.80 0.78 0.76 |
| small ADBC c1 p50 | ms | 12.0 | 15.8 | 1.32 | 1.44 1.23 1.18 |
| small ADBC c1 p95 | ms | 37.2 | 36.6 | 0.98 | 0.97 0.98 0.95 |
| small ADBC c1 p99 | ms | 44.9 | 44.3 | 0.99 | 0.90 0.99 0.88 |
| small ADBC c8 p50 | ms | 82.8 | 83.0 | 1.00 | 1.05 1.01 0.96 |
| small ADBC c8 p95 | ms | 245.7 | 237.7 | 0.97 | 1.02 0.89 1.01 |
| small ADBC c8 p99 | ms | 359.1 | 308.2 | 0.86 | 0.88 0.77 0.91 |
| small ADBC c32 p50 | ms | 353.9 | 307.9 | 0.87 | 0.88 0.77 0.84 |
| small ADBC c32 p95 | ms | 1015.7 | 922.6 | 0.91 | 0.87 0.91 0.91 |
| small ADBC c32 p99 | ms | 1323.9 | 1092.8 | 0.83 | 0.79 0.90 0.88 |
| server RSS peak | MB | 1522.0 | 908.0 | 0.60 | 0.60 0.59 0.58 |

### fu-small-local-vs-gizmo: A = gizmo `-`, B = 2ff221447b5d `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | n/a | 21.8 | n/a | - |
| small JDBC c1 p95 | ms | n/a | 42.6 | n/a | - |
| small JDBC c1 p99 | ms | n/a | 52.3 | n/a | - |
| small JDBC c8 p50 | ms | n/a | 91.3 | n/a | - |
| small JDBC c8 p95 | ms | n/a | 218.4 | n/a | - |
| small JDBC c8 p99 | ms | n/a | 263.9 | n/a | - |
| small JDBC c32 p50 | ms | n/a | 300.1 | n/a | - |
| small JDBC c32 p95 | ms | n/a | 914.3 | n/a | - |
| small JDBC c32 p99 | ms | n/a | 1057.4 | n/a | - |
| small ADBC c1 p50 | ms | n/a | 15.8 | n/a | - |
| small ADBC c1 p95 | ms | n/a | 36.6 | n/a | - |
| small ADBC c1 p99 | ms | n/a | 44.3 | n/a | - |
| small ADBC c8 p50 | ms | n/a | 83.0 | n/a | - |
| small ADBC c8 p95 | ms | n/a | 237.7 | n/a | - |
| small ADBC c8 p99 | ms | n/a | 308.2 | n/a | - |
| small ADBC c32 p50 | ms | n/a | 307.9 | n/a | - |
| small ADBC c32 p95 | ms | n/a | 922.6 | n/a | - |
| small ADBC c32 p99 | ms | n/a | 1092.8 | n/a | - |
| server RSS peak | MB | 429.0 | 908.0 | 2.12 | 1.90 2.12 2.10 |

Correctness gate: A: small-adbc1 (answers differ: meta_schemas), small-adbc32 (answers differ: meta_schemas), small-adbc8 (answers differ: meta_schemas), small-jdbc1 (answers differ: meta_schemas), small-jdbc32 (answers differ: meta_schemas), small-jdbc8 (answers differ: meta_schemas).

### fu-small-s3: A = 2ff221447b5d `-`, B = 2ff221447b5d `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 28.3 | 23.6 | 0.84 | 0.84 0.91 0.83 |
| small JDBC c1 p95 | ms | 699.2 | 40.5 | 0.06 | 0.06 0.06 0.06 |
| small JDBC c1 p99 | ms | 774.3 | 45.4 | 0.06 | 0.06 0.07 0.03 |
| small JDBC c8 p50 | ms | 262.2 | 69.3 | 0.26 | 0.28 0.24 0.27 |
| small JDBC c8 p95 | ms | 3876.7 | 180.7 | 0.05 | 0.04 0.05 0.05 |
| small JDBC c8 p99 | ms | 4274.2 | 222.5 | 0.05 | 0.05 0.05 0.05 |
| small JDBC c32 p50 | ms | 971.2 | 191.6 | 0.20 | 0.20 0.20 0.20 |
| small JDBC c32 p95 | ms | 12982.7 | 799.7 | 0.06 | 0.06 0.06 0.07 |
| small JDBC c32 p99 | ms | 14758.6 | 952.8 | 0.06 | 0.06 0.06 0.07 |
| small ADBC c1 p50 | ms | 21.3 | 11.7 | 0.55 | 0.55 0.58 0.52 |
| small ADBC c1 p95 | ms | 698.3 | 32.5 | 0.05 | 0.04 0.05 0.05 |
| small ADBC c1 p99 | ms | 784.3 | 39.4 | 0.05 | 0.05 0.05 0.06 |
| small ADBC c8 p50 | ms | 259.8 | 55.9 | 0.22 | 0.21 0.22 0.21 |
| small ADBC c8 p95 | ms | 3939.4 | 170.4 | 0.04 | 0.04 0.04 0.04 |
| small ADBC c8 p99 | ms | 4383.1 | 220.0 | 0.05 | 0.05 0.03 0.05 |
| small ADBC c32 p50 | ms | 940.6 | 177.1 | 0.19 | 0.20 0.19 0.18 |
| small ADBC c32 p95 | ms | 13738.2 | 789.4 | 0.06 | 0.06 0.06 0.06 |
| small ADBC c32 p99 | ms | 15036.5 | 921.4 | 0.06 | 0.06 0.06 0.06 |
| server RSS peak | MB | 2284.0 | 1530.0 | 0.67 | 0.70 0.67 0.68 |

### fu-small-s3-vs-gizmo: A = gizmo `-`, B = 2ff221447b5d `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | n/a | 23.6 | n/a | - |
| small JDBC c1 p95 | ms | n/a | 40.5 | n/a | - |
| small JDBC c1 p99 | ms | n/a | 45.4 | n/a | - |
| small JDBC c8 p50 | ms | n/a | 69.3 | n/a | - |
| small JDBC c8 p95 | ms | n/a | 180.7 | n/a | - |
| small JDBC c8 p99 | ms | n/a | 222.5 | n/a | - |
| small JDBC c32 p50 | ms | n/a | 191.6 | n/a | - |
| small JDBC c32 p95 | ms | n/a | 799.7 | n/a | - |
| small JDBC c32 p99 | ms | n/a | 952.8 | n/a | - |
| small ADBC c1 p50 | ms | n/a | 11.7 | n/a | - |
| small ADBC c1 p95 | ms | n/a | 32.5 | n/a | - |
| small ADBC c1 p99 | ms | n/a | 39.4 | n/a | - |
| small ADBC c8 p50 | ms | n/a | 55.9 | n/a | - |
| small ADBC c8 p95 | ms | n/a | 170.4 | n/a | - |
| small ADBC c8 p99 | ms | n/a | 220.0 | n/a | - |
| small ADBC c32 p50 | ms | n/a | 177.1 | n/a | - |
| small ADBC c32 p95 | ms | n/a | 789.4 | n/a | - |
| small ADBC c32 p99 | ms | n/a | 921.4 | n/a | - |
| server RSS peak | MB | 1017.0 | 1530.0 | 1.50 | 1.48 1.51 1.53 |

Correctness gate: A: small-adbc1 (answers differ: meta_schemas), small-adbc32 (answers differ: meta_schemas), small-adbc8 (answers differ: meta_schemas), small-jdbc1 (answers differ: meta_schemas), small-jdbc32 (answers differ: meta_schemas), small-jdbc8 (answers differ: meta_schemas).

### fu-tpch-local: A = 2ff221447b5d `-`, B = 2ff221447b5d `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 3.4 | 3.3 | 0.99 | 0.98 1.01 0.97 |
| TPC-H SF10 ADBC (sum of medians) | s | n/a | 32.7 | n/a | - |
| TPC-H SF1 JDBC (sum of medians) | s | 3.5 | 3.4 | 0.97 | 0.96 0.97 0.96 |
| TPC-H SF10 JDBC (sum of medians) | s | n/a | 32.5 | n/a | - |
| server RSS peak | MB | 720.0 | 1851.0 | 2.57 | 2.34 2.43 2.66 |

Correctness gate: A: adbc10 (failed q09,q10,q13), jdbc10 (md5 73517ed6356d (19/22 ok)).

### fu-tpch-local-vs-gizmo: A = gizmo `-`, B = 2ff221447b5d `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 3.0 | 3.3 | 1.12 | 1.11 1.14 1.11 |
| TPC-H SF10 ADBC (sum of medians) | s | 32.3 | 32.7 | 1.01 | 1.02 1.00 1.01 |
| TPC-H SF1 JDBC (sum of medians) | s | 3.1 | 3.4 | 1.10 | 1.11 1.10 1.10 |
| TPC-H SF10 JDBC (sum of medians) | s | 32.3 | 32.5 | 1.01 | 1.01 1.02 1.01 |
| server RSS peak | MB | 1593.0 | 1851.0 | 1.16 | 1.18 1.09 1.19 |

### fu-zstd-netem-local: A = 2ff221447b5d `CZSTD`, B = 2ff221447b5d `-DresourceProfile=speed CZSTD`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 774.0 | 1638.0 | 2.12 | 2.11 2.06 2.69 |

### fu-zstd-netem-local-vs-gizmo: A = gizmo `-`, B = 2ff221447b5d `-DresourceProfile=speed CZSTD`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 1475.0 | 1638.0 | 1.11 | 1.11 1.12 1.20 |
