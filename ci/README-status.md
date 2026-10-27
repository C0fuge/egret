## In progress

- Server comparison task `ci/COMPARE-TASK.md` (4 servers). `ours-new` is pinned to `7562a5bdb7b9`, the build of the
  first comparison run (workflow input default). The newer pre-release `84fec772ec50` is not `ours-new`; if it is the S3
  read-cache build, it is the `ours-cache` side of the later S3-only pair. Every server runs in an identically limited
  container (`eclipse-temurin:21-jre`, 2 CPUs on cpus 0,1, 6 GB), clients and S3 in their own container on cpus 2,3.
  - Report 1 SPEED: `compare` wave `c2-speed`, run **40483119136** (started 09:55 UTC; at 10:35 2 of 16 jobs done,
    `def-tpch-local` and `def-lat-local`, both green). When it is done: check `results/c2-speed-40483119136/` for failed
    or n/a TPC-H queries first (the `def-tpch-local` job took only ~2.5 min per side for SF10 JDBC+ADBC and SF1 on
    2 CPUs, which looks short), then copy `speed.md` to `results/COMPARE-SPEED-2026-10-27.md`, add a README summary,
    own commit. Artifacts can't be downloaded from the agent sandbox (blob host blocked); runs from commit 8c8db96 on
    print per-round results in the job log.
  - Report 2 LOAD: wave `c3-load`, run **40485420552** (queued behind the speed run; aggregate writes `load.md`). Still
    missing: upstream with its ZSTD Flight compression on the netem path (option name: `COMPRESSION.txt` in the upstream
    build artifact / log) and TLS + token on vs off for ours.
  - Report 3 ROBUSTNESS: waves `c4-robust` (dispatch with rounds = 1: 30-min soak, cold starts, cancel) and `c5-threads`
    (rounds = 3) are committed, not yet dispatched; still to build: 3-node cluster and Trino plugin runs (ours only).
  - Runs 40481883941 and 40482405265 failed (client image build) and were cancelled; 40481152975 (no-container
    reference, same wave, dispatched before the container rule) and 40478832460 (old `c1-servers`) were cancelled but
    GitHub still shows them running and they hold runner slots.
