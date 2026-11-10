# Wave fresh-up-894afb9b48c4 (server comparison), run 42775953599

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

## Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| fu-load-local | 894afb9b48c4 `-` | 894afb9b48c4 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-load-local-vs-up-native | up-native `-` | 894afb9b48c4 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-scan-local | 894afb9b48c4 `-` | 894afb9b48c4 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.00 | none |
| fu-scan-local-vs-up-native | up-native `-` | 894afb9b48c4 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.03 | A: scan8 (rows=226685324 errors=5; rows=321819284 errors=3; rows=381215512 errors=2) |
| fu-scan-s3 | 894afb9b48c4 `-` | 894afb9b48c4 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.12 | none |
| fu-scan-s3-vs-up-native | up-native `-` | 894afb9b48c4 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.18 | A: scan8 (rows=377479960 errors=2; rows=394584856 errors=2; rows=458699676 errors=1) |
| fu-sf1-s3 | 894afb9b48c4 `-` | 894afb9b48c4 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 0.16 | n/a | n/a | n/a | none |
| fu-sf1-s3-vs-up-native | up-native `-` | 894afb9b48c4 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)) |
| fu-sf10adbc-s3 | 894afb9b48c4 `-` | 894afb9b48c4 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C | 3/3 | n/a | n/a | n/a | n/a | n/a | 0.17 | n/a | n/a | none |
| fu-sf10adbc-s3-vs-up-native | up-native `-` | 894afb9b48c4 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22) |
| fu-sf10jdbc-s3 | 894afb9b48c4 `-` | 894afb9b48c4 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | 0.19 | n/a | none |
| fu-sf10jdbc-s3-vs-up-native | up-native `-` | 894afb9b48c4 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: jdbc10 (md5 50bb2801381f (1/22 ok)) |
| fu-small-local | 894afb9b48c4 `-` | 894afb9b48c4 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | 1.28 | 0.81 | 1.19 | 0.87 | n/a | n/a | n/a | n/a | none |
| fu-small-local-vs-up-native | up-native `-` | 894afb9b48c4 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point) |
| fu-small-s3 | 894afb9b48c4 `-` | 894afb9b48c4 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | 0.53 | 0.07 | 0.82 | 0.06 | n/a | n/a | n/a | n/a | none |
| fu-small-s3-vs-up-native | up-native `-` | 894afb9b48c4 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-adbc8 (640/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc8 (376/640 errors; 469/640 errors; 567/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point) |
| fu-tpch-local | 894afb9b48c4 `-` | 894afb9b48c4 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C | 3/3 | n/a | n/a | n/a | n/a | 0.99 | 0.98 | 0.97 | n/a | none |
| fu-tpch-local-vs-up-native | up-native `-` | 894afb9b48c4 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)), jdbc10 (md5 50bb2801381f (1/22 ok)) |
| fu-zstd-netem-local | 894afb9b48c4 `CZSTD` | 894afb9b48c4 `-DresourceProfile=speed CZSTD` | local | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-zstd-netem-local-vs-up-native | up-native `-DflightCompression=zstd` | 894afb9b48c4 `-DresourceProfile=speed CZSTD` | local | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |

## Per job (absolute medians and ratios)

### fu-load-local: A = 894afb9b48c4 `-`, B = 894afb9b48c4 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 5335.0 | 1053.0 | 0.20 | 0.20 0.20 0.20 |

### fu-load-local-vs-up-native: A = up-native `-`, B = 894afb9b48c4 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 1031.0 | 1053.0 | 1.02 | 0.99 1.04 1.10 |

### fu-scan-local: A = 894afb9b48c4 `-`, B = 894afb9b48c4 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 552.0 | 552.1 | 1.00 | 1.00 0.99 1.00 |
| lineitem scan x4 | MB/s | 565.9 | 734.1 | 1.30 | 1.34 1.29 1.30 |
| lineitem scan x8 | MB/s | 487.7 | 740.3 | 1.52 | 1.53 1.48 1.53 |
| lineitem export ADBC | MB/s | 649.6 | 658.1 | 1.01 | 1.00 1.01 1.02 |
| server RSS peak | MB | 1234.0 | 1180.0 | 0.96 | 0.97 0.93 0.96 |

### fu-scan-local-vs-up-native: A = up-native `-`, B = 894afb9b48c4 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 536.1 | 552.1 | 1.03 | 1.05 1.00 1.04 |
| lineitem scan x4 | MB/s | 683.7 | 734.1 | 1.07 | 1.04 1.09 1.07 |
| lineitem scan x8 | MB/s | n/a | 740.3 | n/a | - |
| lineitem export ADBC | MB/s | 661.6 | 658.1 | 0.99 | 0.99 1.01 0.96 |
| server RSS peak | MB | 3680.0 | 1180.0 | 0.32 | 0.32 0.32 0.32 |

Correctness gate: A: scan8 (rows=226685324 errors=5; rows=321819284 errors=3; rows=381215512 errors=2).

### fu-scan-s3: A = 894afb9b48c4 `-`, B = 894afb9b48c4 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 327.2 | 366.8 | 1.12 | 1.13 1.15 1.01 |
| lineitem scan x4 | MB/s | 389.7 | 718.8 | 1.84 | 1.76 1.90 1.75 |
| lineitem scan x8 | MB/s | 420.6 | 691.8 | 1.64 | 1.47 1.69 1.72 |
| lineitem export ADBC | MB/s | 300.7 | 401.2 | 1.33 | 2.00 1.04 1.33 |
| server RSS peak | MB | 1703.0 | 3064.0 | 1.80 | 1.80 1.90 1.80 |

### fu-scan-s3-vs-up-native: A = up-native `-`, B = 894afb9b48c4 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 310.4 | 366.8 | 1.18 | 1.31 1.66 1.06 |
| lineitem scan x4 | MB/s | 669.4 | 718.8 | 1.07 | 1.02 1.12 1.02 |
| lineitem scan x8 | MB/s | n/a | 691.8 | n/a | - |
| lineitem export ADBC | MB/s | 647.4 | 401.2 | 0.62 | 0.92 0.62 0.61 |
| server RSS peak | MB | 5950.0 | 3064.0 | 0.51 | 0.52 0.55 0.51 |

Correctness gate: A: scan8 (rows=377479960 errors=2; rows=394584856 errors=2; rows=458699676 errors=1).

### fu-sf1-s3: A = 894afb9b48c4 `-`, B = 894afb9b48c4 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 26.2 | 4.2 | 0.16 | 0.16 0.17 0.16 |
| TPC-H SF1 JDBC (sum of medians) | s | 26.0 | 4.2 | 0.16 | 0.16 0.17 0.16 |
| server RSS peak | MB | 776.0 | 1002.0 | 1.29 | 1.29 1.18 1.32 |

### fu-sf1-s3-vs-up-native: A = up-native `-`, B = 894afb9b48c4 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | n/a | 4.2 | n/a | - |
| TPC-H SF1 JDBC (sum of medians) | s | n/a | 4.2 | n/a | - |
| server RSS peak | MB | 626.0 | 1002.0 | 1.60 | 1.72 1.53 1.59 |

Correctness gate: A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)).

### fu-sf10adbc-s3: A = 894afb9b48c4 `-`, B = 894afb9b48c4 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | 264.5 | 45.9 | 0.17 | 0.17 0.17 0.18 |
| server RSS peak | MB | 1614.0 | 3043.0 | 1.89 | 1.93 1.88 1.87 |

### fu-sf10adbc-s3-vs-up-native: A = up-native `-`, B = 894afb9b48c4 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | n/a | 45.9 | n/a | - |
| server RSS peak | MB | 978.0 | 3043.0 | 3.11 | 2.98 3.20 3.11 |

Correctness gate: A: adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22).

### fu-sf10jdbc-s3: A = 894afb9b48c4 `-`, B = 894afb9b48c4 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 JDBC (sum of medians) | s | 288.4 | 54.0 | 0.19 | 0.18 0.20 0.19 |
| server RSS peak | MB | 1649.0 | 3179.0 | 1.93 | 1.87 1.91 2.05 |

### fu-sf10jdbc-s3-vs-up-native: A = up-native `-`, B = 894afb9b48c4 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 JDBC (sum of medians) | s | n/a | 54.0 | n/a | - |
| server RSS peak | MB | 982.0 | 3179.0 | 3.24 | 3.14 3.17 3.39 |

Correctness gate: A: jdbc10 (md5 50bb2801381f (1/22 ok)).

### fu-small-local: A = 894afb9b48c4 `-`, B = 894afb9b48c4 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 15.4 | 18.4 | 1.19 | 1.28 1.12 1.19 |
| small JDBC c1 p95 | ms | 31.2 | 31.9 | 1.02 | 1.12 1.01 1.02 |
| small JDBC c1 p99 | ms | 41.2 | 38.7 | 0.94 | 1.10 0.91 0.91 |
| small JDBC c8 p50 | ms | 76.6 | 75.2 | 0.98 | 1.03 0.96 1.00 |
| small JDBC c8 p95 | ms | 186.6 | 182.6 | 0.98 | 0.98 0.91 0.99 |
| small JDBC c8 p99 | ms | 253.2 | 219.2 | 0.87 | 0.84 0.80 1.00 |
| small JDBC c32 p50 | ms | 290.9 | 255.9 | 0.88 | 0.95 0.85 0.83 |
| small JDBC c32 p95 | ms | 828.9 | 717.8 | 0.87 | 0.86 0.88 0.89 |
| small JDBC c32 p99 | ms | 1083.3 | 830.6 | 0.77 | 0.77 0.80 0.75 |
| small ADBC c1 p50 | ms | 10.3 | 13.2 | 1.28 | 1.34 1.20 1.36 |
| small ADBC c1 p95 | ms | 30.2 | 31.0 | 1.03 | 1.02 1.06 0.97 |
| small ADBC c1 p99 | ms | 36.9 | 36.7 | 1.00 | 1.03 1.13 0.90 |
| small ADBC c8 p50 | ms | 65.1 | 62.7 | 0.96 | 1.03 0.98 0.90 |
| small ADBC c8 p95 | ms | 176.3 | 172.7 | 0.98 | 1.01 0.95 0.97 |
| small ADBC c8 p99 | ms | 224.7 | 215.3 | 0.96 | 1.02 0.99 0.96 |
| small ADBC c32 p50 | ms | 271.8 | 231.2 | 0.85 | 0.88 0.84 0.85 |
| small ADBC c32 p95 | ms | 854.2 | 695.9 | 0.81 | 0.80 0.84 0.81 |
| small ADBC c32 p99 | ms | 1139.7 | 827.2 | 0.73 | 0.64 0.77 0.71 |
| server RSS peak | MB | 1552.0 | 794.0 | 0.51 | 0.51 0.50 0.52 |

### fu-small-local-vs-up-native: A = up-native `-`, B = 894afb9b48c4 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | n/a | 18.4 | n/a | - |
| small JDBC c1 p95 | ms | n/a | 31.9 | n/a | - |
| small JDBC c1 p99 | ms | n/a | 38.7 | n/a | - |
| small JDBC c8 p50 | ms | n/a | 75.2 | n/a | - |
| small JDBC c8 p95 | ms | n/a | 182.6 | n/a | - |
| small JDBC c8 p99 | ms | n/a | 219.2 | n/a | - |
| small JDBC c32 p50 | ms | n/a | 255.9 | n/a | - |
| small JDBC c32 p95 | ms | n/a | 717.8 | n/a | - |
| small JDBC c32 p99 | ms | n/a | 830.6 | n/a | - |
| small ADBC c1 p50 | ms | n/a | 13.2 | n/a | - |
| small ADBC c1 p95 | ms | n/a | 31.0 | n/a | - |
| small ADBC c1 p99 | ms | n/a | 36.7 | n/a | - |
| small ADBC c8 p50 | ms | n/a | 62.7 | n/a | - |
| small ADBC c8 p95 | ms | n/a | 172.7 | n/a | - |
| small ADBC c8 p99 | ms | n/a | 215.3 | n/a | - |
| small ADBC c32 p50 | ms | n/a | 231.2 | n/a | - |
| small ADBC c32 p95 | ms | n/a | 695.9 | n/a | - |
| small ADBC c32 p99 | ms | n/a | 827.2 | n/a | - |
| server RSS peak | MB | 254.0 | 794.0 | 3.13 | 3.09 3.11 3.23 |

Correctness gate: A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point).

### fu-small-s3: A = 894afb9b48c4 `-`, B = 894afb9b48c4 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 33.0 | 27.1 | 0.82 | 0.81 0.65 0.92 |
| small JDBC c1 p95 | ms | 581.8 | 74.4 | 0.13 | 0.09 0.11 0.27 |
| small JDBC c1 p99 | ms | 1075.6 | 222.8 | 0.21 | 0.15 0.14 0.23 |
| small JDBC c8 p50 | ms | 260.1 | 76.2 | 0.29 | 0.30 0.29 0.32 |
| small JDBC c8 p95 | ms | 3560.3 | 187.7 | 0.05 | 0.07 0.05 0.05 |
| small JDBC c8 p99 | ms | 3904.2 | 264.0 | 0.07 | 0.09 0.07 0.05 |
| small JDBC c32 p50 | ms | 955.7 | 217.3 | 0.23 | 0.23 0.23 0.21 |
| small JDBC c32 p95 | ms | 12810.0 | 792.9 | 0.06 | 0.06 0.06 0.06 |
| small JDBC c32 p99 | ms | 15588.1 | 927.6 | 0.06 | 0.06 0.07 0.06 |
| small ADBC c1 p50 | ms | 24.5 | 13.0 | 0.53 | 0.53 0.50 0.54 |
| small ADBC c1 p95 | ms | 578.5 | 33.9 | 0.06 | 0.06 0.06 0.06 |
| small ADBC c1 p99 | ms | 664.3 | 43.4 | 0.07 | 0.07 0.04 0.06 |
| small ADBC c8 p50 | ms | 252.6 | 54.6 | 0.22 | 0.22 0.20 0.22 |
| small ADBC c8 p95 | ms | 3529.3 | 166.9 | 0.05 | 0.05 0.05 0.05 |
| small ADBC c8 p99 | ms | 3791.1 | 225.6 | 0.06 | 0.06 0.06 0.06 |
| small ADBC c32 p50 | ms | 897.6 | 181.2 | 0.20 | 0.20 0.20 0.20 |
| small ADBC c32 p95 | ms | 12100.2 | 793.5 | 0.07 | 0.06 0.07 0.07 |
| small ADBC c32 p99 | ms | 13730.8 | 930.3 | 0.07 | 0.07 0.06 0.07 |
| server RSS peak | MB | 2270.0 | 1448.0 | 0.64 | 0.64 0.63 0.64 |

### fu-small-s3-vs-up-native: A = up-native `-`, B = 894afb9b48c4 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | n/a | 27.1 | n/a | - |
| small JDBC c1 p95 | ms | n/a | 74.4 | n/a | - |
| small JDBC c1 p99 | ms | n/a | 222.8 | n/a | - |
| small JDBC c8 p50 | ms | n/a | 76.2 | n/a | - |
| small JDBC c8 p95 | ms | n/a | 187.7 | n/a | - |
| small JDBC c8 p99 | ms | n/a | 264.0 | n/a | - |
| small JDBC c32 p50 | ms | n/a | 217.3 | n/a | - |
| small JDBC c32 p95 | ms | n/a | 792.9 | n/a | - |
| small JDBC c32 p99 | ms | n/a | 927.6 | n/a | - |
| small ADBC c1 p50 | ms | n/a | 13.0 | n/a | - |
| small ADBC c1 p95 | ms | n/a | 33.9 | n/a | - |
| small ADBC c1 p99 | ms | n/a | 43.4 | n/a | - |
| small ADBC c8 p50 | ms | n/a | 54.6 | n/a | - |
| small ADBC c8 p95 | ms | n/a | 166.9 | n/a | - |
| small ADBC c8 p99 | ms | n/a | 225.6 | n/a | - |
| small ADBC c32 p50 | ms | n/a | 181.2 | n/a | - |
| small ADBC c32 p95 | ms | n/a | 793.5 | n/a | - |
| small ADBC c32 p99 | ms | n/a | 930.3 | n/a | - |
| server RSS peak | MB | 401.0 | 1448.0 | 3.61 | 3.61 3.52 4.01 |

Correctness gate: A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-adbc8 (640/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc8 (376/640 errors; 469/640 errors; 567/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point).

### fu-tpch-local: A = 894afb9b48c4 `-`, B = 894afb9b48c4 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 4.1 | 4.1 | 0.99 | 0.98 1.03 1.00 |
| TPC-H SF10 ADBC (sum of medians) | s | 40.3 | 39.4 | 0.98 | 0.98 0.98 0.98 |
| TPC-H SF1 JDBC (sum of medians) | s | 4.1 | 4.2 | 1.01 | 1.01 0.99 1.00 |
| TPC-H SF10 JDBC (sum of medians) | s | 40.8 | 39.5 | 0.97 | 0.97 0.97 0.96 |
| server RSS peak | MB | 1650.0 | 1891.0 | 1.15 | 1.14 1.15 1.18 |

### fu-tpch-local-vs-up-native: A = up-native `-`, B = 894afb9b48c4 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | n/a | 4.1 | n/a | - |
| TPC-H SF10 ADBC (sum of medians) | s | n/a | 39.4 | n/a | - |
| TPC-H SF1 JDBC (sum of medians) | s | n/a | 4.2 | n/a | - |
| TPC-H SF10 JDBC (sum of medians) | s | n/a | 39.5 | n/a | - |
| server RSS peak | MB | 351.0 | 1891.0 | 5.39 | 5.41 5.17 5.39 |

Correctness gate: A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)), jdbc10 (md5 50bb2801381f (1/22 ok)).

### fu-zstd-netem-local: A = 894afb9b48c4 `CZSTD`, B = 894afb9b48c4 `-DresourceProfile=speed CZSTD`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 1613.0 | 1782.0 | 1.10 | 1.14 1.16 1.10 |

### fu-zstd-netem-local-vs-up-native: A = up-native `-DflightCompression=zstd`, B = 894afb9b48c4 `-DresourceProfile=speed CZSTD`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 640.0 | 1782.0 | 2.78 | 2.61 3.16 2.78 |
