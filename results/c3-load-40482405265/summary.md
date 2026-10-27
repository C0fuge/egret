# Wave c3-load (server comparison), run 40482405265

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

## Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| new-vs-27f5-def-load-local | ours-new `-` | ours-27f5 `-` | local | Linux ubuntu24 4 vCPU Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz | 0/0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| new-vs-27f5-def-mix-local | ours-new `-` | ours-27f5 `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 0/0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| new-vs-27f5-t8-load-local | ours-new `-DduckDbThreads=8` | ours-27f5 `-DduckDbThreads=8` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 0/0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| new-vs-27f5-t8-mix-local | ours-new `-DduckDbThreads=8` | ours-27f5 `-DduckDbThreads=8` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 0/0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| new-vs-main-def-load-local | ours-new `-` | up-main `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 0/0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| new-vs-main-def-mix-local | ours-new `-` | up-main `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 0/0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| new-vs-main-t8-load-local | ours-new `-DduckDbThreads=8` | up-main `-DduckDbThreads=8` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 0/0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| new-vs-main-t8-mix-local | ours-new `-DduckDbThreads=8` | up-main `-DduckDbThreads=8` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 0/0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| new-vs-native-def-load-local | ours-new `-` | up-native `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 0/0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| new-vs-native-def-mix-local | ours-new `-` | up-native `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 0/0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| new-vs-native-t8-load-local | ours-new `-DduckDbThreads=8` | up-native `-DduckDbThreads=8` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 0/0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| new-vs-native-t8-mix-local | ours-new `-DduckDbThreads=8` | up-native `-DduckDbThreads=8` | local | Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor | 0/0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |

## Per job (absolute medians and ratios)

### new-vs-27f5-def-load-local: A = ours-new `-`, B = ours-27f5 `-`, local

Runner: Linux ubuntu24 4 vCPU Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|

### new-vs-27f5-def-mix-local: A = ours-new `-`, B = ours-27f5 `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `mixed heavy4a netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|

### new-vs-27f5-t8-load-local: A = ours-new `-DduckDbThreads=8`, B = ours-27f5 `-DduckDbThreads=8`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|

### new-vs-27f5-t8-mix-local: A = ours-new `-DduckDbThreads=8`, B = ours-27f5 `-DduckDbThreads=8`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `mixed heavy4a netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|

### new-vs-main-def-load-local: A = ours-new `-`, B = up-main `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|

### new-vs-main-def-mix-local: A = ours-new `-`, B = up-main `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `mixed heavy4a netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|

### new-vs-main-t8-load-local: A = ours-new `-DduckDbThreads=8`, B = up-main `-DduckDbThreads=8`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|

### new-vs-main-t8-mix-local: A = ours-new `-DduckDbThreads=8`, B = up-main `-DduckDbThreads=8`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `mixed heavy4a netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|

### new-vs-native-def-load-local: A = ours-new `-`, B = up-native `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|

### new-vs-native-def-mix-local: A = ours-new `-`, B = up-native `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `mixed heavy4a netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|

### new-vs-native-t8-load-local: A = ours-new `-DduckDbThreads=8`, B = up-native `-DduckDbThreads=8`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `load`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|

### new-vs-native-t8-mix-local: A = ours-new `-DduckDbThreads=8`, B = up-native `-DduckDbThreads=8`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `mixed heavy4a netem`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
