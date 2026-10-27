# Wave c7-load-tls (server comparison), run 40553901245

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

## Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| new-plain-vs-tls-lat-local | ours-new `-` | ours-new `TLS` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | 0.96 | 1.01 | 1.08 | 1.09 | n/a | 1.01 | n/a | n/a | none |

## Per job (absolute medians and ratios)

### new-plain-vs-tls-lat-local: A = ours-new `-`, B = ours-new `TLS`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small adbcscan adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 25.5 | 27.5 | 1.08 | 1.09 1.10 0.95 |
| small JDBC c1 p95 | ms | 53.3 | 54.3 | 1.02 | 1.02 1.08 0.97 |
| small JDBC c1 p99 | ms | 58.9 | 61.6 | 1.05 | 1.05 1.05 0.96 |
| small JDBC c8 p50 | ms | 124.2 | 122.7 | 0.99 | 0.93 1.00 1.01 |
| small JDBC c8 p95 | ms | 277.6 | 298.6 | 1.08 | 0.98 1.12 1.01 |
| small JDBC c8 p99 | ms | 340.6 | 406.7 | 1.19 | 0.93 1.20 1.23 |
| small JDBC c32 p50 | ms | 469.5 | 448.1 | 0.95 | 1.01 0.92 1.01 |
| small JDBC c32 p95 | ms | 1274.1 | 1385.5 | 1.09 | 0.98 1.11 1.04 |
| small JDBC c32 p99 | ms | 1788.4 | 1853.5 | 1.04 | 1.08 1.04 1.00 |
| small ADBC c1 p50 | ms | 17.7 | 17.0 | 0.96 | 1.03 0.95 0.91 |
| small ADBC c1 p95 | ms | 46.3 | 44.3 | 0.96 | 0.88 0.96 1.02 |
| small ADBC c1 p99 | ms | 61.4 | 54.4 | 0.89 | 0.85 0.87 0.95 |
| small ADBC c8 p50 | ms | 114.4 | 110.8 | 0.97 | 0.96 0.89 1.02 |
| small ADBC c8 p95 | ms | 268.0 | 280.2 | 1.05 | 0.96 1.05 1.08 |
| small ADBC c8 p99 | ms | 344.6 | 324.6 | 0.94 | 0.98 0.92 1.00 |
| small ADBC c32 p50 | ms | 436.5 | 435.0 | 1.00 | 0.99 1.01 0.98 |
| small ADBC c32 p95 | ms | 1244.7 | 1262.3 | 1.01 | 0.90 1.01 1.02 |
| small ADBC c32 p99 | ms | 1787.1 | 1700.0 | 0.95 | 0.85 0.95 1.05 |
| TPC-H SF10 ADBC (sum of medians) | s | 39.4 | 39.8 | 1.01 | 1.01 0.99 1.04 |
| lineitem export ADBC | MB/s | 481.2 | 426.5 | 0.89 | 0.92 0.92 0.86 |
| server RSS peak | MB | 2587.0 | 2699.0 | 1.04 | 0.99 1.00 1.05 |
