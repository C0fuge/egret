# Wave fresh-up-06d6468b17c5 (server comparison), run 44335959845

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

## Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| fu-load-local | 06d6468b17c5 `-` | 06d6468b17c5 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-load-local-vs-up-native | up-native `-` | 06d6468b17c5 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-scan-local | 06d6468b17c5 `-` | 06d6468b17c5 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.03 | none |
| fu-scan-local-vs-up-native | up-native `-` | 06d6468b17c5 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.06 | none |
| fu-scan-s3 | 06d6468b17c5 `-` | 06d6468b17c5 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU Intel(R) Xeon(R) 6975P-C | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.12 | none |
| fu-scan-s3-vs-up-native | up-native `-` | 06d6468b17c5 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU Intel(R) Xeon(R) 6975P-C | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.10 | none |
| fu-sf1-s3 | 06d6468b17c5 `-` | 06d6468b17c5 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 0.11 | n/a | n/a | n/a | none |
| fu-sf1-s3-vs-up-native | up-native `-` | 06d6468b17c5 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)) |
| fu-sf10adbc-s3 | 06d6468b17c5 `-` | 06d6468b17c5 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | 0.13 | n/a | n/a | none |
| fu-sf10adbc-s3-vs-up-native | up-native `-` | 06d6468b17c5 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22) |
| fu-sf10jdbc-s3 | 06d6468b17c5 `-` | 06d6468b17c5 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | 0.11 | n/a | none |
| fu-sf10jdbc-s3-vs-up-native | up-native `-` | 06d6468b17c5 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: jdbc10 (md5 50bb2801381f (1/22 ok)) |
| fu-small-local | 06d6468b17c5 `-` | 06d6468b17c5 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | 1.34 | 1.02 | 1.19 | 1.03 | n/a | n/a | n/a | n/a | none |
| fu-small-local-vs-up-native | up-native `-` | 06d6468b17c5 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point) |
| fu-small-s3 | 06d6468b17c5 `-` | 06d6468b17c5 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | 0.44 | 0.03 | 0.81 | 0.03 | n/a | n/a | n/a | n/a | none |
| fu-small-s3-vs-up-native | up-native `-` | 06d6468b17c5 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-adbc8 (640/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc8 (344/640 errors; 363/640 errors; 446/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point) |
| fu-tpch-local | 06d6468b17c5 `-` | 06d6468b17c5 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 1.05 | 0.96 | 0.97 | n/a | none |
| fu-tpch-local-vs-up-native | up-native `-` | 06d6468b17c5 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)), jdbc10 (md5 50bb2801381f (1/22 ok)) |
| fu-zstd-netem-local | 06d6468b17c5 `CZSTD` | 06d6468b17c5 `-DresourceProfile=speed CZSTD` | local | Linux ubuntu26 4 vCPU Intel(R) Xeon(R) 6975P-C | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-zstd-netem-local-vs-up-native | up-native `-DflightCompression=zstd` | 06d6468b17c5 `-DresourceProfile=speed CZSTD` | local | Linux ubuntu26 4 vCPU Intel(R) Xeon(R) 6975P-C | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |

## Per job (absolute medians and ratios)

### fu-load-local: A = 06d6468b17c5 `-`, B = 06d6468b17c5 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 810.0 | 929.0 | 1.15 | 1.10 1.10 1.17 |

### fu-load-local-vs-up-native: A = up-native `-`, B = 06d6468b17c5 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 1006.0 | 929.0 | 0.92 | 0.89 0.93 0.91 |

### fu-scan-local: A = 06d6468b17c5 `-`, B = 06d6468b17c5 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 435.8 | 449.6 | 1.03 | 1.02 1.05 1.04 |
| lineitem scan x4 | MB/s | 525.6 | 612.6 | 1.17 | 1.17 1.14 1.17 |
| lineitem scan x8 | MB/s | 549.9 | 626.4 | 1.14 | 1.13 1.14 1.14 |
| lineitem export ADBC | MB/s | 502.6 | 540.7 | 1.08 | 1.07 1.08 1.08 |
| server RSS peak | MB | 939.0 | 1127.0 | 1.20 | 1.16 1.20 1.25 |

### fu-scan-local-vs-up-native: A = up-native `-`, B = 06d6468b17c5 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 423.2 | 449.6 | 1.06 | 1.06 1.09 1.06 |
| lineitem scan x4 | MB/s | 554.5 | 612.6 | 1.10 | 1.10 1.10 1.08 |
| lineitem scan x8 | MB/s | 571.9 | 626.4 | 1.10 | 1.10 1.09 1.09 |
| lineitem export ADBC | MB/s | 511.5 | 540.7 | 1.06 | 1.17 1.06 1.06 |
| server RSS peak | MB | 1764.0 | 1127.0 | 0.64 | 0.63 0.64 0.65 |

### fu-scan-s3: A = 06d6468b17c5 `-`, B = 06d6468b17c5 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU Intel(R) Xeon(R) 6975P-C. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 462.5 | 516.1 | 1.12 | 1.09 1.19 1.10 |
| lineitem scan x4 | MB/s | 699.7 | 872.9 | 1.25 | 1.23 1.27 1.23 |
| lineitem scan x8 | MB/s | 726.2 | 886.8 | 1.22 | 1.22 1.23 1.31 |
| lineitem export ADBC | MB/s | 545.5 | 750.0 | 1.37 | 1.31 1.38 1.41 |
| server RSS peak | MB | 1221.0 | 3311.0 | 2.71 | 2.78 2.02 2.71 |

### fu-scan-s3-vs-up-native: A = up-native `-`, B = 06d6468b17c5 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU Intel(R) Xeon(R) 6975P-C. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 467.1 | 516.1 | 1.10 | 1.10 1.14 1.07 |
| lineitem scan x4 | MB/s | 819.0 | 872.9 | 1.07 | 1.07 1.09 1.05 |
| lineitem scan x8 | MB/s | 817.2 | 886.8 | 1.09 | 1.09 1.13 1.08 |
| lineitem export ADBC | MB/s | 658.5 | 750.0 | 1.14 | 1.10 1.17 1.14 |
| server RSS peak | MB | 4277.0 | 3311.0 | 0.77 | 0.77 0.77 0.78 |

### fu-sf1-s3: A = 06d6468b17c5 `-`, B = 06d6468b17c5 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 29.4 | 3.3 | 0.11 | 0.10 0.12 0.11 |
| TPC-H SF1 JDBC (sum of medians) | s | 31.4 | 3.5 | 0.11 | 0.10 0.11 0.13 |
| server RSS peak | MB | 760.0 | 957.0 | 1.26 | 1.26 1.24 1.35 |

### fu-sf1-s3-vs-up-native: A = up-native `-`, B = 06d6468b17c5 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | n/a | 3.3 | n/a | - |
| TPC-H SF1 JDBC (sum of medians) | s | n/a | 3.5 | n/a | - |
| server RSS peak | MB | 579.0 | 957.0 | 1.65 | 1.65 1.64 1.58 |

Correctness gate: A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)).

### fu-sf10adbc-s3: A = 06d6468b17c5 `-`, B = 06d6468b17c5 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | 283.5 | 38.1 | 0.13 | 0.14 0.13 0.12 |
| server RSS peak | MB | 1695.0 | 3423.0 | 2.02 | 1.68 2.29 2.02 |

### fu-sf10adbc-s3-vs-up-native: A = up-native `-`, B = 06d6468b17c5 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | n/a | 38.1 | n/a | - |
| server RSS peak | MB | 1012.0 | 3423.0 | 3.38 | 3.40 3.52 3.23 |

Correctness gate: A: adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22).

### fu-sf10jdbc-s3: A = 06d6468b17c5 `-`, B = 06d6468b17c5 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `sf10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 JDBC (sum of medians) | s | 304.7 | 32.1 | 0.11 | 0.10 0.11 0.11 |
| server RSS peak | MB | 1497.0 | 3363.0 | 2.25 | 2.34 2.24 2.16 |

### fu-sf10jdbc-s3-vs-up-native: A = up-native `-`, B = 06d6468b17c5 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `sf10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 JDBC (sum of medians) | s | n/a | 32.1 | n/a | - |
| server RSS peak | MB | 1008.0 | 3363.0 | 3.34 | 3.53 3.17 3.34 |

Correctness gate: A: jdbc10 (md5 50bb2801381f (1/22 ok)).

### fu-small-local: A = 06d6468b17c5 `-`, B = 06d6468b17c5 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 22.4 | 26.6 | 1.19 | 1.13 1.22 1.14 |
| small JDBC c1 p95 | ms | 44.7 | 49.3 | 1.10 | 1.05 1.20 1.05 |
| small JDBC c1 p99 | ms | 49.9 | 59.6 | 1.19 | 1.17 1.20 1.04 |
| small JDBC c8 p50 | ms | 75.7 | 106.1 | 1.40 | 1.42 1.42 1.32 |
| small JDBC c8 p95 | ms | 302.2 | 285.2 | 0.94 | 0.94 0.92 0.95 |
| small JDBC c8 p99 | ms | 351.9 | 368.2 | 1.05 | 1.03 1.08 1.06 |
| small JDBC c32 p50 | ms | 248.9 | 407.7 | 1.64 | 1.59 1.69 1.53 |
| small JDBC c32 p95 | ms | 1122.1 | 1152.7 | 1.03 | 1.05 0.99 1.03 |
| small JDBC c32 p99 | ms | 1265.1 | 1390.9 | 1.10 | 1.17 1.06 1.10 |
| small ADBC c1 p50 | ms | 15.1 | 20.3 | 1.34 | 1.32 1.29 1.35 |
| small ADBC c1 p95 | ms | 48.5 | 48.4 | 1.00 | 1.00 1.03 0.88 |
| small ADBC c1 p99 | ms | 65.0 | 61.7 | 0.95 | 1.22 0.94 0.90 |
| small ADBC c8 p50 | ms | 67.4 | 95.7 | 1.42 | 1.28 1.45 1.48 |
| small ADBC c8 p95 | ms | 306.9 | 277.1 | 0.90 | 0.88 0.88 0.96 |
| small ADBC c8 p99 | ms | 369.7 | 363.2 | 0.98 | 0.98 0.96 1.01 |
| small ADBC c32 p50 | ms | 234.7 | 351.3 | 1.50 | 1.48 1.53 1.54 |
| small ADBC c32 p95 | ms | 1117.7 | 1134.7 | 1.02 | 1.01 1.02 1.03 |
| small ADBC c32 p99 | ms | 1251.3 | 1301.2 | 1.04 | 1.02 1.04 1.07 |
| server RSS peak | MB | 678.0 | 820.0 | 1.21 | 1.22 1.21 1.24 |

### fu-small-local-vs-up-native: A = up-native `-`, B = 06d6468b17c5 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | n/a | 26.6 | n/a | - |
| small JDBC c1 p95 | ms | n/a | 49.3 | n/a | - |
| small JDBC c1 p99 | ms | n/a | 59.6 | n/a | - |
| small JDBC c8 p50 | ms | n/a | 106.1 | n/a | - |
| small JDBC c8 p95 | ms | n/a | 285.2 | n/a | - |
| small JDBC c8 p99 | ms | n/a | 368.2 | n/a | - |
| small JDBC c32 p50 | ms | n/a | 407.7 | n/a | - |
| small JDBC c32 p95 | ms | n/a | 1152.7 | n/a | - |
| small JDBC c32 p99 | ms | n/a | 1390.9 | n/a | - |
| small ADBC c1 p50 | ms | n/a | 20.3 | n/a | - |
| small ADBC c1 p95 | ms | n/a | 48.4 | n/a | - |
| small ADBC c1 p99 | ms | n/a | 61.7 | n/a | - |
| small ADBC c8 p50 | ms | n/a | 95.7 | n/a | - |
| small ADBC c8 p95 | ms | n/a | 277.1 | n/a | - |
| small ADBC c8 p99 | ms | n/a | 363.2 | n/a | - |
| small ADBC c32 p50 | ms | n/a | 351.3 | n/a | - |
| small ADBC c32 p95 | ms | n/a | 1134.7 | n/a | - |
| small ADBC c32 p99 | ms | n/a | 1301.2 | n/a | - |
| server RSS peak | MB | 247.0 | 820.0 | 3.32 | 3.35 3.28 3.27 |

Correctness gate: A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point).

### fu-small-s3: A = 06d6468b17c5 `-`, B = 06d6468b17c5 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 23.3 | 18.9 | 0.81 | 0.77 0.82 0.80 |
| small JDBC c1 p95 | ms | 703.8 | 34.1 | 0.05 | 0.04 0.05 0.05 |
| small JDBC c1 p99 | ms | 773.7 | 41.1 | 0.05 | 0.05 0.05 0.05 |
| small JDBC c8 p50 | ms | 133.9 | 53.9 | 0.40 | 0.40 0.38 0.44 |
| small JDBC c8 p95 | ms | 5466.7 | 122.6 | 0.02 | 0.02 0.02 0.02 |
| small JDBC c8 p99 | ms | 5864.7 | 153.6 | 0.03 | 0.03 0.03 0.03 |
| small JDBC c32 p50 | ms | 428.5 | 153.4 | 0.36 | 0.35 0.35 0.37 |
| small JDBC c32 p95 | ms | 17388.5 | 584.1 | 0.03 | 0.03 0.03 0.03 |
| small JDBC c32 p99 | ms | 18908.3 | 692.1 | 0.04 | 0.04 0.04 0.04 |
| small ADBC c1 p50 | ms | 19.0 | 8.4 | 0.44 | 0.42 0.43 0.58 |
| small ADBC c1 p95 | ms | 712.8 | 23.6 | 0.03 | 0.04 0.03 0.03 |
| small ADBC c1 p99 | ms | 806.6 | 27.8 | 0.03 | 0.04 0.03 0.03 |
| small ADBC c8 p50 | ms | 131.2 | 40.7 | 0.31 | 0.30 0.31 0.31 |
| small ADBC c8 p95 | ms | 5447.1 | 121.0 | 0.02 | 0.02 0.02 0.02 |
| small ADBC c8 p99 | ms | 5909.2 | 150.4 | 0.03 | 0.03 0.03 0.03 |
| small ADBC c32 p50 | ms | 432.2 | 129.8 | 0.30 | 0.30 0.31 0.30 |
| small ADBC c32 p95 | ms | 17409.0 | 565.5 | 0.03 | 0.03 0.03 0.03 |
| small ADBC c32 p99 | ms | 19209.1 | 679.2 | 0.04 | 0.04 0.04 0.04 |
| server RSS peak | MB | 792.0 | 1497.0 | 1.89 | 2.02 1.88 1.87 |

### fu-small-s3-vs-up-native: A = up-native `-`, B = 06d6468b17c5 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | n/a | 18.9 | n/a | - |
| small JDBC c1 p95 | ms | n/a | 34.1 | n/a | - |
| small JDBC c1 p99 | ms | n/a | 41.1 | n/a | - |
| small JDBC c8 p50 | ms | n/a | 53.9 | n/a | - |
| small JDBC c8 p95 | ms | n/a | 122.6 | n/a | - |
| small JDBC c8 p99 | ms | n/a | 153.6 | n/a | - |
| small JDBC c32 p50 | ms | n/a | 153.4 | n/a | - |
| small JDBC c32 p95 | ms | n/a | 584.1 | n/a | - |
| small JDBC c32 p99 | ms | n/a | 692.1 | n/a | - |
| small ADBC c1 p50 | ms | n/a | 8.4 | n/a | - |
| small ADBC c1 p95 | ms | n/a | 23.6 | n/a | - |
| small ADBC c1 p99 | ms | n/a | 27.8 | n/a | - |
| small ADBC c8 p50 | ms | n/a | 40.7 | n/a | - |
| small ADBC c8 p95 | ms | n/a | 121.0 | n/a | - |
| small ADBC c8 p99 | ms | n/a | 150.4 | n/a | - |
| small ADBC c32 p50 | ms | n/a | 129.8 | n/a | - |
| small ADBC c32 p95 | ms | n/a | 565.5 | n/a | - |
| small ADBC c32 p99 | ms | n/a | 679.2 | n/a | - |
| server RSS peak | MB | 399.0 | 1497.0 | 3.75 | 3.85 3.74 3.78 |

Correctness gate: A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-adbc8 (640/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc8 (344/640 errors; 363/640 errors; 446/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point).

### fu-tpch-local: A = 06d6468b17c5 `-`, B = 06d6468b17c5 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 3.2 | 3.3 | 1.05 | 1.08 1.03 1.04 |
| TPC-H SF10 ADBC (sum of medians) | s | 34.6 | 33.2 | 0.96 | 0.96 0.94 0.96 |
| TPC-H SF1 JDBC (sum of medians) | s | 3.3 | 3.4 | 1.03 | 1.03 0.98 1.05 |
| TPC-H SF10 JDBC (sum of medians) | s | 34.6 | 33.4 | 0.97 | 1.00 0.94 0.99 |
| server RSS peak | MB | 1647.0 | 1773.0 | 1.08 | 0.89 1.07 1.22 |

### fu-tpch-local-vs-up-native: A = up-native `-`, B = 06d6468b17c5 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | n/a | 3.3 | n/a | - |
| TPC-H SF10 ADBC (sum of medians) | s | n/a | 33.2 | n/a | - |
| TPC-H SF1 JDBC (sum of medians) | s | n/a | 3.4 | n/a | - |
| TPC-H SF10 JDBC (sum of medians) | s | n/a | 33.4 | n/a | - |
| server RSS peak | MB | 357.0 | 1773.0 | 4.97 | 4.97 5.01 5.08 |

Correctness gate: A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)), jdbc10 (md5 50bb2801381f (1/22 ok)).

### fu-zstd-netem-local: A = 06d6468b17c5 `CZSTD`, B = 06d6468b17c5 `-DresourceProfile=speed CZSTD`, local

Runner: Linux ubuntu26 4 vCPU Intel(R) Xeon(R) 6975P-C. Workloads: `netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 1499.0 | 1663.0 | 1.11 | 1.10 1.10 1.15 |

### fu-zstd-netem-local-vs-up-native: A = up-native `-DflightCompression=zstd`, B = 06d6468b17c5 `-DresourceProfile=speed CZSTD`, local

Runner: Linux ubuntu26 4 vCPU Intel(R) Xeon(R) 6975P-C. Workloads: `netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 609.0 | 1663.0 | 2.73 | 2.65 2.74 2.83 |
