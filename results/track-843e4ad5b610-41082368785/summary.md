# Wave track-843e4ad5b610 (server comparison), run 41082368785

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

## Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| i23b-load-local | 843e4ad5b610 `-` | 843e4ad5b610 `-DresourceProfile=speed` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| i23b-load-local-vs-up-native | up-native `-` | 843e4ad5b610 `-DresourceProfile=speed` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| i23b-small-local | 843e4ad5b610 `-` | 843e4ad5b610 `-DresourceProfile=speed` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | 0.98 | 0.93 | 0.97 | 0.86 | n/a | n/a | n/a | n/a | none |
| i23b-small-local-vs-up-native | up-native `-` | 843e4ad5b610 `-DresourceProfile=speed` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point) |
| i23b-small-s3 | 843e4ad5b610 `-` | 843e4ad5b610 `-DresourceProfile=speed` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | 0.91 | 1.46 | 1.04 | 1.54 | n/a | n/a | n/a | n/a | none |
| i23b-small-s3-vs-up-native | up-native `-` | 843e4ad5b610 `-DresourceProfile=speed` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-adbc8 (640/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc8 (461/640 errors; 539/640 errors; 613/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point) |

## Per job (absolute medians and ratios)

### i23b-load-local: A = 843e4ad5b610 `-`, B = 843e4ad5b610 `-DresourceProfile=speed`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 4432.0 | 823.0 | 0.19 | 0.20 0.18 0.19 |

### i23b-load-local-vs-up-native: A = up-native `-`, B = 843e4ad5b610 `-DresourceProfile=speed`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 4928.0 | 823.0 | 0.17 | 0.18 0.18 0.17 |

### i23b-small-local: A = 843e4ad5b610 `-`, B = 843e4ad5b610 `-DresourceProfile=speed`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 23.4 | 22.7 | 0.97 | 1.07 0.94 1.06 |
| small JDBC c1 p95 | ms | 50.7 | 47.7 | 0.94 | 1.06 0.87 0.95 |
| small JDBC c1 p99 | ms | 60.6 | 58.6 | 0.97 | 1.00 0.95 1.01 |
| small JDBC c8 p50 | ms | 120.4 | 74.9 | 0.62 | 0.66 0.61 0.65 |
| small JDBC c8 p95 | ms | 298.6 | 303.8 | 1.02 | 1.08 1.02 1.06 |
| small JDBC c8 p99 | ms | 359.8 | 354.2 | 0.98 | 0.91 0.98 1.00 |
| small JDBC c32 p50 | ms | 465.3 | 254.1 | 0.55 | 0.66 0.54 0.53 |
| small JDBC c32 p95 | ms | 1344.3 | 1158.9 | 0.86 | 0.88 0.84 0.88 |
| small JDBC c32 p99 | ms | 1781.5 | 1294.2 | 0.73 | 0.72 0.71 0.75 |
| small ADBC c1 p50 | ms | 16.1 | 15.7 | 0.98 | 0.96 0.97 0.98 |
| small ADBC c1 p95 | ms | 44.0 | 43.2 | 0.98 | 0.98 1.02 1.03 |
| small ADBC c1 p99 | ms | 57.1 | 59.8 | 1.05 | 1.10 0.99 1.05 |
| small ADBC c8 p50 | ms | 105.3 | 65.9 | 0.63 | 0.67 0.63 0.62 |
| small ADBC c8 p95 | ms | 275.4 | 311.8 | 1.13 | 1.10 1.09 1.16 |
| small ADBC c8 p99 | ms | 348.7 | 349.3 | 1.00 | 1.00 1.00 1.10 |
| small ADBC c32 p50 | ms | 439.8 | 244.8 | 0.56 | 0.59 0.53 0.57 |
| small ADBC c32 p95 | ms | 1238.7 | 1149.8 | 0.93 | 0.91 0.91 0.96 |
| small ADBC c32 p99 | ms | 1793.4 | 1262.2 | 0.70 | 0.75 0.73 0.66 |
| server RSS peak | MB | 1468.0 | 691.0 | 0.47 | 0.49 0.47 0.48 |

### i23b-small-local-vs-up-native: A = up-native `-`, B = 843e4ad5b610 `-DresourceProfile=speed`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | n/a | 22.7 | n/a | - |
| small JDBC c1 p95 | ms | n/a | 47.7 | n/a | - |
| small JDBC c1 p99 | ms | n/a | 58.6 | n/a | - |
| small JDBC c8 p50 | ms | n/a | 74.9 | n/a | - |
| small JDBC c8 p95 | ms | n/a | 303.8 | n/a | - |
| small JDBC c8 p99 | ms | n/a | 354.2 | n/a | - |
| small JDBC c32 p50 | ms | n/a | 254.1 | n/a | - |
| small JDBC c32 p95 | ms | n/a | 1158.9 | n/a | - |
| small JDBC c32 p99 | ms | n/a | 1294.2 | n/a | - |
| small ADBC c1 p50 | ms | n/a | 15.7 | n/a | - |
| small ADBC c1 p95 | ms | n/a | 43.2 | n/a | - |
| small ADBC c1 p99 | ms | n/a | 59.8 | n/a | - |
| small ADBC c8 p50 | ms | n/a | 65.9 | n/a | - |
| small ADBC c8 p95 | ms | n/a | 311.8 | n/a | - |
| small ADBC c8 p99 | ms | n/a | 349.3 | n/a | - |
| small ADBC c32 p50 | ms | n/a | 244.8 | n/a | - |
| small ADBC c32 p95 | ms | n/a | 1149.8 | n/a | - |
| small ADBC c32 p99 | ms | n/a | 1262.2 | n/a | - |
| server RSS peak | MB | 248.0 | 691.0 | 2.79 | 2.94 2.82 2.79 |

Correctness gate: A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point).

### i23b-small-s3: A = 843e4ad5b610 `-`, B = 843e4ad5b610 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 31.7 | 33.1 | 1.04 | 1.08 0.88 1.04 |
| small JDBC c1 p95 | ms | 798.7 | 666.5 | 0.83 | 0.80 0.83 0.89 |
| small JDBC c1 p99 | ms | 866.5 | 736.2 | 0.85 | 0.83 0.84 0.91 |
| small JDBC c8 p50 | ms | 326.4 | 163.9 | 0.50 | 0.51 0.52 0.49 |
| small JDBC c8 p95 | ms | 5283.2 | 7193.0 | 1.36 | 1.34 1.37 1.38 |
| small JDBC c8 p99 | ms | 5798.8 | 7944.7 | 1.37 | 1.45 1.38 1.37 |
| small JDBC c32 p50 | ms | 1108.8 | 551.8 | 0.50 | 0.50 0.52 0.48 |
| small JDBC c32 p95 | ms | 16928.7 | 26091.6 | 1.54 | 1.51 1.55 1.58 |
| small JDBC c32 p99 | ms | 19701.6 | 27498.9 | 1.40 | 1.18 1.39 1.44 |
| small ADBC c1 p50 | ms | 23.7 | 21.7 | 0.91 | 0.89 0.95 0.89 |
| small ADBC c1 p95 | ms | 766.3 | 700.7 | 0.91 | 0.89 0.83 0.96 |
| small ADBC c1 p99 | ms | 830.7 | 747.5 | 0.90 | 0.86 0.90 0.94 |
| small ADBC c8 p50 | ms | 326.2 | 163.0 | 0.50 | 0.50 0.58 0.48 |
| small ADBC c8 p95 | ms | 5443.0 | 7248.4 | 1.33 | 1.37 1.27 1.34 |
| small ADBC c8 p99 | ms | 7375.7 | 7817.2 | 1.06 | 1.37 0.96 1.05 |
| small ADBC c32 p50 | ms | 1077.1 | 556.6 | 0.52 | 0.48 0.53 0.52 |
| small ADBC c32 p95 | ms | 17876.7 | 26055.1 | 1.46 | 1.55 1.46 1.42 |
| small ADBC c32 p99 | ms | 24346.7 | 28047.8 | 1.15 | 1.37 1.19 1.15 |
| server RSS peak | MB | 2175.0 | 859.0 | 0.39 | 0.40 0.39 0.39 |

### i23b-small-s3-vs-up-native: A = up-native `-`, B = 843e4ad5b610 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | n/a | 33.1 | n/a | - |
| small JDBC c1 p95 | ms | n/a | 666.5 | n/a | - |
| small JDBC c1 p99 | ms | n/a | 736.2 | n/a | - |
| small JDBC c8 p50 | ms | n/a | 163.9 | n/a | - |
| small JDBC c8 p95 | ms | n/a | 7193.0 | n/a | - |
| small JDBC c8 p99 | ms | n/a | 7944.7 | n/a | - |
| small JDBC c32 p50 | ms | n/a | 551.8 | n/a | - |
| small JDBC c32 p95 | ms | n/a | 26091.6 | n/a | - |
| small JDBC c32 p99 | ms | n/a | 27498.9 | n/a | - |
| small ADBC c1 p50 | ms | n/a | 21.7 | n/a | - |
| small ADBC c1 p95 | ms | n/a | 700.7 | n/a | - |
| small ADBC c1 p99 | ms | n/a | 747.5 | n/a | - |
| small ADBC c8 p50 | ms | n/a | 163.0 | n/a | - |
| small ADBC c8 p95 | ms | n/a | 7248.4 | n/a | - |
| small ADBC c8 p99 | ms | n/a | 7817.2 | n/a | - |
| small ADBC c32 p50 | ms | n/a | 556.6 | n/a | - |
| small ADBC c32 p95 | ms | n/a | 26055.1 | n/a | - |
| small ADBC c32 p99 | ms | n/a | 28047.8 | n/a | - |
| server RSS peak | MB | 391.0 | 859.0 | 2.20 | 2.20 2.20 2.16 |

Correctness gate: A: server (SERVER DIED after small), small-adbc32 (1280/1280 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-adbc8 (640/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point), small-jdbc1 (20/160 errors; answers differ: limit10,limit10_ob,prep_point), small-jdbc8 (461/640 errors; 539/640 errors; 613/640 errors; answers differ: count_filter,limit10,limit10_ob,meta_schemas,meta_tables,point_lineitem,point_orders,prep_point).
