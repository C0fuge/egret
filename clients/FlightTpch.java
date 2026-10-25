import java.math.BigDecimal;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.MessageDigest;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HexFormat;
import java.util.List;
import java.util.Locale;
import java.util.Properties;
import java.util.stream.Stream;

/**
 * TPC-H (or any *.sql set) runner for Trino over JDBC.
 *
 *   java -cp trino-jdbc.jar TpchBench.java <jdbc-url> <queries-dir> <reps> <out-dir> [session k=v ...]
 *   e.g. jdbc:trino://localhost:8080/flight/tpch?user=bench
 *
 * Per query: runs it <reps> times (first run reported separately as "cold"), records wall time,
 * row count and a checksum of the result (rows normalised and sorted), and writes the result rows
 * to <out-dir>/<query>.tsv so two runs (e.g. with/without a pushdown) can be diffed.
 * Writes <out-dir>/summary.tsv: query, status, rows, checksum, cold_s, min_s, median_s.
 */
public class FlightTpch {
    public static void main(String[] args) throws Exception {
        if (args.length < 4) {
            System.err.println("usage: TpchBench <jdbc-url> <queries-dir> <reps> <out-dir> [session k=v ...]");
            System.exit(2);
        }
        String url = args[0];
        Path queriesDir = Path.of(args[1]);
        int reps = Integer.parseInt(args[2]);
        Path out = Files.createDirectories(Path.of(args[3]));
        List<String> session = List.of(args).subList(4, args.length);

        List<Path> queries;
        try (Stream<Path> s = Files.list(queriesDir)) {
            queries = s.filter(p -> p.toString().endsWith(".sql")).sorted().toList();
        }

        Properties props = new Properties();
        if (false) {
            props.setProperty("user", "bench");
        }
        List<String> summary = new ArrayList<>();
        summary.add("query\tstatus\trows\tchecksum\tcold_s\tmin_s\tmedian_s");
        System.out.printf("%-6s %-6s %10s %-12s %8s %8s %8s%n", "query", "status", "rows", "checksum", "cold_s", "min_s", "median_s");

        try (Connection conn = DriverManager.getConnection(url, props)) {
            try (Statement st = conn.createStatement()) {
                for (String kv : session) {
                    int eq = kv.indexOf('=');
                    st.execute("SET SESSION " + kv.substring(0, eq) + " = " + kv.substring(eq + 1));
                }
            }
            for (Path q : queries) {
                String name = q.getFileName().toString().replace(".sql", "");
                String sql = Files.readString(q).trim();
                if (sql.endsWith(";")) {
                    sql = sql.substring(0, sql.length() - 1);
                }
                List<Double> times = new ArrayList<>();
                List<String> rows = null;
                String status = "ok";
                for (int i = 0; i < reps; i++) {
                    long t0 = System.nanoTime();
                    try (Statement st = conn.createStatement(); ResultSet rs = st.executeQuery(sql)) {
                        List<String> r = readAll(rs);
                        times.add((System.nanoTime() - t0) / 1e9);
                        if (rows == null) {
                            rows = r;
                        }
                    }
                    catch (Exception e) {
                        status = "FAIL";
                        String msg = e.getMessage() == null ? e.toString() : e.getMessage();
                        java.io.StringWriter trace = new java.io.StringWriter();
                        e.printStackTrace(new java.io.PrintWriter(trace, true));
                        Files.writeString(out.resolve(name + ".error"), "repetition " + (i + 1) + " of " + reps + "\n" + msg + "\n\n" + trace);
                        System.out.printf("%-6s FAIL   %s%n", name, msg.lines().findFirst().orElse(""));
                        break;
                    }
                }
                if (status.equals("ok")) {
                    List<String> sorted = new ArrayList<>(rows);
                    Collections.sort(sorted);
                    String checksum = HexFormat.of().formatHex(
                            MessageDigest.getInstance("SHA-256").digest(String.join("\n", sorted).getBytes(StandardCharsets.UTF_8)))
                            .substring(0, 12);
                    Files.write(out.resolve(name + ".tsv"), rows);
                    double cold = times.get(0);
                    List<Double> warm = times.size() > 1 ? new ArrayList<>(times.subList(1, times.size())) : new ArrayList<>(times);
                    Collections.sort(warm);
                    double min = warm.get(0);
                    double median = warm.get(warm.size() / 2);
                    System.out.printf(Locale.ROOT, "%-6s %-6s %10d %-12s %8.2f %8.2f %8.2f%n", name, status, rows.size(), checksum, cold, min, median);
                    summary.add(String.format(Locale.ROOT, "%s\t%s\t%d\t%s\t%.3f\t%.3f\t%.3f", name, status, rows.size(), checksum, cold, min, median));
                }
                else {
                    summary.add(name + "\tFAIL\t\t\t\t\t");
                }
            }
        }
        Files.write(out.resolve("summary.tsv"), summary);
    }

    private static List<String> readAll(ResultSet rs) throws Exception {
        ResultSetMetaData md = rs.getMetaData();
        int n = md.getColumnCount();
        List<String> rows = new ArrayList<>();
        while (rs.next()) {
            StringBuilder sb = new StringBuilder();
            for (int i = 1; i <= n; i++) {
                if (i > 1) {
                    sb.append('\t');
                }
                Object v = rs.getObject(i);
                sb.append(normalize(v));
            }
            rows.add(sb.toString());
        }
        return rows;
    }

    /** Doubles rounded to 10 significant digits so summation order does not change checksums. */
    private static String normalize(Object v) {
        if (v == null) {
            return "NULL";
        }
        if (v instanceof Double d) {
            return new BigDecimal(d).round(new java.math.MathContext(10)).stripTrailingZeros().toPlainString();
        }
        if (v instanceof Float f) {
            return new BigDecimal(f).round(new java.math.MathContext(6)).stripTrailingZeros().toPlainString();
        }
        if (v instanceof BigDecimal b) {
            return b.stripTrailingZeros().toPlainString();
        }
        return v.toString();
    }
}
