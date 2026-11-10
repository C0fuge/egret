# Server comparison - Report 2: LOAD (compare run 42865250390)

## Setup

| item | value |
|---|---|
| runner | GitHub-hosted `ubuntu-latest`: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor; Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor; Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor; RAM 15983 MB |
| containers | every server: `eclipse-temurin:21-jre`, `--cpus=2 --cpuset-cpus=0,1 --memory=6g --memory-swap=6g`, JVM `-Xmx3g -XX:MaxDirectMemorySize=2g`, `MALLOC_ARENA_MAX=4`; load generators in their own container on cpus 2,3 (so the client side has 2 cores too: at 64/128 clients the client can be the limit, see client notes) |
| servers | ours-new = `7562a5bdb7b9`; ours-27f5 = `27f583adccd7`; up-native = `0ecca4f9b01e47c5be13e0add79afe4f77b3776f`; up-main = `dbacd8d585bce2ef2a449c821fe3a53cc6060b57` |
| data | TPC-H SF10 Parquet on local disk (load, mixed, heavy, netem) |
| pairs | ours-new (side A) vs one other server (side B) on the same runner, rounds A B / B A / A B |
| load mix | `point_orders`, `point_lineitem`, `count_filter` (every server answers them; upstream has no JDBC prepared statements) |
| settings | `def` = each server's default `duckDbThreads` (ours 4, upstream 2); `t8` = 8 on both; `zstd` = netem path only, up-native with its ZSTD batch compression (`-DflightCompression=zstd`, decoded by ADBC) vs ours plain (up-main has no such option) |

## Setting `def`

### Closed-loop load, JDBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main | 2ff221447b5d | 2ff221447b5d -DresourceProfile=speed | 2ff221447b5d CZSTD | 2ff221447b5d CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| 1 | n/a | n/a | 38 / 21.9 / 47.2 / 67.5 / 0 / 160 / 421 | n/a | 40 / 20.1 / 43.5 / 55.3 / 0 / 167 / 464 | 41 / 20.1 / 43.3 / 55.4 / 0 / 168 / 464 | n/a | n/a |
| 8 | n/a | n/a | 51 / 144.9 / 317.0 / 342.1 / 0 / 197 / 440 | n/a | 48 / 165.1 / 306.5 / 353.5 / 0 / 198 / 839 | 51 / 149.0 / 339.0 / 384.7 / 0 / 199 / 557 | n/a | n/a |
| 32 | n/a | n/a | 53 / 521.6 / 1166.3 / 1288.9 / 0 / 193 / 535 | n/a | 47 / 634.8 / 1238.1 / 1420.6 / 0 / 194 / 1715 | 52 / 535.4 / 1212.9 / 1340.2 / 0 / 200 / 633 | n/a | n/a |
| 64 | n/a | n/a | 54 / 1094.0 / 2318.9 / 2701.2 / 0 / 193 / 762 | n/a | 46 / 1308.4 / 2612.0 / 3121.0 / 0 / 198 / 2530 | 53 / 1114.4 / 2397.3 / 2768.5 / 0 / 202 / 806 | n/a | n/a |
| 128 | n/a | n/a | 53 / 2167.0 / 4863.2 / 5980.7 / 0 / 193 / 971 | n/a | 44 / 2650.9 / 5602.1 / 7050.0 / 0 / 189 / 4007 | 51 / 2258.8 / 5018.4 / 6290.1 / 0 / 188 / 845 | n/a | n/a |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | none | none | 1 | none | 1 | 1 | none | none |

### Closed-loop load, ADBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main | 2ff221447b5d | 2ff221447b5d -DresourceProfile=speed | 2ff221447b5d CZSTD | 2ff221447b5d CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| 1 | n/a | n/a | 43 / 18.7 / 37.0 / 64.6 / 0 / 167 / 408 | n/a | 42 / 19.6 / 38.6 / 51.3 / 0 / 164 / 516 | 43 / 19.4 / 37.8 / 48.3 / 0 / 164 / 468 | n/a | n/a |
| 8 | n/a | n/a | 55 / 132.9 / 298.1 / 326.1 / 0 / 198 / 455 | n/a | 48 / 163.7 / 304.9 / 345.5 / 0 / 198 / 837 | 52 / 147.7 / 333.1 / 375.9 / 0 / 198 / 578 | n/a | n/a |
| 32 | n/a | n/a | 55 / 504.5 / 1139.2 / 1246.4 / 0 / 203 / 594 | n/a | 46 / 645.8 / 1269.3 / 1484.7 / 0 / 193 / 1776 | 52 / 535.1 / 1224.2 / 1366.5 / 0 / 193 / 708 | n/a | n/a |
| 64 | n/a | n/a | 55 / 1057.8 / 2300.0 / 2693.8 / 0 / 203 / 782 | n/a | 46 / 1324.8 / 2587.6 / 3087.6 / 0 / 196 / 2906 | 52 / 1116.6 / 2365.5 / 2738.4 / 0 / 197 / 768 | n/a | n/a |
| 128 | n/a | n/a | 54 / 2172.3 / 4882.2 / 6112.7 / 0 / 199 / 970 | n/a | 43 / 2730.4 / 5696.9 / 7105.4 / 0 / 199 / 4624 | 51 / 2293.7 / 5066.0 / 6427.8 / 0 / 202 / 864 | n/a | n/a |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | none | none | 1 | none | 1 | 1 | none | none |

### Mixed load: 32 ADBC small-query clients alone / with 2 heavy SF10 streams (q01, q18)

| metric | ours-new | ours-27f5 | up-native | up-main | 2ff221447b5d | 2ff221447b5d -DresourceProfile=speed | 2ff221447b5d CZSTD | 2ff221447b5d CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| small QPS alone | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small QPS with heavy | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small p95 ms alone | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small p95 ms with heavy | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy q01 s (median of runs during the window) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy q18 s | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small errors alone / with heavy; heavy failures or wrong answers | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 |

### 4 heavy SF10 queries at once (q01 q09 q18 q21, ADBC) and network-limited client path (netem 10 ms RTT, 1 Gbit/s)

| metric | ours-new | ours-27f5 | up-native | up-main | 2ff221447b5d | 2ff221447b5d -DresourceProfile=speed | 2ff221447b5d CZSTD | 2ff221447b5d CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| heavy x4: slowest query s (n/a if any failed) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy x4: failed or wrong (all rounds) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy x4: server peak RSS MiB | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| netem: SF10 TPC-H ADBC, sum of warm medians s (correct queries) | n/a | n/a | 0.0 (0/22 q) | n/a | n/a | n/a | 41.8 (19/22 q) | 40.7 (22/22 q) |
| netem: full lineitem export over ADBC, MB/s | n/a | n/a | 262 | n/a | n/a | n/a | 258 | 259 |

## Netem pairs per job (both sides on the same runner; medians over rounds, B / A per round)

| job | A | B | TPC-H SF10 ADBC s A | B | B / A | export MB/s A | B | B / A | per-round export B / A | queries not ok A / B |
|---|---|---|---|---|---|---|---|---|---|---|
| fu-zstd-netem-local | 2ff221447b5d CZSTD | 2ff221447b5d CZSTD -DresourceProfile=speed CZSTD | n/a | 40.7 | n/a | 255 | 259 | 1.02 | 1.04 1.02 0.98 | 3 / 0 |
| fu-zstd-netem-local-vs-up-native | up-native | 2ff221447b5d CZSTD | n/a | 40.7 | n/a | 262 | 259 | 0.99 | 0.99 0.99 0.99 | 22 / 0 |

TPC-H n/a = not all 22 queries answered correctly in a round (see 'queries not ok', max over rounds).

Not in this run: up-native with its ZSTD Flight compression on the netem path (job `new-vs-native-zstd-netem`).

Not yet in this report: TLS + token on/off for ours.

