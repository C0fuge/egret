## In progress

- Server comparison task `ci/COMPARE-TASK.md` (4 servers). `ours-new` is pinned to `7562a5bdb7b9`, the build of the
  first comparison run (workflow input default). Newer pre-releases (`84fec772ec50` and any later one) are
  collected and tested only in a final run after Reports 1-3 (including the S3 read-cache pair). Every server runs in an identically limited
  container (`eclipse-temurin:21-jre`, 2 CPUs on cpus 0,1, 6 GB), clients (now also limited to 6 GB) and S3 in their own
  container on cpus 2,3.
  - Report 1 SPEED: first run 40490378159 finished; its ours-new vs ours-27f5 jobs are kept, its upstream jobs were
    unusable (every upstream S3 start failed: up-main has no S3 support, up-native needs its hadoop-aws jars and `s3a://`;
    up-main was OOM-killed inside the 6 GB limit after its point queries errored; both up-native local jobs died with
    "runner received a shutdown signal"). Fixed in 5ff4701 / 96c79b5 / 3802b4c / 14899cd (also the maintainer fix list
    items 1-3: JDBC answers compared numerically with the DuckDB rows, every failed query with its error text in the job
    log and in the report notes, up-native jobs in def and t8, upstream pairs split into `-tpch` and `-lat` jobs).
    Rerun of only the upstream pairs: run **40537011671** (dispatched 16:02 UTC, up-native = head `9fb08d9dd24d`,
    `merge-run=40490378159`, so its `speed.md` contains the ours pairs of the first run too; S3 and `-lat` jobs take
    ~1.5-3 h). Its aggregate commits `results/c2-speed-40537011671/`.
  - Upstream TPC-H over ADBC (fix list item 2, from the local `-tpch` jobs of 40537011671 and the 1-round diagnostic
    40539031628): every query fails on both upstream builds, for server-side reasons, so they are n/a with the reason:
    multi-table queries are rejected by upstream's schema resolver (`Can only select from ONE table`, on Prepare and on
    plain ExecuteQuery alike: upstream runs TPC-H only behind Spark, which does the joins); q04-style subqueries reach
    DuckDB with the table not rewritten (`schema "tpch" does not exist`); q06 returns DECIMAL(38,4) where the advertised
    schema says float64, which ADBC rejects; up-main also has no `AVG` (`Column 'avg(l_quantity)' not found`).
  - Next: when 40537011671 has committed its results, check `speed.md` (up-native small/scan local and S3, up-main
    small/scan local), copy it to `results/COMPARE-SPEED-2026-10-27.md` with the bisect result (below) and the upstream
    TPC-H reasons at the top, add a README summary, own commit. If an up-native `-lat` local job dies again with a runner
    shutdown, its log now shows the last workload and the host's free memory before it.
  - Fix list item 4 done, run 40537018532 (`results/c6-bisect-40537018532/summary.md`, 5 rounds, each build vs
    ours-27f5 on one runner): ADBC SF10 sum of medians B / A = 45fc0a9e6e02 1.00, e46f28dfdf09 0.98, 6acc9cce0b26
    1.00, 7562a5bdb7b9 1.01; small ADBC c1 p50 0.90-1.01 (newer builds equal or faster). **No build regresses.** The
    30-45 % gap of the first speed report was an aggregation artifact (its ours-new column pooled jobs from other runners
    and CPU types, ours-27f5 came from its own pair job only); the speed report now prints the same-runner
    ours-27f5 / ours-new ratio under each TPC-H table. Put this at the top of Report 1.
  - up-main small/scan (`-lat` jobs of 40537011671): JDBC point / count / LIMIT queries fail at once (no prepared
    statements), metadata answers, and the server is OOM-killed (exit 137) inside its 6 GB limit during the ADBC c1
    small queries in every round, so its scans are n/a too (a result, limit not raised).
  - Report 2 LOAD: ZSTD run 40540885908 finished (`results/c3-load-40540885908/load.md`, merged with 40490387806):
    netem 10 ms / 1 Gbit/s full lineitem export over ADBC: up-native with ZSTD 264 MB/s vs ours-new plain 104 MB/s.
    Publish it as `results/COMPARE-LOAD-2026-10-27.md` after Report 1. Earlier: run 40490387806 finished (`results/c3-load-40490387806/load.md`); usable for ours and for upstream
    small-query load over ADBC (upstream TPC-H in heavy x4 / mixed / netem fails for the reasons above; up-main fails
    every JDBC load query). TLS + token for ours still to build: the
    server takes `FLIGHT_TLS_CERT` / `FLIGHT_TLS_KEY` (PEM files) and `FLIGHT_BEARER_TOKEN` (without
    `FLIGHT_ALLOW_INSECURE`); clients then need `grpc+tls://` with the self-signed CA (ADBC) and
    `useEncryption=true&token=...` (JDBC); ab.sh hardcodes the client URIs today.
  - Report 3 ROBUSTNESS: waves `c4-robust` (dispatch with rounds = 1: 30-min soak, cold starts, cancel) and `c5-threads`
    (rounds = 3) are committed, not yet dispatched; still to build: 3-node cluster and Trino plugin runs (ours only).
  - `results/c2-speed-40481152975` is only a "no-container reference". `ci/ignored-runs.txt` blocks the aggregates of
    40483119136 (wrong `ours-new`), 40478832460 (old `c1-servers`) and 40539031628 (diagnostic).
