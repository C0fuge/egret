# Wave fresh-up-fc-f06b5834e76e (server comparison), run 41437982824

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

## Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| fuc-load-local | f06b5834e76e `-` | f06b5834e76e `-DresourceProfile=speed -DduckDbExternalFileCache=true` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fuc-load-local-vs-up-native | up-native `-` | f06b5834e76e `-DresourceProfile=speed -DduckDbExternalFileCache=true` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fuc-scan-local | f06b5834e76e `-` | f06b5834e76e `-DresourceProfile=speed -DduckDbExternalFileCache=true` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.01 | none |
| fuc-scan-local-vs-up-native | up-native `-` | f06b5834e76e `-DresourceProfile=speed -DduckDbExternalFileCache=true` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.08 | none |
| fuc-scan-s3 | f06b5834e76e `-` | f06b5834e76e `-DresourceProfile=speed -DduckDbExternalFileCache=true` | s3 | Linux ubuntu26 4 vCPU Intel(R) Xeon(R) 6975P-C | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 0.84 | none |
| fuc-scan-s3-vs-up-native | up-native `-` | f06b5834e76e `-DresourceProfile=speed -DduckDbExternalFileCache=true` | s3 | Linux ubuntu26 4 vCPU Intel(R) Xeon(R) 6975P-C | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 0.80 | none |
| fuc-sf1-s3 | f06b5834e76e `-` | f06b5834e76e `-DresourceProfile=speed -DduckDbExternalFileCache=true` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 0.15 | n/a | n/a | n/a | none |
| fuc-sf1-s3-vs-up-native | up-native `-` | f06b5834e76e `-DresourceProfile=speed -DduckDbExternalFileCache=true` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)) |
| fuc-sf10adbc-s3 | f06b5834e76e `-` | f06b5834e76e `-DresourceProfile=speed -DduckDbExternalFileCache=true` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | 0.18 | n/a | n/a | none |
| fuc-sf10adbc-s3-vs-up-native | up-native `-` | f06b5834e76e `-DresourceProfile=speed -DduckDbExternalFileCache=true` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22) |
| fuc-sf10jdbc-s3 | f06b5834e76e `-` | f06b5834e76e `-DresourceProfile=speed -DduckDbExternalFileCache=true` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | 0.13 | n/a | none |
| fuc-sf10jdbc-s3-vs-up-native | up-native `-` | f06b5834e76e `-DresourceProfile=speed -DduckDbExternalFileCache=true` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: jdbc10 (md5 50bb2801381f (1/22 ok)) |
| fuc-small-local | f06b5834e76e `-` | f06b5834e76e `-DresourceProfile=speed -DduckDbExternalFileCache=true` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | 0.99 | 0.90 | 1.02 | 0.89 | n/a | n/a | n/a | n/a | none |
| fuc-small-local-vs-up-native | up-native `-` | f06b5834e76e `-DresourceProfile=speed -DduckDbExternalFileCache=true` | local | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point) |
| fuc-small-s3 | f06b5834e76e `-` | f06b5834e76e `-DresourceProfile=speed -DduckDbExternalFileCache=true` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | 0.48 | 0.04 | 0.73 | 0.05 | n/a | n/a | n/a | n/a | none |
| fuc-small-s3-vs-up-native | up-native `-` | f06b5834e76e `-DresourceProfile=speed -DduckDbExternalFileCache=true` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-adbc8 (640/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc8 (429/640 errors; 506/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point) |
| fuc-tpch-local | f06b5834e76e `-` | f06b5834e76e `-DresourceProfile=speed -DduckDbExternalFileCache=true` | local | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 0.98 | 0.95 | 0.98 | n/a | none |
| fuc-tpch-local-vs-up-native | up-native `-` | f06b5834e76e `-DresourceProfile=speed -DduckDbExternalFileCache=true` | local | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)), jdbc10 (md5 50bb2801381f (1/22 ok)) |
| fuc-zstd-netem-local | f06b5834e76e `CZSTD` | f06b5834e76e `-DresourceProfile=speed CZSTD` | local | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fuc-zstd-netem-local-vs-up-native | up-native `-DflightCompression=zstd` | f06b5834e76e `-DresourceProfile=speed CZSTD` | local | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |

## Per job (absolute medians and ratios)

### fuc-load-local: A = f06b5834e76e `-`, B = f06b5834e76e `-DresourceProfile=speed -DduckDbExternalFileCache=true`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 4738.0 | 836.0 | 0.18 | 0.22 0.18 0.17 |

### fuc-load-local-vs-up-native: A = up-native `-`, B = f06b5834e76e `-DresourceProfile=speed -DduckDbExternalFileCache=true`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 973.0 | 836.0 | 0.86 | 1.05 0.86 0.86 |

### fuc-scan-local: A = f06b5834e76e `-`, B = f06b5834e76e `-DresourceProfile=speed -DduckDbExternalFileCache=true`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 698.9 | 706.6 | 1.01 | 1.00 1.01 1.04 |
| lineitem scan x4 | MB/s | 737.8 | 793.9 | 1.08 | 1.07 1.08 1.08 |
| lineitem scan x8 | MB/s | 643.3 | 816.5 | 1.27 | 1.24 1.29 1.27 |
| lineitem export ADBC | MB/s | 814.8 | 847.0 | 1.04 | 1.14 1.02 1.07 |
| server RSS peak | MB | 1208.0 | 1131.0 | 0.94 | 0.94 0.94 0.94 |

### fuc-scan-local-vs-up-native: A = up-native `-`, B = f06b5834e76e `-DresourceProfile=speed -DduckDbExternalFileCache=true`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 651.6 | 706.6 | 1.08 | 1.11 1.08 1.06 |
| lineitem scan x4 | MB/s | 836.0 | 793.9 | 0.95 | 0.95 0.94 0.95 |
| lineitem scan x8 | MB/s | 883.6 | 816.5 | 0.92 | 0.93 0.91 0.93 |
| lineitem export ADBC | MB/s | 813.1 | 847.0 | 1.04 | 1.02 1.01 1.07 |
| server RSS peak | MB | 3544.0 | 1131.0 | 0.32 | 0.32 0.33 0.32 |

### fuc-scan-s3: A = f06b5834e76e `-`, B = f06b5834e76e `-DresourceProfile=speed -DduckDbExternalFileCache=true`, s3

Runner: Linux ubuntu26 4 vCPU Intel(R) Xeon(R) 6975P-C. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 364.3 | 305.2 | 0.84 | 1.68 0.77 1.04 |
| lineitem scan x4 | MB/s | 617.7 | 793.2 | 1.28 | 1.23 1.29 1.29 |
| lineitem scan x8 | MB/s | 585.7 | 815.9 | 1.39 | 1.33 1.45 1.39 |
| lineitem export ADBC | MB/s | 395.7 | 483.5 | 1.22 | 1.37 1.22 1.23 |
| server RSS peak | MB | 1738.0 | 3452.0 | 1.99 | 1.83 2.07 1.97 |

### fuc-scan-s3-vs-up-native: A = up-native `-`, B = f06b5834e76e `-DresourceProfile=speed -DduckDbExternalFileCache=true`, s3

Runner: Linux ubuntu26 4 vCPU Intel(R) Xeon(R) 6975P-C. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 380.8 | 305.2 | 0.80 | 0.80 0.78 0.99 |
| lineitem scan x4 | MB/s | 850.2 | 793.2 | 0.93 | 0.92 0.95 0.93 |
| lineitem scan x8 | MB/s | 853.2 | 815.9 | 0.96 | 0.97 0.98 0.95 |
| lineitem export ADBC | MB/s | 665.7 | 483.5 | 0.73 | 0.93 0.73 0.70 |
| server RSS peak | MB | 4169.0 | 3452.0 | 0.83 | 0.75 0.88 0.81 |

### fuc-sf1-s3: A = f06b5834e76e `-`, B = f06b5834e76e `-DresourceProfile=speed -DduckDbExternalFileCache=true`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 26.7 | 3.9 | 0.15 | 0.15 0.15 0.14 |
| TPC-H SF1 JDBC (sum of medians) | s | 26.7 | 4.1 | 0.15 | 0.15 0.15 0.16 |
| server RSS peak | MB | 717.0 | 928.0 | 1.29 | 1.32 1.27 1.31 |

### fuc-sf1-s3-vs-up-native: A = up-native `-`, B = f06b5834e76e `-DresourceProfile=speed -DduckDbExternalFileCache=true`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | n/a | 3.9 | n/a | - |
| TPC-H SF1 JDBC (sum of medians) | s | n/a | 4.1 | n/a | - |
| server RSS peak | MB | 621.0 | 928.0 | 1.49 | 1.44 1.47 1.53 |

Correctness gate: A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)).

### fuc-sf10adbc-s3: A = f06b5834e76e `-`, B = f06b5834e76e `-DresourceProfile=speed -DduckDbExternalFileCache=true`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | 300.1 | 54.5 | 0.18 | 0.18 0.19 0.18 |
| server RSS peak | MB | 1588.0 | 3096.0 | 1.95 | 1.81 1.96 1.95 |

### fuc-sf10adbc-s3-vs-up-native: A = up-native `-`, B = f06b5834e76e `-DresourceProfile=speed -DduckDbExternalFileCache=true`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | n/a | 54.5 | n/a | - |
| server RSS peak | MB | 995.0 | 3096.0 | 3.11 | 3.04 3.28 3.02 |

Correctness gate: A: adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22).

### fuc-sf10jdbc-s3: A = f06b5834e76e `-`, B = f06b5834e76e `-DresourceProfile=speed -DduckDbExternalFileCache=true`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `sf10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 JDBC (sum of medians) | s | 258.3 | 32.8 | 0.13 | 0.12 0.13 0.15 |
| server RSS peak | MB | 1592.0 | 3094.0 | 1.94 | 1.89 1.95 1.94 |

### fuc-sf10jdbc-s3-vs-up-native: A = up-native `-`, B = f06b5834e76e `-DresourceProfile=speed -DduckDbExternalFileCache=true`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `sf10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 JDBC (sum of medians) | s | n/a | 32.8 | n/a | - |
| server RSS peak | MB | 1022.0 | 3094.0 | 3.03 | 3.15 3.03 2.98 |

Correctness gate: A: jdbc10 (md5 50bb2801381f (1/22 ok)).

### fuc-small-local: A = f06b5834e76e `-`, B = f06b5834e76e `-DresourceProfile=speed -DduckDbExternalFileCache=true`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 19.7 | 20.2 | 1.02 | 0.89 1.08 1.03 |
| small JDBC c1 p95 | ms | 40.2 | 40.4 | 1.01 | 0.94 1.01 1.01 |
| small JDBC c1 p99 | ms | 48.2 | 46.5 | 0.97 | 0.92 1.09 0.96 |
| small JDBC c8 p50 | ms | 97.9 | 71.5 | 0.73 | 0.74 0.72 0.73 |
| small JDBC c8 p95 | ms | 241.1 | 223.0 | 0.92 | 0.91 0.94 0.90 |
| small JDBC c8 p99 | ms | 309.7 | 274.4 | 0.89 | 0.97 0.79 0.86 |
| small JDBC c32 p50 | ms | 380.6 | 223.4 | 0.59 | 0.58 0.59 0.60 |
| small JDBC c32 p95 | ms | 1029.8 | 912.9 | 0.89 | 0.89 0.87 0.86 |
| small JDBC c32 p99 | ms | 1371.2 | 1065.9 | 0.78 | 0.87 0.78 0.74 |
| small ADBC c1 p50 | ms | 13.3 | 13.2 | 0.99 | 1.06 0.92 0.97 |
| small ADBC c1 p95 | ms | 35.4 | 37.8 | 1.07 | 1.06 1.13 1.00 |
| small ADBC c1 p99 | ms | 44.7 | 45.1 | 1.01 | 0.97 1.06 1.18 |
| small ADBC c8 p50 | ms | 79.8 | 63.1 | 0.79 | 0.79 0.82 0.73 |
| small ADBC c8 p95 | ms | 244.1 | 226.9 | 0.93 | 0.93 0.93 0.88 |
| small ADBC c8 p99 | ms | 358.0 | 308.7 | 0.86 | 0.86 0.89 0.81 |
| small ADBC c32 p50 | ms | 367.4 | 233.6 | 0.64 | 0.65 0.58 0.66 |
| small ADBC c32 p95 | ms | 1027.2 | 920.2 | 0.90 | 0.92 0.84 0.90 |
| small ADBC c32 p99 | ms | 1337.5 | 1065.2 | 0.80 | 0.82 0.76 0.83 |
| server RSS peak | MB | 1493.0 | 752.0 | 0.50 | 0.50 0.50 0.53 |

### fuc-small-local-vs-up-native: A = up-native `-`, B = f06b5834e76e `-DresourceProfile=speed -DduckDbExternalFileCache=true`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | n/a | 20.2 | n/a | - |
| small JDBC c1 p95 | ms | n/a | 40.4 | n/a | - |
| small JDBC c1 p99 | ms | n/a | 46.5 | n/a | - |
| small JDBC c8 p50 | ms | n/a | 71.5 | n/a | - |
| small JDBC c8 p95 | ms | n/a | 223.0 | n/a | - |
| small JDBC c8 p99 | ms | n/a | 274.4 | n/a | - |
| small JDBC c32 p50 | ms | n/a | 223.4 | n/a | - |
| small JDBC c32 p95 | ms | n/a | 912.9 | n/a | - |
| small JDBC c32 p99 | ms | n/a | 1065.9 | n/a | - |
| small ADBC c1 p50 | ms | n/a | 13.2 | n/a | - |
| small ADBC c1 p95 | ms | n/a | 37.8 | n/a | - |
| small ADBC c1 p99 | ms | n/a | 45.1 | n/a | - |
| small ADBC c8 p50 | ms | n/a | 63.1 | n/a | - |
| small ADBC c8 p95 | ms | n/a | 226.9 | n/a | - |
| small ADBC c8 p99 | ms | n/a | 308.7 | n/a | - |
| small ADBC c32 p50 | ms | n/a | 233.6 | n/a | - |
| small ADBC c32 p95 | ms | n/a | 920.2 | n/a | - |
| small ADBC c32 p99 | ms | n/a | 1065.2 | n/a | - |
| server RSS peak | MB | 243.0 | 752.0 | 3.09 | 3.08 3.11 3.10 |

Correctness gate: A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point).

### fuc-small-s3: A = f06b5834e76e `-`, B = f06b5834e76e `-DresourceProfile=speed -DduckDbExternalFileCache=true`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 27.6 | 20.0 | 0.73 | 0.65 0.86 0.71 |
| small JDBC c1 p95 | ms | 669.0 | 37.1 | 0.06 | 0.05 0.06 0.06 |
| small JDBC c1 p99 | ms | 719.7 | 45.2 | 0.06 | 0.06 0.07 0.06 |
| small JDBC c8 p50 | ms | 265.3 | 51.4 | 0.19 | 0.19 0.28 0.19 |
| small JDBC c8 p95 | ms | 3715.7 | 119.3 | 0.03 | 0.03 0.03 0.03 |
| small JDBC c8 p99 | ms | 4020.1 | 149.3 | 0.04 | 0.04 0.04 0.04 |
| small JDBC c32 p50 | ms | 951.1 | 138.9 | 0.15 | 0.14 0.15 0.15 |
| small JDBC c32 p95 | ms | 13014.5 | 594.2 | 0.05 | 0.04 0.04 0.05 |
| small JDBC c32 p99 | ms | 14757.4 | 705.9 | 0.05 | 0.05 0.05 0.05 |
| small ADBC c1 p50 | ms | 21.1 | 10.0 | 0.48 | 0.43 0.51 0.48 |
| small ADBC c1 p95 | ms | 684.8 | 27.2 | 0.04 | 0.03 0.04 0.04 |
| small ADBC c1 p99 | ms | 744.1 | 37.6 | 0.05 | 0.04 0.05 0.05 |
| small ADBC c8 p50 | ms | 254.7 | 40.0 | 0.16 | 0.15 0.18 0.16 |
| small ADBC c8 p95 | ms | 3814.2 | 121.0 | 0.03 | 0.03 0.03 0.03 |
| small ADBC c8 p99 | ms | 4148.1 | 156.1 | 0.04 | 0.04 0.04 0.04 |
| small ADBC c32 p50 | ms | 925.9 | 116.4 | 0.13 | 0.12 0.13 0.13 |
| small ADBC c32 p95 | ms | 13127.3 | 580.8 | 0.04 | 0.04 0.05 0.04 |
| small ADBC c32 p99 | ms | 14606.5 | 683.5 | 0.05 | 0.04 0.05 0.05 |
| server RSS peak | MB | 2279.0 | 1337.0 | 0.59 | 0.59 0.58 0.59 |

### fuc-small-s3-vs-up-native: A = up-native `-`, B = f06b5834e76e `-DresourceProfile=speed -DduckDbExternalFileCache=true`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | n/a | 20.0 | n/a | - |
| small JDBC c1 p95 | ms | n/a | 37.1 | n/a | - |
| small JDBC c1 p99 | ms | n/a | 45.2 | n/a | - |
| small JDBC c8 p50 | ms | n/a | 51.4 | n/a | - |
| small JDBC c8 p95 | ms | n/a | 119.3 | n/a | - |
| small JDBC c8 p99 | ms | n/a | 149.3 | n/a | - |
| small JDBC c32 p50 | ms | n/a | 138.9 | n/a | - |
| small JDBC c32 p95 | ms | n/a | 594.2 | n/a | - |
| small JDBC c32 p99 | ms | n/a | 705.9 | n/a | - |
| small ADBC c1 p50 | ms | n/a | 10.0 | n/a | - |
| small ADBC c1 p95 | ms | n/a | 27.2 | n/a | - |
| small ADBC c1 p99 | ms | n/a | 37.6 | n/a | - |
| small ADBC c8 p50 | ms | n/a | 40.0 | n/a | - |
| small ADBC c8 p95 | ms | n/a | 121.0 | n/a | - |
| small ADBC c8 p99 | ms | n/a | 156.1 | n/a | - |
| small ADBC c32 p50 | ms | n/a | 116.4 | n/a | - |
| small ADBC c32 p95 | ms | n/a | 580.8 | n/a | - |
| small ADBC c32 p99 | ms | n/a | 683.5 | n/a | - |
| server RSS peak | MB | 402.0 | 1337.0 | 3.33 | 3.35 3.28 3.58 |

Correctness gate: A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-adbc8 (640/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc8 (429/640 errors; 506/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point).

### fuc-tpch-local: A = f06b5834e76e `-`, B = f06b5834e76e `-DresourceProfile=speed -DduckDbExternalFileCache=true`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 4.1 | 4.0 | 0.98 | 0.98 0.97 1.00 |
| TPC-H SF10 ADBC (sum of medians) | s | 42.3 | 40.0 | 0.95 | 0.96 0.97 0.94 |
| TPC-H SF1 JDBC (sum of medians) | s | 4.2 | 4.2 | 1.00 | 0.98 0.99 1.00 |
| TPC-H SF10 JDBC (sum of medians) | s | 41.4 | 40.7 | 0.98 | 0.96 0.98 0.99 |
| server RSS peak | MB | 1586.0 | 1844.0 | 1.16 | 1.13 1.20 1.12 |

### fuc-tpch-local-vs-up-native: A = up-native `-`, B = f06b5834e76e `-DresourceProfile=speed -DduckDbExternalFileCache=true`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | n/a | 4.0 | n/a | - |
| TPC-H SF10 ADBC (sum of medians) | s | n/a | 40.0 | n/a | - |
| TPC-H SF1 JDBC (sum of medians) | s | n/a | 4.2 | n/a | - |
| TPC-H SF10 JDBC (sum of medians) | s | n/a | 40.7 | n/a | - |
| server RSS peak | MB | 361.0 | 1844.0 | 5.11 | 5.14 5.11 5.03 |

Correctness gate: A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)), jdbc10 (md5 50bb2801381f (1/22 ok)).

### fuc-zstd-netem-local: A = f06b5834e76e `CZSTD`, B = f06b5834e76e `-DresourceProfile=speed CZSTD`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 1550.0 | 1540.0 | 0.99 | 1.08 0.96 1.02 |

### fuc-zstd-netem-local-vs-up-native: A = up-native `-DflightCompression=zstd`, B = f06b5834e76e `-DresourceProfile=speed CZSTD`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 608.0 | 1540.0 | 2.53 | 2.75 2.58 2.51 |
