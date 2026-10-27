# Server comparison - final run: S3 read cache and newer builds (2026-10-27)

Source: compare run 40569584228, wave `c10-cache` ([summary](c10-cache-40569584228/summary.md),
[raw CSV](c10-cache-40569584228/summary.csv)). Task: `ci/COMPARE-TASK.md` "Later addition".

## Setup

- S3 only (MinIO-compatible `rclone serve s3` container on cpus 2,3), TPC-H SF1 and SF10 Parquet, `-DduckDbThreads=4` on both sides.
- Containers as in Reports 1-3: server in `eclipse-temurin:21-jre`, `--cpus=2 --cpuset-cpus=0,1 --memory=6g`,
  `-Xmx3g -XX:MaxDirectMemorySize=2g`; clients on cpus 2,3.
- Builds: `ours-new` = `7562a5bdb7b9` (baseline of Reports 1-3); `ours-cache` = `4e77c6bda59a` (newest pre-release at
  dispatch, node-wide byte-bounded S3 read cache, item 17 option A), cache on = `-Darrowflight.s3.cacheMegabytes=1024`;
  `84fec772ec50` = the first pre-release after `7562a5bdb7b9`.
- Every pair on one runner, rounds A B / B A / A B, workloads TPC-H SF1 + SF10 over ADBC and small queries
  (JDBC and ADBC, 1/8/32 clients). Every TPC-H answer was checked against in-process DuckDB: no side was disqualified,
  no OOM kill.

## Results (ratio B / A of medians over 3 rounds; < 1 = B faster)

| pair (A -> B) | small ADBC c1 p50 | small ADBC c32 p95 | small JDBC c1 p50 | small JDBC c32 p95 | TPC-H SF1 ADBC | TPC-H SF10 ADBC | server RSS peak |
|---|---|---|---|---|---|---|---|
| ours-cache: cache off -> on | 0.33 | 0.06 | 0.64 | 0.07 | 0.32 | 1.08 | 2338 -> 5725 MB (2.45x) |
| ours-new -> ours-cache, cache on | 0.57 | 0.11 | 0.70 | 0.11 | 0.47 | 1.08 | 2219 -> 5709 MB (2.57x) |
| ours-new -> ours-cache, cache off | 1.09 | 1.02 | 0.88 | 1.02 | 1.00 | 1.01 | 2324 -> 2309 MB |
| ours-new -> 84fec772ec50 | 1.23 | 1.58 | 0.99 | 1.51 | 1.45 | 0.83 | 2327 -> 2200 MB |

## Findings

- **Repeated small queries on S3 are much faster with the cache on**: p50 1.4-4x, tails 8-20x (p95 at 1-32 clients falls from ~0.8-20 s to
  ~0.08-1.8 s, ratio 0.05-0.12 in every round, JDBC and ADBC). TPC-H SF1 (fits in the 1 GiB cache) runs in 0.32-0.47x the time.
- **TPC-H SF10 is ~8 % slower with the cache on** (1.08 in both pairs, rounds 1.03-1.45): SF10 does not fit in 1 GiB, so the
  cache only churns. Worth a size-aware bypass (e.g. skip caching for large sequential scans) in the server repo.
- **Peak RSS with the cache on is ~5.7 GB inside the 6 GB container limit** (vs ~2.3 GB off). No OOM kill in these runs, but
  the margin is ~300 MB: the cache memory is evidently not covered by `-Xmx3g` / direct 2g alone. Recommend bounding it to
  the container budget or lowering the default size before it is enabled in production.
- With the cache off, `4e77c6bda59a` equals `7562a5bdb7b9` (all ratios 0.88-1.09, round-to-round noise): no regression.
- `84fec772ec50` vs `7562a5bdb7b9` is **inconclusive**: round 2 is equal everywhere (0.92-1.20), rounds 1 and 3 show slower
  small-query tails and SF1 (1.45-1.50) but a faster SF10 (0.82 in round 3 only). Not "> 5 % slower in all 3 rounds", so no
  regression flag; S3 latency on a shared runner is noisy. It is superseded by `4e77c6bda59a`, whose cache-off side matches
  the baseline; build tracking (`ci/BUILD-TRACK-TASK.md`) re-measures newer builds against `7562a5bdb7b9`.
