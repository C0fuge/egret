# Server comparison - Report 2: LOAD (compare run 41132125972)

## Setup

| item | value |
|---|---|
| runner | GitHub-hosted `ubuntu-latest`: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor; RAM 15983 MB |
| containers | every server: `eclipse-temurin:21-jre`, `--cpus=2 --cpuset-cpus=0,1 --memory=6g --memory-swap=6g`, JVM `-Xmx3g -XX:MaxDirectMemorySize=2g`, `MALLOC_ARENA_MAX=4`; load generators in their own container on cpus 2,3 (so the client side has 2 cores too: at 64/128 clients the client can be the limit, see client notes) |
| servers | ours-new = `7562a5bdb7b9`; ours-27f5 = `27f583adccd7`; up-native = `9fb08d9dd24df3cb838a3172f9375560bb6dc70a`; up-main = `dbacd8d585bce2ef2a449c821fe3a53cc6060b57` |
| data | TPC-H SF10 Parquet on local disk (load, mixed, heavy, netem) |
| pairs | ours-new (side A) vs one other server (side B) on the same runner, rounds A B / B A / A B |
| load mix | `point_orders`, `point_lineitem`, `count_filter` (every server answers them; upstream has no JDBC prepared statements) |
| settings | `def` = each server's default `duckDbThreads` (ours 4, upstream 2); `t8` = 8 on both; `zstd` = netem path only, up-native with its ZSTD batch compression (`-DflightCompression=zstd`, decoded by ADBC) vs ours plain (up-main has no such option) |

## Setting `def`

### Closed-loop load, JDBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main | f06b5834e76e | f06b5834e76e -DresourceProfile=speed |
|---|---|---|---|---|---|---|
| 1 | n/a | n/a | 38 / 22.1 / 46.5 / 69.2 / 0 / 168 / 513 | n/a | 40 / 20.8 / 42.8 / 54.5 / 0 / 170 / 412 | 40 / 20.7 / 42.3 / 54.4 / 0 / 170 / 364 |
| 8 | n/a | n/a | 51 / 146.6 / 318.2 / 345.3 / 0 / 202 / 776 | n/a | 46 / 171.1 / 316.7 / 365.3 / 0 / 188 / 796 | 50 / 153.0 / 350.6 / 392.1 / 0 / 188 / 456 |
| 32 | n/a | n/a | 52 / 539.8 / 1181.9 / 1297.9 / 0 / 193 / 1575 | n/a | 45 / 661.4 / 1298.4 / 1765.2 / 0 / 188 / 1645 | 51 / 553.3 / 1233.4 / 1396.0 / 0 / 182 / 516 |
| 64 | n/a | n/a | 53 / 1121.8 / 2354.6 / 2814.7 / 0 / 180 / 2433 | n/a | 45 / 1354.7 / 2719.6 / 3384.3 / 0 / 186 / 2612 | 51 / 1167.0 / 2420.2 / 2866.5 / 0 / 182 / 668 |
| 128 | n/a | n/a | 52 / 2232.8 / 5093.3 / 6294.5 / 0 / 196 / 3637 | n/a | 42 / 2808.4 / 5974.1 / 7474.2 / 0 / 195 / 4016 | 49 / 2378.0 / 5167.2 / 6389.9 / 0 / 191 / 899 |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | none | none | 1 | none | 1 | 1 |

### Closed-loop load, ADBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main | f06b5834e76e | f06b5834e76e -DresourceProfile=speed |
|---|---|---|---|---|---|---|
| 1 | n/a | n/a | 43 / 19.2 / 36.8 / 62.3 / 0 / 166 / 486 | n/a | 41 / 20.1 / 38.5 / 50.2 / 0 / 165 / 417 | 42 / 19.9 / 38.3 / 50.4 / 0 / 170 / 382 |
| 8 | n/a | n/a | 54 / 137.9 / 300.0 / 324.6 / 0 / 193 / 791 | n/a | 47 / 169.2 / 313.3 / 359.7 / 0 / 203 / 789 | 50 / 153.1 / 344.0 / 393.5 / 0 / 203 / 474 |
| 32 | n/a | n/a | 54 / 520.2 / 1162.6 / 1277.5 / 0 / 203 / 1733 | n/a | 46 / 657.1 / 1294.5 / 1673.8 / 0 / 197 / 1785 | 52 / 552.4 / 1228.4 / 1370.4 / 0 / 202 / 591 |
| 64 | n/a | n/a | 53 / 1102.4 / 2376.6 / 2779.3 / 0 / 192 / 2823 | n/a | 45 / 1371.3 / 2704.9 / 3459.0 / 0 / 191 / 2938 | 51 / 1166.9 / 2394.8 / 2880.4 / 0 / 192 / 821 |
| 128 | n/a | n/a | 53 / 2196.4 / 5029.7 / 6585.9 / 0 / 191 / 4796 | n/a | 42 / 2812.0 / 5805.6 / 7318.8 / 0 / 192 / 4688 | 50 / 2401.7 / 5190.7 / 6351.8 / 0 / 197 / 755 |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | none | none | 1 | none | 1 | 1 |

### Mixed load: 32 ADBC small-query clients alone / with 2 heavy SF10 streams (q01, q18)

| metric | ours-new | ours-27f5 | up-native | up-main | f06b5834e76e | f06b5834e76e -DresourceProfile=speed |
|---|---|---|---|---|---|---|
| small QPS alone | n/a | n/a | n/a | n/a | n/a | n/a |
| small QPS with heavy | n/a | n/a | n/a | n/a | n/a | n/a |
| small p95 ms alone | n/a | n/a | n/a | n/a | n/a | n/a |
| small p95 ms with heavy | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy q01 s (median of runs during the window) | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy q18 s | n/a | n/a | n/a | n/a | n/a | n/a |
| small errors alone / with heavy; heavy failures or wrong answers | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 |

### 4 heavy SF10 queries at once (q01 q09 q18 q21, ADBC) and network-limited client path (netem 10 ms RTT, 1 Gbit/s)

| metric | ours-new | ours-27f5 | up-native | up-main | f06b5834e76e | f06b5834e76e -DresourceProfile=speed |
|---|---|---|---|---|---|---|
| heavy x4: slowest query s (n/a if any failed) | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy x4: failed or wrong (all rounds) | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy x4: server peak RSS MiB | n/a | n/a | n/a | n/a | n/a | n/a |
| netem: SF10 TPC-H ADBC, sum of warm medians s (correct queries) | n/a | n/a | n/a | n/a | n/a | n/a |
| netem: full lineitem export over ADBC, MB/s | n/a | n/a | n/a | n/a | n/a | n/a |

Not in this run: up-native with its ZSTD Flight compression on the netem path (job `new-vs-native-zstd-netem`).

Not yet in this report: TLS + token on/off for ours.

