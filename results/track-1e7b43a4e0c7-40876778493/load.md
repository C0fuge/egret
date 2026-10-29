# Server comparison - Report 2: LOAD (compare run 40876778493)

## Setup

| item | value |
|---|---|
| runner | GitHub-hosted `ubuntu-latest`: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor; Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor; Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor; RAM 15983 MB |
| containers | every server: `eclipse-temurin:21-jre`, `--cpus=2 --cpuset-cpus=0,1 --memory=6g --memory-swap=6g`, JVM `-Xmx3g -XX:MaxDirectMemorySize=2g`, `MALLOC_ARENA_MAX=4`; load generators in their own container on cpus 2,3 (so the client side has 2 cores too: at 64/128 clients the client can be the limit, see client notes) |
| servers | ours-new = `7562a5bdb7b9`; ours-27f5 = `27f583adccd7`; up-native = `9fb08d9dd24df3cb838a3172f9375560bb6dc70a`; up-main = `dbacd8d585bce2ef2a449c821fe3a53cc6060b57` |
| data | TPC-H SF10 Parquet on local disk (load, mixed, heavy, netem) |
| pairs | ours-new (side A) vs one other server (side B) on the same runner, rounds A B / B A / A B |
| load mix | `point_orders`, `point_lineitem`, `count_filter` (every server answers them; upstream has no JDBC prepared statements) |
| settings | `def` = each server's default `duckDbThreads` (ours 4, upstream 2); `t8` = 8 on both; `zstd` = netem path only, up-native with its ZSTD batch compression (`-DflightCompression=zstd`, decoded by ADBC) vs ours plain (up-main has no such option) |

## Setting `def`

### Closed-loop load, JDBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main | 1e7b43a4e0c7 | 1e7b43a4e0c7 CZSTD |
|---|---|---|---|---|---|---|
| 1 | n/a | n/a | n/a | n/a | n/a | n/a |
| 8 | n/a | n/a | n/a | n/a | n/a | n/a |
| 32 | n/a | n/a | n/a | n/a | n/a | n/a |
| 64 | n/a | n/a | n/a | n/a | n/a | n/a |
| 128 | n/a | n/a | n/a | n/a | n/a | n/a |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | none | none | none | none | none | none |

### Closed-loop load, ADBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main | 1e7b43a4e0c7 | 1e7b43a4e0c7 CZSTD |
|---|---|---|---|---|---|---|
| 1 | n/a | n/a | n/a | n/a | n/a | n/a |
| 8 | n/a | n/a | n/a | n/a | n/a | n/a |
| 32 | n/a | n/a | n/a | n/a | n/a | n/a |
| 64 | n/a | n/a | n/a | n/a | n/a | n/a |
| 128 | n/a | n/a | n/a | n/a | n/a | n/a |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | none | none | none | none | none | none |

### Mixed load: 32 ADBC small-query clients alone / with 2 heavy SF10 streams (q01, q18)

| metric | ours-new | ours-27f5 | up-native | up-main | 1e7b43a4e0c7 | 1e7b43a4e0c7 CZSTD |
|---|---|---|---|---|---|---|
| small QPS alone | n/a | n/a | n/a | n/a | n/a | n/a |
| small QPS with heavy | n/a | n/a | n/a | n/a | n/a | n/a |
| small p95 ms alone | n/a | n/a | n/a | n/a | n/a | n/a |
| small p95 ms with heavy | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy q01 s (median of runs during the window) | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy q18 s | n/a | n/a | n/a | n/a | n/a | n/a |
| small errors alone / with heavy; heavy failures or wrong answers | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 |

### 4 heavy SF10 queries at once (q01 q09 q18 q21, ADBC) and network-limited client path (netem 10 ms RTT, 1 Gbit/s)

| metric | ours-new | ours-27f5 | up-native | up-main | 1e7b43a4e0c7 | 1e7b43a4e0c7 CZSTD |
|---|---|---|---|---|---|---|
| heavy x4: slowest query s (n/a if any failed) | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy x4: failed or wrong (all rounds) | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy x4: server peak RSS MiB | n/a | n/a | n/a | n/a | n/a | n/a |
| netem: SF10 TPC-H ADBC, sum of warm medians s (correct queries) | 40.6 (22/22 q) | n/a | 0.0 (0/22 q) | n/a | n/a | 42.6 (22/22 q) |
| netem: full lineitem export over ADBC, MB/s | 104 | n/a | 260 | n/a | n/a | 250 |

## Netem pairs per job (both sides on the same runner; medians over rounds, B / A per round)

| job | A | B | TPC-H SF10 ADBC s A | B | B / A | export MB/s A | B | B / A | per-round export B / A | queries not ok A / B |
|---|---|---|---|---|---|---|---|---|---|---|
| fin-zstd-netem-local | ours-new | 1e7b43a4e0c7 CZSTD | 40.6 | 42.6 | 1.05 | 104 | 250 | 2.40 | 2.54 2.40 2.37 | 0 / 0 |
| fin-zstd-netem-local-vs-up-native | up-native | 1e7b43a4e0c7 CZSTD | n/a | 42.6 | n/a | 260 | 250 | 0.96 | 1.03 0.96 0.95 | 22 / 0 |

TPC-H n/a = not all 22 queries answered correctly in a round (see 'queries not ok', max over rounds).

Not in this run: up-native with its ZSTD Flight compression on the netem path (job `new-vs-native-zstd-netem`).

Not yet in this report: TLS + token on/off for ours.

