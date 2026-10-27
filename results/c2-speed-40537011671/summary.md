# Wave c2-speed (server comparison), run 40537011671

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

## Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| new-vs-27f5-def-lat-local | ours-new `-` | ours-27f5 `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | 1.19 | 1.15 | 1.14 | 1.06 | n/a | n/a | n/a | 1.10 | none |
| new-vs-27f5-def-lat-s3 | ours-new `-` | ours-27f5 `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | 1.19 | 0.98 | 1.16 | 1.00 | n/a | n/a | n/a | 1.04 | none |
| new-vs-27f5-def-tpch-local | ours-new `-` | ours-27f5 `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 1.02 | 0.97 | 0.97 | n/a | none |
| new-vs-27f5-def-tpch-s3 | ours-new `-` | ours-27f5 `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 0.98 | 1.00 | 1.00 | n/a | none |
| new-vs-27f5-t8-lat-local | ours-new `-DduckDbThreads=8` | ours-27f5 `-DduckDbThreads=8` | local | Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | 1.24 | 1.10 | 1.13 | 1.01 | n/a | n/a | n/a | 0.99 | none |
| new-vs-27f5-t8-lat-s3 | ours-new `-DduckDbThreads=8` | ours-27f5 `-DduckDbThreads=8` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | 1.18 | 0.95 | 1.23 | 0.91 | n/a | n/a | n/a | 0.97 | none |
| new-vs-27f5-t8-tpch-local | ours-new `-DduckDbThreads=8` | ours-27f5 `-DduckDbThreads=8` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 1.07 | 1.00 | 1.00 | n/a | none |
| new-vs-27f5-t8-tpch-s3 | ours-new `-DduckDbThreads=8` | ours-27f5 `-DduckDbThreads=8` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 1.02 | 1.00 | 0.74 | n/a | none |
| new-vs-main-def-lat-local | ours-new `-` | up-main `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | B: adbcscan (rows=0 errors=1), scan1 (rows=0 errors=1), scan4 (rows=0 errors=4), scan8 (rows=0 errors=8), server (SERVER DIED after adbcscan SERVER DIED after scan SERVER DIED after small), small-adbc32 (960/960 errors; answers differ: count_filter,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders), small-adbc8 (480/480 errors; answers differ: count_filter,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders), small-jdbc1 (80/120 errors; answers differ: count_filter,limit10_ob,point_lineitem,point_orders), small-jdbc32 (960/960 errors; answers differ: count_filter,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders), small-jdbc8 (320/480 errors; answers differ: count_filter,limit10_ob,point_lineitem,point_orders) |
| new-vs-main-def-tpch-local | ours-new `-` | up-main `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | B: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22) |
| new-vs-main-t8-lat-local | ours-new `-DduckDbThreads=8` | up-main `-DduckDbThreads=8` | local | Linux ubuntu24 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | B: adbcscan (rows=0 errors=1), scan1 (rows=0 errors=1), scan4 (rows=0 errors=4), scan8 (rows=0 errors=8), server (SERVER DIED after adbcscan SERVER DIED after scan SERVER DIED after small), small-adbc32 (960/960 errors; answers differ: count_filter,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders), small-adbc8 (480/480 errors; answers differ: count_filter,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders), small-jdbc1 (80/120 errors; answers differ: count_filter,limit10_ob,point_lineitem,point_orders), small-jdbc32 (960/960 errors; answers differ: count_filter,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders), small-jdbc8 (320/480 errors; answers differ: count_filter,limit10_ob,point_lineitem,point_orders) |
| new-vs-main-t8-tpch-local | ours-new `-DduckDbThreads=8` | up-main `-DduckDbThreads=8` | local | Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | B: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22) |
| new-vs-native-def-lat-local | ours-new `-` | up-native `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.02 | B: server (SERVER DIED after small), small-adbc32 (960/960 errors; answers differ: count_filter,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders), small-jdbc1 (answers differ: limit10_ob), small-jdbc32 (960/960 errors; answers differ: count_filter,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders), small-jdbc8 (34/480 errors; 38/480 errors; 42/480 errors; answers differ: limit10_ob) |
| new-vs-native-def-lat-s3 | ours-new `-` | up-native `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 0.94 | B: scan8 (rows=128712704 errors=8), server (SERVER DIED after scan SERVER DIED after small; SERVER DIED after small), small-adbc32 (960/960 errors; answers differ: count_filter,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders), small-adbc8 (480/480 errors; answers differ: count_filter,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders), small-jdbc1 (answers differ: limit10_ob), small-jdbc32 (960/960 errors; answers differ: count_filter,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders), small-jdbc8 (251/480 errors; 257/480 errors; answers differ: count_filter,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders) |
| new-vs-native-def-tpch-local | ours-new `-` | up-native `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | B: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22) |
| new-vs-native-def-tpch-s3 | ours-new `-` | up-native `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | B: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22) |
| new-vs-native-t8-lat-local | ours-new `-DduckDbThreads=8` | up-native `-DduckDbThreads=8` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 0.92 | B: server (SERVER DIED after small), small-adbc32 (960/960 errors; answers differ: count_filter,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders), small-jdbc1 (answers differ: limit10_ob), small-jdbc32 (960/960 errors; answers differ: count_filter,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders), small-jdbc8 (29/480 errors; 30/480 errors; 42/480 errors; answers differ: limit10_ob) |
| new-vs-native-t8-lat-s3 | ours-new `-DduckDbThreads=8` | up-native `-DduckDbThreads=8` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.28 | B: scan8 (rows=142737408 errors=8; rows=64552960 errors=8; rows=76808192 errors=8), server (SERVER DIED after scan SERVER DIED after small), small-adbc32 (960/960 errors; answers differ: count_filter,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders), small-adbc8 (480/480 errors; answers differ: count_filter,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders), small-jdbc1 (answers differ: limit10_ob), small-jdbc32 (960/960 errors; answers differ: count_filter,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders), small-jdbc8 (264/480 errors; 30/480 errors; 39/480 errors; answers differ: count_filter,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders; answers differ: limit10_ob) |
| new-vs-native-t8-tpch-local | ours-new `-DduckDbThreads=8` | up-native `-DduckDbThreads=8` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | B: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22) |
| new-vs-native-t8-tpch-s3 | ours-new `-DduckDbThreads=8` | up-native `-DduckDbThreads=8` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | B: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22) |

## Per job (absolute medians and ratios)

### new-vs-27f5-def-lat-local: A = ours-new `-`, B = ours-27f5 `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 25.6 | 29.2 | 1.14 | 1.09 1.17 1.17 |
| small JDBC c1 p95 | ms | 52.8 | 57.8 | 1.09 | 1.13 1.12 1.06 |
| small JDBC c1 p99 | ms | 64.4 | 68.9 | 1.07 | 1.20 1.06 1.03 |
| small JDBC c8 p50 | ms | 115.2 | 136.8 | 1.19 | 1.26 1.18 1.14 |
| small JDBC c8 p95 | ms | 287.0 | 322.1 | 1.12 | 1.13 1.16 1.09 |
| small JDBC c8 p99 | ms | 354.6 | 462.0 | 1.30 | 1.32 1.31 1.02 |
| small JDBC c32 p50 | ms | 468.3 | 526.3 | 1.12 | 1.06 1.16 1.12 |
| small JDBC c32 p95 | ms | 1311.0 | 1393.6 | 1.06 | 1.08 1.09 1.03 |
| small JDBC c32 p99 | ms | 1878.2 | 1884.9 | 1.00 | 1.02 1.10 0.89 |
| small ADBC c1 p50 | ms | 17.9 | 21.3 | 1.19 | 1.17 1.19 1.31 |
| small ADBC c1 p95 | ms | 48.4 | 52.0 | 1.08 | 1.02 1.07 1.20 |
| small ADBC c1 p99 | ms | 57.2 | 65.7 | 1.15 | 1.08 1.15 1.45 |
| small ADBC c8 p50 | ms | 108.5 | 130.4 | 1.20 | 1.18 1.25 1.15 |
| small ADBC c8 p95 | ms | 274.9 | 294.0 | 1.07 | 1.06 1.07 1.07 |
| small ADBC c8 p99 | ms | 335.0 | 343.5 | 1.03 | 0.99 1.03 1.07 |
| small ADBC c32 p50 | ms | 438.7 | 476.1 | 1.09 | 1.09 1.09 1.06 |
| small ADBC c32 p95 | ms | 1230.5 | 1414.0 | 1.15 | 1.04 1.11 1.19 |
| small ADBC c32 p99 | ms | 1711.1 | 1900.5 | 1.11 | 1.05 1.22 1.05 |
| lineitem scan x1 | MB/s | 405.1 | 445.8 | 1.10 | 1.11 0.99 1.12 |
| lineitem scan x4 | MB/s | 502.1 | 499.4 | 0.99 | 0.99 0.99 1.04 |
| lineitem scan x8 | MB/s | 460.4 | 462.5 | 1.00 | 1.00 1.01 0.99 |
| lineitem export ADBC | MB/s | 532.1 | 513.9 | 0.97 | 0.92 1.06 1.03 |
| server RSS peak | MB | 1710.0 | 1764.0 | 1.03 | 1.04 1.02 1.03 |

### new-vs-27f5-def-lat-s3: A = ours-new `-`, B = ours-27f5 `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 36.4 | 42.1 | 1.16 | 1.13 1.09 1.22 |
| small JDBC c1 p95 | ms | 645.7 | 654.7 | 1.01 | 1.05 0.94 1.01 |
| small JDBC c1 p99 | ms | 693.1 | 711.4 | 1.03 | 1.04 0.93 1.03 |
| small JDBC c8 p50 | ms | 311.0 | 343.6 | 1.10 | 1.10 1.01 1.14 |
| small JDBC c8 p95 | ms | 5318.4 | 5200.5 | 0.98 | 1.04 0.93 0.98 |
| small JDBC c8 p99 | ms | 5631.9 | 5887.8 | 1.05 | 1.44 0.67 1.00 |
| small JDBC c32 p50 | ms | 1071.1 | 1127.2 | 1.05 | 1.05 0.92 0.90 |
| small JDBC c32 p95 | ms | 16863.2 | 16792.3 | 1.00 | 0.91 1.05 1.02 |
| small JDBC c32 p99 | ms | 22746.8 | 27050.1 | 1.19 | 0.75 1.50 0.65 |
| small ADBC c1 p50 | ms | 25.3 | 30.1 | 1.19 | 1.19 1.14 1.14 |
| small ADBC c1 p95 | ms | 661.9 | 684.0 | 1.03 | 1.03 1.04 1.02 |
| small ADBC c1 p99 | ms | 732.0 | 738.5 | 1.01 | 1.01 0.98 1.03 |
| small ADBC c8 p50 | ms | 325.2 | 348.1 | 1.07 | 0.98 1.05 1.36 |
| small ADBC c8 p95 | ms | 5183.6 | 5289.3 | 1.02 | 1.04 0.93 1.49 |
| small ADBC c8 p99 | ms | 5668.8 | 5790.6 | 1.02 | 1.02 0.91 1.47 |
| small ADBC c32 p50 | ms | 1137.0 | 1104.1 | 0.97 | 1.04 0.97 1.01 |
| small ADBC c32 p95 | ms | 16378.0 | 16083.8 | 0.98 | 1.01 0.98 0.97 |
| small ADBC c32 p99 | ms | 26003.5 | 43118.1 | 1.66 | 2.46 0.68 1.35 |
| lineitem scan x1 | MB/s | 393.9 | 409.3 | 1.04 | 1.04 1.04 1.02 |
| lineitem scan x4 | MB/s | 477.0 | 486.2 | 1.02 | 1.07 1.00 1.00 |
| lineitem scan x8 | MB/s | 452.2 | 460.8 | 1.02 | 1.02 1.02 1.02 |
| lineitem export ADBC | MB/s | 438.5 | 418.4 | 0.95 | 1.01 0.99 0.95 |
| server RSS peak | MB | 2769.0 | 2601.0 | 0.94 | 0.99 0.94 0.89 |

### new-vs-27f5-def-tpch-local: A = ours-new `-`, B = ours-27f5 `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 2.5 | 2.6 | 1.02 | 1.02 0.88 1.11 |
| TPC-H SF10 ADBC (sum of medians) | s | 24.4 | 23.7 | 0.97 | 0.99 0.83 0.98 |
| TPC-H SF1 JDBC (sum of medians) | s | 2.6 | 2.6 | 0.98 | 0.98 0.86 1.13 |
| TPC-H SF10 JDBC (sum of medians) | s | 24.6 | 23.9 | 0.97 | 1.01 0.97 0.85 |
| server RSS peak | MB | 1814.0 | 1792.0 | 0.99 | 0.99 0.98 1.00 |

### new-vs-27f5-def-tpch-s3: A = ours-new `-`, B = ours-27f5 `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 34.4 | 33.9 | 0.98 | 1.44 0.98 0.98 |
| TPC-H SF10 ADBC (sum of medians) | s | 396.9 | 396.7 | 1.00 | 1.38 1.00 0.99 |
| TPC-H SF1 JDBC (sum of medians) | s | 33.1 | 33.1 | 1.00 | 1.37 1.00 0.98 |
| TPC-H SF10 JDBC (sum of medians) | s | 392.2 | 393.3 | 1.00 | 1.00 1.03 1.00 |
| server RSS peak | MB | 1755.0 | 1815.0 | 1.03 | 0.99 1.00 1.07 |

### new-vs-27f5-t8-lat-local: A = ours-new `-DduckDbThreads=8`, B = ours-27f5 `-DduckDbThreads=8`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `small scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 25.6 | 28.8 | 1.13 | 1.08 1.21 1.13 |
| small JDBC c1 p95 | ms | 54.7 | 59.4 | 1.09 | 1.06 1.11 1.15 |
| small JDBC c1 p99 | ms | 70.8 | 71.0 | 1.00 | 1.06 0.94 0.99 |
| small JDBC c8 p50 | ms | 135.4 | 153.2 | 1.13 | 1.14 1.18 1.09 |
| small JDBC c8 p95 | ms | 295.4 | 327.0 | 1.11 | 1.08 1.15 1.04 |
| small JDBC c8 p99 | ms | 402.5 | 416.6 | 1.03 | 1.15 1.14 1.00 |
| small JDBC c32 p50 | ms | 522.8 | 610.4 | 1.17 | 1.22 1.11 1.19 |
| small JDBC c32 p95 | ms | 1434.6 | 1442.2 | 1.01 | 1.00 1.03 1.01 |
| small JDBC c32 p99 | ms | 1964.3 | 1978.5 | 1.01 | 1.09 0.97 1.01 |
| small ADBC c1 p50 | ms | 17.7 | 22.0 | 1.24 | 1.28 1.18 1.24 |
| small ADBC c1 p95 | ms | 47.8 | 52.5 | 1.10 | 1.09 1.14 1.13 |
| small ADBC c1 p99 | ms | 55.7 | 62.3 | 1.12 | 1.12 0.88 1.12 |
| small ADBC c8 p50 | ms | 123.0 | 145.1 | 1.18 | 1.15 1.15 1.20 |
| small ADBC c8 p95 | ms | 281.8 | 305.0 | 1.08 | 1.08 1.18 1.08 |
| small ADBC c8 p99 | ms | 361.7 | 373.6 | 1.03 | 0.93 1.13 1.09 |
| small ADBC c32 p50 | ms | 482.1 | 548.1 | 1.14 | 1.12 1.14 1.12 |
| small ADBC c32 p95 | ms | 1347.6 | 1488.7 | 1.10 | 1.01 1.15 1.13 |
| small ADBC c32 p99 | ms | 1877.4 | 1944.3 | 1.04 | 1.03 1.02 1.07 |
| lineitem scan x1 | MB/s | 425.4 | 422.1 | 0.99 | 0.99 1.03 0.95 |
| lineitem scan x4 | MB/s | 436.1 | 428.3 | 0.98 | 1.00 1.00 0.96 |
| lineitem scan x8 | MB/s | 385.4 | 381.2 | 0.99 | 1.00 0.98 1.00 |
| lineitem export ADBC | MB/s | 492.9 | 484.9 | 0.98 | 0.99 0.97 1.01 |
| server RSS peak | MB | 1881.0 | 1922.0 | 1.02 | 1.02 1.02 0.99 |

### new-vs-27f5-t8-lat-s3: A = ours-new `-DduckDbThreads=8`, B = ours-27f5 `-DduckDbThreads=8`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `small scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 30.3 | 37.4 | 1.23 | 1.05 1.33 1.20 |
| small JDBC c1 p95 | ms | 667.6 | 639.3 | 0.96 | 1.02 0.93 1.00 |
| small JDBC c1 p99 | ms | 774.3 | 974.2 | 1.26 | 1.28 1.18 1.25 |
| small JDBC c8 p50 | ms | 354.0 | 377.0 | 1.06 | 1.04 0.96 1.26 |
| small JDBC c8 p95 | ms | 3150.6 | 3148.0 | 1.00 | 1.00 1.01 0.86 |
| small JDBC c8 p99 | ms | 3844.4 | 4992.7 | 1.30 | 0.97 0.70 1.65 |
| small JDBC c32 p50 | ms | 1423.2 | 1432.3 | 1.01 | 1.06 1.00 1.03 |
| small JDBC c32 p95 | ms | 10924.7 | 9896.5 | 0.91 | 0.91 0.91 0.93 |
| small JDBC c32 p99 | ms | 18478.1 | 18511.2 | 1.00 | 1.38 1.00 0.68 |
| small ADBC c1 p50 | ms | 24.4 | 28.7 | 1.18 | 1.28 1.07 1.23 |
| small ADBC c1 p95 | ms | 660.9 | 650.2 | 0.98 | 1.02 0.98 0.89 |
| small ADBC c1 p99 | ms | 783.1 | 716.2 | 0.91 | 0.95 0.99 0.91 |
| small ADBC c8 p50 | ms | 377.9 | 410.3 | 1.09 | 0.97 1.28 1.02 |
| small ADBC c8 p95 | ms | 3151.5 | 2799.2 | 0.89 | 1.03 0.84 0.95 |
| small ADBC c8 p99 | ms | 3542.9 | 3139.2 | 0.89 | 1.59 0.87 0.88 |
| small ADBC c32 p50 | ms | 1438.6 | 1552.3 | 1.08 | 0.99 1.20 1.05 |
| small ADBC c32 p95 | ms | 10460.9 | 9966.0 | 0.95 | 1.00 0.89 0.97 |
| small ADBC c32 p99 | ms | 12289.0 | 23008.0 | 1.87 | 1.29 1.88 1.93 |
| lineitem scan x1 | MB/s | 423.6 | 410.8 | 0.97 | 0.71 0.97 1.14 |
| lineitem scan x4 | MB/s | 481.5 | 494.9 | 1.03 | 1.02 0.95 1.08 |
| lineitem scan x8 | MB/s | 445.8 | 452.3 | 1.01 | 1.01 1.02 1.02 |
| lineitem export ADBC | MB/s | 390.2 | 483.8 | 1.24 | 0.81 1.18 1.42 |
| server RSS peak | MB | 3256.0 | 3152.0 | 0.97 | 0.97 0.99 0.92 |

### new-vs-27f5-t8-tpch-local: A = ours-new `-DduckDbThreads=8`, B = ours-27f5 `-DduckDbThreads=8`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 4.2 | 4.5 | 1.07 | 1.05 1.08 1.05 |
| TPC-H SF10 ADBC (sum of medians) | s | 39.8 | 39.7 | 1.00 | 1.01 1.00 0.99 |
| TPC-H SF1 JDBC (sum of medians) | s | 4.3 | 4.5 | 1.04 | 1.04 1.03 1.03 |
| TPC-H SF10 JDBC (sum of medians) | s | 39.9 | 40.0 | 1.00 | 1.00 1.01 1.01 |
| server RSS peak | MB | 1883.0 | 1860.0 | 0.99 | 0.99 1.01 0.97 |

### new-vs-27f5-t8-tpch-s3: A = ours-new `-DduckDbThreads=8`, B = ours-27f5 `-DduckDbThreads=8`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 33.1 | 33.9 | 1.02 | 1.52 0.96 0.98 |
| TPC-H SF10 ADBC (sum of medians) | s | 387.0 | 387.9 | 1.00 | 1.08 1.04 0.97 |
| TPC-H SF1 JDBC (sum of medians) | s | 32.6 | 35.4 | 1.09 | 1.23 1.12 1.02 |
| TPC-H SF10 JDBC (sum of medians) | s | 391.3 | 291.4 | 0.74 | 0.92 0.70 0.98 |
| server RSS peak | MB | 1840.0 | 1940.0 | 1.05 | 1.03 1.07 1.01 |

### new-vs-main-def-lat-local: A = ours-new `-`, B = up-main `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small scan adbcscan`, small-query classes `meta_tables,meta_schemas,point_orders,point_lineitem,count_filter,limit10_ob`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 32.2 | n/a | n/a | - |
| small JDBC c1 p95 | ms | 55.9 | n/a | n/a | - |
| small JDBC c1 p99 | ms | 58.2 | n/a | n/a | - |
| small JDBC c8 p50 | ms | 171.4 | n/a | n/a | - |
| small JDBC c8 p95 | ms | 323.5 | n/a | n/a | - |
| small JDBC c8 p99 | ms | 412.3 | n/a | n/a | - |
| small JDBC c32 p50 | ms | 646.8 | n/a | n/a | - |
| small JDBC c32 p95 | ms | 1491.8 | n/a | n/a | - |
| small JDBC c32 p99 | ms | 2006.3 | n/a | n/a | - |
| small ADBC c1 p50 | ms | 23.4 | n/a | n/a | - |
| small ADBC c1 p95 | ms | 52.9 | n/a | n/a | - |
| small ADBC c1 p99 | ms | 69.5 | n/a | n/a | - |
| small ADBC c8 p50 | ms | 152.2 | n/a | n/a | - |
| small ADBC c8 p95 | ms | 322.2 | n/a | n/a | - |
| small ADBC c8 p99 | ms | 442.9 | n/a | n/a | - |
| small ADBC c32 p50 | ms | 590.5 | n/a | n/a | - |
| small ADBC c32 p95 | ms | 1408.4 | n/a | n/a | - |
| small ADBC c32 p99 | ms | 1698.9 | n/a | n/a | - |
| lineitem scan x1 | MB/s | 417.7 | n/a | n/a | - |
| lineitem scan x4 | MB/s | 488.7 | n/a | n/a | - |
| lineitem scan x8 | MB/s | 463.0 | n/a | n/a | - |
| lineitem export ADBC | MB/s | 516.2 | n/a | n/a | - |
| server RSS peak | MB | 1708.0 | 283.0 | 0.17 | 0.16 0.17 0.16 |

Correctness gate: B: adbcscan (rows=0 errors=1), scan1 (rows=0 errors=1), scan4 (rows=0 errors=4), scan8 (rows=0 errors=8), server (SERVER DIED after adbcscan SERVER DIED after scan SERVER DIED after small), small-adbc32 (960/960 errors; answers differ: count_filter,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders), small-adbc8 (480/480 errors; answers differ: count_filter,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders), small-jdbc1 (80/120 errors; answers differ: count_filter,limit10_ob,point_lineitem,point_orders), small-jdbc32 (960/960 errors; answers differ: count_filter,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders), small-jdbc8 (320/480 errors; answers differ: count_filter,limit10_ob,point_lineitem,point_orders).

### new-vs-main-def-tpch-local: A = ours-new `-`, B = up-main `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `adbc10 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 4.2 | n/a | n/a | - |
| TPC-H SF10 ADBC (sum of medians) | s | 40.4 | n/a | n/a | - |
| server RSS peak | MB | 1543.0 | 370.0 | 0.24 | 0.24 0.24 0.24 |

Correctness gate: B: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22).

### new-vs-main-t8-lat-local: A = ours-new `-DduckDbThreads=8`, B = up-main `-DduckDbThreads=8`, local

Runner: Linux ubuntu24 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C. Workloads: `small scan adbcscan`, small-query classes `meta_tables,meta_schemas,point_orders,point_lineitem,count_filter,limit10_ob`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 30.6 | n/a | n/a | - |
| small JDBC c1 p95 | ms | 56.4 | n/a | n/a | - |
| small JDBC c1 p99 | ms | 61.7 | n/a | n/a | - |
| small JDBC c8 p50 | ms | 165.2 | n/a | n/a | - |
| small JDBC c8 p95 | ms | 310.7 | n/a | n/a | - |
| small JDBC c8 p99 | ms | 399.6 | n/a | n/a | - |
| small JDBC c32 p50 | ms | 629.9 | n/a | n/a | - |
| small JDBC c32 p95 | ms | 1382.0 | n/a | n/a | - |
| small JDBC c32 p99 | ms | 1705.1 | n/a | n/a | - |
| small ADBC c1 p50 | ms | 21.7 | n/a | n/a | - |
| small ADBC c1 p95 | ms | 49.7 | n/a | n/a | - |
| small ADBC c1 p99 | ms | 58.8 | n/a | n/a | - |
| small ADBC c8 p50 | ms | 140.5 | n/a | n/a | - |
| small ADBC c8 p95 | ms | 322.9 | n/a | n/a | - |
| small ADBC c8 p99 | ms | 427.6 | n/a | n/a | - |
| small ADBC c32 p50 | ms | 586.2 | n/a | n/a | - |
| small ADBC c32 p95 | ms | 1295.5 | n/a | n/a | - |
| small ADBC c32 p99 | ms | 1609.3 | n/a | n/a | - |
| lineitem scan x1 | MB/s | 420.6 | n/a | n/a | - |
| lineitem scan x4 | MB/s | 454.8 | n/a | n/a | - |
| lineitem scan x8 | MB/s | 407.0 | n/a | n/a | - |
| lineitem export ADBC | MB/s | 501.2 | n/a | n/a | - |
| server RSS peak | MB | 1848.0 | 283.0 | 0.15 | 0.15 0.15 0.16 |

Correctness gate: B: adbcscan (rows=0 errors=1), scan1 (rows=0 errors=1), scan4 (rows=0 errors=4), scan8 (rows=0 errors=8), server (SERVER DIED after adbcscan SERVER DIED after scan SERVER DIED after small), small-adbc32 (960/960 errors; answers differ: count_filter,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders), small-adbc8 (480/480 errors; answers differ: count_filter,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders), small-jdbc1 (80/120 errors; answers differ: count_filter,limit10_ob,point_lineitem,point_orders), small-jdbc32 (960/960 errors; answers differ: count_filter,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders), small-jdbc8 (320/480 errors; answers differ: count_filter,limit10_ob,point_lineitem,point_orders).

### new-vs-main-t8-tpch-local: A = ours-new `-DduckDbThreads=8`, B = up-main `-DduckDbThreads=8`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `adbc10 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 3.1 | n/a | n/a | - |
| TPC-H SF10 ADBC (sum of medians) | s | 28.3 | n/a | n/a | - |
| server RSS peak | MB | 1732.0 | 419.0 | 0.24 | 0.23 0.24 0.25 |

Correctness gate: B: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22).

### new-vs-native-def-lat-local: A = ours-new `-`, B = up-native `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `small scan adbcscan`, small-query classes `meta_tables,meta_schemas,point_orders,point_lineitem,count_filter,limit10_ob`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 25.9 | n/a | n/a | - |
| small JDBC c1 p95 | ms | 40.0 | n/a | n/a | - |
| small JDBC c1 p99 | ms | 42.5 | n/a | n/a | - |
| small JDBC c8 p50 | ms | 125.2 | n/a | n/a | - |
| small JDBC c8 p95 | ms | 248.8 | n/a | n/a | - |
| small JDBC c8 p99 | ms | 313.2 | n/a | n/a | - |
| small JDBC c32 p50 | ms | 399.2 | n/a | n/a | - |
| small JDBC c32 p95 | ms | 1041.6 | n/a | n/a | - |
| small JDBC c32 p99 | ms | 1380.5 | n/a | n/a | - |
| small ADBC c1 p50 | ms | 15.4 | n/a | n/a | - |
| small ADBC c1 p95 | ms | 33.9 | n/a | n/a | - |
| small ADBC c1 p99 | ms | 49.2 | n/a | n/a | - |
| small ADBC c8 p50 | ms | 96.2 | n/a | n/a | - |
| small ADBC c8 p95 | ms | 229.9 | n/a | n/a | - |
| small ADBC c8 p99 | ms | 281.1 | n/a | n/a | - |
| small ADBC c32 p50 | ms | 394.4 | n/a | n/a | - |
| small ADBC c32 p95 | ms | 1035.5 | n/a | n/a | - |
| small ADBC c32 p99 | ms | 1309.2 | n/a | n/a | - |
| lineitem scan x1 | MB/s | 589.0 | 603.0 | 1.02 | 0.88 1.16 1.02 |
| lineitem scan x4 | MB/s | 705.7 | 806.9 | 1.14 | 1.07 1.22 1.14 |
| lineitem scan x8 | MB/s | 659.4 | 823.4 | 1.25 | 1.25 1.26 1.27 |
| lineitem export ADBC | MB/s | 732.0 | 760.7 | 1.04 | 1.04 1.04 1.05 |
| server RSS peak | MB | 1707.0 | 3699.0 | 2.17 | 1.80 2.18 2.21 |

Correctness gate: B: server (SERVER DIED after small), small-adbc32 (960/960 errors; answers differ: count_filter,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders), small-jdbc1 (answers differ: limit10_ob), small-jdbc32 (960/960 errors; answers differ: count_filter,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders), small-jdbc8 (34/480 errors; 38/480 errors; 42/480 errors; answers differ: limit10_ob).

### new-vs-native-def-lat-s3: A = ours-new `-`, B = up-native `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small scan adbcscan`, small-query classes `meta_tables,meta_schemas,point_orders,point_lineitem,count_filter,limit10_ob`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 31.6 | n/a | n/a | - |
| small JDBC c1 p95 | ms | 663.1 | n/a | n/a | - |
| small JDBC c1 p99 | ms | 705.6 | n/a | n/a | - |
| small JDBC c8 p50 | ms | 321.0 | n/a | n/a | - |
| small JDBC c8 p95 | ms | 5799.1 | n/a | n/a | - |
| small JDBC c8 p99 | ms | 6147.3 | n/a | n/a | - |
| small JDBC c32 p50 | ms | 1034.2 | n/a | n/a | - |
| small JDBC c32 p95 | ms | 18716.4 | n/a | n/a | - |
| small JDBC c32 p99 | ms | 37017.4 | n/a | n/a | - |
| small ADBC c1 p50 | ms | 22.4 | n/a | n/a | - |
| small ADBC c1 p95 | ms | 662.8 | n/a | n/a | - |
| small ADBC c1 p99 | ms | 698.0 | n/a | n/a | - |
| small ADBC c8 p50 | ms | 321.0 | n/a | n/a | - |
| small ADBC c8 p95 | ms | 5861.5 | n/a | n/a | - |
| small ADBC c8 p99 | ms | 6181.1 | n/a | n/a | - |
| small ADBC c32 p50 | ms | 1003.5 | n/a | n/a | - |
| small ADBC c32 p95 | ms | 18308.4 | n/a | n/a | - |
| small ADBC c32 p99 | ms | 28425.7 | n/a | n/a | - |
| lineitem scan x1 | MB/s | 397.4 | 375.1 | 0.94 | 0.93 0.93 0.96 |
| lineitem scan x4 | MB/s | 480.8 | 588.2 | 1.22 | 1.26 1.22 1.21 |
| lineitem scan x8 | MB/s | 462.7 | n/a | n/a | - |
| lineitem export ADBC | MB/s | 422.9 | 552.2 | 1.31 | 1.21 0.97 1.36 |
| server RSS peak | MB | 2622.0 | 5745.0 | 2.19 | 2.09 1.20 2.51 |

Correctness gate: B: scan8 (rows=128712704 errors=8), server (SERVER DIED after scan SERVER DIED after small; SERVER DIED after small), small-adbc32 (960/960 errors; answers differ: count_filter,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders), small-adbc8 (480/480 errors; answers differ: count_filter,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders), small-jdbc1 (answers differ: limit10_ob), small-jdbc32 (960/960 errors; answers differ: count_filter,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders), small-jdbc8 (251/480 errors; 257/480 errors; answers differ: count_filter,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders).

### new-vs-native-def-tpch-local: A = ours-new `-`, B = up-native `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `adbc10 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 3.2 | n/a | n/a | - |
| TPC-H SF10 ADBC (sum of medians) | s | 31.4 | n/a | n/a | - |
| server RSS peak | MB | 1720.0 | 392.0 | 0.23 | 0.23 0.24 0.23 |

Correctness gate: B: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22).

### new-vs-native-def-tpch-s3: A = ours-new `-`, B = up-native `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `adbc10 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 24.3 | n/a | n/a | - |
| TPC-H SF10 ADBC (sum of medians) | s | 261.6 | n/a | n/a | - |
| server RSS peak | MB | 1718.0 | 1016.0 | 0.59 | 0.60 0.54 0.59 |

Correctness gate: B: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22).

### new-vs-native-t8-lat-local: A = ours-new `-DduckDbThreads=8`, B = up-native `-DduckDbThreads=8`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small scan adbcscan`, small-query classes `meta_tables,meta_schemas,point_orders,point_lineitem,count_filter,limit10_ob`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 31.1 | n/a | n/a | - |
| small JDBC c1 p95 | ms | 55.2 | n/a | n/a | - |
| small JDBC c1 p99 | ms | 59.4 | n/a | n/a | - |
| small JDBC c8 p50 | ms | 165.8 | n/a | n/a | - |
| small JDBC c8 p95 | ms | 340.5 | n/a | n/a | - |
| small JDBC c8 p99 | ms | 456.9 | n/a | n/a | - |
| small JDBC c32 p50 | ms | 665.8 | n/a | n/a | - |
| small JDBC c32 p95 | ms | 1567.3 | n/a | n/a | - |
| small JDBC c32 p99 | ms | 2072.3 | n/a | n/a | - |
| small ADBC c1 p50 | ms | 22.7 | n/a | n/a | - |
| small ADBC c1 p95 | ms | 55.1 | n/a | n/a | - |
| small ADBC c1 p99 | ms | 62.0 | n/a | n/a | - |
| small ADBC c8 p50 | ms | 151.5 | n/a | n/a | - |
| small ADBC c8 p95 | ms | 333.7 | n/a | n/a | - |
| small ADBC c8 p99 | ms | 466.9 | n/a | n/a | - |
| small ADBC c32 p50 | ms | 618.7 | n/a | n/a | - |
| small ADBC c32 p95 | ms | 1455.0 | n/a | n/a | - |
| small ADBC c32 p99 | ms | 1769.1 | n/a | n/a | - |
| lineitem scan x1 | MB/s | 433.2 | 398.8 | 0.92 | 0.89 0.92 0.97 |
| lineitem scan x4 | MB/s | 467.6 | 557.7 | 1.19 | 1.16 1.19 1.21 |
| lineitem scan x8 | MB/s | 405.2 | 593.2 | 1.46 | 1.46 1.48 1.46 |
| lineitem export ADBC | MB/s | 524.8 | 518.2 | 0.99 | 0.96 1.11 0.99 |
| server RSS peak | MB | 1864.0 | 3920.0 | 2.10 | 2.25 2.09 2.07 |

Correctness gate: B: server (SERVER DIED after small), small-adbc32 (960/960 errors; answers differ: count_filter,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders), small-jdbc1 (answers differ: limit10_ob), small-jdbc32 (960/960 errors; answers differ: count_filter,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders), small-jdbc8 (29/480 errors; 30/480 errors; 42/480 errors; answers differ: limit10_ob).

### new-vs-native-t8-lat-s3: A = ours-new `-DduckDbThreads=8`, B = up-native `-DduckDbThreads=8`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `small scan adbcscan`, small-query classes `meta_tables,meta_schemas,point_orders,point_lineitem,count_filter,limit10_ob`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 40.3 | n/a | n/a | - |
| small JDBC c1 p95 | ms | 724.3 | n/a | n/a | - |
| small JDBC c1 p99 | ms | 1504.8 | n/a | n/a | - |
| small JDBC c8 p50 | ms | 380.5 | n/a | n/a | - |
| small JDBC c8 p95 | ms | 3671.7 | n/a | n/a | - |
| small JDBC c8 p99 | ms | 4075.0 | n/a | n/a | - |
| small JDBC c32 p50 | ms | 1219.9 | n/a | n/a | - |
| small JDBC c32 p95 | ms | 12208.6 | n/a | n/a | - |
| small JDBC c32 p99 | ms | 13719.3 | n/a | n/a | - |
| small ADBC c1 p50 | ms | 27.8 | n/a | n/a | - |
| small ADBC c1 p95 | ms | 891.1 | n/a | n/a | - |
| small ADBC c1 p99 | ms | 1356.9 | n/a | n/a | - |
| small ADBC c8 p50 | ms | 394.9 | n/a | n/a | - |
| small ADBC c8 p95 | ms | 3388.7 | n/a | n/a | - |
| small ADBC c8 p99 | ms | 3832.1 | n/a | n/a | - |
| small ADBC c32 p50 | ms | 1306.5 | n/a | n/a | - |
| small ADBC c32 p95 | ms | 11974.5 | n/a | n/a | - |
| small ADBC c32 p99 | ms | 13304.8 | n/a | n/a | - |
| lineitem scan x1 | MB/s | 270.2 | 346.2 | 1.28 | 2.09 1.11 0.99 |
| lineitem scan x4 | MB/s | 419.7 | 650.3 | 1.55 | 1.55 1.85 1.49 |
| lineitem scan x8 | MB/s | 386.0 | n/a | n/a | - |
| lineitem export ADBC | MB/s | 317.7 | 378.1 | 1.19 | 1.19 1.01 2.00 |
| server RSS peak | MB | 2966.0 | 3292.0 | 1.11 | 1.11 1.02 1.12 |

Correctness gate: B: scan8 (rows=142737408 errors=8; rows=64552960 errors=8; rows=76808192 errors=8), server (SERVER DIED after scan SERVER DIED after small), small-adbc32 (960/960 errors; answers differ: count_filter,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders), small-adbc8 (480/480 errors; answers differ: count_filter,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders), small-jdbc1 (answers differ: limit10_ob), small-jdbc32 (960/960 errors; answers differ: count_filter,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders), small-jdbc8 (264/480 errors; 30/480 errors; 39/480 errors; answers differ: count_filter,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders; answers differ: limit10_ob).

### new-vs-native-t8-tpch-local: A = ours-new `-DduckDbThreads=8`, B = up-native `-DduckDbThreads=8`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `adbc10 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 4.3 | n/a | n/a | - |
| TPC-H SF10 ADBC (sum of medians) | s | 40.3 | n/a | n/a | - |
| server RSS peak | MB | 1763.0 | 416.0 | 0.24 | 0.23 0.23 0.25 |

Correctness gate: B: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22).

### new-vs-native-t8-tpch-s3: A = ours-new `-DduckDbThreads=8`, B = up-native `-DduckDbThreads=8`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `adbc10 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 26.9 | n/a | n/a | - |
| TPC-H SF10 ADBC (sum of medians) | s | 349.2 | n/a | n/a | - |
| server RSS peak | MB | 1852.0 | 1047.0 | 0.57 | 0.57 0.55 0.55 |

Correctness gate: B: adbc1 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22), adbc10 (failed q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22).
