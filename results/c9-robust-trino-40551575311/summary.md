# Wave c9-robust-trino (server comparison), run 40551575311

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

## Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| new-vs-27f5-trino-local | ours-new `-` | ours-27f5 `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor | 1/1 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| new-vs-main-trino-local | ours-new `-` | up-main `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 1/1 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| new-vs-native-trino-local | ours-new `-` | up-native `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 1/1 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |

## Per job (absolute medians and ratios)

### new-vs-27f5-trino-local: A = ours-new `-`, B = ours-27f5 `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `trino`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 954.0 | 806.0 | 0.84 | 0.84 |

### new-vs-main-trino-local: A = ours-new `-`, B = up-main `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `trino`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 970.0 | 1359.0 | 1.40 | 1.40 |

### new-vs-native-trino-local: A = ours-new `-`, B = up-native `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `trino`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 825.0 | 1123.0 | 1.36 | 1.36 |
