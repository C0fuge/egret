# Wave fresh-gizmo-deafc861cce3 (server comparison), run 42629228261

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

## Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| fu-sf1-s3 | deafc861cce3 `-` | deafc861cce3 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 1/1 | n/a | n/a | n/a | n/a | 0.14 | n/a | n/a | n/a | none |
| fu-sf1-s3-vs-gizmo | gizmo `-` | deafc861cce3 `-DresourceProfile=speed` | s3 | Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor | 1/1 | n/a | n/a | n/a | n/a | 1.08 | n/a | n/a | n/a | none |
| fu-tpch-local | deafc861cce3 `-` | deafc861cce3 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz | 1/1 | n/a | n/a | n/a | n/a | 1.02 | 0.95 | 0.96 | n/a | none |
| fu-tpch-local-vs-gizmo | gizmo `-` | deafc861cce3 `-DresourceProfile=speed` | local | Linux ubuntu26 4 vCPU Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz | 1/1 | n/a | n/a | n/a | n/a | 1.10 | 1.00 | 0.99 | n/a | none |

## Per job (absolute medians and ratios)

### fu-sf1-s3: A = deafc861cce3 `-`, B = deafc861cce3 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 23.8 | 3.2 | 0.14 | 0.14 |
| TPC-H SF1 JDBC (sum of medians) | s | 25.6 | 3.3 | 0.13 | 0.13 |
| server RSS peak | MB | 717.0 | 1013.0 | 1.41 | 1.41 |

### fu-sf1-s3-vs-gizmo: A = gizmo `-`, B = deafc861cce3 `-DresourceProfile=speed`, s3

Runner: Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 3.0 | 3.2 | 1.08 | 1.08 |
| TPC-H SF1 JDBC (sum of medians) | s | 3.1 | 3.3 | 1.06 | 1.06 |
| server RSS peak | MB | 597.0 | 1013.0 | 1.70 | 1.70 |

### fu-tpch-local: A = deafc861cce3 `-`, B = deafc861cce3 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 4.3 | 4.4 | 1.02 | 1.02 |
| TPC-H SF10 ADBC (sum of medians) | s | 45.9 | 43.8 | 0.95 | 0.95 |
| TPC-H SF1 JDBC (sum of medians) | s | 4.5 | 4.4 | 0.98 | 0.98 |
| TPC-H SF10 JDBC (sum of medians) | s | 45.5 | 43.7 | 0.96 | 0.96 |
| server RSS peak | MB | 1560.0 | 1885.0 | 1.21 | 1.21 |

### fu-tpch-local-vs-gizmo: A = gizmo `-`, B = deafc861cce3 `-DresourceProfile=speed`, local

Runner: Linux ubuntu26 4 vCPU Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| TPC-H SF1 ADBC (sum of medians) | s | 4.0 | 4.4 | 1.10 | 1.10 |
| TPC-H SF10 ADBC (sum of medians) | s | 43.8 | 43.8 | 1.00 | 1.00 |
| TPC-H SF1 JDBC (sum of medians) | s | 4.2 | 4.4 | 1.06 | 1.06 |
| TPC-H SF10 JDBC (sum of medians) | s | 44.1 | 43.7 | 0.99 | 0.99 |
| server RSS peak | MB | 1580.0 | 1885.0 | 1.19 | 1.19 |
