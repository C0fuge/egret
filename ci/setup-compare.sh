#!/usr/bin/env bash
# setup-compare.sh <assets-dir>: servers for the compare workflow, each under <assets>/srv/<server>/ (server.jar, libs/,
# plugins/). SERVERS = space-separated kestrel pre-release ids (server-1.0.0-<id>) and/or "up-<name>" (jar + libs from
# the upstream job, artifact upstream-up-<name> under UPSTREAM_DIR). DuckDB 1.5.6: the kestrel extension set (release ci-assets) in
# <assets>/duckdb156/extensions/v1.5.6/linux_amd64/, the official httpfs 1.5.6 for upstream in
# <assets>/duckdb-upstream/extensions/v1.5.6/linux_amd64/ (its DuckDB home). Plus the JDBC driver and the Python venv.
set -euo pipefail
A=${1:?}; SERVERS=${SERVERS:?}
K=https://github.com/C0fuge/kestrel/releases/download
mkdir -p "$A/dl" "$A/srv"
cd "$A/dl"
for B in $SERVERS; do
  S="$A/srv/$B"; mkdir -p "$S"
  case $B in upstream|up-*)
    : "${UPSTREAM_DIR:?}"; U="$UPSTREAM_DIR/upstream-$B"; [ -d "$U" ] || U=$UPSTREAM_DIR   # up-<name>: artifact upstream-up-<name>
    (cd "$U" && sha256sum --quiet -c SHA256SUMS)
    cp "$U"/server.jar "$S/server.jar"; cp -r "$U/libs" "$S/libs"; cat "$U/REF.txt"
    continue;;
  esac
  mkdir -p "$B"
  for f in SHA256SUMS arrow-flight-server-1.0.0-$B-linux.jar flight-plugins-1.0.0-$B.tar.zst flight-server-libs-1.0.0-$B.tar.zst; do
    curl -fsSL --retry 3 -o "$B/$f" "$K/server-1.0.0-$B/$f"
  done
  (cd "$B" && sha256sum --check --ignore-missing SHA256SUMS)
  cp "$B/arrow-flight-server-1.0.0-$B-linux.jar" "$S/server.jar"
  tar --zstd -xf "$B/flight-plugins-1.0.0-$B.tar.zst" -C "$S"
  tar --zstd -xf "$B/flight-server-libs-1.0.0-$B.tar.zst" -C "$S"
  (cd "$S/libs" && sha256sum --quiet -c SHA256SUMS)
done
curl -fsSL --retry 3 -o ci-SHA256SUMS "$K/ci-assets/SHA256SUMS"
curl -fsSL --retry 3 -o duckdb-extensions-v1.5.6.tar.zst "$K/ci-assets/duckdb-extensions-v1.5.6.tar.zst"
grep ' duckdb-extensions-v1.5.6.tar.zst$' ci-SHA256SUMS | sha256sum -c
mkdir -p ext156 "$A/duckdb156/extensions/v1.5.6" && tar --zstd -xf duckdb-extensions-v1.5.6.tar.zst -C ext156
X=$(find ext156 -type d -path '*v1.5.6/linux_amd64' | head -1); [ -n "$X" ] || { find ext156 | head -20; exit 1; }
mv "$X" "$A/duckdb156/extensions/v1.5.6/linux_amd64"; ls -l "$A/duckdb156/extensions/v1.5.6/linux_amd64"
U="$A/duckdb-upstream/extensions/v1.5.6/linux_amd64"; mkdir -p "$U"
curl -fsSL --retry 3 "http://extensions.duckdb.org/v1.5.6/linux_amd64/httpfs.duckdb_extension.gz" | gunzip > "$U/httpfs.duckdb_extension"
ls -l "$U"
curl -fsSL --retry 3 -o "$A/flight-sql-jdbc-driver-18.0.0.jar" \
  https://repo1.maven.org/maven2/org/apache/arrow/flight-sql-jdbc-driver/18.0.0/flight-sql-jdbc-driver-18.0.0.jar
python3 -m venv "$A/venv"
"$A/venv/bin/pip" install -q --disable-pip-version-check adbc-driver-flightsql==1.12.0 pyarrow==26.0.0 duckdb==1.4.1
rm -rf "$A/dl"
du -sh "$A"/srv/*
