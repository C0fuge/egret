## In progress

- Server comparison task `ci/COMPARE-TASK.md` (4 servers). `ours-new` is pinned to `7562a5bdb7b9`, the build of the
  first comparison run (workflow input default). Newer pre-releases (`84fec772ec50` and any later one) are
  collected and tested only in a final run after Reports 1-3 (including the S3 read-cache pair). Every server runs in an identically limited
  container (`eclipse-temurin:21-jre`, 2 CPUs on cpus 0,1, 6 GB), clients and S3 in their own container on cpus 2,3.
  - Report 1 SPEED: `compare` wave `c2-speed`, run **40490378159** (dispatched 10:41 UTC with `ours-new=7562a5bdb7b9`).
    When it is done: check `results/c2-speed-40490378159/` for failed or n/a TPC-H queries, then copy `speed.md` to
    `results/COMPARE-SPEED-2026-10-27.md`, add a README summary, own commit. Artifacts can't be downloaded from the agent
    sandbox (blob host blocked); the job log prints per-round results.
  - Report 2 LOAD: wave `c3-load`, run **40490387806** (same `ours-new`, queued behind the speed run; aggregate writes
    `load.md`). Still missing: upstream with its ZSTD Flight compression on the netem path (option name: `COMPRESSION.txt`
    in the upstream build artifact / log) and TLS + token on vs off for ours.
  - Report 3 ROBUSTNESS: waves `c4-robust` (dispatch with rounds = 1: 30-min soak, cold starts, cancel) and `c5-threads`
    (rounds = 3) are committed, not yet dispatched; still to build: 3-node cluster and Trino plugin runs (ours only).
  - Cancelled runs kept running because the `ab` and `aggregate` jobs were gated with `if: always()`, which GitHub
    keeps running after a cancel (fixed in 69b8543: `!cancelled()`; runs dispatched before that can't be stopped and
    run to the end). Still running from before the fix: 40483119136 (`ours-new` = `84fec772ec50` by mistake: delete
    `results/c2-speed-40483119136` when its aggregate commits it, never use it), 40481152975 (no-container reference with
    `7562a5bdb7b9`: keep `results/c2-speed-40481152975` only as "no-container reference"; its two up-native local jobs died
    with "runner received a shutdown signal" during the up-native side, 22 min into round 1), 40478832460 (old
    `c1-servers`, only its aggregate left: delete `results/c1-servers-40478832460` if it appears). Runs 40481883941 and
    40482405265 failed (client image build), 40485420552 was cancelled before it started.
