# Wave w0-smoke, server 4eaab052deaf, run 40210310231

Ratio = variant / default on the same runner (median of rounds per side). Times: < 1 = variant faster;
scan MB/s: > 1 = variant faster; RSS: < 1 = variant smaller. Absolute default values in the second table.

| variant | storage | layout | flags | rounds A/B | small JDBC c1 p50 | c1 p95 | c32 p95 | ADBC c1 p50 | ADBC c32 p95 | SF1 JDBC | SF10 JDBC | scan MB/s x1 | scan MB/s x4 | heavy4 max | RSS peak | correctness |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| aa-control | local | default | `-` | 1/1 | 0.98 | 0.99 | 1.06 | 1.02 | 0.94 | 1.00 | 0.98 | 0.98 | 1.00 | 1.01 | 0.96 | OK |
| threads4 | local | default | `-DduckDbThreads=4` | 1/1 | 0.87 | 0.78 | 1.05 | 0.97 | 1.01 | 0.82 | 0.66 | 1.01 | 0.99 | 0.95 | 0.91 | OK |

Absolute values (default side A / variant side B; ms, s, MB/s, MB):

| variant | small JDBC c1 p50 | c1 p95 | c32 p95 | ADBC c1 p50 | ADBC c32 p95 | SF1 JDBC | SF10 JDBC | scan MB/s x1 | scan MB/s x4 | heavy4 max | RSS peak |
|---|---|---|---|---|---|---|---|---|---|---|---|
| aa-control | 21.3 / 21.0 | 40.7 / 40.2 | 636.3 / 671.4 | 15.2 / 15.5 | 623.5 / 588.5 | 3.1 / 3.1 | 28.7 / 28.2 | 459.8 / 450.3 | 771.1 / 770.6 | 9.0 / 9.1 | 3516.0 / 3359.0 |
| threads4 | 17.1 / 14.9 | 31.0 / 24.0 | 479.1 / 503.1 | 10.6 / 10.3 | 450.7 / 456.2 | 2.1 / 1.7 | 19.8 / 13.1 | 785.9 / 790.3 | 1259.2 / 1246.0 | 6.6 / 6.2 | 3500.0 / 3191.0 |
