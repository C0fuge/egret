# Wave track-1e7b43a4e0c7 (server comparison), run 40876778493

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

## Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| fin-lat-local | ours-new `-` | 1e7b43a4e0c7 `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | 1.00 | 0.99 | 1.00 | 0.97 | n/a | n/a | n/a | 0.98 | none |
| fin-lat-local-vs-up-native | up-native `-` | 1e7b43a4e0c7 `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 0.97 | A: scan8 (rows=464401308 errors=1), server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point) |
| fin-scan-s3 | ours-new `-` | 1e7b43a4e0c7 `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 0.90 | none |
| fin-scan-s3-vs-up-native | up-native `-` | 1e7b43a4e0c7 `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 0.93 | A: scan8 (rows=437924764 errors=1) |
| fin-sf1-s3 | ours-new `-` | 1e7b43a4e0c7 `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 1.00 | n/a | n/a | n/a | none |
| fin-sf1-s3-vs-up-native | up-native `-` | 1e7b43a4e0c7 `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)) |
| fin-sf10adbc-s3 | ours-new `-` | 1e7b43a4e0c7 `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | 0.65 | n/a | n/a | none |
| fin-sf10adbc-s3-vs-up-native | up-native `-` | 1e7b43a4e0c7 `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22) |
| fin-sf10jdbc-s3 | ours-new `-` | 1e7b43a4e0c7 `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | 1.01 | n/a | none |
| fin-sf10jdbc-s3-vs-up-native | up-native `-` | 1e7b43a4e0c7 `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: jdbc10 (md5 50bb2801381f (1/22 ok)) |
| fin-small-s3 | ours-new `-` | 1e7b43a4e0c7 `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | 1.08 | 0.99 | 1.04 | 1.06 | n/a | n/a | n/a | n/a | none |
| fin-small-s3-vs-up-native | up-native `-` | 1e7b43a4e0c7 `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-adbc8 (640/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc8 (504/640 errors; 568/640 errors; 605/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point) |
| fin-tpch-local | ours-new `-` | 1e7b43a4e0c7 `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 0.99 | 1.04 | 1.02 | n/a | none |
| fin-tpch-local-vs-up-native | up-native `-` | 1e7b43a4e0c7 `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)), jdbc10 (md5 50bb2801381f (1/22 ok)) |
| fin-zstd-netem-local | ours-new `-` | 1e7b43a4e0c7 `CZSTD` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| fin-zstd-netem-local-vs-up-native | up-native `-DflightCompression=zstd` | 1e7b43a4e0c7 `CZSTD` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |

## Per job (absolute medians and ratios)

### fin-lat-local: A = ours-new `-`, B = 1e7b43a4e0c7 `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 26.4 | 26.4 | 1.00 | 1.04 0.96 1.00 |
| small JDBC c1 p95 | ms | 55.0 | 51.6 | 0.94 | 0.93 0.94 0.96 |
| small JDBC c1 p99 | ms | 61.2 | 59.5 | 0.97 | 0.98 0.93 1.08 |
| small JDBC c8 p50 | ms | 127.2 | 124.1 | 0.98 | 0.98 1.03 0.88 |
| small JDBC c8 p95 | ms | 290.6 | 283.8 | 0.98 | 0.98 1.00 1.00 |
| small JDBC c8 p99 | ms | 406.7 | 381.3 | 0.94 | 0.94 1.06 1.10 |
| small JDBC c32 p50 | ms | 481.3 | 486.2 | 1.01 | 1.17 0.98 0.96 |
| small JDBC c32 p95 | ms | 1395.0 | 1358.5 | 0.97 | 0.97 0.94 1.06 |
| small JDBC c32 p99 | ms | 2051.6 | 1916.6 | 0.93 | 0.95 0.82 0.98 |
| small ADBC c1 p50 | ms | 17.6 | 17.6 | 1.00 | 1.04 0.91 0.99 |
| small ADBC c1 p95 | ms | 47.5 | 48.6 | 1.02 | 1.02 0.97 1.11 |
| small ADBC c1 p99 | ms | 55.9 | 61.5 | 1.10 | 0.98 1.23 1.10 |
| small ADBC c8 p50 | ms | 115.0 | 114.6 | 1.00 | 1.07 0.96 0.98 |
| small ADBC c8 p95 | ms | 282.9 | 281.6 | 1.00 | 1.00 1.01 0.96 |
| small ADBC c8 p99 | ms | 374.0 | 349.0 | 0.93 | 1.06 0.90 0.88 |
| small ADBC c32 p50 | ms | 448.0 | 448.1 | 1.00 | 1.02 0.97 0.99 |
| small ADBC c32 p95 | ms | 1339.6 | 1328.6 | 0.99 | 0.99 1.00 1.01 |
| small ADBC c32 p99 | ms | 1858.4 | 1822.8 | 0.98 | 1.07 0.98 0.96 |
| lineitem scan x1 | MB/s | 416.1 | 408.4 | 0.98 | 0.92 1.03 1.00 |
| lineitem scan x4 | MB/s | 446.9 | 450.7 | 1.01 | 0.99 1.06 1.02 |
| lineitem scan x8 | MB/s | 414.3 | 416.5 | 1.01 | 0.99 1.02 1.03 |
| lineitem export ADBC | MB/s | 513.9 | 449.5 | 0.87 | 0.82 1.01 1.05 |
| server RSS peak | MB | 1720.0 | 1717.0 | 1.00 | 0.99 0.98 1.00 |

### fin-lat-local-vs-up-native: A = up-native `-`, B = 1e7b43a4e0c7 `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | n/a | 26.4 | n/a | - |
| small JDBC c1 p95 | ms | n/a | 51.6 | n/a | - |
| small JDBC c1 p99 | ms | n/a | 59.5 | n/a | - |
| small JDBC c8 p50 | ms | n/a | 124.1 | n/a | - |
| small JDBC c8 p95 | ms | n/a | 283.8 | n/a | - |
| small JDBC c8 p99 | ms | n/a | 381.3 | n/a | - |
| small JDBC c32 p50 | ms | n/a | 486.2 | n/a | - |
| small JDBC c32 p95 | ms | n/a | 1358.5 | n/a | - |
| small JDBC c32 p99 | ms | n/a | 1916.6 | n/a | - |
| small ADBC c1 p50 | ms | n/a | 17.6 | n/a | - |
| small ADBC c1 p95 | ms | n/a | 48.6 | n/a | - |
| small ADBC c1 p99 | ms | n/a | 61.5 | n/a | - |
| small ADBC c8 p50 | ms | n/a | 114.6 | n/a | - |
| small ADBC c8 p95 | ms | n/a | 281.6 | n/a | - |
| small ADBC c8 p99 | ms | n/a | 349.0 | n/a | - |
| small ADBC c32 p50 | ms | n/a | 448.1 | n/a | - |
| small ADBC c32 p95 | ms | n/a | 1328.6 | n/a | - |
| small ADBC c32 p99 | ms | n/a | 1822.8 | n/a | - |
| lineitem scan x1 | MB/s | 419.4 | 408.4 | 0.97 | 1.02 0.92 0.98 |
| lineitem scan x4 | MB/s | 565.1 | 450.7 | 0.80 | 0.84 0.83 0.78 |
| lineitem scan x8 | MB/s | n/a | 416.5 | n/a | - |
| lineitem export ADBC | MB/s | 544.2 | 449.5 | 0.83 | 0.81 0.96 0.83 |
| server RSS peak | MB | 3638.0 | 1717.0 | 0.47 | 0.48 0.44 0.47 |

Correctness gate: A: scan8 (rows=464401308 errors=1), server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point).

### fin-scan-s3: A = ours-new `-`, B = 1e7b43a4e0c7 `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 535.7 | 481.2 | 0.90 | 1.03 0.88 0.90 |
| lineitem scan x4 | MB/s | 634.8 | 616.2 | 0.97 | 0.90 1.01 1.00 |
| lineitem scan x8 | MB/s | 588.9 | 610.2 | 1.04 | 0.92 1.05 1.07 |
| lineitem export ADBC | MB/s | 620.8 | 615.1 | 0.99 | 0.97 1.00 0.97 |
| server RSS peak | MB | 1762.0 | 1728.0 | 0.98 | 1.03 0.98 0.94 |

### fin-scan-s3-vs-up-native: A = up-native `-`, B = 1e7b43a4e0c7 `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 515.0 | 481.2 | 0.93 | 1.07 0.92 0.85 |
| lineitem scan x4 | MB/s | 825.3 | 616.2 | 0.75 | 0.73 0.75 0.74 |
| lineitem scan x8 | MB/s | n/a | 610.2 | n/a | - |
| lineitem export ADBC | MB/s | 778.5 | 615.1 | 0.79 | 0.85 0.80 0.71 |
| server RSS peak | MB | 5806.0 | 1728.0 | 0.30 | 0.30 0.30 0.29 |

Correctness gate: A: scan8 (rows=437924764 errors=1).

### fin-sf1-s3: A = ours-new `-`, B = 1e7b43a4e0c7 `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 26.3 | 26.4 | 1.00 | 1.01 1.03 0.98 |
| TPC-H SF1 JDBC (sum of medians) | s | 25.7 | 25.9 | 1.01 | 1.01 0.99 1.01 |
| server RSS peak | MB | 728.0 | 742.0 | 1.02 | 0.97 1.02 1.04 |

### fin-sf1-s3-vs-up-native: A = up-native `-`, B = 1e7b43a4e0c7 `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | n/a | 26.4 | n/a | - |
| TPC-H SF1 JDBC (sum of medians) | s | n/a | 25.9 | n/a | - |
| server RSS peak | MB | 576.0 | 742.0 | 1.29 | 1.22 1.20 1.30 |

Correctness gate: A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)).

### fin-sf10adbc-s3: A = ours-new `-`, B = 1e7b43a4e0c7 `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | 455.2 | 297.1 | 0.65 | 1.01 0.65 1.02 |
| server RSS peak | MB | 1727.0 | 1572.0 | 0.91 | 0.91 0.93 0.94 |

### fin-sf10adbc-s3-vs-up-native: A = up-native `-`, B = 1e7b43a4e0c7 `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | n/a | 297.1 | n/a | - |
| server RSS peak | MB | 1022.0 | 1572.0 | 1.54 | 1.64 1.56 1.54 |

Correctness gate: A: adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22).

### fin-sf10jdbc-s3: A = ours-new `-`, B = 1e7b43a4e0c7 `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `sf10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 JDBC (sum of medians) | s | 256.9 | 260.6 | 1.01 | 1.01 1.05 1.06 |
| server RSS peak | MB | 1769.0 | 1598.0 | 0.90 | 0.94 0.90 0.85 |

### fin-sf10jdbc-s3-vs-up-native: A = up-native `-`, B = 1e7b43a4e0c7 `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `sf10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 JDBC (sum of medians) | s | n/a | 260.6 | n/a | - |
| server RSS peak | MB | 1013.0 | 1598.0 | 1.58 | 1.64 1.57 1.49 |

Correctness gate: A: jdbc10 (md5 50bb2801381f (1/22 ok)).

### fin-small-s3: A = ours-new `-`, B = 1e7b43a4e0c7 `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 38.8 | 40.3 | 1.04 | 1.23 1.02 1.05 |
| small JDBC c1 p95 | ms | 794.0 | 809.1 | 1.02 | 1.08 1.06 1.02 |
| small JDBC c1 p99 | ms | 845.2 | 868.9 | 1.03 | 1.01 1.03 0.98 |
| small JDBC c8 p50 | ms | 306.0 | 334.1 | 1.09 | 0.98 0.98 1.17 |
| small JDBC c8 p95 | ms | 5634.5 | 5669.6 | 1.01 | 1.07 0.99 0.95 |
| small JDBC c8 p99 | ms | 6006.6 | 6129.0 | 1.02 | 1.05 0.99 0.97 |
| small JDBC c32 p50 | ms | 1130.7 | 1160.1 | 1.03 | 1.08 0.98 1.62 |
| small JDBC c32 p95 | ms | 17232.4 | 18287.4 | 1.06 | 1.03 1.01 1.44 |
| small JDBC c32 p99 | ms | 20306.4 | 22398.4 | 1.10 | 0.94 1.02 1.32 |
| small ADBC c1 p50 | ms | 24.6 | 26.7 | 1.08 | 1.17 0.99 1.09 |
| small ADBC c1 p95 | ms | 797.8 | 806.8 | 1.01 | 1.03 1.01 1.03 |
| small ADBC c1 p99 | ms | 835.2 | 873.6 | 1.05 | 1.07 1.05 1.00 |
| small ADBC c8 p50 | ms | 347.8 | 303.5 | 0.87 | 0.78 1.00 0.94 |
| small ADBC c8 p95 | ms | 5574.9 | 5730.8 | 1.03 | 1.16 0.97 1.03 |
| small ADBC c8 p99 | ms | 6051.9 | 6500.0 | 1.07 | 1.14 0.67 1.00 |
| small ADBC c32 p50 | ms | 1105.6 | 1170.0 | 1.06 | 1.06 1.00 1.23 |
| small ADBC c32 p95 | ms | 18079.9 | 17979.3 | 0.99 | 1.02 0.99 1.54 |
| small ADBC c32 p99 | ms | 21232.2 | 24504.0 | 1.15 | 1.00 1.15 1.27 |
| server RSS peak | MB | 2175.0 | 2117.0 | 0.97 | 1.00 0.99 0.96 |

### fin-small-s3-vs-up-native: A = up-native `-`, B = 1e7b43a4e0c7 `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | n/a | 40.3 | n/a | - |
| small JDBC c1 p95 | ms | n/a | 809.1 | n/a | - |
| small JDBC c1 p99 | ms | n/a | 868.9 | n/a | - |
| small JDBC c8 p50 | ms | n/a | 334.1 | n/a | - |
| small JDBC c8 p95 | ms | n/a | 5669.6 | n/a | - |
| small JDBC c8 p99 | ms | n/a | 6129.0 | n/a | - |
| small JDBC c32 p50 | ms | n/a | 1160.1 | n/a | - |
| small JDBC c32 p95 | ms | n/a | 18287.4 | n/a | - |
| small JDBC c32 p99 | ms | n/a | 22398.4 | n/a | - |
| small ADBC c1 p50 | ms | n/a | 26.7 | n/a | - |
| small ADBC c1 p95 | ms | n/a | 806.8 | n/a | - |
| small ADBC c1 p99 | ms | n/a | 873.6 | n/a | - |
| small ADBC c8 p50 | ms | n/a | 303.5 | n/a | - |
| small ADBC c8 p95 | ms | n/a | 5730.8 | n/a | - |
| small ADBC c8 p99 | ms | n/a | 6500.0 | n/a | - |
| small ADBC c32 p50 | ms | n/a | 1170.0 | n/a | - |
| small ADBC c32 p95 | ms | n/a | 17979.3 | n/a | - |
| small ADBC c32 p99 | ms | n/a | 24504.0 | n/a | - |
| server RSS peak | MB | 393.0 | 2117.0 | 5.39 | 5.53 5.33 5.42 |

Correctness gate: A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-adbc8 (640/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc8 (504/640 errors; 568/640 errors; 605/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point).

### fin-tpch-local: A = ours-new `-`, B = 1e7b43a4e0c7 `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 3.3 | 3.3 | 0.99 | 0.99 0.98 1.00 |
| TPC-H SF10 ADBC (sum of medians) | s | 33.7 | 35.1 | 1.04 | 1.07 1.06 1.03 |
| TPC-H SF1 JDBC (sum of medians) | s | 3.4 | 3.4 | 0.99 | 0.97 0.99 1.00 |
| TPC-H SF10 JDBC (sum of medians) | s | 33.7 | 34.2 | 1.02 | 1.02 1.02 1.00 |
| server RSS peak | MB | 1710.0 | 1610.0 | 0.94 | 0.87 0.94 0.95 |

### fin-tpch-local-vs-up-native: A = up-native `-`, B = 1e7b43a4e0c7 `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | n/a | 3.3 | n/a | - |
| TPC-H SF10 ADBC (sum of medians) | s | n/a | 35.1 | n/a | - |
| TPC-H SF1 JDBC (sum of medians) | s | n/a | 3.4 | n/a | - |
| TPC-H SF10 JDBC (sum of medians) | s | n/a | 34.2 | n/a | - |
| server RSS peak | MB | 362.0 | 1610.0 | 4.45 | 4.35 4.45 4.48 |

Correctness gate: A: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), jdbc1 (md5 813b233c6193 (1/22 ok)), jdbc10 (md5 50bb2801381f (1/22 ok)).

### fin-zstd-netem-local: A = ours-new `-`, B = 1e7b43a4e0c7 `CZSTD`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 1686.0 | 1478.0 | 0.88 | 0.87 0.88 0.97 |

### fin-zstd-netem-local-vs-up-native: A = up-native `-DflightCompression=zstd`, B = 1e7b43a4e0c7 `CZSTD`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 597.0 | 1478.0 | 2.48 | 2.48 2.48 2.43 |
