#!/usr/bin/env bash
# One cell of accept-hdfs.yml: an HDFS cluster, the server(s) of one pre-release on it, ci/accept/check.py.
#
# Usage: ci/accept/cluster.sh <sasl|open> <default|speed> <1|3> <in dir> <work dir>
#
# Cluster (Docker network 172.31.0.0/24): MIT KDC .5 (realm CI.TEST), ZooKeeper .6, Hadoop 3.1.3
# NameNodes nn1 .10 / nn2 .11 (HA nameservice ns1, ZKFC automatic failover, shared edits directory),
# DataNodes dn1-dn3 .12-.14 with Kerberos, block access tokens and a short-circuit domain socket.
#   sasl: dfs.data.transfer.protection=authentication (a plain TCP read is refused; the cell proves it)
#   open: the reference, same everything without data-transfer protection (ignore.secure.ports.for.testing)
# Servers: one per DataNode (1: dn1 only, 3: all), in that DataNode's network namespace with its domain
# socket, Flight over TLS (one test CA, a certificate per node IP) with Kerberos client authentication
# (FLIGHT_KERBEROS_*, principal flight/<ip>@CI.TEST, which is also the server's HDFS login).
# Data (ci/accept/data.py): /data/tpch replication 3; /data/spread/lineitem_sp (1 MiB blocks, replication
# 2), orders_sp (1 MiB blocks, replication 1): no DataNode may hold any of their files whole (fsck, else
# the cell fails); /data/spread/part_far: its FIRST file (0.parquet) only on dn3, the rest replication 2.
# Stages: main (checks 1, 2), partial (check 3, 3 servers), smalldisk (check 4: servers restarted with
# -DhdfsLocalCopyDir on a 64 MiB tmpfs each), lowdirect (check 5, 3 servers, speed + distributedComplete,
# -XX:MaxDirectMemorySize=512m; run in the speed cell), log checks (check 6).
# Writes <work>/cell.json (checks of this cell; answers in <work>/<stage>.json). Test-only principals,
# keytabs and certificates, all made in the job.
set -u
prot=$1 profile=$2 n=$3 in=$4 work=$5
here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$work"; : > "$work/notes.txt"
note() { echo "$*" | tee -a "$work/notes.txt"; }
declare -A CHECK
setc() { CHECK[$1]="$2|$(echo "${3:-}" | head -n 1 | tr '|' '/' | cut -c1-600)"; note "check $1: $2 ${3:-}"; }
dump() {
  python3 - "$work/cell.json" "$prot" "$profile" "$n" <<EOF
import json, sys
checks = {}
for line in """$(for k in "${!CHECK[@]}"; do echo "$k|${CHECK[$k]}"; done)""".splitlines():
    if line.strip():
        k, s, d = (line.split("|", 2) + ["", ""])[:3]
        checks[k] = {"status": s, "detail": d}
json.dump({"protection": sys.argv[2], "profile": sys.argv[3], "servers": int(sys.argv[4]), "checks": checks,
           "notes": open("$work/notes.txt").read().splitlines()}, open(sys.argv[1], "w"), indent=1)
EOF
}
logs() { for c in kdc zk nn1 nn2 dn1 dn2 dn3 srv1 srv2 srv3 sd1 sd2 sd3 lm1 lm2 lm3; do docker logs "$c" > "$work/$c.log" 2>&1 || rm -f "$work/$c.log"; done; }
abort() { setc setup fail "$1"; logs; dump; exit 1; }

image=accept-hadoop:3.1.3
dnIp() { echo "172.31.0.$(( 11 + $1 ))"; }
docker network create --subnet 172.31.0.0/24 hd > /dev/null || abort "docker network not created"
hd=/srv/hd
sudo rm -rf "$hd"; sudo install -d -o 1000 -g 1000 -m 755 "$hd" "$hd/nn1" "$hd/nn2" "$hd/shared" "$hd/krb" "$hd/sock1" "$hd/sock2" "$hd/sock3"
conf="$work/conf"; mkdir -p "$conf"
docker run --rm "$image" hadoop checknative 2>&1 | tee "$work/checknative.txt" | grep -qE '^hadoop: +true' || abort "Hadoop 3.1.3 native library does not load (no short-circuit): $(head -c 300 "$work/checknative.txt")"

P() { echo "$1/$2@CI.TEST"; }
core=(fs.defaultFS hdfs://ns1 hadoop.security.authentication kerberos hadoop.security.authorization false
  hadoop.rpc.protection authentication ha.zookeeper.quorum 172.31.0.6:2181)
hdfs=(dfs.nameservices ns1 dfs.ha.namenodes.ns1 nn1,nn2
  dfs.namenode.rpc-address.ns1.nn1 172.31.0.10:8020 dfs.namenode.rpc-address.ns1.nn2 172.31.0.11:8020
  dfs.namenode.http-address.ns1.nn1 172.31.0.10:9870 dfs.namenode.http-address.ns1.nn2 172.31.0.11:9870
  dfs.namenode.shared.edits.dir file:///hd/shared dfs.ha.automatic-failover.enabled true
  dfs.ha.fencing.methods 'shell(/bin/true)'
  dfs.client.failover.proxy.provider.ns1 org.apache.hadoop.hdfs.server.namenode.ha.ConfiguredFailoverProxyProvider
  dfs.replication 3 dfs.permissions.enabled false dfs.namenode.rpc-bind-host 0.0.0.0 dfs.namenode.http-bind-host 0.0.0.0
  dfs.namenode.name.dir /hd/name dfs.datanode.data.dir /tmp/hdfs/dn dfs.namenode.datanode.registration.ip-hostname-check false
  dfs.client.read.shortcircuit true dfs.domain.socket.path /var/run/hdfs-sockets/dn
  dfs.block.access.token.enable true
  dfs.namenode.kerberos.principal "$(P nn hdfs.ci)" dfs.namenode.keytab.file /hd/krb/hdfs.keytab
  dfs.namenode.kerberos.internal.spnego.principal '*'
  dfs.datanode.kerberos.principal "$(P dn hdfs.ci)" dfs.datanode.keytab.file /hd/krb/hdfs.keytab
  dfs.web.authentication.kerberos.principal '*' dfs.web.authentication.kerberos.keytab /hd/krb/hdfs.keytab
  ignore.secure.ports.for.testing true
  dfs.namenode.heartbeat.recheck-interval 15000)
[ "$prot" = sasl ] && hdfs+=(dfs.data.transfer.protection authentication)
xml() { echo '<?xml version="1.0"?>'; echo '<configuration>'
  while [ $# -ge 2 ]; do printf '  <property><name>%s</name><value>%s</value></property>\n' "$1" "$2"; shift 2; done
  echo '</configuration>'; }
xml "${core[@]}" > "$conf/core-site.xml"
xml "${core[@]}" "${hdfs[@]}" > "$conf/hdfs-site.xml"
cat > "$conf/krb5.conf" <<'EOF'
[libdefaults]
  default_realm = CI.TEST
  dns_lookup_kdc = false
  dns_lookup_realm = false
  rdns = false
  dns_canonicalize_hostname = false
  udp_preference_limit = 1
  forwardable = true
  ticket_lifetime = 4h
[realms]
  CI.TEST = {
    kdc = 172.31.0.5:88
    admin_server = 172.31.0.5
  }
EOF
note "HDFS Hadoop 3.1.3 (archive tarball on temurin 8), ns1 = nn1 + nn2 with ZKFC on ZooKeeper, Kerberos CI.TEST, 3 DataNodes, data-transfer protection: $([ "$prot" = sasl ] && echo authentication || echo 'none (reference)'); $n server(s), profile $profile"

# KDC: HDFS service principals, flight/<ip> per server node, the client principal tester.
cat > "$work/kdc.sh" <<'EOF'
set -e
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq && apt-get install -y -qq --no-install-recommends krb5-kdc krb5-admin-server krb5-user > /dev/null
cp /conf/krb5.conf /etc/krb5.conf; mkdir -p /etc/krb5kdc
printf '%s\n' '[realms]' ' CI.TEST = {' '  master_key_type = aes256-cts-hmac-sha1-96' \
  '  supported_enctypes = aes256-cts-hmac-sha1-96:normal aes128-cts-hmac-sha1-96:normal' ' }' > /etc/krb5kdc/kdc.conf
kdb5_util create -s -r CI.TEST -P "$KPASS" > /dev/null
for p in nn/hdfs.ci dn/hdfs.ci HTTP/hdfs.ci HTTP/172.31.0.10 HTTP/172.31.0.11; do kadmin.local -q "addprinc -randkey $p@CI.TEST" > /dev/null; done
# fsck and the other web calls go to http://<NameNode IP>:9870 (SPNEGO for HTTP/<IP>); the NameNodes accept every HTTP/ principal of the keytab
kadmin.local -q "ktadd -k /krb/hdfs.keytab nn/hdfs.ci@CI.TEST dn/hdfs.ci@CI.TEST HTTP/hdfs.ci@CI.TEST HTTP/172.31.0.10@CI.TEST HTTP/172.31.0.11@CI.TEST" > /dev/null
for i in 1 2 3; do ip=172.31.0.$((11 + i)); kadmin.local -q "addprinc -randkey flight/$ip@CI.TEST" > /dev/null
  kadmin.local -q "ktadd -k /krb/flight$i.keytab flight/$ip@CI.TEST" > /dev/null; done
kadmin.local -q "addprinc -randkey tester@CI.TEST" > /dev/null
kadmin.local -q "ktadd -k /krb/tester.keytab tester@CI.TEST" > /dev/null
krb5kdc
for _ in $(seq 30); do kinit -kt /krb/hdfs.keytab -c /krb/nn.ccache nn/hdfs.ci@CI.TEST 2> /dev/null && break; sleep 1; done
chmod 644 /krb/*; touch /krb/ready
exec tail -F /var/log/krb5kdc.log /dev/null
EOF
docker run -d --name kdc --network hd --ip 172.31.0.5 -e KPASS="$(openssl rand -hex 16)" -v "$conf:/conf:ro" -v "$hd/krb:/krb" \
  -v "$work/kdc.sh:/kdc.sh:ro" ubuntu:24.04 bash /kdc.sh > /dev/null
docker run -d --name zk --network hd --ip 172.31.0.6 zookeeper:3.8 > /dev/null
for _ in $(seq 180); do [ -f "$hd/krb/ready" ] && break; sleep 1; done
[ -f "$hd/krb/ready" ] || abort "KDC did not come up: $(docker logs kdc 2>&1 | tail -n 3)"

hconf=(-v "$conf/core-site.xml:/opt/hadoop/etc/hadoop/core-site.xml:ro" -v "$conf/hdfs-site.xml:/opt/hadoop/etc/hadoop/hdfs-site.xml:ro"
  -v "$conf/krb5.conf:/etc/krb5.conf:ro" -v "$hd/krb:/hd/krb:ro")
kenv=(-e KRB5CCNAME=/hd/krb/nn.ccache)
docker run -d --name nn1 --network hd --ip 172.31.0.10 --hostname nn1 "${hconf[@]}" "${kenv[@]}" -v "$hd/nn1:/hd/name" -v "$hd/shared:/hd/shared" "$image" \
  bash -c 'hdfs namenode -format -nonInteractive -force > /tmp/format.log 2>&1 || { cat /tmp/format.log; exit 1; }
    hdfs zkfc -formatZK -nonInteractive -force > /tmp/zkformat.log 2>&1 || { cat /tmp/zkformat.log; exit 1; }
    touch /hd/name/.formatted; while [ ! -f /hd/name/.go ]; do sleep 1; done
    hdfs zkfc > /tmp/zkfc.log 2>&1 & exec hdfs namenode' > /dev/null
for _ in $(seq 180); do [ -f "$hd/nn1/.formatted" ] && break; [ "$(docker inspect -f '{{.State.Running}}' nn1)" = true ] || break; sleep 1; done
[ -f "$hd/nn1/.formatted" ] || abort "NameNode / ZKFC format failed: $(docker logs nn1 2>&1 | grep -m 1 -E 'Exception|ERROR' | cut -c1-250)"
sudo rm -rf "$hd/nn2"; sudo cp -a "$hd/nn1" "$hd/nn2"
docker run -d --name nn2 --network hd --ip 172.31.0.11 --hostname nn2 "${hconf[@]}" "${kenv[@]}" -v "$hd/nn2:/hd/name" -v "$hd/shared:/hd/shared" "$image" \
  bash -c 'hdfs zkfc > /tmp/zkfc.log 2>&1 & exec hdfs namenode' > /dev/null
sudo touch "$hd/nn1/.go"
for i in 1 2 3; do
  docker run -d --name "dn$i" --network hd --ip "$(dnIp "$i")" --hostname "dn$i" "${hconf[@]}" "${kenv[@]}" -v "$hd/sock$i:/var/run/hdfs-sockets" "$image" hdfs datanode > /dev/null
done
state=""
for _ in $(seq 150); do
  s1=$(docker exec nn1 hdfs haadmin -getServiceState nn1 2>/dev/null | tail -n 1); s2=$(docker exec nn1 hdfs haadmin -getServiceState nn2 2>/dev/null | tail -n 1)
  state="nn1=$s1 nn2=$s2"
  { [ "$s1" = active ] && [ "$s2" = standby ]; } || { [ "$s1" = standby ] && [ "$s2" = active ]; } && break
  sleep 2
done
note "HA states (ZKFC elected): $state"
[[ $state == *active* && $state == *standby* ]] || abort "ZKFC did not elect an active and a standby NameNode: $state; $(docker exec nn1 grep -m 1 -E 'Exception|ERROR' /tmp/zkfc.log 2>/dev/null | cut -c1-200)"
active=nn1; [[ $state == *"nn2=active"* ]] && active=nn2
for _ in $(seq 150); do
  report=$(docker exec "$active" hdfs dfsadmin -report 2>/dev/null)
  [[ $report == *"Live datanodes (3)"* && $report != *'Safe mode is ON'* ]] && break
  sleep 2
done
[[ $report == *"Live datanodes (3)"* ]] || abort "HDFS did not come up: $(docker logs dn1 2>&1 | grep -m 1 -E 'Exception|ERROR' | cut -c1-250)"

# Data layout
docker cp "$in/data" "$active:/tmp/upload" > /dev/null
docker cp "$in/data/far/part_far/0.parquet" dn3:/tmp/far0.parquet > /dev/null
docker exec "$active" bash -c 'set -e; hdfs dfs -mkdir -p /data/tpch /data/spread/lineitem_sp /data/spread/orders_sp /data/spread/part_far
  hdfs dfs -D dfs.replication=3 -put /tmp/upload/tpch/* /data/tpch/
  hdfs dfs -D dfs.replication=2 -D dfs.blocksize=1048576 -put /tmp/upload/tpch/lineitem/* /data/spread/lineitem_sp/
  hdfs dfs -D dfs.replication=1 -D dfs.blocksize=1048576 -put /tmp/upload/tpch/orders/* /data/spread/orders_sp/
  hdfs dfs -D dfs.replication=2 -put /tmp/upload/far/part_far/1.parquet /tmp/upload/far/part_far/2.parquet /data/spread/part_far/' > "$work/upload.log" 2>&1 \
  || abort "HDFS upload failed: $(grep -m 1 -E 'Exception|ERROR|rror' "$work/upload.log" | cut -c1-250)"
# writer-local placement: a put from dn3 with replication 1 keeps the block on dn3
docker exec dn3 hdfs dfs -D dfs.replication=1 -put /tmp/far0.parquet /data/spread/part_far/0.parquet > "$work/upload-far.log" 2>&1 \
  || abort "HDFS upload of part_far/0.parquet from dn3 failed: $(grep -m 1 -E 'Exception|rror' "$work/upload-far.log" | cut -c1-250)"
docker exec "$active" hdfs fsck /data/spread -files -blocks -locations > "$work/fsck-spread.log" 2>&1 \
  || abort "fsck failed: $(grep -m 1 -E 'Exception|rror' "$work/fsck-spread.log" | cut -c1-250)"
python3 - "$work/fsck-spread.log" > "$work/layout.txt" <<'EOF' || abort "layout: $(tail -n 1 "$work/layout.txt")"
import re, sys
files, cur = {}, None
for line in open(sys.argv[1]):
    m = re.match(r"^(/data/spread/\S+) \d+ bytes", line)
    if m:
        cur = m.group(1); files[cur] = []; continue
    if cur and re.match(r"^\d+\. BP-", line):
        files[cur].append(set(re.findall(r"172\.31\.0\.(1[234]):", line)))
bad = []
for f, blocks in sorted(files.items()):
    held = {dn: sum(dn in b for b in blocks) for dn in ("12", "13", "14")}
    print(f, len(blocks), "blocks", " ".join(f"dn{int(k) - 11}={v}" for k, v in held.items()))
    if "/part_far/0.parquet" in f:
        if held != {"12": 0, "13": 0, "14": len(blocks)}:
            bad.append(f"{f} must be on dn3 only: {held}")
    elif "/part_far/" not in f and (len(blocks) < 2 or max(held.values()) >= len(blocks)):
        bad.append(f"{f}: a DataNode holds it whole ({len(blocks)} blocks, {held})")
print("layout ok" if not bad else "layout FAIL: " + "; ".join(bad))
sys.exit(1 if bad else 0)
EOF
[ "$(grep -c ' blocks ' "$work/layout.txt")" -ge 18 ] || abort "layout: fsck listed $(grep -c ' blocks ' "$work/layout.txt") spread files, want 19"
note "layout: $(grep -c ' blocks ' "$work/layout.txt") spread files, $(tail -n 1 "$work/layout.txt")"
if [ "$prot" = sasl ]; then
  probe=$(docker exec "$active" hdfs dfs -ls /data/tpch/region 2>/dev/null | awk '$1 ~ /^-/ {print $NF}' | head -n 1)
  if docker exec "$active" hdfs dfs -Ddfs.data.transfer.protection= -cat "$probe" > /dev/null 2> "$work/probe-plain.log"; then
    abort "a DataNode served a TCP read without SASL ($probe): data-transfer protection is not enforced"
  fi
  docker exec "$active" hdfs dfs -cat "$probe" > /dev/null 2> "$work/probe-sasl.log" || abort "a SASL TCP read failed: $(grep -m 1 -E 'Exception|ERROR' "$work/probe-sasl.log" | cut -c1-200)"
  note "SASL enforced: plain TCP read refused, SASL read passes"
fi

# TLS: one test CA, a certificate per server IP
tls="$work/tls"; mkdir -p "$tls"
openssl req -x509 -newkey rsa:2048 -nodes -days 2 -subj "/CN=accept-ci-ca" -keyout "$tls/ca.key" -out "$tls/ca.pem" 2> /dev/null
for i in 1 2 3; do
  openssl req -newkey rsa:2048 -nodes -subj "/CN=$(dnIp "$i")" -keyout "$tls/s$i.key" -out "$tls/s$i.csr" 2> /dev/null
  printf 'subjectAltName=IP:%s\nextendedKeyUsage=serverAuth\n' "$(dnIp "$i")" > "$tls/s$i.ext"
  openssl x509 -req -in "$tls/s$i.csr" -CA "$tls/ca.pem" -CAkey "$tls/ca.key" -CAcreateserial -days 2 -extfile "$tls/s$i.ext" -out "$tls/s$i.crt" 2> /dev/null
  openssl pkcs8 -topk8 -nocrypt -in "$tls/s$i.key" -out "$tls/s$i.pk8"
done
chmod 644 "$tls"/*; export ACCEPT_CA="$tls/ca.pem"
secret=$(openssl rand -base64 48 | tr -d '\n')
# client: Kerberos ticket of tester@CI.TEST on the runner
export KRB5_CONFIG="$conf/krb5.conf" KRB5CCNAME="$work/tester.ccache"
kinit -kt "$hd/krb/tester.keytab" tester@CI.TEST || abort "client kinit failed"

native=(-v "$in/hnative:/hnative:ro" -e LD_LIBRARY_PATH=/hnative)
base_opts="-Djava.library.path=/hnative -Djava.security.krb5.conf=/etc/krb5.conf"
[ "$profile" = speed ] && base_opts="$base_opts -DresourceProfile=speed"
peers=$(for i in $(seq "$n"); do printf '%s:5701,' "$(dnIp "$i")"; done); peers=${peers%,}
cpus=2 mem=5g xmx=2g; [ "$n" -gt 1 ] && cpus=1.2 mem=3g xmx=1g
# start <prefix> <extra JVM options> <direct> [extra docker args...]: one server per node 1..n
start() {
  local pre=$1 extra=$2 direct=$3 i c; shift 3
  for i in $(seq "$n"); do
    local cm=(); [ -n "${COPIES:-}" ] && cm=(-v "$(printf "$COPIES" "$i"):/copies")
    # shellcheck disable=SC2086
    docker run -d --name "$pre$i" "${cm[@]}" --network "container:dn$i" -v "$hd/sock$i:/var/run/hdfs-sockets" "${native[@]}" "$@" \
      --cpus=$cpus --memory=$mem -v "$in/app:/app:ro" -v "$in/extdir:/extdir:ro" -v "$JAVA_HOME_21_X64:/jdk:ro" -v "$conf:/conf:ro" \
      -v "$conf/krb5.conf:/etc/krb5.conf:ro" -v "$hd/krb/flight$i.keytab:/krb/flight.keytab:ro" -v "$tls:/tls:ro" \
      -e KRB5_CONFIG=/etc/krb5.conf -e KRB5CCNAME=/tmp/krb5cc_flight \
      -e FLIGHT_TLS_CERT=/tls/s$i.crt -e FLIGHT_TLS_KEY=/tls/s$i.pk8 \
      -e FLIGHT_KERBEROS_PRINCIPAL="flight/$(dnIp "$i")@CI.TEST" -e FLIGHT_KERBEROS_KEYTAB=/krb/flight.keytab \
      -e FLIGHT_KERBEROS_SESSION_SECRET="$secret" \
      -e DUCKDB_ALLOW_UNSIGNED_EXTENSIONS=true -e FLIGHT_PLUGINS_DIR=/app/plugins -e LIBHDFS3_CONF=/conf/hdfs-site.xml -e LANG=C.UTF-8 \
      accept-server /jdk/bin/java -Xmx$xmx -XX:MaxDirectMemorySize=$direct --add-opens=java.base/java.lang=ALL-UNNAMED \
      --add-opens=java.base/java.nio=ALL-UNNAMED --add-opens=java.base/java.util=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED \
      -Dio.netty.tryReflectionSetAccessible=true -Dhazelcast.phone.home.enabled=false -DnumServers=$n \
      $base_opts $extra -DhdfsKerberosPrincipal="flight/$(dnIp "$i")@CI.TEST" -DhdfsKerberosKeytab=/krb/flight.keytab \
      -Darrowflight.duckdb.extensionDir=/extdir \
      -cp "/conf:/app/arrow-flight-server.jar:/app/libs/*" pro.surpin.data.arrowflight.server.HadoopArrowFlightServer \
      --data-dir hdfs://ns1/data --localhost "$(dnIp "$i")" --port 32010 --hazelcast-port 5701 \
      --hosts "$peers" --metrics-enabled false > /dev/null
  done
  for i in $(seq "$n"); do
    c="$pre$i"
    for _ in $(seq 240); do
      docker logs "$c" 2>&1 | grep -q 'Server Arrow Flight SQL started' && break
      [ "$(docker inspect -f '{{.State.Running}}' "$c")" = true ] || break
      sleep 1
    done
    docker logs "$c" 2>&1 | grep -q 'Server Arrow Flight SQL started' \
      || { docker logs "$c" 2>&1 | tail -n 40; return 1; }
  done
  sleep 3
}
stop() { local i; for i in $(seq "$n"); do docker stop -t 20 "$1$i" > /dev/null 2>&1; done; }
servers=$(for i in $(seq "$n"); do printf '%s:32010,' "$(dnIp "$i")"; done); servers=${servers%,}
py="$RUNNER_TEMP/py/bin/python"
fdRequests() { local t=0 i; for i in 1 2 3; do t=$(( t + $(docker logs "dn$i" 2>&1 | grep -c 'REQUEST_SHORT_CIRCUIT_FDS') )); done; echo "$t"; }
fds0=$(fdRequests)

start srv "" 1g || abort "server did not start: $(docker logs srv1 2>&1 | grep -m 1 -E 'Exception|ERROR' | cut -c1-300)"
note "$(docker logs srv1 2>&1 | grep -m 1 -oE 'hdfs=shortCircuit .*' || echo 'no hdfs=shortCircuit line')"
note "$(docker logs srv1 2>&1 | grep -m 1 -oE '(Loaded the native-hadoop library|Unable to load native-hadoop library)' || echo 'no native-hadoop line')"
"$py" -I "$here/check.py" main "$servers" "$in" "$work/main.json" > "$work/main.log" 2>&1; rc=$?
tail -n 5 "$work/main.log"
[ "$rc" -eq 0 ] || setc client fail "check.py main exited $rc: $(grep -m 1 -E 'Error|Exception' "$work/main.log" | cut -c1-300)"
if [ "$n" -gt 1 ]; then
  "$py" -I "$here/check.py" partial "$servers" "$in" "$work/partial.json" > "$work/partial.log" 2>&1
  tail -n 3 "$work/partial.log"
  setc 3-partial "$(jq -r '.checks.partial.status // "fail"' "$work/partial.json" 2>/dev/null || echo fail)" "$(jq -r '.checks.partial.detail // "no result"' "$work/partial.json" 2>/dev/null)"
else
  setc 3-partial n/a "1 server"
fi
qcount=$(grep -cE '^(ok|err|FAIL) ' "$work"/main.log "$work"/partial.log 2>/dev/null | awk -F: '{ s += $NF } END { print s + 0 }')
for i in $(seq "$n"); do docker logs "srv$i" > "$work/srv$i.log" 2>&1; done
reads=$(cat "$work"/srv*.log | grep -c 'hdfs=reads ' || true)
netex=$(cat "$work"/srv*.log | grep -c 'HdfsNetworkException' || true)
sleep 2; fds1=$(fdRequests)
note "queries sent $qcount, hdfs=reads lines $reads, HdfsNetworkException $netex, DataNode short-circuit fd requests $fds0 -> $fds1"
d6=""
# per query (qid, ci/accept/logcheck.py): every query the servers ran has an hdfs=reads line
lc=$("$py" -I "$here/logcheck.py" "$work"/srv*.log); note "hdfs=reads by qid (main + partial): $lc"
[[ $lc == *" missing=0"* ]] || d6="$d6 queries without an hdfs=reads line: $lc;"
[ "$reads" -ge "$qcount" ] || d6="$d6 hdfs=reads lines $reads < queries sent $qcount;"
[ "$netex" -eq 0 ] || d6="$d6 HdfsNetworkException x$netex: $(cat "$work"/srv*.log | grep -m 1 'HdfsNetworkException' | cut -c1-250);"
[ "$fds1" -gt "$fds0" ] || d6="$d6 short-circuit fd counters did not grow ($fds0 -> $fds1);"
stop srv

# check 4: copy disk on a 64 MiB tmpfs per node (-DhdfsLocalCopyDir=/copies)
for i in $(seq "$n"); do
  d="$work/copies$i"; mkdir -p "$d"; sudo mount -t tmpfs -o size=64m,mode=1777 tmpfs "$d" || abort "tmpfs not mounted"
done
( while :; do for i in $(seq "$n"); do echo "$i $(df -B1 --output=used "$work/copies$i" | tail -n 1)"; done; sleep 0.2; done ) > "$work/smalldisk-used.txt" 2>/dev/null &
sampler=$!
if COPIES="$work/copies%d" start sd "-DhdfsLocalCopyDir=/copies" 1g; then
  "$py" -I "$here/check.py" smalldisk "$servers" "$in" "$work/smalldisk.json" > "$work/smalldisk.log" 2>&1
  tail -n 3 "$work/smalldisk.log"
  st=$(jq -r '.checks.smalldisk.status // "fail"' "$work/smalldisk.json" 2>/dev/null || echo fail)
  dt=$(jq -r '.checks.smalldisk.detail // "no result"' "$work/smalldisk.json" 2>/dev/null)
else
  st=fail dt="server with hdfsLocalCopyDir did not start: $(docker logs sd1 2>&1 | grep -m 1 -E 'Exception|ERROR' | cut -c1-250)"
fi
kill "$sampler" 2>/dev/null; wait "$sampler" 2>/dev/null
peak=$(awk '{ print $2 }' "$work/smalldisk-used.txt" | sort -n | tail -n 1)
for i in $(seq "$n"); do docker logs "sd$i" > "$work/sd$i.log" 2>&1; done
nospace=$(cat "$work"/sd*.log | grep -ciE 'No space left on device' || true)
copydir=$(cat "$work"/sd*.log | grep -c 'hdfs=localCopyCache dir=/copies' || true)
batches=$(cat "$work"/sd*.log | grep -cE 'hdfs=(copyBatches|completeInCopyBatches)' || true)
note "small disk: peak use ${peak:-?} of 67108864 bytes, copy batches $batches, copy dir lines $copydir, 'No space left' $nospace"
[ -n "$peak" ] && [ "$peak" -lt 67108864 ] || { st=fail; dt="$dt; tmpfs full (peak ${peak:-?})"; }
[ "$nospace" -eq 0 ] || { st=fail; dt="$dt; 'No space left on device' in a server log"; }
setc 4-smalldisk "$st" "${dt#; }"
reads=$(( reads + $(cat "$work"/sd*.log | grep -c 'hdfs=reads ' || true) ))
netex=$(( netex + $(cat "$work"/sd*.log | grep -c 'HdfsNetworkException' || true) ))
stop sd
for i in $(seq "$n"); do sudo umount "$work/copies$i" || true; done

# check 5: low direct memory (3 servers, speed + distributedComplete, -XX:MaxDirectMemorySize=512m), in the speed cell
if [ "$n" -gt 1 ] && [ "$profile" = speed ]; then
  if start lm "-DdistributedComplete=true" 512m; then
    "$py" -I "$here/check.py" lowdirect "$servers" "$in" "$work/lowdirect.json" > "$work/lowdirect.log" 2>&1
    tail -n 5 "$work/lowdirect.log"
    st=$(jq -r '.checks.lowdirect.status // "fail"' "$work/lowdirect.json" 2>/dev/null || echo fail)
    dt=$(jq -r '.checks.lowdirect.detail // "no result"' "$work/lowdirect.json" 2>/dev/null)
  else
    st=fail dt="servers with 512m direct memory did not start: $(docker logs lm1 2>&1 | grep -m 1 -E 'Exception|ERROR' | cut -c1-250)"
  fi
  for i in $(seq "$n"); do docker logs "lm$i" > "$work/lm$i.log" 2>&1; done
  oom=$(cat "$work"/lm*.log | grep -c 'OutOfMemoryError' || true)
  merged=$(grep -c 'distributedComplete=merged' "$work/lm1.log" || true)
  note "low direct memory: OutOfMemoryError $oom, distributedComplete=merged lines on node 1: $merged"
  [ "$oom" -eq 0 ] || { st=fail; dt="$dt; OutOfMemoryError: $(cat "$work"/lm*.log | grep -m 1 'OutOfMemoryError' | cut -c1-200)"; }
  setc 5-lowdirect "$st" "${dt#; }"
  stop lm
else
  setc 5-lowdirect n/a "run in the 3-server speed cell only"
fi

# check 6: server logs and DataNode counters
[ "$netex" -eq 0 ] || d6="$d6 HdfsNetworkException (copy disk / low direct stages);"
if [ -z "$d6" ]; then setc 6-logs pass "hdfs=reads lines $reads for $qcount queries ($lc), short-circuit fd requests +$(( fds1 - fds0 )), no HdfsNetworkException"
else setc 6-logs fail "${d6# }"; fi
setc setup pass ""
logs; dump
exit 0
