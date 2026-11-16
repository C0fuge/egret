# Server comparison - Report 2: LOAD (compare run 43840086547)

## Setup

| item | value |
|---|---|
| runner | GitHub-hosted `ubuntu-latest`: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor; Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor; Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor; Linux ubuntu26 4 vCPU Intel(R) Xeon(R) 6973P-C; RAM 15983 MB |
| containers | every server: `eclipse-temurin:21-jre`, `--cpus=2 --cpuset-cpus=0,1 --memory=6g --memory-swap=6g`, JVM `-Xmx3g -XX:MaxDirectMemorySize=2g`, `MALLOC_ARENA_MAX=4`; load generators in their own container on cpus 2,3 (so the client side has 2 cores too: at 64/128 clients the client can be the limit, see client notes) |
| servers | ours-new = `7562a5bdb7b9`; ours-27f5 = `27f583adccd7`; up-native = `28d6ea713b8eb6377704ba85807ed7e433ae4869`; up-main = `dbacd8d585bce2ef2a449c821fe3a53cc6060b57` |
| data | TPC-H SF10 Parquet on local disk (load, mixed, heavy, netem) |
| pairs | ours-new (side A) vs one other server (side B) on the same runner, rounds A B / B A / A B |
| load mix | `point_orders`, `point_lineitem`, `count_filter` (every server answers them; upstream has no JDBC prepared statements) |
| settings | `def` = each server's default `duckDbThreads` (ours 4, upstream 2); `t8` = 8 on both; `zstd` = netem path only, up-native with its ZSTD batch compression (`-DflightCompression=zstd`, decoded by ADBC) vs ours plain (up-main has no such option) |

## Setting `def`

### Closed-loop load, JDBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main | 6f0aa5a026fa | 6f0aa5a026fa -DresourceProfile=speed | 6f0aa5a026fa CZSTD | 6f0aa5a026fa CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| 1 | n/a | n/a | 37 / 22.7 / 48.3 / 68.5 / 0 / 162 / 407 | n/a | 41 / 19.8 / 42.7 / 56.0 / 0 / 168 / 437 | 40 / 20.2 / 42.6 / 56.3 / 0 / 168 / 389 | n/a | n/a |
| 8 | n/a | n/a | 51 / 142.9 / 316.4 / 343.6 / 0 / 200 / 428 | n/a | 48 / 166.1 / 306.7 / 352.6 / 0 / 202 / 820 | 51 / 151.4 / 341.4 / 393.7 / 0 / 202 / 510 | n/a | n/a |
| 32 | n/a | n/a | 54 / 514.5 / 1147.9 / 1284.2 / 0 / 193 / 541 | n/a | 47 / 638.3 / 1238.1 / 1439.0 / 0 / 193 / 1617 | 52 / 536.2 / 1220.4 / 1340.7 / 0 / 192 / 579 | n/a | n/a |
| 64 | n/a | n/a | 53 / 1083.8 / 2342.2 / 2773.2 / 0 / 193 / 775 | n/a | 45 / 1321.3 / 2592.3 / 3180.4 / 0 / 190 / 2589 | 52 / 1127.4 / 2373.7 / 2820.3 / 0 / 192 / 725 | n/a | n/a |
| 128 | n/a | n/a | 52 / 2240.2 / 4831.1 / 5941.8 / 0 / 194 / 878 | n/a | 44 / 2718.9 / 5497.5 / 6949.1 / 0 / 189 / 3926 | 50 / 2301.7 / 5067.9 / 6327.8 / 0 / 190 / 942 | n/a | n/a |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | none | none | 1 | none | 1 | 1 | none | none |

### Closed-loop load, ADBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main | 6f0aa5a026fa | 6f0aa5a026fa -DresourceProfile=speed | 6f0aa5a026fa CZSTD | 6f0aa5a026fa CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| 1 | n/a | n/a | 43 / 18.9 / 37.6 / 64.9 / 0 / 164 / 400 | n/a | 43 / 19.2 / 38.0 / 51.1 / 0 / 161 / 444 | 43 / 19.1 / 37.6 / 51.6 / 0 / 161 / 425 | n/a | n/a |
| 8 | n/a | n/a | 55 / 133.5 / 297.0 / 328.4 / 0 / 198 / 461 | n/a | 48 / 164.9 / 306.0 / 358.2 / 0 / 192 / 856 | 51 / 149.8 / 333.3 / 382.0 / 0 / 192 / 506 | n/a | n/a |
| 32 | n/a | n/a | 55 / 510.5 / 1140.9 / 1254.5 / 0 / 204 / 601 | n/a | 46 / 651.3 / 1277.6 / 1459.0 / 0 / 200 / 1688 | 52 / 545.9 / 1217.7 / 1352.7 / 0 / 203 / 611 | n/a | n/a |
| 64 | n/a | n/a | 54 / 1087.3 / 2326.0 / 2759.9 / 0 / 203 / 753 | n/a | 45 / 1331.3 / 2627.7 / 3200.1 / 0 / 201 / 2810 | 52 / 1131.9 / 2391.5 / 2788.8 / 0 / 202 / 749 | n/a | n/a |
| 128 | n/a | n/a | 54 / 2214.2 / 4873.0 / 5941.8 / 0 / 193 / 870 | n/a | 43 / 2766.6 / 5636.8 / 7198.8 / 0 / 194 / 4510 | 51 / 2347.2 / 5000.3 / 6236.8 / 0 / 194 / 1027 | n/a | n/a |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | none | none | 1 | none | 1 | 1 | none | none |

### Mixed load: 32 ADBC small-query clients alone / with 2 heavy SF10 streams (q01, q18)

| metric | ours-new | ours-27f5 | up-native | up-main | 6f0aa5a026fa | 6f0aa5a026fa -DresourceProfile=speed | 6f0aa5a026fa CZSTD | 6f0aa5a026fa CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| small QPS alone | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small QPS with heavy | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small p95 ms alone | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small p95 ms with heavy | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy q01 s (median of runs during the window) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy q18 s | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small errors alone / with heavy; heavy failures or wrong answers | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 |

### 4 heavy SF10 queries at once (q01 q09 q18 q21, ADBC) and network-limited client path (netem 10 ms RTT, 1 Gbit/s)

| metric | ours-new | ours-27f5 | up-native | up-main | 6f0aa5a026fa | 6f0aa5a026fa -DresourceProfile=speed | 6f0aa5a026fa CZSTD | 6f0aa5a026fa CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| heavy x4: slowest query s (n/a if any failed) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy x4: failed or wrong (all rounds) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy x4: server peak RSS MiB | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| netem: SF10 TPC-H ADBC, sum of warm medians s (correct queries) | n/a | n/a | 0.0 (0/22 q) | n/a | n/a | n/a | 41.2 (22/22 q) | 39.6 (22/22 q) |
| netem: full lineitem export over ADBC, MB/s | n/a | n/a | 261 | n/a | n/a | n/a | 255 | 257 |

## Netem pairs per job (both sides on the same runner; medians over rounds, B / A per round)

| job | A | B | TPC-H SF10 ADBC s A | B | B / A | export MB/s A | B | B / A | per-round export B / A | queries not ok A / B |
|---|---|---|---|---|---|---|---|---|---|---|
| fu-zstd-netem-local | 6f0aa5a026fa CZSTD | 6f0aa5a026fa CZSTD -DresourceProfile=speed CZSTD | 41.9 | 39.6 | 0.95 | 254 | 257 | 1.01 | 1.04 0.97 0.99 | 0 / 0 |
| fu-zstd-netem-local-vs-up-native | up-native | 6f0aa5a026fa CZSTD | n/a | 39.6 | n/a | 261 | 257 | 0.98 | 0.99 0.95 0.98 | 22 / 0 |

TPC-H n/a = not all 22 queries answered correctly in a round (see 'queries not ok', max over rounds).

Not in this run: up-native with its ZSTD Flight compression on the netem path (job `new-vs-native-zstd-netem`).

Not yet in this report: TLS + token on/off for ours.

