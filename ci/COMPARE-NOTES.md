# Addendum to the 2026-10-27 server comparison task (maintainer)

1. Add a fourth server: upstream `main` at `dbacd8d585bc` (the fork point), built the same way as the upstream branch
   (read-only checkout, shaded jar). Same caveats: TPC-H-only data dir, `tpch.`-qualified queries, no JDBC prepared
   statements, `LIMIT` without `ORDER BY` returns the whole table. Pair it with 45fc on the workloads it answers
   correctly; mark the rest n/a.
2. Record every metric that can be collected in the same runs, so nothing has to be re-run later. Keep the raw per-run
   files as artifacts and summarize them in `results/`:
   - per query and per client count: every sample (cold + warm), p50 / p95 / p99 / max, errors with their text;
   - TPC-H per query times and checksums, SF1 and SF10;
   - scan throughput (rows/s, MB/s) at 1 / 4 / 8 streams where the server supports it;
   - server process: peak RSS, heap used/committed, direct memory, GC count and time, CPU time (user/sys), threads;
   - bytes sent over Flight, record batches, rows per query;
   - server start time (until the port answers) and the first-query time;
   - server logs (WARN/ERROR excerpts) and the exact JVM flags and settings used;
   - runner: CPU model, cores, memory, kernel, JDK, DuckDB version reported by each server.
3. Load / throughput (maintainer, 2026-10-27). For every server, on the workloads it answers correctly:
   - closed-loop small-query load at 1 / 8 / 32 / 64 / 128 concurrent clients (point lookups, filtered count; JDBC and
     ADBC), 60 s per step after a 10 s warm-up: queries per second, p50 / p95 / p99, error rate, server CPU and RSS;
   - the saturation point: the highest client count / QPS where p95 stays under 100 ms and errors stay at 0;
   - mixed load: 32 small-query clients plus 2 heavy TPC-H streams (q01, q18) at the same time - small-query QPS and
     p95 with and without the heavy streams, and the heavy queries' times;
   - report QPS ratios between servers per step and the saturation points side by side.
