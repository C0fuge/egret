# Wave c7-load-tls (server comparison), run 40550942695

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

## Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| new-plain-vs-tls-lat-local | ours-new `-` | ours-new `TLS` | local | Linux ubuntu24 4 vCPU Intel(R) Xeon(R) 6973P-C | 3/3 | 0.95 | 0.98 | 1.10 | 0.96 | n/a | 0.99 | n/a | n/a | none |
| new-plain-vs-tls-load-local | ours-new `-` | ours-new `TLS` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |

## Per job (absolute medians and ratios)

### new-plain-vs-tls-lat-local: A = ours-new `-`, B = ours-new `TLS`, local

Runner: Linux ubuntu24 4 vCPU Intel(R) Xeon(R) 6973P-C. Workloads: `small adbcscan adbc10`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| small JDBC c1 p50 | ms | 17.2 | 19.0 | 1.10 | 1.12 1.02 1.10 |
| small JDBC c1 p95 | ms | 34.0 | 35.4 | 1.04 | 1.07 0.94 1.04 |
| small JDBC c1 p99 | ms | 41.7 | 41.7 | 1.00 | 0.99 0.90 1.14 |
| small JDBC c8 p50 | ms | 80.5 | 84.7 | 1.05 | 1.02 1.06 1.14 |
| small JDBC c8 p95 | ms | 204.7 | 188.6 | 0.92 | 0.98 0.97 0.90 |
| small JDBC c8 p99 | ms | 250.0 | 238.1 | 0.95 | 1.04 0.95 0.89 |
| small JDBC c32 p50 | ms | 310.7 | 330.0 | 1.06 | 1.07 1.01 1.04 |
| small JDBC c32 p95 | ms | 856.3 | 823.0 | 0.96 | 0.98 0.91 0.98 |
| small JDBC c32 p99 | ms | 1140.6 | 1117.1 | 0.98 | 1.08 0.88 0.98 |
| small ADBC c1 p50 | ms | 12.3 | 11.6 | 0.95 | 0.99 0.95 0.98 |
| small ADBC c1 p95 | ms | 31.3 | 30.6 | 0.98 | 1.02 1.05 0.86 |
| small ADBC c1 p99 | ms | 38.0 | 43.7 | 1.15 | 0.96 1.24 1.09 |
| small ADBC c8 p50 | ms | 76.6 | 73.1 | 0.95 | 1.07 0.95 0.93 |
| small ADBC c8 p95 | ms | 182.4 | 178.1 | 0.98 | 0.98 1.05 0.82 |
| small ADBC c8 p99 | ms | 237.8 | 221.4 | 0.93 | 1.04 0.90 0.83 |
| small ADBC c32 p50 | ms | 306.1 | 299.7 | 0.98 | 1.00 0.95 1.00 |
| small ADBC c32 p95 | ms | 881.3 | 859.9 | 0.98 | 0.99 0.93 0.91 |
| small ADBC c32 p99 | ms | 1221.1 | 1189.9 | 0.97 | 1.03 0.99 0.83 |
| TPC-H SF10 ADBC (sum of medians) | s | 30.3 | 29.9 | 0.99 | 1.00 0.98 0.99 |
| lineitem export ADBC | MB/s | 592.0 | 576.1 | 0.97 | 0.92 0.97 0.99 |
| server RSS peak | MB | 2661.0 | 2694.0 | 1.01 | 1.02 0.97 1.00 |

### new-plain-vs-tls-load-local: A = ours-new `-`, B = ours-new `TLS`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 4666.0 | 4699.0 | 1.01 | 0.98 1.04 0.98 |
