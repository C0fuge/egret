# Server comparison - Report 2: LOAD (compare run 43148390757)

## Setup

| item | value |
|---|---|
| runner | GitHub-hosted `ubuntu-latest`: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor; Linux ubuntu26 4 vCPU AMD EPYC 9V45 96-Core Processor; Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor; Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C; Linux ubuntu26 4 vCPU Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz; RAM 15983 MB |
| containers | every server: `eclipse-temurin:21-jre`, `--cpus=2 --cpuset-cpus=0,1 --memory=6g --memory-swap=6g`, JVM `-Xmx3g -XX:MaxDirectMemorySize=2g`, `MALLOC_ARENA_MAX=4`; load generators in their own container on cpus 2,3 (so the client side has 2 cores too: at 64/128 clients the client can be the limit, see client notes) |
| servers | ours-new = `7562a5bdb7b9`; ours-27f5 = `27f583adccd7`; up-native = `cfaa929746cbf9ba9f6134cbf0c5a9683b2c1e92`; up-main = `dbacd8d585bce2ef2a449c821fe3a53cc6060b57` |
| data | TPC-H SF10 Parquet on local disk (load, mixed, heavy, netem) |
| pairs | ours-new (side A) vs one other server (side B) on the same runner, rounds A B / B A / A B |
| load mix | `point_orders`, `point_lineitem`, `count_filter` (every server answers them; upstream has no JDBC prepared statements) |
| settings | `def` = each server's default `duckDbThreads` (ours 4, upstream 2); `t8` = 8 on both; `zstd` = netem path only, up-native with its ZSTD batch compression (`-DflightCompression=zstd`, decoded by ADBC) vs ours plain (up-main has no such option) |

## Setting `def`

### Closed-loop load, JDBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main | 74464701e372 | 74464701e372 -DresourceProfile=speed | 74464701e372 CZSTD | 74464701e372 CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| 1 | n/a | n/a | 49 / 16.7 / 36.6 / 55.9 / 0 / 166 / 430 | n/a | 54 / 15.0 / 32.3 / 41.8 / 0 / 170 / 439 | 53 / 15.2 / 32.5 / 41.8 / 0 / 170 / 439 | n/a | n/a |
| 8 | n/a | n/a | 66 / 109.5 / 247.0 / 267.6 / 0 / 197 / 462 | n/a | 61 / 128.1 / 242.9 / 285.2 / 0 / 195 / 848 | 65 / 114.4 / 264.7 / 303.9 / 0 / 199 / 570 | n/a | n/a |
| 32 | n/a | n/a | 68 / 401.9 / 914.7 / 1010.9 / 0 / 192 / 595 | n/a | 60 / 501.3 / 1006.2 / 1182.3 / 0 / 186 / 1692 | 67 / 420.1 / 968.9 / 1089.3 / 0 / 191 / 611 | n/a | n/a |
| 64 | n/a | n/a | 68 / 836.9 / 1903.0 / 2244.0 / 0 / 186 / 753 | n/a | 57 / 1055.3 / 2113.4 / 2636.3 / 0 / 194 / 2787 | 66 / 881.2 / 1967.2 / 2340.0 / 0 / 202 / 825 | n/a | n/a |
| 128 | n/a | n/a | 68 / 1713.8 / 3996.5 / 5041.3 / 0 / 201 / 906 | n/a | 55 / 2157.7 / 4708.2 / 5972.6 / 0 / 195 / 4440 | 65 / 1796.9 / 4217.8 / 5353.0 / 0 / 200 / 833 | n/a | n/a |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | none | none | 1 | none | 1 | 1 | none | none |

### Closed-loop load, ADBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main | 74464701e372 | 74464701e372 -DresourceProfile=speed | 74464701e372 CZSTD | 74464701e372 CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| 1 | n/a | n/a | 56 / 14.6 / 28.6 / 48.5 / 0 / 162 / 410 | n/a | 55 / 14.8 / 30.0 / 38.2 / 0 / 161 / 440 | 55 / 14.8 / 30.2 / 39.7 / 0 / 160 / 440 | n/a | n/a |
| 8 | n/a | n/a | 70 / 101.3 / 233.3 / 253.7 / 0 / 203 / 421 | n/a | 61 / 128.3 / 245.2 / 279.8 / 0 / 202 / 857 | 67 / 111.7 / 261.9 / 298.7 / 0 / 202 / 563 | n/a | n/a |
| 32 | n/a | n/a | 69 / 401.7 / 920.1 / 1026.8 / 0 / 197 / 668 | n/a | 58 / 508.7 / 1028.4 / 1197.2 / 0 / 197 / 1808 | 66 / 430.2 / 967.5 / 1080.0 / 0 / 194 / 674 | n/a | n/a |
| 64 | n/a | n/a | 70 / 814.0 / 1865.2 / 2229.7 / 0 / 195 / 800 | n/a | 56 / 1068.3 / 2196.8 / 2707.3 / 0 / 194 / 3154 | 66 / 878.9 / 1940.3 / 2277.8 / 0 / 196 / 822 | n/a | n/a |
| 128 | n/a | n/a | 68 / 1715.2 / 4041.4 / 4983.2 / 0 / 203 / 1052 | n/a | 54 / 2158.5 / 4775.0 / 6034.7 / 0 / 200 / 5017 | 65 / 1806.2 / 4133.5 / 5204.4 / 0 / 200 / 834 | n/a | n/a |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | none | none | 1 | none | 1 | 1 | none | none |

### Mixed load: 32 ADBC small-query clients alone / with 2 heavy SF10 streams (q01, q18)

| metric | ours-new | ours-27f5 | up-native | up-main | 74464701e372 | 74464701e372 -DresourceProfile=speed | 74464701e372 CZSTD | 74464701e372 CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| small QPS alone | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small QPS with heavy | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small p95 ms alone | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small p95 ms with heavy | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy q01 s (median of runs during the window) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy q18 s | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small errors alone / with heavy; heavy failures or wrong answers | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 |

### 4 heavy SF10 queries at once (q01 q09 q18 q21, ADBC) and network-limited client path (netem 10 ms RTT, 1 Gbit/s)

| metric | ours-new | ours-27f5 | up-native | up-main | 74464701e372 | 74464701e372 -DresourceProfile=speed | 74464701e372 CZSTD | 74464701e372 CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| heavy x4: slowest query s (n/a if any failed) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy x4: failed or wrong (all rounds) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy x4: server peak RSS MiB | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| netem: SF10 TPC-H ADBC, sum of warm medians s (correct queries) | n/a | n/a | 0.0 (0/22 q) | n/a | n/a | n/a | 38.7 (22/22 q) | 38.2 (22/22 q) |
| netem: full lineitem export over ADBC, MB/s | n/a | n/a | 270 | n/a | n/a | n/a | 263 | 265 |

## Netem pairs per job (both sides on the same runner; medians over rounds, B / A per round)

| job | A | B | TPC-H SF10 ADBC s A | B | B / A | export MB/s A | B | B / A | per-round export B / A | queries not ok A / B |
|---|---|---|---|---|---|---|---|---|---|---|
| fu-zstd-netem-local | 74464701e372 CZSTD | 74464701e372 CZSTD -DresourceProfile=speed CZSTD | 39.6 | 38.2 | 0.97 | 259 | 265 | 1.02 | 1.00 1.02 1.03 | 0 / 0 |
| fu-zstd-netem-local-vs-up-native | up-native | 74464701e372 CZSTD | n/a | 38.2 | n/a | 270 | 265 | 0.98 | 0.99 0.98 0.98 | 22 / 0 |

TPC-H n/a = not all 22 queries answered correctly in a round (see 'queries not ok', max over rounds).

Not in this run: up-native with its ZSTD Flight compression on the netem path (job `new-vs-native-zstd-netem`).

Not yet in this report: TLS + token on/off for ours.

