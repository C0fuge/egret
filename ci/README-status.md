## In progress

- Server comparison task `ci/COMPARE-TASK.md` (4 servers). `ours-new` is pinned to `7562a5bdb7b9`, the build of the
  first comparison run (workflow input default). Newer pre-releases (`84fec772ec50` and any later one) are
  collected and tested only in a final run after Reports 1-3 (including the S3 read-cache pair). Every server runs in an identically limited
  container (`eclipse-temurin:21-jre`, 2 CPUs on cpus 0,1, 6 GB), clients (now also limited to 6 GB) and S3 in their own
  container on cpus 2,3.
  - Report 1 SPEED: first run 40490378159 finished; its ours-new vs ours-27f5 jobs are kept, its upstream jobs were
    unusable (every upstream S3 start failed: up-main has no S3 support, up-native needs its hadoop-aws jars and `s3a://`;
    up-main was OOM-killed inside the 6 GB limit after its point queries errored; both up-native local jobs died with
    "runner received a shutdown signal"). Fixed in 5ff4701 / 96c79b5 (also the maintainer fix list items 1-3: JDBC
    answers compared numerically with the DuckDB rows, error texts of failed queries in the job log, up-native jobs in
    def and t8, upstream pairs split into `-tpch` and `-lat` jobs). Rerun of only the upstream pairs: run
    **40537011671** (dispatched 16:02 UTC, up-native = newest head `9fb08d9dd24d`, `merge-run=40490378159` so its
    `speed.md` contains the ours pairs of the first run too).
    Next: read the upstream `-tpch` job logs (`adbc10:` lines now followed by the first FAIL lines and server errors),
    fix the harness if the cause is ours, else record the error as the reason; then copy `speed.md` to
    `results/COMPARE-SPEED-2026-10-27.md` with the bisect result at the top, README summary, own commit.
  - Fix list item 4 (ours-new 30-45 % slower than ours-27f5 on ADBC SF10): wave `c6-bisect`, run **40537018532**
    (5 rounds, ADBC SF10 + small, ours-27f5 vs 45fc0a9e6e02 / e46f28dfdf09 / 6acc9cce0b26 / 7562a5bdb7b9, each pair
    on one runner); its `summary.md` B/A ratios give the first slow build.
  - Report 2 LOAD: run 40490387806 finished (`results/c3-load-40490387806/load.md`); usable for ours and for upstream
    small-query load over ADBC. Upstream TPC-H over ADBC (heavy x4, mixed heavy, netem) failed on both upstream builds and
    up-main failed every JDBC load query: rerun after the cause is known from the speed rerun. Still missing: upstream
    with its ZSTD Flight compression on the netem path and TLS + token on vs off for ours.
  - Report 3 ROBUSTNESS: waves `c4-robust` (dispatch with rounds = 1: 30-min soak, cold starts, cancel) and `c5-threads`
    (rounds = 3) are committed, not yet dispatched; still to build: 3-node cluster and Trino plugin runs (ours only).
  - `results/c2-speed-40481152975` is only a "no-container reference". `ci/ignored-runs.txt` blocks the aggregates of
    40483119136 (wrong `ours-new`) and 40478832460 (old `c1-servers`).
