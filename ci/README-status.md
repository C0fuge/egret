## In progress

- Server comparison task `ci/COMPARE-TASK.md` (4 servers; `ours-new` resolved at dispatch to `84fec772ec50`, a newer
  pre-release than the `7562a5bdb7b9` named in the task - check whether it is the S3 read-cache build of the "Later
  addition"; if it is, the cache pair is `84fec772ec50` vs `7562a5bdb7b9`). Every server runs in an identically
  limited container (`eclipse-temurin:21-jre`, 2 CPUs on cpus 0,1, 6 GB), clients and S3 in their own container on cpus 2,3.
  - Report 1 SPEED: `compare` wave `c2-speed`, run **40483119136** (started 09:55 UTC). When it is done: copy
    `results/c2-speed-40483119136/speed.md` to `results/COMPARE-SPEED-2026-10-27.md`, add a README summary, own commit.
  - Report 2 LOAD: wave `c3-load`, run **40485420552** (queued behind the speed run; aggregate writes `load.md`). Still
    missing: upstream with its ZSTD Flight compression on the netem path (option name: `COMPRESSION.txt` in the upstream
    build artifact / log) and TLS + token on vs off for ours.
  - Report 3 ROBUSTNESS: waves `c4-robust` (dispatch with rounds = 1: 30-min soak, cold starts, cancel) and `c5-threads`
    (rounds = 3) are committed, not yet dispatched; still to build: 3-node cluster and Trino plugin runs (ours only).
  - Runs 40481883941 and 40482405265 failed (client image build) and were cancelled; 40481152975 (no-container
    reference, same wave, dispatched before the container rule) and 40478832460 (old `c1-servers`) were cancelled but
    GitHub still shows them running and they hold runner slots.
