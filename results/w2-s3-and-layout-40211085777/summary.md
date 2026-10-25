# Wave w2-s3-and-layout, server server-1.0.0-4eaab052deaf, run 40211085777

Ratio = variant / default on the same runner (median of rounds per side). Times: < 1 = variant faster;
scan MB/s: > 1 = variant faster; RSS: < 1 = variant smaller. Absolute default values in the second table.

| variant | storage | layout | flags | rounds A/B | small JDBC c1 p50 | c1 p95 | c32 p95 | ADBC c1 p50 | ADBC c32 p95 | SF1 JDBC | SF10 JDBC | scan MB/s x1 | scan MB/s x4 | heavy4 max | RSS peak | correctness |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| aa-control | s3 | default | `-` | 3/2 | 0.89 | 0.94 | 0.81 | 0.89 | 0.86 | 1.11 | 0.88 | 0.80 | 0.95 | 1.03 | 0.98 | OK |
| efc-on | s3 | default | `-DduckDbExternalFileCache=true` | 3/3 | 0.72 | 0.18 | 0.05 | 0.51 | 0.04 | 0.10 | 0.02 | 1.15 | 1.23 | 0.65 | 2.36 | B: jdbc10 md5 e80d9048a387 (8/22 ok), scan4 rows=168644740 errors=3, scan4 rows=186077316 errors=3, scan4 rows=192172164 errors=3, server died |
| io16 | s3 | default | `-DioParallelism=16` | 3/2 | 0.97 | 0.93 | 0.98 | 0.93 | 1.01 | 0.86 | 1.08 | 0.94 | 1.41 | 1.21 | 1.01 | OK |
| io8 | s3 | default | `-DioParallelism=8` | 3/2 | 0.89 | 0.82 | 1.03 | 1.01 | 0.98 | 0.96 | 1.14 | 1.25 | 0.91 | 1.28 | 1.00 | OK |
| layout-files64m | local | files64m | `-` | 3/3 | 1.02 | 1.00 | 1.06 | 0.98 | 1.24 | 1.03 | 0.99 | 1.00 | 0.97 | 1.04 | 1.00 | OK |
| layout-files64m | s3 | files64m | `-` | 3/2 | 1.31 | 1.00 | 1.06 | 1.59 | 0.86 | 1.01 | 0.99 | 1.03 | 0.60 | 0.78 | 0.98 | OK |
| layout-onefile | local | onefile | `-` | 3/3 | 1.20 | 1.24 | 1.21 | 1.09 | 1.30 | 0.96 | 1.00 | 1.12 | 0.99 | 0.95 | 2.03 | OK |
| layout-onefile | s3 | onefile | `-` | 2/2 | 1.38 | 1.19 | 2.27 | 1.56 | 2.14 | 1.44 | 1.46 | 1.06 | 0.88 | 1.66 | 0.95 | B: adbc32 1 errors |
| layout-rg1m | local | rg1m | `-` | 3/3 | 2.51 | 4.33 | 5.54 | 3.24 | 5.53 | 0.97 | 0.93 | 1.05 | 1.04 | 0.94 | 1.03 | OK |
| layout-rg1m | s3 | rg1m | `-` | 3/2 | 4.73 | 1.37 | 1.16 | 6.21 | 1.44 | 0.66 | 0.52 | 1.05 | 1.09 | 0.31 | 1.02 | OK |
| layout-rg32k | local | rg32k | `-` | 3/3 | 1.31 | 1.59 | 1.70 | 1.31 | 1.74 | 1.13 | 1.09 | 0.98 | 0.98 | 1.07 | 1.35 | OK |
| layout-rg32k | s3 | rg32k | `-` | 1/2 | 3.34 | 2.56 | - | 4.51 | - | 1.34 | - | 0.74 | 0.42 | 3.23 | 1.09 | OK |
| mem1g | s3 | default | `-DduckDbMemoryLimit=1GB` | 3/2 | 0.97 | 0.97 | 0.99 | 0.95 | 0.99 | 1.16 | 1.08 | 0.90 | 1.30 | 1.22 | 0.84 | OK |
| pio-false | s3 | default | `-DduckDbPreserveInsertionOrder=false` | 3/2 | 1.02 | 0.80 | 1.00 | 1.01 | 1.02 | 1.02 | 1.04 | 1.55 | 1.03 | 1.06 | 0.96 | OK |
| s3meta-off | s3 | default | `-DduckDbS3MetadataCache=false` | 3/2 | 1.41 | 0.78 | 0.62 | 1.38 | 0.75 | 0.86 | 0.87 | 0.64 | 0.92 | 1.19 | 1.01 | OK |
| sbs64m | s3 | default | `-DduckDbStreamingBufferSize=64MiB` | 3/2 | 1.00 | 0.90 | 0.99 | 1.11 | 0.96 | 1.21 | 1.18 | 1.30 | 1.01 | 1.18 | 1.00 | OK |
| stand-profile | s3 | default | `-DioParallelism=4 -DduckDbMemoryLimit=1GB -DduckDbThreads=4 -DflightBackpressureThresholdBytes=16777216 -Xmx2g` | 3/2 | 1.06 | 1.07 | 0.88 | 1.15 | 0.86 | 0.99 | 1.32 | 0.60 | 0.93 | 1.18 | 0.91 | OK |
| threads4 | s3 | default | `-DduckDbThreads=4` | 3/2 | 1.02 | 0.76 | 0.98 | 1.23 | 0.91 | 1.11 | 1.22 | 0.79 | 1.02 | 1.41 | 0.93 | OK |
| threads8 | s3 | default | `-DduckDbThreads=8` | 2/2 | 1.12 | 1.25 | 0.75 | 1.03 | 0.69 | 1.41 | 1.43 | 0.24 | 0.95 | 1.18 | 0.92 | OK |

Absolute values (default side A / variant side B; ms, s, MB/s, MB):

| variant | small JDBC c1 p50 | c1 p95 | c32 p95 | ADBC c1 p50 | ADBC c32 p95 | SF1 JDBC | SF10 JDBC | scan MB/s x1 | scan MB/s x4 | heavy4 max | RSS peak |
|---|---|---|---|---|---|---|---|---|---|---|---|
| aa-control | 35.1 / 31.3 | 484.1 / 455.4 | 24669.1 / 19944.7 | 27.6 / 24.5 | 24188.6 / 20714.7 | 30.2 / 33.6 | 360.9 / 317.6 | 321.8 / 256.5 | 668.9 / 632.5 | 83.5 / 86.3 | 3514.0 / 3453.0 |
| efc-on | 32.5 / 23.5 | 744.9 / 134.0 | 15792.3 / 860.1 | 25.8 / 13.1 | 15677.6 / 588.4 | 35.0 / 3.6 | 314.9 / 7.8 | 313.2 / 360.8 | 614.5 / 754.6 | 89.8 / 58.1 | 3452.0 / 8161.0 |
| io16 | 31.8 / 31.0 | 598.0 / 557.2 | 25096.9 / 24664.9 | 27.0 / 25.1 | 24914.8 / 25220.9 | 42.5 / 36.6 | 349.7 / 377.0 | 403.3 / 380.5 | 426.6 / 601.2 | 110.7 / 133.4 | 3404.0 / 3447.0 |
| io8 | 34.8 / 31.1 | 719.0 / 592.8 | 25162.8 / 26031.7 | 26.9 / 27.1 | 25641.7 / 25208.7 | 38.7 / 37.0 | 345.5 / 392.2 | 309.8 / 386.2 | 661.9 / 600.5 | 107.1 / 136.9 | 3405.0 / 3414.0 |
| layout-files64m | 28.7 / 29.2 | 48.8 / 48.9 | 821.1 / 870.8 | 20.4 / 20.1 | 767.9 / 951.0 | 3.5 / 3.6 | 32.8 / 32.3 | 451.2 / 449.5 | 742.1 / 716.2 | 11.3 / 11.7 | 3466.0 / 3467.0 |
| layout-files64m | 31.8 / 41.6 | 569.9 / 571.8 | 19472.9 / 20618.1 | 25.3 / 40.1 | 25160.3 / 21685.0 | 32.5 / 32.9 | 351.4 / 346.2 | 389.5 / 402.5 | 641.3 / 386.2 | 115.5 / 90.5 | 3423.0 / 3345.0 |
| layout-onefile | 20.1 / 24.1 | 36.1 / 44.9 | 547.3 / 664.6 | 13.5 / 14.8 | 485.0 / 628.1 | 2.4 / 2.3 | 21.8 / 21.9 | 634.8 / 707.9 | 1111.0 / 1097.2 | 7.7 / 7.3 | 3362.0 / 6835.0 |
| layout-onefile | 31.4 / 43.3 | 635.1 / 757.5 | 24469.8 / 55532.5 | 27.8 / 43.5 | 24350.5 / 52118.3 | 30.6 / 43.9 | 274.4 / 400.9 | 390.3 / 412.8 | 667.1 / 586.3 | 90.9 / 150.6 | 3377.0 / 3213.0 |
| layout-rg1m | 25.4 / 63.7 | 49.1 / 212.7 | 763.0 / 4228.2 | 18.0 / 58.2 | 746.5 / 4127.5 | 3.5 / 3.4 | 33.4 / 31.0 | 427.3 / 447.5 | 768.1 / 796.1 | 11.1 / 10.5 | 3450.0 / 3551.0 |
| layout-rg1m | 34.4 / 162.7 | 567.4 / 777.2 | 25253.5 / 29342.4 | 24.7 / 153.2 | 24726.0 / 35710.6 | 35.6 / 23.5 | 353.4 / 182.7 | 423.0 / 444.4 | 650.0 / 707.6 | 107.4 / 32.9 | 3451.0 / 3514.0 |
| layout-rg32k | 23.7 / 30.9 | 45.6 / 72.6 | 785.7 / 1338.4 | 17.1 / 22.5 | 740.1 / 1289.5 | 3.2 / 3.6 | 29.9 / 32.5 | 451.8 / 444.9 | 775.3 / 758.1 | 10.3 / 11.0 | 3428.0 / 4618.0 |
| layout-rg32k | 31.8 / 106.1 | 576.9 / 1478.6 | 20030.2 / - | 23.5 / 106.0 | 20033.7 / - | 51.5 / 68.8 | 272.6 / - | 428.1 / 316.3 | 668.1 / 282.8 | 91.0 / 294.2 | 3242.0 / 3534.0 |
| mem1g | 32.9 / 31.8 | 611.5 / 592.5 | 25789.7 / 25565.6 | 30.3 / 28.8 | 25324.0 / 25182.4 | 32.3 / 37.4 | 348.3 / 374.5 | 408.8 / 367.6 | 469.1 / 609.2 | 113.7 / 138.3 | 3426.0 / 2892.0 |
| pio-false | 32.0 / 32.7 | 854.8 / 685.5 | 24994.9 / 25105.5 | 29.9 / 30.2 | 25583.9 / 26016.7 | 37.1 / 37.8 | 341.9 / 356.9 | 240.9 / 373.6 | 644.0 / 666.1 | 108.9 / 115.7 | 3537.0 / 3405.0 |
| s3meta-off | 29.4 / 41.5 | 694.7 / 541.1 | 23119.0 / 14293.8 | 24.3 / 33.5 | 22958.4 / 17161.7 | 35.4 / 30.4 | 374.8 / 327.9 | 403.2 / 256.9 | 761.7 / 701.0 | 72.6 / 86.5 | 3504.0 / 3541.0 |
| sbs64m | 34.0 / 34.1 | 636.8 / 570.8 | 25599.5 / 25217.4 | 27.0 / 30.0 | 25877.2 / 24841.9 | 31.9 / 38.5 | 340.9 / 401.0 | 305.0 / 396.8 | 644.2 / 649.5 | 115.2 / 136.3 | 3444.0 / 3453.0 |
| stand-profile | 30.2 / 32.1 | 741.5 / 796.1 | 25194.7 / 22095.3 | 28.9 / 33.1 | 25405.7 / 21874.6 | 40.3 / 39.8 | 349.4 / 461.5 | 425.1 / 255.9 | 657.5 / 610.3 | 113.9 / 133.8 | 3407.0 / 3104.0 |
| threads4 | 35.5 / 36.1 | 782.5 / 591.5 | 24167.5 / 23682.1 | 28.6 / 35.2 | 24700.6 / 22372.9 | 35.1 / 38.8 | 346.2 / 420.9 | 402.1 / 319.6 | 622.1 / 634.2 | 107.2 / 150.7 | 3397.0 / 3162.0 |
| threads8 | 31.9 / 35.6 | 548.7 / 687.4 | 25270.7 / 18887.6 | 27.4 / 28.2 | 24542.3 / 17032.9 | 25.5 / 36.0 | 350.8 / 500.0 | 310.4 / 74.7 | 652.0 / 620.0 | 88.9 / 105.3 | 3529.0 / 3263.0 |

Notes (added when aggregated by hand; the in-job aggregate could not push: README conflict with the w1 commit, workflow fixed to check out main):
- 13 of the 15 S3 jobs hit the 120-min job limit; the rounds finished before that are used (rounds A/B column).
- S3 on a runner is an `rclone serve s3` emulation on the same 4-cpu VM: SF10 JDBC ~350 s and c32 p95 ~25 s vs ~22-33 s and < 1 s on local files,
  so the S3 rows mostly measure the emulated storage. Only large effects count (aa-control band here 0.80-1.11).
- efc-on (duckDbExternalFileCache=true): 40x faster on the slow S3, but the server grows to the container limit (RSS 8.2 GB) and is OOM-killed,
  JDBC answers missing/wrong -> disqualified as a default; the cache has no memory bound of its own.
- Layout: 1M-row row groups make point/selective queries 2.5-6x slower (no row-group pruning) but heavy S3 queries ~2x faster (fewer requests);
  32k-row groups: small 1.3x slower, RSS 1.35x; one file per table: small concurrency 1.2-2.3x slower, local RSS 2x; 64 MB files: neutral.
