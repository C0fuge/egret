# Shared ADBC connection options: bearer token and TLS root CA from the environment (FLIGHT_TOKEN, FLIGHT_CA = PEM file);
# without them the plain insecure connection with a dummy token, as before.
import os

import adbc_driver_flightsql as a


def db_kwargs():
    kw = {a.DatabaseOptions.AUTHORIZATION_HEADER.value: "Bearer " + (os.environ.get("FLIGHT_TOKEN") or "unused")}
    ca = os.environ.get("FLIGHT_CA")
    if ca:
        with open(ca) as f:
            kw[a.DatabaseOptions.TLS_ROOT_CERTS.value] = f.read()
    return kw
