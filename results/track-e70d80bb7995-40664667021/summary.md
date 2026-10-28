# Wave track-e70d80bb7995 (server comparison), run 40664667021

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

## Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| core-def-lat-local | ours-new `-` | e70d80bb7995 `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | 0.87 | 0.99 | 0.96 | 0.91 | n/a | n/a | n/a | 1.00 | none |
| core-def-lat-s3 | ours-new `-` | e70d80bb7995 `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | 1.25 | 1.01 | 1.13 | 1.04 | n/a | n/a | n/a | 1.01 | none |
| core-def-sf1-s3 | ours-new `-` | e70d80bb7995 `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | 1.00 | n/a | n/a | n/a | none |
| core-def-sf10adbc-s3 | ours-new `-` | e70d80bb7995 `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | 0.67 | n/a | n/a | none |
| core-def-sf10jdbc-s3 | ours-new `-` | e70d80bb7995 `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | 0.67 | n/a | none |
| core-def-tpch-local | ours-new `-` | e70d80bb7995 `-` | local | Linux ubuntu24 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C | 3/3 | n/a | n/a | n/a | n/a | 0.93 | 0.99 | 0.99 | n/a | none |
| i17-cache-always-vs-reuse-s3 | e70d80bb7995 `-DduckDbThreads=4 -Darrowflight.s3.cacheMegabytes=1024` | e70d80bb7995 `-DduckDbThreads=4 -Darrowflight.s3.cacheMegabytes=1024 -Darrowflight.s3.cacheAdmission=reuse` | s3 | Linux ubuntu24 4 vCPU Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz | 3/3 | 0.99 | 1.02 | 1.00 | 0.98 | 1.04 | 0.92 | n/a | n/a | none |
| i17-cache-off-vs-on-s3 | e70d80bb7995 `-DduckDbThreads=4` | e70d80bb7995 `-DduckDbThreads=4 -Darrowflight.s3.cacheMegabytes=1024` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | 0.43 | 0.07 | 0.68 | 0.07 | 0.35 | 1.34 | n/a | n/a | none |
| i17-cache-on-vs-4e77-s3 | 4e77c6bda59a `-DduckDbThreads=4 -Darrowflight.s3.cacheMegabytes=1024` | e70d80bb7995 `-DduckDbThreads=4 -Darrowflight.s3.cacheMegabytes=1024` | s3 | Linux ubuntu24 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C | 3/3 | 1.04 | 0.99 | 0.97 | 0.92 | 1.01 | 0.99 | n/a | n/a | none |
| i22-prodstreams2-local | e70d80bb7995 `-` | e70d80bb7995 `-DduckDbProducingStreams=2` | local | Linux ubuntu24 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 0.99 | none |
| i22-zerocopy-local | e70d80bb7995 `-` | e70d80bb7995 `-DflightZeroCopyWrites=true` | local | Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.04 | none |
| i22-zerocopy-vs-native-local | e70d80bb7995 `-DflightZeroCopyWrites=true` | up-native `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 0.94 | B: scan8 (rows=355177108 errors=3; rows=387682964 errors=3) |
| tail-vs-4bb6-local | 4bb6441569be `-` | e70d80bb7995 `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | 1.02 | 0.99 | 0.97 | 1.03 | n/a | n/a | n/a | n/a | none |

## Per job (absolute medians and ratios)

### core-def-lat-local: A = ours-new `-`, B = e70d80bb7995 `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `small scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 20.2 | 19.5 | 0.96 | 0.92 0.95 0.96 |
| small JDBC c1 p95 | ms | 41.8 | 38.8 | 0.93 | 0.91 0.93 0.94 |
| small JDBC c1 p99 | ms | 48.8 | 45.9 | 0.94 | 0.92 0.96 0.89 |
| small JDBC c8 p50 | ms | 96.9 | 78.4 | 0.81 | 0.81 0.81 0.81 |
| small JDBC c8 p95 | ms | 245.9 | 229.0 | 0.93 | 0.91 0.93 0.93 |
| small JDBC c8 p99 | ms | 299.4 | 268.5 | 0.90 | 1.02 0.90 0.87 |
| small JDBC c32 p50 | ms | 386.8 | 287.5 | 0.74 | 0.76 0.74 0.77 |
| small JDBC c32 p95 | ms | 1083.6 | 985.2 | 0.91 | 0.91 0.91 0.92 |
| small JDBC c32 p99 | ms | 1360.7 | 1224.0 | 0.90 | 0.75 0.90 0.91 |
| small ADBC c1 p50 | ms | 14.9 | 12.9 | 0.87 | 0.79 0.86 0.91 |
| small ADBC c1 p95 | ms | 38.4 | 34.8 | 0.91 | 0.96 0.78 0.94 |
| small ADBC c1 p99 | ms | 51.5 | 49.4 | 0.96 | 0.86 1.05 1.14 |
| small ADBC c8 p50 | ms | 88.2 | 67.8 | 0.77 | 0.79 0.77 0.76 |
| small ADBC c8 p95 | ms | 249.8 | 234.2 | 0.94 | 0.97 0.92 0.94 |
| small ADBC c8 p99 | ms | 358.0 | 331.3 | 0.93 | 1.06 0.87 0.83 |
| small ADBC c32 p50 | ms | 361.5 | 285.8 | 0.79 | 0.73 0.74 0.82 |
| small ADBC c32 p95 | ms | 1010.1 | 996.4 | 0.99 | 0.96 0.99 0.96 |
| small ADBC c32 p99 | ms | 1322.9 | 1334.6 | 1.01 | 1.01 1.05 0.97 |
| lineitem scan x1 | MB/s | 548.2 | 548.4 | 1.00 | 0.91 1.00 0.99 |
| lineitem scan x4 | MB/s | 556.0 | 602.6 | 1.08 | 1.13 1.05 1.08 |
| lineitem scan x8 | MB/s | 493.7 | 601.1 | 1.22 | 1.22 1.21 1.24 |
| lineitem export ADBC | MB/s | 631.6 | 635.3 | 1.01 | 1.00 1.01 1.01 |
| server RSS peak | MB | 1711.0 | 1604.0 | 0.94 | 0.91 0.94 0.97 |

### core-def-lat-s3: A = ours-new `-`, B = e70d80bb7995 `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `small scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 25.6 | 28.8 | 1.13 | 0.98 1.17 1.11 |
| small JDBC c1 p95 | ms | 694.9 | 686.5 | 0.99 | 0.89 1.04 1.01 |
| small JDBC c1 p99 | ms | 778.2 | 733.7 | 0.94 | 0.91 0.98 0.96 |
| small JDBC c8 p50 | ms | 262.7 | 249.5 | 0.95 | 0.99 0.90 1.56 |
| small JDBC c8 p95 | ms | 3722.3 | 3934.6 | 1.06 | 1.02 1.07 1.57 |
| small JDBC c8 p99 | ms | 4018.1 | 4234.8 | 1.05 | 1.05 1.03 1.61 |
| small JDBC c32 p50 | ms | 959.7 | 930.6 | 0.97 | 0.95 0.96 1.49 |
| small JDBC c32 p95 | ms | 13400.3 | 13872.5 | 1.04 | 1.05 1.04 1.56 |
| small JDBC c32 p99 | ms | 17550.1 | 26100.4 | 1.49 | 1.06 1.49 1.32 |
| small ADBC c1 p50 | ms | 18.1 | 22.7 | 1.25 | 1.31 1.18 1.36 |
| small ADBC c1 p95 | ms | 690.0 | 696.8 | 1.01 | 0.97 0.98 1.35 |
| small ADBC c1 p99 | ms | 750.8 | 758.5 | 1.01 | 0.97 1.01 1.30 |
| small ADBC c8 p50 | ms | 246.1 | 255.0 | 1.04 | 1.07 0.98 1.67 |
| small ADBC c8 p95 | ms | 3774.9 | 3797.9 | 1.01 | 0.93 1.04 1.53 |
| small ADBC c8 p99 | ms | 4148.3 | 4031.6 | 0.97 | 0.93 1.01 1.90 |
| small ADBC c32 p50 | ms | 904.4 | 972.6 | 1.08 | 1.08 1.08 1.00 |
| small ADBC c32 p95 | ms | 13048.1 | 13242.4 | 1.01 | 1.05 1.01 0.98 |
| small ADBC c32 p99 | ms | 15586.6 | 14927.3 | 0.96 | 0.91 1.02 0.94 |
| lineitem scan x1 | MB/s | 560.2 | 565.6 | 1.01 | 0.95 1.01 1.02 |
| lineitem scan x4 | MB/s | 706.5 | 688.7 | 0.97 | 0.95 1.07 0.97 |
| lineitem scan x8 | MB/s | 686.0 | 654.9 | 0.95 | 0.93 1.03 0.95 |
| lineitem export ADBC | MB/s | 610.6 | 595.6 | 0.98 | 1.02 1.02 0.98 |
| server RSS peak | MB | 2890.0 | 2896.0 | 1.00 | 1.02 1.01 0.94 |

### core-def-sf1-s3: A = ours-new `-`, B = e70d80bb7995 `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 26.6 | 26.6 | 1.00 | 1.00 0.99 1.01 |
| TPC-H SF1 JDBC (sum of medians) | s | 26.5 | 26.8 | 1.01 | 1.01 0.97 1.03 |
| server RSS peak | MB | 757.0 | 769.0 | 1.02 | 0.97 1.00 1.02 |

### core-def-sf10adbc-s3: A = ours-new `-`, B = e70d80bb7995 `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 ADBC (sum of medians) | s | 459.4 | 305.8 | 0.67 | 1.03 0.65 0.97 |
| server RSS peak | MB | 1706.0 | 1801.0 | 1.06 | 1.05 1.01 1.07 |

### core-def-sf10jdbc-s3: A = ours-new `-`, B = e70d80bb7995 `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `sf10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF10 JDBC (sum of medians) | s | 497.5 | 334.0 | 0.67 | 1.00 0.66 1.02 |
| server RSS peak | MB | 1730.0 | 1702.0 | 0.98 | 1.07 0.98 0.93 |

### core-def-tpch-local: A = ours-new `-`, B = e70d80bb7995 `-`, local

Runner: Linux ubuntu24 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 4.0 | 3.7 | 0.93 | 0.93 0.92 0.93 |
| TPC-H SF10 ADBC (sum of medians) | s | 37.5 | 37.0 | 0.99 | 0.99 0.98 0.99 |
| TPC-H SF1 JDBC (sum of medians) | s | 4.1 | 3.8 | 0.93 | 0.95 0.92 0.91 |
| TPC-H SF10 JDBC (sum of medians) | s | 37.6 | 37.1 | 0.99 | 1.00 0.99 0.98 |
| server RSS peak | MB | 1702.0 | 1823.0 | 1.07 | 1.02 1.04 1.11 |

### i17-cache-always-vs-reuse-s3: A = e70d80bb7995 `-DduckDbThreads=4 -Darrowflight.s3.cacheMegabytes=1024`, B = e70d80bb7995 `-DduckDbThreads=4 -Darrowflight.s3.cacheMegabytes=1024 -Darrowflight.s3.cacheAdmission=reuse`, s3

Runner: Linux ubuntu24 4 vCPU Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz. Workloads: `adbc10 adbc1 small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 25.8 | 25.9 | 1.00 | 0.90 1.05 0.98 |
| small JDBC c1 p95 | ms | 115.0 | 115.5 | 1.00 | 0.01 0.99 1.00 |
| small JDBC c1 p99 | ms | 126.6 | 191.2 | 1.51 | 0.01 1.74 0.97 |
| small JDBC c8 p50 | ms | 139.4 | 136.9 | 0.98 | 1.26 0.87 1.05 |
| small JDBC c8 p95 | ms | 476.2 | 481.0 | 1.01 | 0.95 1.08 0.96 |
| small JDBC c8 p99 | ms | 541.4 | 540.0 | 1.00 | 0.27 1.11 0.98 |
| small JDBC c32 p50 | ms | 580.3 | 586.1 | 1.01 | 1.13 0.98 1.03 |
| small JDBC c32 p95 | ms | 1906.6 | 1863.8 | 0.98 | 0.93 1.03 0.99 |
| small JDBC c32 p99 | ms | 2277.6 | 2128.8 | 0.93 | 0.46 1.00 0.97 |
| small ADBC c1 p50 | ms | 17.3 | 17.1 | 0.99 | 0.91 1.16 0.98 |
| small ADBC c1 p95 | ms | 109.9 | 99.2 | 0.90 | 0.01 1.04 0.90 |
| small ADBC c1 p99 | ms | 123.6 | 110.3 | 0.89 | 0.01 1.09 0.89 |
| small ADBC c8 p50 | ms | 117.6 | 125.3 | 1.07 | 1.22 0.88 1.07 |
| small ADBC c8 p95 | ms | 487.6 | 487.5 | 1.00 | 1.00 1.16 0.89 |
| small ADBC c8 p99 | ms | 549.2 | 543.8 | 0.99 | 0.32 1.18 0.91 |
| small ADBC c32 p50 | ms | 529.0 | 538.6 | 1.02 | 0.93 1.08 1.05 |
| small ADBC c32 p95 | ms | 1913.8 | 1947.1 | 1.02 | 0.96 1.02 1.04 |
| small ADBC c32 p99 | ms | 2223.7 | 2213.1 | 1.00 | 0.96 1.02 1.02 |
| TPC-H SF1 ADBC (sum of medians) | s | 13.8 | 14.3 | 1.04 | 1.02 1.07 1.03 |
| TPC-H SF10 ADBC (sum of medians) | s | 446.7 | 412.3 | 0.92 | 0.92 1.02 1.03 |
| server RSS peak | MB | 5179.0 | 5569.0 | 1.08 | 1.12 1.07 1.10 |

### i17-cache-off-vs-on-s3: A = e70d80bb7995 `-DduckDbThreads=4`, B = e70d80bb7995 `-DduckDbThreads=4 -Darrowflight.s3.cacheMegabytes=1024`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `adbc10 adbc1 small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 36.6 | 24.9 | 0.68 | 0.75 0.68 0.63 |
| small JDBC c1 p95 | ms | 1143.1 | 106.1 | 0.09 | 0.14 0.09 0.09 |
| small JDBC c1 p99 | ms | 1255.0 | 120.1 | 0.10 | 0.13 0.10 0.08 |
| small JDBC c8 p50 | ms | 464.3 | 126.6 | 0.27 | 0.34 0.27 0.27 |
| small JDBC c8 p95 | ms | 7441.3 | 412.5 | 0.06 | 0.08 0.05 0.06 |
| small JDBC c8 p99 | ms | 7778.1 | 479.4 | 0.06 | 0.08 0.06 0.06 |
| small JDBC c32 p50 | ms | 1676.1 | 498.1 | 0.30 | 0.46 0.31 0.30 |
| small JDBC c32 p95 | ms | 23693.1 | 1655.2 | 0.07 | 0.10 0.07 0.08 |
| small JDBC c32 p99 | ms | 26428.4 | 2152.0 | 0.08 | 0.15 0.07 0.08 |
| small ADBC c1 p50 | ms | 35.2 | 15.3 | 0.43 | 0.60 0.42 0.40 |
| small ADBC c1 p95 | ms | 1141.1 | 102.6 | 0.09 | 0.13 0.09 0.09 |
| small ADBC c1 p99 | ms | 1279.3 | 109.4 | 0.09 | 0.14 0.08 0.29 |
| small ADBC c8 p50 | ms | 415.3 | 102.5 | 0.25 | 0.31 0.21 0.28 |
| small ADBC c8 p95 | ms | 7688.6 | 431.4 | 0.06 | 0.08 0.06 0.05 |
| small ADBC c8 p99 | ms | 8471.6 | 475.3 | 0.06 | 0.08 0.06 0.03 |
| small ADBC c32 p50 | ms | 1561.8 | 462.1 | 0.30 | 0.41 0.28 0.30 |
| small ADBC c32 p95 | ms | 24903.6 | 1687.4 | 0.07 | 0.11 0.07 0.07 |
| small ADBC c32 p99 | ms | 35882.7 | 1989.3 | 0.06 | 0.11 0.06 0.05 |
| TPC-H SF1 ADBC (sum of medians) | s | 37.9 | 13.3 | 0.35 | 0.51 0.35 0.35 |
| TPC-H SF10 ADBC (sum of medians) | s | 404.1 | 541.2 | 1.34 | 1.45 1.34 1.30 |
| server RSS peak | MB | 2289.0 | 5149.0 | 2.25 | 2.16 2.34 2.25 |

### i17-cache-on-vs-4e77-s3: A = 4e77c6bda59a `-DduckDbThreads=4 -Darrowflight.s3.cacheMegabytes=1024`, B = e70d80bb7995 `-DduckDbThreads=4 -Darrowflight.s3.cacheMegabytes=1024`, s3

Runner: Linux ubuntu24 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C. Workloads: `adbc10 adbc1 small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 26.6 | 25.7 | 0.97 | 0.96 0.99 0.95 |
| small JDBC c1 p95 | ms | 104.5 | 100.7 | 0.96 | 0.98 0.96 0.94 |
| small JDBC c1 p99 | ms | 114.7 | 113.0 | 0.98 | 1.01 0.98 0.93 |
| small JDBC c8 p50 | ms | 122.0 | 113.9 | 0.93 | 1.48 0.93 0.86 |
| small JDBC c8 p95 | ms | 434.9 | 455.4 | 1.05 | 1.20 1.00 1.05 |
| small JDBC c8 p99 | ms | 513.9 | 497.7 | 0.97 | 0.23 0.97 1.05 |
| small JDBC c32 p50 | ms | 591.2 | 517.7 | 0.88 | 0.97 0.85 0.85 |
| small JDBC c32 p95 | ms | 1973.8 | 1816.7 | 0.92 | 0.89 0.90 0.93 |
| small JDBC c32 p99 | ms | 2374.5 | 2086.0 | 0.88 | 0.90 0.88 0.86 |
| small ADBC c1 p50 | ms | 14.6 | 15.2 | 1.04 | 1.02 1.02 1.08 |
| small ADBC c1 p95 | ms | 96.3 | 96.4 | 1.00 | 1.11 0.99 1.02 |
| small ADBC c1 p99 | ms | 110.9 | 182.5 | 1.65 | 10.34 0.84 1.65 |
| small ADBC c8 p50 | ms | 105.6 | 101.3 | 0.96 | 1.18 0.92 0.92 |
| small ADBC c8 p95 | ms | 414.6 | 420.8 | 1.01 | 0.92 1.09 1.01 |
| small ADBC c8 p99 | ms | 468.9 | 477.3 | 1.02 | 0.95 1.11 1.02 |
| small ADBC c32 p50 | ms | 472.4 | 472.9 | 1.00 | 0.99 0.98 1.04 |
| small ADBC c32 p95 | ms | 1858.2 | 1845.9 | 0.99 | 1.02 0.94 1.00 |
| small ADBC c32 p99 | ms | 2085.8 | 2081.3 | 1.00 | 1.14 0.97 1.00 |
| TPC-H SF1 ADBC (sum of medians) | s | 13.0 | 13.1 | 1.01 | 1.01 1.05 0.94 |
| TPC-H SF10 ADBC (sum of medians) | s | 512.7 | 509.3 | 0.99 | 0.92 1.00 0.97 |
| server RSS peak | MB | 5702.0 | 5263.0 | 0.92 | 0.91 0.92 0.93 |

### i22-prodstreams2-local: A = e70d80bb7995 `-`, B = e70d80bb7995 `-DduckDbProducingStreams=2`, local

Runner: Linux ubuntu24 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 442.3 | 437.8 | 0.99 | 1.01 1.00 0.99 |
| lineitem scan x4 | MB/s | 498.5 | 504.0 | 1.01 | 1.05 1.00 1.03 |
| lineitem scan x8 | MB/s | 498.7 | 517.0 | 1.04 | 1.03 1.04 1.03 |
| lineitem export ADBC | MB/s | 497.7 | 510.7 | 1.03 | 0.92 1.04 0.99 |
| server RSS peak | MB | 922.0 | 854.0 | 0.93 | 0.94 0.90 0.93 |

### i22-zerocopy-local: A = e70d80bb7995 `-`, B = e70d80bb7995 `-DflightZeroCopyWrites=true`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 567.0 | 591.4 | 1.04 | 1.07 1.03 1.04 |
| lineitem scan x4 | MB/s | 649.2 | 693.8 | 1.07 | 1.08 1.06 1.06 |
| lineitem scan x8 | MB/s | 662.5 | 699.1 | 1.06 | 1.06 1.05 1.07 |
| lineitem export ADBC | MB/s | 664.2 | 688.8 | 1.04 | 1.04 1.04 1.03 |
| server RSS peak | MB | 1415.0 | 1393.0 | 0.98 | 1.00 0.90 0.98 |

### i22-zerocopy-vs-native-local: A = e70d80bb7995 `-DflightZeroCopyWrites=true`, B = up-native `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 710.5 | 666.5 | 0.94 | 0.92 0.92 0.94 |
| lineitem scan x4 | MB/s | 865.7 | 866.8 | 1.00 | 1.01 0.99 1.02 |
| lineitem scan x8 | MB/s | 853.5 | n/a | n/a | - |
| lineitem export ADBC | MB/s | 840.0 | 820.5 | 0.98 | 0.98 0.98 0.95 |
| server RSS peak | MB | 1299.0 | 3732.0 | 2.87 | 2.91 2.88 2.51 |

Correctness gate: B: scan8 (rows=355177108 errors=3; rows=387682964 errors=3).

### tail-vs-4bb6-local: A = 4bb6441569be `-`, B = e70d80bb7995 `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 25.2 | 24.3 | 0.97 | 0.96 0.97 1.03 |
| small JDBC c1 p95 | ms | 50.4 | 50.4 | 1.00 | 1.03 0.93 1.00 |
| small JDBC c1 p99 | ms | 62.3 | 62.0 | 0.99 | 0.99 0.93 1.21 |
| small JDBC c8 p50 | ms | 97.2 | 95.0 | 0.98 | 0.98 0.99 0.94 |
| small JDBC c8 p95 | ms | 288.1 | 284.1 | 0.99 | 1.04 0.99 0.96 |
| small JDBC c8 p99 | ms | 334.0 | 328.1 | 0.98 | 1.07 0.98 0.92 |
| small JDBC c32 p50 | ms | 359.0 | 376.5 | 1.05 | 1.07 1.03 1.03 |
| small JDBC c32 p95 | ms | 1199.6 | 1230.5 | 1.03 | 1.06 1.00 1.02 |
| small JDBC c32 p99 | ms | 1717.7 | 1734.5 | 1.01 | 1.18 0.91 1.01 |
| small ADBC c1 p50 | ms | 15.9 | 16.2 | 1.02 | 0.97 1.02 1.04 |
| small ADBC c1 p95 | ms | 45.4 | 44.4 | 0.98 | 1.03 0.98 0.92 |
| small ADBC c1 p99 | ms | 58.2 | 55.4 | 0.95 | 1.09 0.83 0.98 |
| small ADBC c8 p50 | ms | 81.2 | 82.7 | 1.02 | 1.03 0.99 1.01 |
| small ADBC c8 p95 | ms | 278.0 | 282.9 | 1.02 | 0.95 1.04 1.04 |
| small ADBC c8 p99 | ms | 324.6 | 312.1 | 0.96 | 0.91 1.10 0.99 |
| small ADBC c32 p50 | ms | 332.3 | 327.7 | 0.99 | 1.00 0.99 0.99 |
| small ADBC c32 p95 | ms | 1160.4 | 1148.6 | 0.99 | 1.02 0.98 0.97 |
| small ADBC c32 p99 | ms | 1369.7 | 1323.2 | 0.97 | 1.04 0.95 0.90 |
| server RSS peak | MB | 1439.0 | 1430.0 | 0.99 | 1.00 0.99 1.00 |
