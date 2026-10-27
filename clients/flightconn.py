# Shared ADBC connection options: bearer token and TLS root CA from the environment (FLIGHT_TOKEN, FLIGHT_CA = PEM file);
# without them the plain insecure connection with a dummy token, as before. FLIGHT_COMPRESSION (zstd | lz4 | none) is sent
# as the call header arrow-compression on every call (client-requested result stream compression, kestrel item 20).
import os

import adbc_driver_flightsql as a


def db_kwargs():
    kw = {a.DatabaseOptions.AUTHORIZATION_HEADER.value: "Bearer " + (os.environ.get("FLIGHT_TOKEN") or "unused")}
    ca = os.environ.get("FLIGHT_CA")
    if ca:
        with open(ca) as f:
            kw[a.DatabaseOptions.TLS_ROOT_CERTS.value] = f.read()
    comp = os.environ.get("FLIGHT_COMPRESSION")
    if comp:
        kw[a.DatabaseOptions.RPC_CALL_HEADER_PREFIX.value + "arrow-compression"] = comp
    return kw
