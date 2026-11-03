# Wave fresh-up-25aa7eec0f0f (server comparison), run 41584018828

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

## Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| fu-load-local | 25aa7eec0f0f `-` | 25aa7eec0f0f `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-load-local-vs-up-native | up-native `-` | 25aa7eec0f0f `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-scan-local | 25aa7eec0f0f `-` | 25aa7eec0f0f `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.01 | none |
| fu-scan-local-vs-up-native | up-native `-` | 25aa7eec0f0f `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.05 | none |
| fu-scan-s3 | 25aa7eec0f0f `-` | 25aa7eec0f0f `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.02 | none |
| fu-scan-s3-vs-up-native | up-native `-` | 25aa7eec0f0f `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.02 | none |
| fu-sf1-s3 | 25aa7eec0f0f `-` | 25aa7eec0f0f `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 0.16 | n/a | n/a | n/a | none |
| fu-sf1-s3-vs-up-native | up-native `-` | 25aa7eec0f0f `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)) |
| fu-sf10adbc-s3 | 25aa7eec0f0f `-` | 25aa7eec0f0f `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | 0.19 | n/a | n/a | none |
| fu-sf10adbc-s3-vs-up-native | up-native `-` | 25aa7eec0f0f `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22) |
| fu-sf10jdbc-s3 | 25aa7eec0f0f `-` | 25aa7eec0f0f `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | 0.18 | n/a | none |
| fu-sf10jdbc-s3-vs-up-native | up-native `-` | 25aa7eec0f0f `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: jdbc10 (md5 50bb2801381f (1/22 ok)) |
| fu-small-local | 25aa7eec0f0f `-` | 25aa7eec0f0f `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C | 3/3 | 1.01 | 0.94 | 0.96 | 0.89 | n/a | n/a | n/a | n/a | none |
| fu-small-local-vs-up-native | up-native `-` | 25aa7eec0f0f `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point) |
| fu-small-s3 | 25aa7eec0f0f `-` | 25aa7eec0f0f `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | 0.50 | 0.06 | 0.77 | 0.06 | n/a | n/a | n/a | n/a | none |
| fu-small-s3-vs-up-native | up-native `-` | 25aa7eec0f0f `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-adbc8 (640/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc8 (519/640 errors; 523/640 errors; 547/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point) |
| fu-tpch-local | 25aa7eec0f0f `-` | 25aa7eec0f0f `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 1.02 | 0.96 | 0.97 | n/a | none |
| fu-tpch-local-vs-up-native | up-native `-` | 25aa7eec0f0f `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)), jdbc10 (md5 50bb2801381f (1/22 ok)) |
| fu-zstd-netem-local | 25aa7eec0f0f `CZSTD` | 25aa7eec0f0f `-DresourceProfile=speed CZSTD` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-zstd-netem-local-vs-up-native | up-native `-DflightCompression=zstd` | 25aa7eec0f0f `-DresourceProfile=speed CZSTD` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |

## Per job (absolute medians and ratios)

### fu-load-local: A = 25aa7eec0f0f `-`, B = 25aa7eec0f0f `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 4664.0 | 874.0 | 0.19 | 0.17 0.19 0.24 |

### fu-load-local-vs-up-native: A = up-native `-`, B = 25aa7eec0f0f `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 945.0 | 874.0 | 0.92 | 0.84 0.97 1.19 |

### fu-scan-local: A = 25aa7eec0f0f `-`, B = 25aa7eec0f0f `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 455.4 | 461.1 | 1.01 | 1.00 1.04 1.01 |
| lineitem scan x4 | MB/s | 475.3 | 510.8 | 1.07 | 1.07 1.14 1.06 |
| lineitem scan x8 | MB/s | 424.0 | 531.4 | 1.25 | 1.27 1.25 1.25 |
| lineitem export ADBC | MB/s | 527.4 | 556.7 | 1.06 | 1.21 1.06 1.02 |
| server RSS peak | MB | 1135.0 | 1123.0 | 0.99 | 0.97 1.02 0.98 |

### fu-scan-local-vs-up-native: A = up-native `-`, B = 25aa7eec0f0f `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 439.1 | 461.1 | 1.05 | 1.03 1.09 1.05 |
| lineitem scan x4 | MB/s | 579.6 | 510.8 | 0.88 | 0.88 0.90 0.90 |
| lineitem scan x8 | MB/s | 603.4 | 531.4 | 0.88 | 0.88 0.88 0.88 |
| lineitem export ADBC | MB/s | 561.5 | 556.7 | 0.99 | 1.00 0.99 0.98 |
| server RSS peak | MB | 3610.0 | 1123.0 | 0.31 | 0.33 0.31 0.31 |

### fu-scan-s3: A = 25aa7eec0f0f `-`, B = 25aa7eec0f0f `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 386.4 | 393.5 | 1.02 | 1.02 1.01 1.13 |
| lineitem scan x4 | MB/s | 447.3 | 524.6 | 1.17 | 1.15 1.14 1.18 |
| lineitem scan x8 | MB/s | 434.4 | 545.4 | 1.26 | 1.25 1.27 1.26 |
| lineitem export ADBC | MB/s | 409.4 | 489.7 | 1.20 | 1.18 1.09 1.28 |
| server RSS peak | MB | 1685.0 | 3215.0 | 1.91 | 1.92 1.98 1.74 |

### fu-scan-s3-vs-up-native: A = up-native `-`, B = 25aa7eec0f0f `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 385.5 | 393.5 | 1.02 | 1.02 1.17 1.02 |
| lineitem scan x4 | MB/s | 604.6 | 524.6 | 0.87 | 0.87 0.84 0.87 |
| lineitem scan x8 | MB/s | 613.5 | 545.4 | 0.89 | 0.90 0.88 0.89 |
| lineitem export ADBC | MB/s | 561.5 | 489.7 | 0.87 | 0.86 0.89 0.87 |
| server RSS peak | MB | 5832.0 | 3215.0 | 0.55 | 0.55 0.60 0.48 |

### fu-sf1-s3: A = 25aa7eec0f0f `-`, B = 25aa7eec0f0f `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 26.3 | 4.2 | 0.16 | 0.16 0.16 0.15 |
| TPC-H SF1 JDBC (sum of medians) | s | 26.5 | 4.3 | 0.16 | 0.16 0.16 0.16 |
| server RSS peak | MB | 724.0 | 916.0 | 1.27 | 1.28 1.24 1.28 |

### fu-sf1-s3-vs-up-native: A = up-native `-`, B = 25aa7eec0f0f `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | n/a | 4.2 | n/a | - |
| TPC-H SF1 JDBC (sum of medians) | s | n/a | 4.3 | n/a | - |
| server RSS peak | MB | 630.0 | 916.0 | 1.45 | 1.48 1.56 1.45 |

Correctness gate: A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)).

### fu-sf10adbc-s3: A = 25aa7eec0f0f `-`, B = 25aa7eec0f0f `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | 305.2 | 59.5 | 0.19 | 0.18 0.19 0.20 |
| server RSS peak | MB | 1578.0 | 3054.0 | 1.94 | 1.97 1.94 1.93 |

### fu-sf10adbc-s3-vs-up-native: A = up-native `-`, B = 25aa7eec0f0f `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | n/a | 59.5 | n/a | - |
| server RSS peak | MB | 984.0 | 3054.0 | 3.10 | 3.02 3.13 3.10 |

Correctness gate: A: adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22).

### fu-sf10jdbc-s3: A = 25aa7eec0f0f `-`, B = 25aa7eec0f0f `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 JDBC (sum of medians) | s | 306.5 | 54.2 | 0.18 | 0.17 0.18 0.18 |
| server RSS peak | MB | 1548.0 | 3047.0 | 1.97 | 2.10 1.98 1.91 |

### fu-sf10jdbc-s3-vs-up-native: A = up-native `-`, B = 25aa7eec0f0f `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 JDBC (sum of medians) | s | n/a | 54.2 | n/a | - |
| server RSS peak | MB | 1003.0 | 3047.0 | 3.04 | 3.15 3.02 3.13 |

Correctness gate: A: jdbc10 (md5 50bb2801381f (1/22 ok)).

### fu-small-local: A = 25aa7eec0f0f `-`, B = 25aa7eec0f0f `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 22.6 | 21.7 | 0.96 | 1.00 0.96 0.99 |
| small JDBC c1 p95 | ms | 47.3 | 45.5 | 0.96 | 1.01 0.98 0.93 |
| small JDBC c1 p99 | ms | 56.2 | 52.0 | 0.93 | 1.19 0.84 1.00 |
| small JDBC c8 p50 | ms | 113.2 | 82.8 | 0.73 | 0.74 0.73 0.73 |
| small JDBC c8 p95 | ms | 262.0 | 244.9 | 0.93 | 0.93 0.94 0.93 |
| small JDBC c8 p99 | ms | 343.5 | 313.6 | 0.91 | 0.99 0.84 0.96 |
| small JDBC c32 p50 | ms | 429.3 | 259.4 | 0.60 | 0.61 0.54 0.63 |
| small JDBC c32 p95 | ms | 1185.3 | 1055.7 | 0.89 | 0.88 0.89 0.90 |
| small JDBC c32 p99 | ms | 1602.3 | 1228.3 | 0.77 | 0.77 0.74 0.79 |
| small ADBC c1 p50 | ms | 15.5 | 15.7 | 1.01 | 0.96 0.90 1.08 |
| small ADBC c1 p95 | ms | 43.2 | 42.7 | 0.99 | 0.85 1.12 0.99 |
| small ADBC c1 p99 | ms | 55.5 | 50.1 | 0.90 | 0.90 1.05 0.79 |
| small ADBC c8 p50 | ms | 97.2 | 71.9 | 0.74 | 0.71 0.74 0.76 |
| small ADBC c8 p95 | ms | 273.4 | 267.5 | 0.98 | 1.06 0.97 0.92 |
| small ADBC c8 p99 | ms | 371.8 | 348.0 | 0.94 | 1.16 0.94 0.86 |
| small ADBC c32 p50 | ms | 419.7 | 251.0 | 0.60 | 0.61 0.58 0.62 |
| small ADBC c32 p95 | ms | 1129.6 | 1061.6 | 0.94 | 0.91 0.97 0.95 |
| small ADBC c32 p99 | ms | 1466.4 | 1295.8 | 0.88 | 0.82 0.95 0.88 |
| server RSS peak | MB | 1477.0 | 729.0 | 0.49 | 0.50 0.49 0.49 |

### fu-small-local-vs-up-native: A = up-native `-`, B = 25aa7eec0f0f `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | n/a | 21.7 | n/a | - |
| small JDBC c1 p95 | ms | n/a | 45.5 | n/a | - |
| small JDBC c1 p99 | ms | n/a | 52.0 | n/a | - |
| small JDBC c8 p50 | ms | n/a | 82.8 | n/a | - |
| small JDBC c8 p95 | ms | n/a | 244.9 | n/a | - |
| small JDBC c8 p99 | ms | n/a | 313.6 | n/a | - |
| small JDBC c32 p50 | ms | n/a | 259.4 | n/a | - |
| small JDBC c32 p95 | ms | n/a | 1055.7 | n/a | - |
| small JDBC c32 p99 | ms | n/a | 1228.3 | n/a | - |
| small ADBC c1 p50 | ms | n/a | 15.7 | n/a | - |
| small ADBC c1 p95 | ms | n/a | 42.7 | n/a | - |
| small ADBC c1 p99 | ms | n/a | 50.1 | n/a | - |
| small ADBC c8 p50 | ms | n/a | 71.9 | n/a | - |
| small ADBC c8 p95 | ms | n/a | 267.5 | n/a | - |
| small ADBC c8 p99 | ms | n/a | 348.0 | n/a | - |
| small ADBC c32 p50 | ms | n/a | 251.0 | n/a | - |
| small ADBC c32 p95 | ms | n/a | 1061.6 | n/a | - |
| small ADBC c32 p99 | ms | n/a | 1295.8 | n/a | - |
| server RSS peak | MB | 253.0 | 729.0 | 2.88 | 2.88 2.89 2.85 |

Correctness gate: A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point).

### fu-small-s3: A = 25aa7eec0f0f `-`, B = 25aa7eec0f0f `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 28.5 | 21.8 | 0.77 | 0.76 0.77 0.78 |
| small JDBC c1 p95 | ms | 693.9 | 42.9 | 0.06 | 0.06 0.06 0.07 |
| small JDBC c1 p99 | ms | 733.8 | 54.2 | 0.07 | 0.07 0.05 0.08 |
| small JDBC c8 p50 | ms | 268.3 | 61.1 | 0.23 | 0.23 0.23 0.23 |
| small JDBC c8 p95 | ms | 3647.9 | 161.2 | 0.04 | 0.04 0.04 0.04 |
| small JDBC c8 p99 | ms | 3957.4 | 190.5 | 0.05 | 0.05 0.05 0.03 |
| small JDBC c32 p50 | ms | 967.0 | 165.4 | 0.17 | 0.16 0.19 0.17 |
| small JDBC c32 p95 | ms | 12693.7 | 800.3 | 0.06 | 0.06 0.06 0.06 |
| small JDBC c32 p99 | ms | 14387.9 | 923.6 | 0.06 | 0.06 0.04 0.06 |
| small ADBC c1 p50 | ms | 21.4 | 10.6 | 0.50 | 0.47 0.48 0.51 |
| small ADBC c1 p95 | ms | 685.6 | 30.9 | 0.05 | 0.05 0.05 0.05 |
| small ADBC c1 p99 | ms | 733.5 | 39.7 | 0.05 | 0.05 0.06 0.05 |
| small ADBC c8 p50 | ms | 266.4 | 48.0 | 0.18 | 0.17 0.19 0.19 |
| small ADBC c8 p95 | ms | 3695.7 | 151.9 | 0.04 | 0.04 0.04 0.04 |
| small ADBC c8 p99 | ms | 4043.8 | 193.4 | 0.05 | 0.05 0.04 0.05 |
| small ADBC c32 p50 | ms | 956.3 | 145.0 | 0.15 | 0.15 0.16 0.15 |
| small ADBC c32 p95 | ms | 13292.8 | 772.9 | 0.06 | 0.06 0.06 0.06 |
| small ADBC c32 p99 | ms | 14444.6 | 894.7 | 0.06 | 0.06 0.06 0.03 |
| server RSS peak | MB | 2226.0 | 1351.0 | 0.61 | 0.62 0.57 0.62 |

### fu-small-s3-vs-up-native: A = up-native `-`, B = 25aa7eec0f0f `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | n/a | 21.8 | n/a | - |
| small JDBC c1 p95 | ms | n/a | 42.9 | n/a | - |
| small JDBC c1 p99 | ms | n/a | 54.2 | n/a | - |
| small JDBC c8 p50 | ms | n/a | 61.1 | n/a | - |
| small JDBC c8 p95 | ms | n/a | 161.2 | n/a | - |
| small JDBC c8 p99 | ms | n/a | 190.5 | n/a | - |
| small JDBC c32 p50 | ms | n/a | 165.4 | n/a | - |
| small JDBC c32 p95 | ms | n/a | 800.3 | n/a | - |
| small JDBC c32 p99 | ms | n/a | 923.6 | n/a | - |
| small ADBC c1 p50 | ms | n/a | 10.6 | n/a | - |
| small ADBC c1 p95 | ms | n/a | 30.9 | n/a | - |
| small ADBC c1 p99 | ms | n/a | 39.7 | n/a | - |
| small ADBC c8 p50 | ms | n/a | 48.0 | n/a | - |
| small ADBC c8 p95 | ms | n/a | 151.9 | n/a | - |
| small ADBC c8 p99 | ms | n/a | 193.4 | n/a | - |
| small ADBC c32 p50 | ms | n/a | 145.0 | n/a | - |
| small ADBC c32 p95 | ms | n/a | 772.9 | n/a | - |
| small ADBC c32 p99 | ms | n/a | 894.7 | n/a | - |
| server RSS peak | MB | 383.0 | 1351.0 | 3.53 | 3.60 3.45 3.50 |

Correctness gate: A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-adbc8 (640/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc8 (519/640 errors; 523/640 errors; 547/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point).

### fu-tpch-local: A = 25aa7eec0f0f `-`, B = 25aa7eec0f0f `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 3.2 | 3.2 | 1.02 | 1.02 1.04 0.99 |
| TPC-H SF10 ADBC (sum of medians) | s | 34.2 | 32.9 | 0.96 | 0.97 0.99 0.95 |
| TPC-H SF1 JDBC (sum of medians) | s | 3.3 | 3.4 | 1.01 | 1.01 1.01 0.96 |
| TPC-H SF10 JDBC (sum of medians) | s | 34.1 | 33.2 | 0.97 | 0.96 0.97 0.97 |
| server RSS peak | MB | 1530.0 | 1823.0 | 1.19 | 1.21 1.12 1.17 |

### fu-tpch-local-vs-up-native: A = up-native `-`, B = 25aa7eec0f0f `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | n/a | 3.2 | n/a | - |
| TPC-H SF10 ADBC (sum of medians) | s | n/a | 32.9 | n/a | - |
| TPC-H SF1 JDBC (sum of medians) | s | n/a | 3.4 | n/a | - |
| TPC-H SF10 JDBC (sum of medians) | s | n/a | 33.2 | n/a | - |
| server RSS peak | MB | 354.0 | 1823.0 | 5.15 | 5.23 4.83 5.18 |

Correctness gate: A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)), jdbc10 (md5 50bb2801381f (1/22 ok)).

### fu-zstd-netem-local: A = 25aa7eec0f0f `CZSTD`, B = 25aa7eec0f0f `-DresourceProfile=speed CZSTD`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 1617.0 | 1742.0 | 1.08 | 1.15 1.11 0.99 |

### fu-zstd-netem-local-vs-up-native: A = up-native `-DflightCompression=zstd`, B = 25aa7eec0f0f `-DresourceProfile=speed CZSTD`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 596.0 | 1742.0 | 2.92 | 2.86 3.01 2.71 |
