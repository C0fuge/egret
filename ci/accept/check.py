"""Client of the HDFS acceptance check (ci/accept/cluster.sh runs it on the runner).

  check.py <stage> <host:port,...> <in-dir> <out.json>

Every connection is Flight SQL over TLS (CA <in>/../tls/ca.pem, env ACCEPT_CA) with Kerberos: a SPNEGO
token for flight/<host>@CI.TEST (python-gssapi, the runner's ticket cache) is sent once as
"Authorization: Negotiate ..." and the server's signed "Bearer ..." session is then used by ADBC.

Stages (answers are digests, ci/accept/digest.py; out.json maps "<query id>@n<node>" to a digest or
{"error": ...}; the report compares them with the reference cell and with <in>/expected.json):
  main       complete mode. Node 1: TPC-H plain and schema-qualified, spread, far, full scans; every
             other node: TPC-H plain, spread, far.
  partial    3 servers, header x-flight-result-mode: partial on every node: the per-node parts, summed
             per group, must equal the complete answer (check 3); pass/fail written here.
  smalldisk  copy disk of 64 MiB (check 4): complete and partial count / GROUP BY / scans of the spread
             tables exact; the lineitem_sp x orders_sp join exact or RESOURCE_EXHAUSTED, never INTERNAL
             or a wrong answer; pass/fail written here.
  lowdirect  4 full scans of the 12-file tpch.lineitem in a row on node 1 (check 5), exact.
"""
import base64
import decimal
import json
import os
import re
import sys
import time
import traceback

import adbc_driver_flightsql.dbapi as flightsql
import gssapi
import pyarrow.flight as flight

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import digest  # noqa: E402
import queries  # noqa: E402

SPNEGO = gssapi.OID.from_int_seq("1.3.6.1.5.5.2")
CA = open(os.environ["ACCEPT_CA"], "rb").read()


class _Capture(flight.ClientMiddlewareFactory):
    def __init__(self):
        self.auth = None

    def start_call(self, info):
        factory = self

        class M(flight.ClientMiddleware):
            def received_headers(self, headers):
                for k, v in headers.items():
                    if k.lower() == "authorization":
                        val = v[0] if isinstance(v, list) else v
                        factory.auth = val.decode() if isinstance(val, bytes) else val
        return M()


def bearer(server):
    """Kerberos login against one server: returns its signed bearer header value."""
    host = server.split(":")[0]
    ctx = gssapi.SecurityContext(name=gssapi.Name(f"flight@{host}", gssapi.NameType.hostbased_service),
                                 mech=SPNEGO, usage="initiate")
    token = base64.b64encode(ctx.step()).decode()
    cap = _Capture()
    client = flight.FlightClient(f"grpc+tls://{server}", tls_root_certs=CA, middleware=[cap])
    opts = flight.FlightCallOptions(headers=[(b"authorization", f"Negotiate {token}".encode())], timeout=60)
    try:
        list(client.list_actions(options=opts))
    except flight.FlightError as e:
        if cap.auth is None:
            raise RuntimeError(f"Kerberos login refused by {server}: {e}") from e
    finally:
        client.close()
    if not cap.auth or not cap.auth.startswith("Bearer "):
        raise RuntimeError(f"no bearer session from {server} (got {cap.auth!r})")
    return cap.auth


def connect(server, mode="complete"):
    kwargs = {
        "adbc.flight.sql.client_option.tls_root_certs": CA.decode(),
        "adbc.flight.sql.authorization_header": bearer(server),
        "adbc.flight.sql.rpc.timeout_seconds.query": "900",
        "adbc.flight.sql.rpc.timeout_seconds.fetch": "900",
    }
    if mode != "complete":
        kwargs["adbc.flight.sql.rpc.call_header.x-flight-result-mode"] = mode
    return flightsql.connect(f"grpc+tls://{server}", db_kwargs=kwargs)


def run(conn, sql):
    with conn.cursor() as cur:
        cur.execute(sql)
        return cur.fetch_arrow_table()


def error_text(e):
    return f"{type(e).__name__}: {str(e).strip()}"[:400].replace("\n", " ")


GRPC_CODES = ["Canceled", "Cancelled", "Unknown", "InvalidArgument", "DeadlineExceeded", "NotFound", "AlreadyExists",
              "PermissionDenied", "ResourceExhausted", "FailedPrecondition", "Aborted", "OutOfRange", "Unimplemented",
              "Internal", "Unavailable", "DataLoss", "Unauthenticated", "RESOURCE_EXHAUSTED", "INVALID_ARGUMENT",
              "DEADLINE_EXCEEDED", "NOT_FOUND", "PERMISSION_DENIED", "FAILED_PRECONDITION", "UNAUTHENTICATED"]


def grpc_status(e):
    """The gRPC status of a failed call, read from the FULL error text, not the driver's prefix: the ADBC driver
    prints a wire RESOURCE_EXHAUSTED as `INTERNAL: ... (ResourceExhausted; DoGet: ...)` past the 400 chars kept."""
    full = str(e)
    codes = "|".join(GRPC_CODES)
    for pat in (rf"\(({codes}); ", rf"code = ({codes})\b", rf"\b({codes}):"):
        m = re.findall(pat, full, re.IGNORECASE)
        if m:
            return m[-1].replace("_", "").lower()
    return type(e).__name__.lower()


def answer(conn, q, log):
    t0 = time.time()
    try:
        d = digest.digest(run(conn, q.sql), q.ordered)
        log(f"ok   {q.id} rows={d['rows']} {time.time() - t0:.1f}s")
        return d
    except Exception as e:  # noqa: BLE001 - recorded per query
        log(f"err  {q.id} {time.time() - t0:.1f}s {error_text(e)}")
        return {"error": error_text(e)}


def additive(table, key_cols):
    """Sums every non-key column per key (partial parts -> one answer)."""
    acc = {}
    for row in table.to_pylist():
        k = tuple(row[c] for c in key_cols)
        cur = acc.setdefault(k, {})
        for c, v in row.items():
            if c in key_cols:
                continue
            v = decimal.Decimal(str(v)) if v is not None else decimal.Decimal(0)
            cur[c] = cur.get(c, decimal.Decimal(0)) + v
    return acc


def close(a, b):
    for k in set(a) | set(b):
        x, y = a.get(k), b.get(k)
        if x is None or y is None:
            return False
        for c in set(x) | set(y):
            u, v = x.get(c, 0), y.get(c, 0)
            if abs(u - v) > max(decimal.Decimal("0.01"), abs(v) * decimal.Decimal("1e-9")):
                return False
    return True


def main(stage, servers, base, out):
    nodes = servers.split(",")
    res = {"stage": stage, "answers": {}, "checks": {}, "log": []}

    def log(s):
        print(s, flush=True)
        res["log"].append(s)

    def save():
        with open(out, "w") as f:
            json.dump(res, f, indent=1)

    def connect_or_fail(node, mode="complete"):
        try:
            return connect(node, mode)
        except Exception as e:  # noqa: BLE001
            log(f"err  connect {node} {mode}: {error_text(e)}")
            res["checks"].setdefault("connect", []).append(f"{node} {mode}: {error_text(e)}")
            return None

    if stage == "main":
        for i, node in enumerate(nodes, 1):
            qs = queries.tpch("tpch-plain") + queries.spread() + queries.far()
            if i == 1:
                qs += queries.tpch("tpch-schema") + queries.scans()
            conn = connect_or_fail(node)
            for q in qs:
                if conn is None:
                    res["answers"][f"{q.id}@n{i}"] = {"error": "no connection: " + res["checks"]["connect"][-1]}
                    continue
                res["answers"][f"{q.id}@n{i}"] = answer(conn, q, log)
                save()
            if conn is not None:
                conn.close()
    elif stage in ("partial", "smalldisk"):
        complete = {}
        if stage == "partial":
            plan = [(q, "partial") for q in queries.partial()]
        else:
            sd = [q for q in queries.partial() if "_sp" in q.sql or "-sp" in q.id]
            sd += [q for q in queries.spread() if q.id in ("sp-group", "sp-having", "sp-distinct", "sp-orders-group")]
            sd += [q for q in queries.scans() if q.id == "scan-lineitem-sp"]
            plan = [(q, "complete") for q in sd] + [(q, "partial") for q in queries.partial() if "-sp" in q.id]
            plan.append((next(q for q in queries.spread() if q.id == "sp-join-lineitem"), "complete"))
        expected = json.load(open(os.path.join(base, "expected.json")))
        fails = []
        for i, node in enumerate(nodes, 1):
            conns = {}
            for q, mode in plan:
                key = f"{q.id}@n{i}@{mode}"
                if mode not in conns:
                    conns[mode] = connect_or_fail(node, mode)
                conn = conns[mode]
                if conn is None:
                    fails.append(f"{key}: no connection")
                    continue
                t0 = time.time()
                try:
                    tab = run(conn, q.sql)
                except Exception as e:  # noqa: BLE001
                    txt, status = error_text(e), grpc_status(e)
                    if status == "resourceexhausted" and "resourceexhausted" not in txt.lower().replace("_", ""):
                        txt = "[gRPC ResourceExhausted] " + txt
                    log(f"err  {key} {time.time() - t0:.1f}s {txt}")
                    res["answers"][key] = {"error": txt}
                    # the join may be refused with RESOURCE_EXHAUSTED (gRPC code, also as "ResourceExhausted" inside the
                    # driver's wrapper of a failed DoGet); a server-side INTERNAL refusal is not allowed
                    if stage == "smalldisk" and q.id == "sp-join-lineitem" and status == "resourceexhausted":
                        log(f"ok   {key} refused with RESOURCE_EXHAUSTED (allowed)")
                        res["answers"][key]["refused"] = True
                    else:
                        fails.append(f"{key}: {txt}")
                    save()
                    continue
                if mode == "partial":
                    keys = [c for c in tab.column_names if not c.startswith(("n", "q", "t"))]
                    parts = additive(tab, keys)
                    if q.id not in complete:
                        cconn = conns.get("complete") or connect_or_fail(node)
                        conns["complete"] = cconn
                        complete[q.id] = additive(run(cconn, q.sql), keys) if cconn else {}
                    ok = close(parts, complete[q.id])
                    d = digest.digest(tab, False)
                    d["parts"] = tab.num_rows
                    res["answers"][key] = d
                    log(f"{'ok  ' if ok else 'FAIL'} {key} parts={tab.num_rows} summed {'=' if ok else '!='} complete {time.time() - t0:.1f}s")
                    if not ok:
                        fails.append(f"{key}: per-node parts summed {dict(list(parts.items())[:2])} != complete {dict(list(complete[q.id].items())[:2])}")
                else:
                    d = digest.digest(tab, q.ordered)
                    res["answers"][key] = d
                    ok = digest.same(d, expected[q.id])
                    log(f"{'ok  ' if ok else 'FAIL'} {key} rows={d['rows']} {time.time() - t0:.1f}s")
                    if not ok:
                        fails.append(f"{key}: rows {d['rows']} hash {d['hash']} != expected rows {expected[q.id]['rows']} hash {expected[q.id]['hash']}")
                save()
            for c in conns.values():
                if c is not None:
                    c.close()
        res["checks"][stage] = {"status": "fail" if fails else "pass", "detail": "; ".join(fails)[:1500]}
    elif stage == "lowdirect":
        expected = json.load(open(os.path.join(base, "expected.json")))
        q = next(q for q in queries.scans() if q.id == "scan-lineitem")
        fails = []
        conn = connect_or_fail(nodes[0])
        for r in range(1, 5):
            key = f"{q.id}@n1@r{r}"
            d = answer(conn, q, log) if conn else {"error": "no connection"}
            res["answers"][key] = d
            if "error" in d or not digest.same(d, expected[q.id]):
                fails.append(f"{key}: {d.get('error') or 'rows %s != %s' % (d['rows'], expected[q.id]['rows'])}")
            save()
        res["checks"][stage] = {"status": "fail" if fails else "pass", "detail": "; ".join(fails)[:1500]}
    else:
        raise SystemExit(f"unknown stage {stage}")
    save()


if __name__ == "__main__":
    try:
        main(*sys.argv[1:5])
    except Exception:  # noqa: BLE001
        traceback.print_exc()
        sys.exit(2)
