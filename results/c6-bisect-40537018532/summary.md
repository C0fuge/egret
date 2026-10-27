# Wave c6-bisect (server comparison), run 40537018532

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

## Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 27f5-vs-45fc-local | ours-27f5 `-` | 45fc0a9e6e02 `-` | local | Linux ubuntu24 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C | 5/5 | 0.85 | 1.01 | 0.90 | 0.92 | n/a | 1.00 | n/a | n/a | none |
| 27f5-vs-6acc-local | ours-27f5 `-` | 6acc9cce0b26 `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 5/5 | 0.84 | 0.92 | 0.86 | 0.99 | n/a | 1.00 | n/a | n/a | none |
| 27f5-vs-7562-local | ours-27f5 `-` | ours-new `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor | 5/5 | 0.78 | 0.90 | 0.95 | 1.02 | n/a | 1.01 | n/a | n/a | none |
| 27f5-vs-e46f-local | ours-27f5 `-` | e46f28dfdf09 `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor | 5/5 | 0.79 | 0.90 | 0.88 | 0.89 | n/a | 0.98 | n/a | n/a | none |

## Per job (absolute medians and ratios)

### 27f5-vs-45fc-local: A = ours-27f5 `-`, B = 45fc0a9e6e02 `-`, local

Runner: Linux ubuntu24 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C. Workloads: `adbc10 small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 27.1 | 24.4 | 0.90 | 0.93 0.86 0.93 0.89 0.87 |
| small JDBC c1 p95 | ms | 58.3 | 52.0 | 0.89 | 0.92 0.96 0.89 0.89 0.81 |
| small JDBC c1 p99 | ms | 69.4 | 63.8 | 0.92 | 1.04 1.04 0.85 0.95 0.82 |
| small JDBC c8 p50 | ms | 133.1 | 121.5 | 0.91 | 0.89 0.91 0.86 0.92 0.93 |
| small JDBC c8 p95 | ms | 286.4 | 274.0 | 0.96 | 1.04 0.91 0.96 0.92 0.98 |
| small JDBC c8 p99 | ms | 359.5 | 333.9 | 0.93 | 1.00 0.95 0.89 0.86 0.97 |
| small JDBC c32 p50 | ms | 510.6 | 482.8 | 0.95 | 0.96 0.88 0.95 0.92 0.95 |
| small JDBC c32 p95 | ms | 1190.7 | 1093.9 | 0.92 | 0.92 0.92 0.86 0.89 1.00 |
| small JDBC c32 p99 | ms | 1467.7 | 1402.5 | 0.96 | 0.96 0.97 0.86 0.93 1.00 |
| small ADBC c1 p50 | ms | 20.1 | 17.1 | 0.85 | 0.84 0.86 0.79 0.80 0.87 |
| small ADBC c1 p95 | ms | 46.0 | 44.6 | 0.97 | 0.91 0.90 1.02 0.97 0.97 |
| small ADBC c1 p99 | ms | 65.4 | 63.9 | 0.98 | 0.88 1.13 0.86 0.90 0.93 |
| small ADBC c8 p50 | ms | 131.2 | 114.1 | 0.87 | 0.91 0.86 0.87 0.84 0.86 |
| small ADBC c8 p95 | ms | 285.1 | 258.1 | 0.91 | 0.92 0.85 0.95 0.89 0.96 |
| small ADBC c8 p99 | ms | 342.8 | 321.6 | 0.94 | 0.99 0.88 1.03 0.88 0.88 |
| small ADBC c32 p50 | ms | 509.4 | 410.1 | 0.81 | 0.78 0.81 0.86 0.79 0.88 |
| small ADBC c32 p95 | ms | 1191.8 | 1206.6 | 1.01 | 1.02 1.00 1.04 0.98 1.02 |
| small ADBC c32 p99 | ms | 1463.9 | 1733.3 | 1.18 | 1.20 1.28 1.17 1.20 1.11 |
| TPC-H SF10 ADBC (sum of medians) | s | 40.3 | 40.1 | 1.00 | 0.99 0.99 1.00 1.00 0.99 |
| server RSS peak | MB | 1566.0 | 1546.0 | 0.99 | 0.98 1.00 0.99 0.97 1.01 |

### 27f5-vs-6acc-local: A = ours-27f5 `-`, B = 6acc9cce0b26 `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `adbc10 small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 26.7 | 23.0 | 0.86 | 0.83 0.92 0.83 0.86 0.90 |
| small JDBC c1 p95 | ms | 58.8 | 52.4 | 0.89 | 0.83 1.00 0.89 0.86 0.95 |
| small JDBC c1 p99 | ms | 66.5 | 63.1 | 0.95 | 0.90 1.04 0.85 0.82 0.89 |
| small JDBC c8 p50 | ms | 135.8 | 114.9 | 0.85 | 0.86 0.85 0.87 0.82 0.94 |
| small JDBC c8 p95 | ms | 307.9 | 286.4 | 0.93 | 0.90 0.97 0.96 0.93 0.91 |
| small JDBC c8 p99 | ms | 386.3 | 383.0 | 0.99 | 0.86 1.05 1.08 0.94 0.87 |
| small JDBC c32 p50 | ms | 507.7 | 435.7 | 0.86 | 0.83 0.90 0.82 0.85 0.96 |
| small JDBC c32 p95 | ms | 1270.2 | 1258.1 | 0.99 | 0.89 0.96 1.02 0.98 1.00 |
| small JDBC c32 p99 | ms | 1634.1 | 1677.0 | 1.03 | 0.71 0.95 1.08 1.08 1.03 |
| small ADBC c1 p50 | ms | 19.9 | 16.7 | 0.84 | 0.89 0.81 0.82 0.84 0.81 |
| small ADBC c1 p95 | ms | 47.3 | 45.8 | 0.97 | 1.05 0.97 0.81 1.05 0.87 |
| small ADBC c1 p99 | ms | 64.2 | 53.3 | 0.83 | 0.93 0.80 0.73 1.00 0.80 |
| small ADBC c8 p50 | ms | 123.3 | 107.8 | 0.87 | 0.86 0.83 0.86 0.87 0.88 |
| small ADBC c8 p95 | ms | 288.8 | 269.4 | 0.93 | 0.86 0.93 0.97 0.90 0.97 |
| small ADBC c8 p99 | ms | 347.9 | 329.5 | 0.95 | 0.53 1.00 0.91 0.95 1.12 |
| small ADBC c32 p50 | ms | 460.6 | 405.9 | 0.88 | 0.74 0.85 0.89 0.87 0.94 |
| small ADBC c32 p95 | ms | 1382.9 | 1269.6 | 0.92 | 0.89 0.92 0.89 0.95 0.97 |
| small ADBC c32 p99 | ms | 1773.6 | 1831.6 | 1.03 | 1.10 1.03 0.98 0.82 1.06 |
| TPC-H SF10 ADBC (sum of medians) | s | 37.9 | 37.7 | 1.00 | 1.00 0.99 1.00 0.98 1.02 |
| server RSS peak | MB | 1610.0 | 1640.0 | 1.02 | 1.00 0.95 1.06 1.02 1.02 |

### 27f5-vs-7562-local: A = ours-27f5 `-`, B = ours-new `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `adbc10 small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 19.9 | 19.0 | 0.95 | 1.07 0.89 0.86 0.84 0.87 |
| small JDBC c1 p95 | ms | 41.7 | 39.3 | 0.94 | 1.02 0.99 0.87 0.86 0.93 |
| small JDBC c1 p99 | ms | 56.2 | 51.1 | 0.91 | 0.84 1.09 0.95 0.91 1.01 |
| small JDBC c8 p50 | ms | 97.1 | 86.1 | 0.89 | 0.90 0.89 0.83 0.99 0.86 |
| small JDBC c8 p95 | ms | 218.8 | 210.3 | 0.96 | 0.94 0.96 1.00 0.99 1.00 |
| small JDBC c8 p99 | ms | 272.3 | 260.7 | 0.96 | 0.96 0.91 1.22 1.11 1.02 |
| small JDBC c32 p50 | ms | 352.3 | 340.2 | 0.97 | 0.93 0.84 0.91 1.01 0.86 |
| small JDBC c32 p95 | ms | 900.9 | 915.1 | 1.02 | 0.92 0.93 0.98 1.02 0.97 |
| small JDBC c32 p99 | ms | 1227.8 | 1217.8 | 0.99 | 0.99 0.97 0.99 1.00 0.96 |
| small ADBC c1 p50 | ms | 15.2 | 11.9 | 0.78 | 0.87 0.75 0.75 0.81 0.76 |
| small ADBC c1 p95 | ms | 31.5 | 30.5 | 0.97 | 0.94 0.74 1.01 1.02 1.02 |
| small ADBC c1 p99 | ms | 47.5 | 39.6 | 0.83 | 0.83 0.69 1.03 0.85 0.87 |
| small ADBC c8 p50 | ms | 92.0 | 74.6 | 0.81 | 0.87 0.77 0.81 0.87 0.83 |
| small ADBC c8 p95 | ms | 210.9 | 190.7 | 0.90 | 0.98 0.84 0.88 0.95 0.99 |
| small ADBC c8 p99 | ms | 260.9 | 237.3 | 0.91 | 0.96 0.93 0.94 0.86 0.86 |
| small ADBC c32 p50 | ms | 341.4 | 314.5 | 0.92 | 0.80 0.89 0.89 1.00 0.86 |
| small ADBC c32 p95 | ms | 1038.0 | 930.2 | 0.90 | 0.87 0.89 0.88 0.92 0.87 |
| small ADBC c32 p99 | ms | 1427.1 | 1432.1 | 1.00 | 0.94 1.07 1.01 1.06 0.73 |
| TPC-H SF10 ADBC (sum of medians) | s | 27.0 | 27.3 | 1.01 | 1.06 0.97 1.01 0.99 1.02 |
| server RSS peak | MB | 1734.0 | 1561.0 | 0.90 | 0.89 0.90 0.99 1.08 0.88 |

### 27f5-vs-e46f-local: A = ours-27f5 `-`, B = e46f28dfdf09 `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `adbc10 small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 22.8 | 20.1 | 0.88 | 0.92 0.72 0.99 0.76 1.01 |
| small JDBC c1 p95 | ms | 44.0 | 41.0 | 0.93 | 0.87 0.93 0.96 0.90 0.97 |
| small JDBC c1 p99 | ms | 58.0 | 50.5 | 0.87 | 0.70 1.08 1.06 0.87 1.10 |
| small JDBC c8 p50 | ms | 104.4 | 92.4 | 0.88 | 0.94 0.82 0.94 0.89 0.88 |
| small JDBC c8 p95 | ms | 223.2 | 214.6 | 0.96 | 0.97 0.93 0.92 0.92 0.99 |
| small JDBC c8 p99 | ms | 274.5 | 279.3 | 1.02 | 1.03 1.11 0.89 1.03 0.96 |
| small JDBC c32 p50 | ms | 411.6 | 338.7 | 0.82 | 0.87 0.81 0.88 0.87 0.81 |
| small JDBC c32 p95 | ms | 1030.3 | 912.2 | 0.89 | 0.97 0.84 0.88 0.96 0.90 |
| small JDBC c32 p99 | ms | 1287.2 | 1194.4 | 0.93 | 1.02 0.89 0.92 0.95 0.96 |
| small ADBC c1 p50 | ms | 15.9 | 12.6 | 0.79 | 0.76 0.88 0.77 0.75 0.79 |
| small ADBC c1 p95 | ms | 36.0 | 33.5 | 0.93 | 0.94 1.01 0.87 0.82 0.91 |
| small ADBC c1 p99 | ms | 45.6 | 49.0 | 1.08 | 1.08 1.20 1.08 0.81 0.92 |
| small ADBC c8 p50 | ms | 97.8 | 78.8 | 0.81 | 0.88 0.71 0.84 0.85 0.80 |
| small ADBC c8 p95 | ms | 220.1 | 194.7 | 0.88 | 0.94 0.88 0.98 0.91 0.85 |
| small ADBC c8 p99 | ms | 277.8 | 246.9 | 0.89 | 0.91 0.87 1.01 0.93 0.83 |
| small ADBC c32 p50 | ms | 363.4 | 325.6 | 0.90 | 0.92 0.91 0.90 0.86 0.89 |
| small ADBC c32 p95 | ms | 1066.5 | 963.1 | 0.90 | 0.93 0.86 0.89 0.96 0.88 |
| small ADBC c32 p99 | ms | 1413.0 | 1368.8 | 0.97 | 0.90 0.97 0.92 0.91 1.27 |
| TPC-H SF10 ADBC (sum of medians) | s | 27.7 | 27.2 | 0.98 | 0.99 0.97 1.00 0.98 0.99 |
| server RSS peak | MB | 1723.0 | 1621.0 | 0.94 | 1.09 0.90 1.02 1.01 0.93 |
