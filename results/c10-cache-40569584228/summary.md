# Wave c10-cache (server comparison), run 40569584228

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

## Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cache-off-vs-on-s3 | ours-cache `-DduckDbThreads=4` | ours-cache `-DduckDbThreads=4 -Darrowflight.s3.cacheMegabytes=1024` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | 0.33 | 0.06 | 0.64 | 0.07 | 0.32 | 1.08 | n/a | n/a | none |
| new-vs-84fe-s3 | ours-new `-DduckDbThreads=4` | 84fec772ec50 `-DduckDbThreads=4` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | 1.23 | 1.58 | 0.99 | 1.51 | 1.45 | 0.83 | n/a | n/a | none |
| new-vs-cache-off-s3 | ours-new `-DduckDbThreads=4` | ours-cache `-DduckDbThreads=4` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | 1.09 | 1.02 | 0.88 | 1.02 | 1.00 | 1.01 | n/a | n/a | none |
| new-vs-cache-on-s3 | ours-new `-DduckDbThreads=4` | ours-cache `-DduckDbThreads=4 -Darrowflight.s3.cacheMegabytes=1024` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | 0.57 | 0.11 | 0.70 | 0.11 | 0.47 | 1.08 | n/a | n/a | none |

## Per job (absolute medians and ratios)

### cache-off-vs-on-s3: A = ours-cache `-DduckDbThreads=4`, B = ours-cache `-DduckDbThreads=4 -Darrowflight.s3.cacheMegabytes=1024`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `adbc10 adbc1 small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 30.1 | 19.3 | 0.64 | 0.70 0.59 0.58 |
| small JDBC c1 p95 | ms | 986.1 | 82.1 | 0.08 | 0.12 0.08 0.09 |
| small JDBC c1 p99 | ms | 1019.2 | 102.5 | 0.10 | 0.13 0.10 0.10 |
| small JDBC c8 p50 | ms | 383.9 | 89.2 | 0.23 | 0.37 0.21 0.23 |
| small JDBC c8 p95 | ms | 5940.2 | 294.1 | 0.05 | 0.07 0.05 0.05 |
| small JDBC c8 p99 | ms | 6687.1 | 338.6 | 0.05 | 0.07 0.04 0.05 |
| small JDBC c32 p50 | ms | 1389.9 | 404.5 | 0.29 | 0.42 0.29 0.28 |
| small JDBC c32 p95 | ms | 20034.4 | 1350.4 | 0.07 | 0.11 0.06 0.07 |
| small JDBC c32 p99 | ms | 22775.5 | 1616.1 | 0.07 | 0.11 0.06 0.07 |
| small ADBC c1 p50 | ms | 33.4 | 11.2 | 0.33 | 0.54 0.32 0.32 |
| small ADBC c1 p95 | ms | 988.3 | 75.9 | 0.08 | 0.11 0.08 0.08 |
| small ADBC c1 p99 | ms | 1058.4 | 102.5 | 0.10 | 0.14 0.10 0.09 |
| small ADBC c8 p50 | ms | 312.5 | 68.6 | 0.22 | 0.30 0.17 0.22 |
| small ADBC c8 p95 | ms | 6047.9 | 302.8 | 0.05 | 0.08 0.05 0.05 |
| small ADBC c8 p99 | ms | 6900.9 | 348.5 | 0.05 | 0.08 0.05 0.03 |
| small ADBC c32 p50 | ms | 1373.9 | 328.4 | 0.24 | 0.37 0.25 0.22 |
| small ADBC c32 p95 | ms | 20900.7 | 1261.2 | 0.06 | 0.09 0.05 0.06 |
| small ADBC c32 p99 | ms | 25111.4 | 1462.5 | 0.06 | 0.06 0.05 0.06 |
| TPC-H SF1 ADBC (sum of medians) | s | 34.4 | 11.0 | 0.32 | 0.45 0.34 0.31 |
| TPC-H SF10 ADBC (sum of medians) | s | 350.7 | 380.0 | 1.08 | 1.22 1.08 1.22 |
| server RSS peak | MB | 2338.0 | 5725.0 | 2.45 | 2.33 2.63 2.47 |

### new-vs-84fe-s3: A = ours-new `-DduckDbThreads=4`, B = 84fec772ec50 `-DduckDbThreads=4`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `adbc10 adbc1 small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 33.0 | 32.7 | 0.99 | 0.99 1.04 0.96 |
| small JDBC c1 p95 | ms | 744.9 | 735.1 | 0.99 | 0.98 1.08 0.99 |
| small JDBC c1 p99 | ms | 1236.8 | 794.9 | 0.64 | 0.59 1.55 0.95 |
| small JDBC c8 p50 | ms | 352.9 | 360.5 | 1.02 | 1.02 0.97 0.99 |
| small JDBC c8 p95 | ms | 5226.0 | 6114.8 | 1.17 | 1.22 0.97 1.01 |
| small JDBC c8 p99 | ms | 5621.7 | 7812.5 | 1.39 | 1.45 0.97 0.99 |
| small JDBC c32 p50 | ms | 1101.4 | 1654.9 | 1.50 | 1.81 0.95 1.13 |
| small JDBC c32 p95 | ms | 16373.8 | 24699.2 | 1.51 | 1.54 1.00 1.27 |
| small JDBC c32 p99 | ms | 18204.6 | 27091.2 | 1.49 | 1.83 1.00 1.41 |
| small ADBC c1 p50 | ms | 23.7 | 29.1 | 1.23 | 1.06 1.09 1.26 |
| small ADBC c1 p95 | ms | 780.0 | 730.6 | 0.94 | 0.91 1.01 0.98 |
| small ADBC c1 p99 | ms | 805.7 | 867.2 | 1.08 | 1.08 0.94 1.03 |
| small ADBC c8 p50 | ms | 338.3 | 454.0 | 1.34 | 1.37 0.92 0.96 |
| small ADBC c8 p95 | ms | 5300.6 | 7484.0 | 1.41 | 1.41 1.02 0.97 |
| small ADBC c8 p99 | ms | 5992.5 | 8189.4 | 1.37 | 1.42 1.11 0.92 |
| small ADBC c32 p50 | ms | 1084.7 | 1446.6 | 1.33 | 1.33 0.97 1.39 |
| small ADBC c32 p95 | ms | 16144.8 | 25498.1 | 1.58 | 1.61 1.06 1.58 |
| small ADBC c32 p99 | ms | 17999.0 | 49262.6 | 2.74 | 3.87 1.20 2.74 |
| TPC-H SF1 ADBC (sum of medians) | s | 26.0 | 37.7 | 1.45 | 1.45 0.97 1.50 |
| TPC-H SF10 ADBC (sum of medians) | s | 353.6 | 292.7 | 0.83 | 1.00 1.03 0.82 |
| server RSS peak | MB | 2327.0 | 2200.0 | 0.95 | 0.97 0.98 0.92 |

### new-vs-cache-off-s3: A = ours-new `-DduckDbThreads=4`, B = ours-cache `-DduckDbThreads=4`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `adbc10 adbc1 small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 33.3 | 29.2 | 0.88 | 0.87 0.87 1.09 |
| small JDBC c1 p95 | ms | 938.9 | 946.0 | 1.01 | 1.01 1.00 1.01 |
| small JDBC c1 p99 | ms | 994.9 | 1046.5 | 1.05 | 1.03 1.06 0.98 |
| small JDBC c8 p50 | ms | 357.5 | 343.7 | 0.96 | 1.05 1.07 0.92 |
| small JDBC c8 p95 | ms | 6030.4 | 6179.9 | 1.02 | 0.99 1.02 1.04 |
| small JDBC c8 p99 | ms | 12674.3 | 13878.0 | 1.09 | 0.93 0.94 1.71 |
| small JDBC c32 p50 | ms | 1462.3 | 1447.3 | 0.99 | 0.97 0.98 0.99 |
| small JDBC c32 p95 | ms | 20678.8 | 21037.1 | 1.02 | 0.99 1.02 0.99 |
| small JDBC c32 p99 | ms | 23508.4 | 37791.8 | 1.61 | 0.98 1.78 1.16 |
| small ADBC c1 p50 | ms | 30.8 | 33.5 | 1.09 | 1.33 1.11 0.97 |
| small ADBC c1 p95 | ms | 958.6 | 947.7 | 0.99 | 1.03 0.96 1.00 |
| small ADBC c1 p99 | ms | 1058.6 | 1018.0 | 0.96 | 1.16 0.96 0.98 |
| small ADBC c8 p50 | ms | 393.5 | 395.4 | 1.00 | 0.97 0.98 1.04 |
| small ADBC c8 p95 | ms | 5783.8 | 5753.0 | 0.99 | 1.01 1.04 0.99 |
| small ADBC c8 p99 | ms | 6192.5 | 6423.9 | 1.04 | 0.97 1.05 1.03 |
| small ADBC c32 p50 | ms | 1434.8 | 1517.5 | 1.06 | 1.76 0.98 1.06 |
| small ADBC c32 p95 | ms | 20184.1 | 20529.9 | 1.02 | 1.48 1.02 1.04 |
| small ADBC c32 p99 | ms | 23026.9 | 23300.3 | 1.01 | 1.31 1.00 1.02 |
| TPC-H SF1 ADBC (sum of medians) | s | 33.7 | 33.7 | 1.00 | 1.40 0.97 1.00 |
| TPC-H SF10 ADBC (sum of medians) | s | 385.1 | 387.7 | 1.01 | 1.01 1.00 1.02 |
| server RSS peak | MB | 2324.0 | 2309.0 | 0.99 | 0.97 0.95 1.04 |

### new-vs-cache-on-s3: A = ours-new `-DduckDbThreads=4`, B = ours-cache `-DduckDbThreads=4 -Darrowflight.s3.cacheMegabytes=1024`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `adbc10 adbc1 small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 33.5 | 23.5 | 0.70 | 0.70 0.52 0.79 |
| small JDBC c1 p95 | ms | 811.5 | 100.9 | 0.12 | 0.12 0.08 0.13 |
| small JDBC c1 p99 | ms | 1685.7 | 113.9 | 0.07 | 0.06 0.07 0.13 |
| small JDBC c8 p50 | ms | 345.9 | 125.7 | 0.36 | 0.38 0.25 0.36 |
| small JDBC c8 p95 | ms | 5656.2 | 413.8 | 0.07 | 0.08 0.06 0.07 |
| small JDBC c8 p99 | ms | 7054.0 | 472.5 | 0.07 | 0.08 0.06 0.07 |
| small JDBC c32 p50 | ms | 1071.1 | 540.9 | 0.51 | 0.53 0.34 0.49 |
| small JDBC c32 p95 | ms | 16580.3 | 1835.4 | 0.11 | 0.11 0.07 0.12 |
| small JDBC c32 p99 | ms | 27540.0 | 2231.8 | 0.08 | 0.04 0.08 0.11 |
| small ADBC c1 p50 | ms | 25.7 | 14.6 | 0.57 | 0.66 0.37 0.57 |
| small ADBC c1 p95 | ms | 780.8 | 94.0 | 0.12 | 0.12 0.09 0.12 |
| small ADBC c1 p99 | ms | 860.1 | 110.0 | 0.13 | 0.13 0.10 0.13 |
| small ADBC c8 p50 | ms | 352.7 | 98.0 | 0.28 | 0.28 0.21 0.30 |
| small ADBC c8 p95 | ms | 5503.0 | 418.4 | 0.08 | 0.08 0.06 0.08 |
| small ADBC c8 p99 | ms | 6089.1 | 494.0 | 0.08 | 0.34 0.06 0.08 |
| small ADBC c32 p50 | ms | 1094.9 | 443.4 | 0.40 | 0.40 0.29 0.46 |
| small ADBC c32 p95 | ms | 16677.5 | 1789.2 | 0.11 | 0.11 0.07 0.12 |
| small ADBC c32 p99 | ms | 37918.8 | 2863.7 | 0.08 | 0.18 0.05 0.08 |
| TPC-H SF1 ADBC (sum of medians) | s | 26.9 | 12.6 | 0.47 | 0.49 0.32 0.48 |
| TPC-H SF10 ADBC (sum of medians) | s | 389.1 | 419.2 | 1.08 | 1.45 1.32 1.03 |
| server RSS peak | MB | 2219.0 | 5709.0 | 2.57 | 2.46 2.60 2.55 |
