# Wave fresh-up-f06b5834e76e (server comparison), run 41437099791

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

## Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| fu-load-local | f06b5834e76e `-` | f06b5834e76e `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-load-local-vs-up-native | up-native `-` | f06b5834e76e `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-scan-local | f06b5834e76e `-` | f06b5834e76e `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.03 | none |
| fu-scan-local-vs-up-native | up-native `-` | f06b5834e76e `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.09 | A: scan8 (rows=221573516 errors=5; rows=331190932 errors=3; rows=381084440 errors=2) |
| fu-scan-s3 | f06b5834e76e `-` | f06b5834e76e `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.04 | none |
| fu-scan-s3-vs-up-native | up-native `-` | f06b5834e76e `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.04 | A: scan8 (rows=456602524 errors=1) |
| fu-sf1-s3 | f06b5834e76e `-` | f06b5834e76e `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 1.00 | n/a | n/a | n/a | none |
| fu-sf1-s3-vs-up-native | up-native `-` | f06b5834e76e `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)) |
| fu-sf10adbc-s3 | f06b5834e76e `-` | f06b5834e76e `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | 0.66 | n/a | n/a | none |
| fu-sf10adbc-s3-vs-up-native | up-native `-` | f06b5834e76e `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22) |
| fu-sf10jdbc-s3 | f06b5834e76e `-` | f06b5834e76e `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | 0.68 | n/a | none |
| fu-sf10jdbc-s3-vs-up-native | up-native `-` | f06b5834e76e `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: jdbc10 (md5 50bb2801381f (1/22 ok)) |
| fu-small-local | f06b5834e76e `-` | f06b5834e76e `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | 1.12 | 0.87 | 1.08 | 0.87 | n/a | n/a | n/a | n/a | none |
| fu-small-local-vs-up-native | up-native `-` | f06b5834e76e `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point) |
| fu-small-s3 | f06b5834e76e `-` | f06b5834e76e `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | 1.01 | 1.39 | 1.04 | 1.42 | n/a | n/a | n/a | n/a | none |
| fu-small-s3-vs-up-native | up-native `-` | f06b5834e76e `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-adbc8 (640/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc8 (387/640 errors; 487/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point) |
| fu-tpch-local | f06b5834e76e `-` | f06b5834e76e `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C | 3/3 | n/a | n/a | n/a | n/a | 1.00 | 0.94 | 0.96 | n/a | none |
| fu-tpch-local-vs-up-native | up-native `-` | f06b5834e76e `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)), jdbc10 (md5 50bb2801381f (1/22 ok)) |
| fu-zstd-netem-local | f06b5834e76e `CZSTD` | f06b5834e76e `-DresourceProfile=speed CZSTD` | local | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-zstd-netem-local-vs-up-native | up-native `-DflightCompression=zstd` | f06b5834e76e `-DresourceProfile=speed CZSTD` | local | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |

## Per job (absolute medians and ratios)

### fu-load-local: A = f06b5834e76e `-`, B = f06b5834e76e `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 4536.0 | 830.0 | 0.18 | 0.19 0.18 0.18 |

### fu-load-local-vs-up-native: A = up-native `-`, B = f06b5834e76e `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 946.0 | 830.0 | 0.88 | 0.92 0.67 0.88 |

### fu-scan-local: A = f06b5834e76e `-`, B = f06b5834e76e `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 557.9 | 576.3 | 1.03 | 1.05 1.03 1.03 |
| lineitem scan x4 | MB/s | 568.3 | 624.3 | 1.10 | 1.08 1.10 1.13 |
| lineitem scan x8 | MB/s | 485.3 | 647.6 | 1.33 | 1.33 1.35 1.33 |
| lineitem export ADBC | MB/s | 641.5 | 669.1 | 1.04 | 1.03 1.04 1.05 |
| server RSS peak | MB | 1184.0 | 1073.0 | 0.91 | 0.82 0.92 0.92 |

### fu-scan-local-vs-up-native: A = up-native `-`, B = f06b5834e76e `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 526.8 | 576.3 | 1.09 | 1.09 1.10 1.09 |
| lineitem scan x4 | MB/s | 695.4 | 624.3 | 0.90 | 0.89 0.88 0.92 |
| lineitem scan x8 | MB/s | n/a | 647.6 | n/a | - |
| lineitem export ADBC | MB/s | 646.0 | 669.1 | 1.04 | 1.16 1.02 1.04 |
| server RSS peak | MB | 3665.0 | 1073.0 | 0.29 | 0.29 0.29 0.30 |

Correctness gate: A: scan8 (rows=221573516 errors=5; rows=331190932 errors=3; rows=381084440 errors=2).

### fu-scan-s3: A = f06b5834e76e `-`, B = f06b5834e76e `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 389.8 | 403.7 | 1.04 | 1.02 1.08 1.04 |
| lineitem scan x4 | MB/s | 462.4 | 486.0 | 1.05 | 1.05 1.06 1.05 |
| lineitem scan x8 | MB/s | 438.8 | 501.7 | 1.14 | 1.15 1.16 1.14 |
| lineitem export ADBC | MB/s | 417.4 | 435.4 | 1.04 | 1.05 1.15 1.03 |
| server RSS peak | MB | 1699.0 | 1409.0 | 0.83 | 0.83 0.82 0.84 |

### fu-scan-s3-vs-up-native: A = up-native `-`, B = f06b5834e76e `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 388.9 | 403.7 | 1.04 | 1.01 1.04 1.05 |
| lineitem scan x4 | MB/s | 608.6 | 486.0 | 0.80 | 0.80 0.75 0.80 |
| lineitem scan x8 | MB/s | n/a | 501.7 | n/a | - |
| lineitem export ADBC | MB/s | 568.7 | 435.4 | 0.77 | 0.76 0.85 0.99 |
| server RSS peak | MB | 5784.0 | 1409.0 | 0.24 | 0.24 0.25 0.25 |

Correctness gate: A: scan8 (rows=456602524 errors=1).

### fu-sf1-s3: A = f06b5834e76e `-`, B = f06b5834e76e `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 23.8 | 23.7 | 1.00 | 0.99 0.99 1.01 |
| TPC-H SF1 JDBC (sum of medians) | s | 23.6 | 23.7 | 1.01 | 1.00 1.00 1.03 |
| server RSS peak | MB | 752.0 | 737.0 | 0.98 | 0.93 0.93 1.09 |

### fu-sf1-s3-vs-up-native: A = up-native `-`, B = f06b5834e76e `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | n/a | 23.7 | n/a | - |
| TPC-H SF1 JDBC (sum of medians) | s | n/a | 23.7 | n/a | - |
| server RSS peak | MB | 619.0 | 737.0 | 1.19 | 1.19 1.16 1.21 |

Correctness gate: A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)).

### fu-sf10adbc-s3: A = f06b5834e76e `-`, B = f06b5834e76e `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | 446.4 | 295.3 | 0.66 | 1.00 0.66 0.99 |
| server RSS peak | MB | 1552.0 | 1785.0 | 1.15 | 1.07 1.16 1.13 |

### fu-sf10adbc-s3-vs-up-native: A = up-native `-`, B = f06b5834e76e `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | n/a | 295.3 | n/a | - |
| server RSS peak | MB | 981.0 | 1785.0 | 1.82 | 1.71 1.82 1.85 |

Correctness gate: A: adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22).

### fu-sf10jdbc-s3: A = f06b5834e76e `-`, B = f06b5834e76e `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 JDBC (sum of medians) | s | 436.2 | 295.2 | 0.68 | 1.02 0.68 1.00 |
| server RSS peak | MB | 1600.0 | 1640.0 | 1.02 | 1.01 1.03 1.04 |

### fu-sf10jdbc-s3-vs-up-native: A = up-native `-`, B = f06b5834e76e `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 JDBC (sum of medians) | s | n/a | 295.2 | n/a | - |
| server RSS peak | MB | 982.0 | 1640.0 | 1.67 | 1.68 1.68 1.56 |

Correctness gate: A: jdbc10 (md5 50bb2801381f (1/22 ok)).

### fu-small-local: A = f06b5834e76e `-`, B = f06b5834e76e `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 18.6 | 20.1 | 1.08 | 1.18 1.03 1.06 |
| small JDBC c1 p95 | ms | 40.1 | 40.7 | 1.02 | 1.09 1.04 0.99 |
| small JDBC c1 p99 | ms | 48.8 | 46.3 | 0.95 | 1.11 0.95 0.85 |
| small JDBC c8 p50 | ms | 95.3 | 70.3 | 0.74 | 0.76 0.76 0.70 |
| small JDBC c8 p95 | ms | 248.5 | 227.5 | 0.92 | 0.92 0.85 0.97 |
| small JDBC c8 p99 | ms | 312.3 | 273.3 | 0.88 | 0.86 0.88 0.89 |
| small JDBC c32 p50 | ms | 378.6 | 217.8 | 0.58 | 0.63 0.56 0.58 |
| small JDBC c32 p95 | ms | 1079.4 | 939.0 | 0.87 | 0.87 0.85 0.90 |
| small JDBC c32 p99 | ms | 1375.0 | 1099.8 | 0.80 | 0.79 0.77 0.85 |
| small ADBC c1 p50 | ms | 12.7 | 14.2 | 1.12 | 1.18 1.18 1.00 |
| small ADBC c1 p95 | ms | 37.0 | 37.5 | 1.01 | 0.93 1.05 1.02 |
| small ADBC c1 p99 | ms | 47.1 | 45.2 | 0.96 | 0.88 1.08 0.97 |
| small ADBC c8 p50 | ms | 84.4 | 60.9 | 0.72 | 0.78 0.67 0.72 |
| small ADBC c8 p95 | ms | 258.0 | 231.5 | 0.90 | 1.00 0.86 0.90 |
| small ADBC c8 p99 | ms | 345.5 | 298.9 | 0.87 | 0.97 0.77 0.91 |
| small ADBC c32 p50 | ms | 349.1 | 229.8 | 0.66 | 0.61 0.66 0.65 |
| small ADBC c32 p95 | ms | 1057.5 | 920.7 | 0.87 | 0.87 0.88 0.87 |
| small ADBC c32 p99 | ms | 1301.8 | 1081.4 | 0.83 | 0.84 0.80 0.84 |
| server RSS peak | MB | 1500.0 | 760.0 | 0.51 | 0.48 0.52 0.51 |

### fu-small-local-vs-up-native: A = up-native `-`, B = f06b5834e76e `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | n/a | 20.1 | n/a | - |
| small JDBC c1 p95 | ms | n/a | 40.7 | n/a | - |
| small JDBC c1 p99 | ms | n/a | 46.3 | n/a | - |
| small JDBC c8 p50 | ms | n/a | 70.3 | n/a | - |
| small JDBC c8 p95 | ms | n/a | 227.5 | n/a | - |
| small JDBC c8 p99 | ms | n/a | 273.3 | n/a | - |
| small JDBC c32 p50 | ms | n/a | 217.8 | n/a | - |
| small JDBC c32 p95 | ms | n/a | 939.0 | n/a | - |
| small JDBC c32 p99 | ms | n/a | 1099.8 | n/a | - |
| small ADBC c1 p50 | ms | n/a | 14.2 | n/a | - |
| small ADBC c1 p95 | ms | n/a | 37.5 | n/a | - |
| small ADBC c1 p99 | ms | n/a | 45.2 | n/a | - |
| small ADBC c8 p50 | ms | n/a | 60.9 | n/a | - |
| small ADBC c8 p95 | ms | n/a | 231.5 | n/a | - |
| small ADBC c8 p99 | ms | n/a | 298.9 | n/a | - |
| small ADBC c32 p50 | ms | n/a | 229.8 | n/a | - |
| small ADBC c32 p95 | ms | n/a | 920.7 | n/a | - |
| small ADBC c32 p99 | ms | n/a | 1081.4 | n/a | - |
| server RSS peak | MB | 259.0 | 760.0 | 2.93 | 2.90 2.92 2.93 |

Correctness gate: A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point).

### fu-small-s3: A = f06b5834e76e `-`, B = f06b5834e76e `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 26.3 | 27.4 | 1.04 | 1.08 0.97 0.93 |
| small JDBC c1 p95 | ms | 687.8 | 705.2 | 1.03 | 1.06 0.98 1.04 |
| small JDBC c1 p99 | ms | 754.3 | 761.3 | 1.01 | 1.03 1.00 1.05 |
| small JDBC c8 p50 | ms | 257.9 | 157.4 | 0.61 | 0.54 0.62 0.66 |
| small JDBC c8 p95 | ms | 3801.1 | 4224.1 | 1.11 | 1.13 1.11 1.11 |
| small JDBC c8 p99 | ms | 4190.7 | 6988.7 | 1.67 | 1.67 1.67 1.59 |
| small JDBC c32 p50 | ms | 975.4 | 433.2 | 0.44 | 0.44 0.44 0.48 |
| small JDBC c32 p95 | ms | 12765.6 | 18072.4 | 1.42 | 1.43 1.38 1.50 |
| small JDBC c32 p99 | ms | 14403.3 | 20133.3 | 1.40 | 1.40 1.32 1.49 |
| small ADBC c1 p50 | ms | 19.4 | 19.6 | 1.01 | 1.01 1.09 0.97 |
| small ADBC c1 p95 | ms | 704.4 | 707.0 | 1.00 | 1.02 1.04 0.94 |
| small ADBC c1 p99 | ms | 764.3 | 774.5 | 1.01 | 1.01 1.06 0.56 |
| small ADBC c8 p50 | ms | 251.7 | 158.7 | 0.63 | 0.72 0.62 0.62 |
| small ADBC c8 p95 | ms | 4002.0 | 4114.0 | 1.03 | 1.21 0.99 1.11 |
| small ADBC c8 p99 | ms | 4269.8 | 7014.2 | 1.64 | 1.64 1.25 1.67 |
| small ADBC c32 p50 | ms | 967.7 | 417.5 | 0.43 | 0.43 0.41 0.47 |
| small ADBC c32 p95 | ms | 12683.0 | 17600.4 | 1.39 | 1.38 1.41 1.30 |
| small ADBC c32 p99 | ms | 15001.5 | 19862.4 | 1.32 | 1.39 1.32 1.10 |
| server RSS peak | MB | 2260.0 | 862.0 | 0.38 | 0.38 0.36 0.39 |

### fu-small-s3-vs-up-native: A = up-native `-`, B = f06b5834e76e `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | n/a | 27.4 | n/a | - |
| small JDBC c1 p95 | ms | n/a | 705.2 | n/a | - |
| small JDBC c1 p99 | ms | n/a | 761.3 | n/a | - |
| small JDBC c8 p50 | ms | n/a | 157.4 | n/a | - |
| small JDBC c8 p95 | ms | n/a | 4224.1 | n/a | - |
| small JDBC c8 p99 | ms | n/a | 6988.7 | n/a | - |
| small JDBC c32 p50 | ms | n/a | 433.2 | n/a | - |
| small JDBC c32 p95 | ms | n/a | 18072.4 | n/a | - |
| small JDBC c32 p99 | ms | n/a | 20133.3 | n/a | - |
| small ADBC c1 p50 | ms | n/a | 19.6 | n/a | - |
| small ADBC c1 p95 | ms | n/a | 707.0 | n/a | - |
| small ADBC c1 p99 | ms | n/a | 774.5 | n/a | - |
| small ADBC c8 p50 | ms | n/a | 158.7 | n/a | - |
| small ADBC c8 p95 | ms | n/a | 4114.0 | n/a | - |
| small ADBC c8 p99 | ms | n/a | 7014.2 | n/a | - |
| small ADBC c32 p50 | ms | n/a | 417.5 | n/a | - |
| small ADBC c32 p95 | ms | n/a | 17600.4 | n/a | - |
| small ADBC c32 p99 | ms | n/a | 19862.4 | n/a | - |
| server RSS peak | MB | 401.0 | 862.0 | 2.15 | 2.10 2.09 2.15 |

Correctness gate: A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-adbc8 (640/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc8 (387/640 errors; 487/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point).

### fu-tpch-local: A = f06b5834e76e `-`, B = f06b5834e76e `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 4.1 | 4.1 | 1.00 | 1.00 1.01 0.99 |
| TPC-H SF10 ADBC (sum of medians) | s | 42.4 | 39.9 | 0.94 | 0.97 0.93 0.96 |
| TPC-H SF1 JDBC (sum of medians) | s | 4.2 | 4.2 | 1.02 | 1.00 1.07 1.00 |
| TPC-H SF10 JDBC (sum of medians) | s | 41.5 | 39.9 | 0.96 | 0.95 0.93 0.98 |
| server RSS peak | MB | 1577.0 | 1760.0 | 1.12 | 1.06 1.09 1.19 |

### fu-tpch-local-vs-up-native: A = up-native `-`, B = f06b5834e76e `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | n/a | 4.1 | n/a | - |
| TPC-H SF10 ADBC (sum of medians) | s | n/a | 39.9 | n/a | - |
| TPC-H SF1 JDBC (sum of medians) | s | n/a | 4.2 | n/a | - |
| TPC-H SF10 JDBC (sum of medians) | s | n/a | 39.9 | n/a | - |
| server RSS peak | MB | 357.0 | 1760.0 | 4.93 | 4.68 5.06 4.93 |

Correctness gate: A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)), jdbc10 (md5 50bb2801381f (1/22 ok)).

### fu-zstd-netem-local: A = f06b5834e76e `CZSTD`, B = f06b5834e76e `-DresourceProfile=speed CZSTD`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 1485.0 | 1675.0 | 1.13 | 1.12 1.13 1.20 |

### fu-zstd-netem-local-vs-up-native: A = up-native `-DflightCompression=zstd`, B = f06b5834e76e `-DresourceProfile=speed CZSTD`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 616.0 | 1675.0 | 2.72 | 2.74 2.53 2.74 |
