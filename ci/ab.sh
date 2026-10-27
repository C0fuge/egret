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
# (tpch_adbc.py), mem.txt, steps.tsv, docker-stats.tsv, container.txt.
# Containers (identical for every server): the server runs in eclipse-temurin:21-jre with --cpus=2 --cpuset-cpus=0,1
# --memory=6g --memory-swap=6g (JVM -Xmx3g -XX:MaxDirectMemorySize=2g, MALLOC_ARENA_MAX=4); every client (JDBC/ADBC
# runners, scans, jcmd sampling) runs in the "client" container pinned to cpus 2,3, as does the S3 server.
set -uo pipefail
HERE=$(cd "$(dirname "$0")/.." && pwd)
: "${VARIANT:?}" "${ASSETS:?}" "${DATA:?}" "${OUT:?}"
FLAGS_A=${FLAGS_A:-}; FLAGS_B=${FLAGS_B:-}; LAYOUT_B=${LAYOUT_B:-default}; STORAGE=${STORAGE:-local}
ROUNDS=${ROUNDS:-3}; WORKLOADS=${WORKLOADS:-small sf1 sf10 scan}; NET=egret
JDBC=$ASSETS/flight-sql-jdbc-driver-18.0.0.jar; SRV=$ASSETS/server; SERVER_A=${SERVER_A:-}; SERVER_B=${SERVER_B:-}
QUERIES=${QUERIES:-$HERE/queries/tpch}; UPDUCK=${UPDUCK:-$ASSETS/duckdb-upstream}
# Scan.java needs the Arrow Flight client classes: any kestrel server jar
for x in $SERVER_A $SERVER_B; do case $x in upstream|up-*) continue;; esac; [ -f "$ASSETS/srv/$x/server.jar" ] && SRV=$ASSETS/srv/$x; done
SRV_IMAGE=eclipse-temurin:21-jre; CPU_CL=2,3
LIMITS=(--cpus=2 --cpuset-cpus=0,1 --memory=6g --memory-swap=6g)
PY=/venv/bin/python; LOAD_CLASSES=${LOAD_CLASSES:-point_orders,point_lineitem,count_filter}; pids=()
S3_KEY="ci$(openssl rand -hex 8)"; S3_SECRET="$(openssl rand -hex 24)"
mkdir -p "$OUT"; log() { echo "== $(date -u +%T) $*" | tee -a "$OUT/job.log"; }

# client container: JDK 21 + the same ADBC / pyarrow / duckdb versions as the host venv, host paths mounted 1:1
# (python:3.12-slim + the Temurin 21 JDK of the eclipse-temurin image; build log kept in OUT/client-build.log)
docker build --progress=plain -t egret-client - > "$OUT/client-build.log" 2>&1 <<'DOCKERFILE' || { tail -40 "$OUT/client-build.log"; exit 1; }
FROM python:3.12-slim
COPY --from=eclipse-temurin:21-jdk /opt/java/openjdk /opt/java/openjdk
ENV JAVA_HOME=/opt/java/openjdk PATH=/opt/java/openjdk/bin:$PATH
RUN python -m venv /venv && /venv/bin/pip install -q --no-cache-dir adbc-driver-flightsql==1.12.0 pyarrow==26.0.0 duckdb==1.4.1 \
 && java -version && /venv/bin/python -c "import adbc_driver_flightsql, pyarrow, duckdb"
DOCKERFILE
docker rm -f client > /dev/null 2>&1
docker run -d --name client --network host --cpuset-cpus=$CPU_CL --user "$(id -u):$(id -g)" -e HOME=/tmp -e LANG=C.UTF-8 \
  -v "$HERE":"$HERE":ro -v "$ASSETS":"$ASSETS":ro -v "$DATA":"$DATA":ro -v "$OUT":"$OUT" egret-client sleep infinity > /dev/null || exit 1
cl() { docker exec -e SMALL_CLASSES="${SMALL_CLASSES:-}" client "$@"; }
docker version --format 'docker {{.Server.Version}}' > "$OUT/containers.txt"
{ echo "server image: $SRV_IMAGE limits: ${LIMITS[*]}"; echo "client cpuset: $CPU_CL"; docker image inspect -f '{{.Id}}' $SRV_IMAGE 2>/dev/null; } >> "$OUT/containers.txt"

if [ "$STORAGE" = s3 ]; then
  # rclone serves DATA over the S3 API: directory DATA/<layout> = bucket <layout>
  docker rm -f s3 >/dev/null 2>&1
  docker run -d --name s3 --network host --cpuset-cpus=$CPU_CL -v "$DATA":/data:ro rclone/rclone:1.68.2 \
    serve s3 /data --addr 127.0.0.1:9000 --auth-key "$S3_KEY,$S3_SECRET" >/dev/null
  sleep 3
fi

data_dir() {  # data_dir <layout> <sf1|sf10>
  if [ "$STORAGE" = s3 ]; then echo "s3://$1/$2"; else echo "file:///data/$1/$2"; fi
}

start_server() {  # start_server <dataDir> <flags...>; server of the current side: $SERVER (empty = legacy $ASSETS/server)
  local dd=$1; shift
  docker inspect -f 'container exit={{.State.ExitCode}} oom={{.State.OOMKilled}} finished={{.State.FinishedAt}}' flight >> "$O/container.txt" 2>/dev/null
  docker rm -f flight >/dev/null 2>&1
  local t0=$(( $(date +%s%N) / 1000000 ))
  local env=(-e LANG=C.UTF-8 -e MALLOC_ARENA_MAX=4 -e FLIGHT_ALLOW_INSECURE=true -e FLIGHT_S3_ACCESS_KEY="$S3_KEY" -e FLIGHT_S3_SECRET_KEY="$S3_SECRET")
  local common=(-Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false
    -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir="$dd")
  local args=(-cp "/app/server.jar:/app/libs/*" pro.surpin.data.arrowflight.server.HadoopArrowFlightServer
    --port 32010 --localhost localhost --hosts 127.0.0.1)
  if [ "${SERVER:-}" = upstream ] || [ "${SERVER#up-}" != "${SERVER:-}" ]; then
    # upstream: JVM options of its docker/bin/entrypoint.sh; DuckDB home with the official httpfs 1.5.6; S3 via FLIGHT_S3_*
    docker run -d --name flight --network host "${LIMITS[@]}" "${env[@]}" -e HOME=/duckhome \
      -e FLIGHT_S3_ENDPOINT=http://127.0.0.1:9000 -e FLIGHT_S3_PATH_STYLE=true -e FLIGHT_S3_REGION=us-east-1 \
      -v "$ASSETS/srv/$SERVER":/app:ro -v "$UPDUCK":/duckhome/.duckdb -v "$DATA":/data:ro -w /tmp $SRV_IMAGE \
      java --add-modules java.se,jdk.httpserver --add-exports java.base/jdk.internal.ref=ALL-UNNAMED \
        --add-opens java.base/java.lang=ALL-UNNAMED --add-opens java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED \
        --add-opens java.management/sun.management=ALL-UNNAMED --add-opens jdk.management/com.sun.management.internal=ALL-UNNAMED \
        -Dio.netty.tryReflectionSetAccessible=true "${common[@]}" "$@" "${args[@]}" >/dev/null
  elif [ -n "${SERVER:-}" ]; then
    # kestrel pre-release with the DuckDB 1.5.6 extension set
    docker run -d --name flight --network host "${LIMITS[@]}" "${env[@]}" \
      -v "$ASSETS/srv/$SERVER":/app:ro -v "$ASSETS/duckdb156":/ext/duckdb-home:ro -v "$DATA":/data:ro -w /tmp $SRV_IMAGE \
      java --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED \
        -Darrowflight.plugins.dir=/app/plugins -Darrowflight.duckdb.extensionDir=/ext/duckdb-home/extensions -DduckDbAllowUnsignedExtensions=true \
        -Ds3Endpoint=http://127.0.0.1:9000 -Ds3UrlStyle=path -Ds3Region=us-east-1 "${common[@]}" "$@" "${args[@]}" >/dev/null
  else
    docker run -d --name flight --network host "${LIMITS[@]}" \
      -e LANG=C.UTF-8 -e MALLOC_ARENA_MAX=4 -e FLIGHT_ALLOW_INSECURE=true -e FLIGHT_S3_ACCESS_KEY="$S3_KEY" -e FLIGHT_S3_SECRET_KEY="$S3_SECRET" \
      -v "$SRV":/app:ro -v "$ASSETS/duckdb":/ext/duckdb-home:ro -v "$DATA":/data:ro -w /tmp $SRV_IMAGE \
      java --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED \
        -Darrow.enable_unsafe_memory_access=true -DmetricsEnabled=false -Dhazelcast.phone.home.enabled=false \
        -Darrowflight.plugins.dir=/app/plugins -Darrowflight.duckdb.extensionDir=/ext/duckdb-home/extensions \
        -DduckDbHttpfsExtension=/ext/duckdb-home/extensions/v1.4.5/linux_amd64/httpfs.duckdb_extension \
        -Ds3Endpoint=http://127.0.0.1:9000 -Ds3UrlStyle=path -Ds3Region=us-east-1 \
        -DnumServers=1 -Xmx3g -XX:MaxDirectMemorySize=2g -DdataDir="$dd" "$@" \
        -cp "/app/server.jar:/app/libs/*" pro.surpin.data.arrowflight.server.HadoopArrowFlightServer \
        --port 32010 --localhost localhost --hosts 127.0.0.1 >/dev/null
  fi
  local port=
  for _ in $(seq 1 600); do
    if [ -z "$port" ] && (echo > /dev/tcp/127.0.0.1/32010) 2>/dev/null; then
      port=1; echo "port_ms=$(( $(date +%s%N) / 1000000 - t0 ))" >> "$O/start-times.txt"
    fi
    if docker logs flight 2>&1 | grep -q 'Server Arrow Flight SQL started'; then
      docker inspect -f '{{json .Config.Cmd}}' flight > "$O/jvm-cmd.json" 2>/dev/null
      echo "started_s=$(( $(date +%s%N) / 1000000 - t0 ))ms" >> "$O/start-times.txt"; return 0
    fi
    [ "$(docker inspect -f '{{.State.Running}}' flight)" = true ] || break; sleep 0.2
  done
  docker logs flight 2>&1 | tail -30; return 1
}
mem() {  # RSS / peak RSS / threads / CPU ticks of the server process; JVM heap, GC and direct memory via jcmd
  echo "$1 $(docker exec flight sh -c 'echo rss=$(awk "/VmRSS/{print int(\$2/1024)}" /proc/1/status) hwm=$(awk "/VmHWM/{print int(\$2/1024)}" /proc/1/status) threads=$(awk "/Threads/{print \$2}" /proc/1/status) utime=$(cut -d" " -f14 /proc/1/stat) stime=$(cut -d" " -f15 /proc/1/stat)' 2>/dev/null || echo rss=NA hwm=NA)" >> "$O/mem.txt"
  { echo "== $1"; docker run --rm --pid container:flight --cap-add SYS_PTRACE --cpuset-cpus=$CPU_CL eclipse-temurin:21-jdk sh -c \
      'jcmd 1 GC.heap_info; jcmd 1 PerfCounter.print | grep -E "sun.gc.collector.[0-9].(name|invocations|time)|java.threads.live=|sun.os.hrt.frequency"; jstat -gcutil 1' 2>&1 | head -40; } >> "$O/jvm.txt"
  docker inspect -f "$1 oom={{.State.OOMKilled}} running={{.State.Running}}" flight >> "$O/container.txt" 2>/dev/null
}
firstq() {  # first query after start (ADBC connect + SELECT version()), DuckDB version
  cl $PY -W ignore -c 'import sys, time, adbc_driver_flightsql as a, adbc_driver_flightsql.dbapi as d
t0 = time.perf_counter(); c = d.connect(sys.argv[1], db_kwargs={a.DatabaseOptions.AUTHORIZATION_HEADER.value: "Bearer unused"}); cur = c.cursor()
try:
    cur.execute("SELECT version()"); v = cur.fetchall()[0][0]
except Exception as e:
    v = "error: " + str(e)[:100]
print(f"first_query_ms={(time.perf_counter() - t0) * 1000:.0f} duckdb={v}")' grpc://localhost:32010 >> "$O/start-times.txt" 2>&1
}
cpuloop() {  # cpuloop <file> <stopfile>: server process CPU ticks (utime stime, 100/s) every ~0.25 s
  while [ ! -e "$2" ]; do echo "$(date +%s.%N) $(docker exec flight cut -d' ' -f14,15 /proc/1/stat 2>/dev/null)" >> "$1"; sleep 0.25; done
}
step() { echo -e "$1\t$2\t$(date +%s)\t$(cut -d' ' -f1 /proc/loadavg)" >> "$O/steps.tsv"; }
tpch() {  # tpch <name> <sf> <reps>
  local d=$O/$1; mkdir -p "$d"
  cl timeout 1500 java -Duser.timezone=UTC --add-opens java.base/java.nio=ALL-UNNAMED -cp "$JDBC" "$HERE/clients/FlightTpch.java" \
    "jdbc:arrow-flight-sql://localhost:32010/?useEncryption=false" "$QUERIES" "$3" "$d" > "$d/runner.txt" 2>&1
  tpch_result "$1"
}
tpch_adbc() {  # tpch_adbc <name> <reps>
  local d=$O/$1; mkdir -p "$d"
  cl timeout 1500 $PY -W ignore "$HERE/clients/tpch_adbc.py" grpc://localhost:32010 "$QUERIES" "$2" "$d" > "$d/runner.txt" 2>&1
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
  # docker stats of the server container every ~5 s for the whole side (survives server restarts)
  rm -f "$O/.stats-stop"
  ( while [ ! -e "$O/.stats-stop" ]; do
      docker stats --no-stream --format "{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}\t{{.PIDs}}" flight 2>/dev/null | sed "s|^|$(date +%s)\t|" >> "$O/docker-stats.tsv"
      sleep 3; done ) &
  local statspid=$!
  mem idle
  firstq
  # sf1 / adbc1 restart the server on SF1: always last
  local sf1started=
  for w in $(for x in $WORKLOADS; do case $x in sf1|adbc1) ;; *) echo $x;; esac; done) $(for x in $WORKLOADS; do case $x in sf1|adbc1) echo $x;; esac; done); do
    case $w in
    small)
      step small begin
      for c in "1 20" "8 10" "32 5"; do set -- $c
        cl timeout 600 java -Xmx1g -Duser.timezone=UTC --add-opens java.base/java.nio=ALL-UNNAMED -cp "$JDBC" "$HERE/clients/Lat.java" \
          "jdbc:arrow-flight-sql://localhost:32010/?useEncryption=false" $1 $2 "$O/small-jdbc-c$1.csv" 2>"$O/small-jdbc-c$1.err" | grep '^jdbc' >> "$O/result.txt"
        cl timeout 600 $PY -W ignore "$HERE/clients/lat.py" grpc://localhost:32010 $1 $2 "$O/small-adbc-c$1.csv" \
          2>"$O/small-adbc-c$1.err" | grep '^adbc' >> "$O/result.txt"
      done
      step small end; mem small ;;
    sf10) step jdbc10 begin; tpch jdbc10 sf10 2; step jdbc10 end; mem jdbc10 ;;
    adbc10) step adbc10 begin; tpch_adbc adbc10 2; step adbc10 end; mem adbc10 ;;
    scan)
      step scan begin
      for c in 1 4 8; do
        cl timeout 900 java -Xmx1g -XX:MaxDirectMemorySize=3g --add-opens java.base/java.nio=ALL-UNNAMED -Darrow.enable_unsafe_memory_access=true \
          -cp "$SRV/server.jar" "$HERE/clients/Scan.java" localhost 32010 $c 1 complete "SELECT * FROM tpch.lineitem" 2>"$O/scan-c$c.err" | grep '^scan' >> "$O/result.txt"
      done
      step scan end; mem scan ;;
    adbcscan)
      step adbcscan begin
      cl timeout 900 $PY -W ignore "$HERE/clients/scan_adbc.py" grpc://localhost:32010 "SELECT * FROM tpch.lineitem" \
        2>"$O/adbcscan.err" | grep '^adbcscan' >> "$O/result.txt"
      step adbcscan end; mem adbcscan ;;
    heavy4)
      step heavy4 begin
      for q in q01 q09 q18 q21; do
        mkdir -p "$O/h-$q/q" "$O/heavy4-$q"; cp "$HERE/queries/tpch/$q.sql" "$O/h-$q/q/"
        cl timeout 1200 java -Duser.timezone=UTC --add-opens java.base/java.nio=ALL-UNNAMED -cp "$JDBC" "$HERE/clients/FlightTpch.java" \
          "jdbc:arrow-flight-sql://localhost:32010/?useEncryption=false" "$O/h-$q/q" 1 "$O/heavy4-$q" > "$O/heavy4-$q/runner.txt" 2>&1 &
        pids+=($!)
      done
      wait "${pids[@]}"; pids=()
      echo "heavy4: $(for q in q01 q09 q18 q21; do awk -F'\t' -v q=$q 'NR==2{printf "%s=%s/%s/%s ", q, $2, $5, $4}' "$O/heavy4-$q/summary.tsv" 2>/dev/null; done)" >> "$O/result.txt"
      step heavy4 end; mem heavy4 ;;
    load)  # closed-loop small-query load steps (Report 2): 10 s warm-up + 60 s per step, JDBC and ADBC
      for c in 1 8 32 64 128; do
        step load-jdbc-c$c begin
        cl env SMALL_CLASSES=$LOAD_CLASSES LOAD_WARMUP_S=10 LOAD_DURATION_S=60 timeout 300 java -Xmx2g -Duser.timezone=UTC --add-opens java.base/java.nio=ALL-UNNAMED \
          -cp "$JDBC" "$HERE/clients/Lat.java" "jdbc:arrow-flight-sql://localhost:32010/?useEncryption=false" $c 0 "$O/load-jdbc-c$c.csv" \
          2>"$O/load-jdbc-c$c.err" | grep '^jdbc' | sed 's/^/load /' >> "$O/result.txt"
        step load-jdbc-c$c end; mem load-jdbc-c$c
        step load-adbc-c$c begin
        cl env SMALL_CLASSES=$LOAD_CLASSES timeout 300 $PY -W ignore "$HERE/clients/load.py" grpc://localhost:32010 $c 10 60 "$O/load-adbc-c$c.csv" \
          2>"$O/load-adbc-c$c.err" | grep '^adbc' | sed 's/^/load /' >> "$O/result.txt"
        step load-adbc-c$c end; mem load-adbc-c$c
      done ;;
    mixed)  # 32 ADBC small-query clients alone, then with 2 heavy SF10 streams (q01, q18 back to back over ADBC)
      step mixed-base begin
      cl env SMALL_CLASSES=$LOAD_CLASSES timeout 300 $PY -W ignore "$HERE/clients/load.py" grpc://localhost:32010 32 10 60 "$O/mixed-base.csv" \
        2>"$O/mixed-base.err" | grep '^adbc' | sed 's/^/mixed-base /' >> "$O/result.txt"
      step mixed-base end; mem mixed-base
      step mixed begin
      cl env SMALL_CLASSES=$LOAD_CLASSES timeout 300 $PY -W ignore "$HERE/clients/load.py" grpc://localhost:32010 32 10 60 "$O/mixed-small.csv" \
        2>"$O/mixed-small.err" | grep '^adbc' | sed 's/^/mixed-small /' >> "$O/result.txt" &
      pids=($!)
      for q in q01 q18; do
        ( mkdir -p "$O/mixq-$q"; cp "$QUERIES/$q.sql" "$O/mixq-$q/"; end=$(( $(date +%s) + 73 )); i=0
          while [ "$(date +%s)" -lt $end ]; do
            cl timeout 900 $PY -W ignore "$HERE/clients/tpch_adbc.py" grpc://localhost:32010 "$O/mixq-$q" 1 "$O/mixed-$q-$i" > /dev/null 2>&1
            awk -F'\t' -v q=$q -v i=$i -v t="$(date +%s)" 'NR==2{print "mixed-heavy", q, i, $2, $5, $3, $4, t}' "$O/mixed-$q-$i/summary.tsv" >> "$O/mixed-heavy.txt"
            i=$((i + 1)); done ) &
        pids+=($!)
      done
      wait "${pids[@]}"; pids=()
      step mixed end; mem mixed ;;
    heavy4a)  # 4 heavy SF10 queries at once over ADBC (every server answers ADBC)
      step heavy4a begin
      for q in q01 q09 q18 q21; do
        mkdir -p "$O/h4-$q"; cp "$QUERIES/$q.sql" "$O/h4-$q/"
        cl timeout 1200 $PY -W ignore "$HERE/clients/tpch_adbc.py" grpc://localhost:32010 "$O/h4-$q" 1 "$O/heavy4a-$q" > /dev/null 2>&1 &
        pids+=($!)
      done
      wait "${pids[@]}"; pids=()
      echo "heavy4a: $(for q in q01 q09 q18 q21; do awk -F'\t' -v q=$q 'NR==2{printf "%s=%s/%s/%s/%s ", q, $2, $5, $3, $4}' "$O/heavy4a-$q/summary.tsv" 2>/dev/null; done)" >> "$O/result.txt"
      step heavy4a end; mem heavy4a ;;
    netem)  # client path limited on loopback: netem 5 ms each way (10 ms RTT), 1 Gbit/s; SF10 TPC-H + full lineitem export over ADBC
      sudo tc qdisc add dev lo root netem delay 5ms rate 1gbit limit 100000 && tc qdisc show dev lo >> "$O/netem.txt"
      step netem10 begin; tpch_adbc netem10 2; step netem10 end; mem netem10
      step netemscan begin
      cl timeout 900 $PY -W ignore "$HERE/clients/scan_adbc.py" grpc://localhost:32010 "SELECT * FROM tpch.lineitem" \
        2>"$O/netemscan.err" | grep '^adbcscan' | sed 's/^/netem /' >> "$O/result.txt"
      step netemscan end; mem netemscan
      sudo tc qdisc del dev lo root ;;
    coldstart)  # Report 3: 5 cold starts on SF10: port answers, start log line, first query, idle RSS
      for i in 1 2 3 4 5; do
        echo "== cold $i" >> "$O/start-times.txt"
        # shellcheck disable=SC2086
        start_server "$(data_dir $layout sf10)" $flags > "$O/coldstart-$i.txt" 2>&1 && { firstq; sleep 5; mem cold$i; }
      done ;;
    cancel)  # Report 3: cancel a running SF10 q18 / q21 after 3 s; server CPU sampled to see when it stops working
      for q in q18 q21; do
        step cancel-$q begin
        rm -f "$O/.cpu-stop"; cpuloop "$O/cancel-$q-cpu.txt" "$O/.cpu-stop" & local cp=$!
        sleep 2
        cl timeout 700 $PY -W ignore "$HERE/clients/cancel.py" grpc://localhost:32010 "$QUERIES/$q.sql" 3 2>"$O/cancel-$q.err" >> "$O/result.txt"
        sleep 20; touch "$O/.cpu-stop"; wait $cp; rm -f "$O/.cpu-stop"
        step cancel-$q end; mem cancel-$q
      done ;;
    soak)  # Report 3: 30 min of 32 ADBC small-query clients (6 x 5 min segments) + 1 heavy stream (q01 / q18 alternating);
           # JVM heap / GC / threads and RSS every 10 s
      step soak begin
      docker rm -f jsamp > /dev/null 2>&1
      docker run -d --name jsamp --pid container:flight --cap-add SYS_PTRACE --cpuset-cpus=$CPU_CL eclipse-temurin:21-jdk sleep infinity > /dev/null
      rm -f "$O/.soak-stop"
      ( while [ ! -e "$O/.soak-stop" ]; do
          { echo "== $(date +%s) $(docker exec flight sh -c 'grep -E "VmRSS|Threads" /proc/1/status' | tr -s ' \t\n' ' ')"
            docker exec jsamp sh -c 'jcmd 1 GC.heap_info | sed -n 2,4p; jcmd 1 PerfCounter.print | grep -E "sun.gc.collector.[0-9].(name|invocations|time)=|sun.os.hrt.frequency=|sun.rt.safepointTime="' 2>&1
          } >> "$O/soak-jvm.txt"; sleep 10; done ) & local jp=$!
      ( q=q01; i=0; while [ ! -e "$O/.soak-stop" ]; do
          mkdir -p "$O/soakq-$q"; cp "$QUERIES/$q.sql" "$O/soakq-$q/"
          cl timeout 900 $PY -W ignore "$HERE/clients/tpch_adbc.py" grpc://localhost:32010 "$O/soakq-$q" 1 "$O/soak-$q-$i" > /dev/null 2>&1
          awk -F'\t' -v q=$q -v i=$i -v t="$(date +%s)" 'NR==2{print "soak-heavy", q, i, $2, $5, $3, $4, t}' "$O/soak-$q-$i/summary.tsv" >> "$O/soak-heavy.txt"
          i=$((i + 1)); [ $q = q01 ] && q=q18 || q=q01; done ) & local hp=$!
      for seg in 1 2 3 4 5 6; do
        cl env SMALL_CLASSES=$LOAD_CLASSES timeout 600 $PY -W ignore "$HERE/clients/load.py" grpc://localhost:32010 32 $([ $seg = 1 ] && echo 10 || echo 0) 300 \
          "$O/soak-seg$seg.csv" 2>"$O/soak-seg$seg.err" | grep '^adbc' | sed "s/^/soak seg=$seg /" >> "$O/result.txt"
        alive soak-seg$seg || break
      done
      touch "$O/.soak-stop"; wait $jp $hp; rm -f "$O/.soak-stop"; docker rm -f jsamp > /dev/null 2>&1
      step soak end; mem soak ;;
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
  touch "$O/.stats-stop"; wait "$statspid" 2>/dev/null; rm -f "$O/.stats-stop"
  docker inspect -f 'container exit={{.State.ExitCode}} oom={{.State.OOMKilled}} running={{.State.Running}}' flight >> "$O/container.txt" 2>/dev/null
  docker rm -f flight >/dev/null 2>&1
}

for r in $(seq 1 "$ROUNDS"); do
  if [ $((r % 2)) = 1 ]; then side A "$r"; side B "$r"; else side B "$r"; side A "$r"; fi
done
docker rm -f client s3 >/dev/null 2>&1
log "done"
