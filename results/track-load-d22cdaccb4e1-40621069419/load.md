# Server comparison - Report 2: LOAD (compare run 40621069419)

## Setup

| item | value |
|---|---|
| runner | GitHub-hosted `ubuntu-latest`: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor; Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor; Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor; Linux ubuntu24 4 vCPU Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz; RAM 15989 MB |
| containers | every server: `eclipse-temurin:21-jre`, `--cpus=2 --cpuset-cpus=0,1 --memory=6g --memory-swap=6g`, JVM `-Xmx3g -XX:MaxDirectMemorySize=2g`, `MALLOC_ARENA_MAX=4`; load generators in their own container on cpus 2,3 (so the client side has 2 cores too: at 64/128 clients the client can be the limit, see client notes) |
| servers | ours-new = `7562a5bdb7b9`; ours-27f5 = `27f583adccd7`; up-native = `a4ebfbc55e2307b3b7fe104be1144ea8f555bbca`; up-main = `dbacd8d585bce2ef2a449c821fe3a53cc6060b57` |
| data | TPC-H SF10 Parquet on local disk (load, mixed, heavy, netem) |
| pairs | ours-new (side A) vs one other server (side B) on the same runner, rounds A B / B A / A B |
| load mix | `point_orders`, `point_lineitem`, `count_filter` (every server answers them; upstream has no JDBC prepared statements) |
| settings | `def` = each server's default `duckDbThreads` (ours 4, upstream 2); `t8` = 8 on both; `zstd` = netem path only, up-native with its ZSTD batch compression (`-DflightCompression=zstd`, decoded by ADBC) vs ours plain (up-main has no such option) |

## Setting `def`

### Closed-loop load, JDBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main | d22cdaccb4e1 | d22cdaccb4e1 CLZ4 | d22cdaccb4e1 CZSTD |
|---|---|---|---|---|---|---|---|
| 1 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 8 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 32 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 64 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 128 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | none | none | none | none | none | none | none |

### Closed-loop load, ADBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main | d22cdaccb4e1 | d22cdaccb4e1 CLZ4 | d22cdaccb4e1 CZSTD |
|---|---|---|---|---|---|---|---|
| 1 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 8 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 32 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 64 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 128 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | none | none | none | none | none | none | none |

### Mixed load: 32 ADBC small-query clients alone / with 2 heavy SF10 streams (q01, q18)

| metric | ours-new | ours-27f5 | up-native | up-main | d22cdaccb4e1 | d22cdaccb4e1 CLZ4 | d22cdaccb4e1 CZSTD |
|---|---|---|---|---|---|---|---|
| small QPS alone | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small QPS with heavy | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small p95 ms alone | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small p95 ms with heavy | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy q01 s (median of runs during the window) | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy q18 s | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small errors alone / with heavy; heavy failures or wrong answers | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 |

### 4 heavy SF10 queries at once (q01 q09 q18 q21, ADBC) and network-limited client path (netem 10 ms RTT, 1 Gbit/s)

| metric | ours-new | ours-27f5 | up-native | up-main | d22cdaccb4e1 | d22cdaccb4e1 CLZ4 | d22cdaccb4e1 CZSTD |
|---|---|---|---|---|---|---|---|
| heavy x4: slowest query s (n/a if any failed) | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy x4: failed or wrong (all rounds) | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy x4: server peak RSS MiB | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| netem: SF10 TPC-H ADBC, sum of warm medians s (correct queries) | 33.3 (22/22 q) | n/a | n/a | n/a | 38.6 (22/22 q) | 29.9 (22/22 q) | 25.2 (22/22 q) |
| netem: full lineitem export over ADBC, MB/s | 104 | n/a | n/a | n/a | 104 | 261 | 357 |

## Setting `zstd`

### Closed-loop load, JDBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main | d22cdaccb4e1 | d22cdaccb4e1 CLZ4 | d22cdaccb4e1 CZSTD |
|---|---|---|---|---|---|---|---|
| 1 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 8 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 32 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 64 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 128 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | none | none | none | none | none | none | none |

### Closed-loop load, ADBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main | d22cdaccb4e1 | d22cdaccb4e1 CLZ4 | d22cdaccb4e1 CZSTD |
|---|---|---|---|---|---|---|---|
| 1 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 8 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 32 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 64 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 128 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | none | none | none | none | none | none | none |

### Mixed load: 32 ADBC small-query clients alone / with 2 heavy SF10 streams (q01, q18)

| metric | ours-new | ours-27f5 | up-native | up-main | d22cdaccb4e1 | d22cdaccb4e1 CLZ4 | d22cdaccb4e1 CZSTD |
|---|---|---|---|---|---|---|---|
| small QPS alone | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small QPS with heavy | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small p95 ms alone | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small p95 ms with heavy | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy q01 s (median of runs during the window) | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy q18 s | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small errors alone / with heavy; heavy failures or wrong answers | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 |

### 4 heavy SF10 queries at once (q01 q09 q18 q21, ADBC) and network-limited client path (netem 10 ms RTT, 1 Gbit/s)

| metric | ours-new | ours-27f5 | up-native | up-main | d22cdaccb4e1 | d22cdaccb4e1 CLZ4 | d22cdaccb4e1 CZSTD |
|---|---|---|---|---|---|---|---|
| heavy x4: slowest query s (n/a if any failed) | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy x4: failed or wrong (all rounds) | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy x4: server peak RSS MiB | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| netem: SF10 TPC-H ADBC, sum of warm medians s (correct queries) | n/a | n/a | 0.0 (0/22 q) | n/a | n/a | 40.3 (22/22 q) | 39.5 (22/22 q) |
| netem: full lineitem export over ADBC, MB/s | n/a | n/a | 257 | n/a | n/a | 260 | 223 |

## Netem pairs per job (both sides on the same runner; medians over rounds, B / A per round)

| job | A | B | TPC-H SF10 ADBC s A | B | B / A | export MB/s A | B | B / A | per-round export B / A | queries not ok A / B |
|---|---|---|---|---|---|---|---|---|---|---|
| i20-lz4-netem-local | ours-new | d22cdaccb4e1 CLZ4 | 33.3 | 33.3 | 1.00 | 104 | 261 | 2.51 | 2.51 2.51 2.51 | 0 / 0 |
| i20-lz4-vs-native-zstd-netem-local | d22cdaccb4e1 CLZ4 | up-native | 40.3 | n/a | n/a | 260 | 256 | 0.99 | 0.99 0.99 0.97 | 0 / 22 |
| i20-native-zstd-netem-local | d22cdaccb4e1 CZSTD | up-native | 39.5 | n/a | n/a | 223 | 260 | 1.16 | 1.15 1.17 1.15 | 0 / 22 |
| i20-plain-netem-local | ours-new | d22cdaccb4e1 | 38.5 | 38.6 | 1.00 | 104 | 104 | 1.00 | 1.00 1.00 1.00 | 0 / 0 |
| i20-zstd-netem-local | ours-new | d22cdaccb4e1 CZSTD | 24.7 | 25.0 | 1.02 | 104 | 361 | 3.46 | 3.43 3.47 3.47 | 0 / 0 |
| i20-zstd-vs-lz4-netem-local | d22cdaccb4e1 CZSTD | d22cdaccb4e1 CLZ4 | 27.0 | 26.1 | 0.97 | 345 | 261 | 0.76 | 0.73 0.76 0.76 | 0 / 0 |

TPC-H n/a = not all 22 queries answered correctly in a round (see 'queries not ok', max over rounds).

Not yet in this report: TLS + token on/off for ours.

