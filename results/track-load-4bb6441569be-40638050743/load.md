# Server comparison - Report 2: LOAD (compare run 40638050743)

## Setup

| item | value |
|---|---|
| runner | GitHub-hosted `ubuntu-latest`: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor; Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor; Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor; Linux ubuntu24 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C; Linux ubuntu24 4 vCPU Intel(R) Xeon(R) 6973P-C; RAM 15989 MB |
| containers | every server: `eclipse-temurin:21-jre`, `--cpus=2 --cpuset-cpus=0,1 --memory=6g --memory-swap=6g`, JVM `-Xmx3g -XX:MaxDirectMemorySize=2g`, `MALLOC_ARENA_MAX=4`; load generators in their own container on cpus 2,3 (so the client side has 2 cores too: at 64/128 clients the client can be the limit, see client notes) |
| servers | ours-new = `7562a5bdb7b9`; ours-27f5 = `27f583adccd7`; up-native = `0f77f2cdfa7fa00556ce338723038593e904b066`; up-main = `dbacd8d585bce2ef2a449c821fe3a53cc6060b57` |
| data | TPC-H SF10 Parquet on local disk (load, mixed, heavy, netem) |
| pairs | ours-new (side A) vs one other server (side B) on the same runner, rounds A B / B A / A B |
| load mix | `point_orders`, `point_lineitem`, `count_filter` (every server answers them; upstream has no JDBC prepared statements) |
| settings | `def` = each server's default `duckDbThreads` (ours 4, upstream 2); `t8` = 8 on both; `zstd` = netem path only, up-native with its ZSTD batch compression (`-DflightCompression=zstd`, decoded by ADBC) vs ours plain (up-main has no such option) |

## Setting `def`

### Closed-loop load, JDBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main | 4bb6441569be | d22cdaccb4e1 |
|---|---|---|---|---|---|---|
| 1 | 40 / 20.9 / 44.1 / 54.7 / 0 / 173 / 436 | n/a | 51 / 15.8 / 35.1 / 54.4 / 0 / 168 / 479 | n/a | 49 / 16.5 / 34.7 / 50.5 / 0 / 170 / 428 | n/a |
| 8 | 44 / 184.9 / 276.8 / 324.5 / 0 / 199 / 820 | n/a | 69 / 103.2 / 235.4 / 261.8 / 0 / 197 / 811 | n/a | 53 / 148.5 / 252.0 / 279.6 / 0 / 194 / 776 | n/a |
| 32 | 42 / 741.5 / 1253.1 / 1825.7 / 0 / 183 / 1863 | n/a | 70 / 385.4 / 906.6 / 1015.7 / 0 / 189 / 1737 | n/a | 51 / 632.0 / 1102.1 / 1414.4 / 0 / 185 / 1714 | n/a |
| 64 | 39 / 1518.4 / 2925.7 / 3793.9 / 0 / 182 / 2961 | n/a | 70 / 823.3 / 1881.3 / 2228.1 / 0 / 183 / 2760 | n/a | 49 / 1270.0 / 2388.7 / 2997.7 / 0 / 191 / 2838 | n/a |
| 128 | 35 / 3183.1 / 7232.5 / 9270.5 / 0 / 193 / 4777 | n/a | 70 / 1649.3 / 4053.8 / 5124.1 / 0 / 190 / 4361 | n/a | 47 / 2524.4 / 5418.0 / 7008.3 / 0 / 191 / 4487 | n/a |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | 1 | none | 1 | none | 1 | none |

### Closed-loop load, ADBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main | 4bb6441569be | d22cdaccb4e1 |
|---|---|---|---|---|---|---|
| 1 | 42 / 20.0 / 38.8 / 51.1 / 0 / 164 / 448 | n/a | 57 / 14.5 / 28.8 / 46.1 / 0 / 158 / 476 | n/a | 51 / 16.5 / 32.9 / 42.4 / 0 / 164 / 444 | n/a |
| 8 | 45 / 180.2 / 274.4 / 324.4 / 0 / 204 / 902 | n/a | 70 / 102.6 / 231.1 / 252.9 / 0 / 201 / 835 | n/a | 53 / 150.2 / 252.5 / 278.4 / 0 / 202 / 808 | n/a |
| 32 | 41 / 749.4 / 1316.7 / 2006.2 / 0 / 195 / 1973 | n/a | 71 / 384.1 / 890.8 / 987.2 / 0 / 202 / 1855 | n/a | 51 / 640.9 / 1109.6 / 1372.4 / 0 / 202 / 1861 | n/a |
| 64 | 39 / 1520.8 / 2976.2 / 4303.9 / 0 / 185 / 3485 | n/a | 70 / 841.3 / 1875.8 / 2276.9 / 0 / 195 / 3162 | n/a | 48 / 1297.0 / 2478.0 / 3367.4 / 0 / 195 / 3223 | n/a |
| 128 | 34 / 3277.6 / 6655.2 / 9338.7 / 0 / 183 / 5501 | n/a | 69 / 1674.5 / 3986.3 / 5046.9 / 2 (connect t46: OperationalError: IO: [Flight SQL] failed to up) / 201 / 5036 | n/a | 47 / 2510.6 / 5447.6 / 7022.6 / 0 / 197 / 5229 | n/a |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | 1 | none | 1 | none | 1 | none |

### Mixed load: 32 ADBC small-query clients alone / with 2 heavy SF10 streams (q01, q18)

| metric | ours-new | ours-27f5 | up-native | up-main | 4bb6441569be | d22cdaccb4e1 |
|---|---|---|---|---|---|---|
| small QPS alone | n/a | n/a | n/a | n/a | n/a | n/a |
| small QPS with heavy | n/a | n/a | n/a | n/a | n/a | n/a |
| small p95 ms alone | n/a | n/a | n/a | n/a | n/a | n/a |
| small p95 ms with heavy | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy q01 s (median of runs during the window) | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy q18 s | n/a | n/a | n/a | n/a | n/a | n/a |
| small errors alone / with heavy; heavy failures or wrong answers | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 |

### 4 heavy SF10 queries at once (q01 q09 q18 q21, ADBC) and network-limited client path (netem 10 ms RTT, 1 Gbit/s)

| metric | ours-new | ours-27f5 | up-native | up-main | 4bb6441569be | d22cdaccb4e1 |
|---|---|---|---|---|---|---|
| heavy x4: slowest query s (n/a if any failed) | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy x4: failed or wrong (all rounds) | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy x4: server peak RSS MiB | n/a | n/a | n/a | n/a | n/a | n/a |
| netem: SF10 TPC-H ADBC, sum of warm medians s (correct queries) | n/a | n/a | n/a | n/a | n/a | n/a |
| netem: full lineitem export over ADBC, MB/s | n/a | n/a | n/a | n/a | n/a | n/a |

Not in this run: up-native with its ZSTD Flight compression on the netem path (job `new-vs-native-zstd-netem`).

Not yet in this report: TLS + token on/off for ours.

