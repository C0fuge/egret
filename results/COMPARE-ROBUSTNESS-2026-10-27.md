# Server comparison - Report 3: ROBUSTNESS (2026-10-27)

Sources: soak run 40550552130 (`c4-robust`, rounds 1), cold start + cancel run [40551848571](c4-robust-40551848571/robust.md)
(rounds 3), threads sweep [40550556746](c5-threads-40550556746/summary.md), Trino run [40551575311](c9-robust-trino-40551575311/summary.md),
3-node cluster run Three kestrel nodes in three containers on one runner (each 2 CPUs on cpus 0,1 and 4 GB, `-Xmx2g
-XX:MaxDirectMemorySize=1g`: three 6 GB containers do not fit in the runner's 16 GB), Hazelcast on 5701-5703, Flight on
32010-32012; data = SF10 on the runner's S3 (rclone). On local disks the cluster refuses complete answers by design
(`NOT_IMPLEMENTED: A complete answer needs storage every node can read (HDFS, S3)`, first attempt run 40551320307), so the
cluster runs on S3. Every check = ADBC TPC-H SF10 22 queries through node 1, answers vs the in-process DuckDB reference.
Run 40553385813, 1 round per build, same runner (AMD EPYC):

| step | ours-new `7562a5bdb7b9` | ours-27f5 `27f583adccd7` |
|---|---|---|
| cluster start, all 3 nodes logged "started" | 16.6 s | 16.1 s |
| all 3 up: answers / wall | 22/22 correct, 268 s | 22/22 correct, 260 s |
| node 3 stopped (`docker stop`, graceful 0.8-1.0 s) right before the run | 22/22 correct, 283 s | 22/22 correct, 249 s |
| node 3 back (new container) until "started" | 4.4 s | 5.0 s |
| all 3 up again | 22/22 correct, 294 s | 22/22 correct, 252 s |
| node 2 SIGKILLed 3 s into a q18 + q21 run | q18 ok, q21 ok (both answered) | q18 ok, q21 ok |
| first correct q06 through node 1 after the kill | 54.4 s after the kill (first attempt, made after the q18 + q21 run returned) | 47.7 s (same) |
| node 2 dead: full run | 22/22 correct, 242 s | 22/22 correct, 352 s |
| node 2 back (new container) until "started" | 4.2 s | 4.2 s |
| all 3 up again | 22/22 correct, 254 s | 22/22 correct, 396 s |
| OOM kills / server deaths | 0 | 0 |

No wrong or failed answer in any state, and no query failed when a node was killed under it. The "time to recover" here is
an upper bound: the first probe after the kill already answered correctly, so the cluster was usable no later than the end
of the killed run (the probe could only start after it). Wall times on one runner with three nodes sharing 2 cores and S3
are not speed numbers. Upstream: n/a (no tested multi-node mode; Report 1 shows it cannot answer the TPC-H set at all)._RUN. Same containers as Reports 1 and 2 (server `eclipse-temurin:21-jre`, 2 CPUs on cpus 0,1,
6 GB, `-Xmx3g -XX:MaxDirectMemorySize=2g`; clients on cpus 2,3). Servers: ours-new = `7562a5bdb7b9`, ours-27f5 =
`27f583adccd7`, up-native = `202b4cef8a39` (upstream head at dispatch), up-main = `dbacd8d585bc`.

## Summary

- **Soak 30 min** (32 small clients + heavy SF10 stream): no server died, no OOM kill, 0 small-query errors for our builds;
  ours settles at ~2 GB RSS (peak 2.9 GB, heap <= 224 MiB), p95 drift last / first 5 min 1.08x (ours-new). Upstream
  cannot run the heavy stream (fails in a loop), so its higher small QPS comes without the heavy load; up-main's RSS was
  still rising at the end (4.6 GB).
- **Cold start**: port answers after 4.1-4.6 s for every server; first query 0.64 s ours-new vs 0.79-0.82 s upstream; idle
  RSS ~300-320 MiB for all.
- **Cancel**: ours stops server work at once (CPU below 0.1 core within one 0.25 s sample) on SF10 q18, q21 and a single-table
  aggregation; upstream returns the client call at once but keeps computing for 6.7 s (up-native) / 10.6 s (up-main).
- **3-node cluster (ours, S3)**: 22/22 correct with all nodes up, with one node stopped, and after one node was SIGKILLed
  mid-query (the running q18 / q21 still answered); restarted nodes rejoin in 4-5 s.
- **Trino 455 + our connector, TPC-H SF1**: 22/22 correct on all four servers (Trino does the joins, so upstream works this
  way); ours 0.7-3 % faster on the same runner.
- **duckDbThreads** (ours-new, 2-core container): 2 threads give 20-26 % lower p50 for 8-32 concurrent small queries at equal
  SF10 time; 1 thread halves small-query p50 under concurrency but makes SF10 1.37x slower; 8 threads changes little.

## 30-min soak under mixed load (32 ADBC small-query clients + 1 heavy stream q01 / q18)

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

Read: the upstream heavy stream fails at once on every query (q01 / q18: `AVG` / multi-table, Report 1) and restarts in a tight
loop (5398 / 6498 failed runs), so upstream served the small queries **without** the heavy load ours carried (ours ran the
heavy SF10 queries correctly the whole time, 0 errors): its higher small QPS is not like for like. Memory: ours settles at
~2 GB RSS after the 2.9 GB peak (heap <= 224 MiB, the rest is DuckDB / Arrow off-heap); up-main ends at its maximum 4.6 GB
(still rising at the end of 30 min); up-native ends at 2.9 GB. Latency drift (p95 last / first 5 min): ours-new 1.08x,
ours-27f5 1.19x, up-native 0.98x, up-main 1.04x. No server died, no OOM kill.

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

On upstream, q18 / q21 cannot be cancelled because they never start (multi-table queries are rejected, Report 1). The
single-table `lagg` (`SELECT l_orderkey, l_partkey, sum(l_extendedprice * (1 - l_discount)), count(*) FROM tpch.lineitem GROUP BY
1, 2 ORDER BY 3 DESC, 1, 2 LIMIT 20`, SF10) runs on every server: the client call returns at once everywhere, but **upstream's
server process keeps working for 6.7 s (up-native) and 10.6 s (up-main) after the cancel** (CPU sampled every 0.25 s until
it stays below 0.1 core for 1 s); ours stops within one sample. The first cancel run 40550552130 (cancel after 3 s) is
superseded: ours finished SF10 q18 in under 3 s there.

## Trino 455 + our connector (C0fuge/heron `f3800e8f9b8d`), TPC-H SF1, local

Trino in the client container (cpus 2,3, 6 GB, `-Xmx3G`), catalog `arrow_flight` on the server under test; 2 runs per query
(cold, warm), answers of the first run checked by the connector's `compare.py` against its DuckDB reference. Times are per
query wall time of `trino --execute` (includes ~2 s CLI start per query), so only the comparison on one runner is meaningful.

| pair (same runner) | A ours-new: answers, cold sum s, warm sum s | B: answers, cold sum s, warm sum s |
|---|---|---|
| ours-new vs ours-27f5 (EPYC 9V74) | 22/22 OK, 62.69, 54.20 | ours-27f5: 22/22 OK, 63.77, 54.57 |
| ours-new vs up-native (EPYC 7763) | 22/22 OK, 84.46, 72.52 | up-native: 22/22 OK, 87.04, 74.80 |
| ours-new vs up-main (EPYC 7763) | 22/22 OK, 81.71, 69.75 | up-main: 22/22 OK, 84.20, 70.37 |

Through Trino every server answers TPC-H SF1 correctly: Trino sends single-table scans with pushed-down filters and does the
joins itself, which is the workload upstream was written for. Ours is 0.7-3 % faster on the same runner here (cold and warm sums).

Stock Flight SQL JDBC driver (18.0.0) TPC-H SF1 / SF10: Report 1 JDBC tables. Ours 22/22 correct; upstream n/a there (the
driver prepares every statement; upstream's TPC-H failures over ADBC are listed at the top of Report 1).

## 3-node cluster on one runner (ours only)

Three kestrel nodes in three containers on one runner (each 2 CPUs on cpus 0,1 and 4 GB, `-Xmx2g
-XX:MaxDirectMemorySize=1g`: three 6 GB containers do not fit in the runner's 16 GB), Hazelcast on 5701-5703, Flight on
32010-32012; data = SF10 on the runner's S3 (rclone). On local disks the cluster refuses complete answers by design
(`NOT_IMPLEMENTED: A complete answer needs storage every node can read (HDFS, S3)`, first attempt run 40551320307), so the
cluster runs on S3. Every check = ADBC TPC-H SF10 22 queries through node 1, answers vs the in-process DuckDB reference.
Run 40553385813, 1 round per build, same runner (AMD EPYC):

| step | ours-new `7562a5bdb7b9` | ours-27f5 `27f583adccd7` |
|---|---|---|
| cluster start, all 3 nodes logged "started" | 16.6 s | 16.1 s |
| all 3 up: answers / wall | 22/22 correct, 268 s | 22/22 correct, 260 s |
| node 3 stopped (`docker stop`, graceful 0.8-1.0 s) right before the run | 22/22 correct, 283 s | 22/22 correct, 249 s |
| node 3 back (new container) until "started" | 4.4 s | 5.0 s |
| all 3 up again | 22/22 correct, 294 s | 22/22 correct, 252 s |
| node 2 SIGKILLed 3 s into a q18 + q21 run | q18 ok, q21 ok (both answered) | q18 ok, q21 ok |
| first correct q06 through node 1 after the kill | 54.4 s after the kill (first attempt, made after the q18 + q21 run returned) | 47.7 s (same) |
| node 2 dead: full run | 22/22 correct, 242 s | 22/22 correct, 352 s |
| node 2 back (new container) until "started" | 4.2 s | 4.2 s |
| all 3 up again | 22/22 correct, 254 s | 22/22 correct, 396 s |
| OOM kills / server deaths | 0 | 0 |

No wrong or failed answer in any state, and no query failed when a node was killed under it. The "time to recover" here is
an upper bound: the first probe after the kill already answered correctly, so the cluster was usable no later than the end
of the killed run (the probe could only start after it). Wall times on one runner with three nodes sharing 2 cores and S3
are not speed numbers. Upstream: n/a (no tested multi-node mode; Report 1 shows it cannot answer the TPC-H set at all).

## duckDbThreads sweep (ours-new; A = default 4 threads, B = 1 / 2 / 8; ratios B / A, < 1 = B faster)

| job | A | B | storage | runner | rounds A/B | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC (sum of medians) | TPC-H SF10 ADBC (sum of medians) | TPC-H SF10 JDBC (sum of medians) | lineitem scan x1 | disqualified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| threads-4-vs-1-local | ours-new `-` | ours-new `-DduckDbThreads=1` | local | Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | 0.86 | 0.88 | 0.91 | 0.90 | 1.23 | 1.37 | n/a | n/a | none |
| threads-4-vs-2-local | ours-new `-` | ours-new `-DduckDbThreads=2` | local | Linux ubuntu24 4 vCPU AMD EPYC 7763 64-Core Processor | 3/3 | 0.91 | 0.89 | 0.99 | 0.99 | 0.92 | 0.99 | n/a | n/a | none |
| threads-4-vs-8-local | ours-new `-` | ours-new `-DduckDbThreads=8` | local | Linux ubuntu24 4 vCPU AMD EPYC 9V74 80-Core Processor | 3/3 | 1.08 | 0.98 | 1.06 | 1.02 | 1.04 | 1.03 | n/a | n/a | none |

Read: on 2 server cores, fewer threads help many concurrent small queries (c8 / c32 p50 0.47-0.56x at 1 thread, 0.74-0.80x
at 2 threads) and cost heavy queries (SF10 1.37x slower at 1 thread, 0.99x at 2); 8 threads changes little (0.98-1.08).
2 threads is the best size-aware default for a 2-core container serving mostly small queries; 4 stays right for mixed or
heavy use. Upstream: n/a (its thread knob is not the subject here).
