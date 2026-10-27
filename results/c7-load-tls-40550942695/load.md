# Server comparison - Report 2: LOAD (compare run 40550942695)

## Setup

| item | value |
|---|---|
| runner | GitHub-hosted `ubuntu-latest`: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor; Linux ubuntu24 4 vCPU Intel(R) Xeon(R) 6973P-C; RAM 15988 MB |
| containers | every server: `eclipse-temurin:21-jre`, `--cpus=2 --cpuset-cpus=0,1 --memory=6g --memory-swap=6g`, JVM `-Xmx3g -XX:MaxDirectMemorySize=2g`, `MALLOC_ARENA_MAX=4`; load generators in their own container on cpus 2,3 (so the client side has 2 cores too: at 64/128 clients the client can be the limit, see client notes) |
| servers | ours-new = `7562a5bdb7b9`; ours-27f5 = `27f583adccd7`; up-native = `202b4cef8a395c5ab62456e75fcc027f6f998683`; up-main = `dbacd8d585bce2ef2a449c821fe3a53cc6060b57` |
| data | TPC-H SF10 Parquet on local disk (load, mixed, heavy, netem) |
| pairs | ours-new (side A) vs one other server (side B) on the same runner, rounds A B / B A / A B |
| load mix | `point_orders`, `point_lineitem`, `count_filter` (every server answers them; upstream has no JDBC prepared statements) |
| settings | `def` = each server's default `duckDbThreads` (ours 4, upstream 2); `t8` = 8 on both; `zstd` = netem path only, up-native with its ZSTD batch compression (`-DflightCompression=zstd`, decoded by ADBC) vs ours plain (up-main has no such option) |

## Setting `def`

### Closed-loop load, JDBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main | ours-new TLS |
|---|---|---|---|---|---|
| 1 | 38 / 21.6 / 44.6 / 53.7 / 0 / 173 / 436 | n/a | n/a | n/a | 38 / 21.9 / 45.0 / 55.4 / 0 / 168 / 483 |
| 8 | 44 / 183.7 / 282.1 / 335.4 / 0 / 188 / 860 | n/a | n/a | n/a | 44 / 184.9 / 279.7 / 327.4 / 0 / 199 / 839 |
| 32 | 41 / 752.5 / 1333.4 / 2032.4 / 0 / 186 / 1943 | n/a | n/a | n/a | 41 / 742.5 / 1295.9 / 1923.1 / 0 / 196 / 1830 |
| 64 | 39 / 1534.8 / 2975.7 / 3859.3 / 0 / 194 / 3000 | n/a | n/a | n/a | 39 / 1519.2 / 2921.5 / 3917.7 / 0 / 187 / 2891 |
| 128 | 34 / 3346.7 / 7023.2 / 8943.0 / 0 / 200 / 4723 | n/a | n/a | n/a | 36 / 3239.3 / 6826.1 / 8383.7 / 0 / 185 / 4802 |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | 1 | none | none | none | 1 |

### Closed-loop load, ADBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main | ours-new TLS |
|---|---|---|---|---|---|
| 1 | 40 / 20.8 / 39.7 / 51.7 / 0 / 164 / 435 | n/a | n/a | n/a | 40 / 20.5 / 39.7 / 51.4 / 0 / 164 / 478 |
| 8 | 43 / 187.3 / 283.0 / 330.6 / 0 / 191 / 868 | n/a | n/a | n/a | 44 / 187.8 / 276.9 / 320.6 / 0 / 199 / 845 |
| 32 | 40 / 763.7 / 1367.1 / 1935.5 / 0 / 191 / 2153 | n/a | n/a | n/a | 41 / 758.1 / 1300.4 / 1967.5 / 0 / 203 / 1924 |
| 64 | 37 / 1571.0 / 3098.5 / 4373.7 / 0 / 188 / 3483 | n/a | n/a | n/a | 38 / 1531.2 / 3071.8 / 4071.3 / 0 / 199 / 3411 |
| 128 | 34 / 3270.4 / 6929.0 / 9269.5 / 0 / 192 / 5528 | n/a | n/a | n/a | 34 / 3313.9 / 6742.3 / 8243.3 / 0 / 200 / 5471 |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | 1 | none | none | none | 1 |

### Mixed load: 32 ADBC small-query clients alone / with 2 heavy SF10 streams (q01, q18)

| metric | ours-new | ours-27f5 | up-native | up-main | ours-new TLS |
|---|---|---|---|---|---|
| small QPS alone | n/a | n/a | n/a | n/a | n/a |
| small QPS with heavy | n/a | n/a | n/a | n/a | n/a |
| small p95 ms alone | n/a | n/a | n/a | n/a | n/a |
| small p95 ms with heavy | n/a | n/a | n/a | n/a | n/a |
| heavy q01 s (median of runs during the window) | n/a | n/a | n/a | n/a | n/a |
| heavy q18 s | n/a | n/a | n/a | n/a | n/a |
| small errors alone / with heavy; heavy failures or wrong answers | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 |

### 4 heavy SF10 queries at once (q01 q09 q18 q21, ADBC) and network-limited client path (netem 10 ms RTT, 1 Gbit/s)

| metric | ours-new | ours-27f5 | up-native | up-main | ours-new TLS |
|---|---|---|---|---|---|
| heavy x4: slowest query s (n/a if any failed) | n/a | n/a | n/a | n/a | n/a |
| heavy x4: failed or wrong (all rounds) | n/a | n/a | n/a | n/a | n/a |
| heavy x4: server peak RSS MiB | n/a | n/a | n/a | n/a | n/a |
| netem: SF10 TPC-H ADBC, sum of warm medians s (correct queries) | n/a | n/a | n/a | n/a | n/a |
| netem: full lineitem export over ADBC, MB/s | n/a | n/a | n/a | n/a | n/a |

Not in this run: up-native with its ZSTD Flight compression on the netem path (job `new-vs-native-zstd-netem`).

