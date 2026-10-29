# Wave track-b3bbcce19996 (server comparison), run 40849716676

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

## Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| core-def-lat-local | ours-new `-` | b3bbcce19996 `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | 0.89 | 1.05 | 0.93 | 1.01 | n/a | n/a | n/a | 0.96 | none |
| core-def-lat-s3 | ours-new `-` | b3bbcce19996 `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | 0.85 | 0.69 | 1.04 | 1.06 | n/a | n/a | n/a | 0.99 | none |
| core-def-sf1-s3 | ours-new `-` | b3bbcce19996 `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 1.00 | n/a | n/a | n/a | none |
| core-def-sf10adbc-s3 | ours-new `-` | b3bbcce19996 `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | 1.02 | n/a | n/a | none |
| core-def-sf10jdbc-s3 | ours-new `-` | b3bbcce19996 `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | 0.85 | n/a | none |
| core-def-tpch-local | ours-new `-` | b3bbcce19996 `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 0.99 | 1.03 | 1.06 | n/a | none |

## Per job (absolute medians and ratios)

### core-def-lat-local: A = ours-new `-`, B = b3bbcce19996 `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `small scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 18.4 | 17.1 | 0.93 | 0.93 0.93 0.99 |
| small JDBC c1 p95 | ms | 38.8 | 37.9 | 0.98 | 0.96 0.98 0.97 |
| small JDBC c1 p99 | ms | 50.5 | 45.2 | 0.90 | 0.97 0.87 0.96 |
| small JDBC c8 p50 | ms | 95.6 | 88.5 | 0.93 | 0.90 0.93 0.97 |
| small JDBC c8 p95 | ms | 226.9 | 242.4 | 1.07 | 1.09 1.09 1.03 |
| small JDBC c8 p99 | ms | 289.0 | 318.3 | 1.10 | 1.12 1.07 1.02 |
| small JDBC c32 p50 | ms | 366.5 | 354.5 | 0.97 | 0.96 0.96 1.00 |
| small JDBC c32 p95 | ms | 1026.6 | 1035.9 | 1.01 | 0.99 0.98 1.04 |
| small JDBC c32 p99 | ms | 1338.2 | 1399.5 | 1.05 | 1.02 1.05 1.05 |
| small ADBC c1 p50 | ms | 13.0 | 11.6 | 0.89 | 0.84 0.95 0.81 |
| small ADBC c1 p95 | ms | 36.3 | 34.7 | 0.96 | 0.93 1.01 0.96 |
| small ADBC c1 p99 | ms | 43.3 | 44.9 | 1.04 | 1.06 0.88 1.01 |
| small ADBC c8 p50 | ms | 84.8 | 78.9 | 0.93 | 0.94 0.92 0.93 |
| small ADBC c8 p95 | ms | 242.1 | 248.8 | 1.03 | 0.94 1.11 1.05 |
| small ADBC c8 p99 | ms | 335.6 | 348.0 | 1.04 | 1.06 1.02 1.00 |
| small ADBC c32 p50 | ms | 347.5 | 335.3 | 0.97 | 0.95 1.00 0.99 |
| small ADBC c32 p95 | ms | 1056.4 | 1106.9 | 1.05 | 1.07 1.08 0.98 |
| small ADBC c32 p99 | ms | 1441.3 | 1486.3 | 1.03 | 1.05 1.01 1.07 |
| lineitem scan x1 | MB/s | 533.2 | 511.3 | 0.96 | 0.94 0.93 1.04 |
| lineitem scan x4 | MB/s | 564.7 | 564.4 | 1.00 | 1.01 0.99 1.01 |
| lineitem scan x8 | MB/s | 505.0 | 505.5 | 1.00 | 1.00 0.98 1.01 |
| lineitem export ADBC | MB/s | 638.1 | 644.9 | 1.01 | 1.02 1.15 1.01 |
| server RSS peak | MB | 1704.0 | 1699.0 | 1.00 | 1.00 1.00 1.00 |

### core-def-lat-s3: A = ours-new `-`, B = b3bbcce19996 `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `small scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 32.8 | 34.2 | 1.04 | 0.92 1.05 1.07 |
| small JDBC c1 p95 | ms | 849.1 | 842.0 | 0.99 | 0.98 0.99 1.02 |
| small JDBC c1 p99 | ms | 897.0 | 885.2 | 0.99 | 0.97 0.99 0.99 |
| small JDBC c8 p50 | ms | 338.4 | 369.8 | 1.09 | 0.96 1.22 1.24 |
| small JDBC c8 p95 | ms | 6546.4 | 6386.5 | 0.98 | 1.00 0.88 1.13 |
| small JDBC c8 p99 | ms | 6985.2 | 6906.5 | 0.99 | 1.01 0.91 1.28 |
| small JDBC c32 p50 | ms | 1150.0 | 1117.9 | 0.97 | 0.97 0.99 0.94 |
| small JDBC c32 p95 | ms | 17922.9 | 18999.5 | 1.06 | 1.06 1.01 1.04 |
| small JDBC c32 p99 | ms | 28633.0 | 30465.6 | 1.06 | 1.06 1.09 2.37 |
| small ADBC c1 p50 | ms | 27.6 | 23.4 | 0.85 | 0.98 0.86 0.65 |
| small ADBC c1 p95 | ms | 871.3 | 839.1 | 0.96 | 0.97 1.01 0.89 |
| small ADBC c1 p99 | ms | 910.5 | 910.3 | 1.00 | 0.97 1.02 0.69 |
| small ADBC c8 p50 | ms | 381.9 | 350.9 | 0.92 | 0.99 0.86 0.98 |
| small ADBC c8 p95 | ms | 6134.1 | 6371.9 | 1.04 | 1.00 1.10 0.99 |
| small ADBC c8 p99 | ms | 6587.4 | 6918.4 | 1.05 | 1.01 1.12 0.79 |
| small ADBC c32 p50 | ms | 1665.5 | 1122.1 | 0.67 | 1.01 0.67 0.94 |
| small ADBC c32 p95 | ms | 26626.1 | 18371.3 | 0.69 | 1.04 0.67 1.02 |
| small ADBC c32 p99 | ms | 31398.4 | 20580.3 | 0.66 | 0.98 0.64 1.23 |
| lineitem scan x1 | MB/s | 385.7 | 382.5 | 0.99 | 1.08 1.00 0.99 |
| lineitem scan x4 | MB/s | 420.6 | 433.8 | 1.03 | 1.05 1.03 0.97 |
| lineitem scan x8 | MB/s | 399.8 | 401.8 | 1.01 | 1.01 1.02 0.99 |
| lineitem export ADBC | MB/s | 428.5 | 404.1 | 0.94 | 1.00 0.93 1.00 |
| server RSS peak | MB | 2640.0 | 2632.0 | 1.00 | 0.99 1.00 0.98 |

### core-def-sf1-s3: A = ours-new `-`, B = b3bbcce19996 `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 26.8 | 26.7 | 1.00 | 0.99 1.02 0.99 |
| TPC-H SF1 JDBC (sum of medians) | s | 26.6 | 26.5 | 1.00 | 1.00 0.99 1.01 |
| server RSS peak | MB | 710.0 | 747.0 | 1.05 | 1.00 1.06 1.09 |

### core-def-sf10adbc-s3: A = ours-new `-`, B = b3bbcce19996 `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | 312.4 | 320.1 | 1.02 | 1.11 0.94 1.06 |
| server RSS peak | MB | 1674.0 | 1580.0 | 0.94 | 0.91 0.96 0.97 |

### core-def-sf10jdbc-s3: A = ours-new `-`, B = b3bbcce19996 `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `sf10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 JDBC (sum of medians) | s | 314.0 | 267.3 | 0.85 | 1.03 0.85 1.00 |
| server RSS peak | MB | 1764.0 | 1589.0 | 0.90 | 0.90 0.90 0.94 |

### core-def-tpch-local: A = ours-new `-`, B = b3bbcce19996 `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 2.7 | 2.6 | 0.99 | 1.01 0.97 1.01 |
| TPC-H SF10 ADBC (sum of medians) | s | 26.6 | 27.4 | 1.03 | 1.11 1.03 1.00 |
| TPC-H SF1 JDBC (sum of medians) | s | 2.8 | 2.8 | 0.99 | 1.00 0.99 0.99 |
| TPC-H SF10 JDBC (sum of medians) | s | 26.1 | 27.6 | 1.06 | 1.11 1.01 1.08 |
| server RSS peak | MB | 1762.0 | 1585.0 | 0.90 | 0.89 0.94 0.90 |
