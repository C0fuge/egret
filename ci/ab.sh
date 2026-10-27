#!/usr/bin/env bash
# ab.sh: A/B screening on ONE runner: side A = default server config, side B = a variant (flags and/or data layout),
# run alternately ROUNDS times (A B, B A, A B, ...) so runner noise hits both sides alike.
#
# Env: VARIANT (name), FLAGS_B (extra server -D/-X flags of side B), LAYOUT_B (data layout of side B, default = default),
#      FLAGS_A (extra flags of side A, normally empty), STORAGE (local | s3), ROUNDS (3), WORKLOADS ("small sf1 sf10 scan";
#      also adbc10 adbc1 = TPC-H over ADBC), ASSETS (dir with the server jar/libs/plugins tars), DATA (dir with
#      <layout>/sf1, <layout>/sf10), OUT (results).
#      Server comparison (compare workflow): SERVER_A / SERVER_B = kestrel release id or "upstream" (ASSETS/srv/<server>,
#      setup-compare.sh), QUERIES (TPC-H query dir, default queries/tpch), SMALL_CLASSES (small-query classes, all if empty).
# Per side and round: OUT/<A|B>/r<N>/ with result.txt, small-*.csv, jdbc10/ jdbc1/ (FlightTpch), adbc10/ adbc1/
# (tpch_adbc.py), mem.txt, steps.tsv.
set -uo pipefail
HERE=$(cd "$(dirname "$0")/.." && pwd)
: "${VARIANT:?}" "${ASSETS:?}" "${DATA:?}" "${OUT:?}"
FLAGS_A=${FLAGS_A:-}; FLAGS_B=${FLAGS_B:-}; LAYOUT_B=${LAYOUT_B:-default}; STORAGE=${STORAGE:-local}
ROUNDS=${ROUNDS:-3}; WORKLOADS=${WORKLOADS:-small sf1 sf10 scan}; NET=egret
JDBC=$ASSETS/flight-sql-jdbc-driver-18.0.0.jar; SRV=$ASSETS/server; SERVER_A=${SERVER_A:-}; SERVER_B=${SERVER_B:-}
QUERIES=${QUERIES:-$HERE/queries/tpch}; UPDUCK=${UPDUCK:-$ASSETS/duckdb-upstream}
# Scan.java needs the Arrow Flight client classes: any kestrel server jar
for x in $SERVER_A $SERVER_B; do [ "$x" != upstream ] && [ -f "$ASSETS/srv/$x/server.jar" ] && SRV=$ASSETS/srv/$x; done
S3_KEY="ci$(openssl rand -hex 8)"; S3_SECRET="$(openssl rand -hex 24)"
mkdir -p "$OUT"; log() { echo "== $(date -u +%T) $*" | tee -a "$OUT/job.log"; }

if [ "$STORAGE" = s3 ]; then
  # rclone serves DATA over the S3 API: directory DATA/<layout> = bucket <layout>
  docker rm -f s3 >/dev/null 2>&1
  docker run -d --name s3 --network host -v "$DATA":/data:ro rclone/rclone:1.68.2 \
    serve s3 /data --addr 127.0.0.1:9000 --auth-key "$S3_KEY,$S3_SECRET" >/dev/null
  sleep 3
fi

data_dir() {  # data_dir <layout> <sf1|sf10>
  if [ "$STORAGE" = s3 ]; then echo "s3://$1/$2"; else echo "file:///data/$1/$2"; fi
}

start_server() {  # start_server <dataDir> <flags...>; server of the current side: $SERVER (empty = legacy $ASSETS/server)
  local dd=$1; shift
  docker rm -f flight >/dev/null 2>&1
  local env=(-e LANG=C.UTF-8 -e MALLOC_ARENA_MAX=4 -e FLIGHT_ALLOW_INSECURE=true -e FLIGHT_S3_ACCESS_KEY="$S3_KEY" -e FLIGHT_S3_SECRET_KEY="$S3_SECRET")
  local common=(-Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false
    -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir="$dd")
  local args=(-cp "/app/server.jar:/app/libs/*" pro.surpin.data.arrowflight.server.HadoopArrowFlightServer
    --port 32010 --localhost localhost --hosts 127.0.0.1)
  if [ "${SERVER:-}" = upstream ]; then
    # upstream: JVM options of its docker/bin/entrypoint.sh; DuckDB home with the official httpfs 1.5.6; S3 via FLIGHT_S3_*
    docker run -d --name flight --network host --memory 8g --memory-swap 8g "${env[@]}" -e HOME=/duckhome \
      -e FLIGHT_S3_ENDPOINT=http://127.0.0.1:9000 -e FLIGHT_S3_PATH_STYLE=true -e FLIGHT_S3_REGION=us-east-1 \
      -v "$ASSETS/srv/upstream":/app:ro -v "$UPDUCK":/duckhome/.duckdb -v "$DATA":/data:ro -w /tmp eclipse-temurin:21-jdk \
      java --add-modules java.se,jdk.httpserver --add-exports java.base/jdk.internal.ref=ALL-UNNAMED \
        --add-opens java.base/java.lang=ALL-UNNAMED --add-opens java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED \
        --add-opens java.management/sun.management=ALL-UNNAMED --add-opens jdk.management/com.sun.management.internal=ALL-UNNAMED \
        -Dio.netty.tryReflectionSetAccessible=true "${common[@]}" "$@" "${args[@]}" >/dev/null
  elif [ -n "${SERVER:-}" ]; then
    # kestrel pre-release with the DuckDB 1.5.6 extension set
    docker run -d --name flight --network host --memory 8g --memory-swap 8g "${env[@]}" \
      -v "$ASSETS/srv/$SERVER":/app:ro -v "$ASSETS/duckdb156":/ext/duckdb-home:ro -v "$DATA":/data:ro -w /tmp eclipse-temurin:21-jdk \
      java --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED \
        -Darrowflight.plugins.dir=/app/plugins -Darrowflight.duckdb.extensionDir=/ext/duckdb-home/extensions -DduckDbAllowUnsignedExtensions=true \
        -Ds3Endpoint=http://127.0.0.1:9000 -Ds3UrlStyle=path -Ds3Region=us-east-1 "${common[@]}" "$@" "${args[@]}" >/dev/null
  else
    docker run -d --name flight --network host --memory 8g --memory-swap 8g \
      -e LANG=C.UTF-8 -e MALLOC_ARENA_MAX=4 -e FLIGHT_ALLOW_INSECURE=true -e FLIGHT_S3_ACCESS_KEY="$S3_KEY" -e FLIGHT_S3_SECRET_KEY="$S3_SECRET" \
      -v "$SRV":/app:ro -v "$ASSETS/duckdb":/ext/duckdb-home:ro -v "$DATA":/data:ro -w /tmp eclipse-temurin:21-jdk \
      java --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED \
        -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false \
        -Darrowflight.plugins.dir=/app/plugins -Darrowflight.duckdb.extensionDir=/ext/duckdb-home/extensions \
        -DduckDbHttpfsExtension=/ext/duckdb-home/extensions/v1.4.5/linux_amd64/httpfs.duckdb_extension \
        -Ds3Endpoint=http://127.0.0.1:9000 -Ds3UrlStyle=path -Ds3Region=us-east-1 \
        -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir="$dd" "$@" \
        -cp "/app/server.jar:/app/libs/*" pro.surpin.data.arrowflight.server.HadoopArrowFlightServer \
        --port 32010 --localhost localhost --hosts 127.0.0.1 >/dev/null
  fi
  for _ in $(seq 1 120); do
    docker logs flight 2>&1 | grep -q 'Server Arrow Flight SQL started' && return 0
    [ "$(docker inspect -f '{{.State.Running}}' flight)" = true ] || break; sleep 1
  done
  docker logs flight 2>&1 | tail -30; return 1
}
mem() { echo "$1 $(docker exec flight sh -c 'echo rss=$(awk "/VmRSS/{print int(\$2/1024)}" /proc/1/status) hwm=$(awk "/VmHWM/{print int(\$2/1024)}" /proc/1/status)' 2>/dev/null || echo rss=NA hwm=NA)" >> "$O/mem.txt"; }
step() { echo -e "$1\t$2\t$(date +%s)\t$(cut -d' ' -f1 /proc/loadavg)" >> "$O/steps.tsv"; }
tpch() {  # tpch <name> <sf> <reps>
  local d=$O/$1; mkdir -p "$d"
  timeout 1500 java -Duser.timezone=UTC --add-opens java.base/java.nio=ALL-UNNAMED -cp "$JDBC" "$HERE/clients/FlightTpch.java" \
    "jdbc:arrow-flight-sql://localhost:32010/?useEncryption=false" "$QUERIES" "$3" "$d" > "$d/runner.txt" 2>&1
  tpch_result "$1"
}
tpch_adbc() {  # tpch_adbc <name> <reps>
  local d=$O/$1; mkdir -p "$d"
  timeout 1500 "$ASSETS/venv/bin/python" -W ignore "$HERE/clients/tpch_adbc.py" grpc://localhost:32010 "$QUERIES" "$2" "$d" > "$d/runner.txt" 2>&1
  tpch_result "$1"
}
tpch_result() {
  local d=$O/$1
  echo "$1: ok=$(awk -F'\t' 'NR>1 && $2=="ok"' "$d/summary.tsv" 2>/dev/null | wc -l) cold_sum=$(awk -F'\t' 'NR>1{s+=$5} END{printf "%.2f", s}' "$d/summary.tsv" 2>/dev/null) median_sum=$(awk -F'\t' 'NR>1{s+=$7} END{printf "%.2f", s}' "$d/summary.tsv" 2>/dev/null) md5=$(cut -f1-4 "$d/summary.tsv" 2>/dev/null | md5sum | cut -c1-12)" >> "$O/result.txt"
}
alive() { [ "$(docker inspect -f '{{.State.Running}}' flight 2>/dev/null)" = true ] || { echo "SERVER DIED after $1: $(docker inspect -f 'exit={{.State.ExitCode}} oom={{.State.OOMKilled}}' flight)" >> "$O/result.txt"; docker logs flight > "$O/server-died-$1.log" 2>&1; return 1; }; }

side() {  # side <A|B> <round>
  local s=$1 r=$2 flags layout
  if [ "$s" = A ]; then flags=$FLAGS_A; layout=default; SERVER=$SERVER_A; else flags=$FLAGS_B; layout=$LAYOUT_B; SERVER=$SERVER_B; fi
  O=$OUT/$s/r$r; rm -rf "$O"; mkdir -p "$O"
  log "round $r side $s server=${SERVER:-default} layout=$layout flags=[$flags]"
  step start begin
  # shellcheck disable=SC2086
  if ! start_server "$(data_dir $layout sf10)" $flags > "$O/start.txt" 2>&1; then echo "START FAILED" >> "$O/result.txt"; return; fi
  mem idle
  # sf1 / adbc1 restart the server on SF1: always last
  local sf1started=
  for w in $(for x in $WORKLOADS; do case $x in sf1|adbc1) ;; *) echo $x;; esac; done) $(for x in $WORKLOADS; do case $x in sf1|adbc1) echo $x;; esac; done); do
    case $w in
    small)
      step small begin
      for c in "1 20" "8 10" "32 5"; do set -- $c
        SMALL_CLASSES=${SMALL_CLASSES:-} timeout 600 java -Xmx1g -Duser.timezone=UTC --add-opens java.base/java.nio=ALL-UNNAMED -cp "$JDBC" "$HERE/clients/Lat.java" \
          "jdbc:arrow-flight-sql://localhost:32010/?useEncryption=false" $1 $2 "$O/small-jdbc-c$1.csv" 2>"$O/small-jdbc-c$1.err" | grep '^jdbc' >> "$O/result.txt"
        SMALL_CLASSES=${SMALL_CLASSES:-} timeout 600 "$ASSETS/venv/bin/python" -W ignore "$HERE/clients/lat.py" grpc://localhost:32010 $1 $2 "$O/small-adbc-c$1.csv" \
          2>"$O/small-adbc-c$1.err" | grep '^adbc' >> "$O/result.txt"
      done
      step small end; mem small ;;
    sf10) step jdbc10 begin; tpch jdbc10 sf10 2; step jdbc10 end; mem jdbc10 ;;
    adbc10) step adbc10 begin; tpch_adbc adbc10 2; step adbc10 end; mem adbc10 ;;
    scan)
      step scan begin
      for c in 1 4; do
        timeout 900 java -Xmx1g -XX:MaxDirectMemorySize=3g --add-opens java.base/java.nio=ALL-UNNAMED -Darrow.enable_unsafe_memory_access=true \
          -cp "$SRV/server.jar" "$HERE/clients/Scan.java" localhost 32010 $c 1 complete "SELECT * FROM tpch.lineitem" 2>"$O/scan-c$c.err" | grep '^scan' >> "$O/result.txt"
      done
      step scan end; mem scan ;;
    heavy4)
      step heavy4 begin
      for q in q01 q09 q18 q21; do
        mkdir -p "$O/h-$q/q" "$O/heavy4-$q"; cp "$HERE/queries/tpch/$q.sql" "$O/h-$q/q/"
        timeout 1200 java -Duser.timezone=UTC --add-opens java.base/java.nio=ALL-UNNAMED -cp "$JDBC" "$HERE/clients/FlightTpch.java" \
          "jdbc:arrow-flight-sql://localhost:32010/?useEncryption=false" "$O/h-$q/q" 1 "$O/heavy4-$q" > "$O/heavy4-$q/runner.txt" 2>&1 &
      done
      wait
      echo "heavy4: $(for q in q01 q09 q18 q21; do awk -F'\t' -v q=$q 'NR==2{printf "%s=%s/%s/%s ", q, $2, $5, $4}' "$O/heavy4-$q/summary.tsv" 2>/dev/null; done)" >> "$O/result.txt"
      step heavy4 end; mem heavy4 ;;
    sf1|adbc1)
      step $w begin
      if [ -z "$sf1started" ]; then
        docker logs flight > "$O/server-sf10.log" 2>&1
        # shellcheck disable=SC2086
        if start_server "$(data_dir $layout sf1)" $flags > "$O/start-sf1.txt" 2>&1; then sf1started=1; else sf1started=failed; fi
      fi
      if [ "$sf1started" = 1 ]; then
        if [ $w = sf1 ]; then tpch jdbc1 sf1 3; else tpch_adbc adbc1 3; fi; mem $w
      else echo "START FAILED $w" >> "$O/result.txt"; fi
      step $w end ;;
    esac
    alive "$w" || start_server "$(data_dir $layout "$([ "$sf1started" = 1 ] && echo sf1 || echo sf10)")" $flags > "$O/restart.txt" 2>&1
  done
  docker logs flight > "$O/server-last.log" 2>&1
  grep -cE 'ERROR|OutOfMemory|SIGSEGV' "$O"/server-*.log | awk -F: '{s+=$NF} END{print s+0}' > "$O/server-errors.txt"
  step end end
  docker rm -f flight >/dev/null 2>&1
}

for r in $(seq 1 "$ROUNDS"); do
  if [ $((r % 2)) = 1 ]; then side A "$r"; side B "$r"; else side B "$r"; side A "$r"; fi
done
log "done"
