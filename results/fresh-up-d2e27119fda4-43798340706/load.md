# Server comparison - Report 2: LOAD (compare run 43798340706)

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

| clients | ours-new | ours-27f5 | up-native | up-main | d2e27119fda4 | d2e27119fda4 -DresourceProfile=speed | d2e27119fda4 CZSTD | d2e27119fda4 CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| 1 | n/a | n/a | 49 / 16.6 / 36.2 / 54.7 / 0 / 166 / 676 | n/a | 54 / 14.7 / 31.6 / 42.4 / 0 / 172 / 426 | 54 / 14.6 / 31.7 / 42.4 / 0 / 172 / 410 | n/a | n/a |
| 8 | n/a | n/a | 66 / 107.0 / 244.2 / 270.4 / 0 / 197 / 447 | n/a | 62 / 127.4 / 241.6 / 277.3 / 0 / 181 / 822 | 66 / 112.4 / 264.3 / 298.4 / 0 / 181 / 524 | n/a | n/a |
| 32 | n/a | n/a | 68 / 398.2 / 927.0 / 1055.5 / 0 / 192 / 574 | n/a | 60 / 497.0 / 995.1 / 1179.0 / 0 / 191 / 1662 | 67 / 419.6 / 958.9 / 1063.0 / 0 / 191 / 579 | n/a | n/a |
| 64 | n/a | n/a | 69 / 814.7 / 1892.1 / 2221.0 / 0 / 189 / 747 | n/a | 58 / 1017.2 / 2087.1 / 2565.4 / 0 / 187 / 2656 | 66 / 868.8 / 1918.5 / 2277.6 / 0 / 182 / 676 | n/a | n/a |
| 128 | n/a | n/a | 68 / 1708.2 / 4060.1 / 5038.4 / 0 / 200 / 945 | n/a | 56 / 2147.4 / 4674.4 / 5833.6 / 0 / 189 / 4204 | 66 / 1782.7 / 4154.9 / 5197.7 / 0 / 190 / 839 | n/a | n/a |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | none | none | 1 | none | 1 | 1 | none | none |

### Closed-loop load, ADBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main | d2e27119fda4 | d2e27119fda4 -DresourceProfile=speed | d2e27119fda4 CZSTD | d2e27119fda4 CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| 1 | n/a | n/a | 57 / 14.3 / 27.9 / 50.1 / 0 / 161 / 653 | n/a | 56 / 14.6 / 29.3 / 38.6 / 0 / 164 / 432 | 56 / 14.5 / 29.2 / 39.0 / 0 / 161 / 414 | n/a | n/a |
| 8 | n/a | n/a | 71 / 100.1 / 232.3 / 252.5 / 0 / 203 / 434 | n/a | 62 / 126.8 / 241.4 / 281.5 / 0 / 202 / 822 | 68 / 111.5 / 260.4 / 294.1 / 0 / 202 / 536 | n/a | n/a |
| 32 | n/a | n/a | 70 / 384.4 / 907.9 / 1015.6 / 0 / 193 / 639 | n/a | 59 / 501.1 / 1017.0 / 1197.9 / 0 / 202 / 1754 | 67 / 415.5 / 955.4 / 1084.0 / 0 / 203 / 593 | n/a | n/a |
| 64 | n/a | n/a | 70 / 813.8 / 1893.1 / 2225.5 / 0 / 193 / 822 | n/a | 57 / 1041.5 / 2181.0 / 2702.1 / 0 / 202 / 2943 | 66 / 896.8 / 1911.9 / 2284.8 / 0 / 203 / 725 | n/a | n/a |
| 128 | n/a | n/a | 68 / 1698.7 / 4002.6 / 5134.4 / 0 / 203 / 945 | n/a | 55 / 2137.2 / 4682.1 / 6000.0 / 0 / 202 / 4875 | 65 / 1776.2 / 4186.2 / 5192.5 / 0 / 202 / 836 | n/a | n/a |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | none | none | 1 | none | 1 | 1 | none | none |

### Mixed load: 32 ADBC small-query clients alone / with 2 heavy SF10 streams (q01, q18)

| metric | ours-new | ours-27f5 | up-native | up-main | d2e27119fda4 | d2e27119fda4 -DresourceProfile=speed | d2e27119fda4 CZSTD | d2e27119fda4 CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| small QPS alone | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small QPS with heavy | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small p95 ms alone | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small p95 ms with heavy | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy q01 s (median of runs during the window) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy q18 s | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small errors alone / with heavy; heavy failures or wrong answers | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 |

### 4 heavy SF10 queries at once (q01 q09 q18 q21, ADBC) and network-limited client path (netem 10 ms RTT, 1 Gbit/s)

| metric | ours-new | ours-27f5 | up-native | up-main | d2e27119fda4 | d2e27119fda4 -DresourceProfile=speed | d2e27119fda4 CZSTD | d2e27119fda4 CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| heavy x4: slowest query s (n/a if any failed) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy x4: failed or wrong (all rounds) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy x4: server peak RSS MiB | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| netem: SF10 TPC-H ADBC, sum of warm medians s (correct queries) | n/a | n/a | 0.0 (0/22 q) | n/a | n/a | n/a | 31.2 (22/22 q) | 30.9 (22/22 q) |
| netem: full lineitem export over ADBC, MB/s | n/a | n/a | 333 | n/a | n/a | n/a | 340 | 345 |

## Netem pairs per job (both sides on the same runner; medians over rounds, B / A per round)

| job | A | B | TPC-H SF10 ADBC s A | B | B / A | export MB/s A | B | B / A | per-round export B / A | queries not ok A / B |
|---|---|---|---|---|---|---|---|---|---|---|
| fu-zstd-netem-local | d2e27119fda4 CZSTD | d2e27119fda4 CZSTD -DresourceProfile=speed CZSTD | 31.6 | 30.9 | 0.98 | 329 | 345 | 1.05 | 1.01 1.07 1.03 | 0 / 0 |
| fu-zstd-netem-local-vs-up-native | up-native | d2e27119fda4 CZSTD | n/a | 30.9 | n/a | 333 | 345 | 1.04 | 1.05 1.05 1.02 | 22 / 0 |

TPC-H n/a = not all 22 queries answered correctly in a round (see 'queries not ok', max over rounds).

Not in this run: up-native with its ZSTD Flight compression on the netem path (job `new-vs-native-zstd-netem`).

Not yet in this report: TLS + token on/off for ours.

