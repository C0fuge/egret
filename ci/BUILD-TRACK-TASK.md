# Build tracking task, from 2026-10-28 (maintainer) - starts after COMPARE-TASK.md says ALL DONE

Purpose: every new server pre-release that closes a development item is measured against the **baseline
`7562a5bdb7b9`** (the presented build) on the SAME runner, with the container limits of `COMPARE-TASK.md`
("Containers" section: 2 CPUs pinned, 6 GB, `-Xmx3g`, direct 2g, clients and S3 on other cores). Reuse the compare
workflow, the upstream builds and the report scripts already in the repo.

## Which builds
- Candidates: pre-releases `server-1.0.0-<sha12>` of the server repo newer than the last tracked build, whose release
  notes or the server repo's `docs/dev/STATUS.md` Log line name a stage-3 item (20 compression, 21 small-query load, 22
  multi-stream scan, 18 distributed complete, 17 S3 cache) or any runtime change. Skip docs/test-only builds. If several
  wait, measure the newest one (it contains the others) and note the skipped ones.
- One build per session; record each in `results/BUILDS.md`.

## What to run per build (pairs on one runner: candidate vs 7562a5bdb7b9; 3 rounds, alternate order)
1. Core (always): TPC-H SF1 + SF10 over ADBC and JDBC (answers checked, 22/22), small queries p50/p95/p99 at 1, 8 and 32
   clients, scans 1/4/8 streams, local Parquet and S3 (MinIO).
2. Targeted, by the item the build closes:
   - item 20: slow link (netem 10 ms, 1 Gbit), with and without compression requested by the client, both codecs, plus
     upstream native with its ZSTD as the reference (264 MB/s in Report 2).
   - item 21: closed-loop load 1-128 clients (queries/s, saturation point), upstream native as the reference (~84 q/s).
   - item 22: scan 4 and 8 streams with peak RSS, upstream native as the reference (807-823 MB/s).
   - item 18: 3-node cluster on S3, heavy JDBC queries with `distributedComplete=true` vs false, answers = single node.
   - item 17: S3 cache on/off pair (as `c10-cache`).
3. Every run records everything (`COMPARE-TASK.md` "Every run records everything"); raw files as artifacts.

## Output
- `results/BUILDS.md`: one row per build: date, build, items, then candidate/baseline ratios (SF10 ADBC total, SF10 JDBC
  total, small c1 p50, c32 p95, QPS at saturation, scan 8 streams MB/s, slow-link MB/s where run), correctness (22/22),
  peak RSS, verdict (better / same / worse / wrong answers). Keep a short "Key builds" list at the top: only builds that
  clearly improved something, with one line each on what changed - the maintainer's final report takes only these.
- A per-build summary `results/track-<sha12>/summary.md` with the full tables.
- A regression (>5 % slower on a core metric in all 3 rounds) or any wrong answer: put it at the top of BUILDS.md in bold
  and add a line to README 'In progress'.

## Rules
As `COMPARE-TASK.md` "Rules": no overlap with another session (README 'In progress' commit < 15 min -> wait), ~90 minutes
per session, README 'In progress' updated with running CI ids and the next step before stopping, commit as C0fuge with
the noreply address, never personal data, host names or internal names, never push to the upstream repository. If no
untracked build is waiting, write one line "idle <UTC time>, newest tracked <sha12>" in README 'In progress' (replace the
previous idle line) and stop immediately.

## FINAL (maintainer, 2026-10-29 15:30) - one last build, then stop
The final server pre-release is **`server-1.0.0-1e7b43a4e0c7`** (finish mode; contains every item since 7562a5bdb7b9).
Track it as usual, but as a **three-way** run on the same runner: final build vs `7562a5bdb7b9` vs **upstream native**
(the upstream build used in Reports 1-3). Core set (section 1) plus slow-link with ZSTD (item 20) and scan 4/8 streams
(item 22); 3 rounds, alternate order, answers checked. Output: `results/FINAL-1e7b43a4e0c7.md` - one table per area
with final/7562 and final/upstream ratios, correctness, peak RSS, a short verdict, and the "Key builds" list from
BUILDS.md copied at the top. Then write "EGRET FINAL DONE" in README 'In progress' and stop; no further builds.

## ITEM 23 (maintainer, 2026-10-29 22:10) - after "EGRET FINAL DONE"
When a server pre-release newer than `1e7b43a4e0c7` whose STATUS Log names item 23 (`resourceProfile=speed`) exists:
one three-way run on the same runner: that build with `-DresourceProfile=speed` vs the same build default (balanced)
vs upstream native `9fb08d9dd24d`. Same containers and core set as FINAL (TPC-H SF1/SF10 ADBC+JDBC local+S3, small
queries 1/8/32, scans 1/4/8 + export, slow link with ZSTD) plus closed-loop load 1-128 clients; peak RSS and CPU for
every job. Output `results/ITEM23-<sha12>.md`: speed/balanced and speed/upstream ratios, memory cost per area, verdict
(where speed reaches or passes upstream, and at what memory). Then "EGRET ITEM 23 DONE" in README 'In progress' and stop.

## ITEM 23b (maintainer, 2026-10-30 14:40) - after "EGRET ITEM 23 DONE"
When a server pre-release newer than `d752a7358a65` whose STATUS names item 23b exists: re-run `i23-small` (S3 and
local as a control) and `i23-load` three-way as in ITEM 23 on that build. Output `results/ITEM23b-<sha12>.md`: errors
per concurrency (speed must have 0 at 32 clients on S3), speed/balanced and speed/upstream ratios, peak RSS. If no such
build exists yet, write the idle line and stop. Then "EGRET ITEM 23b DONE" in README 'In progress' and stop.

## FRESH UPSTREAM TRACKING (maintainer, 2026-11-03) - replaces the idle rule
For every new kestrel pre-release (newer than `57e054887f7a`) whose STATUS Log names item 26 or 27 or a connector-
relevant change: one three-way run like wave `fresh-up-fc-f06b5834e76e` (copy it as `fresh-up-<id>.json`): A = the
pre-release default, B = the pre-release `-DresourceProfile=speed` (file cache is in the profile since 57e054887f7a, no
extra flag), C = upstream native at the head of `feat/starrocks-native-integration` resolved at dispatch (input
`upstream-ref`). Output `results/FRESH-<id>.md`: per area speed/balanced, speed/upstream, balanced/upstream, memory,
correctness, and the upstream commit measured. If nothing new is waiting, write the idle line and stop.
Note (maintainer, 2026-11-03): items 29 and 30 change only the HDFS path with protected DataNodes (SASL), which these
waves do not exercise (local disk and S3). Do NOT start a FRESH wave for a pre-release whose new Log entries are only
items 29/30; write the idle line instead. `FRESH-413485ba80fd` stays the current measurement for local and S3.
Maintainer, 2026-11-04: `FRESH-413485ba80fd` is accepted as the final FRESH result for item 30 (`d2313a9eb651`).

## SASL HDFS ACCEPTANCE (maintainer, 2026-11-05 00:10) - first, before anything else
The server lane's own CI cells passed builds that the maintainer's local stand then failed (they used schema-qualified
names, 4-file tables, few endpoints). Build an **independent acceptance check in this repo**, written from the test
list below, not from kestrel's cells, so it runs in the cloud on every server pre-release and the maintainer's laptop
is no longer needed for it. Correctness only, not speed.
- New workflow `.github/workflows/accept-hdfs.yml` (workflow_dispatch, input `server-ref` = pre-release tag). Infra may
  reuse kestrel's service-hdfs images/scripts (check out kestrel at the pre-release commit for them), the queries,
  data layout and checks must be this repo's (`ci/accept/`).
- Cluster: Hadoop 3.1.3, 2 NameNodes HA (ZooKeeper + ZKFC), Kerberos (KDC), 3 DataNodes with
  `dfs.data.transfer.protection=authentication`, short-circuit socket, one Flight server per DataNode in that node's
  network namespace, Flight with Kerberos auth + TLS. Reference = the same build against the same data with
  DataNodes WITHOUT data-transfer protection (privileged ports or protection off), answers hashed (order-insensitive
  where the query has no ORDER BY).
- Data: TPC-H SF1, lineitem split into 12+ files; a schema `spread` with lineitem/orders copies at 1 MiB block size
  (replication 2 and 1) so no DataNode holds any of their files whole; also a layout where the FIRST file of a table
  the query does not touch is on another node.
- Checks, each in default profile and `-DresourceProfile=speed`, on 1 server and on 3 servers (cluster):
  1. TPC-H 22/22 with PLAIN names and default schema (as clients send them) and again schema-qualified; every answer
     equals the reference; no "refused" counts as pass.
  2. spread set with plain names: count(*), full scan (row count + hash), GROUP BY, GROUP BY ORDER BY LIMIT, HAVING,
     count(DISTINCT), comma join `FROM orders_sp o, customer c WHERE ...` and JOIN ... ON, TPC-H q03/q12 on the spread
     tables. A 0-row answer where the reference has rows = FAIL (silent wrong answer).
  3. partial mode (the partial-results header) on 3 servers: per-node sums equal the complete answer.
  4. small copy disk: `-DhdfsLocalCopyDir` on a 64 MiB tmpfs: complete and partial count / GROUP BY / scans of the
     spread tables finish and are exact (batched), tmpfs never full; a join that cannot fit is refused with
     RESOURCE_EXHAUSTED, never INTERNAL or a wrong answer.
  5. low direct memory: 3 servers `-XX:MaxDirectMemorySize=512m`, speed + `-DdistributedComplete=true`, 4 full scans
     of the 12-file lineitem in a row: exact, no OutOfMemoryError.
  6. server logs: every query has an `hdfs=reads` line; short-circuit fd counters on the DataNodes grow; no DuckDB
     read of a non-local file through hadoopfs (no `HdfsNetworkException`).
- Output `results/ACCEPT-<id>.md`: table check x profile x servers = pass/fail with the error text, verdict
  "SHIP" only if all pass. Commit raw logs as a run artifact, not in git.
- First run on `server-1.0.0-8060179bce0c` (kestrel item 31), then on every newer pre-release whose Log names an
  HDFS item. Write "EGRET ACCEPT <id> DONE" in this file's Log when a report exists. Keep the FRESH rules as they are.

## Log
- EGRET ACCEPT 8060179bce0c DONE 2026-11-05: run 41995351608, `results/ACCEPT-8060179bce0c.md`, verdict DO NOT SHIP
  (check 4 small copy disk: every complete copy refused, INTERNAL not RESOURCE_EXHAUSTED; check 6: complete-answer
  queries without an `hdfs=reads` line); checks 1, 2, 3, 5 pass in every cell.
Maintainer, 2026-11-05 13:10: check 4 - the ADBC driver prints a wire RESOURCE_EXHAUSTED as `INTERNAL: ... (ResourceExhausted; ...)`;
count that as RESOURCE_EXHAUSTED (match the gRPC status, not the driver's prefix). Next ACCEPT: the kestrel item 32
pre-release (copy reserve on small disks, `hdfs=reads` on the complete path) as soon as it exists; if it still sets no
lower reserve for small disks, run check 4 with `-DhdfsLocalCopyMinFreeBytes=8m` and report the default separately.
Maintainer, 2026-11-05 14:22: ACCEPT on `server-1.0.0-5f60db1ee304` (item 32) dispatched by the maintainer: run 42018218548 - do not dispatch another; read its report, fix harness false fails (check 4 status reading) with `only` reruns, then write the verdict.
- EGRET ACCEPT 5f60db1ee304 DONE 2026-11-05: runs 42018218548 + 42027069331 (only rerun, harness a5a0469), `results/ACCEPT-5f60db1ee304.md`, verdict DO NOT SHIP (check 4 only: complete sp-group/sp-distinct, 9 copies 156 MB > 64 MiB disk, refused instead of copy batches; the join refusal is an allowed RESOURCE_EXHAUSTED); checks 1, 2, 3, 5, 6 pass in every cell.
- EGRET ACCEPT 50fe065af50c DONE 2026-11-05: run 42055012677, `results/ACCEPT-50fe065af50c.md`, verdict DO NOT SHIP (check 4 only: complete sp-group/sp-distinct still refused instead of copy batches; refusals count ~52 MB of copies "in use by running queries" with no other query running, so finished queries keep copies pinned; speed cells also refuse partial part-lineitem-sp/part-group-sp); checks 1, 2, 3, 5, 6 pass in every cell.
Maintainer, 2026-11-06 00:15: next ACCEPT = the item 33 pre-release after `50fe065af50c` (package run on kestrel 35c15ab2). Run check 4 with `-DhdfsLocalCopyRoomWaitMillis=30000` on every server (opt-in in that build); report also whether the speed partial cells pass without it. The maintainer's watcher dispatches the run when the release appears - if a run for that tag exists, do not dispatch another.
- EGRET ACCEPT 35c15ab226b9 PARTIAL 2026-11-05: run 42113544966 (watcher, without room wait), `results/ACCEPT-35c15ab226b9.md`: checks 1, 2, 3, 5, 6 pass everywhere; check 4 passes in the default cells, fails in the speed cells (partial part-lineitem-sp/part-group-sp refused, ~52 MB pinned by "other running queries"). Room-wait run still to do: `smalldisk-opts=-DhdfsLocalCopyRoomWaitMillis=30000` (input added in 455033c).
- EGRET ACCEPT 35c15ab226b9 DONE 2026-11-06: room-wait run 42196478105 (`smalldisk-opts=-DhdfsLocalCopyRoomWaitMillis=30000`) + watcher run 42113544966 (without), `results/ACCEPT-35c15ab226b9.md`, verdict SHIP with the room wait (all 6 checks pass in every cell); without it the speed cells fail check 4 (partial part-lineitem-sp/part-group-sp refused, ~52 MB pinned), default cells pass either way.
- EGRET ACCEPT deafc861cce3 DONE 2026-11-06: run 42223763930 (`smalldisk-opts=-DhdfsLocalCopyRoomWaitMillis=30000`, harness ea99fcf), `results/ACCEPT-deafc861cce3.md`, verdict SHIP with the room wait (all 6 checks pass in every cell); check 4 without the room wait not run on this build.
Maintainer, 2026-11-06 18:40: write `results/FRESH-deafc861cce3.md` from run 42223833724 (wave fresh-up-deafc861cce3, upstream `9e4787906b07`, dispatched by the maintainer) exactly like FRESH-413485ba80fd, including load (queries/s per client count, via ci/load_report.py) and the slow-link ZSTD export, which the run summary does not show; compare upstream 9e4787906b07 with 6e264c10f403 where both were measured.
- EGRET FRESH deafc861cce3 DONE 2026-11-06: run 42223833724 + rereport 42244896618 (`load.md` via `ci/load_report.py`), `results/FRESH-deafc861cce3.md` with load per step, slow-link ZSTD export and upstream `9e4787906b07` vs `6e264c10f403`; regression by the rule: local small JDBC c1 p50 speed/balanced 1.10 (smaller than 413485ba80fd's 1.18). Open point: `load_report.py` balanced q/s 41-47 vs the client's own count 35-44.
- EGRET ACCEPT 19efa29b1b57 DONE 2026-11-06: run 42261777686 (`smalldisk-opts=-DhdfsLocalCopyRoomWaitMillis=30000`), `results/ACCEPT-19efa29b1b57.md`, verdict SHIP with the room wait (all 6 checks pass in every cell); items 35 and 36 (1) part 1, (3), (5). Check 4 runs without distributedComplete, so the item 36 (1) DC + small copy disk case is not covered; no FRESH wave (no change on the local/S3 path).
- EGRET ACCEPT 6384bc55b173 DONE 2026-11-06: run 42278048164 (release watcher, `smalldisk-opts=-DhdfsLocalCopyRoomWaitMillis=30000`), `results/ACCEPT-6384bc55b173.md`, verdict SHIP with the room wait (all 6 checks pass in every cell); item 36 (1) / (2) / (4). Not covered: DC + small copy disk (item 36 (1) stand case), keytab start, log wording; no FRESH wave.
- EGRET ACCEPT 06c5adc7d7c9 DONE 2026-11-07: run 42351380956 (session, `smalldisk-opts=-DhdfsLocalCopyRoomWaitMillis=30000`), `results/ACCEPT-06c5adc7d7c9.md`, verdict SHIP with the room wait (all 6 checks pass in every cell); item 37 (a)-(d). Not covered: storage denial, stop under load, no-ticket-cache WARN; no FRESH wave.
Maintainer, 2026-11-07 20:55: ACCEPT 06c5adc7d7c9 run 42390647941: 3 speed cells failed the layout check (random placement put a whole spread file on one DataNode: 'a DataNode holds it whole (17 blocks ...)') - harness flake; rerun with only= dispatched by the maintainer. Make the spread layout deterministic (re-place or re-write until no DataNode holds a file whole, or pin with a block placement policy) so it cannot flake.
- EGRET ACCEPT 06c5adc7d7c9 RECHECK DONE 2026-11-07: run 42390647941 lost 3 speed cells to the layout flake (setup only); harness fix fcf1eb3 re-writes a spread file that a DataNode holds whole and checks again (at most 6 rounds); `only` rerun 42396888303 (base-run 42390647941, room wait) green, `results/ACCEPT-06c5adc7d7c9.md` verdict SHIP (all 6 checks in every cell); the maintainer's rerun 42398263063 of the same cells also green.
