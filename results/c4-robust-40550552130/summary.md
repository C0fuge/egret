# Wave c4-robust (server comparison), run 40550552130

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

## Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| new-vs-27f5-soak-local | ours-new `-` | ours-27f5 `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 1/1 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| new-vs-27f5-start-cancel-local | ours-new `-` | ours-27f5 `-` | local | Linux ubuntu24 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C | 1/1 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| new-vs-main-soak-local | ours-new `-` | up-main `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor | 1/1 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| new-vs-main-start-cancel-local | ours-new `-` | up-main `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 1/1 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| new-vs-native-soak-local | ours-new `-` | up-native `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor | 1/1 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| new-vs-native-start-cancel-local | ours-new `-` | up-native `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor | 1/1 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |

## Per job (absolute medians and ratios)

### new-vs-27f5-soak-local: A = ours-new `-`, B = ours-27f5 `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `soak`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 2837.0 | 2725.0 | 0.96 | 0.96 |

### new-vs-27f5-start-cancel-local: A = ours-new `-`, B = ours-27f5 `-`, local

Runner: Linux ubuntu24 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C. Workloads: `coldstart cancel`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 1162.0 | 1156.0 | 0.99 | 0.99 |

### new-vs-main-soak-local: A = ours-new `-`, B = up-main `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `soak`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 3024.0 | 4649.0 | 1.54 | 1.54 |

### new-vs-main-start-cancel-local: A = ours-new `-`, B = up-main `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `coldstart cancel`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 1212.0 | 350.0 | 0.29 | 0.29 |

### new-vs-native-soak-local: A = ours-new `-`, B = up-native `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `soak`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 2942.0 | 2938.0 | 1.00 | 1.00 |

### new-vs-native-start-cancel-local: A = ours-new `-`, B = up-native `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `coldstart cancel`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 1251.0 | 342.0 | 0.27 | 0.27 |
