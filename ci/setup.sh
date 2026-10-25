#!/usr/bin/env bash
# setup.sh <assets-dir>: server build (public kestrel release), DuckDB v1.4.5 httpfs extension, Flight SQL JDBC driver,
# Python venv with ADBC Flight SQL + pyarrow + duckdb. SERVER_BUILD = release id (default 4eaab052deaf).
set -euo pipefail
A=${1:?}; B=${SERVER_BUILD:-4eaab052deaf}
REL=https://github.com/C0fuge/kestrel/releases/download/server-1.0.0-$B
mkdir -p "$A/server" "$A/duckdb/extensions/v1.4.5/linux_amd64"
cd "$A"
for f in SHA256SUMS arrow-flight-server-1.0.0-$B-linux.jar flight-plugins-1.0.0-$B.tar.zst flight-server-libs-1.0.0-$B.tar.zst; do
  curl -fsSL --retry 3 -o "$f" "$REL/$f"
done
sha256sum --check --ignore-missing SHA256SUMS
cp arrow-flight-server-1.0.0-$B-linux.jar server/server.jar
tar --zstd -xf flight-plugins-1.0.0-$B.tar.zst -C server
tar --zstd -xf flight-server-libs-1.0.0-$B.tar.zst -C server
(cd server/libs && sha256sum --quiet -c SHA256SUMS)
curl -fsSL --retry 3 "http://extensions.duckdb.org/v1.4.5/linux_amd64/httpfs.duckdb_extension.gz" | gunzip > duckdb/extensions/v1.4.5/linux_amd64/httpfs.duckdb_extension
curl -fsSL --retry 3 -o flight-sql-jdbc-driver-18.0.0.jar \
  https://repo1.maven.org/maven2/org/apache/arrow/flight-sql-jdbc-driver/18.0.0/flight-sql-jdbc-driver-18.0.0.jar
python3 -m venv venv
venv/bin/pip install -q --disable-pip-version-check adbc-driver-flightsql==1.12.0 pyarrow==26.0.0 duckdb==1.4.1
ls -l "$A" "$A/server" | head -30
