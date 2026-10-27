# Server comparison - Report 3: ROBUSTNESS (compare run 40551848571)

Same runner type and containers as Reports 1 and 2 (server: `eclipse-temurin:21-jre`, 2 CPUs on cpus 0,1, 6 GB, `-Xmx3g -XX:MaxDirectMemorySize=2g`; clients on cpus 2,3). Servers: ours-new = `7562a5bdb7b9`; ours-27f5 = `27f583adccd7`; up-native = `202b4cef8a395c5ab62456e75fcc027f6f998683`; up-main = `dbacd8d585bce2ef2a449c821fe3a53cc6060b57`.

## Cold start (SF10 data dir, 5 starts per round)

| metric (median) | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|
| port answers, ms after `docker run` | 4577 (n=43) | 4622 (n=14) | 4115 (n=15) | 4333 (n=13) |
| 'started' log line, ms | 4612 (n=45) | 4664 (n=15) | 4151 (n=15) | 4151 (n=15) |
| first query (connect + SELECT version()), ms | 638 (n=45) | 673 (n=15) | 786 (n=15) | 816 (n=15) |
| idle RSS MiB, 5 s after first query | 312 (n=45) | 310 (n=15) | 305 (n=15) | 320 (n=15) |

## Cancel a running SF10 query after 1 s (ADBC `adbc_cancel`)

| query | metric | ours-new | ours-27f5 | up-native | up-main |
|---|---|---|---|---|---|
| q18 | client returns, s after cancel | 0.00 | 0.00 | n/a | n/a |
| q18 | server CPU < 0.1 core, s after cancel | 0.00 | 0.03 | n/a | n/a |
| q18 | outcome | cancelled | cancelled | error (detail=InternalError: INTERNAL: [FlightSQL] Failed to prepare Flight S) | error (detail=InternalError: INTERNAL: [FlightSQL] Error getting Arrow schema) |
| q21 | client returns, s after cancel | 0.00 | 0.00 | n/a | n/a |
| q21 | server CPU < 0.1 core, s after cancel | 0.00 | 0.00 | n/a | n/a |
| q21 | outcome | cancelled | cancelled | error (detail=InternalError: INTERNAL: [FlightSQL] Failed to prepare Flight S) | error (detail=InternalError: INTERNAL: [FlightSQL] Error getting Arrow schema) |
| lagg | client returns, s after cancel | 0.00 | 0.00 | 0.00 | 0.00 |
| lagg | server CPU < 0.1 core, s after cancel | 0.00 | 0.02 | 6.67 | 10.63 |
| lagg | outcome | cancelled | cancelled | cancelled | cancelled |

Not in this run (ours only, next session): 3-node cluster on one runner (node stopped before / killed during a query),
Trino SF1 through our plugin, stock Flight SQL JDBC driver TPC-H SF1 (see Report 1 JDBC tables: upstream fails there).

