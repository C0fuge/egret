# Server comparison - Report 2: LOAD (compare run 44335959845)

## Setup

| item | value |
|---|---|
| runner | GitHub-hosted `ubuntu-latest`: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor; Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor; Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor; Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C; Linux ubuntu26 4 vCPU Intel(R) Xeon(R) 6975P-C; RAM 15983 MB |
| containers | every server: `eclipse-temurin:21-jre`, `--cpus=2 --cpuset-cpus=0,1 --memory=6g --memory-swap=6g`, JVM `-Xmx3g -XX:MaxDirectMemorySize=2g`, `MALLOC_ARENA_MAX=4`; load generators in their own container on cpus 2,3 (so the client side has 2 cores too: at 64/128 clients the client can be the limit, see client notes) |
| servers | ours-new = `7562a5bdb7b9`; ours-27f5 = `27f583adccd7`; up-native = `47c6c7d95db0b78a807c40b56f3bc303ccc4fc04`; up-main = `dbacd8d585bce2ef2a449c821fe3a53cc6060b57` |
| data | TPC-H SF10 Parquet on local disk (load, mixed, heavy, netem) |
| pairs | ours-new (side A) vs one other server (side B) on the same runner, rounds A B / B A / A B |
| load mix | `point_orders`, `point_lineitem`, `count_filter` (every server answers them; upstream has no JDBC prepared statements) |
| settings | `def` = each server's default `duckDbThreads` (ours 4, upstream 2); `t8` = 8 on both; `zstd` = netem path only, up-native with its ZSTD batch compression (`-DflightCompression=zstd`, decoded by ADBC) vs ours plain (up-main has no such option) |

## Setting `def`

### Closed-loop load, JDBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main | 06d6468b17c5 | 06d6468b17c5 -DresourceProfile=speed | 06d6468b17c5 CZSTD | 06d6468b17c5 CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| 1 | n/a | n/a | 49 / 16.7 / 37.1 / 56.1 / 0 / 166 / 410 | n/a | 55 / 14.6 / 31.4 / 42.3 / 0 / 172 / 401 | 55 / 14.8 / 32.0 / 42.0 / 0 / 172 / 401 | n/a | n/a |
| 8 | n/a | n/a | 67 / 106.9 / 245.9 / 268.7 / 0 / 196 / 466 | n/a | 67 / 105.9 / 253.9 / 284.4 / 0 / 181 / 531 | 66 / 111.9 / 263.6 / 303.9 / 0 / 181 / 531 | n/a | n/a |
| 32 | n/a | n/a | 69 / 396.5 / 915.5 / 1027.9 / 0 / 192 / 617 | n/a | 67 / 407.7 / 952.9 / 1068.3 / 0 / 191 / 577 | 66 / 426.9 / 964.7 / 1078.1 / 0 / 191 / 577 | n/a | n/a |
| 64 | n/a | n/a | 69 / 811.0 / 1890.4 / 2213.1 / 0 / 188 / 794 | n/a | 66 / 879.8 / 1912.4 / 2313.2 / 0 / 184 / 682 | 66 / 888.5 / 1913.3 / 2333.1 / 0 / 183 / 682 | n/a | n/a |
| 128 | n/a | n/a | 68 / 1719.1 / 4022.8 / 4986.2 / 0 / 193 / 930 | n/a | 65 / 1788.3 / 4172.8 / 5275.0 / 0 / 192 / 841 | 64 / 1795.4 / 4169.7 / 5264.4 / 0 / 192 / 841 | n/a | n/a |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | none | none | 1 | none | 1 | 1 | none | none |

### Closed-loop load, ADBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main | 06d6468b17c5 | 06d6468b17c5 -DresourceProfile=speed | 06d6468b17c5 CZSTD | 06d6468b17c5 CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| 1 | n/a | n/a | 58 / 13.8 / 28.0 / 50.8 / 0 / 161 / 390 | n/a | 57 / 14.4 / 28.8 / 38.9 / 0 / 170 / 429 | 57 / 14.5 / 29.3 / 39.4 / 0 / 170 / 429 | n/a | n/a |
| 8 | n/a | n/a | 72 / 98.6 / 231.5 / 255.6 / 0 / 203 / 522 | n/a | 68 / 106.1 / 249.8 / 278.9 / 0 / 202 / 548 | 67 / 113.1 / 257.6 / 295.0 / 0 / 202 / 548 | n/a | n/a |
| 32 | n/a | n/a | 71 / 382.7 / 885.9 / 992.0 / 0 / 193 / 645 | n/a | 67 / 412.8 / 943.2 / 1057.3 / 0 / 203 / 594 | 66 / 423.5 / 964.4 / 1086.2 / 0 / 203 / 594 | n/a | n/a |
| 64 | n/a | n/a | 70 / 803.2 / 1862.9 / 2233.7 / 0 / 193 / 821 | n/a | 66 / 894.8 / 1922.0 / 2292.6 / 0 / 203 / 724 | 66 / 904.6 / 1926.5 / 2276.5 / 0 / 203 / 724 | n/a | n/a |
| 128 | n/a | n/a | 67 / 1744.0 / 4056.6 / 5096.6 / 0 / 203 / 940 | n/a | 65 / 1791.2 / 4212.2 / 5327.8 / 0 / 202 / 863 | 65 / 1816.3 / 4234.4 / 5274.9 / 0 / 203 / 863 | n/a | n/a |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | none | none | 1 | none | 1 | 1 | none | none |

### Mixed load: 32 ADBC small-query clients alone / with 2 heavy SF10 streams (q01, q18)

| metric | ours-new | ours-27f5 | up-native | up-main | 06d6468b17c5 | 06d6468b17c5 -DresourceProfile=speed | 06d6468b17c5 CZSTD | 06d6468b17c5 CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| small QPS alone | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small QPS with heavy | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small p95 ms alone | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small p95 ms with heavy | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy q01 s (median of runs during the window) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy q18 s | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small errors alone / with heavy; heavy failures or wrong answers | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 |

### 4 heavy SF10 queries at once (q01 q09 q18 q21, ADBC) and network-limited client path (netem 10 ms RTT, 1 Gbit/s)

| metric | ours-new | ours-27f5 | up-native | up-main | 06d6468b17c5 | 06d6468b17c5 -DresourceProfile=speed | 06d6468b17c5 CZSTD | 06d6468b17c5 CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| heavy x4: slowest query s (n/a if any failed) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy x4: failed or wrong (all rounds) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy x4: server peak RSS MiB | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| netem: SF10 TPC-H ADBC, sum of warm medians s (correct queries) | n/a | n/a | 0.0 (0/22 q) | n/a | n/a | n/a | 24.0 (22/22 q) | 23.8 (22/22 q) |
| netem: full lineitem export over ADBC, MB/s | n/a | n/a | 331 | n/a | n/a | n/a | 350 | 356 |

## Netem pairs per job (both sides on the same runner; medians over rounds, B / A per round)

| job | A | B | TPC-H SF10 ADBC s A | B | B / A | export MB/s A | B | B / A | per-round export B / A | queries not ok A / B |
|---|---|---|---|---|---|---|---|---|---|---|
| fu-zstd-netem-local | 06d6468b17c5 CZSTD | 06d6468b17c5 CZSTD -DresourceProfile=speed CZSTD | 24.2 | 23.8 | 0.98 | 349 | 356 | 1.02 | 1.01 1.02 1.02 | 0 / 0 |
| fu-zstd-netem-local-vs-up-native | up-native | 06d6468b17c5 CZSTD | n/a | 23.8 | n/a | 331 | 356 | 1.07 | 1.07 1.07 1.07 | 22 / 0 |

TPC-H n/a = not all 22 queries answered correctly in a round (see 'queries not ok', max over rounds).

Not in this run: up-native with its ZSTD Flight compression on the netem path (job `new-vs-native-zstd-netem`).

Not yet in this report: TLS + token on/off for ours.

