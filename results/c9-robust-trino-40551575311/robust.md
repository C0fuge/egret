# Server comparison - Report 3: ROBUSTNESS (compare run 40551575311)

Same runner type and containers as Reports 1 and 2 (server: `eclipse-temurin:21-jre`, 2 CPUs on cpus 0,1, 6 GB, `-Xmx3g -XX:MaxDirectMemorySize=2g`; clients on cpus 2,3). Servers: ours-new = `7562a5bdb7b9`; ours-27f5 = `27f583adccd7`; up-native = `202b4cef8a395c5ab62456e75fcc027f6f998683`; up-main = `dbacd8d585bce2ef2a449c821fe3a53cc6060b57`.

Not in this run (ours only, next session): 3-node cluster on one runner (node stopped before / killed during a query),
Trino SF1 through our plugin, stock Flight SQL JDBC driver TPC-H SF1 (see Report 1 JDBC tables: upstream fails there).

