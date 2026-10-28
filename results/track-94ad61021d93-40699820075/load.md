# Server comparison - Report 2: LOAD (compare run 40699820075)

## Setup

| item | value |
|---|---|
| runner | GitHub-hosted `ubuntu-latest`: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor; Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor; Linux ubuntu24 4 vCPU Intel(R) Xeon(R) 6973P-C; Linux ubuntu24 4 vCPU Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz; RAM 15983 MB |
| containers | every server: `eclipse-temurin:21-jre`, `--cpus=2 --cpuset-cpus=0,1 --memory=6g --memory-swap=6g`, JVM `-Xmx3g -XX:MaxDirectMemorySize=2g`, `MALLOC_ARENA_MAX=4`; load generators in their own container on cpus 2,3 (so the client side has 2 cores too: at 64/128 clients the client can be the limit, see client notes) |
| servers | ours-new = `7562a5bdb7b9`; ours-27f5 = `27f583adccd7`; up-native = `9db2bf16a0d15a657f491bb18de1ef50e2e208a8`; up-main = `dbacd8d585bce2ef2a449c821fe3a53cc6060b57` |
| data | TPC-H SF10 Parquet on local disk (load, mixed, heavy, netem) |
| pairs | ours-new (side A) vs one other server (side B) on the same runner, rounds A B / B A / A B |
| load mix | `point_orders`, `point_lineitem`, `count_filter` (every server answers them; upstream has no JDBC prepared statements) |
| settings | `def` = each server's default `duckDbThreads` (ours 4, upstream 2); `t8` = 8 on both; `zstd` = netem path only, up-native with its ZSTD batch compression (`-DflightCompression=zstd`, decoded by ADBC) vs ours plain (up-main has no such option) |

## Setting `def`

### Closed-loop load, JDBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main | 94ad61021d93 | 94ad61021d93 -DdistributedComplete=true |
|---|---|---|---|---|---|---|
| 1 | 59 / 14.6 / 27.9 / 37.4 / 0 / 163 / 383 | n/a | n/a | n/a | 64 / 13.1 / 25.4 / 37.6 / 0 / 163 / 385 | n/a |
| 8 | 67 / 119.4 / 187.9 / 246.6 / 0 / 184 / 798 | n/a | n/a | n/a | 72 / 114.0 / 181.8 / 208.9 / 0 / 186 / 755 | n/a |
| 32 | 61 / 496.3 / 898.9 / 1216.5 / 0 / 187 / 1755 | n/a | n/a | n/a | 67 / 474.8 / 832.2 / 1026.7 / 0 / 188 / 1663 | n/a |
| 64 | 57 / 1055.2 / 2053.0 / 2546.2 / 0 / 182 / 2713 | n/a | n/a | n/a | 64 / 957.3 / 1816.9 / 2333.6 / 0 / 194 / 2770 | n/a |
| 128 | 48 / 2327.1 / 4972.3 / 6399.6 / 0 / 183 / 4221 | n/a | n/a | n/a | 59 / 1957.2 / 4192.1 / 5419.7 / 0 / 190 / 4327 | n/a |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | 1 | none | none | none | 1 | none |

### Closed-loop load, ADBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main | 94ad61021d93 | 94ad61021d93 -DdistributedComplete=true |
|---|---|---|---|---|---|---|
| 1 | 63 / 14.1 / 25.2 / 30.9 / 0 / 163 / 392 | n/a | n/a | n/a | 65 / 13.3 / 24.5 / 30.0 / 0 / 163 / 408 | n/a |
| 8 | 67 / 120.3 / 184.1 / 219.0 / 0 / 194 / 812 | n/a | n/a | n/a | 71 / 117.6 / 180.2 / 206.5 / 0 / 195 / 783 | n/a |
| 32 | 57 / 534.0 / 974.5 / 1235.9 / 0 / 196 / 1794 | n/a | n/a | n/a | 64 / 488.4 / 885.1 / 1102.1 / 0 / 199 / 1749 | n/a |
| 64 | 53 / 1104.6 / 2213.0 / 2847.6 / 0 / 190 / 2873 | n/a | n/a | n/a | 61 / 978.4 / 1935.8 / 2528.2 / 0 / 199 / 2948 | n/a |
| 128 | 49 / 2350.9 / 4918.5 / 6480.9 / 0 / 195 / 4921 | n/a | n/a | n/a | 58 / 1969.0 / 4342.7 / 5357.0 / 0 / 194 / 5085 | n/a |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | 1 | none | none | none | 1 | none |

### Mixed load: 32 ADBC small-query clients alone / with 2 heavy SF10 streams (q01, q18)

| metric | ours-new | ours-27f5 | up-native | up-main | 94ad61021d93 | 94ad61021d93 -DdistributedComplete=true |
|---|---|---|---|---|---|---|
| small QPS alone | n/a | n/a | n/a | n/a | n/a | n/a |
| small QPS with heavy | n/a | n/a | n/a | n/a | n/a | n/a |
| small p95 ms alone | n/a | n/a | n/a | n/a | n/a | n/a |
| small p95 ms with heavy | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy q01 s (median of runs during the window) | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy q18 s | n/a | n/a | n/a | n/a | n/a | n/a |
| small errors alone / with heavy; heavy failures or wrong answers | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 |

### 4 heavy SF10 queries at once (q01 q09 q18 q21, ADBC) and network-limited client path (netem 10 ms RTT, 1 Gbit/s)

| metric | ours-new | ours-27f5 | up-native | up-main | 94ad61021d93 | 94ad61021d93 -DdistributedComplete=true |
|---|---|---|---|---|---|---|
| heavy x4: slowest query s (n/a if any failed) | n/a | n/a | n/a | n/a | 18.1 | n/a |
| heavy x4: failed or wrong (all rounds) | n/a | n/a | n/a | n/a | 0 | n/a |
| heavy x4: server peak RSS MiB | n/a | n/a | n/a | n/a | 2763 | n/a |
| netem: SF10 TPC-H ADBC, sum of warm medians s (correct queries) | n/a | n/a | n/a | n/a | n/a | n/a |
| netem: full lineitem export over ADBC, MB/s | n/a | n/a | n/a | n/a | n/a | n/a |

Not in this run: up-native with its ZSTD Flight compression on the netem path (job `new-vs-native-zstd-netem`).

Not yet in this report: TLS + token on/off for ours.

