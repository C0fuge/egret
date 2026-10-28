# Wave track-load-d22cdaccb4e1 (server comparison), run 40621069419

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

## Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| core-def-lat-local | ours-new `-` | d22cdaccb4e1 `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | 0.94 | 0.88 | 0.95 | 0.86 | n/a | n/a | n/a | 1.00 | none |
| core-def-lat-s3 | ours-new `-` | d22cdaccb4e1 `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | 0.88 | 0.82 | 0.91 | 1.21 | n/a | n/a | n/a | 1.01 | none |
| core-def-sf1-s3 | ours-new `-` | d22cdaccb4e1 `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 1.04 | n/a | n/a | n/a | none |
| core-def-sf10adbc-s3 | ours-new `-` | d22cdaccb4e1 `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | 0.84 | n/a | n/a | none |
| core-def-sf10jdbc-s3 | ours-new `-` | d22cdaccb4e1 `-` | s3 | Linux ubuntu24 4 vCPU Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | 0.60 | n/a | none |
| core-def-tpch-local | ours-new `-` | d22cdaccb4e1 `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 0.94 | 0.98 | 0.99 | n/a | none |
| core-def-tpch-s3 | ours-new `-` | d22cdaccb4e1 `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 0.92 | 0.89 | 0.82 | n/a | none |
| core-t4-lat-local | ours-new `-DduckDbThreads=4` | d22cdaccb4e1 `-DduckDbThreads=4` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | 1.05 | 1.04 | 0.96 | 1.01 | n/a | n/a | n/a | 1.02 | none |
| core-t4-tpch-local | ours-new `-DduckDbThreads=4` | d22cdaccb4e1 `-DduckDbThreads=4` | local | Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 1.01 | 0.99 | 1.00 | n/a | none |
| i20-fast-lz4-local | d22cdaccb4e1 `-` | d22cdaccb4e1 `CLZ4` | local | Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | 0.98 | n/a | n/a | none |
| i20-fast-zstd-local | d22cdaccb4e1 `-` | d22cdaccb4e1 `CZSTD` | local | Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | 1.00 | n/a | n/a | none |
| i20-lz4-netem-local | ours-new `-` | d22cdaccb4e1 `CLZ4` | local | Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| i20-lz4-vs-native-zstd-netem-local | d22cdaccb4e1 `CLZ4` | up-native `-DflightCompression=zstd` | local | Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| i20-native-zstd-netem-local | d22cdaccb4e1 `CZSTD` | up-native `-DflightCompression=zstd` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| i20-plain-netem-local | ours-new `-` | d22cdaccb4e1 `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| i20-zstd-netem-local | ours-new `-` | d22cdaccb4e1 `CZSTD` | local | Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| i20-zstd-vs-lz4-netem-local | d22cdaccb4e1 `CZSTD` | d22cdaccb4e1 `CLZ4` | local | Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |

## Per job (absolute medians and ratios)

### core-def-lat-local: A = ours-new `-`, B = d22cdaccb4e1 `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 26.9 | 25.6 | 0.95 | 1.04 0.95 0.94 |
| small JDBC c1 p95 | ms | 53.8 | 53.6 | 1.00 | 0.97 1.00 0.92 |
| small JDBC c1 p99 | ms | 67.0 | 65.5 | 0.98 | 0.89 1.07 0.91 |
| small JDBC c8 p50 | ms | 126.0 | 99.9 | 0.79 | 0.81 0.80 0.78 |
| small JDBC c8 p95 | ms | 296.2 | 287.7 | 0.97 | 1.00 1.01 0.97 |
| small JDBC c8 p99 | ms | 372.3 | 332.7 | 0.89 | 0.80 0.95 0.87 |
| small JDBC c32 p50 | ms | 482.3 | 370.7 | 0.77 | 0.88 0.73 0.76 |
| small JDBC c32 p95 | ms | 1408.4 | 1217.4 | 0.86 | 0.90 0.92 0.86 |
| small JDBC c32 p99 | ms | 1822.5 | 1615.9 | 0.89 | 0.99 0.77 0.89 |
| small ADBC c1 p50 | ms | 17.8 | 16.7 | 0.94 | 0.83 1.00 0.91 |
| small ADBC c1 p95 | ms | 48.0 | 46.8 | 0.98 | 0.99 0.98 0.95 |
| small ADBC c1 p99 | ms | 55.9 | 58.8 | 1.05 | 1.10 1.06 0.82 |
| small ADBC c8 p50 | ms | 114.9 | 87.1 | 0.76 | 0.77 0.76 0.73 |
| small ADBC c8 p95 | ms | 268.3 | 281.1 | 1.05 | 0.99 1.07 1.05 |
| small ADBC c8 p99 | ms | 336.0 | 321.6 | 0.96 | 0.95 1.08 0.95 |
| small ADBC c32 p50 | ms | 440.6 | 350.9 | 0.80 | 0.83 0.80 0.78 |
| small ADBC c32 p95 | ms | 1341.5 | 1175.8 | 0.88 | 0.89 0.91 0.82 |
| small ADBC c32 p99 | ms | 1759.2 | 1450.3 | 0.82 | 0.73 0.82 0.77 |
| lineitem scan x1 | MB/s | 443.9 | 442.1 | 1.00 | 1.00 1.00 1.01 |
| lineitem scan x4 | MB/s | 494.6 | 530.4 | 1.07 | 1.06 1.05 1.10 |
| lineitem scan x8 | MB/s | 458.0 | 527.5 | 1.15 | 1.15 1.15 1.12 |
| lineitem export ADBC | MB/s | 524.2 | 530.3 | 1.01 | 1.07 1.00 1.03 |
| server RSS peak | MB | 1755.0 | 1654.0 | 0.94 | 0.94 0.96 0.96 |

### core-def-lat-s3: A = ours-new `-`, B = d22cdaccb4e1 `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 30.6 | 28.0 | 0.91 | 1.02 0.90 0.91 |
| small JDBC c1 p95 | ms | 792.0 | 660.5 | 0.83 | 0.84 0.80 0.86 |
| small JDBC c1 p99 | ms | 848.0 | 706.6 | 0.83 | 0.84 0.79 0.84 |
| small JDBC c8 p50 | ms | 331.4 | 248.6 | 0.75 | 0.75 0.83 0.65 |
| small JDBC c8 p95 | ms | 5883.3 | 6597.4 | 1.12 | 1.18 1.12 1.36 |
| small JDBC c8 p99 | ms | 11952.2 | 7541.8 | 0.63 | 1.22 0.59 0.75 |
| small JDBC c32 p50 | ms | 1105.1 | 737.0 | 0.67 | 0.71 0.64 0.69 |
| small JDBC c32 p95 | ms | 16787.4 | 20322.3 | 1.21 | 1.13 1.26 1.13 |
| small JDBC c32 p99 | ms | 23354.3 | 26447.5 | 1.13 | 0.92 1.48 0.83 |
| small ADBC c1 p50 | ms | 24.2 | 21.2 | 0.88 | 0.86 0.95 0.79 |
| small ADBC c1 p95 | ms | 797.6 | 655.3 | 0.82 | 0.87 0.82 0.80 |
| small ADBC c1 p99 | ms | 849.7 | 713.8 | 0.84 | 0.85 0.84 0.82 |
| small ADBC c8 p50 | ms | 365.1 | 237.5 | 0.65 | 0.66 0.65 0.74 |
| small ADBC c8 p95 | ms | 5423.3 | 6525.3 | 1.20 | 1.20 1.19 1.31 |
| small ADBC c8 p99 | ms | 6455.8 | 7025.7 | 1.09 | 1.20 1.05 1.38 |
| small ADBC c32 p50 | ms | 1482.1 | 740.6 | 0.50 | 0.61 0.50 0.70 |
| small ADBC c32 p95 | ms | 24285.3 | 19815.7 | 0.82 | 1.22 0.81 1.11 |
| small ADBC c32 p99 | ms | 34362.3 | 21139.2 | 0.62 | 1.15 0.62 0.87 |
| lineitem scan x1 | MB/s | 413.9 | 416.3 | 1.01 | 0.99 1.01 0.99 |
| lineitem scan x4 | MB/s | 483.2 | 493.7 | 1.02 | 1.03 1.05 0.98 |
| lineitem scan x8 | MB/s | 462.2 | 507.9 | 1.10 | 1.10 1.09 1.10 |
| lineitem export ADBC | MB/s | 438.0 | 464.6 | 1.06 | 0.99 1.05 1.09 |
| server RSS peak | MB | 2814.0 | 2572.0 | 0.91 | 0.90 0.95 1.01 |

### core-def-sf1-s3: A = ours-new `-`, B = d22cdaccb4e1 `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 24.2 | 25.3 | 1.04 | 1.08 0.99 1.04 |
| TPC-H SF1 JDBC (sum of medians) | s | 23.9 | 24.6 | 1.03 | 1.02 1.03 1.03 |
| server RSS peak | MB | 801.0 | 877.0 | 1.09 | 0.97 1.12 1.10 |

### core-def-sf10adbc-s3: A = ours-new `-`, B = d22cdaccb4e1 `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | 316.7 | 266.6 | 0.84 | 1.03 0.83 0.91 |
| server RSS peak | MB | 1767.0 | 2018.0 | 1.14 | 1.27 1.13 1.04 |

### core-def-sf10jdbc-s3: A = ours-new `-`, B = d22cdaccb4e1 `-`, s3

Runner: Linux ubuntu24 4 vCPU Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz. Workloads: `sf10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 JDBC (sum of medians) | s | 451.9 | 269.3 | 0.60 | 0.86 0.60 0.83 |
| server RSS peak | MB | 1627.0 | 1721.0 | 1.06 | 1.05 1.06 1.05 |

### core-def-tpch-local: A = ours-new `-`, B = d22cdaccb4e1 `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 4.0 | 3.7 | 0.94 | 0.94 0.94 0.94 |
| TPC-H SF10 ADBC (sum of medians) | s | 39.3 | 38.6 | 0.98 | 0.98 0.98 0.98 |
| TPC-H SF1 JDBC (sum of medians) | s | 4.1 | 3.8 | 0.93 | 0.93 0.93 0.93 |
| TPC-H SF10 JDBC (sum of medians) | s | 38.8 | 38.5 | 0.99 | 0.99 0.98 0.99 |
| server RSS peak | MB | 1722.0 | 1776.0 | 1.03 | 1.10 0.99 1.03 |

### core-def-tpch-s3: A = ours-new `-`, B = d22cdaccb4e1 `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 40.3 | 37.0 | 0.92 | 1.38 0.93 |
| TPC-H SF10 ADBC (sum of medians) | s | 463.6 | 414.8 | 0.89 | 1.40 0.88 |
| TPC-H SF1 JDBC (sum of medians) | s | 38.5 | 35.8 | 0.93 | 1.36 0.92 |
| TPC-H SF10 JDBC (sum of medians) | s | 489.9 | 401.9 | 0.82 | 0.96 0.81 0.83 |
| server RSS peak | MB | 1754.0 | 1805.0 | 1.03 | 1.05 1.03 1.01 |

### core-t4-lat-local: A = ours-new `-DduckDbThreads=4`, B = d22cdaccb4e1 `-DduckDbThreads=4`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 26.1 | 25.2 | 0.96 | 0.98 0.95 0.94 |
| small JDBC c1 p95 | ms | 53.2 | 51.9 | 0.97 | 1.00 0.97 1.03 |
| small JDBC c1 p99 | ms | 61.6 | 65.2 | 1.06 | 0.95 1.16 1.07 |
| small JDBC c8 p50 | ms | 130.1 | 126.3 | 0.97 | 1.10 0.95 0.97 |
| small JDBC c8 p95 | ms | 299.5 | 291.0 | 0.97 | 1.10 0.95 0.93 |
| small JDBC c8 p99 | ms | 391.5 | 351.7 | 0.90 | 1.21 0.90 0.85 |
| small JDBC c32 p50 | ms | 474.2 | 494.1 | 1.04 | 0.99 1.06 1.05 |
| small JDBC c32 p95 | ms | 1340.6 | 1355.3 | 1.01 | 1.01 0.99 1.06 |
| small JDBC c32 p99 | ms | 1949.0 | 1943.5 | 1.00 | 1.11 0.94 1.08 |
| small ADBC c1 p50 | ms | 17.3 | 18.1 | 1.05 | 1.08 0.97 1.05 |
| small ADBC c1 p95 | ms | 48.6 | 46.6 | 0.96 | 0.95 0.92 1.06 |
| small ADBC c1 p99 | ms | 58.0 | 52.2 | 0.90 | 0.90 0.88 1.07 |
| small ADBC c8 p50 | ms | 114.8 | 116.5 | 1.01 | 1.01 1.00 1.03 |
| small ADBC c8 p95 | ms | 277.4 | 284.8 | 1.03 | 1.03 1.03 1.04 |
| small ADBC c8 p99 | ms | 324.9 | 339.8 | 1.05 | 1.00 1.06 1.02 |
| small ADBC c32 p50 | ms | 445.2 | 447.3 | 1.00 | 0.99 1.00 1.02 |
| small ADBC c32 p95 | ms | 1261.8 | 1306.8 | 1.04 | 1.05 1.05 0.95 |
| small ADBC c32 p99 | ms | 1886.7 | 1841.1 | 0.98 | 1.12 0.82 1.04 |
| lineitem scan x1 | MB/s | 432.8 | 442.6 | 1.02 | 1.01 1.13 1.04 |
| lineitem scan x4 | MB/s | 462.1 | 461.5 | 1.00 | 1.00 0.97 1.00 |
| lineitem scan x8 | MB/s | 419.8 | 420.6 | 1.00 | 1.01 1.00 1.01 |
| lineitem export ADBC | MB/s | 519.7 | 515.8 | 0.99 | 0.86 0.99 1.18 |
| server RSS peak | MB | 1738.0 | 1708.0 | 0.98 | 1.00 0.96 0.98 |

### core-t4-tpch-local: A = ours-new `-DduckDbThreads=4`, B = d22cdaccb4e1 `-DduckDbThreads=4`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 2.6 | 2.6 | 1.01 | 1.01 1.06 1.00 |
| TPC-H SF10 ADBC (sum of medians) | s | 25.6 | 25.3 | 0.99 | 0.99 1.00 0.99 |
| TPC-H SF1 JDBC (sum of medians) | s | 2.7 | 2.6 | 1.00 | 0.98 1.08 1.00 |
| TPC-H SF10 JDBC (sum of medians) | s | 25.4 | 25.5 | 1.00 | 1.04 0.99 0.97 |
| server RSS peak | MB | 1801.0 | 1768.0 | 0.98 | 0.92 1.00 0.99 |

### i20-fast-lz4-local: A = d22cdaccb4e1 `-`, B = d22cdaccb4e1 `CLZ4`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `adbc10 adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | 25.0 | 24.5 | 0.98 | 1.02 0.98 0.95 |
| lineitem export ADBC | MB/s | 725.5 | 487.4 | 0.67 | 0.63 0.67 0.66 |
| server RSS peak | MB | 1780.0 | 1955.0 | 1.10 | 1.19 0.95 1.12 |

### i20-fast-zstd-local: A = d22cdaccb4e1 `-`, B = d22cdaccb4e1 `CZSTD`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `adbc10 adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | 31.1 | 31.3 | 1.00 | 0.98 1.00 1.00 |
| lineitem export ADBC | MB/s | 602.6 | 283.7 | 0.47 | 0.54 0.46 0.44 |
| server RSS peak | MB | 1958.0 | 1889.0 | 0.96 | 0.96 0.90 1.03 |

### i20-lz4-netem-local: A = ours-new `-`, B = d22cdaccb4e1 `CLZ4`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 1658.0 | 1672.0 | 1.01 | 0.95 1.01 1.08 |

### i20-lz4-vs-native-zstd-netem-local: A = d22cdaccb4e1 `CLZ4`, B = up-native `-DflightCompression=zstd`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 1790.0 | 646.0 | 0.36 | 0.38 0.29 0.36 |

### i20-native-zstd-netem-local: A = d22cdaccb4e1 `CZSTD`, B = up-native `-DflightCompression=zstd`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 1772.0 | 658.0 | 0.37 | 0.37 0.37 0.34 |

### i20-plain-netem-local: A = ours-new `-`, B = d22cdaccb4e1 `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 1703.0 | 1765.0 | 1.04 | 1.08 0.98 1.04 |

### i20-zstd-netem-local: A = ours-new `-`, B = d22cdaccb4e1 `CZSTD`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 1730.0 | 1735.0 | 1.00 | 1.00 1.01 1.04 |

### i20-zstd-vs-lz4-netem-local: A = d22cdaccb4e1 `CZSTD`, B = d22cdaccb4e1 `CLZ4`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 1840.0 | 1856.0 | 1.01 | 1.17 1.01 0.93 |
