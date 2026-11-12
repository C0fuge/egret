# Wave fresh-up-2c169a53db3b (server comparison), run 43175544843

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

## Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| fu-load-local | 2c169a53db3b `-` | 2c169a53db3b `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-load-local-vs-up-native | up-native `-` | 2c169a53db3b `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-scan-local | 2c169a53db3b `-` | 2c169a53db3b `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.01 | none |
| fu-scan-local-vs-up-native | up-native `-` | 2c169a53db3b `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.05 | A: scan8 (rows=376759064 errors=2; rows=387703576 errors=2; rows=427942680 errors=2) |
| fu-scan-s3 | 2c169a53db3b `-` | 2c169a53db3b `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.06 | none |
| fu-scan-s3-vs-up-native | up-native `-` | 2c169a53db3b `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.12 | A: scan8 (rows=430388124 errors=1; rows=430650268 errors=1) |
| fu-sf1-s3 | 2c169a53db3b `-` | 2c169a53db3b `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU Intel(R) Xeon(R) 6973P-C | 3/3 | n/a | n/a | n/a | n/a | 0.14 | n/a | n/a | n/a | none |
| fu-sf1-s3-vs-up-native | up-native `-` | 2c169a53db3b `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU Intel(R) Xeon(R) 6973P-C | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)) |
| fu-sf10adbc-s3 | 2c169a53db3b `-` | 2c169a53db3b `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | 0.13 | n/a | n/a | none |
| fu-sf10adbc-s3-vs-up-native | up-native `-` | 2c169a53db3b `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22) |
| fu-sf10jdbc-s3 | 2c169a53db3b `-` | 2c169a53db3b `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | 0.16 | n/a | none |
| fu-sf10jdbc-s3-vs-up-native | up-native `-` | 2c169a53db3b `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: jdbc10 (md5 50bb2801381f (1/22 ok)) |
| fu-small-local | 2c169a53db3b `-` | 2c169a53db3b `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | 1.14 | 0.87 | 1.09 | 0.84 | n/a | n/a | n/a | n/a | none |
| fu-small-local-vs-up-native | up-native `-` | 2c169a53db3b `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point) |
| fu-small-s3 | 2c169a53db3b `-` | 2c169a53db3b `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | 0.47 | 0.05 | 0.81 | 0.05 | n/a | n/a | n/a | n/a | none |
| fu-small-s3-vs-up-native | up-native `-` | 2c169a53db3b `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-adbc8 (640/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc8 (346/640 errors; 430/640 errors; 483/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point) |
| fu-tpch-local | 2c169a53db3b `-` | 2c169a53db3b `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 1.01 | 0.99 | 0.99 | n/a | none |
| fu-tpch-local-vs-up-native | up-native `-` | 2c169a53db3b `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)), jdbc10 (md5 50bb2801381f (1/22 ok)) |
| fu-zstd-netem-local | 2c169a53db3b `CZSTD` | 2c169a53db3b `-DresourceProfile=speed CZSTD` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-zstd-netem-local-vs-up-native | up-native `-DflightCompression=zstd` | 2c169a53db3b `-DresourceProfile=speed CZSTD` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |

## Per job (absolute medians and ratios)

### fu-load-local: A = 2c169a53db3b `-`, B = 2c169a53db3b `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 4557.0 | 902.0 | 0.20 | 0.20 0.19 0.20 |

### fu-load-local-vs-up-native: A = up-native `-`, B = 2c169a53db3b `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 929.0 | 902.0 | 0.97 | 0.91 0.93 1.04 |

### fu-scan-local: A = 2c169a53db3b `-`, B = 2c169a53db3b `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 550.6 | 555.5 | 1.01 | 1.00 1.03 1.01 |
| lineitem scan x4 | MB/s | 565.1 | 720.3 | 1.27 | 1.27 1.26 1.33 |
| lineitem scan x8 | MB/s | 485.0 | 734.8 | 1.52 | 1.54 1.51 1.51 |
| lineitem export ADBC | MB/s | 639.1 | 647.7 | 1.01 | 1.01 1.02 1.02 |
| server RSS peak | MB | 1208.0 | 1150.0 | 0.95 | 0.85 1.00 0.95 |

### fu-scan-local-vs-up-native: A = up-native `-`, B = 2c169a53db3b `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 527.9 | 555.5 | 1.05 | 1.04 1.06 1.05 |
| lineitem scan x4 | MB/s | 680.5 | 720.3 | 1.06 | 1.07 1.05 1.04 |
| lineitem scan x8 | MB/s | n/a | 734.8 | n/a | - |
| lineitem export ADBC | MB/s | 652.9 | 647.7 | 0.99 | 0.98 0.99 1.01 |
| server RSS peak | MB | 3731.0 | 1150.0 | 0.31 | 0.31 0.31 0.31 |

Correctness gate: A: scan8 (rows=376759064 errors=2; rows=387703576 errors=2; rows=427942680 errors=2).

### fu-scan-s3: A = 2c169a53db3b `-`, B = 2c169a53db3b `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 383.4 | 404.6 | 1.06 | 0.93 1.06 1.10 |
| lineitem scan x4 | MB/s | 512.9 | 736.2 | 1.44 | 1.44 1.39 1.64 |
| lineitem scan x8 | MB/s | 472.6 | 740.1 | 1.57 | 1.55 1.57 1.59 |
| lineitem export ADBC | MB/s | 360.4 | 669.4 | 1.86 | 1.69 1.85 2.02 |
| server RSS peak | MB | 1717.0 | 3326.0 | 1.94 | 1.96 1.92 1.93 |

### fu-scan-s3-vs-up-native: A = up-native `-`, B = 2c169a53db3b `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 360.6 | 404.6 | 1.12 | 0.83 1.17 1.21 |
| lineitem scan x4 | MB/s | 678.1 | 736.2 | 1.09 | 1.09 1.03 1.12 |
| lineitem scan x8 | MB/s | n/a | 740.1 | n/a | - |
| lineitem export ADBC | MB/s | 654.5 | 669.4 | 1.02 | 1.03 1.14 1.01 |
| server RSS peak | MB | 5907.0 | 3326.0 | 0.56 | 0.56 0.54 0.57 |

Correctness gate: A: scan8 (rows=430388124 errors=1; rows=430650268 errors=1).

### fu-sf1-s3: A = 2c169a53db3b `-`, B = 2c169a53db3b `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU Intel(R) Xeon(R) 6973P-C. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 25.1 | 3.6 | 0.14 | 0.15 0.14 0.14 |
| TPC-H SF1 JDBC (sum of medians) | s | 24.7 | 3.7 | 0.15 | 0.15 0.15 0.15 |
| server RSS peak | MB | 771.0 | 984.0 | 1.28 | 1.38 1.29 1.22 |

### fu-sf1-s3-vs-up-native: A = up-native `-`, B = 2c169a53db3b `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU Intel(R) Xeon(R) 6973P-C. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | n/a | 3.6 | n/a | - |
| TPC-H SF1 JDBC (sum of medians) | s | n/a | 3.7 | n/a | - |
| server RSS peak | MB | 597.0 | 984.0 | 1.65 | 1.79 1.62 1.63 |

Correctness gate: A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)).

### fu-sf10adbc-s3: A = 2c169a53db3b `-`, B = 2c169a53db3b `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | 288.7 | 37.8 | 0.13 | 0.13 0.16 0.13 |
| server RSS peak | MB | 1654.0 | 3404.0 | 2.06 | 2.04 2.14 2.12 |

### fu-sf10adbc-s3-vs-up-native: A = up-native `-`, B = 2c169a53db3b `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | n/a | 37.8 | n/a | - |
| server RSS peak | MB | 1031.0 | 3404.0 | 3.30 | 3.23 3.30 3.41 |

Correctness gate: A: adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22).

### fu-sf10jdbc-s3: A = 2c169a53db3b `-`, B = 2c169a53db3b `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz. Workloads: `sf10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 JDBC (sum of medians) | s | 284.6 | 45.3 | 0.16 | 0.16 0.16 0.16 |
| server RSS peak | MB | 1595.0 | 3451.0 | 2.16 | 2.20 2.04 2.18 |

### fu-sf10jdbc-s3-vs-up-native: A = up-native `-`, B = 2c169a53db3b `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz. Workloads: `sf10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 JDBC (sum of medians) | s | n/a | 45.3 | n/a | - |
| server RSS peak | MB | 1040.0 | 3451.0 | 3.32 | 3.42 3.25 3.32 |

Correctness gate: A: jdbc10 (md5 50bb2801381f (1/22 ok)).

### fu-small-local: A = 2c169a53db3b `-`, B = 2c169a53db3b `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 15.6 | 17.0 | 1.09 | 1.19 1.09 1.13 |
| small JDBC c1 p95 | ms | 31.0 | 30.9 | 1.00 | 1.07 0.99 1.00 |
| small JDBC c1 p99 | ms | 36.5 | 35.1 | 0.96 | 1.02 1.01 0.96 |
| small JDBC c8 p50 | ms | 73.7 | 68.2 | 0.93 | 0.99 0.89 0.95 |
| small JDBC c8 p95 | ms | 186.1 | 173.6 | 0.93 | 0.93 0.93 0.93 |
| small JDBC c8 p99 | ms | 247.4 | 210.1 | 0.85 | 0.88 0.84 0.88 |
| small JDBC c32 p50 | ms | 279.8 | 257.3 | 0.92 | 0.85 0.96 0.89 |
| small JDBC c32 p95 | ms | 839.9 | 708.5 | 0.84 | 0.83 0.84 0.84 |
| small JDBC c32 p99 | ms | 1098.2 | 857.9 | 0.78 | 0.69 0.88 0.72 |
| small ADBC c1 p50 | ms | 10.8 | 12.3 | 1.14 | 1.26 1.14 1.13 |
| small ADBC c1 p95 | ms | 32.8 | 31.4 | 0.96 | 1.00 0.92 1.03 |
| small ADBC c1 p99 | ms | 42.1 | 37.8 | 0.90 | 1.01 0.88 1.08 |
| small ADBC c8 p50 | ms | 62.1 | 63.7 | 1.03 | 0.99 0.99 1.04 |
| small ADBC c8 p95 | ms | 179.2 | 170.8 | 0.95 | 0.93 0.93 0.97 |
| small ADBC c8 p99 | ms | 241.8 | 217.4 | 0.90 | 0.91 0.89 0.88 |
| small ADBC c32 p50 | ms | 271.0 | 242.1 | 0.89 | 0.93 0.94 0.84 |
| small ADBC c32 p95 | ms | 794.9 | 695.0 | 0.87 | 0.83 0.90 0.86 |
| small ADBC c32 p99 | ms | 1031.3 | 825.2 | 0.80 | 0.67 0.80 0.83 |
| server RSS peak | MB | 1505.0 | 837.0 | 0.56 | 0.51 0.56 0.57 |

### fu-small-local-vs-up-native: A = up-native `-`, B = 2c169a53db3b `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | n/a | 17.0 | n/a | - |
| small JDBC c1 p95 | ms | n/a | 30.9 | n/a | - |
| small JDBC c1 p99 | ms | n/a | 35.1 | n/a | - |
| small JDBC c8 p50 | ms | n/a | 68.2 | n/a | - |
| small JDBC c8 p95 | ms | n/a | 173.6 | n/a | - |
| small JDBC c8 p99 | ms | n/a | 210.1 | n/a | - |
| small JDBC c32 p50 | ms | n/a | 257.3 | n/a | - |
| small JDBC c32 p95 | ms | n/a | 708.5 | n/a | - |
| small JDBC c32 p99 | ms | n/a | 857.9 | n/a | - |
| small ADBC c1 p50 | ms | n/a | 12.3 | n/a | - |
| small ADBC c1 p95 | ms | n/a | 31.4 | n/a | - |
| small ADBC c1 p99 | ms | n/a | 37.8 | n/a | - |
| small ADBC c8 p50 | ms | n/a | 63.7 | n/a | - |
| small ADBC c8 p95 | ms | n/a | 170.8 | n/a | - |
| small ADBC c8 p99 | ms | n/a | 217.4 | n/a | - |
| small ADBC c32 p50 | ms | n/a | 242.1 | n/a | - |
| small ADBC c32 p95 | ms | n/a | 695.0 | n/a | - |
| small ADBC c32 p99 | ms | n/a | 825.2 | n/a | - |
| server RSS peak | MB | 251.0 | 837.0 | 3.33 | 3.19 3.30 3.39 |

Correctness gate: A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point).

### fu-small-s3: A = 2c169a53db3b `-`, B = 2c169a53db3b `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 28.0 | 22.8 | 0.81 | 0.83 0.78 0.81 |
| small JDBC c1 p95 | ms | 692.2 | 42.5 | 0.06 | 0.06 0.06 0.06 |
| small JDBC c1 p99 | ms | 782.0 | 52.3 | 0.07 | 0.07 0.06 0.07 |
| small JDBC c8 p50 | ms | 268.2 | 63.3 | 0.24 | 0.24 0.23 0.26 |
| small JDBC c8 p95 | ms | 3755.2 | 141.1 | 0.04 | 0.04 0.04 0.03 |
| small JDBC c8 p99 | ms | 4038.8 | 182.7 | 0.05 | 0.05 0.05 0.04 |
| small JDBC c32 p50 | ms | 953.9 | 177.2 | 0.19 | 0.19 0.19 0.19 |
| small JDBC c32 p95 | ms | 13161.0 | 661.6 | 0.05 | 0.05 0.05 0.05 |
| small JDBC c32 p99 | ms | 15031.9 | 769.3 | 0.05 | 0.05 0.02 0.05 |
| small ADBC c1 p50 | ms | 20.8 | 9.9 | 0.47 | 0.58 0.46 0.42 |
| small ADBC c1 p95 | ms | 705.5 | 28.2 | 0.04 | 0.04 0.04 0.04 |
| small ADBC c1 p99 | ms | 747.8 | 34.4 | 0.05 | 0.04 0.05 0.05 |
| small ADBC c8 p50 | ms | 250.7 | 50.8 | 0.20 | 0.21 0.19 0.18 |
| small ADBC c8 p95 | ms | 3805.2 | 130.9 | 0.03 | 0.03 0.04 0.03 |
| small ADBC c8 p99 | ms | 4142.9 | 161.8 | 0.04 | 0.04 0.04 0.04 |
| small ADBC c32 p50 | ms | 1007.1 | 156.6 | 0.16 | 0.17 0.15 0.18 |
| small ADBC c32 p95 | ms | 12801.8 | 628.7 | 0.05 | 0.05 0.05 0.04 |
| small ADBC c32 p99 | ms | 15087.8 | 759.1 | 0.05 | 0.05 0.05 0.04 |
| server RSS peak | MB | 2307.0 | 1523.0 | 0.66 | 0.65 0.66 0.66 |

### fu-small-s3-vs-up-native: A = up-native `-`, B = 2c169a53db3b `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | n/a | 22.8 | n/a | - |
| small JDBC c1 p95 | ms | n/a | 42.5 | n/a | - |
| small JDBC c1 p99 | ms | n/a | 52.3 | n/a | - |
| small JDBC c8 p50 | ms | n/a | 63.3 | n/a | - |
| small JDBC c8 p95 | ms | n/a | 141.1 | n/a | - |
| small JDBC c8 p99 | ms | n/a | 182.7 | n/a | - |
| small JDBC c32 p50 | ms | n/a | 177.2 | n/a | - |
| small JDBC c32 p95 | ms | n/a | 661.6 | n/a | - |
| small JDBC c32 p99 | ms | n/a | 769.3 | n/a | - |
| small ADBC c1 p50 | ms | n/a | 9.9 | n/a | - |
| small ADBC c1 p95 | ms | n/a | 28.2 | n/a | - |
| small ADBC c1 p99 | ms | n/a | 34.4 | n/a | - |
| small ADBC c8 p50 | ms | n/a | 50.8 | n/a | - |
| small ADBC c8 p95 | ms | n/a | 130.9 | n/a | - |
| small ADBC c8 p99 | ms | n/a | 161.8 | n/a | - |
| small ADBC c32 p50 | ms | n/a | 156.6 | n/a | - |
| small ADBC c32 p95 | ms | n/a | 628.7 | n/a | - |
| small ADBC c32 p99 | ms | n/a | 759.1 | n/a | - |
| server RSS peak | MB | 396.0 | 1523.0 | 3.85 | 3.79 4.02 3.84 |

Correctness gate: A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-adbc8 (640/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc8 (346/640 errors; 430/640 errors; 483/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point).

### fu-tpch-local: A = 2c169a53db3b `-`, B = 2c169a53db3b `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 3.4 | 3.4 | 1.01 | 1.01 0.97 1.04 |
| TPC-H SF10 ADBC (sum of medians) | s | 34.6 | 34.2 | 0.99 | 0.99 0.97 0.99 |
| TPC-H SF1 JDBC (sum of medians) | s | 3.5 | 3.4 | 0.97 | 1.01 0.95 0.97 |
| TPC-H SF10 JDBC (sum of medians) | s | 34.8 | 34.3 | 0.99 | 1.03 0.98 0.97 |
| server RSS peak | MB | 1624.0 | 1827.0 | 1.12 | 1.12 1.09 1.18 |

### fu-tpch-local-vs-up-native: A = up-native `-`, B = 2c169a53db3b `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | n/a | 3.4 | n/a | - |
| TPC-H SF10 ADBC (sum of medians) | s | n/a | 34.2 | n/a | - |
| TPC-H SF1 JDBC (sum of medians) | s | n/a | 3.4 | n/a | - |
| TPC-H SF10 JDBC (sum of medians) | s | n/a | 34.3 | n/a | - |
| server RSS peak | MB | 368.0 | 1827.0 | 4.96 | 4.96 5.06 5.09 |

Correctness gate: A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)), jdbc10 (md5 50bb2801381f (1/22 ok)).

### fu-zstd-netem-local: A = 2c169a53db3b `CZSTD`, B = 2c169a53db3b `-DresourceProfile=speed CZSTD`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 1532.0 | 1730.0 | 1.13 | 1.14 1.13 1.09 |

### fu-zstd-netem-local-vs-up-native: A = up-native `-DflightCompression=zstd`, B = 2c169a53db3b `-DresourceProfile=speed CZSTD`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 602.0 | 1730.0 | 2.87 | 2.85 2.99 2.77 |
