# Server comparison - Report 2: LOAD (compare run 41029626461)

## Setup

| item | value |
|---|---|
| runner | GitHub-hosted `ubuntu-latest`: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor; Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor; Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor; RAM 15983 MB |
| containers | every server: `eclipse-temurin:21-jre`, `--cpus=2 --cpuset-cpus=0,1 --memory=6g --memory-swap=6g`, JVM `-Xmx3g -XX:MaxDirectMemorySize=2g`, `MALLOC_ARENA_MAX=4`; load generators in their own container on cpus 2,3 (so the client side has 2 cores too: at 64/128 clients the client can be the limit, see client notes) |
| servers | ours-new = `7562a5bdb7b9`; ours-27f5 = `27f583adccd7`; up-native = `9fb08d9dd24df3cb838a3172f9375560bb6dc70a`; up-main = `dbacd8d585bce2ef2a449c821fe3a53cc6060b57` |
| data | TPC-H SF10 Parquet on local disk (load, mixed, heavy, netem) |
| pairs | ours-new (side A) vs one other server (side B) on the same runner, rounds A B / B A / A B |
| load mix | `point_orders`, `point_lineitem`, `count_filter` (every server answers them; upstream has no JDBC prepared statements) |
| settings | `def` = each server's default `duckDbThreads` (ours 4, upstream 2); `t8` = 8 on both; `zstd` = netem path only, up-native with its ZSTD batch compression (`-DflightCompression=zstd`, decoded by ADBC) vs ours plain (up-main has no such option) |

## Setting `def`

### Closed-loop load, JDBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main | d752a7358a65 | d752a7358a65 -DresourceProfile=speed | d752a7358a65 CZSTD | d752a7358a65 CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| 1 | n/a | n/a | 55 / 15.9 / 30.2 / 45.3 / 0 / 157 / 470 | n/a | 65 / 12.9 / 25.4 / 32.9 / 0 / 165 / 387 | 65 / 12.6 / 24.9 / 33.4 / 0 / 164 / 387 | n/a | n/a |
| 8 | n/a | n/a | 81 / 92.2 / 190.8 / 214.6 / 0 / 190 / 825 | n/a | 72 / 108.3 / 194.9 / 221.1 / 0 / 185 / 805 | 80 / 93.0 / 198.0 / 218.8 / 0 / 191 / 654 | n/a | n/a |
| 32 | n/a | n/a | 85 / 335.3 / 722.7 / 833.3 / 0 / 202 / 1802 | n/a | 72 / 421.0 / 820.2 / 1082.4 / 0 / 194 / 1705 | 81 / 366.0 / 748.3 / 883.1 / 0 / 199 / 1490 | n/a | n/a |
| 64 | n/a | n/a | 85 / 682.0 / 1511.6 / 1853.1 / 0 / 191 / 2915 | n/a | 68 / 890.6 / 1905.1 / 2645.3 / 0 / 196 / 2899 | 78 / 764.6 / 1709.6 / 2289.3 / 0 / 195 / 2372 | n/a | n/a |
| 128 | n/a | n/a | 81 / 1407.9 / 3559.3 / 4567.1 / 0 / 194 / 4173 | n/a | 64 / 1831.9 / 4353.3 / 5652.2 / 0 / 185 / 4386 | 78 / 1437.7 / 3765.4 / 4984.4 / 0 / 184 / 3613 | n/a | n/a |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | none | none | 1 | none | 1 | 1 | none | none |

### Closed-loop load, ADBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main | d752a7358a65 | d752a7358a65 -DresourceProfile=speed | d752a7358a65 CZSTD | d752a7358a65 CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| 1 | n/a | n/a | 65 / 13.6 / 24.2 / 33.8 / 0 / 162 / 474 | n/a | 67 / 12.8 / 23.8 / 29.9 / 0 / 163 / 417 | 66 / 12.7 / 23.7 / 30.0 / 0 / 163 / 369 | n/a | n/a |
| 8 | n/a | n/a | 87 / 86.8 / 179.9 / 200.7 / 0 / 199 / 900 | n/a | 74 / 107.4 / 193.8 / 220.5 / 0 / 196 / 800 | 79 / 96.8 / 195.5 / 216.9 / 0 / 197 / 700 | n/a | n/a |
| 32 | n/a | n/a | 86 / 332.6 / 714.1 / 812.4 / 0 / 200 / 1895 | n/a | 67 / 456.0 / 870.7 / 1135.4 / 0 / 200 / 1737 | 78 / 390.1 / 762.3 / 955.7 / 0 / 194 / 1496 | n/a | n/a |
| 64 | n/a | n/a | 84 / 693.4 / 1564.2 / 1885.9 / 0 / 202 / 3020 | n/a | 65 / 935.2 / 1958.3 / 2852.9 / 0 / 196 / 3067 | 78 / 753.2 / 1707.1 / 2469.9 / 0 / 198 / 2398 | n/a | n/a |
| 128 | n/a | n/a | 81 / 1408.4 / 3558.7 / 4538.6 / 0 / 201 / 4852 | n/a | 63 / 1819.2 / 4341.4 / 6079.4 / 0 / 196 / 5059 | 73 / 1538.2 / 4025.9 / 5764.3 / 0 / 195 / 4095 | n/a | n/a |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | none | none | 1 | none | 1 | 1 | none | none |

### Mixed load: 32 ADBC small-query clients alone / with 2 heavy SF10 streams (q01, q18)

| metric | ours-new | ours-27f5 | up-native | up-main | d752a7358a65 | d752a7358a65 -DresourceProfile=speed | d752a7358a65 CZSTD | d752a7358a65 CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| small QPS alone | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small QPS with heavy | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small p95 ms alone | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small p95 ms with heavy | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy q01 s (median of runs during the window) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy q18 s | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small errors alone / with heavy; heavy failures or wrong answers | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 |

### 4 heavy SF10 queries at once (q01 q09 q18 q21, ADBC) and network-limited client path (netem 10 ms RTT, 1 Gbit/s)

| metric | ours-new | ours-27f5 | up-native | up-main | d752a7358a65 | d752a7358a65 -DresourceProfile=speed | d752a7358a65 CZSTD | d752a7358a65 CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| heavy x4: slowest query s (n/a if any failed) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy x4: failed or wrong (all rounds) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy x4: server peak RSS MiB | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| netem: SF10 TPC-H ADBC, sum of warm medians s (correct queries) | n/a | n/a | 0.0 (0/22 q) | n/a | n/a | n/a | 42.0 (22/22 q) | 41.3 (22/22 q) |
| netem: full lineitem export over ADBC, MB/s | n/a | n/a | 259 | n/a | n/a | n/a | 260 | 260 |

## Netem pairs per job (both sides on the same runner; medians over rounds, B / A per round)

| job | A | B | TPC-H SF10 ADBC s A | B | B / A | export MB/s A | B | B / A | per-round export B / A | queries not ok A / B |
|---|---|---|---|---|---|---|---|---|---|---|
| i23-zstd-netem-local | d752a7358a65 CZSTD | d752a7358a65 CZSTD -DresourceProfile=speed CZSTD | 42.3 | 41.3 | 0.98 | 259 | 260 | 1.00 | 0.99 1.01 1.02 | 0 / 0 |
| i23-zstd-netem-local-vs-up-native | up-native | d752a7358a65 CZSTD | n/a | 41.3 | n/a | 259 | 260 | 1.01 | 1.01 0.99 1.02 | 22 / 0 |

TPC-H n/a = not all 22 queries answered correctly in a round (see 'queries not ok', max over rounds).

Not in this run: up-native with its ZSTD Flight compression on the netem path (job `new-vs-native-zstd-netem`).

Not yet in this report: TLS + token on/off for ours.

