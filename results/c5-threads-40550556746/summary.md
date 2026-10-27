# Wave c5-threads (server comparison), run 40550556746

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

## Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| threads-4-vs-1-local | ours-new `-` | ours-new `-DduckDbThreads=1` | local | Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | 0.86 | 0.88 | 0.91 | 0.90 | 1.23 | 1.37 | n/a | n/a | none |
| threads-4-vs-2-local | ours-new `-` | ours-new `-DduckDbThreads=2` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | 0.91 | 0.89 | 0.99 | 0.99 | 0.92 | 0.99 | n/a | n/a | none |
| threads-4-vs-8-local | ours-new `-` | ours-new `-DduckDbThreads=8` | local | Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | 1.08 | 0.98 | 1.06 | 1.02 | 1.04 | 1.03 | n/a | n/a | none |

## Per job (absolute medians and ratios)

### threads-4-vs-1-local: A = ours-new `-`, B = ours-new `-DduckDbThreads=1`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `adbc10 adbc1 small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 27.3 | 24.9 | 0.91 | 0.90 1.01 0.90 |
| small JDBC c1 p95 | ms | 57.0 | 56.6 | 0.99 | 0.97 1.08 0.92 |
| small JDBC c1 p99 | ms | 68.2 | 70.3 | 1.03 | 0.98 1.28 0.98 |
| small JDBC c8 p50 | ms | 134.8 | 76.0 | 0.56 | 0.55 0.60 0.56 |
| small JDBC c8 p95 | ms | 291.2 | 313.4 | 1.08 | 1.05 1.12 1.06 |
| small JDBC c8 p99 | ms | 352.0 | 345.0 | 0.98 | 0.93 1.03 0.97 |
| small JDBC c32 p50 | ms | 492.1 | 244.1 | 0.50 | 0.48 0.52 0.50 |
| small JDBC c32 p95 | ms | 1297.7 | 1169.6 | 0.90 | 0.86 0.91 0.91 |
| small JDBC c32 p99 | ms | 1775.1 | 1341.9 | 0.76 | 0.74 0.83 0.74 |
| small ADBC c1 p50 | ms | 18.1 | 15.5 | 0.86 | 0.85 0.92 0.88 |
| small ADBC c1 p95 | ms | 47.5 | 47.6 | 1.00 | 0.98 1.02 0.98 |
| small ADBC c1 p99 | ms | 54.6 | 59.2 | 1.08 | 1.08 1.14 0.87 |
| small ADBC c8 p50 | ms | 118.2 | 66.5 | 0.56 | 0.55 0.58 0.57 |
| small ADBC c8 p95 | ms | 312.6 | 311.4 | 1.00 | 1.01 1.09 0.98 |
| small ADBC c8 p99 | ms | 600.8 | 355.9 | 0.59 | 0.59 1.05 0.58 |
| small ADBC c32 p50 | ms | 476.7 | 226.3 | 0.47 | 0.47 0.49 0.47 |
| small ADBC c32 p95 | ms | 1321.5 | 1157.1 | 0.88 | 0.86 0.95 0.89 |
| small ADBC c32 p99 | ms | 1689.7 | 1288.2 | 0.76 | 0.92 0.84 0.76 |
| TPC-H SF1 ADBC (sum of medians) | s | 4.2 | 5.2 | 1.23 | 1.19 1.22 1.25 |
| TPC-H SF10 ADBC (sum of medians) | s | 41.9 | 57.5 | 1.37 | 1.30 1.43 1.41 |
| server RSS peak | MB | 1733.0 | 1734.0 | 1.00 | 1.41 1.00 1.06 |

### threads-4-vs-2-local: A = ours-new `-`, B = ours-new `-DduckDbThreads=2`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `adbc10 adbc1 small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 22.5 | 22.2 | 0.99 | 0.99 1.08 0.92 |
| small JDBC c1 p95 | ms | 52.8 | 49.1 | 0.93 | 0.93 1.05 0.98 |
| small JDBC c1 p99 | ms | 62.0 | 64.5 | 1.04 | 1.05 1.00 0.95 |
| small JDBC c8 p50 | ms | 115.3 | 90.7 | 0.79 | 0.78 0.81 0.79 |
| small JDBC c8 p95 | ms | 291.5 | 284.4 | 0.98 | 0.98 0.97 0.96 |
| small JDBC c8 p99 | ms | 359.6 | 318.8 | 0.89 | 0.89 0.86 0.90 |
| small JDBC c32 p50 | ms | 465.1 | 343.1 | 0.74 | 0.73 0.76 0.74 |
| small JDBC c32 p95 | ms | 1199.4 | 1188.0 | 0.99 | 1.01 0.99 0.99 |
| small JDBC c32 p99 | ms | 1545.1 | 1612.6 | 1.04 | 1.11 1.05 1.04 |
| small ADBC c1 p50 | ms | 17.2 | 15.7 | 0.91 | 0.99 0.85 0.92 |
| small ADBC c1 p95 | ms | 45.8 | 43.8 | 0.96 | 0.96 0.93 1.11 |
| small ADBC c1 p99 | ms | 53.2 | 59.7 | 1.12 | 1.24 1.07 1.05 |
| small ADBC c8 p50 | ms | 106.2 | 82.9 | 0.78 | 0.76 0.77 0.78 |
| small ADBC c8 p95 | ms | 271.3 | 272.0 | 1.00 | 1.02 1.01 0.93 |
| small ADBC c8 p99 | ms | 321.3 | 301.7 | 0.94 | 1.01 0.94 0.86 |
| small ADBC c32 p50 | ms | 414.4 | 330.4 | 0.80 | 0.78 0.80 0.84 |
| small ADBC c32 p95 | ms | 1309.2 | 1168.3 | 0.89 | 0.89 0.91 0.85 |
| small ADBC c32 p99 | ms | 1873.4 | 1524.4 | 0.81 | 0.84 0.80 0.76 |
| TPC-H SF1 ADBC (sum of medians) | s | 4.0 | 3.7 | 0.92 | 0.91 0.94 0.92 |
| TPC-H SF10 ADBC (sum of medians) | s | 38.4 | 38.0 | 0.99 | 0.97 0.99 0.99 |
| server RSS peak | MB | 1624.0 | 1835.0 | 1.13 | 1.04 1.14 1.07 |

### threads-4-vs-8-local: A = ours-new `-`, B = ours-new `-DduckDbThreads=8`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `adbc10 adbc1 small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 18.8 | 19.9 | 1.06 | 1.07 0.89 1.06 |
| small JDBC c1 p95 | ms | 41.9 | 44.0 | 1.05 | 1.10 0.98 1.06 |
| small JDBC c1 p99 | ms | 49.3 | 52.6 | 1.07 | 1.07 0.98 1.11 |
| small JDBC c8 p50 | ms | 96.8 | 105.0 | 1.09 | 1.06 1.11 1.11 |
| small JDBC c8 p95 | ms | 231.6 | 241.5 | 1.04 | 0.97 1.06 1.03 |
| small JDBC c8 p99 | ms | 293.6 | 297.8 | 1.01 | 0.96 1.12 0.93 |
| small JDBC c32 p50 | ms | 372.3 | 415.7 | 1.12 | 1.11 1.08 1.14 |
| small JDBC c32 p95 | ms | 1039.6 | 1064.7 | 1.02 | 0.96 1.04 1.09 |
| small JDBC c32 p99 | ms | 1387.7 | 1370.5 | 0.99 | 0.93 0.96 1.08 |
| small ADBC c1 p50 | ms | 13.0 | 14.1 | 1.08 | 1.08 1.13 1.11 |
| small ADBC c1 p95 | ms | 37.0 | 38.2 | 1.03 | 0.99 1.17 1.03 |
| small ADBC c1 p99 | ms | 46.7 | 48.8 | 1.04 | 1.04 1.26 0.81 |
| small ADBC c8 p50 | ms | 87.5 | 95.1 | 1.09 | 1.15 1.06 1.09 |
| small ADBC c8 p95 | ms | 239.9 | 253.7 | 1.06 | 1.03 1.07 1.07 |
| small ADBC c8 p99 | ms | 337.4 | 354.1 | 1.05 | 1.10 1.03 1.09 |
| small ADBC c32 p50 | ms | 341.2 | 397.2 | 1.16 | 1.12 1.14 1.20 |
| small ADBC c32 p95 | ms | 1044.9 | 1024.7 | 0.98 | 1.04 0.98 0.94 |
| small ADBC c32 p99 | ms | 1402.1 | 1302.8 | 0.93 | 1.01 1.02 0.87 |
| TPC-H SF1 ADBC (sum of medians) | s | 3.3 | 3.4 | 1.04 | 1.04 1.04 1.03 |
| TPC-H SF10 ADBC (sum of medians) | s | 31.1 | 32.2 | 1.03 | 1.04 1.04 1.02 |
| server RSS peak | MB | 1728.0 | 1771.0 | 1.02 | 1.00 0.99 1.14 |
