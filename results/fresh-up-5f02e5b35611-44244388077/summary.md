# Wave fresh-up-5f02e5b35611 (server comparison), run 44244388077

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

## Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| fu-load-local | 5f02e5b35611 `-` | 5f02e5b35611 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-load-local-vs-up-native | up-native `-` | 5f02e5b35611 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-scan-local | 5f02e5b35611 `-` | 5f02e5b35611 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU Intel(R) Xeon(R) 6975P-C | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.07 | none |
| fu-scan-local-vs-up-native | up-native `-` | 5f02e5b35611 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU Intel(R) Xeon(R) 6975P-C | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.11 | none |
| fu-scan-s3 | 5f02e5b35611 `-` | 5f02e5b35611 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.26 | none |
| fu-scan-s3-vs-up-native | up-native `-` | 5f02e5b35611 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.15 | A: scan8 (rows=272646672 errors=4; rows=397402904 errors=2) |
| fu-sf1-s3 | 5f02e5b35611 `-` | 5f02e5b35611 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 0.09 | n/a | n/a | n/a | none |
| fu-sf1-s3-vs-up-native | up-native `-` | 5f02e5b35611 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)) |
| fu-sf10adbc-s3 | 5f02e5b35611 `-` | 5f02e5b35611 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU Intel(R) Xeon(R) 6975P-C | 3/3 | n/a | n/a | n/a | n/a | n/a | 0.10 | n/a | n/a | none |
| fu-sf10adbc-s3-vs-up-native | up-native `-` | 5f02e5b35611 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU Intel(R) Xeon(R) 6975P-C | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22) |
| fu-sf10jdbc-s3 | 5f02e5b35611 `-` | 5f02e5b35611 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | 0.12 | n/a | none |
| fu-sf10jdbc-s3-vs-up-native | up-native `-` | 5f02e5b35611 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: jdbc10 (md5 50bb2801381f (1/22 ok)) |
| fu-small-local | 5f02e5b35611 `-` | 5f02e5b35611 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | 1.26 | 0.99 | 1.18 | 1.01 | n/a | n/a | n/a | n/a | none |
| fu-small-local-vs-up-native | up-native `-` | 5f02e5b35611 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point) |
| fu-small-s3 | 5f02e5b35611 `-` | 5f02e5b35611 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | 0.71 | 0.04 | 0.91 | 0.04 | n/a | n/a | n/a | n/a | none |
| fu-small-s3-vs-up-native | up-native `-` | 5f02e5b35611 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-adbc8 (640/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc8 (405/640 errors; 440/640 errors; 532/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point) |
| fu-tpch-local | 5f02e5b35611 `-` | 5f02e5b35611 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 1.01 | 0.97 | 1.01 | n/a | none |
| fu-tpch-local-vs-up-native | up-native `-` | 5f02e5b35611 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)), jdbc10 (md5 50bb2801381f (1/22 ok)) |
| fu-zstd-netem-local | 5f02e5b35611 `CZSTD` | 5f02e5b35611 `-DresourceProfile=speed CZSTD` | local | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fu-zstd-netem-local-vs-up-native | up-native `-DflightCompression=zstd` | 5f02e5b35611 `-DresourceProfile=speed CZSTD` | local | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |

## Per job (absolute medians and ratios)

### fu-load-local: A = 5f02e5b35611 `-`, B = 5f02e5b35611 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 810.0 | 920.0 | 1.14 | 1.06 1.22 1.12 |

### fu-load-local-vs-up-native: A = up-native `-`, B = 5f02e5b35611 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 1000.0 | 920.0 | 0.92 | 0.86 0.99 0.92 |

### fu-scan-local: A = 5f02e5b35611 `-`, B = 5f02e5b35611 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU Intel(R) Xeon(R) 6975P-C. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 575.4 | 617.6 | 1.07 | 1.10 1.07 1.07 |
| lineitem scan x4 | MB/s | 794.1 | 872.7 | 1.10 | 1.10 1.14 1.12 |
| lineitem scan x8 | MB/s | 804.2 | 874.0 | 1.09 | 1.11 1.07 1.08 |
| lineitem export ADBC | MB/s | 672.1 | 749.6 | 1.12 | 1.12 1.10 1.12 |
| server RSS peak | MB | 1208.0 | 1155.0 | 0.96 | 0.96 1.00 0.95 |

### fu-scan-local-vs-up-native: A = up-native `-`, B = 5f02e5b35611 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU Intel(R) Xeon(R) 6975P-C. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 554.6 | 617.6 | 1.11 | 1.08 1.12 1.14 |
| lineitem scan x4 | MB/s | 799.1 | 872.7 | 1.09 | 1.08 1.08 1.14 |
| lineitem scan x8 | MB/s | 821.2 | 874.0 | 1.06 | 1.06 1.07 1.06 |
| lineitem export ADBC | MB/s | 636.5 | 749.6 | 1.18 | 1.13 1.29 1.18 |
| server RSS peak | MB | 1942.0 | 1155.0 | 0.59 | 0.59 0.58 0.61 |

### fu-scan-s3: A = 5f02e5b35611 `-`, B = 5f02e5b35611 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 360.0 | 452.0 | 1.26 | 1.14 1.26 1.25 |
| lineitem scan x4 | MB/s | 641.3 | 727.0 | 1.13 | 1.27 1.11 1.13 |
| lineitem scan x8 | MB/s | 645.7 | 734.3 | 1.14 | 1.13 1.14 1.16 |
| lineitem export ADBC | MB/s | 428.9 | 672.9 | 1.57 | 1.60 1.47 1.57 |
| server RSS peak | MB | 1530.0 | 3316.0 | 2.17 | 2.17 2.17 2.13 |

### fu-scan-s3-vs-up-native: A = up-native `-`, B = 5f02e5b35611 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 392.1 | 452.0 | 1.15 | 1.16 1.51 1.06 |
| lineitem scan x4 | MB/s | 703.8 | 727.0 | 1.03 | 1.05 1.02 1.03 |
| lineitem scan x8 | MB/s | n/a | 734.3 | n/a | - |
| lineitem export ADBC | MB/s | 648.8 | 672.9 | 1.04 | 1.09 1.02 1.04 |
| server RSS peak | MB | 5996.0 | 3316.0 | 0.55 | 0.57 0.55 0.55 |

Correctness gate: A: scan8 (rows=272646672 errors=4; rows=397402904 errors=2).

### fu-sf1-s3: A = 5f02e5b35611 `-`, B = 5f02e5b35611 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 36.0 | 3.3 | 0.09 | 0.11 0.09 0.08 |
| TPC-H SF1 JDBC (sum of medians) | s | 30.6 | 3.4 | 0.11 | 0.12 0.08 0.11 |
| server RSS peak | MB | 725.0 | 996.0 | 1.37 | 1.49 1.32 1.35 |

### fu-sf1-s3-vs-up-native: A = up-native `-`, B = 5f02e5b35611 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | n/a | 3.3 | n/a | - |
| TPC-H SF1 JDBC (sum of medians) | s | n/a | 3.4 | n/a | - |
| server RSS peak | MB | 687.0 | 996.0 | 1.45 | 1.68 1.39 1.29 |

Correctness gate: A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)).

### fu-sf10adbc-s3: A = 5f02e5b35611 `-`, B = 5f02e5b35611 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU Intel(R) Xeon(R) 6975P-C. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | 229.8 | 23.1 | 0.10 | 0.10 0.10 0.10 |
| server RSS peak | MB | 1554.0 | 3405.0 | 2.19 | 2.05 2.22 2.25 |

### fu-sf10adbc-s3-vs-up-native: A = up-native `-`, B = 5f02e5b35611 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU Intel(R) Xeon(R) 6975P-C. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | n/a | 23.1 | n/a | - |
| server RSS peak | MB | 1065.0 | 3405.0 | 3.20 | 3.20 3.14 3.37 |

Correctness gate: A: adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22).

### fu-sf10jdbc-s3: A = 5f02e5b35611 `-`, B = 5f02e5b35611 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `sf10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 JDBC (sum of medians) | s | 264.6 | 32.2 | 0.12 | 0.12 0.12 0.12 |
| server RSS peak | MB | 1479.0 | 3370.0 | 2.28 | 2.29 2.27 2.29 |

### fu-sf10jdbc-s3-vs-up-native: A = up-native `-`, B = 5f02e5b35611 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `sf10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 JDBC (sum of medians) | s | n/a | 32.2 | n/a | - |
| server RSS peak | MB | 1029.0 | 3370.0 | 3.28 | 3.24 3.28 3.26 |

Correctness gate: A: jdbc10 (md5 50bb2801381f (1/22 ok)).

### fu-small-local: A = 5f02e5b35611 `-`, B = 5f02e5b35611 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 17.7 | 20.8 | 1.18 | 1.19 1.16 1.17 |
| small JDBC c1 p95 | ms | 37.2 | 39.1 | 1.05 | 0.96 1.06 1.05 |
| small JDBC c1 p99 | ms | 42.4 | 50.6 | 1.19 | 1.23 1.24 0.99 |
| small JDBC c8 p50 | ms | 60.5 | 83.6 | 1.38 | 1.42 1.37 1.38 |
| small JDBC c8 p95 | ms | 239.9 | 218.8 | 0.91 | 0.93 0.92 0.90 |
| small JDBC c8 p99 | ms | 273.2 | 294.5 | 1.08 | 1.09 1.10 1.04 |
| small JDBC c32 p50 | ms | 201.7 | 317.5 | 1.57 | 1.60 1.60 1.46 |
| small JDBC c32 p95 | ms | 892.6 | 897.2 | 1.01 | 1.01 1.00 1.06 |
| small JDBC c32 p99 | ms | 1038.7 | 1059.7 | 1.02 | 1.05 1.02 1.03 |
| small ADBC c1 p50 | ms | 12.4 | 15.6 | 1.26 | 1.24 1.24 1.26 |
| small ADBC c1 p95 | ms | 40.6 | 38.0 | 0.94 | 1.02 0.94 0.86 |
| small ADBC c1 p99 | ms | 48.2 | 45.6 | 0.95 | 1.11 0.87 0.94 |
| small ADBC c8 p50 | ms | 54.2 | 83.7 | 1.55 | 1.49 1.58 1.40 |
| small ADBC c8 p95 | ms | 235.7 | 223.8 | 0.95 | 0.95 0.94 1.00 |
| small ADBC c8 p99 | ms | 277.5 | 306.8 | 1.11 | 1.09 1.11 1.23 |
| small ADBC c32 p50 | ms | 192.9 | 313.6 | 1.63 | 1.74 1.63 1.59 |
| small ADBC c32 p95 | ms | 905.4 | 900.5 | 0.99 | 0.99 0.99 1.03 |
| small ADBC c32 p99 | ms | 1068.1 | 1097.2 | 1.03 | 0.92 1.04 1.03 |
| server RSS peak | MB | 687.0 | 865.0 | 1.26 | 1.10 1.24 1.31 |

### fu-small-local-vs-up-native: A = up-native `-`, B = 5f02e5b35611 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | n/a | 20.8 | n/a | - |
| small JDBC c1 p95 | ms | n/a | 39.1 | n/a | - |
| small JDBC c1 p99 | ms | n/a | 50.6 | n/a | - |
| small JDBC c8 p50 | ms | n/a | 83.6 | n/a | - |
| small JDBC c8 p95 | ms | n/a | 218.8 | n/a | - |
| small JDBC c8 p99 | ms | n/a | 294.5 | n/a | - |
| small JDBC c32 p50 | ms | n/a | 317.5 | n/a | - |
| small JDBC c32 p95 | ms | n/a | 897.2 | n/a | - |
| small JDBC c32 p99 | ms | n/a | 1059.7 | n/a | - |
| small ADBC c1 p50 | ms | n/a | 15.6 | n/a | - |
| small ADBC c1 p95 | ms | n/a | 38.0 | n/a | - |
| small ADBC c1 p99 | ms | n/a | 45.6 | n/a | - |
| small ADBC c8 p50 | ms | n/a | 83.7 | n/a | - |
| small ADBC c8 p95 | ms | n/a | 223.8 | n/a | - |
| small ADBC c8 p99 | ms | n/a | 306.8 | n/a | - |
| small ADBC c32 p50 | ms | n/a | 313.6 | n/a | - |
| small ADBC c32 p95 | ms | n/a | 900.5 | n/a | - |
| small ADBC c32 p99 | ms | n/a | 1097.2 | n/a | - |
| server RSS peak | MB | 255.0 | 865.0 | 3.39 | 3.42 3.35 3.21 |

Correctness gate: A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point).

### fu-small-s3: A = 5f02e5b35611 `-`, B = 5f02e5b35611 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 30.3 | 27.7 | 0.91 | 0.99 0.90 0.89 |
| small JDBC c1 p95 | ms | 616.8 | 51.2 | 0.08 | 0.08 0.08 0.08 |
| small JDBC c1 p99 | ms | 649.5 | 73.0 | 0.11 | 0.10 0.09 0.12 |
| small JDBC c8 p50 | ms | 179.3 | 84.4 | 0.47 | 0.50 0.53 0.46 |
| small JDBC c8 p95 | ms | 6394.2 | 226.3 | 0.04 | 0.03 0.03 0.04 |
| small JDBC c8 p99 | ms | 6984.5 | 316.4 | 0.05 | 0.04 0.05 0.33 |
| small JDBC c32 p50 | ms | 598.0 | 235.8 | 0.39 | 0.42 0.41 0.39 |
| small JDBC c32 p95 | ms | 24688.6 | 1015.6 | 0.04 | 0.04 0.04 0.04 |
| small JDBC c32 p99 | ms | 28090.1 | 1173.3 | 0.04 | 0.04 0.05 0.04 |
| small ADBC c1 p50 | ms | 21.2 | 15.0 | 0.71 | 0.75 0.61 0.74 |
| small ADBC c1 p95 | ms | 637.1 | 42.4 | 0.07 | 0.07 0.06 0.07 |
| small ADBC c1 p99 | ms | 669.9 | 46.4 | 0.07 | 0.08 0.07 0.07 |
| small ADBC c8 p50 | ms | 159.7 | 68.0 | 0.43 | 0.44 0.41 0.44 |
| small ADBC c8 p95 | ms | 6380.1 | 201.3 | 0.03 | 0.03 0.03 0.03 |
| small ADBC c8 p99 | ms | 6707.7 | 283.9 | 0.04 | 0.04 0.04 0.04 |
| small ADBC c32 p50 | ms | 580.2 | 220.4 | 0.38 | 0.38 0.35 0.39 |
| small ADBC c32 p95 | ms | 24652.0 | 992.1 | 0.04 | 0.04 0.04 0.04 |
| small ADBC c32 p99 | ms | 26477.4 | 1155.1 | 0.04 | 0.04 0.05 0.04 |
| server RSS peak | MB | 792.0 | 1506.0 | 1.90 | 1.90 1.85 1.92 |

### fu-small-s3-vs-up-native: A = up-native `-`, B = 5f02e5b35611 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | n/a | 27.7 | n/a | - |
| small JDBC c1 p95 | ms | n/a | 51.2 | n/a | - |
| small JDBC c1 p99 | ms | n/a | 73.0 | n/a | - |
| small JDBC c8 p50 | ms | n/a | 84.4 | n/a | - |
| small JDBC c8 p95 | ms | n/a | 226.3 | n/a | - |
| small JDBC c8 p99 | ms | n/a | 316.4 | n/a | - |
| small JDBC c32 p50 | ms | n/a | 235.8 | n/a | - |
| small JDBC c32 p95 | ms | n/a | 1015.6 | n/a | - |
| small JDBC c32 p99 | ms | n/a | 1173.3 | n/a | - |
| small ADBC c1 p50 | ms | n/a | 15.0 | n/a | - |
| small ADBC c1 p95 | ms | n/a | 42.4 | n/a | - |
| small ADBC c1 p99 | ms | n/a | 46.4 | n/a | - |
| small ADBC c8 p50 | ms | n/a | 68.0 | n/a | - |
| small ADBC c8 p95 | ms | n/a | 201.3 | n/a | - |
| small ADBC c8 p99 | ms | n/a | 283.9 | n/a | - |
| small ADBC c32 p50 | ms | n/a | 220.4 | n/a | - |
| small ADBC c32 p95 | ms | n/a | 992.1 | n/a | - |
| small ADBC c32 p99 | ms | n/a | 1155.1 | n/a | - |
| server RSS peak | MB | 390.0 | 1506.0 | 3.86 | 3.86 4.01 3.78 |

Correctness gate: A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-adbc8 (640/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc8 (405/640 errors; 440/640 errors; 532/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point).

### fu-tpch-local: A = 5f02e5b35611 `-`, B = 5f02e5b35611 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 2.6 | 2.7 | 1.01 | 1.06 1.01 1.00 |
| TPC-H SF10 ADBC (sum of medians) | s | 28.7 | 27.9 | 0.97 | 1.02 0.99 0.94 |
| TPC-H SF1 JDBC (sum of medians) | s | 2.7 | 2.9 | 1.09 | 1.03 1.09 1.04 |
| TPC-H SF10 JDBC (sum of medians) | s | 27.7 | 28.0 | 1.01 | 1.08 0.94 1.01 |
| server RSS peak | MB | 1530.0 | 1905.0 | 1.25 | 1.23 1.30 1.21 |

### fu-tpch-local-vs-up-native: A = up-native `-`, B = 5f02e5b35611 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | n/a | 2.7 | n/a | - |
| TPC-H SF10 ADBC (sum of medians) | s | n/a | 27.9 | n/a | - |
| TPC-H SF1 JDBC (sum of medians) | s | n/a | 2.9 | n/a | - |
| TPC-H SF10 JDBC (sum of medians) | s | n/a | 28.0 | n/a | - |
| server RSS peak | MB | 363.0 | 1905.0 | 5.25 | 4.96 5.54 5.25 |

Correctness gate: A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)), jdbc10 (md5 50bb2801381f (1/22 ok)).

### fu-zstd-netem-local: A = 5f02e5b35611 `CZSTD`, B = 5f02e5b35611 `-DresourceProfile=speed CZSTD`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 1446.0 | 1625.0 | 1.12 | 1.24 1.12 1.10 |

### fu-zstd-netem-local-vs-up-native: A = up-native `-DflightCompression=zstd`, B = 5f02e5b35611 `-DresourceProfile=speed CZSTD`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 607.0 | 1625.0 | 2.68 | 2.90 2.68 2.64 |
