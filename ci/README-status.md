## Server comparison reports (2026-10-27)

- **Report 1 SPEED** - [results/COMPARE-SPEED-2026-10-27.md](results/COMPARE-SPEED-2026-10-27.md): TPC-H SF1/SF10 (ADBC, JDBC,
  local, S3) is answered only by our builds; both upstream builds fail every TPC-H query for server-side reasons (single-table
  schema resolver, unrewritten subquery tables, DECIMAL vs float64 schema, no `AVG` / no prepared statements on up-main), so
  their columns are n/a with the reason. ours-new = ours-27f5 within noise on the same runner (bisect of 4 intermediate
  builds: no regression; the earlier 30-45 % gap was an aggregation artifact). Small queries: up-native has ~25 % lower JDBC
  p50 at c1/c8 but fails at c32; both upstream servers were OOM-killed inside the 6 GB limit in 3 of 6 rounds, ours never
  (peak 1.7-3.2 GB). Parallel raw Flight scans: up-native faster (4-8 streams, up to ~1.8x) at twice the memory.

- **Report 2 LOAD** - [results/COMPARE-LOAD-2026-10-27.md](results/COMPARE-LOAD-2026-10-27.md): on 2 server cores every
  server saturates at 1 client (p95 < 100 ms); throughput at saturation for point / count queries: up-native ~84 QPS, ours-new
  ~50, ours-27f5 ~45, up-main ~48 over ADBC (up-main fails every JDBC query). Only ours runs the heavy parts (mixed, 4 heavy at
  once: 0 failures, peak RSS 4.3 GB). Slow link (10 ms RTT, 1 Gbit/s): up-native with ZSTD exports `lineitem` at 264 MB/s vs
  104 MB/s plain (ours has no Flight compression). TLS + token on ours: latency unchanged, SF10 TPC-H 1.01x, export -11 %.

## In progress

- Server comparison task `ci/COMPARE-TASK.md` (4 servers). `ours-new` is pinned to `7562a5bdb7b9`, the build of the
  first comparison run (workflow input default). Newer pre-releases (`84fec772ec50` and any later one) are
  collected and tested only in a final run after Reports 1-3 (including the S3 read-cache pair). Every server runs in an identically limited
  container (`eclipse-temurin:21-jre`, 2 CPUs on cpus 0,1, 6 GB), clients (now also limited to 6 GB) and S3 in their own
  container on cpus 2,3.
  - Report 1 SPEED: **published** `results/COMPARE-SPEED-2026-10-27.md` (run 40537011671 merged with the ours pairs of
    40490378159; fix list items 1-4 at its top, bisect 40537018532: no build regresses).
  - Report 2 LOAD: **published** `results/COMPARE-LOAD-2026-10-27.md`. Still to add: the TLS closed-loop load job
    `new-plain-vs-tls-load` of run 40550942695 (results/c7-load-tls-40550942695 once its aggregate has committed).
  - Report 3 ROBUSTNESS (all dispatched 17:26-17:33 UTC): `c4-robust` run **40550552130** (rounds 1: 30-min soak, cold
    starts, cancel; all 3 pairs), `c5-threads` run **40550556746** (rounds 3: ours-new duckDbThreads 1/2/4/8, SF1/SF10 ADBC +
    small), `c8-robust-cluster` run **40551320307** (new `cluster` workload: 3 kestrel nodes on one runner, 4 GB / 2 CPUs
    each on cpus 0,1 since 3 x 6 GB does not fit; node 3 stopped before SF10 TPC-H, node 2 SIGKILLed during q18/q21, time until
    node 1 answers q06 correctly again, rejoin times, every check vs the reference answers), `c9-robust-trino` run
    **40551575311** (new `trino` workload: TPC-H SF1 through Trino 455 + the C0fuge/heron connector built read-only by the
    new `trino-plugin` job, answers vs heron's reference via its compare.py; upstream pairs record their failure text).
    The stock Flight SQL JDBC driver TPC-H is the JDBC tables of Report 1 (upstream fails there). Next: when they have
    committed, check `robust.md` / `summary.md` and the job logs (cluster / trino lines are in result.txt), fix failures,
    then write `results/COMPARE-ROBUSTNESS-2026-10-27.md`.
  - `results/c2-speed-40481152975` is only a "no-container reference". `ci/ignored-runs.txt` blocks the aggregates of
    40483119136 (wrong `ours-new`), 40478832460 (old `c1-servers`) and 40539031628 (diagnostic).
