# Wave c2-speed (server comparison), run 40481152975

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

## Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| new-vs-27f5-def-lat-local | ours-new `-` | ours-27f5 `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | 1.32 | 1.05 | 1.18 | 1.02 | n/a | n/a | n/a | 1.00 | none |
| new-vs-27f5-def-lat-s3 | ours-new `-` | ours-27f5 `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | 0.66 | 0.94 | 1.11 | 0.91 | n/a | n/a | n/a | 1.01 | none |
| new-vs-27f5-def-tpch-local | ours-new `-` | ours-27f5 `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 1.10 | 1.01 | 0.99 | n/a | none |
| new-vs-27f5-def-tpch-s3 | ours-new `-` | ours-27f5 `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 0.99 | 1.00 | 1.00 | n/a | none |
| new-vs-27f5-t8-lat-local | ours-new `-DduckDbThreads=8` | ours-27f5 `-DduckDbThreads=8` | local | Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | 1.23 | 1.05 | 1.15 | 1.00 | n/a | n/a | n/a | 0.98 | none |
| new-vs-27f5-t8-lat-s3 | ours-new `-DduckDbThreads=8` | ours-27f5 `-DduckDbThreads=8` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | 0.69 | 0.75 | 1.14 | 0.61 | n/a | n/a | n/a | 1.02 | none |
| new-vs-27f5-t8-tpch-local | ours-new `-DduckDbThreads=8` | ours-27f5 `-DduckDbThreads=8` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 1.08 | 1.01 | 1.01 | n/a | none |
| new-vs-27f5-t8-tpch-s3 | ours-new `-DduckDbThreads=8` | ours-27f5 `-DduckDbThreads=8` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/2 | n/a | n/a | n/a | n/a | 1.19 | 0.98 | 0.90 | n/a | none |
| new-vs-main-def-local | ours-new `-` | up-main `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | B: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbcscan (rows=0 errors=1), scan1 (rows=0 errors=1), scan4 (rows=0 errors=4), scan8 (rows=0 errors=8), server (SERVER DIED after adbcscan SERVER DIED after scan SERVER DIED after small), small-adbc32 (960/960 errors; answers differ: count_filter,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders), small-adbc8 (480/480 errors; answers differ: count_filter,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders), small-jdbc1 (80/120 errors; answers differ: count_filter,limit10_ob,point_lineitem,point_orders), small-jdbc32 (960/960 errors; answers differ: count_filter,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders), small-jdbc8 (320/480 errors; answers differ: count_filter,limit10_ob,point_lineitem,point_orders) |
| new-vs-main-def-s3 | ours-new `-` | up-main `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | B: server (START FAILED
) |
| new-vs-main-t8-local | ours-new `-DduckDbThreads=8` | up-main `-DduckDbThreads=8` | local | Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | B: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbcscan (rows=0 errors=1), scan1 (rows=0 errors=1), scan4 (rows=0 errors=4), scan8 (rows=0 errors=8), server (SERVER DIED after adbcscan SERVER DIED after scan SERVER DIED after small), small-adbc32 (960/960 errors; answers differ: count_filter,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders), small-adbc8 (480/480 errors; answers differ: count_filter,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders), small-jdbc1 (80/120 errors; answers differ: count_filter,limit10_ob,point_lineitem,point_orders), small-jdbc32 (960/960 errors; answers differ: count_filter,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders), small-jdbc8 (320/480 errors; answers differ: count_filter,limit10_ob,point_lineitem,point_orders) |
| new-vs-main-t8-s3 | ours-new `-DduckDbThreads=8` | up-main `-DduckDbThreads=8` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | B: server (START FAILED
) |
| new-vs-native-def-s3 | ours-new `-` | up-native `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | B: server (START FAILED
) |
| new-vs-native-t8-s3 | ours-new `-DduckDbThreads=8` | up-native `-DduckDbThreads=8` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | B: server (START FAILED
) |

## Per job (absolute medians and ratios)

### new-vs-27f5-def-lat-local: A = ours-new `-`, B = ours-27f5 `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 20.0 | 23.6 | 1.18 | 1.22 1.17 1.12 |
| small JDBC c1 p95 | ms | 34.1 | 40.0 | 1.17 | 1.13 1.13 1.27 |
| small JDBC c1 p99 | ms | 40.9 | 45.6 | 1.12 | 1.18 1.11 1.29 |
| small JDBC c8 p50 | ms | 83.4 | 100.3 | 1.20 | 1.25 1.16 1.09 |
| small JDBC c8 p95 | ms | 204.1 | 222.7 | 1.09 | 1.07 1.03 1.13 |
| small JDBC c8 p99 | ms | 276.6 | 274.4 | 0.99 | 0.99 0.89 1.15 |
| small JDBC c32 p50 | ms | 287.8 | 331.4 | 1.15 | 1.16 1.17 1.12 |
| small JDBC c32 p95 | ms | 800.4 | 814.2 | 1.02 | 1.04 1.05 1.01 |
| small JDBC c32 p99 | ms | 1015.3 | 1014.0 | 1.00 | 1.01 1.03 0.85 |
| small ADBC c1 p50 | ms | 12.8 | 16.9 | 1.32 | 1.22 1.32 1.32 |
| small ADBC c1 p95 | ms | 27.6 | 32.2 | 1.17 | 1.09 1.29 1.14 |
| small ADBC c1 p99 | ms | 30.2 | 36.3 | 1.20 | 1.20 1.33 1.10 |
| small ADBC c8 p50 | ms | 70.6 | 84.0 | 1.19 | 1.20 1.19 1.14 |
| small ADBC c8 p95 | ms | 176.3 | 194.1 | 1.10 | 1.07 1.10 1.15 |
| small ADBC c8 p99 | ms | 202.8 | 248.2 | 1.22 | 0.92 1.29 1.22 |
| small ADBC c32 p50 | ms | 283.1 | 329.3 | 1.16 | 1.20 1.14 1.16 |
| small ADBC c32 p95 | ms | 817.9 | 858.2 | 1.05 | 1.06 1.05 1.06 |
| small ADBC c32 p99 | ms | 1182.2 | 1177.1 | 1.00 | 0.93 0.98 1.14 |
| lineitem scan x1 | MB/s | 498.8 | 500.8 | 1.00 | 1.03 0.99 0.99 |
| lineitem scan x4 | MB/s | 780.4 | 788.9 | 1.01 | 1.00 1.03 0.99 |
| lineitem scan x8 | MB/s | 782.0 | 777.9 | 0.99 | 0.98 1.00 0.99 |
| lineitem export ADBC | MB/s | 534.3 | 534.6 | 1.00 | 0.99 1.01 1.00 |
| server RSS peak | MB | 2133.0 | 2238.0 | 1.05 | 1.08 1.08 0.89 |

### new-vs-27f5-def-lat-s3: A = ours-new `-`, B = ours-27f5 `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 27.4 | 30.4 | 1.11 | 1.20 1.10 1.09 |
| small JDBC c1 p95 | ms | 682.1 | 682.9 | 1.00 | 1.02 1.00 0.96 |
| small JDBC c1 p99 | ms | 705.1 | 731.0 | 1.04 | 1.03 1.00 1.04 |
| small JDBC c8 p50 | ms | 342.9 | 331.6 | 0.97 | 0.97 0.75 0.95 |
| small JDBC c8 p95 | ms | 5140.7 | 4918.5 | 0.96 | 0.97 0.62 0.98 |
| small JDBC c8 p99 | ms | 5618.1 | 5534.0 | 0.99 | 1.00 0.47 1.03 |
| small JDBC c32 p50 | ms | 1081.4 | 1146.6 | 1.06 | 1.10 0.72 1.00 |
| small JDBC c32 p95 | ms | 18576.0 | 16934.8 | 0.91 | 0.89 0.63 0.99 |
| small JDBC c32 p99 | ms | 26906.1 | 27825.2 | 1.03 | 0.72 0.54 1.63 |
| small ADBC c1 p50 | ms | 36.1 | 23.9 | 0.66 | 1.25 0.68 0.62 |
| small ADBC c1 p95 | ms | 729.7 | 687.6 | 0.94 | 1.07 0.66 0.91 |
| small ADBC c1 p99 | ms | 1136.9 | 737.7 | 0.65 | 0.99 0.67 0.63 |
| small ADBC c8 p50 | ms | 338.1 | 298.5 | 0.88 | 0.87 0.68 1.01 |
| small ADBC c8 p95 | ms | 5293.9 | 5183.4 | 0.98 | 1.04 0.65 0.98 |
| small ADBC c8 p99 | ms | 8582.6 | 5744.5 | 0.67 | 1.36 0.65 0.59 |
| small ADBC c32 p50 | ms | 1120.0 | 1068.9 | 0.95 | 0.91 1.03 0.95 |
| small ADBC c32 p95 | ms | 17301.1 | 16332.2 | 0.94 | 1.04 0.94 0.94 |
| small ADBC c32 p99 | ms | 21020.3 | 19358.6 | 0.92 | 1.29 0.97 0.81 |
| lineitem scan x1 | MB/s | 436.7 | 439.6 | 1.01 | 1.01 0.99 1.01 |
| lineitem scan x4 | MB/s | 691.0 | 696.8 | 1.01 | 1.06 0.96 1.03 |
| lineitem scan x8 | MB/s | 683.0 | 705.6 | 1.03 | 1.03 0.88 1.06 |
| lineitem export ADBC | MB/s | 473.4 | 472.2 | 1.00 | 0.94 1.00 1.00 |
| server RSS peak | MB | 3085.0 | 2924.0 | 0.95 | 0.98 0.95 0.84 |

### new-vs-27f5-def-tpch-local: A = ours-new `-`, B = ours-27f5 `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 1.8 | 1.9 | 1.10 | 1.10 1.07 1.13 |
| TPC-H SF10 ADBC (sum of medians) | s | 16.2 | 16.4 | 1.01 | 1.01 1.00 1.01 |
| TPC-H SF1 JDBC (sum of medians) | s | 1.9 | 2.0 | 1.05 | 1.06 1.04 1.12 |
| TPC-H SF10 JDBC (sum of medians) | s | 16.2 | 16.0 | 0.99 | 1.00 0.99 0.99 |
| server RSS peak | MB | 1764.0 | 1747.0 | 0.99 | 1.03 0.98 0.97 |

### new-vs-27f5-def-tpch-s3: A = ours-new `-`, B = ours-27f5 `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 38.1 | 37.8 | 0.99 | 1.54 0.99 |
| TPC-H SF10 ADBC (sum of medians) | s | 449.0 | 448.5 | 1.00 | 1.61 1.00 |
| TPC-H SF1 JDBC (sum of medians) | s | 36.3 | 36.1 | 0.99 | 1.46 1.00 |
| TPC-H SF10 JDBC (sum of medians) | s | 433.5 | 434.0 | 1.00 | 1.02 0.99 1.01 |
| server RSS peak | MB | 1785.0 | 1738.0 | 0.97 | 0.97 1.08 0.92 |

### new-vs-27f5-t8-lat-local: A = ours-new `-DduckDbThreads=8`, B = ours-27f5 `-DduckDbThreads=8`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `small scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 17.2 | 19.8 | 1.15 | 1.27 1.10 1.05 |
| small JDBC c1 p95 | ms | 30.3 | 33.9 | 1.12 | 1.26 1.10 1.04 |
| small JDBC c1 p99 | ms | 38.5 | 37.9 | 0.99 | 1.33 0.92 0.95 |
| small JDBC c8 p50 | ms | 73.2 | 85.9 | 1.17 | 1.18 1.19 1.07 |
| small JDBC c8 p95 | ms | 177.9 | 180.3 | 1.01 | 1.08 1.08 0.98 |
| small JDBC c8 p99 | ms | 239.7 | 233.9 | 0.98 | 0.95 0.99 1.02 |
| small JDBC c32 p50 | ms | 263.4 | 283.0 | 1.07 | 1.14 1.11 1.04 |
| small JDBC c32 p95 | ms | 706.3 | 707.8 | 1.00 | 1.03 0.88 1.04 |
| small JDBC c32 p99 | ms | 881.3 | 926.2 | 1.05 | 1.05 0.77 1.09 |
| small ADBC c1 p50 | ms | 11.4 | 14.0 | 1.23 | 1.23 1.29 1.11 |
| small ADBC c1 p95 | ms | 24.8 | 26.8 | 1.08 | 1.04 1.19 1.03 |
| small ADBC c1 p99 | ms | 26.8 | 31.6 | 1.18 | 1.11 1.23 1.20 |
| small ADBC c8 p50 | ms | 63.8 | 71.9 | 1.13 | 1.12 1.13 1.15 |
| small ADBC c8 p95 | ms | 151.3 | 154.3 | 1.02 | 1.09 0.99 0.96 |
| small ADBC c8 p99 | ms | 182.8 | 180.7 | 0.99 | 1.03 1.01 0.97 |
| small ADBC c32 p50 | ms | 264.4 | 301.9 | 1.14 | 1.11 1.10 1.19 |
| small ADBC c32 p95 | ms | 653.5 | 687.4 | 1.05 | 1.08 0.99 1.01 |
| small ADBC c32 p99 | ms | 796.7 | 857.2 | 1.08 | 1.05 0.99 1.08 |
| lineitem scan x1 | MB/s | 593.6 | 583.8 | 0.98 | 1.06 0.98 0.96 |
| lineitem scan x4 | MB/s | 932.4 | 952.4 | 1.02 | 1.04 0.99 1.02 |
| lineitem scan x8 | MB/s | 902.5 | 899.0 | 1.00 | 0.98 1.00 1.00 |
| lineitem export ADBC | MB/s | 628.3 | 635.0 | 1.01 | 1.01 1.01 1.00 |
| server RSS peak | MB | 2430.0 | 2539.0 | 1.04 | 1.23 1.00 1.04 |

### new-vs-27f5-t8-lat-s3: A = ours-new `-DduckDbThreads=8`, B = ours-27f5 `-DduckDbThreads=8`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 30.0 | 34.4 | 1.14 | 1.14 1.29 1.00 |
| small JDBC c1 p95 | ms | 758.4 | 748.4 | 0.99 | 1.02 1.03 0.92 |
| small JDBC c1 p99 | ms | 963.5 | 798.0 | 0.83 | 1.00 0.87 0.66 |
| small JDBC c8 p50 | ms | 692.5 | 539.5 | 0.78 | 0.95 0.78 1.08 |
| small JDBC c8 p95 | ms | 6242.1 | 3952.0 | 0.63 | 0.96 0.56 0.93 |
| small JDBC c8 p99 | ms | 7001.6 | 6777.6 | 0.97 | 1.45 0.60 1.19 |
| small JDBC c32 p50 | ms | 2508.1 | 1899.7 | 0.76 | 1.35 0.67 0.95 |
| small JDBC c32 p95 | ms | 21074.6 | 12841.8 | 0.61 | 0.89 0.49 1.08 |
| small JDBC c32 p99 | ms | 31051.9 | 32829.9 | 1.06 | 0.49 0.44 1.82 |
| small ADBC c1 p50 | ms | 36.5 | 25.2 | 0.69 | 1.09 0.58 1.09 |
| small ADBC c1 p95 | ms | 1184.7 | 769.7 | 0.65 | 0.99 0.65 0.92 |
| small ADBC c1 p99 | ms | 1232.5 | 830.8 | 0.67 | 1.03 0.67 1.06 |
| small ADBC c8 p50 | ms | 678.2 | 441.1 | 0.65 | 0.85 0.64 1.08 |
| small ADBC c8 p95 | ms | 6637.9 | 4293.9 | 0.65 | 1.01 0.62 0.89 |
| small ADBC c8 p99 | ms | 8875.0 | 6847.7 | 0.77 | 1.63 0.74 0.53 |
| small ADBC c32 p50 | ms | 2649.7 | 1882.7 | 0.71 | 1.08 0.58 0.94 |
| small ADBC c32 p95 | ms | 20258.4 | 15118.4 | 0.75 | 0.95 0.59 1.11 |
| small ADBC c32 p99 | ms | 24724.8 | 29184.9 | 1.18 | 1.49 0.60 1.82 |
| lineitem scan x1 | MB/s | 416.7 | 423.6 | 1.02 | 1.00 1.04 1.09 |
| lineitem scan x4 | MB/s | 608.2 | 660.3 | 1.09 | 1.09 1.02 1.09 |
| lineitem scan x8 | MB/s | 606.5 | 594.2 | 0.98 | 0.97 1.01 0.95 |
| lineitem export ADBC | MB/s | 461.9 | 431.4 | 0.93 | 0.93 1.03 0.97 |
| server RSS peak | MB | 3342.0 | 3131.0 | 0.94 | 0.90 1.04 0.94 |

### new-vs-27f5-t8-tpch-local: A = ours-new `-DduckDbThreads=8`, B = ours-27f5 `-DduckDbThreads=8`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 2.3 | 2.5 | 1.08 | 1.08 1.07 1.07 |
| TPC-H SF10 ADBC (sum of medians) | s | 20.1 | 20.2 | 1.01 | 1.01 1.00 1.00 |
| TPC-H SF1 JDBC (sum of medians) | s | 2.5 | 2.6 | 1.07 | 1.08 1.09 1.04 |
| TPC-H SF10 JDBC (sum of medians) | s | 20.1 | 20.2 | 1.01 | 1.01 1.01 1.00 |
| server RSS peak | MB | 1920.0 | 1975.0 | 1.03 | 0.98 1.14 1.03 |

### new-vs-27f5-t8-tpch-s3: A = ours-new `-DduckDbThreads=8`, B = ours-27f5 `-DduckDbThreads=8`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 32.9 | 39.2 | 1.19 | 1.50 0.99 |
| TPC-H SF10 ADBC (sum of medians) | s | 499.2 | 489.5 | 0.98 | 1.57 0.98 |
| TPC-H SF1 JDBC (sum of medians) | s | 37.8 | 37.6 | 1.00 | 1.42 1.00 |
| TPC-H SF10 JDBC (sum of medians) | s | 486.2 | 438.6 | 0.90 | 1.25 0.96 |
| server RSS peak | MB | 1956.0 | 1915.5 | 0.98 | 0.98 0.97 |

### new-vs-main-def-local: A = ours-new `-`, B = up-main `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small adbc10 adbc1 scan adbcscan`, small-query classes `meta_tables,meta_schemas,point_orders,point_lineitem,count_filter,limit10_ob`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 26.0 | n/a | n/a | - |
| small JDBC c1 p95 | ms | 37.4 | n/a | n/a | - |
| small JDBC c1 p99 | ms | 41.1 | n/a | n/a | - |
| small JDBC c8 p50 | ms | 107.5 | n/a | n/a | - |
| small JDBC c8 p95 | ms | 235.5 | n/a | n/a | - |
| small JDBC c8 p99 | ms | 323.9 | n/a | n/a | - |
| small JDBC c32 p50 | ms | 401.4 | n/a | n/a | - |
| small JDBC c32 p95 | ms | 938.4 | n/a | n/a | - |
| small JDBC c32 p99 | ms | 1174.2 | n/a | n/a | - |
| small ADBC c1 p50 | ms | 16.6 | n/a | n/a | - |
| small ADBC c1 p95 | ms | 29.9 | n/a | n/a | - |
| small ADBC c1 p99 | ms | 34.8 | n/a | n/a | - |
| small ADBC c8 p50 | ms | 88.2 | n/a | n/a | - |
| small ADBC c8 p95 | ms | 191.9 | n/a | n/a | - |
| small ADBC c8 p99 | ms | 213.2 | n/a | n/a | - |
| small ADBC c32 p50 | ms | 346.0 | n/a | n/a | - |
| small ADBC c32 p95 | ms | 832.8 | n/a | n/a | - |
| small ADBC c32 p99 | ms | 1004.9 | n/a | n/a | - |
| TPC-H SF1 ADBC (sum of medians) | s | 2.3 | n/a | n/a | - |
| TPC-H SF10 ADBC (sum of medians) | s | 20.4 | n/a | n/a | - |
| lineitem scan x1 | MB/s | 481.0 | n/a | n/a | - |
| lineitem scan x4 | MB/s | 766.9 | n/a | n/a | - |
| lineitem scan x8 | MB/s | 775.6 | n/a | n/a | - |
| lineitem export ADBC | MB/s | 528.5 | n/a | n/a | - |
| server RSS peak | MB | 2764.0 | 394.0 | 0.14 | 0.14 0.14 0.14 |

Correctness gate: B: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbcscan (rows=0 errors=1), scan1 (rows=0 errors=1), scan4 (rows=0 errors=4), scan8 (rows=0 errors=8), server (SERVER DIED after adbcscan SERVER DIED after scan SERVER DIED after small), small-adbc32 (960/960 errors; answers differ: count_filter,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders), small-adbc8 (480/480 errors; answers differ: count_filter,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders), small-jdbc1 (80/120 errors; answers differ: count_filter,limit10_ob,point_lineitem,point_orders), small-jdbc32 (960/960 errors; answers differ: count_filter,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders), small-jdbc8 (320/480 errors; answers differ: count_filter,limit10_ob,point_lineitem,point_orders).

### new-vs-main-def-s3: A = ours-new `-`, B = up-main `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small adbc10 adbc1 scan adbcscan`, small-query classes `meta_tables,meta_schemas,point_orders,point_lineitem,count_filter,limit10_ob`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 25.2 | n/a | n/a | - |
| small JDBC c1 p95 | ms | 650.4 | n/a | n/a | - |
| small JDBC c1 p99 | ms | 688.3 | n/a | n/a | - |
| small JDBC c8 p50 | ms | 308.7 | n/a | n/a | - |
| small JDBC c8 p95 | ms | 5604.4 | n/a | n/a | - |
| small JDBC c8 p99 | ms | 5987.9 | n/a | n/a | - |
| small JDBC c32 p50 | ms | 1053.6 | n/a | n/a | - |
| small JDBC c32 p95 | ms | 20522.2 | n/a | n/a | - |
| small JDBC c32 p99 | ms | 27838.7 | n/a | n/a | - |
| small ADBC c1 p50 | ms | 17.5 | n/a | n/a | - |
| small ADBC c1 p95 | ms | 673.1 | n/a | n/a | - |
| small ADBC c1 p99 | ms | 696.9 | n/a | n/a | - |
| small ADBC c8 p50 | ms | 305.8 | n/a | n/a | - |
| small ADBC c8 p95 | ms | 5805.3 | n/a | n/a | - |
| small ADBC c8 p99 | ms | 8750.2 | n/a | n/a | - |
| small ADBC c32 p50 | ms | 1042.1 | n/a | n/a | - |
| small ADBC c32 p95 | ms | 25736.7 | n/a | n/a | - |
| small ADBC c32 p99 | ms | 37534.1 | n/a | n/a | - |
| TPC-H SF1 ADBC (sum of medians) | s | 35.1 | n/a | n/a | - |
| TPC-H SF10 ADBC (sum of medians) | s | 414.5 | n/a | n/a | - |
| lineitem scan x1 | MB/s | 421.3 | n/a | n/a | - |
| lineitem scan x4 | MB/s | 633.6 | n/a | n/a | - |
| lineitem scan x8 | MB/s | 634.2 | n/a | n/a | - |
| lineitem export ADBC | MB/s | 470.8 | n/a | n/a | - |
| server RSS peak | MB | 2271.0 | n/a | n/a | - |

Correctness gate: B: server (START FAILED
).

### new-vs-main-t8-local: A = ours-new `-DduckDbThreads=8`, B = up-main `-DduckDbThreads=8`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `small adbc10 adbc1 scan adbcscan`, small-query classes `meta_tables,meta_schemas,point_orders,point_lineitem,count_filter,limit10_ob`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 23.3 | n/a | n/a | - |
| small JDBC c1 p95 | ms | 37.0 | n/a | n/a | - |
| small JDBC c1 p99 | ms | 38.8 | n/a | n/a | - |
| small JDBC c8 p50 | ms | 85.4 | n/a | n/a | - |
| small JDBC c8 p95 | ms | 182.3 | n/a | n/a | - |
| small JDBC c8 p99 | ms | 235.9 | n/a | n/a | - |
| small JDBC c32 p50 | ms | 298.1 | n/a | n/a | - |
| small JDBC c32 p95 | ms | 777.1 | n/a | n/a | - |
| small JDBC c32 p99 | ms | 1173.8 | n/a | n/a | - |
| small ADBC c1 p50 | ms | 13.6 | n/a | n/a | - |
| small ADBC c1 p95 | ms | 23.6 | n/a | n/a | - |
| small ADBC c1 p99 | ms | 29.3 | n/a | n/a | - |
| small ADBC c8 p50 | ms | 69.3 | n/a | n/a | - |
| small ADBC c8 p95 | ms | 143.0 | n/a | n/a | - |
| small ADBC c8 p99 | ms | 173.9 | n/a | n/a | - |
| small ADBC c32 p50 | ms | 288.5 | n/a | n/a | - |
| small ADBC c32 p95 | ms | 671.2 | n/a | n/a | - |
| small ADBC c32 p99 | ms | 805.4 | n/a | n/a | - |
| TPC-H SF1 ADBC (sum of medians) | s | 1.8 | n/a | n/a | - |
| TPC-H SF10 ADBC (sum of medians) | s | 16.0 | n/a | n/a | - |
| lineitem scan x1 | MB/s | 668.0 | n/a | n/a | - |
| lineitem scan x4 | MB/s | 1029.1 | n/a | n/a | - |
| lineitem scan x8 | MB/s | 1020.8 | n/a | n/a | - |
| lineitem export ADBC | MB/s | 738.9 | n/a | n/a | - |
| server RSS peak | MB | 2862.0 | 452.0 | 0.16 | 0.16 0.16 0.17 |

Correctness gate: B: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbcscan (rows=0 errors=1), scan1 (rows=0 errors=1), scan4 (rows=0 errors=4), scan8 (rows=0 errors=8), server (SERVER DIED after adbcscan SERVER DIED after scan SERVER DIED after small), small-adbc32 (960/960 errors; answers differ: count_filter,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders), small-adbc8 (480/480 errors; answers differ: count_filter,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders), small-jdbc1 (80/120 errors; answers differ: count_filter,limit10_ob,point_lineitem,point_orders), small-jdbc32 (960/960 errors; answers differ: count_filter,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders), small-jdbc8 (320/480 errors; answers differ: count_filter,limit10_ob,point_lineitem,point_orders).

### new-vs-main-t8-s3: A = ours-new `-DduckDbThreads=8`, B = up-main `-DduckDbThreads=8`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small adbc10 adbc1 scan adbcscan`, small-query classes `meta_tables,meta_schemas,point_orders,point_lineitem,count_filter,limit10_ob`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 28.0 | n/a | n/a | - |
| small JDBC c1 p95 | ms | 783.3 | n/a | n/a | - |
| small JDBC c1 p99 | ms | 831.3 | n/a | n/a | - |
| small JDBC c8 p50 | ms | 463.7 | n/a | n/a | - |
| small JDBC c8 p95 | ms | 4992.1 | n/a | n/a | - |
| small JDBC c8 p99 | ms | 5404.7 | n/a | n/a | - |
| small JDBC c32 p50 | ms | 1931.0 | n/a | n/a | - |
| small JDBC c32 p95 | ms | 33080.6 | n/a | n/a | - |
| small JDBC c32 p99 | ms | 66296.2 | n/a | n/a | - |
| small ADBC c1 p50 | ms | 19.4 | n/a | n/a | - |
| small ADBC c1 p95 | ms | 793.9 | n/a | n/a | - |
| small ADBC c1 p99 | ms | 836.1 | n/a | n/a | - |
| small ADBC c8 p50 | ms | 478.7 | n/a | n/a | - |
| small ADBC c8 p95 | ms | 5048.0 | n/a | n/a | - |
| small ADBC c8 p99 | ms | 9746.2 | n/a | n/a | - |
| small ADBC c32 p50 | ms | 1693.6 | n/a | n/a | - |
| small ADBC c32 p95 | ms | 19436.8 | n/a | n/a | - |
| small ADBC c32 p99 | ms | 44721.5 | n/a | n/a | - |
| TPC-H SF1 ADBC (sum of medians) | s | 37.6 | n/a | n/a | - |
| TPC-H SF10 ADBC (sum of medians) | s | 515.5 | n/a | n/a | - |
| lineitem scan x1 | MB/s | 427.3 | n/a | n/a | - |
| lineitem scan x4 | MB/s | 583.7 | n/a | n/a | - |
| lineitem scan x8 | MB/s | 582.5 | n/a | n/a | - |
| lineitem export ADBC | MB/s | 462.0 | n/a | n/a | - |
| server RSS peak | MB | 2666.0 | n/a | n/a | - |

Correctness gate: B: server (START FAILED
).

### new-vs-native-def-s3: A = ours-new `-`, B = up-native `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small adbc10 adbc1 scan adbcscan`, small-query classes `meta_tables,meta_schemas,point_orders,point_lineitem,count_filter,limit10_ob`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 26.2 | n/a | n/a | - |
| small JDBC c1 p95 | ms | 672.2 | n/a | n/a | - |
| small JDBC c1 p99 | ms | 701.9 | n/a | n/a | - |
| small JDBC c8 p50 | ms | 298.6 | n/a | n/a | - |
| small JDBC c8 p95 | ms | 5904.2 | n/a | n/a | - |
| small JDBC c8 p99 | ms | 6183.8 | n/a | n/a | - |
| small JDBC c32 p50 | ms | 1014.6 | n/a | n/a | - |
| small JDBC c32 p95 | ms | 23369.5 | n/a | n/a | - |
| small JDBC c32 p99 | ms | 34171.8 | n/a | n/a | - |
| small ADBC c1 p50 | ms | 17.8 | n/a | n/a | - |
| small ADBC c1 p95 | ms | 666.1 | n/a | n/a | - |
| small ADBC c1 p99 | ms | 711.9 | n/a | n/a | - |
| small ADBC c8 p50 | ms | 289.2 | n/a | n/a | - |
| small ADBC c8 p95 | ms | 5800.3 | n/a | n/a | - |
| small ADBC c8 p99 | ms | 6104.4 | n/a | n/a | - |
| small ADBC c32 p50 | ms | 1051.3 | n/a | n/a | - |
| small ADBC c32 p95 | ms | 23675.7 | n/a | n/a | - |
| small ADBC c32 p99 | ms | 36580.0 | n/a | n/a | - |
| TPC-H SF1 ADBC (sum of medians) | s | 35.1 | n/a | n/a | - |
| TPC-H SF10 ADBC (sum of medians) | s | 397.3 | n/a | n/a | - |
| lineitem scan x1 | MB/s | 432.7 | n/a | n/a | - |
| lineitem scan x4 | MB/s | 625.9 | n/a | n/a | - |
| lineitem scan x8 | MB/s | 630.5 | n/a | n/a | - |
| lineitem export ADBC | MB/s | 445.3 | n/a | n/a | - |
| server RSS peak | MB | 2259.0 | n/a | n/a | - |

Correctness gate: B: server (START FAILED
).

### new-vs-native-t8-s3: A = ours-new `-DduckDbThreads=8`, B = up-native `-DduckDbThreads=8`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `small adbc10 adbc1 scan adbcscan`, small-query classes `meta_tables,meta_schemas,point_orders,point_lineitem,count_filter,limit10_ob`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 22.5 | n/a | n/a | - |
| small JDBC c1 p95 | ms | 783.4 | n/a | n/a | - |
| small JDBC c1 p99 | ms | 968.7 | n/a | n/a | - |
| small JDBC c8 p50 | ms | 377.5 | n/a | n/a | - |
| small JDBC c8 p95 | ms | 3779.2 | n/a | n/a | - |
| small JDBC c8 p99 | ms | 4079.5 | n/a | n/a | - |
| small JDBC c32 p50 | ms | 1330.9 | n/a | n/a | - |
| small JDBC c32 p95 | ms | 12659.3 | n/a | n/a | - |
| small JDBC c32 p99 | ms | 14508.8 | n/a | n/a | - |
| small ADBC c1 p50 | ms | 17.2 | n/a | n/a | - |
| small ADBC c1 p95 | ms | 717.8 | n/a | n/a | - |
| small ADBC c1 p99 | ms | 996.7 | n/a | n/a | - |
| small ADBC c8 p50 | ms | 387.0 | n/a | n/a | - |
| small ADBC c8 p95 | ms | 3807.3 | n/a | n/a | - |
| small ADBC c8 p99 | ms | 4003.2 | n/a | n/a | - |
| small ADBC c32 p50 | ms | 1534.0 | n/a | n/a | - |
| small ADBC c32 p95 | ms | 13518.8 | n/a | n/a | - |
| small ADBC c32 p99 | ms | 35789.4 | n/a | n/a | - |
| TPC-H SF1 ADBC (sum of medians) | s | 31.5 | n/a | n/a | - |
| TPC-H SF10 ADBC (sum of medians) | s | 266.1 | n/a | n/a | - |
| lineitem scan x1 | MB/s | 416.4 | n/a | n/a | - |
| lineitem scan x4 | MB/s | 791.8 | n/a | n/a | - |
| lineitem scan x8 | MB/s | 730.2 | n/a | n/a | - |
| lineitem export ADBC | MB/s | 503.1 | n/a | n/a | - |
| server RSS peak | MB | 2563.0 | n/a | n/a | - |

Correctness gate: B: server (START FAILED
).
