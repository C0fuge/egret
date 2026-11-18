# Server comparison - Report 2: LOAD (compare run 44244388077)

## Setup

| item | value |
|---|---|
| runner | GitHub-hosted `ubuntu-latest`: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor; Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor; Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor; Linux ubuntu26 4 vCPU Intel(R) Xeon(R) 6975P-C; RAM 15983 MB |
| containers | every server: `eclipse-temurin:21-jre`, `--cpus=2 --cpuset-cpus=0,1 --memory=6g --memory-swap=6g`, JVM `-Xmx3g -XX:MaxDirectMemorySize=2g`, `MALLOC_ARENA_MAX=4`; load generators in their own container on cpus 2,3 (so the client side has 2 cores too: at 64/128 clients the client can be the limit, see client notes) |
| servers | ours-new = `7562a5bdb7b9`; ours-27f5 = `27f583adccd7`; up-native = `d05bf9c521294a6a91c5da44800aa420ab92a523`; up-main = `dbacd8d585bce2ef2a449c821fe3a53cc6060b57` |
| data | TPC-H SF10 Parquet on local disk (load, mixed, heavy, netem) |
| pairs | ours-new (side A) vs one other server (side B) on the same runner, rounds A B / B A / A B |
| load mix | `point_orders`, `point_lineitem`, `count_filter` (every server answers them; upstream has no JDBC prepared statements) |
| settings | `def` = each server's default `duckDbThreads` (ours 4, upstream 2); `t8` = 8 on both; `zstd` = netem path only, up-native with its ZSTD batch compression (`-DflightCompression=zstd`, decoded by ADBC) vs ours plain (up-main has no such option) |

## Setting `def`

### Closed-loop load, JDBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main | 5f02e5b35611 | 5f02e5b35611 -DresourceProfile=speed | 5f02e5b35611 CZSTD | 5f02e5b35611 CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| 1 | n/a | n/a | 46 / 18.0 / 38.5 / 56.8 / 0 / 162 / 410 | n/a | 54 / 15.2 / 31.6 / 46.2 / 0 / 169 / 400 | 54 / 14.8 / 31.7 / 43.1 / 0 / 172 / 400 | n/a | n/a |
| 8 | n/a | n/a | 63 / 115.8 / 253.1 / 279.1 / 0 / 201 / 455 | n/a | 66 / 111.4 / 255.6 / 287.2 / 0 / 183 / 534 | 66 / 114.6 / 263.7 / 301.3 / 0 / 183 / 534 | n/a | n/a |
| 32 | n/a | n/a | 67 / 408.1 / 943.8 / 1047.7 / 0 / 192 / 598 | n/a | 66 / 422.0 / 964.1 / 1082.9 / 0 / 192 / 588 | 65 / 433.8 / 967.6 / 1092.5 / 0 / 192 / 588 | n/a | n/a |
| 64 | n/a | n/a | 67 / 839.0 / 1916.2 / 2286.2 / 0 / 203 / 728 | n/a | 65 / 909.9 / 1950.1 / 2339.7 / 0 / 191 / 745 | 65 / 910.9 / 1961.3 / 2399.0 / 0 / 189 / 745 | n/a | n/a |
| 128 | n/a | n/a | 68 / 1723.5 / 4123.3 / 5113.1 / 0 / 203 / 935 | n/a | 64 / 1810.1 / 4210.0 / 5283.4 / 0 / 193 / 842 | 64 / 1811.9 / 4272.4 / 5302.7 / 0 / 193 / 842 | n/a | n/a |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | none | none | 1 | none | 1 | 1 | none | none |

### Closed-loop load, ADBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main | 5f02e5b35611 | 5f02e5b35611 -DresourceProfile=speed | 5f02e5b35611 CZSTD | 5f02e5b35611 CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| 1 | n/a | n/a | 54 / 15.5 / 29.3 / 51.9 / 0 / 159 / 389 | n/a | 55 / 15.1 / 29.3 / 40.7 / 0 / 164 / 407 | 56 / 14.6 / 29.5 / 38.7 / 0 / 169 / 407 | n/a | n/a |
| 8 | n/a | n/a | 69 / 103.2 / 236.5 / 261.1 / 0 / 203 / 445 | n/a | 66 / 115.0 / 253.9 / 284.5 / 0 / 202 / 562 | 65 / 117.3 / 263.8 / 302.1 / 0 / 202 / 562 | n/a | n/a |
| 32 | n/a | n/a | 70 / 389.3 / 898.5 / 1014.7 / 0 / 195 / 574 | n/a | 66 / 427.4 / 952.7 / 1067.9 / 0 / 201 / 590 | 65 / 430.0 / 962.9 / 1087.6 / 0 / 203 / 590 | n/a | n/a |
| 64 | n/a | n/a | 69 / 815.1 / 1897.8 / 2260.4 / 0 / 197 / 833 | n/a | 64 / 917.5 / 1934.2 / 2306.0 / 0 / 199 / 763 | 64 / 922.3 / 1941.8 / 2322.5 / 0 / 192 / 763 | n/a | n/a |
| 128 | n/a | n/a | 68 / 1698.5 / 4051.7 / 5064.9 / 0 / 203 / 937 | n/a | 63 / 1839.6 / 4250.6 / 5283.1 / 0 / 197 / 884 | 63 / 1882.4 / 4247.9 / 5282.9 / 0 / 200 / 884 | n/a | n/a |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | none | none | 1 | none | 1 | 1 | none | none |

### Mixed load: 32 ADBC small-query clients alone / with 2 heavy SF10 streams (q01, q18)

| metric | ours-new | ours-27f5 | up-native | up-main | 5f02e5b35611 | 5f02e5b35611 -DresourceProfile=speed | 5f02e5b35611 CZSTD | 5f02e5b35611 CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| small QPS alone | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small QPS with heavy | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small p95 ms alone | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small p95 ms with heavy | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy q01 s (median of runs during the window) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy q18 s | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small errors alone / with heavy; heavy failures or wrong answers | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 |

### 4 heavy SF10 queries at once (q01 q09 q18 q21, ADBC) and network-limited client path (netem 10 ms RTT, 1 Gbit/s)

| metric | ours-new | ours-27f5 | up-native | up-main | 5f02e5b35611 | 5f02e5b35611 -DresourceProfile=speed | 5f02e5b35611 CZSTD | 5f02e5b35611 CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| heavy x4: slowest query s (n/a if any failed) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy x4: failed or wrong (all rounds) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy x4: server peak RSS MiB | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| netem: SF10 TPC-H ADBC, sum of warm medians s (correct queries) | n/a | n/a | 0.0 (0/22 q) | n/a | n/a | n/a | 41.6 (22/22 q) | 41.1 (22/22 q) |
| netem: full lineitem export over ADBC, MB/s | n/a | n/a | 261 | n/a | n/a | n/a | 254 | 248 |

## Netem pairs per job (both sides on the same runner; medians over rounds, B / A per round)

| job | A | B | TPC-H SF10 ADBC s A | B | B / A | export MB/s A | B | B / A | per-round export B / A | queries not ok A / B |
|---|---|---|---|---|---|---|---|---|---|---|
| fu-zstd-netem-local | 5f02e5b35611 CZSTD | 5f02e5b35611 CZSTD -DresourceProfile=speed CZSTD | 42.0 | 41.1 | 0.98 | 262 | 248 | 0.95 | 0.95 0.96 0.95 | 0 / 0 |
| fu-zstd-netem-local-vs-up-native | up-native | 5f02e5b35611 CZSTD | n/a | 41.1 | n/a | 261 | 248 | 0.95 | 0.95 0.95 0.96 | 22 / 0 |

TPC-H n/a = not all 22 queries answered correctly in a round (see 'queries not ok', max over rounds).

Not in this run: up-native with its ZSTD Flight compression on the netem path (job `new-vs-native-zstd-netem`).

Not yet in this report: TLS + token on/off for ours.

