# Server comparison - Report 2: LOAD (compare run 42791002963)

## Setup

| item | value |
|---|---|
| runner | GitHub-hosted `ubuntu-latest`: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor; Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor; Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor; Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C; RAM 15982 MB |
| containers | every server: `eclipse-temurin:21-jre`, `--cpus=2 --cpuset-cpus=0,1 --memory=6g --memory-swap=6g`, JVM `-Xmx3g -XX:MaxDirectMemorySize=2g`, `MALLOC_ARENA_MAX=4`; load generators in their own container on cpus 2,3 (so the client side has 2 cores too: at 64/128 clients the client can be the limit, see client notes) |
| servers | ours-new = `7562a5bdb7b9`; ours-27f5 = `27f583adccd7`; up-native = `b7d32cf3b3f0ba71f79a7d3f425bbc0241eb6036`; up-main = `dbacd8d585bce2ef2a449c821fe3a53cc6060b57` |
| data | TPC-H SF10 Parquet on local disk (load, mixed, heavy, netem) |
| pairs | ours-new (side A) vs one other server (side B) on the same runner, rounds A B / B A / A B |
| load mix | `point_orders`, `point_lineitem`, `count_filter` (every server answers them; upstream has no JDBC prepared statements) |
| settings | `def` = each server's default `duckDbThreads` (ours 4, upstream 2); `t8` = 8 on both; `zstd` = netem path only, up-native with its ZSTD batch compression (`-DflightCompression=zstd`, decoded by ADBC) vs ours plain (up-main has no such option) |

## Setting `def`

### Closed-loop load, JDBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main | 37bf9401d77c | 37bf9401d77c -DresourceProfile=speed | 37bf9401d77c CZSTD | 37bf9401d77c CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| 1 | n/a | n/a | 42 / 19.7 / 42.6 / 63.3 / 0 / 158 / 413 | n/a | 43 / 19.2 / 40.9 / 53.4 / 0 / 166 / 555 | 43 / 19.2 / 40.9 / 54.1 / 0 / 167 / 484 | n/a | n/a |
| 8 | n/a | n/a | 57 / 124.9 / 288.3 / 308.0 / 0 / 200 / 440 | n/a | 52 / 148.6 / 283.0 / 325.6 / 0 / 200 / 834 | 56 / 136.4 / 310.7 / 353.0 / 0 / 200 / 581 | n/a | n/a |
| 32 | n/a | n/a | 60 / 454.9 / 1050.1 / 1170.5 / 0 / 202 / 592 | n/a | 51 / 576.0 / 1137.4 / 1326.4 / 0 / 195 / 1726 | 57 / 490.0 / 1137.0 / 1276.9 / 0 / 193 / 690 | n/a | n/a |
| 64 | n/a | n/a | 60 / 967.6 / 2144.9 / 2540.2 / 0 / 182 / 799 | n/a | 50 / 1236.9 / 2399.0 / 2958.5 / 0 / 191 / 2597 | 57 / 1071.9 / 2229.2 / 2731.5 / 0 / 190 / 799 | n/a | n/a |
| 128 | n/a | n/a | 60 / 1952.3 / 4557.6 / 5657.0 / 0 / 201 / 943 | n/a | 47 / 2501.0 / 5238.1 / 6414.2 / 0 / 191 / 4255 | 56 / 2096.7 / 4841.4 / 5960.5 / 0 / 192 / 920 | n/a | n/a |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | none | none | 1 | none | 1 | 1 | none | none |

### Closed-loop load, ADBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main | 37bf9401d77c | 37bf9401d77c -DresourceProfile=speed | 37bf9401d77c CZSTD | 37bf9401d77c CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| 1 | n/a | n/a | 49 / 16.8 / 32.5 / 55.0 / 0 / 164 / 394 | n/a | 46 / 18.3 / 35.1 / 47.6 / 0 / 164 / 477 | 45 / 18.4 / 35.6 / 47.7 / 0 / 164 / 470 | n/a | n/a |
| 8 | n/a | n/a | 62 / 114.7 / 267.3 / 289.0 / 0 / 192 / 439 | n/a | 52 / 150.0 / 276.0 / 317.5 / 0 / 196 / 870 | 57 / 134.5 / 299.0 / 341.2 / 0 / 195 / 595 | n/a | n/a |
| 32 | n/a | n/a | 61 / 444.1 / 1038.1 / 1147.4 / 0 / 194 / 649 | n/a | 51 / 587.3 / 1158.2 / 1336.4 / 0 / 200 / 1880 | 57 / 486.2 / 1128.6 / 1263.0 / 0 / 201 / 686 | n/a | n/a |
| 64 | n/a | n/a | 60 / 967.3 / 2160.6 / 2540.0 / 0 / 191 / 809 | n/a | 49 / 1239.6 / 2380.6 / 2864.2 / 0 / 200 / 3034 | 57 / 1082.1 / 2201.9 / 2656.5 / 0 / 201 / 815 | n/a | n/a |
| 128 | n/a | n/a | 59 / 1916.3 / 4585.5 / 5758.2 / 1 (connect t75: OperationalError: IO: [Flight SQL] failed to up) / 189 / 993 | n/a | 47 / 2520.7 / 5247.9 / 6691.2 / 0 / 199 / 4919 | 56 / 2095.6 / 4813.4 / 5944.5 / 0 / 201 / 984 | n/a | n/a |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | none | none | 1 | none | 1 | 1 | none | none |

### Mixed load: 32 ADBC small-query clients alone / with 2 heavy SF10 streams (q01, q18)

| metric | ours-new | ours-27f5 | up-native | up-main | 37bf9401d77c | 37bf9401d77c -DresourceProfile=speed | 37bf9401d77c CZSTD | 37bf9401d77c CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| small QPS alone | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small QPS with heavy | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small p95 ms alone | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small p95 ms with heavy | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy q01 s (median of runs during the window) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy q18 s | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small errors alone / with heavy; heavy failures or wrong answers | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 |

### 4 heavy SF10 queries at once (q01 q09 q18 q21, ADBC) and network-limited client path (netem 10 ms RTT, 1 Gbit/s)

| metric | ours-new | ours-27f5 | up-native | up-main | 37bf9401d77c | 37bf9401d77c -DresourceProfile=speed | 37bf9401d77c CZSTD | 37bf9401d77c CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| heavy x4: slowest query s (n/a if any failed) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy x4: failed or wrong (all rounds) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy x4: server peak RSS MiB | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| netem: SF10 TPC-H ADBC, sum of warm medians s (correct queries) | n/a | n/a | 0.0 (0/22 q) | n/a | n/a | n/a | 33.5 (22/22 q) | 33.1 (22/22 q) |
| netem: full lineitem export over ADBC, MB/s | n/a | n/a | 321 | n/a | n/a | n/a | 324 | 323 |

## Netem pairs per job (both sides on the same runner; medians over rounds, B / A per round)

| job | A | B | TPC-H SF10 ADBC s A | B | B / A | export MB/s A | B | B / A | per-round export B / A | queries not ok A / B |
|---|---|---|---|---|---|---|---|---|---|---|
| fu-zstd-netem-local | 37bf9401d77c CZSTD | 37bf9401d77c CZSTD -DresourceProfile=speed CZSTD | 34.3 | 33.1 | 0.96 | 326 | 323 | 0.99 | 0.99 0.94 1.02 | 0 / 0 |
| fu-zstd-netem-local-vs-up-native | up-native | 37bf9401d77c CZSTD | n/a | 33.1 | n/a | 321 | 323 | 1.01 | 1.03 0.95 1.01 | 22 / 0 |

TPC-H n/a = not all 22 queries answered correctly in a round (see 'queries not ok', max over rounds).

Not in this run: up-native with its ZSTD Flight compression on the netem path (job `new-vs-native-zstd-netem`).

Not yet in this report: TLS + token on/off for ours.

