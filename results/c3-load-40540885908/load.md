# Server comparison - Report 2: LOAD (compare run 40540885908)

## Setup

| item | value |
|---|---|
| runner | GitHub-hosted `ubuntu-latest`: Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor; Linux ubuntu24 4 vCPU AMD EPYC 9V45 96-Core Processor; Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor; Linux ubuntu24 4 vCPU INTEL(R) XEON(R) PLATINUM 8573C; Linux ubuntu24 4 vCPU Intel(R) Xeon(R) 6973P-C; Linux ubuntu24 4 vCPU Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz; RAM 15989 MB |
| containers | every server: `eclipse-temurin:21-jre`, `--cpus=2 --cpuset-cpus=0,1 --memory=6g --memory-swap=6g`, JVM `-Xmx3g -XX:MaxDirectMemorySize=2g`, `MALLOC_ARENA_MAX=4`; load generators in their own container on cpus 2,3 (so the client side has 2 cores too: at 64/128 clients the client can be the limit, see client notes) |
| servers | ours-new = `7562a5bdb7b9`; ours-27f5 = `27f583adccd7`; up-native = `30855be44317d344f76d89043f1a6513afe60a8b`; up-main = `dbacd8d585bce2ef2a449c821fe3a53cc6060b57` |
| data | TPC-H SF10 Parquet on local disk (load, mixed, heavy, netem) |
| pairs | ours-new (side A) vs one other server (side B) on the same runner, rounds A B / B A / A B |
| load mix | `point_orders`, `point_lineitem`, `count_filter` (every server answers them; upstream has no JDBC prepared statements) |
| settings | `def` = each server's default `duckDbThreads` (ours 4, upstream 2); `t8` = 8 on both; `zstd` = netem path only, up-native with its ZSTD batch compression (`-DflightCompression=zstd`, decoded by ADBC) vs ours plain (up-main has no such option) |

## Setting `def`

### Closed-loop load, JDBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| 1 | 50 / 16.9 / 34.3 / 42.7 / 0 / 166 / 478 | 45 / 19.0 / 36.5 / 46.3 / 0 / 164 / 423 | 65 / 12.9 / 26.6 / 42.2 / 0 / 163 / 567 | 0 / n/a / n/a / n/a / 551175 (Oct 27, 2026 12:24:01 PM org.apache.arrow.driver.jdbc.shaded) / 94 / 303 |
| 8 | 55 / 145.2 / 226.7 / 269.4 / 0 / 193 / 872 | 51 / 158.8 / 238.6 / 276.0 / 0 / 178 / 863 | 82 / 90.8 / 192.6 / 217.6 / 0 / 188 / 948 | 0 / n/a / n/a / n/a / 1552302 (Oct 27, 2026 12:26:29 PM org.apache.arrow.driver.jdbc.shaded) / 105 / 576 |
| 32 | 52 / 585.8 / 1068.2 / 1498.7 / 0 / 191 / 2049 | 48 / 641.0 / 1108.3 / 1557.4 / 0 / 194 / 1958 | 85 / 334.0 / 732.2 / 829.9 / 0 / 202 / 1832 | 0 / n/a / n/a / n/a / 1920891 (Oct 27, 2026 12:28:57 PM org.apache.arrow.driver.jdbc.shaded) / 107 / 954 |
| 64 | 49 / 1230.4 / 2387.3 / 3044.3 / 0 / 196 / 3429 | 45 / 1351.5 / 2570.6 / 3412.5 / 0 / 191 / 3094 | 84 / 690.2 / 1531.6 / 1898.0 / 0 / 193 / 2920 | 0 / n/a / n/a / n/a / 2023464 (Oct 27, 2026 12:31:26 PM org.apache.arrow.driver.jdbc.shaded) / 103 / 1814 |
| 128 | 42 / 2668.6 / 6292.0 / 8007.6 / 0 / 192 / 5167 | 40 / 2866.2 / 6198.3 / 8962.2 / 0 / 198 / 4869 | 84 / 1340.4 / 3490.4 / 4406.4 / 0 / 193 / 4353 | 0 / n/a / n/a / n/a / 2053482 (Oct 27, 2026 12:33:56 PM org.apache.arrow.driver.jdbc.shaded) / 104 / 3730 |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | 1 | 1 | 1 | none |

### Closed-loop load, ADBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| 1 | 51 / 16.5 / 31.2 / 39.7 / 0 / 165 / 469 | 47 / 18.3 / 32.8 / 41.0 / 0 / 161 / 436 | 72 / 11.7 / 22.7 / 36.5 / 0 / 167 / 524 | 45 / 17.9 / 37.8 / 59.9 / 0 / 176 / 577 |
| 8 | 55 / 147.5 / 225.7 / 265.5 / 0 / 201 / 1030 | 51 / 158.4 / 238.9 / 275.0 / 0 / 202 / 913 | 86 / 87.5 / 183.3 / 203.2 / 0 / 198 / 935 | 50 / 152.0 / 269.4 / 294.0 / 0 / 203 / 966 |
| 32 | 50 / 610.6 / 1109.8 / 1510.1 / 0 / 201 / 2173 | 46 / 661.2 / 1184.7 / 1660.3 / 0 / 190 / 2165 | 85 / 338.9 / 737.9 / 830.8 / 0 / 197 / 1975 | 50 / 632.4 / 1136.9 / 1313.9 / 0 / 201 / 1852 |
| 64 | 47 / 1250.6 / 2576.6 / 3386.7 / 0 / 194 / 3630 | 43 / 1383.1 / 2693.8 / 3536.9 / 0 / 187 / 3497 | 86 / 671.9 / 1572.1 / 1921.5 / 0 / 202 / 3123 | 48 / 1283.1 / 2423.4 / 2905.0 / 0 / 197 / 2927 |
| 128 | 42 / 2722.6 / 5849.5 / 7785.4 / 0 / 196 / 6118 | 40 / 2922.1 / 6269.9 / 7852.3 / 0 / 196 / 5752 | 81 / 1389.5 / 3487.9 / 4545.7 / 0 / 195 / 5228 | 46 / 2533.8 / 5374.4 / 6906.0 / 0 / 203 / 5132 |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | 1 | 1 | 1 | 1 |

### Mixed load: 32 ADBC small-query clients alone / with 2 heavy SF10 streams (q01, q18)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| small QPS alone | 39 | 57 | 49 | 43 |
| small QPS with heavy | 33 | 46 | 45 | 42 |
| small p95 ms alone | 1265.6 | 903.0 | 1233.3 | 1238.5 |
| small p95 ms with heavy | 1529.9 | 1158.6 | 1379.9 | 1323.7 |
| heavy q01 s (median of runs during the window) | 25.92 | 23.64 | n/a | n/a |
| heavy q18 s | 31.55 | 28.04 | n/a | n/a |
| small errors alone / with heavy; heavy failures or wrong answers | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 |

### 4 heavy SF10 queries at once (q01 q09 q18 q21, ADBC) and network-limited client path (netem 10 ms RTT, 1 Gbit/s)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| heavy x4: slowest query s (n/a if any failed) | 16.3 | 11.5 | n/a | n/a |
| heavy x4: failed or wrong (all rounds) | 0 | 0 | 12 | 12 |
| heavy x4: server peak RSS MiB | 4202 | 4158 | 2039 | 2143 |
| netem: SF10 TPC-H ADBC, sum of warm medians s (correct queries) | 40.4 (22/22 q) | 26.8 (22/22 q) | 0.0 (0/22 q) | 0.0 (0/22 q) |
| netem: full lineitem export over ADBC, MB/s | 104 | 104 | 104 | n/a |

## Setting `t8`

### Closed-loop load, JDBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| 1 | 47 / 18.1 / 35.5 / 41.7 / 0 / 167 / 428 | 43 / 20.4 / 38.2 / 44.3 / 0 / 164 / 435 | 57 / 15.7 / 29.7 / 37.4 / 0 / 162 / 500 | 0 / n/a / n/a / n/a / 1125198 (Oct 27, 2026 1:07:28 PM org.apache.arrow.driver.jdbc.shaded.) / 59 / 324 |
| 8 | 55 / 142.5 / 231.9 / 283.2 / 0 / 184 / 920 | 49 / 162.0 / 245.1 / 293.3 / 0 / 178 / 874 | 82 / 93.7 / 167.9 / 225.8 / 0 / 184 / 888 | 0 / n/a / n/a / n/a / 3367509 (Oct 27, 2026 1:09:55 PM org.apache.arrow.driver.jdbc.shaded.) / 95 / 587 |
| 32 | 50 / 607.5 / 1056.2 / 1477.8 / 0 / 190 / 2138 | 45 / 676.5 / 1134.9 / 1750.0 / 0 / 189 / 2047 | 86 / 336.9 / 730.9 / 862.8 / 0 / 201 / 1864 | 0 / n/a / n/a / n/a / 3942006 (Oct 27, 2026 1:12:23 PM org.apache.arrow.driver.jdbc.shaded.) / 100 / 1024 |
| 64 | 46 / 1300.5 / 2458.0 / 3063.0 / 0 / 196 / 3429 | 42 / 1429.1 / 2609.1 / 3326.3 / 0 / 201 / 3205 | 83 / 709.7 / 1581.9 / 1919.7 / 0 / 191 / 2839 | 0 / n/a / n/a / n/a / 4190868 (Oct 27, 2026 1:14:52 PM org.apache.arrow.driver.jdbc.shaded.) / 100 / 2206 |
| 128 | 40 / 2925.8 / 5766.6 / 7561.0 / 0 / 195 / 5493 | 37 / 3200.6 / 6343.7 / 8159.6 / 0 / 201 / 5204 | 82 / 1390.3 / 3470.6 / 4406.4 / 0 / 190 / 4758 | 0 / n/a / n/a / n/a / 3986463 (Oct 27, 2026 1:17:22 PM org.apache.arrow.driver.jdbc.shaded.) / 102 / 3851 |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | 1 | 1 | 1 | none |

### Closed-loop load, ADBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| 1 | 51 / 16.8 / 32.0 / 37.9 / 0 / 166 / 464 | 45 / 19.3 / 34.7 / 40.4 / 0 / 164 / 455 | 63 / 13.9 / 26.0 / 32.7 / 0 / 163 / 475 | 49 / 17.3 / 35.4 / 41.8 / 0 / 172 / 579 |
| 8 | 54 / 145.0 / 232.8 / 280.3 / 0 / 201 / 1000 | 48 / 164.8 / 252.4 / 297.1 / 0 / 201 / 894 | 84 / 91.0 / 165.4 / 220.6 / 0 / 202 / 914 | 53 / 148.4 / 232.6 / 278.1 / 1 (connect t3: OperationalError: IO: [Flight SQL] failed to upd) / 191 / 1041 |
| 32 | 48 / 633.7 / 1131.1 / 1500.2 / 0 / 201 / 2209 | 44 / 691.2 / 1146.0 / 1698.3 / 0 / 201 / 2124 | 86 / 341.2 / 738.4 / 863.5 / 0 / 200 / 2003 | 51 / 596.9 / 1074.1 / 1294.4 / 0 / 196 / 2242 |
| 64 | 45 / 1337.3 / 2533.2 / 3107.1 / 0 / 194 / 3806 | 40 / 1513.0 / 2741.9 / 3616.7 / 0 / 189 / 3715 | 79 / 751.8 / 1617.8 / 2029.8 / 0 / 202 / 2970 | 48 / 1241.1 / 2433.3 / 3013.6 / 0 / 191 / 3508 |
| 128 | 39 / 2923.4 / 6058.8 / 7500.4 / 0 / 196 / 6059 | 35 / 3231.5 / 7169.8 / 8955.0 / 0 / 196 / 5923 | 80 / 1452.3 / 3495.8 / 4563.9 / 0 / 201 / 5549 | 43 / 2714.6 / 5848.2 / 7339.9 / 1 (connect t95: OperationalError: IO: [Flight SQL] failed to up) / 201 / 5279 |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | 1 | 1 | 1 | 1 |

### Mixed load: 32 ADBC small-query clients alone / with 2 heavy SF10 streams (q01, q18)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| small QPS alone | 36 | 33 | 60 | 38 |
| small QPS with heavy | 26 | 23 | 56 | 36 |
| small p95 ms alone | 1353.9 | 1468.2 | 1043.9 | 1315.1 |
| small p95 ms with heavy | 1884.0 | 2042.5 | 1140.1 | 1466.2 |
| heavy q01 s (median of runs during the window) | 19.93 | 25.90 | n/a | n/a |
| heavy q18 s | 27.04 | 27.51 | n/a | n/a |
| small errors alone / with heavy; heavy failures or wrong answers | 0 / 0; 0 | 0 / 0; 0 | 1 / 0; 0 | 0 / 0; 0 |

### 4 heavy SF10 queries at once (q01 q09 q18 q21, ADBC) and network-limited client path (netem 10 ms RTT, 1 Gbit/s)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| heavy x4: slowest query s (n/a if any failed) | 17.9 | 18.0 | n/a | n/a |
| heavy x4: failed or wrong (all rounds) | 0 | 0 | 12 | 12 |
| heavy x4: server peak RSS MiB | 4301 | 4197 | 1779 | 2296 |
| netem: SF10 TPC-H ADBC, sum of warm medians s (correct queries) | 45.8 (22/22 q) | 46.9 (22/22 q) | 0.0 (0/22 q) | 0.0 (0/22 q) |
| netem: full lineitem export over ADBC, MB/s | 104 | 104 | 104 | n/a |

## Setting `zstd`

### Closed-loop load, JDBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| 1 | n/a | n/a | n/a | n/a |
| 8 | n/a | n/a | n/a | n/a |
| 32 | n/a | n/a | n/a | n/a |
| 64 | n/a | n/a | n/a | n/a |
| 128 | n/a | n/a | n/a | n/a |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | none | none | none | none |

### Closed-loop load, ADBC (QPS / p50 / p95 / p99 ms / errors / server CPU % / server mem MiB)

| clients | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| 1 | n/a | n/a | n/a | n/a |
| 8 | n/a | n/a | n/a | n/a |
| 32 | n/a | n/a | n/a | n/a |
| 64 | n/a | n/a | n/a | n/a |
| 128 | n/a | n/a | n/a | n/a |
| **saturation** (highest step with p95 < 100 ms, 0 errors) | none | none | none | none |

### Mixed load: 32 ADBC small-query clients alone / with 2 heavy SF10 streams (q01, q18)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| small QPS alone | n/a | n/a | n/a | n/a |
| small QPS with heavy | n/a | n/a | n/a | n/a |
| small p95 ms alone | n/a | n/a | n/a | n/a |
| small p95 ms with heavy | n/a | n/a | n/a | n/a |
| heavy q01 s (median of runs during the window) | n/a | n/a | n/a | n/a |
| heavy q18 s | n/a | n/a | n/a | n/a |
| small errors alone / with heavy; heavy failures or wrong answers | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 | 0 / 0; 0 |

### 4 heavy SF10 queries at once (q01 q09 q18 q21, ADBC) and network-limited client path (netem 10 ms RTT, 1 Gbit/s)

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| heavy x4: slowest query s (n/a if any failed) | n/a | n/a | n/a | n/a |
| heavy x4: failed or wrong (all rounds) | n/a | n/a | n/a | n/a |
| heavy x4: server peak RSS MiB | n/a | n/a | n/a | n/a |
| netem: SF10 TPC-H ADBC, sum of warm medians s (correct queries) | 38.6 (22/22 q) | n/a | 0.0 (0/22 q) | n/a |
| netem: full lineitem export over ADBC, MB/s | 104 | n/a | 264 | n/a |

Not yet in this report: TLS + token on/off for ours.

