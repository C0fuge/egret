# Wave fresh-up-37bf9401d77c (server comparison), run 42791002963

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

## Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| fu-load-local | 37bf9401d77c `-` | 37bf9401d77c `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-load-local-vs-up-native | up-native `-` | 37bf9401d77c `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-scan-local | 37bf9401d77c `-` | 37bf9401d77c `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.03 | none |
| fu-scan-local-vs-up-native | up-native `-` | 37bf9401d77c `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.02 | none |
| fu-scan-s3 | 37bf9401d77c `-` | 37bf9401d77c `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.09 | none |
| fu-scan-s3-vs-up-native | up-native `-` | 37bf9401d77c `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.08 | A: scan8 (rows=385868568 errors=2; rows=431502236 errors=1) |
| fu-sf1-s3 | 37bf9401d77c `-` | 37bf9401d77c `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C | 3/3 | n/a | n/a | n/a | n/a | 0.20 | n/a | n/a | n/a | none |
| fu-sf1-s3-vs-up-native | up-native `-` | 37bf9401d77c `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)) |
| fu-sf10adbc-s3 | 37bf9401d77c `-` | 37bf9401d77c `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | 0.14 | n/a | n/a | none |
| fu-sf10adbc-s3-vs-up-native | up-native `-` | 37bf9401d77c `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22) |
| fu-sf10jdbc-s3 | 37bf9401d77c `-` | 37bf9401d77c `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | 0.16 | n/a | none |
| fu-sf10jdbc-s3-vs-up-native | up-native `-` | 37bf9401d77c `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: jdbc10 (md5 50bb2801381f (1/22 ok)) |
| fu-small-local | 37bf9401d77c `-` | 37bf9401d77c `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | 1.32 | 0.82 | 1.14 | 0.89 | n/a | n/a | n/a | n/a | none |
| fu-small-local-vs-up-native | up-native `-` | 37bf9401d77c `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point) |
| fu-small-s3 | 37bf9401d77c `-` | 37bf9401d77c `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | 0.56 | 0.06 | 0.78 | 0.05 | n/a | n/a | n/a | n/a | none |
| fu-small-s3-vs-up-native | up-native `-` | 37bf9401d77c `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-adbc8 (640/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc8 (422/640 errors; 431/640 errors; 566/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point) |
| fu-tpch-local | 37bf9401d77c `-` | 37bf9401d77c `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 0.97 | 0.97 | 0.99 | n/a | none |
| fu-tpch-local-vs-up-native | up-native `-` | 37bf9401d77c `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)), jdbc10 (md5 50bb2801381f (1/22 ok)) |
| fu-zstd-netem-local | 37bf9401d77c `CZSTD` | 37bf9401d77c `-DresourceProfile=speed CZSTD` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-zstd-netem-local-vs-up-native | up-native `-DflightCompression=zstd` | 37bf9401d77c `-DresourceProfile=speed CZSTD` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |

## Per job (absolute medians and ratios)

### fu-load-local: A = 37bf9401d77c `-`, B = 37bf9401d77c `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 4926.0 | 936.0 | 0.19 | 0.19 0.21 0.19 |

### fu-load-local-vs-up-native: A = up-native `-`, B = 37bf9401d77c `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 945.0 | 936.0 | 0.99 | 1.02 1.00 0.97 |

### fu-scan-local: A = 37bf9401d77c `-`, B = 37bf9401d77c `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 500.9 | 517.7 | 1.03 | 1.04 1.15 1.00 |
| lineitem scan x4 | MB/s | 546.8 | 706.8 | 1.29 | 1.33 1.29 1.31 |
| lineitem scan x8 | MB/s | 474.5 | 722.1 | 1.52 | 1.53 1.49 1.52 |
| lineitem export ADBC | MB/s | 607.3 | 626.4 | 1.03 | 1.02 1.02 1.05 |
| server RSS peak | MB | 1128.0 | 1168.0 | 1.04 | 1.01 1.04 1.05 |

### fu-scan-local-vs-up-native: A = up-native `-`, B = 37bf9401d77c `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 505.8 | 517.7 | 1.02 | 1.05 1.01 1.02 |
| lineitem scan x4 | MB/s | 644.5 | 706.8 | 1.10 | 1.10 1.10 1.11 |
| lineitem scan x8 | MB/s | 655.5 | 722.1 | 1.10 | 1.12 1.08 1.11 |
| lineitem export ADBC | MB/s | 616.6 | 626.4 | 1.02 | 1.01 1.06 1.02 |
| server RSS peak | MB | 1800.0 | 1168.0 | 0.65 | 0.64 0.65 0.67 |

### fu-scan-s3: A = 37bf9401d77c `-`, B = 37bf9401d77c `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 366.3 | 399.5 | 1.09 | 1.09 1.09 1.08 |
| lineitem scan x4 | MB/s | 452.3 | 598.4 | 1.32 | 1.31 1.33 1.37 |
| lineitem scan x8 | MB/s | 422.7 | 603.6 | 1.43 | 1.43 1.40 1.46 |
| lineitem export ADBC | MB/s | 436.6 | 559.8 | 1.28 | 1.41 1.28 1.28 |
| server RSS peak | MB | 1762.0 | 3305.0 | 1.88 | 1.75 1.93 1.87 |

### fu-scan-s3-vs-up-native: A = up-native `-`, B = 37bf9401d77c `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 370.2 | 399.5 | 1.08 | 1.09 1.07 1.07 |
| lineitem scan x4 | MB/s | 586.5 | 598.4 | 1.02 | 1.01 1.04 1.02 |
| lineitem scan x8 | MB/s | n/a | 603.6 | n/a | - |
| lineitem export ADBC | MB/s | 547.7 | 559.8 | 1.02 | 1.00 1.02 1.09 |
| server RSS peak | MB | 5892.0 | 3305.0 | 0.56 | 0.56 0.56 0.56 |

Correctness gate: A: scan8 (rows=385868568 errors=2; rows=431502236 errors=1).

### fu-sf1-s3: A = 37bf9401d77c `-`, B = 37bf9401d77c `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 21.6 | 4.3 | 0.20 | 0.20 0.20 0.20 |
| TPC-H SF1 JDBC (sum of medians) | s | 21.7 | 4.3 | 0.20 | 0.20 0.20 0.20 |
| server RSS peak | MB | 769.0 | 994.0 | 1.29 | 1.23 1.33 1.27 |

### fu-sf1-s3-vs-up-native: A = up-native `-`, B = 37bf9401d77c `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | n/a | 4.3 | n/a | - |
| TPC-H SF1 JDBC (sum of medians) | s | n/a | 4.3 | n/a | - |
| server RSS peak | MB | 609.0 | 994.0 | 1.63 | 1.63 1.63 1.64 |

Correctness gate: A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)).

### fu-sf10adbc-s3: A = 37bf9401d77c `-`, B = 37bf9401d77c `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | 294.4 | 41.6 | 0.14 | 0.14 0.14 0.14 |
| server RSS peak | MB | 1667.0 | 3472.0 | 2.08 | 2.21 2.08 1.95 |

### fu-sf10adbc-s3-vs-up-native: A = up-native `-`, B = 37bf9401d77c `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | n/a | 41.6 | n/a | - |
| server RSS peak | MB | 1030.0 | 3472.0 | 3.37 | 3.53 3.30 3.38 |

Correctness gate: A: adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22).

### fu-sf10jdbc-s3: A = 37bf9401d77c `-`, B = 37bf9401d77c `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C. Workloads: `sf10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 JDBC (sum of medians) | s | 233.8 | 36.8 | 0.16 | 0.16 0.16 0.16 |
| server RSS peak | MB | 1614.0 | 3378.0 | 2.09 | 2.07 2.15 2.10 |

### fu-sf10jdbc-s3-vs-up-native: A = up-native `-`, B = 37bf9401d77c `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C. Workloads: `sf10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 JDBC (sum of medians) | s | n/a | 36.8 | n/a | - |
| server RSS peak | MB | 996.0 | 3378.0 | 3.39 | 3.31 3.48 3.40 |

Correctness gate: A: jdbc10 (md5 50bb2801381f (1/22 ok)).

### fu-small-local: A = 37bf9401d77c `-`, B = 37bf9401d77c `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 16.6 | 18.9 | 1.14 | 1.15 1.14 1.13 |
| small JDBC c1 p95 | ms | 33.7 | 34.5 | 1.02 | 1.14 1.02 1.01 |
| small JDBC c1 p99 | ms | 37.8 | 39.8 | 1.05 | 1.03 1.15 0.98 |
| small JDBC c8 p50 | ms | 85.6 | 79.6 | 0.93 | 0.93 0.93 0.93 |
| small JDBC c8 p95 | ms | 193.4 | 181.3 | 0.94 | 0.96 0.93 0.88 |
| small JDBC c8 p99 | ms | 257.5 | 223.5 | 0.87 | 0.86 0.95 0.82 |
| small JDBC c32 p50 | ms | 291.4 | 266.1 | 0.91 | 0.89 0.95 0.90 |
| small JDBC c32 p95 | ms | 857.1 | 762.3 | 0.89 | 0.87 0.91 0.87 |
| small JDBC c32 p99 | ms | 1158.7 | 896.1 | 0.77 | 0.74 0.76 0.79 |
| small ADBC c1 p50 | ms | 10.9 | 14.3 | 1.32 | 1.08 1.33 1.26 |
| small ADBC c1 p95 | ms | 31.1 | 28.8 | 0.93 | 0.92 1.14 0.87 |
| small ADBC c1 p99 | ms | 40.1 | 38.5 | 0.96 | 1.03 0.97 0.96 |
| small ADBC c8 p50 | ms | 66.4 | 67.5 | 1.02 | 0.95 1.05 1.05 |
| small ADBC c8 p95 | ms | 181.6 | 178.2 | 0.98 | 0.99 1.00 0.95 |
| small ADBC c8 p99 | ms | 231.0 | 214.2 | 0.93 | 0.94 0.98 0.84 |
| small ADBC c32 p50 | ms | 273.0 | 242.3 | 0.89 | 0.87 0.89 0.88 |
| small ADBC c32 p95 | ms | 858.8 | 706.4 | 0.82 | 0.82 0.83 0.79 |
| small ADBC c32 p99 | ms | 1277.5 | 857.3 | 0.67 | 0.66 0.67 0.65 |
| server RSS peak | MB | 1555.0 | 840.0 | 0.54 | 0.54 0.56 0.51 |

### fu-small-local-vs-up-native: A = up-native `-`, B = 37bf9401d77c `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | n/a | 18.9 | n/a | - |
| small JDBC c1 p95 | ms | n/a | 34.5 | n/a | - |
| small JDBC c1 p99 | ms | n/a | 39.8 | n/a | - |
| small JDBC c8 p50 | ms | n/a | 79.6 | n/a | - |
| small JDBC c8 p95 | ms | n/a | 181.3 | n/a | - |
| small JDBC c8 p99 | ms | n/a | 223.5 | n/a | - |
| small JDBC c32 p50 | ms | n/a | 266.1 | n/a | - |
| small JDBC c32 p95 | ms | n/a | 762.3 | n/a | - |
| small JDBC c32 p99 | ms | n/a | 896.1 | n/a | - |
| small ADBC c1 p50 | ms | n/a | 14.3 | n/a | - |
| small ADBC c1 p95 | ms | n/a | 28.8 | n/a | - |
| small ADBC c1 p99 | ms | n/a | 38.5 | n/a | - |
| small ADBC c8 p50 | ms | n/a | 67.5 | n/a | - |
| small ADBC c8 p95 | ms | n/a | 178.2 | n/a | - |
| small ADBC c8 p99 | ms | n/a | 214.2 | n/a | - |
| small ADBC c32 p50 | ms | n/a | 242.3 | n/a | - |
| small ADBC c32 p95 | ms | n/a | 706.4 | n/a | - |
| small ADBC c32 p99 | ms | n/a | 857.3 | n/a | - |
| server RSS peak | MB | 252.0 | 840.0 | 3.33 | 3.31 3.39 3.39 |

Correctness gate: A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point).

### fu-small-s3: A = 37bf9401d77c `-`, B = 37bf9401d77c `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 34.8 | 27.0 | 0.78 | 0.83 0.78 0.64 |
| small JDBC c1 p95 | ms | 866.7 | 47.7 | 0.06 | 0.05 0.06 0.05 |
| small JDBC c1 p99 | ms | 907.0 | 55.9 | 0.06 | 0.06 0.07 0.04 |
| small JDBC c8 p50 | ms | 354.6 | 76.5 | 0.22 | 0.17 0.25 0.23 |
| small JDBC c8 p95 | ms | 5832.8 | 232.7 | 0.04 | 0.04 0.04 0.04 |
| small JDBC c8 p99 | ms | 6318.1 | 2426.7 | 0.38 | 0.38 0.05 0.43 |
| small JDBC c32 p50 | ms | 1063.7 | 240.3 | 0.23 | 0.24 0.21 0.23 |
| small JDBC c32 p95 | ms | 18951.5 | 1019.7 | 0.05 | 0.06 0.06 0.05 |
| small JDBC c32 p99 | ms | 24463.3 | 1205.1 | 0.05 | 0.06 0.05 0.05 |
| small ADBC c1 p50 | ms | 26.9 | 15.1 | 0.56 | 0.54 0.64 0.51 |
| small ADBC c1 p95 | ms | 856.0 | 42.1 | 0.05 | 0.05 0.05 0.05 |
| small ADBC c1 p99 | ms | 936.2 | 56.5 | 0.06 | 0.06 0.06 0.06 |
| small ADBC c8 p50 | ms | 351.5 | 65.3 | 0.19 | 0.18 0.19 0.19 |
| small ADBC c8 p95 | ms | 5864.6 | 207.6 | 0.04 | 0.03 0.04 0.04 |
| small ADBC c8 p99 | ms | 6371.2 | 304.8 | 0.05 | 0.04 0.05 0.05 |
| small ADBC c32 p50 | ms | 1167.5 | 213.8 | 0.18 | 0.18 0.19 0.18 |
| small ADBC c32 p95 | ms | 17131.8 | 994.9 | 0.06 | 0.06 0.06 0.06 |
| small ADBC c32 p99 | ms | 20395.7 | 1152.5 | 0.06 | 0.06 0.05 0.06 |
| server RSS peak | MB | 2270.0 | 1523.0 | 0.67 | 0.68 0.66 0.69 |

### fu-small-s3-vs-up-native: A = up-native `-`, B = 37bf9401d77c `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | n/a | 27.0 | n/a | - |
| small JDBC c1 p95 | ms | n/a | 47.7 | n/a | - |
| small JDBC c1 p99 | ms | n/a | 55.9 | n/a | - |
| small JDBC c8 p50 | ms | n/a | 76.5 | n/a | - |
| small JDBC c8 p95 | ms | n/a | 232.7 | n/a | - |
| small JDBC c8 p99 | ms | n/a | 2426.7 | n/a | - |
| small JDBC c32 p50 | ms | n/a | 240.3 | n/a | - |
| small JDBC c32 p95 | ms | n/a | 1019.7 | n/a | - |
| small JDBC c32 p99 | ms | n/a | 1205.1 | n/a | - |
| small ADBC c1 p50 | ms | n/a | 15.1 | n/a | - |
| small ADBC c1 p95 | ms | n/a | 42.1 | n/a | - |
| small ADBC c1 p99 | ms | n/a | 56.5 | n/a | - |
| small ADBC c8 p50 | ms | n/a | 65.3 | n/a | - |
| small ADBC c8 p95 | ms | n/a | 207.6 | n/a | - |
| small ADBC c8 p99 | ms | n/a | 304.8 | n/a | - |
| small ADBC c32 p50 | ms | n/a | 213.8 | n/a | - |
| small ADBC c32 p95 | ms | n/a | 994.9 | n/a | - |
| small ADBC c32 p99 | ms | n/a | 1152.5 | n/a | - |
| server RSS peak | MB | 394.0 | 1523.0 | 3.87 | 3.79 4.38 3.85 |

Correctness gate: A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-adbc8 (640/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc8 (422/640 errors; 431/640 errors; 566/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point).

### fu-tpch-local: A = 37bf9401d77c `-`, B = 37bf9401d77c `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 4.3 | 4.1 | 0.97 | 1.00 0.99 0.95 |
| TPC-H SF10 ADBC (sum of medians) | s | 41.6 | 40.4 | 0.97 | 0.97 0.98 0.93 |
| TPC-H SF1 JDBC (sum of medians) | s | 4.3 | 4.2 | 0.98 | 0.98 1.01 0.96 |
| TPC-H SF10 JDBC (sum of medians) | s | 41.3 | 40.8 | 0.99 | 1.00 1.01 0.96 |
| server RSS peak | MB | 1617.0 | 1882.0 | 1.16 | 1.13 1.13 1.18 |

### fu-tpch-local-vs-up-native: A = up-native `-`, B = 37bf9401d77c `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | n/a | 4.1 | n/a | - |
| TPC-H SF10 ADBC (sum of medians) | s | n/a | 40.4 | n/a | - |
| TPC-H SF1 JDBC (sum of medians) | s | n/a | 4.2 | n/a | - |
| TPC-H SF10 JDBC (sum of medians) | s | n/a | 40.8 | n/a | - |
| server RSS peak | MB | 348.0 | 1882.0 | 5.41 | 5.05 5.41 5.50 |

Correctness gate: A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)), jdbc10 (md5 50bb2801381f (1/22 ok)).

### fu-zstd-netem-local: A = 37bf9401d77c `CZSTD`, B = 37bf9401d77c `-DresourceProfile=speed CZSTD`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 1545.0 | 1798.0 | 1.16 | 1.16 1.23 1.16 |

### fu-zstd-netem-local-vs-up-native: A = up-native `-DflightCompression=zstd`, B = 37bf9401d77c `-DresourceProfile=speed CZSTD`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 605.0 | 1798.0 | 2.97 | 3.02 3.00 2.97 |
