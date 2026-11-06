# Server comparison - Report 2: LOAD (compare run 42223833724)

## Setup

| item | value |
|---|---|
| runner | GitHub-hosted `ubuntu-latest`: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor; Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor; Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor; Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C; RAM 15983 MB |
| containers | every server: `eclipse-temurin:21-jre`, `--cpus=2 --cpuset-cpus=0,1 --memory=6g --memory-swap=6g`, JVM `-Xmx3g -XX:MaxDirectMemorySize=2g`, `MALLOC_ARENA_MAX=4`; load generators in their own container on cpus 2,3 (so the client side has 2 cores too: at 64/128 clients the client can be the limit, see client notes) |
| servers | ours-new = `7562a5bdb7b9`; ours-27f5 = `27f583adccd7`; up-native = `9e4787906b07b6ecee80167ad3a0a2f0022d0ff3`; up-main = `dbacd8d585bce2ef2a449c821fe3a53cc6060b57` |
| data | TPC-H SF10 Parquet on local disk (load, mixed, heavy, netem) |
| pairs | ours-new (side A) vs one other server (side B) on the same runner, rounds A B / B A / A B |
| load mix | `point_orders`, `point_lineitem`, `count_filter` (every server answers them; upstream has no JDBC prepared statements) |
| settings | `def` = each server's default `duckDbThreads` (ours 4, upstream 2); `t8` = 8 on both; `zstd` = netem path only, up-native with its ZSTD batch compression (`-DflightCompression=zstd`, decoded by ADBC) vs ours plain (up-main has no such option) |

## Setting `def`

### Closed-loop load, JDBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main | deafc861cce3 | deafc861cce3 -DresourceProfile=speed | deafc861cce3 CZSTD | deafc861cce3 CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| 1 | n/a | n/a | 39 / 21.2 / 46.2 / 67.9 / 0 / 163 / 437 | n/a | 41 / 19.9 / 42.1 / 53.9 / 0 / 167 / 397 | 42 / 19.6 / 40.8 / 53.1 / 0 / 169 / 390 | n/a | n/a |
| 8 | n/a | n/a | 53 / 137.8 / 306.4 / 335.5 / 0 / 199 / 447 | n/a | 46 / 171.4 / 312.4 / 362.5 / 0 / 198 / 770 | 50 / 152.6 / 344.8 / 395.3 / 0 / 200 / 479 | n/a | n/a |
| 32 | n/a | n/a | 54 / 517.8 / 1144.0 / 1246.4 / 0 / 191 / 550 | n/a | 46 / 652.2 / 1279.6 / 1715.4 / 0 / 196 / 1617 | 51 / 544.0 / 1239.0 / 1401.8 / 0 / 197 / 588 | n/a | n/a |
| 64 | n/a | n/a | 54 / 1071.7 / 2335.6 / 2754.6 / 0 / 192 / 691 | n/a | 45 / 1352.3 / 2693.6 / 3324.0 / 0 / 188 / 2503 | 51 / 1174.9 / 2406.2 / 2856.8 / 0 / 193 / 720 | n/a | n/a |
| 128 | n/a | n/a | 54 / 2157.9 / 4805.7 / 5965.4 / 0 / 193 / 917 | n/a | 43 / 2711.7 / 5837.6 / 7548.1 / 0 / 188 / 3949 | 52 / 2281.5 / 5174.1 / 6416.9 / 0 / 186 / 886 | n/a | n/a |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | none | none | 1 | none | 1 | 1 | none | none |

### Closed-loop load, ADBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main | deafc861cce3 | deafc861cce3 -DresourceProfile=speed | deafc861cce3 CZSTD | deafc861cce3 CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| 1 | n/a | n/a | 45 / 17.8 / 35.8 / 59.4 / 0 / 165 / 412 | n/a | 42 / 19.7 / 38.3 / 49.4 / 0 / 163 / 418 | 43 / 19.3 / 37.5 / 49.1 / 0 / 162 / 418 | n/a | n/a |
| 8 | n/a | n/a | 56 / 130.0 / 293.6 / 320.8 / 0 / 197 / 444 | n/a | 47 / 170.8 / 314.6 / 364.1 / 0 / 191 / 800 | 50 / 155.0 / 339.4 / 384.7 / 0 / 191 / 534 | n/a | n/a |
| 32 | n/a | n/a | 56 / 504.8 / 1125.5 / 1269.5 / 0 / 203 / 603 | n/a | 45 / 660.1 / 1287.7 / 1695.4 / 0 / 193 / 1686 | 51 / 560.2 / 1234.6 / 1385.5 / 0 / 193 / 597 | n/a | n/a |
| 64 | n/a | n/a | 56 / 1052.5 / 2280.2 / 2698.0 / 0 / 200 / 743 | n/a | 45 / 1340.9 / 2656.7 / 3414.1 / 0 / 196 / 2875 | 52 / 1140.1 / 2402.1 / 2816.6 / 0 / 202 / 747 | n/a | n/a |
| 128 | n/a | n/a | 55 / 2166.7 / 4764.1 / 5957.8 / 0 / 193 / 1004 | n/a | 43 / 2777.7 / 5772.9 / 6977.2 / 0 / 195 / 4477 | 52 / 2280.8 / 5032.6 / 6303.5 / 0 / 201 / 922 | n/a | n/a |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | none | none | 1 | none | 1 | 1 | none | none |

### Mixed load: 32 ADBC small-query clients alone / with 2 heavy SF10 streams (q01, q18)

| metric | ours-new | ours-27f5 | up-native | up-main | deafc861cce3 | deafc861cce3 -DresourceProfile=speed | deafc861cce3 CZSTD | deafc861cce3 CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| small QPS alone | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small QPS with heavy | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small p95 ms alone | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small p95 ms with heavy | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy q01 s (median of runs during the window) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy q18 s | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small errors alone / with heavy; heavy failures or wrong answers | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 |

### 4 heavy SF10 queries at once (q01 q09 q18 q21, ADBC) and network-limited client path (netem 10 ms RTT, 1 Gbit/s)

| metric | ours-new | ours-27f5 | up-native | up-main | deafc861cce3 | deafc861cce3 -DresourceProfile=speed | deafc861cce3 CZSTD | deafc861cce3 CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| heavy x4: slowest query s (n/a if any failed) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy x4: failed or wrong (all rounds) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy x4: server peak RSS MiB | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| netem: SF10 TPC-H ADBC, sum of warm medians s (correct queries) | n/a | n/a | 0.0 (0/22 q) | n/a | n/a | n/a | 40.7 (22/22 q) | 39.5 (22/22 q) |
| netem: full lineitem export over ADBC, MB/s | n/a | n/a | 263 | n/a | n/a | n/a | 254 | 255 |

## Netem pairs per job (both sides on the same runner; medians over rounds, B / A per round)

| job | A | B | TPC-H SF10 ADBC s A | B | B / A | export MB/s A | B | B / A | per-round export B / A | queries not ok A / B |
|---|---|---|---|---|---|---|---|---|---|---|
| fu-zstd-netem-local | deafc861cce3 CZSTD | deafc861cce3 CZSTD -DresourceProfile=speed CZSTD | 41.5 | 39.5 | 0.95 | 254 | 255 | 1.00 | 0.99 1.02 1.00 | 0 / 0 |
| fu-zstd-netem-local-vs-up-native | up-native | deafc861cce3 CZSTD | n/a | 39.5 | n/a | 263 | 255 | 0.97 | 0.95 0.99 0.98 | 22 / 0 |

TPC-H n/a = not all 22 queries answered correctly in a round (see 'queries not ok', max over rounds).

Not in this run: up-native with its ZSTD Flight compression on the netem path (job `new-vs-native-zstd-netem`).

Not yet in this report: TLS + token on/off for ours.

