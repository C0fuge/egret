# Server comparison - Report 2: LOAD (compare run 41082368785)

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

| clients | ours-new | ours-27f5 | up-native | up-main | 843e4ad5b610 | 843e4ad5b610 -DresourceProfile=speed |
|---|---|---|---|---|---|---|
| 1 | n/a | n/a | 37 / 22.7 / 46.4 / 67.6 / 0 / 167 / 530 | n/a | 40 / 20.8 / 42.6 / 60.3 / 0 / 169 / 381 | 40 / 20.5 / 40.7 / 63.6 / 0 / 169 / 342 |
| 8 | n/a | n/a | 49 / 150.6 / 320.5 / 347.4 / 0 / 203 / 780 | n/a | 46 / 168.3 / 303.0 / 347.0 / 0 / 192 / 781 | 50 / 144.9 / 317.8 / 347.6 / 0 / 188 / 438 |
| 32 | n/a | n/a | 51 / 549.0 / 1186.1 / 1320.2 / 0 / 191 / 1537 | n/a | 46 / 651.9 / 1263.5 / 1664.2 / 0 / 188 / 1604 | 51 / 548.2 / 1191.4 / 1345.4 / 0 / 184 / 555 |
| 64 | n/a | n/a | 53 / 1135.0 / 2375.8 / 2798.9 / 0 / 189 / 2603 | n/a | 44 / 1385.1 / 2675.1 / 3356.3 / 0 / 190 / 2462 | 51 / 1211.0 / 2396.4 / 2849.9 / 0 / 189 / 676 |
| 128 | n/a | n/a | 52 / 2246.8 / 5167.5 / 6838.5 / 0 / 192 / 4110 | n/a | 42 / 2849.0 / 5956.1 / 7588.9 / 0 / 191 / 3855 | 50 / 2346.5 / 5226.0 / 6467.1 / 0 / 192 / 812 |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | none | none | 1 | none | 1 | 1 |

### Closed-loop load, ADBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main | 843e4ad5b610 | 843e4ad5b610 -DresourceProfile=speed |
|---|---|---|---|---|---|---|
| 1 | n/a | n/a | 42 / 19.8 / 36.9 / 62.3 / 0 / 164 / 490 | n/a | 41 / 20.5 / 38.2 / 52.9 / 0 / 165 / 387 | 42 / 20.4 / 37.5 / 54.1 / 0 / 168 / 381 |
| 8 | n/a | n/a | 52 / 144.0 / 303.5 / 331.9 / 0 / 192 / 824 | n/a | 47 / 165.2 / 297.3 / 332.1 / 0 / 200 / 837 | 52 / 141.7 / 307.8 / 333.0 / 0 / 203 / 491 |
| 32 | n/a | n/a | 53 / 540.4 / 1178.7 / 1306.2 / 0 / 203 / 1708 | n/a | 45 / 665.8 / 1265.9 / 1701.8 / 0 / 202 / 1731 | 51 / 548.3 / 1197.0 / 1323.8 / 0 / 202 / 535 |
| 64 | n/a | n/a | 53 / 1109.5 / 2388.2 / 2842.3 / 0 / 198 / 3182 | n/a | 44 / 1386.4 / 2765.8 / 3533.1 / 0 / 190 / 2792 | 51 / 1194.1 / 2429.2 / 2846.1 / 0 / 190 / 693 |
| 128 | n/a | n/a | 53 / 2224.1 / 5145.5 / 6709.8 / 0 / 203 / 4911 | n/a | 41 / 2899.9 / 5838.4 / 7110.7 / 0 / 194 / 4400 | 50 / 2382.7 / 5143.3 / 6403.5 / 0 / 203 / 808 |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | none | none | 1 | none | 1 | 1 |

### Mixed load: 32 ADBC small-query clients alone / with 2 heavy SF10 streams (q01, q18)

| metric | ours-new | ours-27f5 | up-native | up-main | 843e4ad5b610 | 843e4ad5b610 -DresourceProfile=speed |
|---|---|---|---|---|---|---|
| small QPS alone | n/a | n/a | n/a | n/a | n/a | n/a |
| small QPS with heavy | n/a | n/a | n/a | n/a | n/a | n/a |
| small p95 ms alone | n/a | n/a | n/a | n/a | n/a | n/a |
| small p95 ms with heavy | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy q01 s (median of runs during the window) | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy q18 s | n/a | n/a | n/a | n/a | n/a | n/a |
| small errors alone / with heavy; heavy failures or wrong answers | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 |

### 4 heavy SF10 queries at once (q01 q09 q18 q21, ADBC) and network-limited client path (netem 10 ms RTT, 1 Gbit/s)

| metric | ours-new | ours-27f5 | up-native | up-main | 843e4ad5b610 | 843e4ad5b610 -DresourceProfile=speed |
|---|---|---|---|---|---|---|
| heavy x4: slowest query s (n/a if any failed) | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy x4: failed or wrong (all rounds) | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy x4: server peak RSS MiB | n/a | n/a | n/a | n/a | n/a | n/a |
| netem: SF10 TPC-H ADBC, sum of warm medians s (correct queries) | n/a | n/a | n/a | n/a | n/a | n/a |
| netem: full lineitem export over ADBC, MB/s | n/a | n/a | n/a | n/a | n/a | n/a |

Not in this run: up-native with its ZSTD Flight compression on the netem path (job `new-vs-native-zstd-netem`).

Not yet in this report: TLS + token on/off for ours.

