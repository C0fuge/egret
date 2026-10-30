# Wave track-f06b5834e76e (server comparison), run 41132125972

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

## Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| i23b-load-local | f06b5834e76e `-` | f06b5834e76e `-DresourceProfile=speed` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| i23b-load-local-vs-up-native | up-native `-` | f06b5834e76e `-DresourceProfile=speed` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| i23b-small-local | f06b5834e76e `-` | f06b5834e76e `-DresourceProfile=speed` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | 0.97 | 0.93 | 0.97 | 0.88 | n/a | n/a | n/a | n/a | none |
| i23b-small-local-vs-up-native | up-native `-` | f06b5834e76e `-DresourceProfile=speed` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point) |
| i23b-small-s3 | f06b5834e76e `-` | f06b5834e76e `-DresourceProfile=speed` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | 0.91 | 1.50 | 0.98 | 1.59 | n/a | n/a | n/a | n/a | none |
| i23b-small-s3-vs-up-native | up-native `-` | f06b5834e76e `-DresourceProfile=speed` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-adbc8 (640/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc8 (541/640 errors; 593/640 errors; 594/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point) |

## Per job (absolute medians and ratios)

### i23b-load-local: A = f06b5834e76e `-`, B = f06b5834e76e `-DresourceProfile=speed`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 4577.0 | 823.0 | 0.18 | 0.17 0.18 0.21 |

### i23b-load-local-vs-up-native: A = up-native `-`, B = f06b5834e76e `-DresourceProfile=speed`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 4322.0 | 823.0 | 0.19 | 0.18 0.19 0.20 |

### i23b-small-local: A = f06b5834e76e `-`, B = f06b5834e76e `-DresourceProfile=speed`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 23.3 | 22.5 | 0.97 | 0.92 0.96 1.02 |
| small JDBC c1 p95 | ms | 48.9 | 48.8 | 1.00 | 1.00 1.01 0.98 |
| small JDBC c1 p99 | ms | 58.5 | 57.2 | 0.98 | 0.87 1.09 0.98 |
| small JDBC c8 p50 | ms | 119.4 | 82.9 | 0.69 | 0.68 0.71 0.69 |
| small JDBC c8 p95 | ms | 286.1 | 284.5 | 0.99 | 0.95 1.02 1.00 |
| small JDBC c8 p99 | ms | 356.4 | 353.2 | 0.99 | 0.87 0.98 1.05 |
| small JDBC c32 p50 | ms | 450.1 | 259.1 | 0.58 | 0.59 0.58 0.55 |
| small JDBC c32 p95 | ms | 1292.7 | 1135.7 | 0.88 | 0.86 0.88 0.88 |
| small JDBC c32 p99 | ms | 1674.8 | 1296.9 | 0.77 | 0.77 0.81 0.75 |
| small ADBC c1 p50 | ms | 15.7 | 15.1 | 0.97 | 0.96 1.08 0.96 |
| small ADBC c1 p95 | ms | 45.4 | 45.4 | 1.00 | 0.98 1.02 1.01 |
| small ADBC c1 p99 | ms | 52.1 | 55.7 | 1.07 | 1.15 1.07 1.09 |
| small ADBC c8 p50 | ms | 105.4 | 74.3 | 0.70 | 0.71 0.69 0.70 |
| small ADBC c8 p95 | ms | 281.9 | 291.0 | 1.03 | 1.06 1.03 1.03 |
| small ADBC c8 p99 | ms | 356.6 | 398.7 | 1.12 | 1.13 1.02 1.12 |
| small ADBC c32 p50 | ms | 426.8 | 244.3 | 0.57 | 0.57 0.56 0.57 |
| small ADBC c32 p95 | ms | 1239.5 | 1147.9 | 0.93 | 0.90 0.94 0.93 |
| small ADBC c32 p99 | ms | 1686.5 | 1308.0 | 0.78 | 0.77 0.82 0.75 |
| server RSS peak | MB | 1458.0 | 705.0 | 0.48 | 0.48 0.48 0.49 |

### i23b-small-local-vs-up-native: A = up-native `-`, B = f06b5834e76e `-DresourceProfile=speed`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | n/a | 22.5 | n/a | - |
| small JDBC c1 p95 | ms | n/a | 48.8 | n/a | - |
| small JDBC c1 p99 | ms | n/a | 57.2 | n/a | - |
| small JDBC c8 p50 | ms | n/a | 82.9 | n/a | - |
| small JDBC c8 p95 | ms | n/a | 284.5 | n/a | - |
| small JDBC c8 p99 | ms | n/a | 353.2 | n/a | - |
| small JDBC c32 p50 | ms | n/a | 259.1 | n/a | - |
| small JDBC c32 p95 | ms | n/a | 1135.7 | n/a | - |
| small JDBC c32 p99 | ms | n/a | 1296.9 | n/a | - |
| small ADBC c1 p50 | ms | n/a | 15.1 | n/a | - |
| small ADBC c1 p95 | ms | n/a | 45.4 | n/a | - |
| small ADBC c1 p99 | ms | n/a | 55.7 | n/a | - |
| small ADBC c8 p50 | ms | n/a | 74.3 | n/a | - |
| small ADBC c8 p95 | ms | n/a | 291.0 | n/a | - |
| small ADBC c8 p99 | ms | n/a | 398.7 | n/a | - |
| small ADBC c32 p50 | ms | n/a | 244.3 | n/a | - |
| small ADBC c32 p95 | ms | n/a | 1147.9 | n/a | - |
| small ADBC c32 p99 | ms | n/a | 1308.0 | n/a | - |
| server RSS peak | MB | 246.0 | 705.0 | 2.87 | 2.77 2.87 2.89 |

Correctness gate: A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point).

### i23b-small-s3: A = f06b5834e76e `-`, B = f06b5834e76e `-DresourceProfile=speed`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 34.4 | 33.7 | 0.98 | 0.91 1.18 0.95 |
| small JDBC c1 p95 | ms | 771.1 | 776.4 | 1.01 | 1.00 1.02 1.05 |
| small JDBC c1 p99 | ms | 827.0 | 833.7 | 1.01 | 1.01 0.99 1.01 |
| small JDBC c8 p50 | ms | 339.1 | 198.6 | 0.59 | 0.59 0.60 0.62 |
| small JDBC c8 p95 | ms | 5521.2 | 5296.6 | 0.96 | 0.96 1.10 0.93 |
| small JDBC c8 p99 | ms | 8981.7 | 9038.6 | 1.01 | 1.55 0.87 0.91 |
| small JDBC c32 p50 | ms | 1118.7 | 591.7 | 0.53 | 0.54 0.53 0.72 |
| small JDBC c32 p95 | ms | 17005.1 | 26976.4 | 1.59 | 1.45 1.59 2.08 |
| small JDBC c32 p99 | ms | 20012.6 | 29596.6 | 1.48 | 1.16 1.49 1.92 |
| small ADBC c1 p50 | ms | 24.9 | 22.7 | 0.91 | 1.30 0.89 0.86 |
| small ADBC c1 p95 | ms | 783.3 | 755.3 | 0.96 | 0.96 0.96 1.08 |
| small ADBC c1 p99 | ms | 824.6 | 849.4 | 1.03 | 1.34 0.96 1.14 |
| small ADBC c8 p50 | ms | 335.6 | 199.0 | 0.59 | 0.61 0.57 0.67 |
| small ADBC c8 p95 | ms | 5513.5 | 6052.8 | 1.10 | 1.10 0.98 1.08 |
| small ADBC c8 p99 | ms | 6023.7 | 9503.0 | 1.58 | 1.58 1.55 1.54 |
| small ADBC c32 p50 | ms | 1100.9 | 553.8 | 0.50 | 0.50 0.49 0.76 |
| small ADBC c32 p95 | ms | 17608.6 | 26346.3 | 1.50 | 1.59 1.49 1.90 |
| small ADBC c32 p99 | ms | 20086.7 | 27993.3 | 1.39 | 1.39 1.39 0.89 |
| server RSS peak | MB | 2221.0 | 832.0 | 0.37 | 0.37 0.37 0.39 |

### i23b-small-s3-vs-up-native: A = up-native `-`, B = f06b5834e76e `-DresourceProfile=speed`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | n/a | 33.7 | n/a | - |
| small JDBC c1 p95 | ms | n/a | 776.4 | n/a | - |
| small JDBC c1 p99 | ms | n/a | 833.7 | n/a | - |
| small JDBC c8 p50 | ms | n/a | 198.6 | n/a | - |
| small JDBC c8 p95 | ms | n/a | 5296.6 | n/a | - |
| small JDBC c8 p99 | ms | n/a | 9038.6 | n/a | - |
| small JDBC c32 p50 | ms | n/a | 591.7 | n/a | - |
| small JDBC c32 p95 | ms | n/a | 26976.4 | n/a | - |
| small JDBC c32 p99 | ms | n/a | 29596.6 | n/a | - |
| small ADBC c1 p50 | ms | n/a | 22.7 | n/a | - |
| small ADBC c1 p95 | ms | n/a | 755.3 | n/a | - |
| small ADBC c1 p99 | ms | n/a | 849.4 | n/a | - |
| small ADBC c8 p50 | ms | n/a | 199.0 | n/a | - |
| small ADBC c8 p95 | ms | n/a | 6052.8 | n/a | - |
| small ADBC c8 p99 | ms | n/a | 9503.0 | n/a | - |
| small ADBC c32 p50 | ms | n/a | 553.8 | n/a | - |
| small ADBC c32 p95 | ms | n/a | 26346.3 | n/a | - |
| small ADBC c32 p99 | ms | n/a | 27993.3 | n/a | - |
| server RSS peak | MB | 389.0 | 832.0 | 2.14 | 2.08 2.19 2.21 |

Correctness gate: A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-adbc8 (640/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc8 (541/640 errors; 593/640 errors; 594/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point).
