# Server comparison - Report 2: LOAD (compare run 44158872708)

## Setup

| item | value |
|---|---|
| runner | GitHub-hosted `ubuntu-latest`: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor; Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor; Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor; Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C; Linux ubuntu26 4 vCPU Intel(R) Xeon(R) 6975P-C; RAM 15983 MB |
| containers | every server: `eclipse-temurin:21-jre`, `--cpus=2 --cpuset-cpus=0,1 --memory=6g --memory-swap=6g`, JVM `-Xmx3g -XX:MaxDirectMemorySize=2g`, `MALLOC_ARENA_MAX=4`; load generators in their own container on cpus 2,3 (so the client side has 2 cores too: at 64/128 clients the client can be the limit, see client notes) |
| servers | ours-new = `7562a5bdb7b9`; ours-27f5 = `27f583adccd7`; up-native = `d05bf9c521294a6a91c5da44800aa420ab92a523`; up-main = `dbacd8d585bce2ef2a449c821fe3a53cc6060b57` |
| data | TPC-H SF10 Parquet on local disk (load, mixed, heavy, netem) |
| pairs | ours-new (side A) vs one other server (side B) on the same runner, rounds A B / B A / A B |
| load mix | `point_orders`, `point_lineitem`, `count_filter` (every server answers them; upstream has no JDBC prepared statements) |
| settings | `def` = each server's default `duckDbThreads` (ours 4, upstream 2); `t8` = 8 on both; `zstd` = netem path only, up-native with its ZSTD batch compression (`-DflightCompression=zstd`, decoded by ADBC) vs ours plain (up-main has no such option) |

## Setting `def`

### Closed-loop load, JDBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main | f4feb0d5e404 | f4feb0d5e404 -DresourceProfile=speed | f4feb0d5e404 CZSTD | f4feb0d5e404 CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| 1 | n/a | n/a | 39 / 20.9 / 47.4 / 67.6 / 0 / 165 / 408 | n/a | 43 / 18.7 / 40.1 / 56.3 / 0 / 172 / 404 | 43 / 18.8 / 40.8 / 54.5 / 0 / 174 / 404 | n/a | n/a |
| 8 | n/a | n/a | 52 / 137.7 / 312.1 / 341.1 / 0 / 201 / 464 | n/a | 53 / 139.0 / 319.9 / 358.7 / 0 / 202 / 530 | 53 / 143.0 / 334.8 / 382.5 / 0 / 202 / 530 | n/a | n/a |
| 32 | n/a | n/a | 55 / 500.1 / 1126.7 / 1228.8 / 0 / 193 / 554 | n/a | 54 / 518.1 / 1186.1 / 1287.3 / 0 / 192 / 602 | 54 / 521.1 / 1196.3 / 1328.7 / 0 / 183 / 602 | n/a | n/a |
| 64 | n/a | n/a | 56 / 1037.0 / 2277.3 / 2654.9 / 0 / 193 / 736 | n/a | 54 / 1086.6 / 2348.3 / 2702.8 / 0 / 193 / 658 | 54 / 1093.1 / 2367.3 / 2778.8 / 0 / 192 / 658 | n/a | n/a |
| 128 | n/a | n/a | 54 / 2154.9 / 4833.0 / 6056.1 / 0 / 194 / 896 | n/a | 52 / 2244.2 / 4971.2 / 6185.9 / 0 / 193 / 824 | 52 / 2243.5 / 4959.9 / 6255.8 / 0 / 193 / 824 | n/a | n/a |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | none | none | 1 | none | 1 | 1 | none | none |

### Closed-loop load, ADBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main | f4feb0d5e404 | f4feb0d5e404 -DresourceProfile=speed | f4feb0d5e404 CZSTD | f4feb0d5e404 CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| 1 | n/a | n/a | 45 / 17.8 / 36.4 / 64.8 / 0 / 167 / 397 | n/a | 45 / 18.2 / 36.6 / 51.8 / 0 / 163 / 437 | 45 / 18.2 / 36.6 / 50.5 / 0 / 163 / 437 | n/a | n/a |
| 8 | n/a | n/a | 56 / 128.2 / 292.5 / 319.2 / 0 / 196 / 450 | n/a | 54 / 137.6 / 319.9 / 353.7 / 0 / 194 / 546 | 53 / 141.9 / 332.3 / 374.5 / 0 / 203 / 546 | n/a | n/a |
| 32 | n/a | n/a | 56 / 487.7 / 1102.5 / 1215.3 / 0 / 194 / 618 | n/a | 53 / 517.9 / 1189.7 / 1319.9 / 0 / 203 / 586 | 53 / 520.4 / 1199.4 / 1333.9 / 0 / 203 / 586 | n/a | n/a |
| 64 | n/a | n/a | 56 / 1018.5 / 2332.5 / 2743.3 / 0 / 203 / 751 | n/a | 53 / 1081.8 / 2340.4 / 2694.3 / 0 / 203 / 689 | 53 / 1097.9 / 2405.3 / 2790.9 / 0 / 203 / 689 | n/a | n/a |
| 128 | n/a | n/a | 55 / 2134.5 / 4771.3 / 5861.2 / 0 / 203 / 923 | n/a | 53 / 2267.4 / 4998.1 / 6175.8 / 0 / 193 / 843 | 52 / 2287.7 / 5035.9 / 6066.0 / 0 / 196 / 843 | n/a | n/a |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | none | none | 1 | none | 1 | 1 | none | none |

### Mixed load: 32 ADBC small-query clients alone / with 2 heavy SF10 streams (q01, q18)

| metric | ours-new | ours-27f5 | up-native | up-main | f4feb0d5e404 | f4feb0d5e404 -DresourceProfile=speed | f4feb0d5e404 CZSTD | f4feb0d5e404 CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| small QPS alone | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small QPS with heavy | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small p95 ms alone | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small p95 ms with heavy | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy q01 s (median of runs during the window) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy q18 s | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small errors alone / with heavy; heavy failures or wrong answers | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 |

### 4 heavy SF10 queries at once (q01 q09 q18 q21, ADBC) and network-limited client path (netem 10 ms RTT, 1 Gbit/s)

| metric | ours-new | ours-27f5 | up-native | up-main | f4feb0d5e404 | f4feb0d5e404 -DresourceProfile=speed | f4feb0d5e404 CZSTD | f4feb0d5e404 CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| heavy x4: slowest query s (n/a if any failed) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy x4: failed or wrong (all rounds) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy x4: server peak RSS MiB | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| netem: SF10 TPC-H ADBC, sum of warm medians s (correct queries) | n/a | n/a | 0.0 (0/22 q) | n/a | n/a | n/a | 40.8 (22/22 q) | 40.1 (22/22 q) |
| netem: full lineitem export over ADBC, MB/s | n/a | n/a | 255 | n/a | n/a | n/a | 249 | 250 |

## Netem pairs per job (both sides on the same runner; medians over rounds, B / A per round)

| job | A | B | TPC-H SF10 ADBC s A | B | B / A | export MB/s A | B | B / A | per-round export B / A | queries not ok A / B |
|---|---|---|---|---|---|---|---|---|---|---|
| fu-zstd-netem-local | f4feb0d5e404 CZSTD | f4feb0d5e404 CZSTD -DresourceProfile=speed CZSTD | 41.1 | 40.1 | 0.98 | 248 | 250 | 1.01 | 1.00 1.01 1.01 | 0 / 0 |
| fu-zstd-netem-local-vs-up-native | up-native | f4feb0d5e404 CZSTD | n/a | 40.1 | n/a | 255 | 250 | 0.98 | 0.97 0.98 0.98 | 22 / 0 |

TPC-H n/a = not all 22 queries answered correctly in a round (see 'queries not ok', max over rounds).

Not in this run: up-native with its ZSTD Flight compression on the netem path (job `new-vs-native-zstd-netem`).

Not yet in this report: TLS + token on/off for ours.

