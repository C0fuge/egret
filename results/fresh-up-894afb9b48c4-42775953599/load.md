# Server comparison - Report 2: LOAD (compare run 42775953599)

## Setup

| item | value |
|---|---|
| runner | GitHub-hosted `ubuntu-latest`: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor; Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor; Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor; Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C; RAM 15983 MB |
| containers | every server: `eclipse-temurin:21-jre`, `--cpus=2 --cpuset-cpus=0,1 --memory=6g --memory-swap=6g`, JVM `-Xmx3g -XX:MaxDirectMemorySize=2g`, `MALLOC_ARENA_MAX=4`; load generators in their own container on cpus 2,3 (so the client side has 2 cores too: at 64/128 clients the client can be the limit, see client notes) |
| servers | ours-new = `7562a5bdb7b9`; ours-27f5 = `27f583adccd7`; up-native = `cec626bbb54aabb64d9e4a12beca40b7fbfa3fa6`; up-main = `dbacd8d585bce2ef2a449c821fe3a53cc6060b57` |
| data | TPC-H SF10 Parquet on local disk (load, mixed, heavy, netem) |
| pairs | ours-new (side A) vs one other server (side B) on the same runner, rounds A B / B A / A B |
| load mix | `point_orders`, `point_lineitem`, `count_filter` (every server answers them; upstream has no JDBC prepared statements) |
| settings | `def` = each server's default `duckDbThreads` (ours 4, upstream 2); `t8` = 8 on both; `zstd` = netem path only, up-native with its ZSTD batch compression (`-DflightCompression=zstd`, decoded by ADBC) vs ours plain (up-main has no such option) |

## Setting `def`

### Closed-loop load, JDBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main | 894afb9b48c4 | 894afb9b48c4 -DresourceProfile=speed | 894afb9b48c4 CZSTD | 894afb9b48c4 CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| 1 | n/a | n/a | 64 / 13.0 / 27.2 / 42.0 / 0 / 161 / 420 | n/a | 65 / 13.0 / 26.3 / 33.8 / 0 / 167 / 482 | 65 / 12.9 / 26.3 / 34.0 / 0 / 167 / 476 | n/a | n/a |
| 8 | n/a | n/a | 87 / 84.2 / 183.2 / 205.0 / 0 / 187 / 520 | n/a | 76 / 102.9 / 186.3 / 218.3 / 0 / 183 / 858 | 84 / 91.5 / 190.1 / 224.6 / 0 / 188 / 561 | n/a | n/a |
| 32 | n/a | n/a | 89 / 311.5 / 706.4 / 798.6 / 0 / 203 / 639 | n/a | 74 / 402.9 / 813.2 / 959.5 / 0 / 197 / 1862 | 84 / 336.2 / 744.5 / 872.0 / 0 / 202 / 670 | n/a | n/a |
| 64 | n/a | n/a | 91 / 625.0 / 1453.5 / 1777.2 / 0 / 198 / 824 | n/a | 71 / 840.0 / 1739.2 / 2158.3 / 0 / 199 / 2917 | 84 / 691.1 / 1538.3 / 1899.0 / 0 / 200 / 758 | n/a | n/a |
| 128 | n/a | n/a | 85 / 1334.7 / 3289.2 / 4238.7 / 0 / 193 / 960 | n/a | 69 / 1714.9 / 3908.9 / 4907.6 / 0 / 188 / 4605 | 81 / 1426.2 / 3474.9 / 4478.0 / 0 / 186 / 978 | n/a | n/a |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | none | none | 1 | none | 1 | 1 | none | none |

### Closed-loop load, ADBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main | 894afb9b48c4 | 894afb9b48c4 -DresourceProfile=speed | 894afb9b48c4 CZSTD | 894afb9b48c4 CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| 1 | n/a | n/a | 75 / 11.1 / 21.6 / 30.9 / 0 / 167 / 399 | n/a | 70 / 12.3 / 23.1 / 28.7 / 0 / 165 / 478 | 71 / 12.2 / 22.6 / 28.4 / 0 / 165 / 452 | n/a | n/a |
| 8 | n/a | n/a | 89 / 81.2 / 178.8 / 197.3 / 0 / 202 / 509 | n/a | 77 / 102.5 / 184.6 / 214.8 / 0 / 200 / 971 | 87 / 89.2 / 185.9 / 217.6 / 0 / 198 / 547 | n/a | n/a |
| 32 | n/a | n/a | 91 / 306.6 / 705.8 / 806.0 / 0 / 201 / 663 | n/a | 72 / 410.6 / 847.2 / 985.0 / 0 / 199 / 1933 | 85 / 342.3 / 728.3 / 831.1 / 0 / 201 / 655 | n/a | n/a |
| 64 | n/a | n/a | 91 / 630.1 / 1465.6 / 1793.5 / 0 / 204 / 881 | n/a | 70 / 859.7 / 1802.0 / 2260.7 / 0 / 200 / 3239 | 84 / 706.8 / 1538.1 / 1927.3 / 0 / 195 / 797 | n/a | n/a |
| 128 | n/a | n/a | 85 / 1324.1 / 3315.9 / 4371.6 / 1 (connect t78: OperationalError: IO: [Flight SQL] failed to up) / 203 / 970 | n/a | 67 / 1761.7 / 3914.7 / 4968.0 / 0 / 195 / 5341 | 83 / 1370.0 / 3473.6 / 4461.7 / 0 / 198 / 982 | n/a | n/a |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | none | none | 1 | none | 1 | 1 | none | none |

### Mixed load: 32 ADBC small-query clients alone / with 2 heavy SF10 streams (q01, q18)

| metric | ours-new | ours-27f5 | up-native | up-main | 894afb9b48c4 | 894afb9b48c4 -DresourceProfile=speed | 894afb9b48c4 CZSTD | 894afb9b48c4 CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| small QPS alone | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small QPS with heavy | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small p95 ms alone | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small p95 ms with heavy | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy q01 s (median of runs during the window) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy q18 s | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small errors alone / with heavy; heavy failures or wrong answers | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 |

### 4 heavy SF10 queries at once (q01 q09 q18 q21, ADBC) and network-limited client path (netem 10 ms RTT, 1 Gbit/s)

| metric | ours-new | ours-27f5 | up-native | up-main | 894afb9b48c4 | 894afb9b48c4 -DresourceProfile=speed | 894afb9b48c4 CZSTD | 894afb9b48c4 CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| heavy x4: slowest query s (n/a if any failed) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy x4: failed or wrong (all rounds) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy x4: server peak RSS MiB | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| netem: SF10 TPC-H ADBC, sum of warm medians s (correct queries) | n/a | n/a | 0.0 (0/22 q) | n/a | n/a | n/a | 42.6 (22/22 q) | 41.9 (22/22 q) |
| netem: full lineitem export over ADBC, MB/s | n/a | n/a | 258 | n/a | n/a | n/a | 253 | 254 |

## Netem pairs per job (both sides on the same runner; medians over rounds, B / A per round)

| job | A | B | TPC-H SF10 ADBC s A | B | B / A | export MB/s A | B | B / A | per-round export B / A | queries not ok A / B |
|---|---|---|---|---|---|---|---|---|---|---|
| fu-zstd-netem-local | 894afb9b48c4 CZSTD | 894afb9b48c4 CZSTD -DresourceProfile=speed CZSTD | 43.0 | 41.9 | 0.97 | 252 | 254 | 1.01 | 1.01 1.08 0.94 | 0 / 0 |
| fu-zstd-netem-local-vs-up-native | up-native | 894afb9b48c4 CZSTD | n/a | 41.9 | n/a | 258 | 254 | 0.99 | 0.98 1.04 0.94 | 22 / 0 |

TPC-H n/a = not all 22 queries answered correctly in a round (see 'queries not ok', max over rounds).

Not in this run: up-native with its ZSTD Flight compression on the netem path (job `new-vs-native-zstd-netem`).

Not yet in this report: TLS + token on/off for ours.

