# Wave track-2cfa23eb62f9-cluster (server comparison), run 40736487295

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

## Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| i18-dc-off-vs-on-s3 | 2cfa23eb62f9 `-DdistributedComplete=false` | 2cfa23eb62f9 `-DdistributedComplete=true` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor | 2/2 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |

## Per job (absolute medians and ratios)

### i18-dc-off-vs-on-s3: A = 2cfa23eb62f9 `-DdistributedComplete=false`, B = 2cfa23eb62f9 `-DdistributedComplete=true`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `cluster`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
| server RSS peak | MB | 311.0 | 316.5 | 1.02 | 1.01 1.02 |
