# Server comparison - Report 2: LOAD (compare run 43175544843)

## Setup

| item | value |
|---|---|
| runner | GitHub-hosted `ubuntu-latest`: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor; Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor; Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor; Linux ubuntu26 4 vCPU Intel(R) Xeon(R) 6973P-C; Linux ubuntu26 4 vCPU Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz; RAM 15983 MB |
| containers | every server: `eclipse-temurin:21-jre`, `--cpus=2 --cpuset-cpus=0,1 --memory=6g --memory-swap=6g`, JVM `-Xmx3g -XX:MaxDirectMemorySize=2g`, `MALLOC_ARENA_MAX=4`; load generators in their own container on cpus 2,3 (so the client side has 2 cores too: at 64/128 clients the client can be the limit, see client notes) |
| servers | ours-new = `7562a5bdb7b9`; ours-27f5 = `27f583adccd7`; up-native = `cfaa929746cbf9ba9f6134cbf0c5a9683b2c1e92`; up-main = `dbacd8d585bce2ef2a449c821fe3a53cc6060b57` |
| data | TPC-H SF10 Parquet on local disk (load, mixed, heavy, netem) |
| pairs | ours-new (side A) vs one other server (side B) on the same runner, rounds A B / B A / A B |
| load mix | `point_orders`, `point_lineitem`, `count_filter` (every server answers them; upstream has no JDBC prepared statements) |
| settings | `def` = each server's default `duckDbThreads` (ours 4, upstream 2); `t8` = 8 on both; `zstd` = netem path only, up-native with its ZSTD batch compression (`-DflightCompression=zstd`, decoded by ADBC) vs ours plain (up-main has no such option) |

## Setting `def`

### Closed-loop load, JDBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main | 2c169a53db3b | 2c169a53db3b -DresourceProfile=speed | 2c169a53db3b CZSTD | 2c169a53db3b CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| 1 | n/a | n/a | 38 / 21.7 / 47.3 / 68.1 / 0 / 161 / 405 | n/a | 41 / 19.7 / 41.7 / 53.9 / 0 / 166 / 459 | 42 / 19.3 / 41.0 / 53.6 / 0 / 167 / 399 | n/a | n/a |
| 8 | n/a | n/a | 51 / 140.9 / 315.3 / 340.6 / 0 / 199 / 439 | n/a | 47 / 166.9 / 306.0 / 348.1 / 0 / 202 / 788 | 52 / 147.1 / 338.1 / 380.0 / 0 / 202 / 515 | n/a | n/a |
| 32 | n/a | n/a | 54 / 510.8 / 1158.6 / 1274.6 / 0 / 194 / 588 | n/a | 47 / 638.3 / 1251.7 / 1444.3 / 0 / 194 / 1633 | 52 / 529.4 / 1220.9 / 1361.9 / 0 / 195 / 584 | n/a | n/a |
| 64 | n/a | n/a | 54 / 1065.4 / 2327.9 / 2708.3 / 0 / 193 / 747 | n/a | 45 / 1339.6 / 2560.8 / 3090.9 / 0 / 190 / 2516 | 53 / 1136.9 / 2338.1 / 2786.3 / 0 / 192 / 642 | n/a | n/a |
| 128 | n/a | n/a | 54 / 2203.8 / 4849.2 / 6047.9 / 0 / 194 / 901 | n/a | 44 / 2709.8 / 5484.3 / 6731.0 / 0 / 188 / 3999 | 52 / 2237.2 / 5055.3 / 6147.4 / 0 / 192 / 807 | n/a | n/a |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | none | none | 1 | none | 1 | 1 | none | none |

### Closed-loop load, ADBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main | 2c169a53db3b | 2c169a53db3b -DresourceProfile=speed | 2c169a53db3b CZSTD | 2c169a53db3b CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| 1 | n/a | n/a | 44 / 18.0 / 36.7 / 65.2 / 0 / 168 / 392 | n/a | 42 / 19.5 / 38.3 / 50.2 / 0 / 161 / 444 | 43 / 19.1 / 37.9 / 50.1 / 0 / 161 / 411 | n/a | n/a |
| 8 | n/a | n/a | 55 / 131.1 / 291.6 / 319.7 / 0 / 199 / 466 | n/a | 48 / 165.6 / 305.5 / 351.0 / 0 / 195 / 804 | 52 / 146.1 / 335.5 / 373.4 / 0 / 192 / 585 | n/a | n/a |
| 32 | n/a | n/a | 55 / 499.7 / 1123.1 / 1237.9 / 0 / 203 / 637 | n/a | 46 / 645.6 / 1244.6 / 1457.7 / 0 / 202 / 1680 | 52 / 533.2 / 1214.1 / 1339.3 / 0 / 203 / 599 | n/a | n/a |
| 64 | n/a | n/a | 55 / 1095.8 / 2306.6 / 2687.6 / 0 / 204 / 795 | n/a | 45 / 1341.1 / 2617.5 / 3174.1 / 0 / 201 / 2878 | 52 / 1108.9 / 2370.9 / 2772.8 / 0 / 202 / 654 | n/a | n/a |
| 128 | n/a | n/a | 54 / 2156.3 / 4814.7 / 5866.3 / 0 / 203 / 911 | n/a | 44 / 2748.3 / 5426.8 / 6698.8 / 0 / 194 / 4596 | 52 / 2256.7 / 5007.8 / 6208.1 / 0 / 193 / 881 | n/a | n/a |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | none | none | 1 | none | 1 | 1 | none | none |

### Mixed load: 32 ADBC small-query clients alone / with 2 heavy SF10 streams (q01, q18)

| metric | ours-new | ours-27f5 | up-native | up-main | 2c169a53db3b | 2c169a53db3b -DresourceProfile=speed | 2c169a53db3b CZSTD | 2c169a53db3b CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| small QPS alone | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small QPS with heavy | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small p95 ms alone | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small p95 ms with heavy | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy q01 s (median of runs during the window) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy q18 s | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small errors alone / with heavy; heavy failures or wrong answers | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 |

### 4 heavy SF10 queries at once (q01 q09 q18 q21, ADBC) and network-limited client path (netem 10 ms RTT, 1 Gbit/s)

| metric | ours-new | ours-27f5 | up-native | up-main | 2c169a53db3b | 2c169a53db3b -DresourceProfile=speed | 2c169a53db3b CZSTD | 2c169a53db3b CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| heavy x4: slowest query s (n/a if any failed) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy x4: failed or wrong (all rounds) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy x4: server peak RSS MiB | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| netem: SF10 TPC-H ADBC, sum of warm medians s (correct queries) | n/a | n/a | 0.0 (0/22 q) | n/a | n/a | n/a | 34.8 (22/22 q) | 34.3 (22/22 q) |
| netem: full lineitem export over ADBC, MB/s | n/a | n/a | 318 | n/a | n/a | n/a | 322 | 321 |

## Netem pairs per job (both sides on the same runner; medians over rounds, B / A per round)

| job | A | B | TPC-H SF10 ADBC s A | B | B / A | export MB/s A | B | B / A | per-round export B / A | queries not ok A / B |
|---|---|---|---|---|---|---|---|---|---|---|
| fu-zstd-netem-local | 2c169a53db3b CZSTD | 2c169a53db3b CZSTD -DresourceProfile=speed CZSTD | 35.2 | 34.3 | 0.98 | 322 | 321 | 1.00 | 1.00 1.07 0.95 | 0 / 0 |
| fu-zstd-netem-local-vs-up-native | up-native | 2c169a53db3b CZSTD | n/a | 34.3 | n/a | 318 | 321 | 1.01 | 1.02 1.01 0.96 | 22 / 0 |

TPC-H n/a = not all 22 queries answered correctly in a round (see 'queries not ok', max over rounds).

Not in this run: up-native with its ZSTD Flight compression on the netem path (job `new-vs-native-zstd-netem`).

Not yet in this report: TLS + token on/off for ours.

