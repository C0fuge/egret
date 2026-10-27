# Server comparison task, 2026-10-27 (maintainer) - supersedes ci/COMPARE-NOTES.md

## Servers (4)
| id | what | how to get |
|---|---|---|
| `ours-new` | newest C0fuge/kestrel pre-release at dispatch time (`gh release list -R C0fuge/kestrel -L 1`; at writing `server-1.0.0-7562a5bdb7b9`) | release assets: jar, flight-server-libs tar, flight-plugins tar |
| `ours-27f5` | `server-1.0.0-27f583adccd7` (presentation build, DuckDB 1.5.6) | same |
| `up-native` | upstream VadimSurpin/arrow-flight-server `feat/starrocks-native-integration`, newest head at dispatch (at writing `30855be44317`, 2026-10-26; was `07631d72954a`) | build read-only from the public repo (see compare/build-upstream workflows) |
| `up-main` | upstream `main` @ `dbacd8d585bc` (our fork point) | same |

Ours need `duckdb-extensions-v1.5.6.tar.zst` (C0fuge/kestrel release `ci-assets`, `extensions/v1.5.6/linux_amd64/`) and
`-Darrowflight.duckdb.extensionDir=<dir> -DduckDbAllowUnsignedExtensions=true`. Upstream jars bundle DuckDB 1.5.6, need the
official httpfs 1.5.6, `--add-modules java.se,jdk.httpserver` + their entrypoint's add-opens/exports. Upstream refuses a data
dir with a BINARY column -> every server gets the same TPC-H-only data dir and the same `tpch.`-qualified queries. Upstream:
JDBC prepared statements not implemented, `LIMIT` without `ORDER BY` returns the whole table, `AVG` missing on the native
branch -> use only workloads it answers correctly, mark the rest `n/a` with the reason. Wrong TPC-H checksum = disqualified
for that workload, never ranked. Every A/B pair runs on the SAME runner, alternating rounds, 3 rounds, 1 warm-up.
Settings per server: its defaults AND its best thread count (ours 4 and 8; upstream its default and 8); keep both.


## Containers - identical limits for every server (maintainer, 2026-10-27; applies to ALL reports)
Production runs the server in containers with resource limits, so the comparison must too:
- every server runs in a Docker container from the SAME image (`eclipse-temurin:21-jre`), started the same way, with the
  SAME limits: `--cpus=2 --cpuset-cpus=0,1 --memory=6g --memory-swap=6g`, JVM `-Xmx3g -XX:MaxDirectMemorySize=2g`
  (`MALLOC_ARENA_MAX=4`), only the server's own required flags differ (upstream: its add-modules/add-opens);
- clients (JDBC/ADBC runners, load generators, Trino) run in their own container(s) pinned to the other cores
  (`--cpuset-cpus=2,3`), never inside the server container;
- data (local Parquet) mounted read-only into the server container; S3 = the MinIO container, also pinned off the server
  cores;
- record `docker stats` samples (CPU %, memory) of the server container for every run, and the container OOM-kill state;
- if a server is OOM-killed inside its limit, that is a result (record it), not a reason to raise its limit.
If you already dispatched runs without containers, keep them only as "no-container reference" and redo the reported
numbers with containers.

## Report 1 - SPEED (run first, publish as soon as done: `results/COMPARE-SPEED-2026-10-27.md` + README summary, own commit)
Format like the upstream README benchmark section: an "Experiment setup" table (runner type/vCPU/RAM, scale factor, data
layout, repetitions, batch size, versions incl. DuckDB per server, JVM flags) and per-query tables:
`| Q | Pattern | ours-new (ms) | ours-27f5 (ms) | up-native (ms) | up-main (ms) | ours-new vs best upstream |` for TPC-H SF1 and
SF10 (ADBC; JDBC too where the server supports it) with a Score row, plus a small-query table (point lookup orders /
lineitem, filtered count, LIMIT 10 with ORDER BY, metadata calls; JDBC and ADBC; c1/c8/c32; p50/p95/p99) and a scan table
(1/4/8 streams MB/s, full `lineitem` export over ADBC MB/s + server peak RSS). Local Parquet and S3 (the workflow's MinIO).
SF30 too if the runner disk allows, else note why not.

## Report 2 - LOAD (`results/COMPARE-LOAD-2026-10-27.md`)
- closed-loop small-query load at 1/8/32/64/128 clients (point + filtered count; JDBC and ADBC), 10 s warm-up + 60 s per step:
  QPS, p50/p95/p99, error rate, server CPU and RSS; saturation point (highest step with p95 < 100 ms and 0 errors);
- mixed load: 32 small-query clients + 2 heavy streams (q01, q18): small QPS/p95 with and without heavy, heavy times;
- 4 heavy queries at once (q01, q09, q18, q21): slowest time, failures, peak RSS;
- network-limited client path (`tc netem` 10 ms delay, 1 Gbit/s) for SF10 over ADBC, upstream with and without its ZSTD
  compression (only ADBC decodes it), ours plain; TLS + token on vs off for ours (cost of a secured connection).

## Report 3 - ROBUSTNESS (`results/COMPARE-ROBUSTNESS-2026-10-27.md`)
- 30-min soak under mixed load: RSS / heap / direct memory over time (sample every 10 s), errors, latency drift;
- cold start: time until the port answers, first-query latency, idle RSS;
- cancel: client cancels a running SF10 q18/q21 -> time until server CPU drops (server-side "stopped" evidence);
- ours only (upstream n/a with reason): 3-node cluster on one runner - stop a node before a query and kill one mid-query,
  answer correctness and time to recover; Trino SF1 through our plugin (C0fuge/heron release `e2e-assets`/CI artifact)
  and the stock Flight SQL JDBC driver TPC-H SF1 (upstream: record the failure text); duckDbThreads 1/2/4/8 sweep on SF1/SF10
  + small c1/c32 (feeds the size-aware default).

## Every run records everything (raw files as artifacts, summaries in results/)
every sample (cold+warm), p50/p95/p99/max, errors with text; per-query TPC-H times and checksums; rows/s and MB/s; server
peak RSS, heap used/committed, direct memory, GC count/time, CPU user/sys, threads; Flight bytes/batches/rows; start and
first-query time; WARN/ERROR excerpts; exact JVM flags and settings; runner CPU model, cores, RAM, kernel, JDK, DuckDB version.

## Rules
Public repo: no personal data, host names or internal names. Commit as C0fuge <189659128+C0fuge@users.noreply.github.com>,
trailer `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. Never push to the upstream repository. Finish within
~90 min per session; record running CI ids and the next step in README "In progress" so the next session continues.

## Later addition
If a newer C0fuge/kestrel pre-release appears while this task runs (expected: the S3 plugin's node-wide byte-bounded read
cache, item 17 option A), add it as `ours-cache` in an extra S3-only pair against `ours-new` (SF1/SF10 and repeated
small queries, cache on vs off) after Report 1 is published; do not restart finished work.

Update (maintainer, 2026-10-27): `ours-new` stays `7562a5bdb7b9` for Reports 1-3. Newer pre-releases (first one:
`84fec772ec50`) are collected and tested only in a final run once Reports 1-3 are done (S3 cache pair included).

## Fix list after the first speed run 40490378159 (maintainer, 2026-10-27 18:55) - do these BEFORE publishing Report 1
1. **"wrong answer" on JDBC for q01/q05/q06/q07/q09/q15/q19 for BOTH our builds**: identical on both builds and these
   are exactly the queries with DECIMAL/aggregate results, so it is almost certainly the harness (JDBC value formatting
   or rounding vs the reference), not the servers. Compare numerically (decimal-aware, same rounding as the reference) or
   build the JDBC reference from DuckDB through the same JDBC formatting. Report only real mismatches.
2. **up-main: every ADBC TPC-H query "failed"**: find the actual error text (job log). ADBC uses plain
   CommandStatementQuery, not prepared statements, so it should run; fix the harness side (table qualification, data dir,
   startup) if that is the cause, else record the server's error text as the reason.
3. **up-native "not run: not in this setting's jobs"**: add its jobs (def and t8) so it appears in every table.
4. **ours-new (7562a5bdb7b9) is 30-45 % slower than ours-27f5 on TPC-H SF10 over ADBC on the same runner** (q01 2204 vs
   1510 ms, q03 1208 vs 862 ...). The maintainer's local stand saw the same direction for the intermediate build
   45fc0a9e6e02. Confirm with a dedicated same-runner job (5 rounds, ADBC SF10 + small queries) for 27f5 vs
   `server-1.0.0-45fc0a9e6e02` vs `server-1.0.0-e46f28dfdf09` vs `server-1.0.0-6acc9cce0b26` vs 7562a5bdb7b9 (all
   C0fuge/kestrel pre-releases) to find the first slow build, and put the result at the top of Report 1. Do not change
   server code here; the coordinator forwards it to the server repo.
