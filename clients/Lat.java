import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.Path;
import java.sql.Connection;
import java.sql.DatabaseMetaData;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Locale;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * Small-query latency load generator over the Flight SQL JDBC driver.
 *
 *   java -cp flight-sql-jdbc.jar Lat.java <url> <conc> <rounds> <out.csv> [fetchSize]
 *
 * Each of <conc> threads opens its own connection, runs one warm-up round, then <rounds> rounds of the 7 query
 * classes (metadata tables/schemas, point orders/lineitem, LIMIT 10, filtered count, prepared point query reused).
 * Keys are deterministic per (thread, round), so the row/value sums per class are comparable between server variants.
 * CSV: client,conc,class,thread,round,lat_ms,rows,val,ok
 */
public class Lat {
    static final String[] CLASSES = {"meta_tables", "meta_schemas", "point_orders", "point_lineitem", "limit10", "count_filter", "prep_point"};

    static long orderKey(long seed) {
        long r = 1 + Math.floorMod(seed * 2654435761L + 12345L, 14_999_999L);
        return (r / 8) * 32 + (r % 8);
    }

    static String day(long seed) {
        java.time.LocalDate d = java.time.LocalDate.of(1992, 1, 1).plusDays(Math.floorMod(seed * 40503L, 2400L));
        return d.toString();
    }

    public static void main(String[] a) throws Exception {
        String url = a[0];
        int conc = Integer.parseInt(a[1]);
        int rounds = Integer.parseInt(a[2]);
        Path out = Path.of(a[3]);
        int fetch = a.length > 4 ? Integer.parseInt(a[4]) : 0;
        List<String> lines = Collections.synchronizedList(new ArrayList<>());
        CountDownLatch ready = new CountDownLatch(conc);
        CountDownLatch go = new CountDownLatch(1);
        AtomicInteger errors = new AtomicInteger();
        List<Thread> ts = new ArrayList<>();
        long[] wall = new long[2];
        for (int t = 0; t < conc; t++) {
            final int tid = t;
            Thread th = new Thread(() -> {
                try (Connection c = DriverManager.getConnection(url)) {
                    PreparedStatement ps = c.prepareStatement("SELECT o_orderkey, o_totalprice FROM tpch.orders WHERE o_orderkey = ?");
                    round(c, ps, tid, -1, conc, fetch, null, errors); // warm-up
                    ready.countDown();
                    go.await();
                    for (int r = 0; r < rounds; r++) {
                        round(c, ps, tid, r, conc, fetch, lines, errors);
                    }
                    ps.close();
                } catch (Exception e) {
                    errors.incrementAndGet();
                    System.err.println("thread " + tid + ": " + e);
                    ready.countDown();
                }
            });
            ts.add(th);
            th.start();
        }
        ready.await();
        wall[0] = System.nanoTime();
        go.countDown();
        for (Thread th : ts) {
            th.join();
        }
        wall[1] = System.nanoTime();
        double secs = (wall[1] - wall[0]) / 1e9;
        try (PrintWriter w = new PrintWriter(Files.newBufferedWriter(out))) {
            w.println("client,conc,class,thread,round,lat_ms,rows,val,ok");
            for (String l : lines) {
                w.println(l);
            }
        }
        System.out.printf(Locale.ROOT, "jdbc conc=%d rounds=%d queries=%d wall=%.2fs qps=%.1f errors=%d%n", conc, rounds, lines.size(), secs,
                lines.size() / secs, errors.get());
        System.exit(0);
    }

    static void round(Connection c, PreparedStatement ps, int tid, int r, int conc, int fetch, List<String> lines, AtomicInteger errors) {
        long seed = tid * 100_003L + r + 7;
        for (int k = 0; k < CLASSES.length; k++) {
            String cls = CLASSES[(k + tid) % CLASSES.length];
            long t0 = System.nanoTime();
            long rows = 0;
            double val = 0;
            boolean ok = true;
            try {
                switch (cls) {
                    case "meta_tables" -> {
                        DatabaseMetaData md = c.getMetaData();
                        try (ResultSet rs = md.getTables(null, "tpch", "%", null)) {
                            while (rs.next()) {
                                rows++;
                            }
                        }
                    }
                    case "meta_schemas" -> {
                        try (ResultSet rs = c.getMetaData().getSchemas()) {
                            while (rs.next()) {
                                rows++;
                            }
                        }
                    }
                    case "prep_point" -> {
                        ps.setLong(1, orderKey(seed * 3 + 1));
                        try (ResultSet rs = ps.executeQuery()) {
                            while (rs.next()) {
                                rows++;
                                val += rs.getDouble(2);
                            }
                        }
                    }
                    default -> {
                        String sql = switch (cls) {
                            case "point_orders" -> "SELECT o_orderkey, o_custkey, o_totalprice, o_orderdate FROM tpch.orders WHERE o_orderkey = "
                                    + orderKey(seed * 3);
                            case "point_lineitem" -> "SELECT l_orderkey, l_linenumber, l_quantity, l_extendedprice FROM tpch.lineitem WHERE l_orderkey = "
                                    + orderKey(seed * 3 + 2);
                            case "limit10" -> "SELECT l_orderkey, l_partkey, l_quantity, l_comment FROM tpch.lineitem LIMIT 10";
                            default -> "SELECT count(*) FROM tpch.orders WHERE o_orderdate = DATE '" + day(seed) + "'";
                        };
                        try (Statement s = c.createStatement()) {
                            if (fetch > 0) {
                                s.setFetchSize(fetch);
                            }
                            try (ResultSet rs = s.executeQuery(sql)) {
                                int n = rs.getMetaData().getColumnCount();
                                while (rs.next()) {
                                    rows++;
                                    if (!cls.equals("limit10")) {
                                        val += rs.getDouble(n == 1 ? 1 : 3);
                                    }
                                }
                            }
                        }
                    }
                }
            } catch (Exception e) {
                ok = false;
                errors.incrementAndGet();
                System.err.println(cls + " t" + tid + " r" + r + ": " + e.toString().replace('\n', ' '));
            }
            double ms = (System.nanoTime() - t0) / 1e6;
            if (lines != null) {
                lines.add(String.format(Locale.ROOT, "jdbc,%d,%s,%d,%d,%.3f,%d,%.2f,%d", conc, cls, tid, r, ms, rows, val, ok ? 1 : 0));
            }
        }
    }
}
