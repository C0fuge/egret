# Wave fresh-up-413485ba80fd (server comparison), run 41604206524

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

## Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| fu-load-local | 413485ba80fd `-` | 413485ba80fd `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-load-local-vs-up-native | up-native `-` | 413485ba80fd `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-scan-local | 413485ba80fd `-` | 413485ba80fd `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.00 | none |
| fu-scan-local-vs-up-native | up-native `-` | 413485ba80fd `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.04 | A: scan8 (rows=382067480 errors=2; rows=396288792 errors=2; rows=461279892 errors=3) |
| fu-scan-s3 | 413485ba80fd `-` | 413485ba80fd `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.00 | none |
| fu-scan-s3-vs-up-native | up-native `-` | 413485ba80fd `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.02 | A: scan8 (rows=439956380 errors=1) |
| fu-sf1-s3 | 413485ba80fd `-` | 413485ba80fd `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 0.15 | n/a | n/a | n/a | none |
| fu-sf1-s3-vs-up-native | up-native `-` | 413485ba80fd `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)) |
| fu-sf10adbc-s3 | 413485ba80fd `-` | 413485ba80fd `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | 0.19 | n/a | n/a | none |
| fu-sf10adbc-s3-vs-up-native | up-native `-` | 413485ba80fd `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22) |
| fu-sf10jdbc-s3 | 413485ba80fd `-` | 413485ba80fd `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | 0.14 | n/a | none |
| fu-sf10jdbc-s3-vs-up-native | up-native `-` | 413485ba80fd `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: jdbc10 (md5 50bb2801381f (1/22 ok)) |
| fu-small-local | 413485ba80fd `-` | 413485ba80fd `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | 1.19 | 0.89 | 1.18 | 0.88 | n/a | n/a | n/a | n/a | none |
| fu-small-local-vs-up-native | up-native `-` | 413485ba80fd `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point) |
| fu-small-s3 | 413485ba80fd `-` | 413485ba80fd `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | 0.63 | 0.06 | 0.85 | 0.06 | n/a | n/a | n/a | n/a | none |
| fu-small-s3-vs-up-native | up-native `-` | 413485ba80fd `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-adbc8 (640/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc8 (434/640 errors; 563/640 errors; 601/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point) |
| fu-tpch-local | 413485ba80fd `-` | 413485ba80fd `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 1.03 | 0.94 | 0.95 | n/a | none |
| fu-tpch-local-vs-up-native | up-native `-` | 413485ba80fd `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)), jdbc10 (md5 50bb2801381f (1/22 ok)) |
| fu-zstd-netem-local | 413485ba80fd `CZSTD` | 413485ba80fd `-DresourceProfile=speed CZSTD` | local | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-zstd-netem-local-vs-up-native | up-native `-DflightCompression=zstd` | 413485ba80fd `-DresourceProfile=speed CZSTD` | local | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |

## Per job (absolute medians and ratios)

### fu-load-local: A = 413485ba80fd `-`, B = 413485ba80fd `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 4522.0 | 905.0 | 0.20 | 0.20 0.20 0.19 |

### fu-load-local-vs-up-native: A = up-native `-`, B = 413485ba80fd `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 985.0 | 905.0 | 0.92 | 0.89 0.92 0.98 |

### fu-scan-local: A = 413485ba80fd `-`, B = 413485ba80fd `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 432.5 | 431.9 | 1.00 | 0.99 1.00 1.02 |
| lineitem scan x4 | MB/s | 436.5 | 568.2 | 1.30 | 1.25 1.30 1.30 |
| lineitem scan x8 | MB/s | 392.9 | 574.4 | 1.46 | 1.46 1.47 1.46 |
| lineitem export ADBC | MB/s | 509.6 | 512.2 | 1.01 | 1.01 1.01 1.00 |
| server RSS peak | MB | 1171.0 | 1137.0 | 0.97 | 0.97 0.92 0.99 |

### fu-scan-local-vs-up-native: A = up-native `-`, B = 413485ba80fd `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 416.9 | 431.9 | 1.04 | 1.02 1.04 1.05 |
| lineitem scan x4 | MB/s | 545.3 | 568.2 | 1.04 | 1.05 1.04 1.06 |
| lineitem scan x8 | MB/s | n/a | 574.4 | n/a | - |
| lineitem export ADBC | MB/s | 520.7 | 512.2 | 0.98 | 0.97 0.98 1.00 |
| server RSS peak | MB | 3746.0 | 1137.0 | 0.30 | 0.30 0.30 0.30 |

Correctness gate: A: scan8 (rows=382067480 errors=2; rows=396288792 errors=2; rows=461279892 errors=3).

### fu-scan-s3: A = 413485ba80fd `-`, B = 413485ba80fd `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 371.3 | 371.0 | 1.00 | 1.04 0.94 1.09 |
| lineitem scan x4 | MB/s | 434.7 | 578.2 | 1.33 | 1.33 1.31 1.33 |
| lineitem scan x8 | MB/s | 428.8 | 606.0 | 1.41 | 1.37 1.41 1.42 |
| lineitem export ADBC | MB/s | 396.6 | 500.0 | 1.26 | 1.35 1.12 1.15 |
| server RSS peak | MB | 1695.0 | 2988.0 | 1.76 | 1.80 1.75 1.76 |

### fu-scan-s3-vs-up-native: A = up-native `-`, B = 413485ba80fd `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 362.8 | 371.0 | 1.02 | 1.02 0.99 1.10 |
| lineitem scan x4 | MB/s | 578.3 | 578.2 | 1.00 | 1.00 0.95 1.04 |
| lineitem scan x8 | MB/s | n/a | 606.0 | n/a | - |
| lineitem export ADBC | MB/s | 545.5 | 500.0 | 0.92 | 0.97 0.92 0.82 |
| server RSS peak | MB | 5946.0 | 2988.0 | 0.50 | 0.50 0.52 0.50 |

Correctness gate: A: scan8 (rows=439956380 errors=1).

### fu-sf1-s3: A = 413485ba80fd `-`, B = 413485ba80fd `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 26.7 | 3.9 | 0.15 | 0.15 0.15 0.14 |
| TPC-H SF1 JDBC (sum of medians) | s | 26.7 | 4.0 | 0.15 | 0.15 0.15 0.15 |
| server RSS peak | MB | 739.0 | 971.0 | 1.31 | 1.31 1.35 1.25 |

### fu-sf1-s3-vs-up-native: A = up-native `-`, B = 413485ba80fd `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | n/a | 3.9 | n/a | - |
| TPC-H SF1 JDBC (sum of medians) | s | n/a | 4.0 | n/a | - |
| server RSS peak | MB | 612.0 | 971.0 | 1.59 | 1.59 1.50 1.64 |

Correctness gate: A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)).

### fu-sf10adbc-s3: A = 413485ba80fd `-`, B = 413485ba80fd `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | 304.4 | 57.0 | 0.19 | 0.19 0.19 0.19 |
| server RSS peak | MB | 1568.0 | 3079.0 | 1.96 | 1.98 1.86 2.02 |

### fu-sf10adbc-s3-vs-up-native: A = up-native `-`, B = 413485ba80fd `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | n/a | 57.0 | n/a | - |
| server RSS peak | MB | 1027.0 | 3079.0 | 3.00 | 2.99 2.95 3.01 |

Correctness gate: A: adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22).

### fu-sf10jdbc-s3: A = 413485ba80fd `-`, B = 413485ba80fd `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `sf10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 JDBC (sum of medians) | s | 261.1 | 37.7 | 0.14 | 0.15 0.15 0.14 |
| server RSS peak | MB | 1560.0 | 3096.0 | 1.98 | 2.06 1.89 1.93 |

### fu-sf10jdbc-s3-vs-up-native: A = up-native `-`, B = 413485ba80fd `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `sf10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 JDBC (sum of medians) | s | n/a | 37.7 | n/a | - |
| server RSS peak | MB | 1015.0 | 3096.0 | 3.05 | 3.17 3.05 2.86 |

Correctness gate: A: jdbc10 (md5 50bb2801381f (1/22 ok)).

### fu-small-local: A = 413485ba80fd `-`, B = 413485ba80fd `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 23.5 | 27.7 | 1.18 | 1.17 1.17 1.18 |
| small JDBC c1 p95 | ms | 49.7 | 50.7 | 1.02 | 1.00 1.00 1.04 |
| small JDBC c1 p99 | ms | 59.0 | 57.7 | 0.98 | 0.98 0.88 1.09 |
| small JDBC c8 p50 | ms | 120.7 | 111.8 | 0.93 | 0.95 0.94 0.93 |
| small JDBC c8 p95 | ms | 279.1 | 278.4 | 1.00 | 0.95 1.01 1.04 |
| small JDBC c8 p99 | ms | 351.5 | 367.1 | 1.04 | 0.97 1.04 1.04 |
| small JDBC c32 p50 | ms | 465.8 | 420.5 | 0.90 | 0.85 0.97 0.90 |
| small JDBC c32 p95 | ms | 1356.3 | 1187.7 | 0.88 | 0.90 0.83 0.87 |
| small JDBC c32 p99 | ms | 1925.9 | 1444.1 | 0.75 | 0.71 0.71 0.94 |
| small ADBC c1 p50 | ms | 17.1 | 20.4 | 1.19 | 1.28 1.13 1.07 |
| small ADBC c1 p95 | ms | 47.7 | 46.4 | 0.97 | 1.03 0.92 0.95 |
| small ADBC c1 p99 | ms | 57.2 | 66.3 | 1.16 | 1.17 1.17 0.85 |
| small ADBC c8 p50 | ms | 113.1 | 102.4 | 0.91 | 0.95 0.98 0.90 |
| small ADBC c8 p95 | ms | 274.5 | 290.6 | 1.06 | 1.09 1.05 1.04 |
| small ADBC c8 p99 | ms | 332.9 | 379.1 | 1.14 | 1.15 1.15 1.06 |
| small ADBC c32 p50 | ms | 445.1 | 374.1 | 0.84 | 0.84 0.86 0.88 |
| small ADBC c32 p95 | ms | 1287.2 | 1150.8 | 0.89 | 0.88 0.87 0.90 |
| small ADBC c32 p99 | ms | 1772.1 | 1324.1 | 0.75 | 0.74 0.73 0.79 |
| server RSS peak | MB | 1531.0 | 759.0 | 0.50 | 0.50 0.50 0.48 |

### fu-small-local-vs-up-native: A = up-native `-`, B = 413485ba80fd `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | n/a | 27.7 | n/a | - |
| small JDBC c1 p95 | ms | n/a | 50.7 | n/a | - |
| small JDBC c1 p99 | ms | n/a | 57.7 | n/a | - |
| small JDBC c8 p50 | ms | n/a | 111.8 | n/a | - |
| small JDBC c8 p95 | ms | n/a | 278.4 | n/a | - |
| small JDBC c8 p99 | ms | n/a | 367.1 | n/a | - |
| small JDBC c32 p50 | ms | n/a | 420.5 | n/a | - |
| small JDBC c32 p95 | ms | n/a | 1187.7 | n/a | - |
| small JDBC c32 p99 | ms | n/a | 1444.1 | n/a | - |
| small ADBC c1 p50 | ms | n/a | 20.4 | n/a | - |
| small ADBC c1 p95 | ms | n/a | 46.4 | n/a | - |
| small ADBC c1 p99 | ms | n/a | 66.3 | n/a | - |
| small ADBC c8 p50 | ms | n/a | 102.4 | n/a | - |
| small ADBC c8 p95 | ms | n/a | 290.6 | n/a | - |
| small ADBC c8 p99 | ms | n/a | 379.1 | n/a | - |
| small ADBC c32 p50 | ms | n/a | 374.1 | n/a | - |
| small ADBC c32 p95 | ms | n/a | 1150.8 | n/a | - |
| small ADBC c32 p99 | ms | n/a | 1324.1 | n/a | - |
| server RSS peak | MB | 247.0 | 759.0 | 3.07 | 3.07 3.07 2.99 |

Correctness gate: A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point).

### fu-small-s3: A = 413485ba80fd `-`, B = 413485ba80fd `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 37.1 | 31.4 | 0.85 | 0.92 0.85 0.80 |
| small JDBC c1 p95 | ms | 707.7 | 51.7 | 0.07 | 0.08 0.07 0.07 |
| small JDBC c1 p99 | ms | 780.1 | 64.3 | 0.08 | 0.08 0.07 0.09 |
| small JDBC c8 p50 | ms | 348.4 | 92.4 | 0.27 | 0.27 0.26 0.26 |
| small JDBC c8 p95 | ms | 5074.5 | 216.2 | 0.04 | 0.04 0.04 0.04 |
| small JDBC c8 p99 | ms | 5682.6 | 285.2 | 0.05 | 0.06 0.05 0.04 |
| small JDBC c32 p50 | ms | 1087.3 | 259.2 | 0.24 | 0.19 0.23 0.25 |
| small JDBC c32 p95 | ms | 18177.0 | 1107.9 | 0.06 | 0.06 0.06 0.06 |
| small JDBC c32 p99 | ms | 24924.1 | 1274.1 | 0.05 | 0.27 0.05 0.06 |
| small ADBC c1 p50 | ms | 25.9 | 16.4 | 0.63 | 0.67 0.41 0.63 |
| small ADBC c1 p95 | ms | 682.7 | 42.1 | 0.06 | 0.06 0.06 0.06 |
| small ADBC c1 p99 | ms | 746.2 | 51.3 | 0.07 | 0.07 0.04 0.07 |
| small ADBC c8 p50 | ms | 307.1 | 72.8 | 0.24 | 0.23 0.24 0.24 |
| small ADBC c8 p95 | ms | 5340.1 | 215.5 | 0.04 | 0.04 0.04 0.04 |
| small ADBC c8 p99 | ms | 5830.9 | 284.4 | 0.05 | 0.05 0.05 0.05 |
| small ADBC c32 p50 | ms | 1119.1 | 236.2 | 0.21 | 0.21 0.20 0.21 |
| small ADBC c32 p95 | ms | 17314.3 | 1026.8 | 0.06 | 0.06 0.06 0.06 |
| small ADBC c32 p99 | ms | 19373.9 | 1181.9 | 0.06 | 0.06 0.06 0.06 |
| server RSS peak | MB | 2204.0 | 1385.0 | 0.63 | 0.61 0.63 0.65 |

### fu-small-s3-vs-up-native: A = up-native `-`, B = 413485ba80fd `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | n/a | 31.4 | n/a | - |
| small JDBC c1 p95 | ms | n/a | 51.7 | n/a | - |
| small JDBC c1 p99 | ms | n/a | 64.3 | n/a | - |
| small JDBC c8 p50 | ms | n/a | 92.4 | n/a | - |
| small JDBC c8 p95 | ms | n/a | 216.2 | n/a | - |
| small JDBC c8 p99 | ms | n/a | 285.2 | n/a | - |
| small JDBC c32 p50 | ms | n/a | 259.2 | n/a | - |
| small JDBC c32 p95 | ms | n/a | 1107.9 | n/a | - |
| small JDBC c32 p99 | ms | n/a | 1274.1 | n/a | - |
| small ADBC c1 p50 | ms | n/a | 16.4 | n/a | - |
| small ADBC c1 p95 | ms | n/a | 42.1 | n/a | - |
| small ADBC c1 p99 | ms | n/a | 51.3 | n/a | - |
| small ADBC c8 p50 | ms | n/a | 72.8 | n/a | - |
| small ADBC c8 p95 | ms | n/a | 215.5 | n/a | - |
| small ADBC c8 p99 | ms | n/a | 284.4 | n/a | - |
| small ADBC c32 p50 | ms | n/a | 236.2 | n/a | - |
| small ADBC c32 p95 | ms | n/a | 1026.8 | n/a | - |
| small ADBC c32 p99 | ms | n/a | 1181.9 | n/a | - |
| server RSS peak | MB | 357.0 | 1385.0 | 3.88 | 3.53 3.90 3.90 |

Correctness gate: A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-adbc8 (640/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc8 (434/640 errors; 563/640 errors; 601/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point).

### fu-tpch-local: A = 413485ba80fd `-`, B = 413485ba80fd `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 2.7 | 2.8 | 1.03 | 1.06 1.01 1.00 |
| TPC-H SF10 ADBC (sum of medians) | s | 29.2 | 27.5 | 0.94 | 0.94 0.93 0.98 |
| TPC-H SF1 JDBC (sum of medians) | s | 2.9 | 2.9 | 1.00 | 1.01 0.99 0.95 |
| TPC-H SF10 JDBC (sum of medians) | s | 29.0 | 27.4 | 0.95 | 0.95 0.98 0.96 |
| server RSS peak | MB | 1600.0 | 1924.0 | 1.20 | 1.20 1.23 1.20 |

### fu-tpch-local-vs-up-native: A = up-native `-`, B = 413485ba80fd `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | n/a | 2.8 | n/a | - |
| TPC-H SF10 ADBC (sum of medians) | s | n/a | 27.5 | n/a | - |
| TPC-H SF1 JDBC (sum of medians) | s | n/a | 2.9 | n/a | - |
| TPC-H SF10 JDBC (sum of medians) | s | n/a | 27.4 | n/a | - |
| server RSS peak | MB | 350.0 | 1924.0 | 5.50 | 5.44 5.47 5.61 |

Correctness gate: A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)), jdbc10 (md5 50bb2801381f (1/22 ok)).

### fu-zstd-netem-local: A = 413485ba80fd `CZSTD`, B = 413485ba80fd `-DresourceProfile=speed CZSTD`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 1518.0 | 1711.0 | 1.13 | 1.06 1.13 1.14 |

### fu-zstd-netem-local-vs-up-native: A = up-native `-DflightCompression=zstd`, B = 413485ba80fd `-DresourceProfile=speed CZSTD`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 613.0 | 1711.0 | 2.79 | 2.75 2.76 2.81 |
