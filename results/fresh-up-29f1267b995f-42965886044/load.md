# Server comparison - Report 2: LOAD (compare run 42965886044)

## Setup

| item | value |
|---|---|
| runner | GitHub-hosted `ubuntu-latest`: Linux ubuntu26 4 vCPU AMD EPYC 7763 64-Core Processor; Linux ubuntu26 4 vCPU AMD EPYC 9V74 80-Core Processor; Linux ubuntu26 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C; RAM 15983 MB |
| containers | every server: `eclipse-temurin:21-jre`, `--cpus=2 --cpuset-cpus=0,1 --memory=6g --memory-swap=6g`, JVM `-Xmx3g -XX:MaxDirectMemorySize=2g`, `MALLOC_ARENA_MAX=4`; load generators in their own container on cpus 2,3 (so the client side has 2 cores too: at 64/128 clients the client can be the limit, see client notes) |
| servers | ours-new = `7562a5bdb7b9`; ours-27f5 = `27f583adccd7`; up-native = `46d565e93c19d841ddc0b2cd5811f4cee1c84881`; up-main = `dbacd8d585bce2ef2a449c821fe3a53cc6060b57` |
| data | TPC-H SF10 Parquet on local disk (load, mixed, heavy, netem) |
| pairs | ours-new (side A) vs one other server (side B) on the same runner, rounds A B / B A / A B |
| load mix | `point_orders`, `point_lineitem`, `count_filter` (every server answers them; upstream has no JDBC prepared statements) |
| settings | `def` = each server's default `duckDbThreads` (ours 4, upstream 2); `t8` = 8 on both; `zstd` = netem path only, up-native with its ZSTD batch compression (`-DflightCompression=zstd`, decoded by ADBC) vs ours plain (up-main has no such option) |

## Setting `def`

### Closed-loop load, JDBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main | 29f1267b995f | 29f1267b995f -DresourceProfile=speed | 29f1267b995f CZSTD | 29f1267b995f CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| 1 | n/a | n/a | 44 / 19.6 / 40.2 / 57.8 / 0 / 159 / 416 | n/a | 49 / 16.8 / 34.2 / 43.9 / 0 / 166 / 434 | 49 / 16.8 / 33.7 / 44.1 / 0 / 166 / 432 | n/a | n/a |
| 8 | n/a | n/a | 63 / 116.1 / 251.1 / 274.1 / 0 / 203 / 453 | n/a | 58 / 134.7 / 250.6 / 293.6 / 0 / 201 / 813 | 62 / 123.1 / 271.1 / 305.3 / 0 / 202 / 552 | n/a | n/a |
| 32 | n/a | n/a | 67 / 417.1 / 919.0 / 1028.4 / 0 / 192 / 565 | n/a | 58 / 518.1 / 1034.1 / 1216.8 / 0 / 192 / 1762 | 64 / 442.2 / 982.4 / 1119.1 / 0 / 188 / 610 | n/a | n/a |
| 64 | n/a | n/a | 67 / 855.1 / 1924.2 / 2260.8 / 0 / 196 / 759 | n/a | 56 / 1082.4 / 2138.8 / 2645.7 / 0 / 194 / 2668 | 64 / 925.4 / 1944.5 / 2296.6 / 0 / 197 / 733 | n/a | n/a |
| 128 | n/a | n/a | 65 / 1791.2 / 4065.3 / 5108.4 / 0 / 191 / 927 | n/a | 53 / 2255.0 / 4804.6 / 5929.1 / 0 / 189 / 4310 | 62 / 1861.9 / 4279.7 / 5434.3 / 0 / 192 / 913 | n/a | n/a |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | none | none | 1 | none | 1 | 1 | none | none |

### Closed-loop load, ADBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main | 29f1267b995f | 29f1267b995f -DresourceProfile=speed | 29f1267b995f CZSTD | 29f1267b995f CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| 1 | n/a | n/a | 52 / 15.9 / 30.5 / 53.0 / 0 / 158 / 398 | n/a | 52 / 16.1 / 30.8 / 39.5 / 0 / 161 / 438 | 52 / 16.0 / 30.8 / 39.6 / 0 / 161 / 432 | n/a | n/a |
| 8 | n/a | n/a | 68 / 107.1 / 237.2 / 258.2 / 0 / 202 / 442 | n/a | 59 / 133.8 / 247.9 / 281.8 / 0 / 198 / 949 | 64 / 120.3 / 261.7 / 297.7 / 0 / 200 / 619 | n/a | n/a |
| 32 | n/a | n/a | 67 / 412.9 / 921.3 / 1019.7 / 0 / 198 / 618 | n/a | 56 / 533.3 / 1050.0 / 1244.7 / 0 / 199 / 1822 | 63 / 450.2 / 986.7 / 1115.8 / 0 / 200 / 622 | n/a | n/a |
| 64 | n/a | n/a | 67 / 860.0 / 1913.3 / 2258.4 / 0 / 204 / 806 | n/a | 55 / 1112.4 / 2229.9 / 2733.6 / 0 / 200 / 3104 | 63 / 960.6 / 1961.6 / 2341.1 / 0 / 200 / 762 | n/a | n/a |
| 128 | n/a | n/a | 67 / 1720.5 / 4115.8 / 5190.9 / 0 / 199 / 921 | n/a | 53 / 2247.2 / 4884.1 / 6234.4 / 0 / 200 / 4895 | 63 / 1823.0 / 4335.8 / 5446.2 / 0 / 199 / 923 | n/a | n/a |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | none | none | 1 | none | 1 | 1 | none | none |

### Mixed load: 32 ADBC small-query clients alone / with 2 heavy SF10 streams (q01, q18)

| metric | ours-new | ours-27f5 | up-native | up-main | 29f1267b995f | 29f1267b995f -DresourceProfile=speed | 29f1267b995f CZSTD | 29f1267b995f CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| small QPS alone | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small QPS with heavy | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small p95 ms alone | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small p95 ms with heavy | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy q01 s (median of runs during the window) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy q18 s | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| small errors alone / with heavy; heavy failures or wrong answers | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 |

### 4 heavy SF10 queries at once (q01 q09 q18 q21, ADBC) and network-limited client path (netem 10 ms RTT, 1 Gbit/s)

| metric | ours-new | ours-27f5 | up-native | up-main | 29f1267b995f | 29f1267b995f -DresourceProfile=speed | 29f1267b995f CZSTD | 29f1267b995f CZSTD -DresourceProfile=speed CZSTD |
|---|---|---|---|---|---|---|---|---|
| heavy x4: slowest query s (n/a if any failed) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy x4: failed or wrong (all rounds) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| heavy x4: server peak RSS MiB | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| netem: SF10 TPC-H ADBC, sum of warm medians s (correct queries) | n/a | n/a | 0.0 (0/22 q) | n/a | n/a | n/a | 35.3 (22/22 q) | 35.1 (22/22 q) |
| netem: full lineitem export over ADBC, MB/s | n/a | n/a | 316 | n/a | n/a | n/a | 312 | 310 |

## Netem pairs per job (both sides on the same runner; medians over rounds, B / A per round)

| job | A | B | TPC-H SF10 ADBC s A | B | B / A | export MB/s A | B | B / A | per-round export B / A | queries not ok A / B |
|---|---|---|---|---|---|---|---|---|---|---|
| fu-zstd-netem-local | 29f1267b995f CZSTD | 29f1267b995f CZSTD -DresourceProfile=speed CZSTD | 36.3 | 35.1 | 0.97 | 313 | 310 | 0.99 | 1.08 0.98 0.96 | 0 / 0 |
| fu-zstd-netem-local-vs-up-native | up-native | 29f1267b995f CZSTD | n/a | 35.1 | n/a | 316 | 310 | 0.98 | 1.02 0.97 0.99 | 22 / 0 |

TPC-H n/a = not all 22 queries answered correctly in a round (see 'queries not ok', max over rounds).

Not in this run: up-native with its ZSTD Flight compression on the netem path (job `new-vs-native-zstd-netem`).

Not yet in this report: TLS + token on/off for ours.

