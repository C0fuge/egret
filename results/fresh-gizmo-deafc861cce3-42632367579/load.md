# Server comparison - Report 2: LOAD (compare run 42632367579)

## Setup

| item | value |
|---|---|
| runner | GitHub-hosted `ubuntu-latest`: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor; Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor; Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor; Linux ubuntu26 4 vCPU Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz; RAM 15983 MB |
| containers | every server: `eclipse-temurin:21-jre`, `--cpus=2 --cpuset-cpus=0,1 --memory=6g --memory-swap=6g`, JVM `-Xmx3g -XX:MaxDirectMemorySize=2g`, `MALLOC_ARENA_MAX=4`; load generators in their own container on cpus 2,3 (so the client side has 2 cores too: at 64/128 clients the client can be the limit, see client notes) |
| servers | ours-new = `7562a5bdb7b9`; ours-27f5 = `27f583adccd7`; up-native = `caa12d3c64aeb03252ad4905072f53f754cf19cd`; up-main = `dbacd8d585bce2ef2a449c821fe3a53cc6060b57` |
| data | TPC-H SF10 Parquet on local disk (load, mixed, heavy, netem) |
| pairs | ours-new (side A) vs one other server (side B) on the same runner, rounds A B / B A / A B |
| load mix | `point_orders`, `point_lineitem`, `count_filter` (every server answers them; upstream has no JDBC prepared statements) |
| settings | `def` = each server's default `duckDbThreads` (ours 4, upstream 2); `t8` = 8 on both; `zstd` = netem path only, up-native with its ZSTD batch compression (`-DflightCompression=zstd`, decoded by ADBC) vs ours plain (up-main has no such option) |

## Setting `def`

### Closed-loop load, JDBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main | deafc861cce3 | deafc861cce3 -DresourceProfile=speed | deafc861cce3 CZSTD | deafc861cce3 CZSTD -DresourceProfile=speed CZSTD | gizmo |
|---|---|---|---|---|---|---|---|---|---|
| 1 | n/a | n/a | n/a | n/a | 41 / 19.9 / 41.6 / 53.5 / 0 / 169 / 400 | 42 / 19.2 / 40.3 / 53.8 / 0 / 171 / 382 | n/a | n/a | 50 / 16.8 / 33.9 / 35.6 / 0 / 159 / 79 |
| 8 | n/a | n/a | n/a | n/a | 47 / 169.2 / 306.7 / 358.5 / 0 / 199 / 759 | 52 / 144.8 / 339.1 / 384.3 / 0 / 200 / 468 | n/a | n/a | 55 / 129.0 / 294.8 / 314.7 / 0 / 190 / 149 |
| 32 | n/a | n/a | n/a | n/a | 47 / 638.4 / 1278.1 / 1659.8 / 0 / 195 / 1665 | 53 / 526.7 / 1218.4 / 1374.2 / 0 / 194 / 531 | n/a | n/a | 55 / 505.0 / 1101.1 / 1186.7 / 0 / 191 / 231 |
| 64 | n/a | n/a | n/a | n/a | 46 / 1307.7 / 2622.3 / 3287.4 / 0 / 192 / 2516 | 53 / 1110.1 / 2353.0 / 2816.0 / 0 / 192 / 622 | n/a | n/a | 54 / 1022.3 / 2296.0 / 2682.6 / 0 / 191 / 321 |
| 128 | n/a | n/a | n/a | n/a | 44 / 2680.4 / 5882.3 / 7512.8 / 0 / 193 / 3970 | 52 / 2265.3 / 5005.2 / 6309.7 / 0 / 193 / 837 | n/a | n/a | 52 / 2184.1 / 4805.6 / 5772.5 / 0 / 187 / 469 |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | none | none | none | none | 1 | 1 | none | none | 1 |

### Closed-loop load, ADBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main | deafc861cce3 | deafc861cce3 -DresourceProfile=speed | deafc861cce3 CZSTD | deafc861cce3 CZSTD -DresourceProfile=speed CZSTD | gizmo |
|---|---|---|---|---|---|---|---|---|---|
| 1 | n/a | n/a | n/a | n/a | 43 / 19.1 / 37.4 / 47.9 / 0 / 163 / 406 | 45 / 18.5 / 36.6 / 46.5 / 0 / 163 / 406 | n/a | n/a | 49 / 17.1 / 33.9 / 34.7 / 0 / 169 / 78 |
| 8 | n/a | n/a | n/a | n/a | 48 / 163.5 / 307.0 / 354.4 / 0 / 191 / 786 | 53 / 141.7 / 335.7 / 372.8 / 0 / 191 / 473 | n/a | n/a | 55 / 129.7 / 295.7 / 317.9 / 0 / 196 / 149 |
| 32 | n/a | n/a | n/a | n/a | 47 / 633.6 / 1279.2 / 1625.0 / 0 / 200 / 1744 | 53 / 528.4 / 1217.9 / 1325.7 / 0 / 203 / 547 | n/a | n/a | 54 / 506.3 / 1103.0 / 1183.7 / 0 / 202 / 243 |
| 64 | n/a | n/a | n/a | n/a | 45 / 1363.6 / 2687.4 / 3491.8 / 0 / 200 / 2909 | 53 / 1120.1 / 2411.6 / 2818.5 / 0 / 203 / 635 | n/a | n/a | 54 / 998.0 / 2324.3 / 2661.3 / 0 / 200 / 334 |
| 128 | n/a | n/a | n/a | n/a | 43 / 2742.5 / 5771.1 / 7270.3 / 0 / 196 / 4584 | 52 / 2291.3 / 5038.5 / 6112.0 / 0 / 198 / 831 | n/a | n/a | 52 / 2210.4 / 4695.5 / 5525.5 / 0 / 201 / 491 |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | none | none | none | none | 1 | 1 | none | none | 1 |

### Mixed load: 32 ADBC small-query clients alone / with 2 heavy SF10 streams (q01, q18)

| metric | ours-new | ours-27f5 | up-native | up-main | deafc861cce3 | deafc861cce3 -DresourceProfile=speed | deafc861cce3 CZSTD | deafc861cce3 CZSTD -DresourceProfile=speed CZSTD | gizmo |
|---|---|---|---|---|---|---|---|---|---|
| small QPS alone | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small QPS with heavy | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small p95 ms alone | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small p95 ms with heavy | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy q01 s (median of runs during the window) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy q18 s | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small errors alone / with heavy; heavy failures or wrong answers | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 |

### 4 heavy SF10 queries at once (q01 q09 q18 q21, ADBC) and network-limited client path (netem 10 ms RTT, 1 Gbit/s)

| metric | ours-new | ours-27f5 | up-native | up-main | deafc861cce3 | deafc861cce3 -DresourceProfile=speed | deafc861cce3 CZSTD | deafc861cce3 CZSTD -DresourceProfile=speed CZSTD | gizmo |
|---|---|---|---|---|---|---|---|---|---|
| heavy x4: slowest query s (n/a if any failed) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy x4: failed or wrong (all rounds) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy x4: server peak RSS MiB | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| netem: SF10 TPC-H ADBC, sum of warm medians s (correct queries) | n/a | n/a | n/a | n/a | n/a | n/a | 26.1 (22/22 q) | 25.6 (22/22 q) | 26.4 (22/22 q) |
| netem: full lineitem export over ADBC, MB/s | n/a | n/a | n/a | n/a | n/a | n/a | 410 | 420 | 106 |

## Netem pairs per job (both sides on the same runner; medians over rounds, B / A per round)

| job | A | B | TPC-H SF10 ADBC s A | B | B / A | export MB/s A | B | B / A | per-round export B / A | queries not ok A / B |
|---|---|---|---|---|---|---|---|---|---|---|
| fu-zstd-netem-local | deafc861cce3 CZSTD | deafc861cce3 CZSTD -DresourceProfile=speed CZSTD | 26.8 | 25.6 | 0.96 | 392 | 420 | 1.07 | 1.01 1.04 1.09 | 0 / 0 |
| fu-zstd-netem-local-vs-gizmo | gizmo | deafc861cce3 CZSTD | 26.4 | 25.6 | 0.97 | 106 | 420 | 3.95 | 3.95 3.81 4.03 | 0 / 0 |

TPC-H n/a = not all 22 queries answered correctly in a round (see 'queries not ok', max over rounds).

Not in this run: up-native with its ZSTD Flight compression on the netem path (job `new-vs-native-zstd-netem`).

Not yet in this report: TLS + token on/off for ours.

