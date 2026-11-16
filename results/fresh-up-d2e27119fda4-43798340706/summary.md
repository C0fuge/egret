# Wave fresh-up-d2e27119fda4 (server comparison), run 43798340706

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

## Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| fu-load-local | d2e27119fda4 `-` | d2e27119fda4 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-load-local-vs-up-native | up-native `-` | d2e27119fda4 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-scan-local | d2e27119fda4 `-` | d2e27119fda4 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 0.98 | none |
| fu-scan-local-vs-up-native | up-native `-` | d2e27119fda4 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.08 | A: scan8 (rows=380822296 errors=2; rows=435106716 errors=1) |
| fu-scan-s3 | d2e27119fda4 `-` | d2e27119fda4 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.03 | none |
| fu-scan-s3-vs-up-native | up-native `-` | d2e27119fda4 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.08 | A: scan8 (rows=391635736 errors=2) |
| fu-sf1-s3 | d2e27119fda4 `-` | d2e27119fda4 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 0.16 | n/a | n/a | n/a | none |
| fu-sf1-s3-vs-up-native | up-native `-` | d2e27119fda4 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)) |
| fu-sf10adbc-s3 | d2e27119fda4 `-` | d2e27119fda4 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | 0.14 | n/a | n/a | none |
| fu-sf10adbc-s3-vs-up-native | up-native `-` | d2e27119fda4 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22) |
| fu-sf10jdbc-s3 | d2e27119fda4 `-` | d2e27119fda4 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | 0.13 | n/a | none |
| fu-sf10jdbc-s3-vs-up-native | up-native `-` | d2e27119fda4 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: jdbc10 (md5 50bb2801381f (1/22 ok)) |
| fu-small-local | d2e27119fda4 `-` | d2e27119fda4 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | 1.15 | 0.86 | 1.12 | 0.85 | n/a | n/a | n/a | n/a | none |
| fu-small-local-vs-up-native | up-native `-` | d2e27119fda4 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point) |
| fu-small-s3 | d2e27119fda4 `-` | d2e27119fda4 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | 0.49 | 0.06 | 0.63 | 0.06 | n/a | n/a | n/a | n/a | none |
| fu-small-s3-vs-up-native | up-native `-` | d2e27119fda4 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-adbc8 (640/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc8 (326/640 errors; 485/640 errors; 572/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point) |
| fu-tpch-local | d2e27119fda4 `-` | d2e27119fda4 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 1.02 | 0.96 | 0.98 | n/a | none |
| fu-tpch-local-vs-up-native | up-native `-` | d2e27119fda4 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)), jdbc10 (md5 50bb2801381f (1/22 ok)) |
| fu-zstd-netem-local | d2e27119fda4 `CZSTD` | d2e27119fda4 `-DresourceProfile=speed CZSTD` | local | Linux ubuntu26 4 vCPU Intel(R) Xeon(R) 6973P-C | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-zstd-netem-local-vs-up-native | up-native `-DflightCompression=zstd` | d2e27119fda4 `-DresourceProfile=speed CZSTD` | local | Linux ubuntu26 4 vCPU Intel(R) Xeon(R) 6973P-C | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |

## Per job (absolute medians and ratios)

### fu-load-local: A = d2e27119fda4 `-`, B = d2e27119fda4 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 4915.0 | 866.0 | 0.18 | 0.18 0.17 0.18 |

### fu-load-local-vs-up-native: A = up-native `-`, B = d2e27119fda4 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 975.0 | 866.0 | 0.89 | 0.85 0.88 0.89 |

### fu-scan-local: A = d2e27119fda4 `-`, B = d2e27119fda4 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 712.9 | 697.1 | 0.98 | 0.96 0.97 0.98 |
| lineitem scan x4 | MB/s | 744.5 | 902.3 | 1.21 | 1.21 1.21 1.22 |
| lineitem scan x8 | MB/s | 642.6 | 915.2 | 1.42 | 1.39 1.40 1.47 |
| lineitem export ADBC | MB/s | 832.3 | 835.2 | 1.00 | 1.02 1.00 1.00 |
| server RSS peak | MB | 1230.0 | 1157.0 | 0.94 | 0.83 0.94 0.93 |

### fu-scan-local-vs-up-native: A = up-native `-`, B = d2e27119fda4 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 643.3 | 697.1 | 1.08 | 1.04 1.08 1.03 |
| lineitem scan x4 | MB/s | 845.7 | 902.3 | 1.07 | 1.10 1.05 1.08 |
| lineitem scan x8 | MB/s | n/a | 915.2 | n/a | - |
| lineitem export ADBC | MB/s | 818.6 | 835.2 | 1.02 | 0.98 1.04 0.98 |
| server RSS peak | MB | 3714.0 | 1157.0 | 0.31 | 0.32 0.30 0.31 |

Correctness gate: A: scan8 (rows=380822296 errors=2; rows=435106716 errors=1).

### fu-scan-s3: A = d2e27119fda4 `-`, B = d2e27119fda4 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 558.1 | 577.0 | 1.03 | 1.03 1.05 1.03 |
| lineitem scan x4 | MB/s | 655.1 | 913.4 | 1.39 | 1.35 1.41 1.52 |
| lineitem scan x8 | MB/s | 617.0 | 929.3 | 1.51 | 1.43 1.51 1.57 |
| lineitem export ADBC | MB/s | 666.0 | 857.1 | 1.29 | 1.28 1.29 1.24 |
| server RSS peak | MB | 1779.0 | 3316.0 | 1.86 | 1.93 1.87 1.86 |

### fu-scan-s3-vs-up-native: A = up-native `-`, B = d2e27119fda4 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 535.7 | 577.0 | 1.08 | 1.02 1.19 1.05 |
| lineitem scan x4 | MB/s | 837.2 | 913.4 | 1.09 | 1.02 1.10 1.05 |
| lineitem scan x8 | MB/s | n/a | 929.3 | n/a | - |
| lineitem export ADBC | MB/s | 828.4 | 857.1 | 1.03 | 1.03 1.03 1.03 |
| server RSS peak | MB | 5926.0 | 3316.0 | 0.56 | 0.58 0.56 0.56 |

Correctness gate: A: scan8 (rows=391635736 errors=2).

### fu-sf1-s3: A = d2e27119fda4 `-`, B = d2e27119fda4 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 26.5 | 4.2 | 0.16 | 0.16 0.16 0.15 |
| TPC-H SF1 JDBC (sum of medians) | s | 26.4 | 4.2 | 0.16 | 0.16 0.16 0.15 |
| server RSS peak | MB | 755.0 | 995.0 | 1.32 | 1.29 1.40 1.28 |

### fu-sf1-s3-vs-up-native: A = up-native `-`, B = d2e27119fda4 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | n/a | 4.2 | n/a | - |
| TPC-H SF1 JDBC (sum of medians) | s | n/a | 4.2 | n/a | - |
| server RSS peak | MB | 582.0 | 995.0 | 1.71 | 1.71 1.81 1.68 |

Correctness gate: A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)).

### fu-sf10adbc-s3: A = d2e27119fda4 `-`, B = d2e27119fda4 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | 276.2 | 39.8 | 0.14 | 0.14 0.15 0.14 |
| server RSS peak | MB | 1666.0 | 3380.0 | 2.03 | 2.10 2.07 2.01 |

### fu-sf10adbc-s3-vs-up-native: A = up-native `-`, B = d2e27119fda4 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | n/a | 39.8 | n/a | - |
| server RSS peak | MB | 1007.0 | 3380.0 | 3.36 | 3.47 3.39 3.27 |

Correctness gate: A: adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22).

### fu-sf10jdbc-s3: A = d2e27119fda4 `-`, B = d2e27119fda4 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 JDBC (sum of medians) | s | 300.5 | 38.5 | 0.13 | 0.13 0.13 0.15 |
| server RSS peak | MB | 1618.0 | 3375.0 | 2.09 | 2.12 2.05 2.09 |

### fu-sf10jdbc-s3-vs-up-native: A = up-native `-`, B = d2e27119fda4 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 JDBC (sum of medians) | s | n/a | 38.5 | n/a | - |
| server RSS peak | MB | 1023.0 | 3375.0 | 3.30 | 3.38 3.29 3.20 |

Correctness gate: A: jdbc10 (md5 50bb2801381f (1/22 ok)).

### fu-small-local: A = d2e27119fda4 `-`, B = d2e27119fda4 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 14.9 | 16.7 | 1.12 | 1.15 1.07 1.14 |
| small JDBC c1 p95 | ms | 30.2 | 30.7 | 1.02 | 0.88 1.02 1.05 |
| small JDBC c1 p99 | ms | 37.1 | 33.4 | 0.90 | 0.79 0.99 0.95 |
| small JDBC c8 p50 | ms | 69.2 | 69.3 | 1.00 | 1.00 0.86 1.02 |
| small JDBC c8 p95 | ms | 185.4 | 169.9 | 0.92 | 0.92 0.97 0.88 |
| small JDBC c8 p99 | ms | 239.7 | 208.5 | 0.87 | 0.84 0.91 0.87 |
| small JDBC c32 p50 | ms | 269.6 | 252.5 | 0.94 | 0.88 0.94 0.98 |
| small JDBC c32 p95 | ms | 808.3 | 687.0 | 0.85 | 0.80 0.83 0.94 |
| small JDBC c32 p99 | ms | 1118.0 | 876.2 | 0.78 | 0.70 0.75 0.78 |
| small ADBC c1 p50 | ms | 10.6 | 12.2 | 1.15 | 1.13 1.15 1.27 |
| small ADBC c1 p95 | ms | 31.1 | 30.0 | 0.96 | 1.00 0.86 0.98 |
| small ADBC c1 p99 | ms | 39.1 | 35.2 | 0.90 | 1.04 0.84 0.99 |
| small ADBC c8 p50 | ms | 61.8 | 62.4 | 1.01 | 1.01 1.05 1.02 |
| small ADBC c8 p95 | ms | 170.3 | 167.8 | 0.99 | 0.99 0.84 1.02 |
| small ADBC c8 p99 | ms | 224.1 | 212.7 | 0.95 | 0.99 0.84 0.95 |
| small ADBC c32 p50 | ms | 259.4 | 225.1 | 0.87 | 0.87 0.85 1.00 |
| small ADBC c32 p95 | ms | 781.4 | 673.5 | 0.86 | 0.87 0.86 0.92 |
| small ADBC c32 p99 | ms | 1027.1 | 771.3 | 0.75 | 0.77 0.75 0.82 |
| server RSS peak | MB | 1503.0 | 831.0 | 0.55 | 0.56 0.55 0.53 |

### fu-small-local-vs-up-native: A = up-native `-`, B = d2e27119fda4 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | n/a | 16.7 | n/a | - |
| small JDBC c1 p95 | ms | n/a | 30.7 | n/a | - |
| small JDBC c1 p99 | ms | n/a | 33.4 | n/a | - |
| small JDBC c8 p50 | ms | n/a | 69.3 | n/a | - |
| small JDBC c8 p95 | ms | n/a | 169.9 | n/a | - |
| small JDBC c8 p99 | ms | n/a | 208.5 | n/a | - |
| small JDBC c32 p50 | ms | n/a | 252.5 | n/a | - |
| small JDBC c32 p95 | ms | n/a | 687.0 | n/a | - |
| small JDBC c32 p99 | ms | n/a | 876.2 | n/a | - |
| small ADBC c1 p50 | ms | n/a | 12.2 | n/a | - |
| small ADBC c1 p95 | ms | n/a | 30.0 | n/a | - |
| small ADBC c1 p99 | ms | n/a | 35.2 | n/a | - |
| small ADBC c8 p50 | ms | n/a | 62.4 | n/a | - |
| small ADBC c8 p95 | ms | n/a | 167.8 | n/a | - |
| small ADBC c8 p99 | ms | n/a | 212.7 | n/a | - |
| small ADBC c32 p50 | ms | n/a | 225.1 | n/a | - |
| small ADBC c32 p95 | ms | n/a | 673.5 | n/a | - |
| small ADBC c32 p99 | ms | n/a | 771.3 | n/a | - |
| server RSS peak | MB | 253.0 | 831.0 | 3.28 | 3.42 3.28 3.17 |

Correctness gate: A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point).

### fu-small-s3: A = d2e27119fda4 `-`, B = d2e27119fda4 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 40.9 | 25.8 | 0.63 | 0.76 0.70 0.63 |
| small JDBC c1 p95 | ms | 712.0 | 66.1 | 0.09 | 0.08 0.09 0.10 |
| small JDBC c1 p99 | ms | 1022.1 | 164.6 | 0.16 | 0.07 0.17 0.09 |
| small JDBC c8 p50 | ms | 259.1 | 68.2 | 0.26 | 0.25 0.27 0.30 |
| small JDBC c8 p95 | ms | 3660.4 | 178.6 | 0.05 | 0.04 0.06 0.05 |
| small JDBC c8 p99 | ms | 6572.6 | 235.8 | 0.04 | 0.04 0.03 0.06 |
| small JDBC c32 p50 | ms | 978.7 | 197.9 | 0.20 | 0.20 0.22 0.22 |
| small JDBC c32 p95 | ms | 12685.5 | 778.8 | 0.06 | 0.06 0.06 0.06 |
| small JDBC c32 p99 | ms | 14132.5 | 909.6 | 0.06 | 0.06 0.07 0.06 |
| small ADBC c1 p50 | ms | 25.4 | 12.5 | 0.49 | 0.48 0.50 0.49 |
| small ADBC c1 p95 | ms | 595.7 | 34.5 | 0.06 | 0.06 0.04 0.06 |
| small ADBC c1 p99 | ms | 1197.1 | 43.9 | 0.04 | 0.06 0.04 0.03 |
| small ADBC c8 p50 | ms | 256.4 | 53.3 | 0.21 | 0.21 0.24 0.20 |
| small ADBC c8 p95 | ms | 3603.7 | 164.6 | 0.05 | 0.05 0.04 0.04 |
| small ADBC c8 p99 | ms | 3977.9 | 205.3 | 0.05 | 0.06 0.04 0.05 |
| small ADBC c32 p50 | ms | 945.3 | 170.0 | 0.18 | 0.18 0.20 0.18 |
| small ADBC c32 p95 | ms | 12351.1 | 781.2 | 0.06 | 0.06 0.06 0.06 |
| small ADBC c32 p99 | ms | 14192.3 | 927.3 | 0.07 | 0.06 0.05 0.07 |
| server RSS peak | MB | 2259.0 | 1522.0 | 0.67 | 0.68 0.68 0.67 |

### fu-small-s3-vs-up-native: A = up-native `-`, B = d2e27119fda4 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | n/a | 25.8 | n/a | - |
| small JDBC c1 p95 | ms | n/a | 66.1 | n/a | - |
| small JDBC c1 p99 | ms | n/a | 164.6 | n/a | - |
| small JDBC c8 p50 | ms | n/a | 68.2 | n/a | - |
| small JDBC c8 p95 | ms | n/a | 178.6 | n/a | - |
| small JDBC c8 p99 | ms | n/a | 235.8 | n/a | - |
| small JDBC c32 p50 | ms | n/a | 197.9 | n/a | - |
| small JDBC c32 p95 | ms | n/a | 778.8 | n/a | - |
| small JDBC c32 p99 | ms | n/a | 909.6 | n/a | - |
| small ADBC c1 p50 | ms | n/a | 12.5 | n/a | - |
| small ADBC c1 p95 | ms | n/a | 34.5 | n/a | - |
| small ADBC c1 p99 | ms | n/a | 43.9 | n/a | - |
| small ADBC c8 p50 | ms | n/a | 53.3 | n/a | - |
| small ADBC c8 p95 | ms | n/a | 164.6 | n/a | - |
| small ADBC c8 p99 | ms | n/a | 205.3 | n/a | - |
| small ADBC c32 p50 | ms | n/a | 170.0 | n/a | - |
| small ADBC c32 p95 | ms | n/a | 781.2 | n/a | - |
| small ADBC c32 p99 | ms | n/a | 927.3 | n/a | - |
| server RSS peak | MB | 390.0 | 1522.0 | 3.90 | 3.95 3.72 3.90 |

Correctness gate: A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-adbc8 (640/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc8 (326/640 errors; 485/640 errors; 572/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point).

### fu-tpch-local: A = d2e27119fda4 `-`, B = d2e27119fda4 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 2.4 | 2.4 | 1.02 | 1.03 1.02 1.03 |
| TPC-H SF10 ADBC (sum of medians) | s | 25.3 | 24.4 | 0.96 | 0.96 0.97 0.97 |
| TPC-H SF1 JDBC (sum of medians) | s | 2.6 | 2.5 | 0.98 | 0.98 0.98 1.00 |
| TPC-H SF10 JDBC (sum of medians) | s | 24.5 | 23.9 | 0.98 | 0.98 0.98 0.97 |
| server RSS peak | MB | 1617.0 | 1818.0 | 1.12 | 1.11 1.14 1.14 |

### fu-tpch-local-vs-up-native: A = up-native `-`, B = d2e27119fda4 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | n/a | 2.4 | n/a | - |
| TPC-H SF10 ADBC (sum of medians) | s | n/a | 24.4 | n/a | - |
| TPC-H SF1 JDBC (sum of medians) | s | n/a | 2.5 | n/a | - |
| TPC-H SF10 JDBC (sum of medians) | s | n/a | 23.9 | n/a | - |
| server RSS peak | MB | 361.0 | 1818.0 | 5.04 | 5.15 4.99 5.04 |

Correctness gate: A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)), jdbc10 (md5 50bb2801381f (1/22 ok)).

### fu-zstd-netem-local: A = d2e27119fda4 `CZSTD`, B = d2e27119fda4 `-DresourceProfile=speed CZSTD`, local

Runner: Linux ubuntu26 4 vCPU Intel(R) Xeon(R) 6973P-C. Workloads: `netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 1554.0 | 1638.0 | 1.05 | 1.17 1.05 1.05 |

### fu-zstd-netem-local-vs-up-native: A = up-native `-DflightCompression=zstd`, B = d2e27119fda4 `-DresourceProfile=speed CZSTD`, local

Runner: Linux ubuntu26 4 vCPU Intel(R) Xeon(R) 6973P-C. Workloads: `netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 610.0 | 1638.0 | 2.69 | 2.82 2.68 2.70 |
