# Shared ADBC connection options: bearer token and TLS root CA from the environment (FLIGHT_TOKEN, FLIGHT_CA = PEM file);
# without them the plain insecure connection with a dummy token, as before. FLIGHT_COMPRESSION (zstd | lz4 | none) is sent
# as the call header arrow-compression on every call (client-requested result stream compression, kestrel item 20).
# FLIGHT_USER / FLIGHT_PASSWORD (servers that require a login, e.g. GizmoSQL): ADBC username/password handshake instead
# of the bearer header (the driver then sends the token the server returns).
import os

import adbc_driver_flightsql as a


def db_kwargs():
    if os.environ.get("FLIGHT_USER"):
        kw = {"username": os.environ["FLIGHT_USER"], "password": os.environ.get("FLIGHT_PASSWORD", "")}
    else:
        kw = {a.DatabaseOptions.AUTHORIZATION_HEADER.value: "Bearer " + (os.environ.get("FLIGHT_TOKEN") or "unused")}
    ca = os.environ.get("FLIGHT_CA")
    if ca:
        with open(ca) as f:
            kw[a.DatabaseOptions.TLS_ROOT_CERTS.value] = f.read()
    comp = os.environ.get("FLIGHT_COMPRESSION")
    if comp:
        kw[a.DatabaseOptions.RPC_CALL_HEADER_PREFIX.value + "arrow-compression"] = comp
    return kw
