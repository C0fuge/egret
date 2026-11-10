# Server comparison - Report 2: LOAD (compare run 42888240521)

## Setup

| item | value |
|---|---|
| runner | GitHub-hosted `ubuntu-latest`: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor; Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor; Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor; Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C; Linux ubuntu26 4 vCPU Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz; RAM 15982 MB |
| containers | every server: `eclipse-temurin:21-jre`, `--cpus=2 --cpuset-cpus=0,1 --memory=6g --memory-swap=6g`, JVM `-Xmx3g -XX:MaxDirectMemorySize=2g`, `MALLOC_ARENA_MAX=4`; load generators in their own container on cpus 2,3 (so the client side has 2 cores too: at 64/128 clients the client can be the limit, see client notes) |
| servers | ours-new = `7562a5bdb7b9`; ours-27f5 = `27f583adccd7`; up-native = `0ecca4f9b01e47c5be13e0add79afe4f77b3776f`; up-main = `dbacd8d585bce2ef2a449c821fe3a53cc6060b57` |
| data | TPC-H SF10 Parquet on local disk (load, mixed, heavy, netem) |
| pairs | ours-new (side A) vs one other server (side B) on the same runner, rounds A B / B A / A B |
| load mix | `point_orders`, `point_lineitem`, `count_filter` (every server answers them; upstream has no JDBC prepared statements) |
| settings | `def` = each server's default `duckDbThreads` (ours 4, upstream 2); `t8` = 8 on both; `zstd` = netem path only, up-native with its ZSTD batch compression (`-DflightCompression=zstd`, decoded by ADBC) vs ours plain (up-main has no such option) |

## Setting `def`

### Closed-loop load, JDBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main | 2ff221447b5d | 2ff221447b5d -DresourceProfile=speed | 2ff221447b5d CZSTD | 2ff221447b5d CZSTD -DresourceProfile=speed CZSTD | gizmo |
|---|---|---|---|---|---|---|---|---|---|
| 1 | n/a | n/a | n/a | n/a | 47 / 17.2 / 37.2 / 50.2 / 0 / 169 / 478 | 47 / 17.2 / 36.8 / 50.7 / 0 / 169 / 434 | n/a | n/a | 54 / 15.5 / 31.2 / 32.8 / 0 / 157 / 78 |
| 8 | n/a | n/a | n/a | n/a | 55 / 141.4 / 269.8 / 310.7 / 0 / 201 / 878 | 59 / 126.6 / 300.9 / 342.6 / 0 / 201 / 554 | n/a | n/a | 61 / 115.0 / 268.0 / 287.8 / 0 / 183 / 151 |
| 32 | n/a | n/a | n/a | n/a | 54 / 544.7 / 1097.1 / 1266.6 / 0 / 193 / 1720 | 60 / 456.2 / 1078.7 / 1209.1 / 0 / 191 / 616 | n/a | n/a | 60 / 447.1 / 1001.5 / 1099.0 / 0 / 189 / 240 |
| 64 | n/a | n/a | n/a | n/a | 52 / 1139.9 / 2281.1 / 2849.5 / 0 / 189 / 2568 | 59 / 969.3 / 2144.3 / 2546.8 / 0 / 186 / 715 | n/a | n/a | 59 / 912.0 / 2076.7 / 2407.2 / 0 / 181 / 320 |
| 128 | n/a | n/a | n/a | n/a | 51 / 2376.5 / 4972.7 / 6249.6 / 0 / 188 / 4091 | 59 / 1976.6 / 4604.7 / 5738.9 / 0 / 191 / 907 | n/a | n/a | 58 / 2026.2 / 4321.4 / 5344.5 / 0 / 186 / 471 |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | none | none | none | none | 1 | 1 | none | none | 1 |

### Closed-loop load, ADBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main | 2ff221447b5d | 2ff221447b5d -DresourceProfile=speed | 2ff221447b5d CZSTD | 2ff221447b5d CZSTD -DresourceProfile=speed CZSTD | gizmo |
|---|---|---|---|---|---|---|---|---|---|
| 1 | n/a | n/a | n/a | n/a | 49 / 16.8 / 33.3 / 45.3 / 0 / 167 / 472 | 49 / 16.9 / 33.2 / 43.1 / 0 / 167 / 436 | n/a | n/a | 53 / 15.9 / 31.4 / 32.0 / 0 / 166 / 79 |
| 8 | n/a | n/a | n/a | n/a | 56 / 140.3 / 266.5 / 303.5 / 0 / 191 / 828 | 60 / 124.4 / 295.6 / 332.3 / 0 / 191 / 557 | n/a | n/a | 61 / 116.0 / 268.4 / 287.9 / 0 / 201 / 156 |
| 32 | n/a | n/a | n/a | n/a | 53 / 554.1 / 1107.4 / 1275.8 / 0 / 197 / 1819 | 60 / 449.1 / 1075.7 / 1197.2 / 0 / 201 / 632 | n/a | n/a | 60 / 449.2 / 1006.2 / 1089.3 / 0 / 194 / 251 |
| 64 | n/a | n/a | n/a | n/a | 52 / 1167.0 / 2371.9 / 2846.2 / 0 / 195 / 2906 | 60 / 1000.9 / 2156.5 / 2535.0 / 0 / 193 / 791 | n/a | n/a | 59 / 901.2 / 2063.1 / 2406.4 / 0 / 191 / 332 |
| 128 | n/a | n/a | n/a | n/a | 50 / 2382.8 / 5101.4 / 6380.3 / 0 / 200 / 4688 | 59 / 1970.6 / 4586.7 / 5721.0 / 0 / 201 / 902 | n/a | n/a | 59 / 1969.4 / 4283.2 / 5411.9 / 0 / 200 / 496 |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | none | none | none | none | 1 | 1 | none | none | 1 |

### Mixed load: 32 ADBC small-query clients alone / with 2 heavy SF10 streams (q01, q18)

| metric | ours-new | ours-27f5 | up-native | up-main | 2ff221447b5d | 2ff221447b5d -DresourceProfile=speed | 2ff221447b5d CZSTD | 2ff221447b5d CZSTD -DresourceProfile=speed CZSTD | gizmo |
|---|---|---|---|---|---|---|---|---|---|
| small QPS alone | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small QPS with heavy | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small p95 ms alone | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small p95 ms with heavy | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy q01 s (median of runs during the window) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy q18 s | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small errors alone / with heavy; heavy failures or wrong answers | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 |

### 4 heavy SF10 queries at once (q01 q09 q18 q21, ADBC) and network-limited client path (netem 10 ms RTT, 1 Gbit/s)

| metric | ours-new | ours-27f5 | up-native | up-main | 2ff221447b5d | 2ff221447b5d -DresourceProfile=speed | 2ff221447b5d CZSTD | 2ff221447b5d CZSTD -DresourceProfile=speed CZSTD | gizmo |
|---|---|---|---|---|---|---|---|---|---|
| heavy x4: slowest query s (n/a if any failed) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy x4: failed or wrong (all rounds) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy x4: server peak RSS MiB | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| netem: SF10 TPC-H ADBC, sum of warm medians s (correct queries) | n/a | n/a | n/a | n/a | n/a | n/a | 35.0 (19/22 q) | 33.7 (22/22 q) | 33.1 (22/22 q) |
| netem: full lineitem export over ADBC, MB/s | n/a | n/a | n/a | n/a | n/a | n/a | 313 | 311 | 106 |

## Netem pairs per job (both sides on the same runner; medians over rounds, B / A per round)

| job | A | B | TPC-H SF10 ADBC s A | B | B / A | export MB/s A | B | B / A | per-round export B / A | queries not ok A / B |
|---|---|---|---|---|---|---|---|---|---|---|
| fu-zstd-netem-local | 2ff221447b5d CZSTD | 2ff221447b5d CZSTD -DresourceProfile=speed CZSTD | n/a | 33.7 | n/a | 321 | 311 | 0.97 | 0.95 1.03 0.97 | 3 / 0 |
| fu-zstd-netem-local-vs-gizmo | gizmo | 2ff221447b5d CZSTD | 33.1 | 33.7 | 1.02 | 106 | 311 | 2.92 | 2.90 2.97 2.92 | 0 / 0 |

TPC-H n/a = not all 22 queries answered correctly in a round (see 'queries not ok', max over rounds).

Not in this run: up-native with its ZSTD Flight compression on the netem path (job `new-vs-native-zstd-netem`).

Not yet in this report: TLS + token on/off for ours.

