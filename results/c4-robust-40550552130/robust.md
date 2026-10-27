# Server comparison - Report 3: ROBUSTNESS (compare run 40550552130)

Same runner type and containers as Reports 1 and 2 (server: `eclipse-temurin:21-jre`, 2 CPUs on cpus 0,1, 6 GB, `-Xmx3g -XX:MaxDirectMemorySize=2g`; clients on cpus 2,3). Servers: ours-new = `7562a5bdb7b9`; ours-27f5 = `27f583adccd7`; up-native = `202b4cef8a395c5ab62456e75fcc027f6f998683`; up-main = `dbacd8d585bce2ef2a449c821fe3a53cc6060b57`.

## Soak: 30 min, 32 ADBC small-query clients + 1 heavy SF10 stream

| metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| RSS MiB at start | 316 | 304 | 292 | 322 |
| RSS MiB at end | 1993 | 1916 | 2918 | 4628 |
| RSS MiB max | 2863 | 2568 | 2922 | 4628 |
| heap used MiB max | 224 | 191 | 248 | 296 |
| GC count (30 min) | 246 | 229 | 443 | 345 |
| GC time s | 25.2 | 28.4 | 37.8 | 33.7 |
| threads max | 274 | 259 | 119 | 226 |
| small QPS (median segment) | 46 | 30 | 70 | 72 |
| small p95 ms, first 5 min | 1227.1 | 1677.7 | 867.3 | 800.3 |
| small p95 ms, last 5 min | 1329.4 | 1990.8 | 846.9 | 828.1 |
| heavy q01 s (median) | 20.9 | 37.1 | n/a | n/a |
| heavy q18 s (median) | 25.4 | 22.3 | n/a | n/a |
| errors: small / heavy failed / server died | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 5398 / 0 | 1 / 6498 / 0 |

Direct (off-heap) memory is not sampled separately (no NMT in the measured JVM): RSS minus heap is the off-heap estimate.

## Cold start (SF10 data dir, 5 starts per round)

| metric (median) | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| port answers, ms after `docker run` | 4113 (n=15) | 4119 (n=5) | 2788 (n=4) | 4080 (n=5) |
| 'started' log line, ms | 4150 (n=15) | 4152 (n=5) | 2809 (n=5) | 4112 (n=5) |
| first query (connect + SELECT version()), ms | 590 (n=15) | 563 (n=5) | 518 (n=5) | 723 (n=5) |
| idle RSS MiB, 5 s after first query | 315 (n=15) | 290 (n=5) | 307 (n=5) | 319 (n=5) |

## Cancel a running SF10 query after 1 s (ADBC `adbc_cancel`)

| query | metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|---|
| q18 | client returns, s after cancel | 0.00 | 0.00 | n/a | n/a |
| q18 | server CPU < 0.1 core, s after cancel | 0.19 | 0.26 | n/a | n/a |
| q18 | outcome | cancelled, finished (detail=) | cancelled | error (detail=InternalError: INTERNAL: [FlightSQL] Failed to prepare Flight S) | error (detail=InternalError: INTERNAL: [FlightSQL] Error getting Arrow schema) |
| q21 | client returns, s after cancel | 0.00 | 0.00 | n/a | n/a |
| q21 | server CPU < 0.1 core, s after cancel | 0.20 | 0.13 | n/a | n/a |
| q21 | outcome | cancelled | cancelled | error (detail=InternalError: INTERNAL: [FlightSQL] Failed to prepare Flight S) | error (detail=InternalError: INTERNAL: [FlightSQL] Error getting Arrow schema) |
| lagg | client returns, s after cancel | n/a | n/a | n/a | n/a |
| lagg | server CPU < 0.1 core, s after cancel | n/a | n/a | n/a | n/a |
| lagg | outcome | n/a | n/a | n/a | n/a |

Not in this run (ours only, next session): 3-node cluster on one runner (node stopped before / killed during a query),
Trino SF1 through our plugin, stock Flight SQL JDBC driver TPC-H SF1 (see Report 1 JDBC tables: upstream fails there).

