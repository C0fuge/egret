# Wave w3-combos-c3b2, server c3b276054cc3, run 40232144198

Ratio = variant / default on the same runner (median of rounds per side). Times: < 1 = variant faster;
scan MB/s: > 1 = variant faster; RSS: < 1 = variant smaller. Absolute default values in the second table.

| variant | storage | layout | flags | rounds A/B | small JDBC c1 p50 | c1 p95 | c32 p95 | ADBC c1 p50 | ADBC c32 p95 | SF1 JDBC | SF10 JDBC | scan MB/s x1 | scan MB/s x4 | heavy4 max | RSS peak | correctness |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| aa-control | local | default | `-` | 3/3 | 1.04 | 0.97 | 1.04 | 1.04 | 1.01 | 1.03 | 1.00 | 0.99 | 1.01 | 1.03 | 0.98 | OK |
| eps2-bp16m | local | default | `-DendpointsPerServer=2 -DflightBackpressureThresholdBytes=16777216` | 3/3 | 1.04 | 1.05 | 1.02 | 1.04 | 0.99 | 0.99 | 1.01 | 0.96 | 1.00 | 1.00 | 1.02 | OK |
| eps4-default-bp | local | default | `-DendpointsPerServer=4` | 3/3 | 1.04 | 1.06 | 0.99 | 1.04 | 1.01 | 1.02 | 1.01 | 1.00 | 1.00 | 1.00 | 0.98 | OK |
| t4-mem1g | local | default | `-DduckDbThreads=4 -DduckDbMemoryLimit=1GB` | 3/3 | 1.03 | 1.00 | 1.00 | 1.04 | 1.08 | 0.84 | 0.76 | 0.94 | 0.99 | 1.10 | 1.05 | OK |
| t8-mem2g | local | default | `-DduckDbThreads=8 -DduckDbMemoryLimit=2GB` | 3/3 | 1.01 | 0.90 | 1.05 | 1.04 | 1.03 | 0.86 | 0.73 | 1.00 | 0.95 | 0.99 | 1.11 | OK |
| threads4 | local | default | `-DduckDbThreads=4` | 3/3 | 1.03 | 0.92 | 1.02 | 1.07 | 0.95 | 0.86 | 0.75 | 1.01 | 0.98 | 0.97 | 0.91 | OK |
| threads8 | local | default | `-DduckDbThreads=8` | 3/3 | 1.04 | 0.90 | 1.06 | 0.99 | 0.99 | 0.91 | 0.75 | 1.01 | 0.97 | 0.98 | 0.97 | OK |

Absolute values (default side A / variant side B; ms, s, MB/s, MB):

| variant | small JDBC c1 p50 | c1 p95 | c32 p95 | ADBC c1 p50 | ADBC c32 p95 | SF1 JDBC | SF10 JDBC | scan MB/s x1 | scan MB/s x4 | heavy4 max | RSS peak |
|---|---|---|---|---|---|---|---|---|---|---|---|
| aa-control | 22.9 / 23.8 | 44.6 / 43.3 | 755.3 / 784.6 | 16.3 / 17.0 | 732.8 / 740.8 | 3.2 / 3.3 | 30.4 / 30.4 | 472.7 / 466.9 | 769.8 / 778.3 | 10.0 / 10.3 | 3430.0 / 3367.0 |
| eps2-bp16m | 24.5 / 25.5 | 44.6 / 47.0 | 748.8 / 761.7 | 17.4 / 18.0 | 722.6 / 715.5 | 3.4 / 3.4 | 31.3 / 31.5 | 459.2 / 441.7 | 803.7 / 801.0 | 10.3 / 10.3 | 3411.0 / 3463.0 |
| eps4-default-bp | 17.0 / 17.6 | 32.8 / 34.7 | 618.4 / 613.7 | 12.3 / 12.8 | 562.3 / 567.8 | 2.6 / 2.6 | 24.4 / 24.5 | 587.0 / 586.0 | 992.3 / 996.7 | 8.5 / 8.5 | 3499.0 / 3427.0 |
| t4-mem1g | 26.6 / 27.4 | 48.8 / 48.8 | 885.0 / 887.5 | 18.5 / 19.3 | 843.9 / 914.5 | 3.6 / 3.0 | 35.6 / 26.9 | 399.7 / 375.8 | 603.8 / 600.0 | 12.8 / 14.1 | 3387.0 / 3573.0 |
| t8-mem2g | 18.0 / 18.2 | 34.1 / 30.8 | 583.1 / 611.9 | 13.1 / 13.6 | 516.7 / 532.0 | 2.7 / 2.3 | 24.9 / 18.3 | 557.4 / 559.0 | 867.8 / 828.5 | 8.5 / 8.3 | 3456.0 / 3847.0 |
| threads4 | 20.7 / 21.4 | 39.7 / 36.6 | 747.8 / 763.0 | 15.4 / 16.5 | 721.3 / 686.6 | 3.1 / 2.6 | 29.1 / 21.8 | 488.0 / 491.3 | 804.4 / 788.1 | 9.6 / 9.2 | 3481.0 / 3167.0 |
| threads8 | 22.6 / 23.5 | 44.2 / 39.6 | 754.4 / 800.6 | 17.1 / 16.9 | 715.4 / 708.7 | 3.1 / 2.9 | 29.5 / 22.0 | 464.2 / 469.7 | 778.9 / 753.0 | 9.8 / 9.6 | 3371.0 / 3282.0 |
