# Wave c2-speed (server comparison), run 40481883941

Each job: server A and server B on the same GitHub runner, alternating rounds (A B, B A, A B); same TPC-H Parquet
data dir and same schema-qualified queries for both. Ratio = B / A of the medians over rounds: times < 1 = B faster;
scan MB/s > 1 = B faster. **n/a** = not measured, or the server failed that workload's correctness gate
(wrong or failed answers, errors): such a value is never ranked. TPC-H answers are checked per query against
in-process DuckDB on the same files.

## Overview (ratios B / A)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| new-vs-27f5-def-lat-local | ours-new `-` | ours-27f5 `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 0/0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| new-vs-27f5-def-lat-s3 | ours-new `-` | ours-27f5 `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor | 0/0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| new-vs-27f5-def-tpch-local | ours-new `-` | ours-27f5 `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 0/0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| new-vs-27f5-def-tpch-s3 | ours-new `-` | ours-27f5 `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 0/0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| new-vs-27f5-t8-lat-local | ours-new `-DduckDbThreads=8` | ours-27f5 `-DduckDbThreads=8` | local | Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor | 0/0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| new-vs-27f5-t8-lat-s3 | ours-new `-DduckDbThreads=8` | ours-27f5 `-DduckDbThreads=8` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 0/0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| new-vs-27f5-t8-tpch-local | ours-new `-DduckDbThreads=8` | ours-27f5 `-DduckDbThreads=8` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 0/0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| new-vs-27f5-t8-tpch-s3 | ours-new `-DduckDbThreads=8` | ours-27f5 `-DduckDbThreads=8` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 0/0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| new-vs-main-def-local | ours-new `-` | up-main `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 0/0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| new-vs-main-def-s3 | ours-new `-` | up-main `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 0/0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| new-vs-main-t8-local | ours-new `-DduckDbThreads=8` | up-main `-DduckDbThreads=8` | local | Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor | 0/0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| new-vs-main-t8-s3 | ours-new `-DduckDbThreads=8` | up-main `-DduckDbThreads=8` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 0/0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| new-vs-native-def-local | ours-new `-` | up-native `-` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 0/0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| new-vs-native-def-s3 | ours-new `-` | up-native `-` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 0/0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| new-vs-native-t8-local | ours-new `-DduckDbThreads=8` | up-native `-DduckDbThreads=8` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 0/0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |
| new-vs-native-t8-s3 | ours-new `-DduckDbThreads=8` | up-native `-DduckDbThreads=8` | s3 | Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor | 0/0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | none |

## Per job (absolute medians and ratios)

### new-vs-27f5-def-lat-local: A = ours-new `-`, B = ours-27f5 `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|

### new-vs-27f5-def-lat-s3: A = ours-new `-`, B = ours-27f5 `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `small scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|

### new-vs-27f5-def-tpch-local: A = ours-new `-`, B = ours-27f5 `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|

### new-vs-27f5-def-tpch-s3: A = ours-new `-`, B = ours-27f5 `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|

### new-vs-27f5-t8-lat-local: A = ours-new `-DduckDbThreads=8`, B = ours-27f5 `-DduckDbThreads=8`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `small scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|

### new-vs-27f5-t8-lat-s3: A = ours-new `-DduckDbThreads=8`, B = ours-27f5 `-DduckDbThreads=8`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small scan adbcscan`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|

### new-vs-27f5-t8-tpch-local: A = ours-new `-DduckDbThreads=8`, B = ours-27f5 `-DduckDbThreads=8`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|

### new-vs-27f5-t8-tpch-s3: A = ours-new `-DduckDbThreads=8`, B = ours-27f5 `-DduckDbThreads=8`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `sf10 adbc10 sf1 adbc1`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|

### new-vs-main-def-local: A = ours-new `-`, B = up-main `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small adbc10 adbc1 scan adbcscan`, small-query classes `meta_tables,meta_schemas,point_orders,point_lineitem,count_filter,limit10_ob`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|

### new-vs-main-def-s3: A = ours-new `-`, B = up-main `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small adbc10 adbc1 scan adbcscan`, small-query classes `meta_tables,meta_schemas,point_orders,point_lineitem,count_filter,limit10_ob`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|

### new-vs-main-t8-local: A = ours-new `-DduckDbThreads=8`, B = up-main `-DduckDbThreads=8`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor. Workloads: `small adbc10 adbc1 scan adbcscan`, small-query classes `meta_tables,meta_schemas,point_orders,point_lineitem,count_filter,limit10_ob`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|

### new-vs-main-t8-s3: A = ours-new `-DduckDbThreads=8`, B = up-main `-DduckDbThreads=8`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small adbc10 adbc1 scan adbcscan`, small-query classes `meta_tables,meta_schemas,point_orders,point_lineitem,count_filter,limit10_ob`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|

### new-vs-native-def-local: A = ours-new `-`, B = up-native `-`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small adbc10 adbc1 scan adbcscan`, small-query classes `meta_tables,meta_schemas,point_orders,point_lineitem,count_filter,limit10_ob`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|

### new-vs-native-def-s3: A = ours-new `-`, B = up-native `-`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small adbc10 adbc1 scan adbcscan`, small-query classes `meta_tables,meta_schemas,point_orders,point_lineitem,count_filter,limit10_ob`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|

### new-vs-native-t8-local: A = ours-new `-DduckDbThreads=8`, B = up-native `-DduckDbThreads=8`, local

Runner: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor. Workloads: `small adbc10 adbc1 scan adbcscan`, small-query classes `meta_tables,meta_schemas,point_orders,point_lineitem,count_filter,limit10_ob`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|

### new-vs-native-t8-s3: A = ours-new `-DduckDbThreads=8`, B = up-native `-DduckDbThreads=8`, s3

Runner: Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor. Workloads: `small adbc10 adbc1 scan adbcscan`, small-query classes `meta_tables,meta_schemas,point_orders,point_lineitem,count_filter,limit10_ob`.

| metric | unit | A median | B median | B / A | per-round B / A |
|---|---|---|---|---|---|
