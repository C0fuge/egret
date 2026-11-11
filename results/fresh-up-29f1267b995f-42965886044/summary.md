# Wave fresh-up-29f1267b995f (server comparison), run 42965886044

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

## Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| fu-load-local | 29f1267b995f `-` | 29f1267b995f `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-load-local-vs-up-native | up-native `-` | 29f1267b995f `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-scan-local | 29f1267b995f `-` | 29f1267b995f `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.00 | none |
| fu-scan-local-vs-up-native | up-native `-` | 29f1267b995f `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.03 | A: scan8 (rows=390062872 errors=2) |
| fu-scan-s3 | 29f1267b995f `-` | 29f1267b995f `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.06 | none |
| fu-scan-s3-vs-up-native | up-native `-` | 29f1267b995f `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.08 | A: scan8 (rows=343315092 errors=3) |
| fu-sf1-s3 | 29f1267b995f `-` | 29f1267b995f `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 0.16 | n/a | n/a | n/a | none |
| fu-sf1-s3-vs-up-native | up-native `-` | 29f1267b995f `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)) |
| fu-sf10adbc-s3 | 29f1267b995f `-` | 29f1267b995f `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | 0.12 | n/a | n/a | none |
| fu-sf10adbc-s3-vs-up-native | up-native `-` | 29f1267b995f `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22) |
| fu-sf10jdbc-s3 | 29f1267b995f `-` | 29f1267b995f `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | 0.13 | n/a | none |
| fu-sf10jdbc-s3-vs-up-native | up-native `-` | 29f1267b995f `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: jdbc10 (md5 50bb2801381f (1/22 ok)) |
| fu-small-local | 29f1267b995f `-` | 29f1267b995f `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | 1.16 | 0.88 | 1.19 | 0.89 | n/a | n/a | n/a | n/a | none |
| fu-small-local-vs-up-native | up-native `-` | 29f1267b995f `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point) |
| fu-small-s3 | 29f1267b995f `-` | 29f1267b995f `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | 0.48 | 0.06 | 0.57 | 0.07 | n/a | n/a | n/a | n/a | none |
| fu-small-s3-vs-up-native | up-native `-` | 29f1267b995f `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-adbc8 (640/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc8 (471/640 errors; 518/640 errors; 525/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point) |
| fu-tpch-local | 29f1267b995f `-` | 29f1267b995f `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C | 3/3 | n/a | n/a | n/a | n/a | 1.01 | 0.96 | 0.96 | n/a | none |
| fu-tpch-local-vs-up-native | up-native `-` | 29f1267b995f `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)), jdbc10 (md5 50bb2801381f (1/22 ok)) |
| fu-zstd-netem-local | 29f1267b995f `CZSTD` | 29f1267b995f `-DresourceProfile=speed CZSTD` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-zstd-netem-local-vs-up-native | up-native `-DflightCompression=zstd` | 29f1267b995f `-DresourceProfile=speed CZSTD` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |

## Per job (absolute medians and ratios)

### fu-load-local: A = 29f1267b995f `-`, B = 29f1267b995f `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 4794.0 | 986.0 | 0.21 | 0.19 0.21 0.20 |

### fu-load-local-vs-up-native: A = up-native `-`, B = 29f1267b995f `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 989.0 | 986.0 | 1.00 | 0.93 0.99 1.00 |

### fu-scan-local: A = 29f1267b995f `-`, B = 29f1267b995f `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 450.6 | 450.2 | 1.00 | 0.98 1.01 1.01 |
| lineitem scan x4 | MB/s | 470.0 | 604.2 | 1.29 | 1.28 1.26 1.33 |
| lineitem scan x8 | MB/s | 422.3 | 617.6 | 1.46 | 1.46 1.46 1.47 |
| lineitem export ADBC | MB/s | 544.8 | 549.7 | 1.01 | 1.01 1.05 1.01 |
| server RSS peak | MB | 1148.0 | 1166.0 | 1.02 | 1.03 1.00 1.02 |

### fu-scan-local-vs-up-native: A = up-native `-`, B = 29f1267b995f `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 438.2 | 450.2 | 1.03 | 1.01 1.04 1.03 |
| lineitem scan x4 | MB/s | 584.5 | 604.2 | 1.03 | 1.03 1.10 1.03 |
| lineitem scan x8 | MB/s | n/a | 617.6 | n/a | - |
| lineitem export ADBC | MB/s | 556.2 | 549.7 | 0.99 | 0.99 1.00 0.98 |
| server RSS peak | MB | 3842.0 | 1166.0 | 0.30 | 0.31 0.30 0.30 |

Correctness gate: A: scan8 (rows=390062872 errors=2).

### fu-scan-s3: A = 29f1267b995f `-`, B = 29f1267b995f `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 382.3 | 404.3 | 1.06 | 1.04 1.08 1.06 |
| lineitem scan x4 | MB/s | 460.9 | 618.2 | 1.34 | 1.33 1.34 1.34 |
| lineitem scan x8 | MB/s | 436.2 | 632.7 | 1.45 | 1.44 1.43 1.46 |
| lineitem export ADBC | MB/s | 414.4 | 566.9 | 1.37 | 1.39 1.37 1.35 |
| server RSS peak | MB | 1765.0 | 3310.0 | 1.88 | 1.86 1.87 1.92 |

### fu-scan-s3-vs-up-native: A = up-native `-`, B = 29f1267b995f `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 374.1 | 404.3 | 1.08 | 1.24 1.11 1.05 |
| lineitem scan x4 | MB/s | 605.4 | 618.2 | 1.02 | 1.02 1.04 1.02 |
| lineitem scan x8 | MB/s | n/a | 632.7 | n/a | - |
| lineitem export ADBC | MB/s | 556.6 | 566.9 | 1.02 | 1.02 1.02 1.01 |
| server RSS peak | MB | 5900.0 | 3310.0 | 0.56 | 0.56 0.56 0.56 |

Correctness gate: A: scan8 (rows=343315092 errors=3).

### fu-sf1-s3: A = 29f1267b995f `-`, B = 29f1267b995f `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 26.5 | 4.2 | 0.16 | 0.16 0.16 0.16 |
| TPC-H SF1 JDBC (sum of medians) | s | 26.2 | 4.2 | 0.16 | 0.16 0.17 0.16 |
| server RSS peak | MB | 757.0 | 975.0 | 1.29 | 1.28 1.29 1.30 |

### fu-sf1-s3-vs-up-native: A = up-native `-`, B = 29f1267b995f `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | n/a | 4.2 | n/a | - |
| TPC-H SF1 JDBC (sum of medians) | s | n/a | 4.2 | n/a | - |
| server RSS peak | MB | 579.0 | 975.0 | 1.68 | 1.68 1.68 1.62 |

Correctness gate: A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)).

### fu-sf10adbc-s3: A = 29f1267b995f `-`, B = 29f1267b995f `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | 269.7 | 33.0 | 0.12 | 0.15 0.11 0.12 |
| server RSS peak | MB | 1573.0 | 3419.0 | 2.17 | 2.19 2.16 2.16 |

### fu-sf10adbc-s3-vs-up-native: A = up-native `-`, B = 29f1267b995f `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | n/a | 33.0 | n/a | - |
| server RSS peak | MB | 1063.0 | 3419.0 | 3.22 | 3.22 3.37 3.19 |

Correctness gate: A: adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22).

### fu-sf10jdbc-s3: A = 29f1267b995f `-`, B = 29f1267b995f `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 JDBC (sum of medians) | s | 287.1 | 38.1 | 0.13 | 0.13 0.13 0.13 |
| server RSS peak | MB | 1641.0 | 3378.0 | 2.06 | 2.05 2.14 2.08 |

### fu-sf10jdbc-s3-vs-up-native: A = up-native `-`, B = 29f1267b995f `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 JDBC (sum of medians) | s | n/a | 38.1 | n/a | - |
| server RSS peak | MB | 1043.0 | 3378.0 | 3.24 | 3.21 3.24 3.34 |

Correctness gate: A: jdbc10 (md5 50bb2801381f (1/22 ok)).

### fu-small-local: A = 29f1267b995f `-`, B = 29f1267b995f `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 19.0 | 22.7 | 1.19 | 1.12 1.09 1.19 |
| small JDBC c1 p95 | ms | 42.6 | 42.8 | 1.01 | 0.94 1.07 1.01 |
| small JDBC c1 p99 | ms | 48.4 | 51.5 | 1.07 | 0.96 1.12 1.06 |
| small JDBC c8 p50 | ms | 98.6 | 90.2 | 0.91 | 0.92 0.93 0.89 |
| small JDBC c8 p95 | ms | 248.2 | 228.2 | 0.92 | 0.90 0.96 0.95 |
| small JDBC c8 p99 | ms | 290.7 | 297.6 | 1.02 | 1.04 1.01 1.01 |
| small JDBC c32 p50 | ms | 371.6 | 299.6 | 0.81 | 0.84 0.81 0.80 |
| small JDBC c32 p95 | ms | 1056.4 | 945.0 | 0.89 | 0.89 0.93 0.88 |
| small JDBC c32 p99 | ms | 1374.8 | 1084.0 | 0.79 | 0.71 0.83 0.80 |
| small ADBC c1 p50 | ms | 13.0 | 15.1 | 1.16 | 1.14 1.17 1.16 |
| small ADBC c1 p95 | ms | 34.6 | 37.6 | 1.09 | 1.08 1.02 1.15 |
| small ADBC c1 p99 | ms | 41.8 | 42.8 | 1.02 | 1.02 1.07 1.04 |
| small ADBC c8 p50 | ms | 86.7 | 86.6 | 1.00 | 1.01 0.93 1.04 |
| small ADBC c8 p95 | ms | 252.8 | 228.2 | 0.90 | 0.94 0.96 0.87 |
| small ADBC c8 p99 | ms | 370.9 | 320.3 | 0.86 | 0.86 1.01 0.78 |
| small ADBC c32 p50 | ms | 348.3 | 298.2 | 0.86 | 0.90 0.86 0.86 |
| small ADBC c32 p95 | ms | 1065.9 | 935.8 | 0.88 | 0.88 0.88 0.93 |
| small ADBC c32 p99 | ms | 1298.4 | 1102.8 | 0.85 | 0.82 0.85 0.86 |
| server RSS peak | MB | 1519.0 | 875.0 | 0.58 | 0.57 0.58 0.57 |

### fu-small-local-vs-up-native: A = up-native `-`, B = 29f1267b995f `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | n/a | 22.7 | n/a | - |
| small JDBC c1 p95 | ms | n/a | 42.8 | n/a | - |
| small JDBC c1 p99 | ms | n/a | 51.5 | n/a | - |
| small JDBC c8 p50 | ms | n/a | 90.2 | n/a | - |
| small JDBC c8 p95 | ms | n/a | 228.2 | n/a | - |
| small JDBC c8 p99 | ms | n/a | 297.6 | n/a | - |
| small JDBC c32 p50 | ms | n/a | 299.6 | n/a | - |
| small JDBC c32 p95 | ms | n/a | 945.0 | n/a | - |
| small JDBC c32 p99 | ms | n/a | 1084.0 | n/a | - |
| small ADBC c1 p50 | ms | n/a | 15.1 | n/a | - |
| small ADBC c1 p95 | ms | n/a | 37.6 | n/a | - |
| small ADBC c1 p99 | ms | n/a | 42.8 | n/a | - |
| small ADBC c8 p50 | ms | n/a | 86.6 | n/a | - |
| small ADBC c8 p95 | ms | n/a | 228.2 | n/a | - |
| small ADBC c8 p99 | ms | n/a | 320.3 | n/a | - |
| small ADBC c32 p50 | ms | n/a | 298.2 | n/a | - |
| small ADBC c32 p95 | ms | n/a | 935.8 | n/a | - |
| small ADBC c32 p99 | ms | n/a | 1102.8 | n/a | - |
| server RSS peak | MB | 257.0 | 875.0 | 3.40 | 3.35 3.39 3.43 |

Correctness gate: A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point).

### fu-small-s3: A = 29f1267b995f `-`, B = 29f1267b995f `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 47.0 | 26.7 | 0.57 | 0.75 0.69 0.50 |
| small JDBC c1 p95 | ms | 766.5 | 93.6 | 0.12 | 0.18 0.15 0.05 |
| small JDBC c1 p99 | ms | 1154.2 | 191.1 | 0.17 | 0.33 0.17 0.05 |
| small JDBC c8 p50 | ms | 237.4 | 71.7 | 0.30 | 0.27 0.36 0.29 |
| small JDBC c8 p95 | ms | 3571.5 | 185.2 | 0.05 | 0.06 0.05 0.05 |
| small JDBC c8 p99 | ms | 4172.7 | 278.1 | 0.07 | 0.10 0.06 0.07 |
| small JDBC c32 p50 | ms | 959.7 | 203.6 | 0.21 | 0.20 0.22 0.21 |
| small JDBC c32 p95 | ms | 12014.9 | 794.5 | 0.07 | 0.07 0.07 0.07 |
| small JDBC c32 p99 | ms | 13327.2 | 956.4 | 0.07 | 0.07 0.07 0.07 |
| small ADBC c1 p50 | ms | 26.8 | 12.9 | 0.48 | 0.50 0.49 0.29 |
| small ADBC c1 p95 | ms | 674.4 | 31.9 | 0.05 | 0.05 0.05 0.04 |
| small ADBC c1 p99 | ms | 1201.1 | 41.1 | 0.03 | 0.03 0.04 0.03 |
| small ADBC c8 p50 | ms | 258.6 | 55.0 | 0.21 | 0.21 0.23 0.20 |
| small ADBC c8 p95 | ms | 3606.9 | 164.3 | 0.05 | 0.05 0.05 0.04 |
| small ADBC c8 p99 | ms | 4524.5 | 217.3 | 0.05 | 0.06 0.04 0.05 |
| small ADBC c32 p50 | ms | 921.8 | 170.2 | 0.18 | 0.17 0.21 0.19 |
| small ADBC c32 p95 | ms | 12526.2 | 794.1 | 0.06 | 0.06 0.07 0.06 |
| small ADBC c32 p99 | ms | 14316.7 | 942.5 | 0.07 | 0.07 0.07 0.03 |
| server RSS peak | MB | 2319.0 | 1496.0 | 0.65 | 0.66 0.64 0.65 |

### fu-small-s3-vs-up-native: A = up-native `-`, B = 29f1267b995f `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | n/a | 26.7 | n/a | - |
| small JDBC c1 p95 | ms | n/a | 93.6 | n/a | - |
| small JDBC c1 p99 | ms | n/a | 191.1 | n/a | - |
| small JDBC c8 p50 | ms | n/a | 71.7 | n/a | - |
| small JDBC c8 p95 | ms | n/a | 185.2 | n/a | - |
| small JDBC c8 p99 | ms | n/a | 278.1 | n/a | - |
| small JDBC c32 p50 | ms | n/a | 203.6 | n/a | - |
| small JDBC c32 p95 | ms | n/a | 794.5 | n/a | - |
| small JDBC c32 p99 | ms | n/a | 956.4 | n/a | - |
| small ADBC c1 p50 | ms | n/a | 12.9 | n/a | - |
| small ADBC c1 p95 | ms | n/a | 31.9 | n/a | - |
| small ADBC c1 p99 | ms | n/a | 41.1 | n/a | - |
| small ADBC c8 p50 | ms | n/a | 55.0 | n/a | - |
| small ADBC c8 p95 | ms | n/a | 164.3 | n/a | - |
| small ADBC c8 p99 | ms | n/a | 217.3 | n/a | - |
| small ADBC c32 p50 | ms | n/a | 170.2 | n/a | - |
| small ADBC c32 p95 | ms | n/a | 794.1 | n/a | - |
| small ADBC c32 p99 | ms | n/a | 942.5 | n/a | - |
| server RSS peak | MB | 404.0 | 1496.0 | 3.70 | 4.19 3.63 3.70 |

Correctness gate: A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-adbc8 (640/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc8 (471/640 errors; 518/640 errors; 525/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point).

### fu-tpch-local: A = 29f1267b995f `-`, B = 29f1267b995f `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 3.4 | 3.4 | 1.01 | 1.02 1.00 1.02 |
| TPC-H SF10 ADBC (sum of medians) | s | 34.4 | 33.0 | 0.96 | 0.94 0.97 0.96 |
| TPC-H SF1 JDBC (sum of medians) | s | 3.6 | 3.5 | 0.98 | 0.99 0.99 0.97 |
| TPC-H SF10 JDBC (sum of medians) | s | 34.5 | 33.0 | 0.96 | 0.95 0.97 0.96 |
| server RSS peak | MB | 1592.0 | 1831.0 | 1.15 | 1.18 1.13 1.15 |

### fu-tpch-local-vs-up-native: A = up-native `-`, B = 29f1267b995f `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | n/a | 3.4 | n/a | - |
| TPC-H SF10 ADBC (sum of medians) | s | n/a | 33.0 | n/a | - |
| TPC-H SF1 JDBC (sum of medians) | s | n/a | 3.5 | n/a | - |
| TPC-H SF10 JDBC (sum of medians) | s | n/a | 33.0 | n/a | - |
| server RSS peak | MB | 356.0 | 1831.0 | 5.14 | 5.05 5.28 4.99 |

Correctness gate: A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)), jdbc10 (md5 50bb2801381f (1/22 ok)).

### fu-zstd-netem-local: A = 29f1267b995f `CZSTD`, B = 29f1267b995f `-DresourceProfile=speed CZSTD`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 1611.0 | 1775.0 | 1.10 | 1.11 1.07 1.10 |

### fu-zstd-netem-local-vs-up-native: A = up-native `-DflightCompression=zstd`, B = 29f1267b995f `-DresourceProfile=speed CZSTD`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 607.0 | 1775.0 | 2.92 | 2.97 2.94 2.81 |
