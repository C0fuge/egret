# Wave fresh-up-deafc861cce3 (server comparison), run 42223833724

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

## Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| fu-load-local | deafc861cce3 `-` | deafc861cce3 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-load-local-vs-up-native | up-native `-` | deafc861cce3 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-scan-local | deafc861cce3 `-` | deafc861cce3 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 0.98 | none |
| fu-scan-local-vs-up-native | up-native `-` | deafc861cce3 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.02 | A: scan8 (rows=370512532 errors=3; rows=385147672 errors=2) |
| fu-scan-s3 | deafc861cce3 `-` | deafc861cce3 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.08 | none |
| fu-scan-s3-vs-up-native | up-native `-` | deafc861cce3 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.10 | none |
| fu-sf1-s3 | deafc861cce3 `-` | deafc861cce3 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 0.18 | n/a | n/a | n/a | none |
| fu-sf1-s3-vs-up-native | up-native `-` | deafc861cce3 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)) |
| fu-sf10adbc-s3 | deafc861cce3 `-` | deafc861cce3 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | 0.16 | n/a | n/a | none |
| fu-sf10adbc-s3-vs-up-native | up-native `-` | deafc861cce3 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22) |
| fu-sf10jdbc-s3 | deafc861cce3 `-` | deafc861cce3 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | 0.15 | n/a | none |
| fu-sf10jdbc-s3-vs-up-native | up-native `-` | deafc861cce3 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: jdbc10 (md5 50bb2801381f (1/22 ok)) |
| fu-small-local | deafc861cce3 `-` | deafc861cce3 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | 1.08 | 0.78 | 1.10 | 0.84 | n/a | n/a | n/a | n/a | none |
| fu-small-local-vs-up-native | up-native `-` | deafc861cce3 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point) |
| fu-small-s3 | deafc861cce3 `-` | deafc861cce3 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | 0.59 | 0.05 | 0.91 | 0.05 | n/a | n/a | n/a | n/a | none |
| fu-small-s3-vs-up-native | up-native `-` | deafc861cce3 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-adbc8 (640/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc8 (291/640 errors; 581/640 errors; 605/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point) |
| fu-tpch-local | deafc861cce3 `-` | deafc861cce3 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 1.01 | 0.97 | 0.95 | n/a | none |
| fu-tpch-local-vs-up-native | up-native `-` | deafc861cce3 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)), jdbc10 (md5 50bb2801381f (1/22 ok)) |
| fu-zstd-netem-local | deafc861cce3 `CZSTD` | deafc861cce3 `-DresourceProfile=speed CZSTD` | local | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-zstd-netem-local-vs-up-native | up-native `-DflightCompression=zstd` | deafc861cce3 `-DresourceProfile=speed CZSTD` | local | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |

## Per job (absolute medians and ratios)

### fu-load-local: A = deafc861cce3 `-`, B = deafc861cce3 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 4491.0 | 961.0 | 0.21 | 0.22 0.22 0.19 |

### fu-load-local-vs-up-native: A = up-native `-`, B = deafc861cce3 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 923.0 | 961.0 | 1.04 | 0.92 1.04 0.95 |

### fu-scan-local: A = deafc861cce3 `-`, B = deafc861cce3 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 547.6 | 536.5 | 0.98 | 1.00 0.99 0.98 |
| lineitem scan x4 | MB/s | 549.8 | 713.8 | 1.30 | 1.28 1.30 1.30 |
| lineitem scan x8 | MB/s | 477.4 | 730.2 | 1.53 | 1.51 1.53 1.50 |
| lineitem export ADBC | MB/s | 630.0 | 646.3 | 1.03 | 1.03 1.00 1.03 |
| server RSS peak | MB | 1236.0 | 1140.0 | 0.92 | 0.89 0.92 0.98 |

### fu-scan-local-vs-up-native: A = up-native `-`, B = deafc861cce3 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 528.3 | 536.5 | 1.02 | 1.01 1.04 1.01 |
| lineitem scan x4 | MB/s | 672.7 | 713.8 | 1.06 | 1.04 1.06 1.03 |
| lineitem scan x8 | MB/s | n/a | 730.2 | n/a | - |
| lineitem export ADBC | MB/s | 650.3 | 646.3 | 0.99 | 0.99 0.98 1.00 |
| server RSS peak | MB | 3666.0 | 1140.0 | 0.31 | 0.30 0.31 0.31 |

Correctness gate: A: scan8 (rows=370512532 errors=3; rows=385147672 errors=2).

### fu-scan-s3: A = deafc861cce3 `-`, B = deafc861cce3 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 404.4 | 437.9 | 1.08 | 1.08 1.08 1.13 |
| lineitem scan x4 | MB/s | 481.9 | 719.9 | 1.49 | 1.46 1.49 1.49 |
| lineitem scan x8 | MB/s | 458.8 | 726.1 | 1.58 | 1.58 1.58 1.59 |
| lineitem export ADBC | MB/s | 421.1 | 567.0 | 1.35 | 1.30 1.36 1.35 |
| server RSS peak | MB | 1714.0 | 2967.0 | 1.73 | 1.73 1.72 1.75 |

### fu-scan-s3-vs-up-native: A = up-native `-`, B = deafc861cce3 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 396.3 | 437.9 | 1.10 | 1.10 1.10 1.12 |
| lineitem scan x4 | MB/s | 639.9 | 719.9 | 1.13 | 1.16 1.11 1.13 |
| lineitem scan x8 | MB/s | 632.9 | 726.1 | 1.15 | 1.17 1.16 1.11 |
| lineitem export ADBC | MB/s | 622.2 | 567.0 | 0.91 | 0.88 0.96 0.91 |
| server RSS peak | MB | 4009.0 | 2967.0 | 0.74 | 0.72 0.74 0.75 |

### fu-sf1-s3: A = deafc861cce3 `-`, B = deafc861cce3 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 25.8 | 4.5 | 0.18 | 0.18 0.16 0.17 |
| TPC-H SF1 JDBC (sum of medians) | s | 25.8 | 4.5 | 0.18 | 0.18 0.17 0.18 |
| server RSS peak | MB | 738.0 | 912.0 | 1.24 | 1.29 1.26 1.13 |

### fu-sf1-s3-vs-up-native: A = up-native `-`, B = deafc861cce3 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | n/a | 4.5 | n/a | - |
| TPC-H SF1 JDBC (sum of medians) | s | n/a | 4.5 | n/a | - |
| server RSS peak | MB | 608.0 | 912.0 | 1.50 | 1.61 1.50 1.32 |

Correctness gate: A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)).

### fu-sf10adbc-s3: A = deafc861cce3 `-`, B = deafc861cce3 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | 264.5 | 41.6 | 0.16 | 0.21 0.16 0.14 |
| server RSS peak | MB | 1589.0 | 3040.0 | 1.91 | 1.92 1.90 1.90 |

### fu-sf10adbc-s3-vs-up-native: A = up-native `-`, B = deafc861cce3 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | n/a | 41.6 | n/a | - |
| server RSS peak | MB | 988.0 | 3040.0 | 3.08 | 3.08 3.06 2.99 |

Correctness gate: A: adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22).

### fu-sf10jdbc-s3: A = deafc861cce3 `-`, B = deafc861cce3 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C. Workloads: `sf10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 JDBC (sum of medians) | s | 421.4 | 64.2 | 0.15 | 0.14 0.15 0.15 |
| server RSS peak | MB | 1563.0 | 3066.0 | 1.96 | 1.95 1.95 2.03 |

### fu-sf10jdbc-s3-vs-up-native: A = up-native `-`, B = deafc861cce3 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C. Workloads: `sf10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 JDBC (sum of medians) | s | n/a | 64.2 | n/a | - |
| server RSS peak | MB | 975.0 | 3066.0 | 3.14 | 3.15 2.98 3.26 |

Correctness gate: A: jdbc10 (md5 50bb2801381f (1/22 ok)).

### fu-small-local: A = deafc861cce3 `-`, B = deafc861cce3 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 15.5 | 17.1 | 1.10 | 1.18 1.10 1.12 |
| small JDBC c1 p95 | ms | 33.9 | 31.0 | 0.91 | 0.99 0.91 0.92 |
| small JDBC c1 p99 | ms | 39.7 | 39.0 | 0.98 | 0.86 0.98 1.07 |
| small JDBC c8 p50 | ms | 74.7 | 73.4 | 0.98 | 0.95 0.86 1.02 |
| small JDBC c8 p95 | ms | 186.5 | 175.5 | 0.94 | 0.93 0.92 0.98 |
| small JDBC c8 p99 | ms | 230.4 | 213.1 | 0.92 | 0.95 0.88 0.92 |
| small JDBC c32 p50 | ms | 298.1 | 248.9 | 0.83 | 0.95 0.78 0.83 |
| small JDBC c32 p95 | ms | 830.4 | 694.0 | 0.84 | 0.84 0.83 0.86 |
| small JDBC c32 p99 | ms | 1058.7 | 836.3 | 0.79 | 0.81 0.79 0.77 |
| small ADBC c1 p50 | ms | 11.1 | 11.9 | 1.08 | 1.17 1.08 1.02 |
| small ADBC c1 p95 | ms | 27.6 | 26.9 | 0.98 | 0.99 0.91 1.05 |
| small ADBC c1 p99 | ms | 42.0 | 31.3 | 0.74 | 0.74 0.77 0.76 |
| small ADBC c8 p50 | ms | 66.8 | 62.1 | 0.93 | 0.94 0.95 0.93 |
| small ADBC c8 p95 | ms | 171.0 | 171.7 | 1.00 | 0.98 1.03 0.95 |
| small ADBC c8 p99 | ms | 211.3 | 213.0 | 1.01 | 1.03 1.00 0.84 |
| small ADBC c32 p50 | ms | 272.9 | 243.1 | 0.89 | 0.87 0.89 0.91 |
| small ADBC c32 p95 | ms | 903.0 | 702.3 | 0.78 | 0.87 0.75 0.79 |
| small ADBC c32 p99 | ms | 1214.2 | 815.8 | 0.67 | 0.80 0.68 0.62 |
| server RSS peak | MB | 1484.0 | 757.0 | 0.51 | 0.50 0.52 0.51 |

### fu-small-local-vs-up-native: A = up-native `-`, B = deafc861cce3 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | n/a | 17.1 | n/a | - |
| small JDBC c1 p95 | ms | n/a | 31.0 | n/a | - |
| small JDBC c1 p99 | ms | n/a | 39.0 | n/a | - |
| small JDBC c8 p50 | ms | n/a | 73.4 | n/a | - |
| small JDBC c8 p95 | ms | n/a | 175.5 | n/a | - |
| small JDBC c8 p99 | ms | n/a | 213.1 | n/a | - |
| small JDBC c32 p50 | ms | n/a | 248.9 | n/a | - |
| small JDBC c32 p95 | ms | n/a | 694.0 | n/a | - |
| small JDBC c32 p99 | ms | n/a | 836.3 | n/a | - |
| small ADBC c1 p50 | ms | n/a | 11.9 | n/a | - |
| small ADBC c1 p95 | ms | n/a | 26.9 | n/a | - |
| small ADBC c1 p99 | ms | n/a | 31.3 | n/a | - |
| small ADBC c8 p50 | ms | n/a | 62.1 | n/a | - |
| small ADBC c8 p95 | ms | n/a | 171.7 | n/a | - |
| small ADBC c8 p99 | ms | n/a | 213.0 | n/a | - |
| small ADBC c32 p50 | ms | n/a | 243.1 | n/a | - |
| small ADBC c32 p95 | ms | n/a | 702.3 | n/a | - |
| small ADBC c32 p99 | ms | n/a | 815.8 | n/a | - |
| server RSS peak | MB | 252.0 | 757.0 | 3.00 | 2.97 3.11 3.00 |

Correctness gate: A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point).

### fu-small-s3: A = deafc861cce3 `-`, B = deafc861cce3 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 27.0 | 24.5 | 0.91 | 0.84 0.87 0.91 |
| small JDBC c1 p95 | ms | 698.1 | 39.3 | 0.06 | 0.06 0.06 0.05 |
| small JDBC c1 p99 | ms | 767.3 | 47.2 | 0.06 | 0.06 0.06 0.06 |
| small JDBC c8 p50 | ms | 243.8 | 65.9 | 0.27 | 0.24 0.27 0.28 |
| small JDBC c8 p95 | ms | 3888.4 | 139.5 | 0.04 | 0.04 0.03 0.04 |
| small JDBC c8 p99 | ms | 4262.0 | 170.6 | 0.04 | 0.04 0.03 0.04 |
| small JDBC c32 p50 | ms | 945.9 | 178.5 | 0.19 | 0.17 0.20 0.20 |
| small JDBC c32 p95 | ms | 13000.4 | 638.2 | 0.05 | 0.05 0.05 0.05 |
| small JDBC c32 p99 | ms | 14293.5 | 759.5 | 0.05 | 0.05 0.05 0.03 |
| small ADBC c1 p50 | ms | 19.1 | 11.3 | 0.59 | 0.54 0.52 0.59 |
| small ADBC c1 p95 | ms | 696.0 | 28.1 | 0.04 | 0.04 0.04 0.04 |
| small ADBC c1 p99 | ms | 736.9 | 35.3 | 0.05 | 0.05 0.05 0.04 |
| small ADBC c8 p50 | ms | 257.8 | 46.7 | 0.18 | 0.16 0.18 0.21 |
| small ADBC c8 p95 | ms | 3846.1 | 129.2 | 0.03 | 0.03 0.03 0.03 |
| small ADBC c8 p99 | ms | 4127.2 | 168.3 | 0.04 | 0.04 0.04 0.04 |
| small ADBC c32 p50 | ms | 954.7 | 150.2 | 0.16 | 0.14 0.16 0.16 |
| small ADBC c32 p95 | ms | 13195.3 | 621.6 | 0.05 | 0.05 0.05 0.05 |
| small ADBC c32 p99 | ms | 14969.4 | 737.2 | 0.05 | 0.05 0.04 0.05 |
| server RSS peak | MB | 2227.0 | 1388.0 | 0.62 | 0.63 0.61 0.62 |

### fu-small-s3-vs-up-native: A = up-native `-`, B = deafc861cce3 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | n/a | 24.5 | n/a | - |
| small JDBC c1 p95 | ms | n/a | 39.3 | n/a | - |
| small JDBC c1 p99 | ms | n/a | 47.2 | n/a | - |
| small JDBC c8 p50 | ms | n/a | 65.9 | n/a | - |
| small JDBC c8 p95 | ms | n/a | 139.5 | n/a | - |
| small JDBC c8 p99 | ms | n/a | 170.6 | n/a | - |
| small JDBC c32 p50 | ms | n/a | 178.5 | n/a | - |
| small JDBC c32 p95 | ms | n/a | 638.2 | n/a | - |
| small JDBC c32 p99 | ms | n/a | 759.5 | n/a | - |
| small ADBC c1 p50 | ms | n/a | 11.3 | n/a | - |
| small ADBC c1 p95 | ms | n/a | 28.1 | n/a | - |
| small ADBC c1 p99 | ms | n/a | 35.3 | n/a | - |
| small ADBC c8 p50 | ms | n/a | 46.7 | n/a | - |
| small ADBC c8 p95 | ms | n/a | 129.2 | n/a | - |
| small ADBC c8 p99 | ms | n/a | 168.3 | n/a | - |
| small ADBC c32 p50 | ms | n/a | 150.2 | n/a | - |
| small ADBC c32 p95 | ms | n/a | 621.6 | n/a | - |
| small ADBC c32 p99 | ms | n/a | 737.2 | n/a | - |
| server RSS peak | MB | 402.0 | 1388.0 | 3.45 | 3.51 3.41 3.46 |

Correctness gate: A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-adbc8 (640/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc8 (291/640 errors; 581/640 errors; 605/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point).

### fu-tpch-local: A = deafc861cce3 `-`, B = deafc861cce3 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 4.0 | 4.0 | 1.01 | 1.01 1.01 0.99 |
| TPC-H SF10 ADBC (sum of medians) | s | 40.3 | 39.1 | 0.97 | 0.96 0.96 0.98 |
| TPC-H SF1 JDBC (sum of medians) | s | 4.0 | 4.0 | 1.00 | 1.00 1.00 1.00 |
| TPC-H SF10 JDBC (sum of medians) | s | 40.3 | 38.3 | 0.95 | 0.95 0.95 0.95 |
| server RSS peak | MB | 1591.0 | 1733.0 | 1.09 | 1.09 1.07 1.09 |

### fu-tpch-local-vs-up-native: A = up-native `-`, B = deafc861cce3 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | n/a | 4.0 | n/a | - |
| TPC-H SF10 ADBC (sum of medians) | s | n/a | 39.1 | n/a | - |
| TPC-H SF1 JDBC (sum of medians) | s | n/a | 4.0 | n/a | - |
| TPC-H SF10 JDBC (sum of medians) | s | n/a | 38.3 | n/a | - |
| server RSS peak | MB | 357.0 | 1733.0 | 4.85 | 4.75 4.68 4.98 |

Correctness gate: A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)), jdbc10 (md5 50bb2801381f (1/22 ok)).

### fu-zstd-netem-local: A = deafc861cce3 `CZSTD`, B = deafc861cce3 `-DresourceProfile=speed CZSTD`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 1549.0 | 1720.0 | 1.11 | 1.15 1.03 1.11 |

### fu-zstd-netem-local-vs-up-native: A = up-native `-DflightCompression=zstd`, B = deafc861cce3 `-DresourceProfile=speed CZSTD`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 607.0 | 1720.0 | 2.83 | 2.86 2.63 2.81 |
