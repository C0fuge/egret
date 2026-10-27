# Wave c4-robust (server comparison), run 40551848571

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

## Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| new-vs-27f5-start-cancel-local | ours-new `-` | ours-27f5 `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| new-vs-main-start-cancel-local | ours-new `-` | up-main `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| new-vs-native-start-cancel-local | ours-new `-` | up-native `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |

## Per job (absolute medians and ratios)

### new-vs-27f5-start-cancel-local: A = ours-new `-`, B = ours-27f5 `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `coldstart cancel`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 1360.0 | 1331.0 | 0.98 | 0.98 1.03 0.96 |

### new-vs-main-start-cancel-local: A = ours-new `-`, B = up-main `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `coldstart cancel`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 1398.0 | 4909.0 | 3.51 | 3.42 3.58 3.54 |

### new-vs-native-start-cancel-local: A = ours-new `-`, B = up-native `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `coldstart cancel`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 1404.0 | 4481.0 | 3.19 | 3.17 3.12 3.23 |
