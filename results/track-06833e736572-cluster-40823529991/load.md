# Server comparison - Report 2: LOAD (compare run 40823529991)

## Setup

| item | value |
|---|---|
| runner | GitHub-hosted `ubuntu-latest`: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor; RAM 15983 MB |
| containers | every server: `eclipse-temurin:21-jre`, `--cpus=2 --cpuset-cpus=0,1 --memory=6g --memory-swap=6g`, JVM `-Xmx3g -XX:MaxDirectMemorySize=2g`, `MALLOC_ARENA_MAX=4`; load generators in their own container on cpus 2,3 (so the client side has 2 cores too: at 64/128 clients the client can be the limit, see client notes) |
| servers | ours-new = `7562a5bdb7b9`; ours-27f5 = `27f583adccd7`; up-native = `1de5f6b4b218f83f01a3adf2708af5f36f80811b`; up-main = `dbacd8d585bce2ef2a449c821fe3a53cc6060b57` |
| data | TPC-H SF10 Parquet on local disk (load, mixed, heavy, netem) |
| pairs | ours-new (side A) vs one other server (side B) on the same runner, rounds A B / B A / A B |
| load mix | `point_orders`, `point_lineitem`, `count_filter` (every server answers them; upstream has no JDBC prepared statements) |
| settings | `def` = each server's default `duckDbThreads` (ours 4, upstream 2); `t8` = 8 on both; `zstd` = netem path only, up-native with its ZSTD batch compression (`-DflightCompression=zstd`, decoded by ADBC) vs ours plain (up-main has no such option) |

## Setting `def`

### Closed-loop load, JDBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main | 06833e736572 | 06833e736572 -DdistributedComplete=true |
|---|---|---|---|---|---|---|
| 1 | n/a | n/a | n/a | n/a | n/a | n/a |
| 8 | n/a | n/a | n/a | n/a | n/a | n/a |
| 32 | n/a | n/a | n/a | n/a | n/a | n/a |
| 64 | n/a | n/a | n/a | n/a | n/a | n/a |
| 128 | n/a | n/a | n/a | n/a | n/a | n/a |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | none | none | none | none | none | none |

### Closed-loop load, ADBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main | 06833e736572 | 06833e736572 -DdistributedComplete=true |
|---|---|---|---|---|---|---|
| 1 | n/a | n/a | n/a | n/a | n/a | n/a |
| 8 | n/a | n/a | n/a | n/a | n/a | n/a |
| 32 | n/a | n/a | n/a | n/a | n/a | n/a |
| 64 | n/a | n/a | n/a | n/a | n/a | n/a |
| 128 | n/a | n/a | n/a | n/a | n/a | n/a |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | none | none | none | none | none | none |

### Mixed load: 32 ADBC small-query clients alone / with 2 heavy SF10 streams (q01, q18)

| metric | ours-new | ours-27f5 | up-native | up-main | 06833e736572 | 06833e736572 -DdistributedComplete=true |
|---|---|---|---|---|---|---|
| small QPS alone | n/a | n/a | n/a | n/a | n/a | n/a |
| small QPS with heavy | n/a | n/a | n/a | n/a | n/a | n/a |
| small p95 ms alone | n/a | n/a | n/a | n/a | n/a | n/a |
| small p95 ms with heavy | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy q01 s (median of runs during the window) | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy q18 s | n/a | n/a | n/a | n/a | n/a | n/a |
| small errors alone / with heavy; heavy failures or wrong answers | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 |

### 4 heavy SF10 queries at once (q01 q09 q18 q21, ADBC) and network-limited client path (netem 10 ms RTT, 1 Gbit/s)

| metric | ours-new | ours-27f5 | up-native | up-main | 06833e736572 | 06833e736572 -DdistributedComplete=true |
|---|---|---|---|---|---|---|
| heavy x4: slowest query s (n/a if any failed) | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy x4: failed or wrong (all rounds) | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy x4: server peak RSS MiB | n/a | n/a | n/a | n/a | n/a | n/a |
| netem: SF10 TPC-H ADBC, sum of warm medians s (correct queries) | n/a | n/a | n/a | n/a | n/a | n/a |
| netem: full lineitem export over ADBC, MB/s | n/a | n/a | n/a | n/a | n/a | n/a |

Not in this run: up-native with its ZSTD Flight compression on the netem path (job `new-vs-native-zstd-netem`).

Not yet in this report: TLS + token on/off for ours.

