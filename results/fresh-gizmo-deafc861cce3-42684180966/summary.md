# Wave fresh-gizmo-deafc861cce3 (server comparison), run 42684180966

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

## Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| fu-scan-local | deafc861cce3 `-` | deafc861cce3 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.02 | none |
| fu-scan-local-vs-gizmo | gizmo `-` | deafc861cce3 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.01 | none |
| fu-scan-s3 | deafc861cce3 `-` | deafc861cce3 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.42 | none |
| fu-scan-s3-vs-gizmo | gizmo `-` | deafc861cce3 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 1.15 | none |

## Per job (absolute medians and ratios)

### fu-scan-local: A = deafc861cce3 `-`, B = deafc861cce3 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 456.6 | 465.4 | 1.02 | 1.02 1.04 0.98 |
| lineitem scan x4 | MB/s | 489.9 | 615.7 | 1.26 | 1.23 1.30 1.25 |
| lineitem scan x8 | MB/s | 423.7 | 624.5 | 1.47 | 1.50 1.47 1.48 |
| lineitem export ADBC | MB/s | 544.8 | 561.4 | 1.03 | 1.02 1.03 1.03 |
| server RSS peak | MB | 1127.0 | 1142.0 | 1.01 | 1.02 1.00 1.04 |

### fu-scan-local-vs-gizmo: A = gizmo `-`, B = deafc861cce3 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 460.1 | 465.4 | 1.01 | 1.01 1.02 1.01 |
| lineitem scan x4 | MB/s | 622.2 | 615.7 | 0.99 | 0.99 1.00 0.98 |
| lineitem scan x8 | MB/s | 632.1 | 624.5 | 0.99 | 0.99 1.00 0.99 |
| lineitem export ADBC | MB/s | 504.7 | 561.4 | 1.11 | 1.11 1.11 1.12 |
| server RSS peak | MB | 474.0 | 1142.0 | 2.41 | 2.36 2.39 2.50 |

### fu-scan-s3: A = deafc861cce3 `-`, B = deafc861cce3 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 318.7 | 451.3 | 1.42 | 1.13 1.45 1.51 |
| lineitem scan x4 | MB/s | 453.5 | 736.4 | 1.62 | 1.56 1.64 1.85 |
| lineitem scan x8 | MB/s | 463.2 | 736.1 | 1.59 | 1.50 1.59 1.64 |
| lineitem export ADBC | MB/s | 377.6 | 569.9 | 1.51 | 2.27 1.43 1.36 |
| server RSS peak | MB | 1675.0 | 3013.0 | 1.80 | 1.79 1.84 1.75 |

### fu-scan-s3-vs-gizmo: A = gizmo `-`, B = deafc861cce3 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| lineitem scan x1 | MB/s | 391.7 | 451.3 | 1.15 | 1.31 1.13 1.12 |
| lineitem scan x4 | MB/s | 791.7 | 736.4 | 0.93 | 1.05 0.93 0.93 |
| lineitem scan x8 | MB/s | 801.9 | 736.1 | 0.92 | 0.88 0.92 1.06 |
| lineitem export ADBC | MB/s | 614.9 | 569.9 | 0.93 | 1.06 1.17 0.92 |
| server RSS peak | MB | 2546.0 | 3013.0 | 1.18 | 1.16 1.21 1.15 |
