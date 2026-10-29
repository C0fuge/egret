# Server comparison - Report 2: LOAD (compare run 40800578035)

## Setup

| item | value |
|---|---|
| runner | GitHub-hosted `ubuntu-latest`: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor; Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor; Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor; Linux ubuntu24 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C; RAM 15983 MB |
| containers | every server: `eclipse-temurin:21-jre`, `--cpus=2 --cpuset-cpus=0,1 --memory=6g --memory-swap=6g`, JVM `-Xmx3g -XX:MaxDirectMemorySize=2g`, `MALLOC_ARENA_MAX=4`; load generators in their own container on cpus 2,3 (so the client side has 2 cores too: at 64/128 clients the client can be the limit, see client notes) |
| servers | ours-new = `7562a5bdb7b9`; ours-27f5 = `27f583adccd7`; up-native = `1de5f6b4b218f83f01a3adf2708af5f36f80811b`; up-main = `dbacd8d585bce2ef2a449c821fe3a53cc6060b57` |
| data | TPC-H SF10 Parquet on local disk (load, mixed, heavy, netem) |
| pairs | ours-new (side A) vs one other server (side B) on the same runner, rounds A B / B A / A B |
| load mix | `point_orders`, `point_lineitem`, `count_filter` (every server answers them; upstream has no JDBC prepared statements) |
| settings | `def` = each server's default `duckDbThreads` (ours 4, upstream 2); `t8` = 8 on both; `zstd` = netem path only, up-native with its ZSTD batch compression (`-DflightCompression=zstd`, decoded by ADBC) vs ours plain (up-main has no such option) |

## Setting `def`

### Closed-loop load, JDBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main | 881bbf73e946 | 881bbf73e946 -DduckDbSharedDatabase=true |
|---|---|---|---|---|---|---|
| 1 | 38 / 21.4 / 44.8 / 55.4 / 0 / 171 / 390 | n/a | n/a | n/a | 40 / 20.4 / 42.5 / 53.6 / 0 / 171 / 387 | 41 / 20.3 / 40.8 / 61.9 / 0 / 169 / 368 |
| 8 | 44 / 182.9 / 280.4 / 342.8 / 0 / 198 / 772 | n/a | n/a | n/a | 44 / 183.8 / 281.8 / 331.1 / 0 / 198 / 822 | 50 / 145.3 / 318.7 / 347.9 / 0 / 199 / 638 |
| 32 | 41 / 753.7 / 1326.9 / 2122.8 / 0 / 185 / 1652 | n/a | n/a | n/a | 41 / 751.7 / 1317.7 / 2017.2 / 0 / 183 / 1677 | 51 / 559.5 / 1195.1 / 1523.7 / 0 / 186 / 1378 |
| 64 | 38 / 1580.5 / 3029.0 / 4105.3 / 0 / 189 / 2524 | n/a | n/a | n/a | 38 / 1552.2 / 2989.2 / 3925.2 / 0 / 185 / 2517 | 50 / 1233.1 / 2440.5 / 3256.2 / 0 / 188 / 2118 |
| 128 | 35 / 3265.4 / 6925.5 / 8933.2 / 0 / 187 / 3910 | n/a | n/a | n/a | 35 / 3219.3 / 6924.3 / 8790.2 / 0 / 194 / 3959 | 48 / 2380.7 / 5437.2 / 7271.3 / 0 / 195 / 3167 |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | 1 | none | none | none | 1 | 1 |

### Closed-loop load, ADBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main | 881bbf73e946 | 881bbf73e946 -DduckDbSharedDatabase=true |
|---|---|---|---|---|---|---|
| 1 | 41 / 20.1 / 39.5 / 51.8 / 0 / 162 / 404 | n/a | n/a | n/a | 42 / 20.0 / 38.4 / 51.2 / 0 / 162 / 410 | 42 / 20.0 / 37.3 / 55.5 / 0 / 159 / 376 |
| 8 | 44 / 179.5 / 280.8 / 327.8 / 0 / 202 / 814 | n/a | n/a | n/a | 44 / 183.4 / 279.1 / 331.2 / 0 / 197 / 811 | 51 / 145.3 / 312.0 / 337.7 / 0 / 203 / 657 |
| 32 | 39 / 768.7 / 1393.1 / 2085.0 / 0 / 190 / 1773 | n/a | n/a | n/a | 40 / 758.4 / 1392.7 / 2046.5 / 0 / 196 / 1718 | 51 / 572.8 / 1216.9 / 1513.3 / 0 / 191 / 1435 |
| 64 | 37 / 1570.2 / 3124.1 / 4408.8 / 0 / 190 / 2865 | n/a | n/a | n/a | 37 / 1560.3 / 3183.2 / 4476.1 / 0 / 190 / 2830 | 49 / 1260.7 / 2475.4 / 3707.7 / 0 / 184 / 2406 |
| 128 | 34 / 3308.4 / 6920.9 / 8996.0 / 0 / 191 / 4431 | n/a | n/a | n/a | 34 / 3312.3 / 6957.4 / 9087.5 / 0 / 189 / 4457 | 48 / 2432.2 / 5537.7 / 7475.5 / 0 / 198 / 3910 |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | 1 | none | none | none | 1 | 1 |

### Mixed load: 32 ADBC small-query clients alone / with 2 heavy SF10 streams (q01, q18)

| metric | ours-new | ours-27f5 | up-native | up-main | 881bbf73e946 | 881bbf73e946 -DduckDbSharedDatabase=true |
|---|---|---|---|---|---|---|
| small QPS alone | n/a | n/a | n/a | n/a | n/a | n/a |
| small QPS with heavy | n/a | n/a | n/a | n/a | n/a | n/a |
| small p95 ms alone | n/a | n/a | n/a | n/a | n/a | n/a |
| small p95 ms with heavy | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy q01 s (median of runs during the window) | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy q18 s | n/a | n/a | n/a | n/a | n/a | n/a |
| small errors alone / with heavy; heavy failures or wrong answers | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 |

### 4 heavy SF10 queries at once (q01 q09 q18 q21, ADBC) and network-limited client path (netem 10 ms RTT, 1 Gbit/s)

| metric | ours-new | ours-27f5 | up-native | up-main | 881bbf73e946 | 881bbf73e946 -DduckDbSharedDatabase=true |
|---|---|---|---|---|---|---|
| heavy x4: slowest query s (n/a if any failed) | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy x4: failed or wrong (all rounds) | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy x4: server peak RSS MiB | n/a | n/a | n/a | n/a | n/a | n/a |
| netem: SF10 TPC-H ADBC, sum of warm medians s (correct queries) | n/a | n/a | n/a | n/a | n/a | n/a |
| netem: full lineitem export over ADBC, MB/s | n/a | n/a | n/a | n/a | n/a | n/a |

Not in this run: up-native with its ZSTD Flight compression on the netem path (job `new-vs-native-zstd-netem`).

Not yet in this report: TLS + token on/off for ours.

