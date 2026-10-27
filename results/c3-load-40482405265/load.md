# Server comparison - Report 2: LOAD (compare run 40482405265)

## Setup

| item | value |
|---|---|
| runner | GitHub-hosted `ubuntu-latest`: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor; Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor; Linux ubuntu24 4 vCPU Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz; RAM 15988 MB |
| containers | every server: `eclipse-temurin:21-jre`, `--cpus=2 --cpuset-cpus=0,1 --memory=6g --memory-swap=6g`, JVM `-Xmx3g -XX:MaxDirectMemorySize=2g`, `MALLOC_ARENA_MAX=4`; load generators in their own container on cpus 2,3 (so the client side has 2 cores too: at 64/128 clients the client can be the limit, see client notes) |
| servers | ours-new = `84fec772ec50`; ours-27f5 = `27f583adccd7`; up-native = `30855be44317d344f76d89043f1a6513afe60a8b`; up-main = `dbacd8d585bce2ef2a449c821fe3a53cc6060b57` |
| data | TPC-H SF10 Parquet on local disk (load, mixed, heavy, netem) |
| pairs | ours-new (side A) vs one other server (side B) on the same runner, rounds A B / B A / A B |
| load mix | `point_orders`, `point_lineitem`, `count_filter` (every server answers them; upstream has no JDBC prepared statements) |
| settings | `def` = each server's default `duckDbThreads` (ours 4, upstream 2); `t8` = 8 on both |

## Setting `def`

### Closed-loop load, JDBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| 1 | n/a | n/a | n/a | n/a |
| 8 | n/a | n/a | n/a | n/a |
| 32 | n/a | n/a | n/a | n/a |
| 64 | n/a | n/a | n/a | n/a |
| 128 | n/a | n/a | n/a | n/a |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | none | none | none | none |

### Closed-loop load, ADBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| 1 | n/a | n/a | n/a | n/a |
| 8 | n/a | n/a | n/a | n/a |
| 32 | n/a | n/a | n/a | n/a |
| 64 | n/a | n/a | n/a | n/a |
| 128 | n/a | n/a | n/a | n/a |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | none | none | none | none |

### Mixed load: 32 ADBC small-query clients alone / with 2 heavy SF10 streams (q01, q18)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| small QPS alone | n/a | n/a | n/a | n/a |
| small QPS with heavy | n/a | n/a | n/a | n/a |
| small p95 ms alone | n/a | n/a | n/a | n/a |
| small p95 ms with heavy | n/a | n/a | n/a | n/a |
| heavy q01 s (median of runs during the window) | n/a | n/a | n/a | n/a |
| heavy q18 s | n/a | n/a | n/a | n/a |
| small errors alone / with heavy; heavy failures or wrong answers | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 |

### 4 heavy SF10 queries at once (q01 q09 q18 q21, ADBC) and network-limited client path (netem 10 ms RTT, 1 Gbit/s)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| heavy x4: slowest query s (n/a if any failed) | n/a | n/a | n/a | n/a |
| heavy x4: failed or wrong (all rounds) | n/a | n/a | n/a | n/a |
| heavy x4: server peak RSS MiB | n/a | n/a | n/a | n/a |
| netem: SF10 TPC-H ADBC, sum of warm medians s (correct queries) | n/a | n/a | n/a | n/a |
| netem: full lineitem export over ADBC, MB/s | n/a | n/a | n/a | n/a |

## Setting `t8`

### Closed-loop load, JDBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| 1 | n/a | n/a | n/a | n/a |
| 8 | n/a | n/a | n/a | n/a |
| 32 | n/a | n/a | n/a | n/a |
| 64 | n/a | n/a | n/a | n/a |
| 128 | n/a | n/a | n/a | n/a |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | none | none | none | none |

### Closed-loop load, ADBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| 1 | n/a | n/a | n/a | n/a |
| 8 | n/a | n/a | n/a | n/a |
| 32 | n/a | n/a | n/a | n/a |
| 64 | n/a | n/a | n/a | n/a |
| 128 | n/a | n/a | n/a | n/a |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | none | none | none | none |

### Mixed load: 32 ADBC small-query clients alone / with 2 heavy SF10 streams (q01, q18)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| small QPS alone | n/a | n/a | n/a | n/a |
| small QPS with heavy | n/a | n/a | n/a | n/a |
| small p95 ms alone | n/a | n/a | n/a | n/a |
| small p95 ms with heavy | n/a | n/a | n/a | n/a |
| heavy q01 s (median of runs during the window) | n/a | n/a | n/a | n/a |
| heavy q18 s | n/a | n/a | n/a | n/a |
| small errors alone / with heavy; heavy failures or wrong answers | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 |

### 4 heavy SF10 queries at once (q01 q09 q18 q21, ADBC) and network-limited client path (netem 10 ms RTT, 1 Gbit/s)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| heavy x4: slowest query s (n/a if any failed) | n/a | n/a | n/a | n/a |
| heavy x4: failed or wrong (all rounds) | n/a | n/a | n/a | n/a |
| heavy x4: server peak RSS MiB | n/a | n/a | n/a | n/a |
| netem: SF10 TPC-H ADBC, sum of warm medians s (correct queries) | n/a | n/a | n/a | n/a |
| netem: full lineitem export over ADBC, MB/s | n/a | n/a | n/a | n/a |

Not yet in this report: upstream with its ZSTD Flight compression on the netem path (the option name is taken from the
upstream build log, `COMPRESSION.txt`, in a follow-up run) and TLS + token on/off for ours.

