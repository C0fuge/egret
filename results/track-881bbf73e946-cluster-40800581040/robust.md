# Server comparison - Report 3: ROBUSTNESS (compare run 40800581040)

Same runner type and containers as Reports 1 and 2 (server: `eclipse-temurin:21-jre`, 2 CPUs on cpus 0,1, 6 GB, `-Xmx3g -XX:MaxDirectMemorySize=2g`; clients on cpus 2,3). Servers: ours-new = `7562a5bdb7b9`; ours-27f5 = `27f583adccd7`; up-native = `1de5f6b4b218f83f01a3adf2708af5f36f80811b`; up-main = `dbacd8d585bce2ef2a449c821fe3a53cc6060b57`.

## 3-node cluster: i18-dc-off-vs-on (s3)

Side A = 881bbf73e946 `-DdistributedComplete=false`, rounds with data: 2

| check | wall s median | per round wall s | correct / queries per round | failed |
|---|---|---|---|---|
| all-up | 376.1 | r1=302.0 r2=450.1 | 22/22 22/22 | - |
| node3-stopped | 386.3 | r1=300.6 r2=472.0 | 22/22 22/22 | - |
| node3-back | 389.0 | r1=303.0 r2=475.0 | 22/22 22/22 | - |
| node2-dead | 391.9 | r1=305.0 r2=478.9 | 22/22 22/22 | - |
| node2-back | 386.8 | r1=296.9 r2=476.6 | 22/22 22/22 | - |

- r1: cluster start: all 3 nodes started in 20.9s
- r1: cluster stop-node3: docker stop took 0.8s
- r1: cluster rejoin-node3 (new container): 5.8s
- r1: cluster kill-node2-mid-query: q18=ok q21=ok  
- r1: cluster recover-after-kill: first correct q06 through node 1 after 59.8s, attempts=1
- r1: cluster restart-node2: 6.5s
- r2: cluster start: all 3 nodes started in 19.9s
- r2: cluster stop-node3: docker stop took 0.9s
- r2: cluster rejoin-node3 (new container): 6.1s
- r2: cluster kill-node2-mid-query: q18=ok q21=ok  
- r2: cluster recover-after-kill: first correct q06 through node 1 after 95.0s, attempts=1
- r2: cluster restart-node2: 5.6s

Side B = 881bbf73e946 `-DdistributedComplete=true`, rounds with data: 2

| check | wall s median | per round wall s | correct / queries per round | failed |
|---|---|---|---|---|
| all-up | 380.1 | r1=305.9 r2=454.3 | 22/22 22/22 | - |
| node3-stopped | 473.4 | r1=450.9 r2=496.0 | 22/22 22/22 | - |
| node3-back | 482.5 | r1=483.7 r2=481.4 | 22/22 22/22 | - |
| node2-dead | 486.8 | r1=494.6 r2=479.0 | 22/22 22/22 | - |
| node2-back | 483.0 | r1=482.7 r2=483.3 | 22/22 22/22 | - |

- r1: cluster start: all 3 nodes started in 21.4s
- r1: cluster stop-node3: docker stop took 1.0s
- r1: cluster rejoin-node3 (new container): 5.7s
- r1: cluster kill-node2-mid-query: q18=ok q21=ok  
- r1: cluster recover-after-kill: first correct q06 through node 1 after 96.0s, attempts=1
- r1: cluster restart-node2: 6.0s
- r2: cluster start: all 3 nodes started in 19.5s
- r2: cluster stop-node3: docker stop took 0.8s
- r2: cluster rejoin-node3 (new container): 5.6s
- r2: cluster kill-node2-mid-query: q18=ok q21=ok  
- r2: cluster recover-after-kill: first correct q06 through node 1 after 96.3s, attempts=1
- r2: cluster restart-node2: 5.3s

