"""cancel.py <uri> <query.sql> <cancel_after_s>: run one query through Python ADBC Flight SQL and cancel it from another thread.
Prints: cancel query=<name> sent=<epoch s> returned=<epoch s> return_s=<s after cancel> outcome=<cancelled|finished|error> detail=<text>.
The server side (CPU of the server process dropping after `sent`) is measured by ab.sh."""
import os
import sys
import threading
import time

import adbc_driver_flightsql as a
import adbc_driver_flightsql.dbapi as d

uri, qf, after = sys.argv[1], sys.argv[2], float(sys.argv[3])
sql = open(qf).read().strip().rstrip(";")
con = d.connect(uri, db_kwargs={a.DatabaseOptions.AUTHORIZATION_HEADER.value: "Bearer unused"})
cur = con.cursor()
res = {}


def run():
    try:
        cur.execute(sql)
        cur.fetch_arrow_table()
        res["outcome"], res["detail"] = "finished", ""
    except Exception as e:
        txt = str(e).splitlines()[0][:150] if str(e) else type(e).__name__
        res["outcome"] = "cancelled" if "cancel" in txt.lower() else "error"
        res["detail"] = f"{type(e).__name__}: {txt}"
    res["returned"] = time.time()


t = threading.Thread(target=run)
t.start()
t.join(after)
sent = None
if t.is_alive():
    sent = time.time()
    try:
        cur.adbc_cancel()
    except Exception as e:
        res["cancel_error"] = f"{type(e).__name__}: {str(e)[:100]}"
t.join(600)
ret = res.get("returned")
print(f"cancel query={os.path.basename(qf)[:-4]} sent={sent if sent else 'none'} returned={ret} "
      f"return_s={(ret - sent) if sent and ret else 'n/a'} outcome={res.get('outcome', 'hung')} "
      f"detail={res.get('detail', '')} {res.get('cancel_error', '')}".rstrip())
try:
    con.close()
except Exception:
    pass
