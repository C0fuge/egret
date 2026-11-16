# Wave fresh-up-6f0aa5a026fa (server comparison), run 43840086547

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

## Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| fu-load-local | 6f0aa5a026fa `-` | 6f0aa5a026fa `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-load-local-vs-up-native | up-native `-` | 6f0aa5a026fa `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-scan-local | 6f0aa5a026fa `-` | 6f0aa5a026fa `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 0.97 | none |
| fu-scan-local-vs-up-native | up-native `-` | 6f0aa5a026fa `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.03 | A: scan8 (rows=382919448 errors=2; rows=388948760 errors=2) |
| fu-scan-s3 | 6f0aa5a026fa `-` | 6f0aa5a026fa `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.08 | none |
| fu-scan-s3-vs-up-native | up-native `-` | 6f0aa5a026fa `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.24 | A: scan8 (rows=324047508 errors=3; rows=434320284 errors=1; rows=445723548 errors=1) |
| fu-sf1-s3 | 6f0aa5a026fa `-` | 6f0aa5a026fa `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 0.13 | n/a | n/a | n/a | none |
| fu-sf1-s3-vs-up-native | up-native `-` | 6f0aa5a026fa `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)) |
| fu-sf10adbc-s3 | 6f0aa5a026fa `-` | 6f0aa5a026fa `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU Intel(R) Xeon(R) 6973P-C | 3/3 | n/a | n/a | n/a | n/a | n/a | 0.11 | n/a | n/a | none |
| fu-sf10adbc-s3-vs-up-native | up-native `-` | 6f0aa5a026fa `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU Intel(R) Xeon(R) 6973P-C | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22) |
| fu-sf10jdbc-s3 | 6f0aa5a026fa `-` | 6f0aa5a026fa `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | 0.16 | n/a | none |
| fu-sf10jdbc-s3-vs-up-native | up-native `-` | 6f0aa5a026fa `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: jdbc10 (md5 50bb2801381f (1/22 ok)) |
| fu-small-local | 6f0aa5a026fa `-` | 6f0aa5a026fa `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | 1.26 | 0.81 | 1.11 | 0.80 | n/a | n/a | n/a | n/a | none |
| fu-small-local-vs-up-native | up-native `-` | 6f0aa5a026fa `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point) |
| fu-small-s3 | 6f0aa5a026fa `-` | 6f0aa5a026fa `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | 0.51 | 0.06 | 0.78 | 0.06 | n/a | n/a | n/a | n/a | none |
| fu-small-s3-vs-up-native | up-native `-` | 6f0aa5a026fa `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-adbc8 (640/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc8 (425/640 errors; 456/640 errors; 527/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point) |
| fu-tpch-local | 6f0aa5a026fa `-` | 6f0aa5a026fa `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 1.03 | 0.98 | 0.95 | n/a | none |
| fu-tpch-local-vs-up-native | up-native `-` | 6f0aa5a026fa `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)), jdbc10 (md5 50bb2801381f (1/22 ok)) |
| fu-zstd-netem-local | 6f0aa5a026fa `CZSTD` | 6f0aa5a026fa `-DresourceProfile=speed CZSTD` | local | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-zstd-netem-local-vs-up-native | up-native `-DflightCompression=zstd` | 6f0aa5a026fa `-DresourceProfile=speed CZSTD` | local | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |

## Per job (absolute medians and ratios)

### fu-load-local: A = 6f0aa5a026fa `-`, B = 6f0aa5a026fa `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 4554.0 | 858.0 | 0.19 | 0.19 0.24 0.19 |

### fu-load-local-vs-up-native: A = up-native `-`, B = 6f0aa5a026fa `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 932.0 | 858.0 | 0.92 | 0.91 1.17 0.93 |

### fu-scan-local: A = 6f0aa5a026fa `-`, B = 6f0aa5a026fa `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 654.7 | 636.3 | 0.97 | 1.00 0.96 1.04 |
| lineitem scan x4 | MB/s | 681.6 | 846.5 | 1.24 | 1.24 1.18 1.30 |
| lineitem scan x8 | MB/s | 613.2 | 860.4 | 1.40 | 1.46 1.40 1.44 |
| lineitem export ADBC | MB/s | 766.5 | 790.2 | 1.03 | 1.05 1.04 0.99 |
| server RSS peak | MB | 1364.0 | 1184.0 | 0.87 | 0.80 0.87 0.93 |

### fu-scan-local-vs-up-native: A = up-native `-`, B = 6f0aa5a026fa `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 617.8 | 636.3 | 1.03 | 1.02 1.03 1.10 |
| lineitem scan x4 | MB/s | 795.3 | 846.5 | 1.06 | 1.06 1.06 1.09 |
| lineitem scan x8 | MB/s | n/a | 860.4 | n/a | - |
| lineitem export ADBC | MB/s | 773.1 | 790.2 | 1.02 | 1.01 1.04 1.01 |
| server RSS peak | MB | 3692.0 | 1184.0 | 0.32 | 0.30 0.32 0.32 |

Correctness gate: A: scan8 (rows=382919448 errors=2; rows=388948760 errors=2).

### fu-scan-s3: A = 6f0aa5a026fa `-`, B = 6f0aa5a026fa `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 380.2 | 410.5 | 1.08 | 1.67 1.03 0.78 |
| lineitem scan x4 | MB/s | 443.8 | 721.0 | 1.62 | 1.60 1.62 1.66 |
| lineitem scan x8 | MB/s | 452.3 | 728.4 | 1.61 | 1.61 1.75 1.55 |
| lineitem export ADBC | MB/s | 380.9 | 659.3 | 1.73 | 1.65 1.83 1.73 |
| server RSS peak | MB | 1741.0 | 3317.0 | 1.91 | 1.91 1.93 1.89 |

### fu-scan-s3-vs-up-native: A = up-native `-`, B = 6f0aa5a026fa `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 330.6 | 410.5 | 1.24 | 1.59 1.07 0.90 |
| lineitem scan x4 | MB/s | 685.0 | 721.0 | 1.05 | 1.06 1.06 1.05 |
| lineitem scan x8 | MB/s | n/a | 728.4 | n/a | - |
| lineitem export ADBC | MB/s | 651.8 | 659.3 | 1.01 | 1.03 1.02 0.99 |
| server RSS peak | MB | 5937.0 | 3317.0 | 0.56 | 0.56 0.56 0.57 |

Correctness gate: A: scan8 (rows=324047508 errors=3; rows=434320284 errors=1; rows=445723548 errors=1).

### fu-sf1-s3: A = 6f0aa5a026fa `-`, B = 6f0aa5a026fa `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 25.3 | 3.3 | 0.13 | 0.15 0.11 0.13 |
| TPC-H SF1 JDBC (sum of medians) | s | 24.4 | 3.4 | 0.14 | 0.15 0.12 0.14 |
| server RSS peak | MB | 785.0 | 1001.0 | 1.28 | 1.31 1.26 1.20 |

### fu-sf1-s3-vs-up-native: A = up-native `-`, B = 6f0aa5a026fa `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | n/a | 3.3 | n/a | - |
| TPC-H SF1 JDBC (sum of medians) | s | n/a | 3.4 | n/a | - |
| server RSS peak | MB | 568.0 | 1001.0 | 1.76 | 1.82 1.76 1.53 |

Correctness gate: A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)).

### fu-sf10adbc-s3: A = 6f0aa5a026fa `-`, B = 6f0aa5a026fa `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU Intel(R) Xeon(R) 6973P-C. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | 276.1 | 30.1 | 0.11 | 0.14 0.10 0.11 |
| server RSS peak | MB | 1642.0 | 3447.0 | 2.10 | 2.12 2.07 2.08 |

### fu-sf10adbc-s3-vs-up-native: A = up-native `-`, B = 6f0aa5a026fa `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU Intel(R) Xeon(R) 6973P-C. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | n/a | 30.1 | n/a | - |
| server RSS peak | MB | 1068.0 | 3447.0 | 3.23 | 3.15 3.28 3.36 |

Correctness gate: A: adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22).

### fu-sf10jdbc-s3: A = 6f0aa5a026fa `-`, B = 6f0aa5a026fa `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 JDBC (sum of medians) | s | 289.5 | 46.0 | 0.16 | 0.16 0.15 0.16 |
| server RSS peak | MB | 1601.0 | 3362.0 | 2.10 | 2.13 2.09 2.01 |

### fu-sf10jdbc-s3-vs-up-native: A = up-native `-`, B = 6f0aa5a026fa `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 JDBC (sum of medians) | s | n/a | 46.0 | n/a | - |
| server RSS peak | MB | 1015.0 | 3362.0 | 3.31 | 3.38 3.30 3.24 |

Correctness gate: A: jdbc10 (md5 50bb2801381f (1/22 ok)).

### fu-small-local: A = 6f0aa5a026fa `-`, B = 6f0aa5a026fa `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 16.0 | 17.8 | 1.11 | 1.12 1.01 1.05 |
| small JDBC c1 p95 | ms | 33.1 | 32.9 | 0.99 | 0.99 1.06 0.99 |
| small JDBC c1 p99 | ms | 41.7 | 38.6 | 0.93 | 0.82 0.97 1.05 |
| small JDBC c8 p50 | ms | 77.9 | 75.9 | 0.97 | 0.90 0.97 0.99 |
| small JDBC c8 p95 | ms | 199.3 | 174.0 | 0.87 | 0.85 0.88 0.87 |
| small JDBC c8 p99 | ms | 275.0 | 211.7 | 0.77 | 0.79 0.77 0.76 |
| small JDBC c32 p50 | ms | 314.4 | 252.8 | 0.80 | 0.88 0.80 0.84 |
| small JDBC c32 p95 | ms | 891.5 | 710.1 | 0.80 | 0.85 0.78 0.79 |
| small JDBC c32 p99 | ms | 1168.2 | 831.5 | 0.71 | 0.72 0.71 0.68 |
| small ADBC c1 p50 | ms | 10.4 | 13.1 | 1.26 | 1.22 1.16 1.26 |
| small ADBC c1 p95 | ms | 31.9 | 32.4 | 1.01 | 0.93 0.88 1.10 |
| small ADBC c1 p99 | ms | 43.6 | 39.1 | 0.90 | 0.83 0.87 0.93 |
| small ADBC c8 p50 | ms | 64.3 | 62.4 | 0.97 | 0.97 0.92 1.02 |
| small ADBC c8 p95 | ms | 182.0 | 166.4 | 0.91 | 0.95 0.94 0.91 |
| small ADBC c8 p99 | ms | 235.3 | 220.3 | 0.94 | 0.92 0.88 0.94 |
| small ADBC c32 p50 | ms | 277.7 | 243.8 | 0.88 | 0.94 0.81 0.86 |
| small ADBC c32 p95 | ms | 872.9 | 708.6 | 0.81 | 0.82 0.78 0.81 |
| small ADBC c32 p99 | ms | 1370.1 | 824.9 | 0.60 | 0.61 0.56 0.60 |
| server RSS peak | MB | 1513.0 | 794.0 | 0.52 | 0.55 0.51 0.52 |

### fu-small-local-vs-up-native: A = up-native `-`, B = 6f0aa5a026fa `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | n/a | 17.8 | n/a | - |
| small JDBC c1 p95 | ms | n/a | 32.9 | n/a | - |
| small JDBC c1 p99 | ms | n/a | 38.6 | n/a | - |
| small JDBC c8 p50 | ms | n/a | 75.9 | n/a | - |
| small JDBC c8 p95 | ms | n/a | 174.0 | n/a | - |
| small JDBC c8 p99 | ms | n/a | 211.7 | n/a | - |
| small JDBC c32 p50 | ms | n/a | 252.8 | n/a | - |
| small JDBC c32 p95 | ms | n/a | 710.1 | n/a | - |
| small JDBC c32 p99 | ms | n/a | 831.5 | n/a | - |
| small ADBC c1 p50 | ms | n/a | 13.1 | n/a | - |
| small ADBC c1 p95 | ms | n/a | 32.4 | n/a | - |
| small ADBC c1 p99 | ms | n/a | 39.1 | n/a | - |
| small ADBC c8 p50 | ms | n/a | 62.4 | n/a | - |
| small ADBC c8 p95 | ms | n/a | 166.4 | n/a | - |
| small ADBC c8 p99 | ms | n/a | 220.3 | n/a | - |
| small ADBC c32 p50 | ms | n/a | 243.8 | n/a | - |
| small ADBC c32 p95 | ms | n/a | 708.6 | n/a | - |
| small ADBC c32 p99 | ms | n/a | 824.9 | n/a | - |
| server RSS peak | MB | 252.0 | 794.0 | 3.15 | 3.21 3.23 3.15 |

Correctness gate: A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point).

### fu-small-s3: A = 6f0aa5a026fa `-`, B = 6f0aa5a026fa `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 31.0 | 24.0 | 0.78 | 0.85 0.78 0.85 |
| small JDBC c1 p95 | ms | 561.1 | 45.0 | 0.08 | 0.08 0.08 0.08 |
| small JDBC c1 p99 | ms | 671.6 | 55.4 | 0.08 | 0.08 0.10 0.08 |
| small JDBC c8 p50 | ms | 264.3 | 72.1 | 0.27 | 0.25 0.27 0.33 |
| small JDBC c8 p95 | ms | 3507.3 | 175.0 | 0.05 | 0.05 0.05 0.05 |
| small JDBC c8 p99 | ms | 3755.5 | 225.9 | 0.06 | 0.07 0.06 0.05 |
| small JDBC c32 p50 | ms | 963.0 | 196.3 | 0.20 | 0.20 0.21 0.21 |
| small JDBC c32 p95 | ms | 12362.4 | 796.6 | 0.06 | 0.06 0.06 0.06 |
| small JDBC c32 p99 | ms | 13837.3 | 926.5 | 0.07 | 0.07 0.07 0.07 |
| small ADBC c1 p50 | ms | 24.2 | 12.4 | 0.51 | 0.51 0.51 0.54 |
| small ADBC c1 p95 | ms | 598.6 | 32.4 | 0.05 | 0.06 0.05 0.05 |
| small ADBC c1 p99 | ms | 728.6 | 42.7 | 0.06 | 0.06 0.06 0.06 |
| small ADBC c8 p50 | ms | 252.0 | 54.5 | 0.22 | 0.20 0.20 0.24 |
| small ADBC c8 p95 | ms | 3439.1 | 163.6 | 0.05 | 0.05 0.05 0.05 |
| small ADBC c8 p99 | ms | 3830.6 | 228.2 | 0.06 | 0.06 0.05 0.06 |
| small ADBC c32 p50 | ms | 918.5 | 175.7 | 0.19 | 0.20 0.19 0.19 |
| small ADBC c32 p95 | ms | 12991.2 | 788.0 | 0.06 | 0.05 0.06 0.06 |
| small ADBC c32 p99 | ms | 22381.5 | 942.9 | 0.04 | 0.04 0.06 0.03 |
| server RSS peak | MB | 2327.0 | 1515.0 | 0.65 | 0.65 0.65 0.67 |

### fu-small-s3-vs-up-native: A = up-native `-`, B = 6f0aa5a026fa `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | n/a | 24.0 | n/a | - |
| small JDBC c1 p95 | ms | n/a | 45.0 | n/a | - |
| small JDBC c1 p99 | ms | n/a | 55.4 | n/a | - |
| small JDBC c8 p50 | ms | n/a | 72.1 | n/a | - |
| small JDBC c8 p95 | ms | n/a | 175.0 | n/a | - |
| small JDBC c8 p99 | ms | n/a | 225.9 | n/a | - |
| small JDBC c32 p50 | ms | n/a | 196.3 | n/a | - |
| small JDBC c32 p95 | ms | n/a | 796.6 | n/a | - |
| small JDBC c32 p99 | ms | n/a | 926.5 | n/a | - |
| small ADBC c1 p50 | ms | n/a | 12.4 | n/a | - |
| small ADBC c1 p95 | ms | n/a | 32.4 | n/a | - |
| small ADBC c1 p99 | ms | n/a | 42.7 | n/a | - |
| small ADBC c8 p50 | ms | n/a | 54.5 | n/a | - |
| small ADBC c8 p95 | ms | n/a | 163.6 | n/a | - |
| small ADBC c8 p99 | ms | n/a | 228.2 | n/a | - |
| small ADBC c32 p50 | ms | n/a | 175.7 | n/a | - |
| small ADBC c32 p95 | ms | n/a | 788.0 | n/a | - |
| small ADBC c32 p99 | ms | n/a | 942.9 | n/a | - |
| server RSS peak | MB | 394.0 | 1515.0 | 3.85 | 3.68 3.88 3.80 |

Correctness gate: A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-adbc8 (640/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc8 (425/640 errors; 456/640 errors; 527/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point).

### fu-tpch-local: A = 6f0aa5a026fa `-`, B = 6f0aa5a026fa `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 4.2 | 4.3 | 1.03 | 1.08 0.97 0.92 |
| TPC-H SF10 ADBC (sum of medians) | s | 42.8 | 41.9 | 0.98 | 1.03 1.00 0.89 |
| TPC-H SF1 JDBC (sum of medians) | s | 4.3 | 4.4 | 1.03 | 1.07 1.02 0.96 |
| TPC-H SF10 JDBC (sum of medians) | s | 44.4 | 42.0 | 0.95 | 1.05 0.92 0.90 |
| server RSS peak | MB | 1564.0 | 1742.0 | 1.11 | 1.06 1.07 1.16 |

### fu-tpch-local-vs-up-native: A = up-native `-`, B = 6f0aa5a026fa `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | n/a | 4.3 | n/a | - |
| TPC-H SF10 ADBC (sum of medians) | s | n/a | 41.9 | n/a | - |
| TPC-H SF1 JDBC (sum of medians) | s | n/a | 4.4 | n/a | - |
| TPC-H SF10 JDBC (sum of medians) | s | n/a | 42.0 | n/a | - |
| server RSS peak | MB | 358.0 | 1742.0 | 4.87 | 5.03 4.62 5.07 |

Correctness gate: A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)), jdbc10 (md5 50bb2801381f (1/22 ok)).

### fu-zstd-netem-local: A = 6f0aa5a026fa `CZSTD`, B = 6f0aa5a026fa `-DresourceProfile=speed CZSTD`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 1525.0 | 1692.0 | 1.11 | 1.10 1.20 1.09 |

### fu-zstd-netem-local-vs-up-native: A = up-native `-DflightCompression=zstd`, B = 6f0aa5a026fa `-DresourceProfile=speed CZSTD`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 608.0 | 1692.0 | 2.78 | 2.79 3.00 2.71 |
