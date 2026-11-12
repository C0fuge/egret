# Wave fresh-up-74464701e372 (server comparison), run 43148390757

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

## Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| fu-load-local | 74464701e372 `-` | 74464701e372 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-load-local-vs-up-native | up-native `-` | 74464701e372 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-scan-local | 74464701e372 `-` | 74464701e372 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.01 | none |
| fu-scan-local-vs-up-native | up-native `-` | 74464701e372 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.04 | A: scan8 (rows=342069908 errors=3; rows=381412120 errors=2; rows=383443736 errors=2) |
| fu-scan-s3 | 74464701e372 `-` | 74464701e372 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.07 | none |
| fu-scan-s3-vs-up-native | up-native `-` | 74464701e372 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.06 | A: scan8 (rows=272581136 errors=4; rows=336695956 errors=3; rows=378528536 errors=2) |
| fu-sf1-s3 | 74464701e372 `-` | 74464701e372 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz | 3/3 | n/a | n/a | n/a | n/a | 0.18 | n/a | n/a | n/a | none |
| fu-sf1-s3-vs-up-native | up-native `-` | 74464701e372 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)) |
| fu-sf10adbc-s3 | 74464701e372 `-` | 74464701e372 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | 0.12 | n/a | n/a | none |
| fu-sf10adbc-s3-vs-up-native | up-native `-` | 74464701e372 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22) |
| fu-sf10jdbc-s3 | 74464701e372 `-` | 74464701e372 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | 0.09 | n/a | none |
| fu-sf10jdbc-s3-vs-up-native | up-native `-` | 74464701e372 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: jdbc10 (md5 50bb2801381f (1/22 ok)) |
| fu-small-local | 74464701e372 `-` | 74464701e372 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C | 3/3 | 1.23 | 0.86 | 1.12 | 0.90 | n/a | n/a | n/a | n/a | none |
| fu-small-local-vs-up-native | up-native `-` | 74464701e372 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point) |
| fu-small-s3 | 74464701e372 `-` | 74464701e372 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | 0.55 | 0.06 | 0.84 | 0.06 | n/a | n/a | n/a | n/a | none |
| fu-small-s3-vs-up-native | up-native `-` | 74464701e372 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-adbc8 (640/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc8 (423/640 errors; 473/640 errors; 477/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point) |
| fu-tpch-local | 74464701e372 `-` | 74464701e372 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 1.01 | 0.96 | 0.97 | n/a | none |
| fu-tpch-local-vs-up-native | up-native `-` | 74464701e372 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)), jdbc10 (md5 50bb2801381f (1/22 ok)) |
| fu-zstd-netem-local | 74464701e372 `CZSTD` | 74464701e372 `-DresourceProfile=speed CZSTD` | local | Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-zstd-netem-local-vs-up-native | up-native `-DflightCompression=zstd` | 74464701e372 `-DresourceProfile=speed CZSTD` | local | Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |

## Per job (absolute medians and ratios)

### fu-load-local: A = 74464701e372 `-`, B = 74464701e372 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 5038.0 | 890.0 | 0.18 | 0.17 0.18 0.19 |

### fu-load-local-vs-up-native: A = up-native `-`, B = 74464701e372 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 986.0 | 890.0 | 0.90 | 0.88 0.80 0.92 |

### fu-scan-local: A = 74464701e372 `-`, B = 74464701e372 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 711.0 | 717.3 | 1.01 | 1.04 0.98 1.01 |
| lineitem scan x4 | MB/s | 752.3 | 964.3 | 1.28 | 1.31 1.27 1.28 |
| lineitem scan x8 | MB/s | 662.4 | 969.3 | 1.46 | 1.46 1.47 1.45 |
| lineitem export ADBC | MB/s | 850.3 | 874.1 | 1.03 | 1.03 0.98 1.03 |
| server RSS peak | MB | 1279.0 | 1188.0 | 0.93 | 0.93 0.90 1.00 |

### fu-scan-local-vs-up-native: A = up-native `-`, B = 74464701e372 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 687.8 | 717.3 | 1.04 | 1.06 1.02 1.03 |
| lineitem scan x4 | MB/s | 908.8 | 964.3 | 1.06 | 1.06 1.06 1.06 |
| lineitem scan x8 | MB/s | n/a | 969.3 | n/a | - |
| lineitem export ADBC | MB/s | 868.2 | 874.1 | 1.01 | 1.02 0.97 1.01 |
| server RSS peak | MB | 3709.0 | 1188.0 | 0.32 | 0.32 0.31 0.32 |

Correctness gate: A: scan8 (rows=342069908 errors=3; rows=381412120 errors=2; rows=383443736 errors=2).

### fu-scan-s3: A = 74464701e372 `-`, B = 74464701e372 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 368.0 | 395.3 | 1.07 | 1.07 1.08 1.06 |
| lineitem scan x4 | MB/s | 443.2 | 602.9 | 1.36 | 1.31 1.36 1.38 |
| lineitem scan x8 | MB/s | 419.0 | 607.6 | 1.45 | 1.43 1.46 1.46 |
| lineitem export ADBC | MB/s | 407.5 | 555.3 | 1.36 | 1.36 1.44 1.38 |
| server RSS peak | MB | 1717.0 | 3311.0 | 1.93 | 1.89 1.93 1.94 |

### fu-scan-s3-vs-up-native: A = up-native `-`, B = 74464701e372 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 372.6 | 395.3 | 1.06 | 1.07 1.05 1.05 |
| lineitem scan x4 | MB/s | 587.6 | 602.9 | 1.03 | 1.03 1.02 1.03 |
| lineitem scan x8 | MB/s | n/a | 607.6 | n/a | - |
| lineitem export ADBC | MB/s | 550.9 | 555.3 | 1.01 | 1.00 1.01 1.03 |
| server RSS peak | MB | 5857.0 | 3311.0 | 0.57 | 0.57 0.57 0.56 |

Correctness gate: A: scan8 (rows=272581136 errors=4; rows=336695956 errors=3; rows=378528536 errors=2).

### fu-sf1-s3: A = 74464701e372 `-`, B = 74464701e372 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 24.8 | 4.5 | 0.18 | 0.19 0.18 0.18 |
| TPC-H SF1 JDBC (sum of medians) | s | 24.6 | 4.6 | 0.19 | 0.19 0.19 0.19 |
| server RSS peak | MB | 750.0 | 979.0 | 1.31 | 1.31 1.33 1.26 |

### fu-sf1-s3-vs-up-native: A = up-native `-`, B = 74464701e372 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | n/a | 4.5 | n/a | - |
| TPC-H SF1 JDBC (sum of medians) | s | n/a | 4.6 | n/a | - |
| server RSS peak | MB | 587.0 | 979.0 | 1.67 | 1.73 1.59 1.67 |

Correctness gate: A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)).

### fu-sf10adbc-s3: A = 74464701e372 `-`, B = 74464701e372 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | 261.2 | 30.5 | 0.12 | 0.12 0.12 0.11 |
| server RSS peak | MB | 1606.0 | 3521.0 | 2.19 | 2.14 2.01 2.24 |

### fu-sf10adbc-s3-vs-up-native: A = up-native `-`, B = 74464701e372 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | n/a | 30.5 | n/a | - |
| server RSS peak | MB | 1037.0 | 3521.0 | 3.40 | 3.34 3.40 3.27 |

Correctness gate: A: adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22).

### fu-sf10jdbc-s3: A = 74464701e372 `-`, B = 74464701e372 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `sf10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 JDBC (sum of medians) | s | 261.7 | 24.8 | 0.09 | 0.10 0.09 0.09 |
| server RSS peak | MB | 1620.0 | 3382.0 | 2.09 | 2.03 2.19 2.09 |

### fu-sf10jdbc-s3-vs-up-native: A = up-native `-`, B = 74464701e372 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `sf10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 JDBC (sum of medians) | s | n/a | 24.8 | n/a | - |
| server RSS peak | MB | 1048.0 | 3382.0 | 3.23 | 3.23 3.30 3.14 |

Correctness gate: A: jdbc10 (md5 50bb2801381f (1/22 ok)).

### fu-small-local: A = 74464701e372 `-`, B = 74464701e372 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 19.2 | 21.6 | 1.12 | 1.08 1.12 1.15 |
| small JDBC c1 p95 | ms | 40.1 | 37.4 | 0.93 | 0.95 0.93 0.92 |
| small JDBC c1 p99 | ms | 47.6 | 43.8 | 0.92 | 0.87 0.76 1.00 |
| small JDBC c8 p50 | ms | 92.3 | 85.9 | 0.93 | 0.94 0.92 0.93 |
| small JDBC c8 p95 | ms | 223.8 | 212.4 | 0.95 | 0.87 0.91 0.98 |
| small JDBC c8 p99 | ms | 276.4 | 271.5 | 0.98 | 0.77 0.99 0.98 |
| small JDBC c32 p50 | ms | 345.9 | 286.7 | 0.83 | 0.78 0.84 0.82 |
| small JDBC c32 p95 | ms | 978.8 | 881.0 | 0.90 | 0.86 0.90 0.89 |
| small JDBC c32 p99 | ms | 1289.6 | 1031.4 | 0.80 | 0.75 0.77 0.80 |
| small ADBC c1 p50 | ms | 12.8 | 15.7 | 1.23 | 1.23 1.33 1.20 |
| small ADBC c1 p95 | ms | 36.1 | 36.2 | 1.00 | 1.01 1.08 0.94 |
| small ADBC c1 p99 | ms | 49.4 | 41.1 | 0.83 | 0.72 0.83 1.12 |
| small ADBC c8 p50 | ms | 81.4 | 79.6 | 0.98 | 0.91 0.94 1.03 |
| small ADBC c8 p95 | ms | 239.2 | 217.0 | 0.91 | 0.91 0.89 0.92 |
| small ADBC c8 p99 | ms | 309.5 | 287.5 | 0.93 | 0.95 0.88 1.03 |
| small ADBC c32 p50 | ms | 310.3 | 286.3 | 0.92 | 0.78 0.92 0.95 |
| small ADBC c32 p95 | ms | 1004.0 | 858.4 | 0.86 | 0.88 0.84 0.86 |
| small ADBC c32 p99 | ms | 1331.1 | 1045.7 | 0.79 | 0.82 0.74 0.76 |
| server RSS peak | MB | 1554.0 | 904.0 | 0.58 | 0.57 0.59 0.57 |

### fu-small-local-vs-up-native: A = up-native `-`, B = 74464701e372 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | n/a | 21.6 | n/a | - |
| small JDBC c1 p95 | ms | n/a | 37.4 | n/a | - |
| small JDBC c1 p99 | ms | n/a | 43.8 | n/a | - |
| small JDBC c8 p50 | ms | n/a | 85.9 | n/a | - |
| small JDBC c8 p95 | ms | n/a | 212.4 | n/a | - |
| small JDBC c8 p99 | ms | n/a | 271.5 | n/a | - |
| small JDBC c32 p50 | ms | n/a | 286.7 | n/a | - |
| small JDBC c32 p95 | ms | n/a | 881.0 | n/a | - |
| small JDBC c32 p99 | ms | n/a | 1031.4 | n/a | - |
| small ADBC c1 p50 | ms | n/a | 15.7 | n/a | - |
| small ADBC c1 p95 | ms | n/a | 36.2 | n/a | - |
| small ADBC c1 p99 | ms | n/a | 41.1 | n/a | - |
| small ADBC c8 p50 | ms | n/a | 79.6 | n/a | - |
| small ADBC c8 p95 | ms | n/a | 217.0 | n/a | - |
| small ADBC c8 p99 | ms | n/a | 287.5 | n/a | - |
| small ADBC c32 p50 | ms | n/a | 286.3 | n/a | - |
| small ADBC c32 p95 | ms | n/a | 858.4 | n/a | - |
| small ADBC c32 p99 | ms | n/a | 1045.7 | n/a | - |
| server RSS peak | MB | 253.0 | 904.0 | 3.57 | 3.49 3.63 3.58 |

Correctness gate: A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point).

### fu-small-s3: A = 74464701e372 `-`, B = 74464701e372 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 29.1 | 24.6 | 0.84 | 0.90 0.80 0.79 |
| small JDBC c1 p95 | ms | 709.9 | 46.7 | 0.07 | 0.06 0.07 0.07 |
| small JDBC c1 p99 | ms | 772.5 | 57.3 | 0.07 | 0.07 0.07 0.09 |
| small JDBC c8 p50 | ms | 272.3 | 70.7 | 0.26 | 0.24 0.28 0.25 |
| small JDBC c8 p95 | ms | 3736.6 | 168.5 | 0.05 | 0.04 0.04 0.05 |
| small JDBC c8 p99 | ms | 4071.1 | 217.7 | 0.05 | 0.05 0.05 0.05 |
| small JDBC c32 p50 | ms | 971.4 | 196.9 | 0.20 | 0.20 0.20 0.22 |
| small JDBC c32 p95 | ms | 13244.0 | 820.8 | 0.06 | 0.06 0.06 0.05 |
| small JDBC c32 p99 | ms | 14995.0 | 938.7 | 0.06 | 0.06 0.07 0.04 |
| small ADBC c1 p50 | ms | 22.5 | 12.3 | 0.55 | 0.55 0.54 0.55 |
| small ADBC c1 p95 | ms | 729.1 | 32.8 | 0.04 | 0.04 0.05 0.04 |
| small ADBC c1 p99 | ms | 759.7 | 40.7 | 0.05 | 0.05 0.06 0.04 |
| small ADBC c8 p50 | ms | 259.6 | 53.8 | 0.21 | 0.19 0.21 0.21 |
| small ADBC c8 p95 | ms | 3818.9 | 166.3 | 0.04 | 0.04 0.04 0.04 |
| small ADBC c8 p99 | ms | 4287.2 | 218.9 | 0.05 | 0.05 0.05 0.05 |
| small ADBC c32 p50 | ms | 984.7 | 174.1 | 0.18 | 0.19 0.17 0.16 |
| small ADBC c32 p95 | ms | 13487.7 | 794.2 | 0.06 | 0.06 0.06 0.06 |
| small ADBC c32 p99 | ms | 15123.6 | 933.6 | 0.06 | 0.06 0.05 0.06 |
| server RSS peak | MB | 2303.0 | 1523.0 | 0.66 | 0.66 0.68 0.65 |

### fu-small-s3-vs-up-native: A = up-native `-`, B = 74464701e372 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | n/a | 24.6 | n/a | - |
| small JDBC c1 p95 | ms | n/a | 46.7 | n/a | - |
| small JDBC c1 p99 | ms | n/a | 57.3 | n/a | - |
| small JDBC c8 p50 | ms | n/a | 70.7 | n/a | - |
| small JDBC c8 p95 | ms | n/a | 168.5 | n/a | - |
| small JDBC c8 p99 | ms | n/a | 217.7 | n/a | - |
| small JDBC c32 p50 | ms | n/a | 196.9 | n/a | - |
| small JDBC c32 p95 | ms | n/a | 820.8 | n/a | - |
| small JDBC c32 p99 | ms | n/a | 938.7 | n/a | - |
| small ADBC c1 p50 | ms | n/a | 12.3 | n/a | - |
| small ADBC c1 p95 | ms | n/a | 32.8 | n/a | - |
| small ADBC c1 p99 | ms | n/a | 40.7 | n/a | - |
| small ADBC c8 p50 | ms | n/a | 53.8 | n/a | - |
| small ADBC c8 p95 | ms | n/a | 166.3 | n/a | - |
| small ADBC c8 p99 | ms | n/a | 218.9 | n/a | - |
| small ADBC c32 p50 | ms | n/a | 174.1 | n/a | - |
| small ADBC c32 p95 | ms | n/a | 794.2 | n/a | - |
| small ADBC c32 p99 | ms | n/a | 933.6 | n/a | - |
| server RSS peak | MB | 378.0 | 1523.0 | 4.03 | 4.03 4.16 3.83 |

Correctness gate: A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-adbc8 (640/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc8 (423/640 errors; 473/640 errors; 477/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point).

### fu-tpch-local: A = 74464701e372 `-`, B = 74464701e372 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 3.3 | 3.3 | 1.01 | 1.01 1.01 1.03 |
| TPC-H SF10 ADBC (sum of medians) | s | 34.3 | 32.7 | 0.96 | 0.97 0.96 0.95 |
| TPC-H SF1 JDBC (sum of medians) | s | 3.4 | 3.4 | 1.00 | 1.00 1.04 0.98 |
| TPC-H SF10 JDBC (sum of medians) | s | 33.8 | 32.8 | 0.97 | 0.97 0.97 0.96 |
| server RSS peak | MB | 1649.0 | 1829.0 | 1.11 | 1.09 1.11 1.22 |

### fu-tpch-local-vs-up-native: A = up-native `-`, B = 74464701e372 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | n/a | 3.3 | n/a | - |
| TPC-H SF10 ADBC (sum of medians) | s | n/a | 32.7 | n/a | - |
| TPC-H SF1 JDBC (sum of medians) | s | n/a | 3.4 | n/a | - |
| TPC-H SF10 JDBC (sum of medians) | s | n/a | 32.8 | n/a | - |
| server RSS peak | MB | 355.0 | 1829.0 | 5.15 | 5.16 5.15 5.30 |

Correctness gate: A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)), jdbc10 (md5 50bb2801381f (1/22 ok)).

### fu-zstd-netem-local: A = 74464701e372 `CZSTD`, B = 74464701e372 `-DresourceProfile=speed CZSTD`, local

Runner: Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C. Workloads: `netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 1604.0 | 1782.0 | 1.11 | 1.18 1.12 1.11 |

### fu-zstd-netem-local-vs-up-native: A = up-native `-DflightCompression=zstd`, B = 74464701e372 `-DresourceProfile=speed CZSTD`, local

Runner: Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C. Workloads: `netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 603.0 | 1782.0 | 2.96 | 2.94 2.97 2.86 |
