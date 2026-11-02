# Wave fc-s3-f06b5834e76e (server comparison), run 41437523179

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

## Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| fc-scan-s3 | f06b5834e76e `-DresourceProfile=speed` | f06b5834e76e `-DresourceProfile=speed -DduckDbExternalFileCache=true` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 0.93 | none |
| fc-scan-s3-vs-up-native | up-native `-` | f06b5834e76e `-DresourceProfile=speed -DduckDbExternalFileCache=true` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.13 | A: scan8 (rows=313803280 errors=4; rows=433075100 errors=1) |
| fc-sf10adbc-s3 | f06b5834e76e `-DresourceProfile=speed` | f06b5834e76e `-DresourceProfile=speed -DduckDbExternalFileCache=true` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | 0.16 | n/a | n/a | none |
| fc-sf10adbc-s3-vs-up-native | up-native `-` | f06b5834e76e `-DresourceProfile=speed -DduckDbExternalFileCache=true` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22) |
| fc-small-s3 | f06b5834e76e `-DresourceProfile=speed` | f06b5834e76e `-DresourceProfile=speed -DduckDbExternalFileCache=true` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | 0.44 | 0.03 | 0.81 | 0.03 | n/a | n/a | n/a | n/a | none |
| fc-small-s3-vs-up-native | up-native `-` | f06b5834e76e `-DresourceProfile=speed -DduckDbExternalFileCache=true` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-adbc8 (640/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc8 (381/640 errors; 509/640 errors; 524/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point) |

## Per job (absolute medians and ratios)

### fc-scan-s3: A = f06b5834e76e `-DresourceProfile=speed`, B = f06b5834e76e `-DresourceProfile=speed -DduckDbExternalFileCache=true`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 395.3 | 365.8 | 0.93 | 0.96 0.91 0.87 |
| lineitem scan x4 | MB/s | 456.3 | 491.8 | 1.08 | 1.08 1.06 1.11 |
| lineitem scan x8 | MB/s | 495.8 | 524.6 | 1.06 | 1.06 1.04 1.06 |
| lineitem export ADBC | MB/s | 465.6 | 476.9 | 1.02 | 1.14 1.02 1.02 |
| server RSS peak | MB | 1418.0 | 2979.0 | 2.10 | 2.11 2.23 2.10 |

### fc-scan-s3-vs-up-native: A = up-native `-`, B = f06b5834e76e `-DresourceProfile=speed -DduckDbExternalFileCache=true`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 322.3 | 365.8 | 1.13 | 1.01 1.13 1.05 |
| lineitem scan x4 | MB/s | 583.0 | 491.8 | 0.84 | 0.86 0.83 0.86 |
| lineitem scan x8 | MB/s | n/a | 524.6 | n/a | - |
| lineitem export ADBC | MB/s | 540.2 | 476.9 | 0.88 | 0.85 0.89 0.91 |
| server RSS peak | MB | 5882.0 | 2979.0 | 0.51 | 0.51 0.55 0.51 |

Correctness gate: A: scan8 (rows=313803280 errors=4; rows=433075100 errors=1).

### fc-sf10adbc-s3: A = f06b5834e76e `-DresourceProfile=speed`, B = f06b5834e76e `-DresourceProfile=speed -DduckDbExternalFileCache=true`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | 262.5 | 42.7 | 0.16 | 0.16 0.17 0.16 |
| server RSS peak | MB | 1809.0 | 3067.0 | 1.70 | 1.91 1.58 1.66 |

### fc-sf10adbc-s3-vs-up-native: A = up-native `-`, B = f06b5834e76e `-DresourceProfile=speed -DduckDbExternalFileCache=true`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | n/a | 42.7 | n/a | - |
| server RSS peak | MB | 1014.0 | 3067.0 | 3.02 | 3.12 3.13 2.92 |

Correctness gate: A: adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22).

### fc-small-s3: A = f06b5834e76e `-DresourceProfile=speed`, B = f06b5834e76e `-DresourceProfile=speed -DduckDbExternalFileCache=true`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 23.7 | 19.3 | 0.81 | 0.72 0.70 0.84 |
| small JDBC c1 p95 | ms | 700.0 | 34.4 | 0.05 | 0.05 0.05 0.05 |
| small JDBC c1 p99 | ms | 758.8 | 45.6 | 0.06 | 0.06 0.03 0.06 |
| small JDBC c8 p50 | ms | 152.3 | 51.7 | 0.34 | 0.34 0.31 0.34 |
| small JDBC c8 p95 | ms | 4013.1 | 114.5 | 0.03 | 0.03 0.03 0.03 |
| small JDBC c8 p99 | ms | 6945.7 | 141.7 | 0.02 | 0.02 0.02 0.02 |
| small JDBC c32 p50 | ms | 429.2 | 130.8 | 0.30 | 0.31 0.29 0.31 |
| small JDBC c32 p95 | ms | 18049.8 | 580.6 | 0.03 | 0.03 0.03 0.03 |
| small JDBC c32 p99 | ms | 20107.6 | 721.7 | 0.04 | 0.03 0.04 0.04 |
| small ADBC c1 p50 | ms | 20.0 | 8.8 | 0.44 | 0.47 0.35 0.44 |
| small ADBC c1 p95 | ms | 717.5 | 24.4 | 0.03 | 0.03 0.03 0.04 |
| small ADBC c1 p99 | ms | 774.3 | 29.1 | 0.04 | 0.04 0.03 0.05 |
| small ADBC c8 p50 | ms | 151.0 | 38.4 | 0.25 | 0.25 0.24 0.26 |
| small ADBC c8 p95 | ms | 4087.7 | 111.8 | 0.03 | 0.03 0.03 0.03 |
| small ADBC c8 p99 | ms | 6894.8 | 141.5 | 0.02 | 0.02 0.02 0.02 |
| small ADBC c32 p50 | ms | 452.6 | 113.8 | 0.25 | 0.25 0.25 0.28 |
| small ADBC c32 p95 | ms | 18000.8 | 544.5 | 0.03 | 0.03 0.03 0.03 |
| small ADBC c32 p99 | ms | 19957.7 | 654.1 | 0.03 | 0.03 0.03 0.03 |
| server RSS peak | MB | 866.0 | 1352.0 | 1.56 | 1.56 1.58 1.53 |

### fc-small-s3-vs-up-native: A = up-native `-`, B = f06b5834e76e `-DresourceProfile=speed -DduckDbExternalFileCache=true`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | n/a | 19.3 | n/a | - |
| small JDBC c1 p95 | ms | n/a | 34.4 | n/a | - |
| small JDBC c1 p99 | ms | n/a | 45.6 | n/a | - |
| small JDBC c8 p50 | ms | n/a | 51.7 | n/a | - |
| small JDBC c8 p95 | ms | n/a | 114.5 | n/a | - |
| small JDBC c8 p99 | ms | n/a | 141.7 | n/a | - |
| small JDBC c32 p50 | ms | n/a | 130.8 | n/a | - |
| small JDBC c32 p95 | ms | n/a | 580.6 | n/a | - |
| small JDBC c32 p99 | ms | n/a | 721.7 | n/a | - |
| small ADBC c1 p50 | ms | n/a | 8.8 | n/a | - |
| small ADBC c1 p95 | ms | n/a | 24.4 | n/a | - |
| small ADBC c1 p99 | ms | n/a | 29.1 | n/a | - |
| small ADBC c8 p50 | ms | n/a | 38.4 | n/a | - |
| small ADBC c8 p95 | ms | n/a | 111.8 | n/a | - |
| small ADBC c8 p99 | ms | n/a | 141.5 | n/a | - |
| small ADBC c32 p50 | ms | n/a | 113.8 | n/a | - |
| small ADBC c32 p95 | ms | n/a | 544.5 | n/a | - |
| small ADBC c32 p99 | ms | n/a | 654.1 | n/a | - |
| server RSS peak | MB | 406.0 | 1352.0 | 3.33 | 3.43 3.33 3.28 |

Correctness gate: A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-adbc8 (640/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc8 (381/640 errors; 509/640 errors; 524/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point).
