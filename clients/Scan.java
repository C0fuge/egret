import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.atomic.AtomicLong;

import org.apache.arrow.flight.CallOption;
import org.apache.arrow.flight.CallHeaders;
import org.apache.arrow.flight.FlightCallHeaders;
import org.apache.arrow.flight.FlightClient;
import org.apache.arrow.flight.FlightEndpoint;
import org.apache.arrow.flight.FlightInfo;
import org.apache.arrow.flight.FlightStream;
import org.apache.arrow.flight.HeaderCallOption;
import org.apache.arrow.flight.Location;
import org.apache.arrow.flight.sql.FlightSqlClient;
import org.apache.arrow.memory.BufferAllocator;
import org.apache.arrow.memory.RootAllocator;
import org.apache.arrow.vector.FieldVector;
import org.apache.arrow.vector.VectorSchemaRoot;

/**
 * Concurrent full-scan throughput over raw Flight SQL (no JDBC row conversion).
 *
 *   java -cp server.jar Scan.java <host> <port> <conc> <reps> <mode partial|complete> <sql>
 *
 * Each rep starts <conc> scans of <sql> at once; every scan plans (GetFlightInfo), reads all endpoints at their first location
 * and counts rows and Arrow buffer bytes. Prints one line per rep: wall time, total rows, MB, rows/s, MB/s, errors.
 */
public class Scan {
    public static void main(String[] a) throws Exception {
        String host = a[0];
        int port = Integer.parseInt(a[1]);
        int conc = Integer.parseInt(a[2]);
        int reps = Integer.parseInt(a[3]);
        String mode = a[4];
        String sql = a[5];
        CallHeaders h = new FlightCallHeaders();
        h.insert("authorization", "Bearer unused");
        h.insert("x-flight-result-mode", mode);
        CallOption[] co = {new HeaderCallOption(h)};
        try (BufferAllocator root = new RootAllocator(Long.MAX_VALUE)) {
            for (int r = 0; r < reps; r++) {
                AtomicLong rows = new AtomicLong();
                AtomicLong bytes = new AtomicLong();
                AtomicLong errs = new AtomicLong();
                AtomicLong endpoints = new AtomicLong();
                List<Thread> ts = new ArrayList<>();
                long[] each = new long[conc];
                CountDownLatch go = new CountDownLatch(1);
                for (int t = 0; t < conc; t++) {
                    final int tid = t;
                    Thread th = new Thread(() -> {
                        try (BufferAllocator al = root.newChildAllocator("s" + tid, 0, Long.MAX_VALUE);
                             FlightClient c = FlightClient.builder(al, Location.forGrpcInsecure(host, port)).build()) {
                            FlightSqlClient q = new FlightSqlClient(c);
                            go.await();
                            long t0 = System.nanoTime();
                            FlightInfo info = q.execute(sql, co);
                            List<Thread> eps = new ArrayList<>();
                            for (FlightEndpoint ep : info.getEndpoints()) {
                                Thread et = new Thread(() -> {
                                    try {
                                        readEndpoint(al, c, host, port, ep, co, rows, bytes);
                                    } catch (Exception e) {
                                        errs.incrementAndGet();
                                        System.err.println("scan " + tid + " endpoint: " + e.toString().replace('\n', ' '));
                                    }
                                });
                                eps.add(et);
                                et.start();
                            }
                            for (Thread et : eps) {
                                et.join();
                            }
                            endpoints.set(info.getEndpoints().size());
                            each[tid] = System.nanoTime() - t0;
                        } catch (Exception e) {
                            errs.incrementAndGet();
                            System.err.println("scan " + tid + ": " + e.toString().replace('\n', ' '));
                        }
                    });
                    ts.add(th);
                    th.start();
                }
                long t0 = System.nanoTime();
                go.countDown();
                for (Thread th : ts) {
                    th.join();
                }
                double s = (System.nanoTime() - t0) / 1e9;
                double mb = bytes.get() / 1048576.0;
                double maxEach = 0;
                for (long e : each) {
                    maxEach = Math.max(maxEach, e / 1e9);
                }
                System.out.printf(Locale.ROOT, "scan conc=%d rep=%d wall=%.2f rows=%d mb=%.0f rows_per_s=%.0f mb_per_s=%.1f slowest=%.2f endpoints=%d errors=%d%n",
                        conc, r, s, rows.get(), mb, rows.get() / s, mb / s, maxEach, endpoints.get(), errs.get());
            }
        }
        System.exit(0);
    }

    static void readEndpoint(BufferAllocator al, FlightClient c, String host, int port, FlightEndpoint ep, CallOption[] co,
                             AtomicLong rows, AtomicLong bytes) throws Exception {
        FlightClient rc = c;
        FlightClient other = null;
        if (!ep.getLocations().isEmpty()) {
            Location loc = ep.getLocations().get(0);
            if (!(loc.getUri().getHost().equals(host) && loc.getUri().getPort() == port)) {
                other = FlightClient.builder(al, loc).build();
                rc = other;
            }
        }
        try (FlightStream s = rc.getStream(ep.getTicket(), co)) {
            VectorSchemaRoot vr = s.getRoot();
            while (s.next()) {
                rows.addAndGet(vr.getRowCount());
                long b = 0;
                for (FieldVector v : vr.getFieldVectors()) {
                    b += v.getBufferSize();
                }
                bytes.addAndGet(b);
            }
        } finally {
            if (other != null) {
                other.close();
            }
        }
    }
}
