# Wave fresh-up-2ff221447b5d (server comparison), run 42865250390

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

## Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| fu-load-local | 2ff221447b5d `-` | 2ff221447b5d `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-load-local-vs-up-native | up-native `-` | 2ff221447b5d `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-scan-local | 2ff221447b5d `-` | 2ff221447b5d `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.04 | none |
| fu-scan-local-vs-up-native | up-native `-` | 2ff221447b5d `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.05 | A: scan8 (rows=367956628 errors=3; rows=430760728 errors=2) |
| fu-scan-s3 | 2ff221447b5d `-` | 2ff221447b5d `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.05 | none |
| fu-scan-s3-vs-up-native | up-native `-` | 2ff221447b5d `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.04 | A: scan8 (rows=434123676 errors=1; rows=468202396 errors=1) |
| fu-sf1-s3 | 2ff221447b5d `-` | 2ff221447b5d `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc1 (failed q08,q09,q10,q13,q21; failed q09,q10,q13,q21; failed q09,q13,q21), jdbc1 (md5 64ff22581be0 (21/22 ok); md5 7754a7b2f986 (20/22 ok)) |
| fu-sf1-s3-vs-up-native | up-native `-` | 2ff221447b5d `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)) |
| fu-sf10adbc-s3 | 2ff221447b5d `-` | 2ff221447b5d `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc10 (failed q08,q09,q10,q13,q16,q18,q21,q22; failed q08,q09,q10,q13,q18) |
| fu-sf10adbc-s3-vs-up-native | up-native `-` | 2ff221447b5d `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22) |
| fu-sf10jdbc-s3 | 2ff221447b5d `-` | 2ff221447b5d `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: jdbc10 (md5 1251b392a461 (14/22 ok); md5 20941714c548 (17/22 ok); md5 fe761fa99f4b (17/22 ok)) |
| fu-sf10jdbc-s3-vs-up-native | up-native `-` | 2ff221447b5d `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: jdbc10 (md5 50bb2801381f (1/22 ok)) |
| fu-small-local | 2ff221447b5d `-` | 2ff221447b5d `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | 1.11 | 0.91 | 1.07 | 0.89 | n/a | n/a | n/a | n/a | none |
| fu-small-local-vs-up-native | up-native `-` | 2ff221447b5d `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point) |
| fu-small-s3 | 2ff221447b5d `-` | 2ff221447b5d `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | 0.61 | 0.06 | 0.90 | 0.06 | n/a | n/a | n/a | n/a | none |
| fu-small-s3-vs-up-native | up-native `-` | 2ff221447b5d `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-adbc8 (640/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc8 (476/640 errors; 492/640 errors; 564/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point) |
| fu-tpch-local | 2ff221447b5d `-` | 2ff221447b5d `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 0.96 | n/a | n/a | n/a | A: adbc10 (failed q09,q10,q13), jdbc10 (md5 73517ed6356d (19/22 ok)) |
| fu-tpch-local-vs-up-native | up-native `-` | 2ff221447b5d `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)), jdbc10 (md5 50bb2801381f (1/22 ok)) |
| fu-zstd-netem-local | 2ff221447b5d `CZSTD` | 2ff221447b5d `-DresourceProfile=speed CZSTD` | local | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-zstd-netem-local-vs-up-native | up-native `-DflightCompression=zstd` | 2ff221447b5d `-DresourceProfile=speed CZSTD` | local | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |

## Per job (absolute medians and ratios)

### fu-load-local: A = 2ff221447b5d `-`, B = 2ff221447b5d `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 4596.0 | 909.0 | 0.20 | 0.20 0.20 0.20 |

### fu-load-local-vs-up-native: A = up-native `-`, B = 2ff221447b5d `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 963.0 | 909.0 | 0.94 | 0.94 0.87 0.99 |

### fu-scan-local: A = 2ff221447b5d `-`, B = 2ff221447b5d `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 664.0 | 692.4 | 1.04 | 1.07 0.97 1.02 |
| lineitem scan x4 | MB/s | 708.2 | 927.6 | 1.31 | 1.32 1.23 1.26 |
| lineitem scan x8 | MB/s | 644.5 | 923.9 | 1.43 | 1.42 1.39 1.43 |
| lineitem export ADBC | MB/s | 820.1 | 843.8 | 1.03 | 1.04 1.02 1.03 |
| server RSS peak | MB | 1286.0 | 1170.0 | 0.91 | 0.91 0.95 0.89 |

### fu-scan-local-vs-up-native: A = up-native `-`, B = 2ff221447b5d `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 658.8 | 692.4 | 1.05 | 1.08 0.97 1.04 |
| lineitem scan x4 | MB/s | 853.5 | 927.6 | 1.09 | 1.09 1.04 1.05 |
| lineitem scan x8 | MB/s | n/a | 923.9 | n/a | - |
| lineitem export ADBC | MB/s | 797.8 | 843.8 | 1.06 | 1.03 1.07 1.06 |
| server RSS peak | MB | 3745.0 | 1170.0 | 0.31 | 0.31 0.32 0.31 |

Correctness gate: A: scan8 (rows=367956628 errors=3; rows=430760728 errors=2).

### fu-scan-s3: A = 2ff221447b5d `-`, B = 2ff221447b5d `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 366.6 | 384.0 | 1.05 | 1.03 1.07 1.00 |
| lineitem scan x4 | MB/s | 439.4 | 591.7 | 1.35 | 1.33 1.35 1.42 |
| lineitem scan x8 | MB/s | 414.0 | 599.1 | 1.45 | 1.46 1.45 1.43 |
| lineitem export ADBC | MB/s | 439.1 | 550.3 | 1.25 | 1.39 1.23 1.24 |
| server RSS peak | MB | 1705.0 | 3304.0 | 1.94 | 1.94 1.94 1.82 |

### fu-scan-s3-vs-up-native: A = up-native `-`, B = 2ff221447b5d `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 367.8 | 384.0 | 1.04 | 1.03 1.13 1.00 |
| lineitem scan x4 | MB/s | 560.6 | 591.7 | 1.06 | 1.01 1.06 1.07 |
| lineitem scan x8 | MB/s | n/a | 599.1 | n/a | - |
| lineitem export ADBC | MB/s | 537.2 | 550.3 | 1.02 | 1.04 1.00 1.02 |
| server RSS peak | MB | 5940.0 | 3304.0 | 0.56 | 0.56 0.55 0.56 |

Correctness gate: A: scan8 (rows=434123676 errors=1; rows=468202396 errors=1).

### fu-sf1-s3: A = 2ff221447b5d `-`, B = 2ff221447b5d `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | n/a | 4.1 | n/a | - |
| TPC-H SF1 JDBC (sum of medians) | s | n/a | 4.2 | n/a | - |
| server RSS peak | MB | 640.0 | 1013.0 | 1.58 | 1.53 1.49 1.68 |

Correctness gate: A: adbc1 (failed q08,q09,q10,q13,q21; failed q09,q10,q13,q21; failed q09,q13,q21), jdbc1 (md5 64ff22581be0 (21/22 ok); md5 7754a7b2f986 (20/22 ok)).

### fu-sf1-s3-vs-up-native: A = up-native `-`, B = 2ff221447b5d `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | n/a | 4.1 | n/a | - |
| TPC-H SF1 JDBC (sum of medians) | s | n/a | 4.2 | n/a | - |
| server RSS peak | MB | 611.0 | 1013.0 | 1.66 | 1.74 1.43 1.69 |

Correctness gate: A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)).

### fu-sf10adbc-s3: A = 2ff221447b5d `-`, B = 2ff221447b5d `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | n/a | 40.9 | n/a | - |
| server RSS peak | MB | 674.0 | 3571.0 | 5.30 | 5.30 5.07 5.26 |

Correctness gate: A: adbc10 (failed q08,q09,q10,q13,q16,q18,q21,q22; failed q08,q09,q10,q13,q18).

### fu-sf10adbc-s3-vs-up-native: A = up-native `-`, B = 2ff221447b5d `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | n/a | 40.9 | n/a | - |
| server RSS peak | MB | 1042.0 | 3571.0 | 3.43 | 3.46 3.21 3.47 |

Correctness gate: A: adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22).

### fu-sf10jdbc-s3: A = 2ff221447b5d `-`, B = 2ff221447b5d `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `sf10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 JDBC (sum of medians) | s | n/a | 33.7 | n/a | - |
| server RSS peak | MB | 643.0 | 3393.0 | 5.28 | 5.44 5.28 5.21 |

Correctness gate: A: jdbc10 (md5 1251b392a461 (14/22 ok); md5 20941714c548 (17/22 ok); md5 fe761fa99f4b (17/22 ok)).

### fu-sf10jdbc-s3-vs-up-native: A = up-native `-`, B = 2ff221447b5d `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `sf10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 JDBC (sum of medians) | s | n/a | 33.7 | n/a | - |
| server RSS peak | MB | 1051.0 | 3393.0 | 3.23 | 3.19 3.23 3.23 |

Correctness gate: A: jdbc10 (md5 50bb2801381f (1/22 ok)).

### fu-small-local: A = 2ff221447b5d `-`, B = 2ff221447b5d `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 21.3 | 22.9 | 1.07 | 1.10 1.09 0.97 |
| small JDBC c1 p95 | ms | 45.2 | 44.4 | 0.98 | 1.00 0.98 0.97 |
| small JDBC c1 p99 | ms | 50.8 | 56.1 | 1.11 | 1.11 1.08 1.03 |
| small JDBC c8 p50 | ms | 99.0 | 90.4 | 0.91 | 0.86 0.96 0.91 |
| small JDBC c8 p95 | ms | 246.0 | 225.8 | 0.92 | 0.91 1.00 0.89 |
| small JDBC c8 p99 | ms | 309.6 | 286.9 | 0.93 | 0.92 0.97 0.82 |
| small JDBC c32 p50 | ms | 377.1 | 308.2 | 0.82 | 0.82 0.87 0.73 |
| small JDBC c32 p95 | ms | 1049.9 | 932.4 | 0.89 | 0.89 0.91 0.82 |
| small JDBC c32 p99 | ms | 1408.2 | 1085.3 | 0.77 | 0.78 0.80 0.75 |
| small ADBC c1 p50 | ms | 14.2 | 15.8 | 1.11 | 1.19 1.09 1.11 |
| small ADBC c1 p95 | ms | 38.9 | 36.8 | 0.95 | 0.94 1.06 0.89 |
| small ADBC c1 p99 | ms | 51.6 | 44.0 | 0.85 | 0.84 1.14 0.78 |
| small ADBC c8 p50 | ms | 88.0 | 84.0 | 0.96 | 1.01 1.04 0.91 |
| small ADBC c8 p95 | ms | 258.3 | 232.7 | 0.90 | 0.86 0.94 0.89 |
| small ADBC c8 p99 | ms | 344.3 | 322.3 | 0.94 | 0.95 0.94 0.77 |
| small ADBC c32 p50 | ms | 361.6 | 309.2 | 0.85 | 0.83 0.85 0.85 |
| small ADBC c32 p95 | ms | 1032.2 | 938.1 | 0.91 | 0.92 0.91 0.90 |
| small ADBC c32 p99 | ms | 1314.6 | 1120.4 | 0.85 | 0.89 0.84 0.87 |
| server RSS peak | MB | 1547.0 | 895.0 | 0.58 | 0.56 0.58 0.60 |

### fu-small-local-vs-up-native: A = up-native `-`, B = 2ff221447b5d `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | n/a | 22.9 | n/a | - |
| small JDBC c1 p95 | ms | n/a | 44.4 | n/a | - |
| small JDBC c1 p99 | ms | n/a | 56.1 | n/a | - |
| small JDBC c8 p50 | ms | n/a | 90.4 | n/a | - |
| small JDBC c8 p95 | ms | n/a | 225.8 | n/a | - |
| small JDBC c8 p99 | ms | n/a | 286.9 | n/a | - |
| small JDBC c32 p50 | ms | n/a | 308.2 | n/a | - |
| small JDBC c32 p95 | ms | n/a | 932.4 | n/a | - |
| small JDBC c32 p99 | ms | n/a | 1085.3 | n/a | - |
| small ADBC c1 p50 | ms | n/a | 15.8 | n/a | - |
| small ADBC c1 p95 | ms | n/a | 36.8 | n/a | - |
| small ADBC c1 p99 | ms | n/a | 44.0 | n/a | - |
| small ADBC c8 p50 | ms | n/a | 84.0 | n/a | - |
| small ADBC c8 p95 | ms | n/a | 232.7 | n/a | - |
| small ADBC c8 p99 | ms | n/a | 322.3 | n/a | - |
| small ADBC c32 p50 | ms | n/a | 309.2 | n/a | - |
| small ADBC c32 p95 | ms | n/a | 938.1 | n/a | - |
| small ADBC c32 p99 | ms | n/a | 1120.4 | n/a | - |
| server RSS peak | MB | 257.0 | 895.0 | 3.48 | 3.54 3.48 3.53 |

Correctness gate: A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point).

### fu-small-s3: A = 2ff221447b5d `-`, B = 2ff221447b5d `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 32.1 | 28.8 | 0.90 | 0.94 0.84 0.83 |
| small JDBC c1 p95 | ms | 846.6 | 51.8 | 0.06 | 0.18 0.06 0.06 |
| small JDBC c1 p99 | ms | 912.0 | 62.5 | 0.07 | 0.59 0.06 0.07 |
| small JDBC c8 p50 | ms | 376.9 | 86.4 | 0.23 | 0.22 0.25 0.23 |
| small JDBC c8 p95 | ms | 6114.1 | 221.2 | 0.04 | 0.03 0.04 0.04 |
| small JDBC c8 p99 | ms | 8579.9 | 294.7 | 0.03 | 0.04 0.03 0.04 |
| small JDBC c32 p50 | ms | 1165.6 | 246.1 | 0.21 | 0.20 0.21 0.23 |
| small JDBC c32 p95 | ms | 17564.9 | 1017.2 | 0.06 | 0.06 0.06 0.06 |
| small JDBC c32 p99 | ms | 21339.8 | 1147.8 | 0.05 | 0.05 0.05 0.05 |
| small ADBC c1 p50 | ms | 24.6 | 15.0 | 0.61 | 0.61 0.64 0.60 |
| small ADBC c1 p95 | ms | 842.7 | 43.3 | 0.05 | 0.05 0.05 0.05 |
| small ADBC c1 p99 | ms | 896.4 | 57.8 | 0.06 | 0.06 0.06 0.06 |
| small ADBC c8 p50 | ms | 355.2 | 66.0 | 0.19 | 0.19 0.18 0.20 |
| small ADBC c8 p95 | ms | 5924.5 | 211.1 | 0.04 | 0.03 0.04 0.04 |
| small ADBC c8 p99 | ms | 6523.0 | 302.4 | 0.05 | 0.04 0.05 0.05 |
| small ADBC c32 p50 | ms | 1131.5 | 213.0 | 0.19 | 0.20 0.19 0.19 |
| small ADBC c32 p95 | ms | 17113.1 | 1015.3 | 0.06 | 0.06 0.06 0.06 |
| small ADBC c32 p99 | ms | 21138.6 | 1145.3 | 0.05 | 0.06 0.05 0.06 |
| server RSS peak | MB | 2211.0 | 1507.0 | 0.68 | 0.69 0.68 0.68 |

### fu-small-s3-vs-up-native: A = up-native `-`, B = 2ff221447b5d `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | n/a | 28.8 | n/a | - |
| small JDBC c1 p95 | ms | n/a | 51.8 | n/a | - |
| small JDBC c1 p99 | ms | n/a | 62.5 | n/a | - |
| small JDBC c8 p50 | ms | n/a | 86.4 | n/a | - |
| small JDBC c8 p95 | ms | n/a | 221.2 | n/a | - |
| small JDBC c8 p99 | ms | n/a | 294.7 | n/a | - |
| small JDBC c32 p50 | ms | n/a | 246.1 | n/a | - |
| small JDBC c32 p95 | ms | n/a | 1017.2 | n/a | - |
| small JDBC c32 p99 | ms | n/a | 1147.8 | n/a | - |
| small ADBC c1 p50 | ms | n/a | 15.0 | n/a | - |
| small ADBC c1 p95 | ms | n/a | 43.3 | n/a | - |
| small ADBC c1 p99 | ms | n/a | 57.8 | n/a | - |
| small ADBC c8 p50 | ms | n/a | 66.0 | n/a | - |
| small ADBC c8 p95 | ms | n/a | 211.1 | n/a | - |
| small ADBC c8 p99 | ms | n/a | 302.4 | n/a | - |
| small ADBC c32 p50 | ms | n/a | 213.0 | n/a | - |
| small ADBC c32 p95 | ms | n/a | 1015.3 | n/a | - |
| small ADBC c32 p99 | ms | n/a | 1145.3 | n/a | - |
| server RSS peak | MB | 388.0 | 1507.0 | 3.88 | 3.91 4.12 3.88 |

Correctness gate: A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-adbc8 (640/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc8 (476/640 errors; 492/640 errors; 564/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point).

### fu-tpch-local: A = 2ff221447b5d `-`, B = 2ff221447b5d `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 2.6 | 2.5 | 0.96 | 0.98 0.91 0.96 |
| TPC-H SF10 ADBC (sum of medians) | s | n/a | 24.0 | n/a | - |
| TPC-H SF1 JDBC (sum of medians) | s | 2.7 | 2.5 | 0.94 | 0.95 0.92 0.97 |
| TPC-H SF10 JDBC (sum of medians) | s | n/a | 24.2 | n/a | - |
| server RSS peak | MB | 727.0 | 1872.0 | 2.57 | 2.47 2.76 2.54 |

Correctness gate: A: adbc10 (failed q09,q10,q13), jdbc10 (md5 73517ed6356d (19/22 ok)).

### fu-tpch-local-vs-up-native: A = up-native `-`, B = 2ff221447b5d `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | n/a | 2.5 | n/a | - |
| TPC-H SF10 ADBC (sum of medians) | s | n/a | 24.0 | n/a | - |
| TPC-H SF1 JDBC (sum of medians) | s | n/a | 2.5 | n/a | - |
| TPC-H SF10 JDBC (sum of medians) | s | n/a | 24.2 | n/a | - |
| server RSS peak | MB | 365.0 | 1872.0 | 5.13 | 4.82 5.35 5.13 |

Correctness gate: A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)), jdbc10 (md5 50bb2801381f (1/22 ok)).

### fu-zstd-netem-local: A = 2ff221447b5d `CZSTD`, B = 2ff221447b5d `-DresourceProfile=speed CZSTD`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 708.0 | 1775.0 | 2.51 | 2.49 2.53 2.46 |

### fu-zstd-netem-local-vs-up-native: A = up-native `-DflightCompression=zstd`, B = 2ff221447b5d `-DresourceProfile=speed CZSTD`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 604.0 | 1775.0 | 2.94 | 2.96 2.91 2.94 |
