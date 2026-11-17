# Wave fresh-up-f4feb0d5e404 (server comparison), run 44158872708

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

## Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| fu-load-local | f4feb0d5e404 `-` | f4feb0d5e404 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-load-local-vs-up-native | up-native `-` | f4feb0d5e404 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-scan-local | f4feb0d5e404 `-` | f4feb0d5e404 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.04 | none |
| fu-scan-local-vs-up-native | up-native `-` | f4feb0d5e404 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.09 | none |
| fu-scan-s3 | f4feb0d5e404 `-` | f4feb0d5e404 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU Intel(R) Xeon(R) 6975P-C | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.12 | none |
| fu-scan-s3-vs-up-native | up-native `-` | f4feb0d5e404 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU Intel(R) Xeon(R) 6975P-C | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.12 | none |
| fu-sf1-s3 | f4feb0d5e404 `-` | f4feb0d5e404 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 0.11 | n/a | n/a | n/a | none |
| fu-sf1-s3-vs-up-native | up-native `-` | f4feb0d5e404 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)) |
| fu-sf10adbc-s3 | f4feb0d5e404 `-` | f4feb0d5e404 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | 0.12 | n/a | n/a | none |
| fu-sf10adbc-s3-vs-up-native | up-native `-` | f4feb0d5e404 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22) |
| fu-sf10jdbc-s3 | f4feb0d5e404 `-` | f4feb0d5e404 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | 0.14 | n/a | none |
| fu-sf10jdbc-s3-vs-up-native | up-native `-` | f4feb0d5e404 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: jdbc10 (md5 50bb2801381f (1/22 ok)) |
| fu-small-local | f4feb0d5e404 `-` | f4feb0d5e404 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | 1.19 | 1.00 | 1.15 | 1.01 | n/a | n/a | n/a | n/a | none |
| fu-small-local-vs-up-native | up-native `-` | f4feb0d5e404 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point) |
| fu-small-s3 | f4feb0d5e404 `-` | f4feb0d5e404 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU Intel(R) Xeon(R) 6975P-C | 3/3 | 0.66 | 0.03 | 0.89 | 0.04 | n/a | n/a | n/a | n/a | none |
| fu-small-s3-vs-up-native | up-native `-` | f4feb0d5e404 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU Intel(R) Xeon(R) 6975P-C | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-adbc8 (640/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc8 (507/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point) |
| fu-tpch-local | f4feb0d5e404 `-` | f4feb0d5e404 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU Intel(R) Xeon(R) 6975P-C | 3/3 | n/a | n/a | n/a | n/a | 1.10 | 1.00 | 1.00 | n/a | none |
| fu-tpch-local-vs-up-native | up-native `-` | f4feb0d5e404 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU Intel(R) Xeon(R) 6975P-C | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)), jdbc10 (md5 50bb2801381f (1/22 ok)) |
| fu-zstd-netem-local | f4feb0d5e404 `CZSTD` | f4feb0d5e404 `-DresourceProfile=speed CZSTD` | local | Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-zstd-netem-local-vs-up-native | up-native `-DflightCompression=zstd` | f4feb0d5e404 `-DresourceProfile=speed CZSTD` | local | Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |

## Per job (absolute medians and ratios)

### fu-load-local: A = f4feb0d5e404 `-`, B = f4feb0d5e404 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 887.0 | 885.0 | 1.00 | 1.20 0.99 0.98 |

### fu-load-local-vs-up-native: A = up-native `-`, B = f4feb0d5e404 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 988.0 | 885.0 | 0.90 | 0.94 0.89 0.90 |

### fu-scan-local: A = f4feb0d5e404 `-`, B = f4feb0d5e404 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 446.0 | 463.1 | 1.04 | 1.03 1.04 1.05 |
| lineitem scan x4 | MB/s | 547.8 | 620.4 | 1.13 | 1.16 1.12 1.14 |
| lineitem scan x8 | MB/s | 567.4 | 626.5 | 1.10 | 1.10 1.10 1.14 |
| lineitem export ADBC | MB/s | 515.0 | 551.5 | 1.07 | 1.18 1.07 1.06 |
| server RSS peak | MB | 908.0 | 1129.0 | 1.24 | 1.23 1.27 1.24 |

### fu-scan-local-vs-up-native: A = up-native `-`, B = f4feb0d5e404 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 423.2 | 463.1 | 1.09 | 1.09 1.07 1.11 |
| lineitem scan x4 | MB/s | 568.3 | 620.4 | 1.09 | 1.09 1.06 1.11 |
| lineitem scan x8 | MB/s | 586.3 | 626.5 | 1.07 | 1.07 1.07 1.07 |
| lineitem export ADBC | MB/s | 515.0 | 551.5 | 1.07 | 1.06 1.08 1.06 |
| server RSS peak | MB | 1816.0 | 1129.0 | 0.62 | 0.64 0.61 0.64 |

### fu-scan-s3: A = f4feb0d5e404 `-`, B = f4feb0d5e404 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU Intel(R) Xeon(R) 6975P-C. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 463.0 | 517.6 | 1.12 | 1.11 1.16 1.12 |
| lineitem scan x4 | MB/s | 690.9 | 870.1 | 1.26 | 1.21 1.27 1.26 |
| lineitem scan x8 | MB/s | 718.2 | 886.4 | 1.23 | 1.20 1.24 1.31 |
| lineitem export ADBC | MB/s | 550.5 | 754.3 | 1.37 | 1.27 1.42 1.37 |
| server RSS peak | MB | 1199.0 | 3306.0 | 2.76 | 2.77 2.05 2.76 |

### fu-scan-s3-vs-up-native: A = up-native `-`, B = f4feb0d5e404 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU Intel(R) Xeon(R) 6975P-C. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 461.5 | 517.6 | 1.12 | 1.16 1.09 1.09 |
| lineitem scan x4 | MB/s | 810.5 | 870.1 | 1.07 | 1.07 1.08 1.06 |
| lineitem scan x8 | MB/s | 809.6 | 886.4 | 1.09 | 1.07 1.10 1.09 |
| lineitem export ADBC | MB/s | 641.0 | 754.3 | 1.18 | 1.13 1.18 1.18 |
| server RSS peak | MB | 4206.0 | 3306.0 | 0.79 | 0.81 0.78 0.77 |

### fu-sf1-s3: A = f4feb0d5e404 `-`, B = f4feb0d5e404 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 30.1 | 3.3 | 0.11 | 0.11 0.10 0.14 |
| TPC-H SF1 JDBC (sum of medians) | s | 28.8 | 3.4 | 0.12 | 0.12 0.07 0.14 |
| server RSS peak | MB | 734.0 | 974.0 | 1.33 | 1.41 1.33 1.23 |

### fu-sf1-s3-vs-up-native: A = up-native `-`, B = f4feb0d5e404 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | n/a | 3.3 | n/a | - |
| TPC-H SF1 JDBC (sum of medians) | s | n/a | 3.4 | n/a | - |
| server RSS peak | MB | 593.0 | 974.0 | 1.64 | 1.75 1.76 1.61 |

Correctness gate: A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)).

### fu-sf10adbc-s3: A = f4feb0d5e404 `-`, B = f4feb0d5e404 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | 266.3 | 32.3 | 0.12 | 0.12 0.12 0.11 |
| server RSS peak | MB | 1591.0 | 3436.0 | 2.16 | 2.16 2.19 1.71 |

### fu-sf10adbc-s3-vs-up-native: A = up-native `-`, B = f4feb0d5e404 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | n/a | 32.3 | n/a | - |
| server RSS peak | MB | 1039.0 | 3436.0 | 3.31 | 3.32 3.28 3.34 |

Correctness gate: A: adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22).

### fu-sf10jdbc-s3: A = f4feb0d5e404 `-`, B = f4feb0d5e404 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 JDBC (sum of medians) | s | 273.9 | 38.2 | 0.14 | 0.14 0.14 0.14 |
| server RSS peak | MB | 1475.0 | 3358.0 | 2.28 | 2.16 2.29 2.28 |

### fu-sf10jdbc-s3-vs-up-native: A = up-native `-`, B = f4feb0d5e404 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 JDBC (sum of medians) | s | n/a | 38.2 | n/a | - |
| server RSS peak | MB | 1016.0 | 3358.0 | 3.31 | 3.25 3.34 3.29 |

Correctness gate: A: jdbc10 (md5 50bb2801381f (1/22 ok)).

### fu-small-local: A = f4feb0d5e404 `-`, B = f4feb0d5e404 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 16.3 | 18.8 | 1.15 | 1.00 1.15 1.13 |
| small JDBC c1 p95 | ms | 32.7 | 34.5 | 1.05 | 0.98 1.08 1.08 |
| small JDBC c1 p99 | ms | 36.4 | 41.0 | 1.13 | 1.01 1.14 1.07 |
| small JDBC c8 p50 | ms | 55.5 | 74.5 | 1.34 | 1.24 1.34 1.39 |
| small JDBC c8 p95 | ms | 192.7 | 188.3 | 0.98 | 0.91 0.99 0.92 |
| small JDBC c8 p99 | ms | 228.7 | 227.9 | 1.00 | 0.95 1.04 0.98 |
| small JDBC c32 p50 | ms | 183.1 | 271.2 | 1.48 | 1.40 1.55 1.39 |
| small JDBC c32 p95 | ms | 741.4 | 747.0 | 1.01 | 0.95 1.01 0.99 |
| small JDBC c32 p99 | ms | 883.8 | 864.1 | 0.98 | 1.02 0.98 0.95 |
| small ADBC c1 p50 | ms | 11.2 | 13.3 | 1.19 | 1.06 1.21 1.10 |
| small ADBC c1 p95 | ms | 31.0 | 31.8 | 1.03 | 1.04 1.10 0.97 |
| small ADBC c1 p99 | ms | 35.7 | 41.6 | 1.17 | 0.93 1.19 1.21 |
| small ADBC c8 p50 | ms | 45.3 | 70.3 | 1.55 | 1.48 1.55 1.55 |
| small ADBC c8 p95 | ms | 186.8 | 182.3 | 0.98 | 0.95 1.01 0.96 |
| small ADBC c8 p99 | ms | 218.7 | 217.3 | 0.99 | 0.93 1.07 1.01 |
| small ADBC c32 p50 | ms | 164.5 | 255.2 | 1.55 | 1.50 1.64 1.51 |
| small ADBC c32 p95 | ms | 740.2 | 740.6 | 1.00 | 0.94 1.00 0.96 |
| small ADBC c32 p99 | ms | 835.8 | 855.5 | 1.02 | 0.96 1.04 0.98 |
| server RSS peak | MB | 711.0 | 796.0 | 1.12 | 1.15 1.09 1.14 |

### fu-small-local-vs-up-native: A = up-native `-`, B = f4feb0d5e404 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | n/a | 18.8 | n/a | - |
| small JDBC c1 p95 | ms | n/a | 34.5 | n/a | - |
| small JDBC c1 p99 | ms | n/a | 41.0 | n/a | - |
| small JDBC c8 p50 | ms | n/a | 74.5 | n/a | - |
| small JDBC c8 p95 | ms | n/a | 188.3 | n/a | - |
| small JDBC c8 p99 | ms | n/a | 227.9 | n/a | - |
| small JDBC c32 p50 | ms | n/a | 271.2 | n/a | - |
| small JDBC c32 p95 | ms | n/a | 747.0 | n/a | - |
| small JDBC c32 p99 | ms | n/a | 864.1 | n/a | - |
| small ADBC c1 p50 | ms | n/a | 13.3 | n/a | - |
| small ADBC c1 p95 | ms | n/a | 31.8 | n/a | - |
| small ADBC c1 p99 | ms | n/a | 41.6 | n/a | - |
| small ADBC c8 p50 | ms | n/a | 70.3 | n/a | - |
| small ADBC c8 p95 | ms | n/a | 182.3 | n/a | - |
| small ADBC c8 p99 | ms | n/a | 217.3 | n/a | - |
| small ADBC c32 p50 | ms | n/a | 255.2 | n/a | - |
| small ADBC c32 p95 | ms | n/a | 740.6 | n/a | - |
| small ADBC c32 p99 | ms | n/a | 855.5 | n/a | - |
| server RSS peak | MB | 252.0 | 796.0 | 3.16 | 3.12 3.12 3.29 |

Correctness gate: A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point).

### fu-small-s3: A = f4feb0d5e404 `-`, B = f4feb0d5e404 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU Intel(R) Xeon(R) 6975P-C. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 21.5 | 19.1 | 0.89 | 0.95 0.87 0.81 |
| small JDBC c1 p95 | ms | 602.8 | 30.6 | 0.05 | 0.05 0.05 0.06 |
| small JDBC c1 p99 | ms | 641.4 | 40.1 | 0.06 | 0.06 0.06 0.07 |
| small JDBC c8 p50 | ms | 100.7 | 57.2 | 0.57 | 0.57 0.54 0.57 |
| small JDBC c8 p95 | ms | 3806.5 | 119.1 | 0.03 | 0.03 0.03 0.03 |
| small JDBC c8 p99 | ms | 4163.4 | 147.7 | 0.04 | 0.04 0.03 0.04 |
| small JDBC c32 p50 | ms | 336.6 | 156.2 | 0.46 | 0.49 0.45 0.46 |
| small JDBC c32 p95 | ms | 13323.6 | 515.8 | 0.04 | 0.04 0.04 0.04 |
| small JDBC c32 p99 | ms | 14469.7 | 628.5 | 0.04 | 0.04 0.04 0.04 |
| small ADBC c1 p50 | ms | 14.5 | 9.6 | 0.66 | 0.73 0.60 0.59 |
| small ADBC c1 p95 | ms | 613.7 | 21.4 | 0.03 | 0.04 0.03 0.04 |
| small ADBC c1 p99 | ms | 663.7 | 23.9 | 0.04 | 0.04 0.04 0.04 |
| small ADBC c8 p50 | ms | 98.5 | 41.1 | 0.42 | 0.43 0.42 0.39 |
| small ADBC c8 p95 | ms | 3822.0 | 106.5 | 0.03 | 0.03 0.03 0.03 |
| small ADBC c8 p99 | ms | 4155.9 | 131.8 | 0.03 | 0.03 0.03 0.03 |
| small ADBC c32 p50 | ms | 346.7 | 126.4 | 0.36 | 0.38 0.36 0.34 |
| small ADBC c32 p95 | ms | 13836.8 | 451.6 | 0.03 | 0.03 0.03 0.03 |
| small ADBC c32 p99 | ms | 16345.1 | 539.3 | 0.03 | 0.03 0.03 0.03 |
| server RSS peak | MB | 793.0 | 1534.0 | 1.93 | 1.94 1.93 1.91 |

### fu-small-s3-vs-up-native: A = up-native `-`, B = f4feb0d5e404 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU Intel(R) Xeon(R) 6975P-C. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | n/a | 19.1 | n/a | - |
| small JDBC c1 p95 | ms | n/a | 30.6 | n/a | - |
| small JDBC c1 p99 | ms | n/a | 40.1 | n/a | - |
| small JDBC c8 p50 | ms | n/a | 57.2 | n/a | - |
| small JDBC c8 p95 | ms | n/a | 119.1 | n/a | - |
| small JDBC c8 p99 | ms | n/a | 147.7 | n/a | - |
| small JDBC c32 p50 | ms | n/a | 156.2 | n/a | - |
| small JDBC c32 p95 | ms | n/a | 515.8 | n/a | - |
| small JDBC c32 p99 | ms | n/a | 628.5 | n/a | - |
| small ADBC c1 p50 | ms | n/a | 9.6 | n/a | - |
| small ADBC c1 p95 | ms | n/a | 21.4 | n/a | - |
| small ADBC c1 p99 | ms | n/a | 23.9 | n/a | - |
| small ADBC c8 p50 | ms | n/a | 41.1 | n/a | - |
| small ADBC c8 p95 | ms | n/a | 106.5 | n/a | - |
| small ADBC c8 p99 | ms | n/a | 131.8 | n/a | - |
| small ADBC c32 p50 | ms | n/a | 126.4 | n/a | - |
| small ADBC c32 p95 | ms | n/a | 451.6 | n/a | - |
| small ADBC c32 p99 | ms | n/a | 539.3 | n/a | - |
| server RSS peak | MB | 396.0 | 1534.0 | 3.87 | 3.73 3.83 3.87 |

Correctness gate: A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-adbc8 (640/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc8 (507/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point).

### fu-tpch-local: A = f4feb0d5e404 `-`, B = f4feb0d5e404 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU Intel(R) Xeon(R) 6975P-C. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 2.3 | 2.5 | 1.10 | 1.11 1.11 1.10 |
| TPC-H SF10 ADBC (sum of medians) | s | 23.2 | 23.1 | 1.00 | 0.98 1.00 1.00 |
| TPC-H SF1 JDBC (sum of medians) | s | 2.5 | 2.6 | 1.08 | 1.09 1.07 1.08 |
| TPC-H SF10 JDBC (sum of medians) | s | 23.0 | 23.0 | 1.00 | 0.97 0.99 1.01 |
| server RSS peak | MB | 1717.0 | 1934.0 | 1.13 | 1.11 1.17 1.11 |

### fu-tpch-local-vs-up-native: A = up-native `-`, B = f4feb0d5e404 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU Intel(R) Xeon(R) 6975P-C. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | n/a | 2.5 | n/a | - |
| TPC-H SF10 ADBC (sum of medians) | s | n/a | 23.1 | n/a | - |
| TPC-H SF1 JDBC (sum of medians) | s | n/a | 2.6 | n/a | - |
| TPC-H SF10 JDBC (sum of medians) | s | n/a | 23.0 | n/a | - |
| server RSS peak | MB | 353.0 | 1934.0 | 5.48 | 5.48 5.51 5.33 |

Correctness gate: A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)), jdbc10 (md5 50bb2801381f (1/22 ok)).

### fu-zstd-netem-local: A = f4feb0d5e404 `CZSTD`, B = f4feb0d5e404 `-DresourceProfile=speed CZSTD`, local

Runner: Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C. Workloads: `netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 1448.0 | 1685.0 | 1.16 | 1.19 1.16 1.11 |

### fu-zstd-netem-local-vs-up-native: A = up-native `-DflightCompression=zstd`, B = f4feb0d5e404 `-DresourceProfile=speed CZSTD`, local

Runner: Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C. Workloads: `netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 617.0 | 1685.0 | 2.73 | 2.85 2.63 2.73 |
