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
