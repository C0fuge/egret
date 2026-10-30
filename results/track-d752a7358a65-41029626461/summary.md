# Wave track-d752a7358a65 (server comparison), run 41029626461

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

## Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| i23-load-local | d752a7358a65 `-` | d752a7358a65 `-DresourceProfile=speed` | local | Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| i23-load-local-vs-up-native | up-native `-` | d752a7358a65 `-DresourceProfile=speed` | local | Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| i23-scan-local | d752a7358a65 `-` | d752a7358a65 `-DresourceProfile=speed` | local | Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.07 | none |
| i23-scan-local-vs-up-native | up-native `-` | d752a7358a65 `-DresourceProfile=speed` | local | Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.13 | A: scan8 (rows=340431508 errors=3) |
| i23-scan-s3 | d752a7358a65 `-` | d752a7358a65 `-DresourceProfile=speed` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.01 | none |
| i23-scan-s3-vs-up-native | up-native `-` | d752a7358a65 `-DresourceProfile=speed` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 0.96 | A: scan8 (rows=288834064 errors=4; rows=429077404 errors=1; rows=429732764 errors=1) |
| i23-sf1-s3 | d752a7358a65 `-` | d752a7358a65 `-DresourceProfile=speed` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 0.95 | n/a | n/a | n/a | none |
| i23-sf1-s3-vs-up-native | up-native `-` | d752a7358a65 `-DresourceProfile=speed` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)) |
| i23-sf10adbc-s3 | d752a7358a65 `-` | d752a7358a65 `-DresourceProfile=speed` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | 0.81 | n/a | n/a | none |
| i23-sf10adbc-s3-vs-up-native | up-native `-` | d752a7358a65 `-DresourceProfile=speed` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22) |
| i23-sf10jdbc-s3 | d752a7358a65 `-` | d752a7358a65 `-DresourceProfile=speed` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | 0.81 | n/a | none |
| i23-sf10jdbc-s3-vs-up-native | up-native `-` | d752a7358a65 `-DresourceProfile=speed` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: jdbc10 (md5 50bb2801381f (1/22 ok)) |
| i23-small-local | d752a7358a65 `-` | d752a7358a65 `-DresourceProfile=speed` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | 1.06 | 0.91 | 1.13 | 0.87 | n/a | n/a | n/a | n/a | none |
| i23-small-local-vs-up-native | up-native `-` | d752a7358a65 `-DresourceProfile=speed` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point) |
| i23-small-s3 | d752a7358a65 `-` | d752a7358a65 `-DresourceProfile=speed` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | 0.97 | n/a | 1.07 | n/a | n/a | n/a | n/a | n/a | B: small-adbc32 (702/1280 errors; 753/1280 errors; answers differ: count_filter,limit10,limit10_ob,point_lineitem,point_orders,prep_point), small-jdbc32 (66/1280 errors; 72/1280 errors; 91/1280 errors; answers differ: count_filter,limit10,limit10_ob,point_lineitem,point_orders,prep_point) |
| i23-small-s3-vs-up-native | up-native `-` | d752a7358a65 `-DresourceProfile=speed` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-adbc8 (640/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc8 (373/640 errors; 379/640 errors; 528/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point); B: small-adbc32 (702/1280 errors; 753/1280 errors; answers differ: count_filter,limit10,limit10_ob,point_lineitem,point_orders,prep_point), small-jdbc32 (66/1280 errors; 72/1280 errors; 91/1280 errors; answers differ: count_filter,limit10,limit10_ob,point_lineitem,point_orders,prep_point) |
| i23-tpch-local | d752a7358a65 `-` | d752a7358a65 `-DresourceProfile=speed` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 0.93 | 0.97 | 0.98 | n/a | none |
| i23-tpch-local-vs-up-native | up-native `-` | d752a7358a65 `-DresourceProfile=speed` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)), jdbc10 (md5 50bb2801381f (1/22 ok)) |
| i23-zstd-netem-local | d752a7358a65 `CZSTD` | d752a7358a65 `-DresourceProfile=speed CZSTD` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| i23-zstd-netem-local-vs-up-native | up-native `-DflightCompression=zstd` | d752a7358a65 `-DresourceProfile=speed CZSTD` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |

## Per job (absolute medians and ratios)

### i23-load-local: A = d752a7358a65 `-`, B = d752a7358a65 `-DresourceProfile=speed`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 4970.0 | 4122.0 | 0.83 | 0.80 0.84 0.82 |

### i23-load-local-vs-up-native: A = up-native `-`, B = d752a7358a65 `-DresourceProfile=speed`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 4896.0 | 4122.0 | 0.84 | 0.84 0.89 0.83 |

### i23-scan-local: A = d752a7358a65 `-`, B = d752a7358a65 `-DresourceProfile=speed`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 683.7 | 728.3 | 1.07 | 1.06 1.08 1.08 |
| lineitem scan x4 | MB/s | 722.8 | 918.2 | 1.27 | 1.27 1.31 1.30 |
| lineitem scan x8 | MB/s | 650.0 | 930.4 | 1.43 | 1.43 1.51 1.42 |
| lineitem export ADBC | MB/s | 792.6 | 856.6 | 1.08 | 1.09 1.09 1.04 |
| server RSS peak | MB | 1246.0 | 883.0 | 0.71 | 0.72 0.72 0.69 |

### i23-scan-local-vs-up-native: A = up-native `-`, B = d752a7358a65 `-DresourceProfile=speed`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 646.2 | 728.3 | 1.13 | 1.10 1.15 1.13 |
| lineitem scan x4 | MB/s | 866.4 | 918.2 | 1.06 | 1.06 1.05 1.13 |
| lineitem scan x8 | MB/s | n/a | 930.4 | n/a | - |
| lineitem export ADBC | MB/s | 826.3 | 856.6 | 1.04 | 1.05 1.04 1.02 |
| server RSS peak | MB | 3677.0 | 883.0 | 0.24 | 0.24 0.24 0.24 |

Correctness gate: A: scan8 (rows=340431508 errors=3).

### i23-scan-s3: A = d752a7358a65 `-`, B = d752a7358a65 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 284.9 | 288.8 | 1.01 | 0.77 1.02 1.14 |
| lineitem scan x4 | MB/s | 440.5 | 479.8 | 1.09 | 1.12 0.88 1.15 |
| lineitem scan x8 | MB/s | 446.1 | 605.6 | 1.36 | 1.44 1.28 1.38 |
| lineitem export ADBC | MB/s | 354.7 | 311.8 | 0.88 | 0.60 1.07 1.04 |
| server RSS peak | MB | 1700.0 | 1137.0 | 0.67 | 0.66 0.67 0.68 |

### i23-scan-s3-vs-up-native: A = up-native `-`, B = d752a7358a65 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 300.1 | 288.8 | 0.96 | 0.82 1.11 1.09 |
| lineitem scan x4 | MB/s | 687.8 | 479.8 | 0.70 | 0.75 0.61 0.68 |
| lineitem scan x8 | MB/s | n/a | 605.6 | n/a | - |
| lineitem export ADBC | MB/s | 650.4 | 311.8 | 0.48 | 0.33 0.48 0.55 |
| server RSS peak | MB | 5885.0 | 1137.0 | 0.19 | 0.19 0.19 0.20 |

Correctness gate: A: scan8 (rows=288834064 errors=4; rows=429077404 errors=1; rows=429732764 errors=1).

### i23-sf1-s3: A = d752a7358a65 `-`, B = d752a7358a65 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 26.1 | 24.9 | 0.95 | 0.96 0.95 0.94 |
| TPC-H SF1 JDBC (sum of medians) | s | 26.5 | 24.9 | 0.94 | 0.94 0.96 0.94 |
| server RSS peak | MB | 737.0 | 737.0 | 1.00 | 1.00 0.88 1.06 |

### i23-sf1-s3-vs-up-native: A = up-native `-`, B = d752a7358a65 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | n/a | 24.9 | n/a | - |
| TPC-H SF1 JDBC (sum of medians) | s | n/a | 24.9 | n/a | - |
| server RSS peak | MB | 627.0 | 737.0 | 1.18 | 1.22 1.04 1.19 |

Correctness gate: A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)).

### i23-sf10adbc-s3: A = d752a7358a65 `-`, B = d752a7358a65 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | 323.5 | 262.1 | 0.81 | 1.01 0.81 0.98 |
| server RSS peak | MB | 1600.0 | 1925.0 | 1.20 | 1.24 1.20 0.97 |

### i23-sf10adbc-s3-vs-up-native: A = up-native `-`, B = d752a7358a65 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | n/a | 262.1 | n/a | - |
| server RSS peak | MB | 982.0 | 1925.0 | 1.96 | 1.88 1.96 1.63 |

Correctness gate: A: adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22).

### i23-sf10jdbc-s3: A = d752a7358a65 `-`, B = d752a7358a65 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `sf10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 JDBC (sum of medians) | s | 329.4 | 266.1 | 0.81 | 1.02 0.81 0.93 |
| server RSS peak | MB | 1559.0 | 1495.0 | 0.96 | 1.09 0.93 0.92 |

### i23-sf10jdbc-s3-vs-up-native: A = up-native `-`, B = d752a7358a65 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `sf10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 JDBC (sum of medians) | s | n/a | 266.1 | n/a | - |
| server RSS peak | MB | 987.0 | 1495.0 | 1.51 | 1.73 1.52 1.41 |

Correctness gate: A: jdbc10 (md5 50bb2801381f (1/22 ok)).

### i23-small-local: A = d752a7358a65 `-`, B = d752a7358a65 `-DresourceProfile=speed`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 22.5 | 25.4 | 1.13 | 1.14 0.96 1.14 |
| small JDBC c1 p95 | ms | 49.1 | 48.9 | 0.99 | 0.98 0.97 0.99 |
| small JDBC c1 p99 | ms | 56.8 | 54.9 | 0.97 | 0.97 0.97 0.97 |
| small JDBC c8 p50 | ms | 120.9 | 76.5 | 0.63 | 0.60 0.67 0.63 |
| small JDBC c8 p95 | ms | 291.6 | 309.4 | 1.06 | 1.00 1.08 1.06 |
| small JDBC c8 p99 | ms | 405.5 | 359.5 | 0.89 | 0.80 0.89 0.96 |
| small JDBC c32 p50 | ms | 461.2 | 251.7 | 0.55 | 0.57 0.48 0.55 |
| small JDBC c32 p95 | ms | 1320.7 | 1144.4 | 0.87 | 0.86 0.88 0.84 |
| small JDBC c32 p99 | ms | 1909.5 | 1297.4 | 0.68 | 0.64 0.69 0.70 |
| small ADBC c1 p50 | ms | 15.8 | 16.7 | 1.06 | 1.06 1.07 1.06 |
| small ADBC c1 p95 | ms | 43.5 | 44.0 | 1.01 | 0.94 1.04 0.93 |
| small ADBC c1 p99 | ms | 57.1 | 61.0 | 1.07 | 0.92 1.13 1.14 |
| small ADBC c8 p50 | ms | 107.6 | 66.8 | 0.62 | 0.62 0.63 0.64 |
| small ADBC c8 p95 | ms | 278.4 | 319.5 | 1.15 | 1.10 1.07 1.19 |
| small ADBC c8 p99 | ms | 339.8 | 358.7 | 1.06 | 1.01 1.09 1.13 |
| small ADBC c32 p50 | ms | 444.4 | 223.7 | 0.50 | 0.49 0.49 0.52 |
| small ADBC c32 p95 | ms | 1237.9 | 1121.2 | 0.91 | 0.84 0.91 0.91 |
| small ADBC c32 p99 | ms | 1749.1 | 1272.3 | 0.73 | 0.73 0.75 0.80 |
| server RSS peak | MB | 1514.0 | 1196.0 | 0.79 | 0.79 0.76 0.77 |

### i23-small-local-vs-up-native: A = up-native `-`, B = d752a7358a65 `-DresourceProfile=speed`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | n/a | 25.4 | n/a | - |
| small JDBC c1 p95 | ms | n/a | 48.9 | n/a | - |
| small JDBC c1 p99 | ms | n/a | 54.9 | n/a | - |
| small JDBC c8 p50 | ms | n/a | 76.5 | n/a | - |
| small JDBC c8 p95 | ms | n/a | 309.4 | n/a | - |
| small JDBC c8 p99 | ms | n/a | 359.5 | n/a | - |
| small JDBC c32 p50 | ms | n/a | 251.7 | n/a | - |
| small JDBC c32 p95 | ms | n/a | 1144.4 | n/a | - |
| small JDBC c32 p99 | ms | n/a | 1297.4 | n/a | - |
| small ADBC c1 p50 | ms | n/a | 16.7 | n/a | - |
| small ADBC c1 p95 | ms | n/a | 44.0 | n/a | - |
| small ADBC c1 p99 | ms | n/a | 61.0 | n/a | - |
| small ADBC c8 p50 | ms | n/a | 66.8 | n/a | - |
| small ADBC c8 p95 | ms | n/a | 319.5 | n/a | - |
| small ADBC c8 p99 | ms | n/a | 358.7 | n/a | - |
| small ADBC c32 p50 | ms | n/a | 223.7 | n/a | - |
| small ADBC c32 p95 | ms | n/a | 1121.2 | n/a | - |
| small ADBC c32 p99 | ms | n/a | 1272.3 | n/a | - |
| server RSS peak | MB | 245.0 | 1196.0 | 4.88 | 4.89 4.75 4.76 |

Correctness gate: A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point).

### i23-small-s3: A = d752a7358a65 `-`, B = d752a7358a65 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 26.9 | 28.8 | 1.07 | 1.07 1.08 1.07 |
| small JDBC c1 p95 | ms | 687.0 | 691.8 | 1.01 | 1.05 0.97 1.01 |
| small JDBC c1 p99 | ms | 756.2 | 768.3 | 1.02 | 1.02 0.51 1.07 |
| small JDBC c8 p50 | ms | 261.9 | 142.9 | 0.55 | 0.50 0.54 0.58 |
| small JDBC c8 p95 | ms | 3872.8 | 5569.3 | 1.44 | 1.41 1.44 1.52 |
| small JDBC c8 p99 | ms | 4148.1 | 6170.3 | 1.49 | 1.40 1.64 1.52 |
| small JDBC c32 p50 | ms | 984.6 | n/a | n/a | - |
| small JDBC c32 p95 | ms | 12912.6 | n/a | n/a | - |
| small JDBC c32 p99 | ms | 14895.4 | n/a | n/a | - |
| small ADBC c1 p50 | ms | 20.8 | 20.1 | 0.97 | 0.97 0.88 0.92 |
| small ADBC c1 p95 | ms | 695.9 | 687.7 | 0.99 | 0.98 0.98 1.07 |
| small ADBC c1 p99 | ms | 757.9 | 783.0 | 1.03 | 1.02 0.88 1.03 |
| small ADBC c8 p50 | ms | 248.4 | 133.0 | 0.54 | 0.54 0.61 0.49 |
| small ADBC c8 p95 | ms | 3904.6 | 5526.3 | 1.42 | 1.42 1.38 1.46 |
| small ADBC c8 p99 | ms | 4184.4 | 5957.0 | 1.42 | 1.42 1.39 1.49 |
| small ADBC c32 p50 | ms | 908.5 | n/a | n/a | - |
| small ADBC c32 p95 | ms | 13113.3 | n/a | n/a | - |
| small ADBC c32 p99 | ms | 14868.8 | n/a | n/a | - |
| server RSS peak | MB | 2280.0 | 1555.0 | 0.68 | 0.69 0.68 0.68 |

Correctness gate: B: small-adbc32 (702/1280 errors; 753/1280 errors; answers differ: count_filter,limit10,limit10_ob,point_lineitem,point_orders,prep_point), small-jdbc32 (66/1280 errors; 72/1280 errors; 91/1280 errors; answers differ: count_filter,limit10,limit10_ob,point_lineitem,point_orders,prep_point).

### i23-small-s3-vs-up-native: A = up-native `-`, B = d752a7358a65 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | n/a | 28.8 | n/a | - |
| small JDBC c1 p95 | ms | n/a | 691.8 | n/a | - |
| small JDBC c1 p99 | ms | n/a | 768.3 | n/a | - |
| small JDBC c8 p50 | ms | n/a | 142.9 | n/a | - |
| small JDBC c8 p95 | ms | n/a | 5569.3 | n/a | - |
| small JDBC c8 p99 | ms | n/a | 6170.3 | n/a | - |
| small JDBC c32 p50 | ms | n/a | n/a | n/a | - |
| small JDBC c32 p95 | ms | n/a | n/a | n/a | - |
| small JDBC c32 p99 | ms | n/a | n/a | n/a | - |
| small ADBC c1 p50 | ms | n/a | 20.1 | n/a | - |
| small ADBC c1 p95 | ms | n/a | 687.7 | n/a | - |
| small ADBC c1 p99 | ms | n/a | 783.0 | n/a | - |
| small ADBC c8 p50 | ms | n/a | 133.0 | n/a | - |
| small ADBC c8 p95 | ms | n/a | 5526.3 | n/a | - |
| small ADBC c8 p99 | ms | n/a | 5957.0 | n/a | - |
| small ADBC c32 p50 | ms | n/a | n/a | n/a | - |
| small ADBC c32 p95 | ms | n/a | n/a | n/a | - |
| small ADBC c32 p99 | ms | n/a | n/a | n/a | - |
| server RSS peak | MB | 405.0 | 1555.0 | 3.84 | 3.75 3.91 3.84 |

Correctness gate: A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-adbc8 (640/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc8 (373/640 errors; 379/640 errors; 528/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point); B: small-adbc32 (702/1280 errors; 753/1280 errors; answers differ: count_filter,limit10,limit10_ob,point_lineitem,point_orders,prep_point), small-jdbc32 (66/1280 errors; 72/1280 errors; 91/1280 errors; answers differ: count_filter,limit10,limit10_ob,point_lineitem,point_orders,prep_point).

### i23-tpch-local: A = d752a7358a65 `-`, B = d752a7358a65 `-DresourceProfile=speed`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 4.2 | 3.9 | 0.93 | 0.93 0.95 0.92 |
| TPC-H SF10 ADBC (sum of medians) | s | 43.9 | 42.6 | 0.97 | 0.98 0.97 0.96 |
| TPC-H SF1 JDBC (sum of medians) | s | 4.2 | 4.0 | 0.95 | 0.94 0.95 0.93 |
| TPC-H SF10 JDBC (sum of medians) | s | 43.3 | 42.5 | 0.98 | 0.97 0.98 1.00 |
| server RSS peak | MB | 1521.0 | 1905.0 | 1.25 | 1.21 1.25 0.99 |

### i23-tpch-local-vs-up-native: A = up-native `-`, B = d752a7358a65 `-DresourceProfile=speed`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | n/a | 3.9 | n/a | - |
| TPC-H SF10 ADBC (sum of medians) | s | n/a | 42.6 | n/a | - |
| TPC-H SF1 JDBC (sum of medians) | s | n/a | 4.0 | n/a | - |
| TPC-H SF10 JDBC (sum of medians) | s | n/a | 42.5 | n/a | - |
| server RSS peak | MB | 366.0 | 1905.0 | 5.20 | 5.28 5.12 4.22 |

Correctness gate: A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)), jdbc10 (md5 50bb2801381f (1/22 ok)).

### i23-zstd-netem-local: A = d752a7358a65 `CZSTD`, B = d752a7358a65 `-DresourceProfile=speed CZSTD`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 1543.0 | 1390.0 | 0.90 | 0.99 0.90 0.86 |

### i23-zstd-netem-local-vs-up-native: A = up-native `-DflightCompression=zstd`, B = d752a7358a65 `-DresourceProfile=speed CZSTD`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 613.0 | 1390.0 | 2.27 | 2.24 2.27 2.23 |
