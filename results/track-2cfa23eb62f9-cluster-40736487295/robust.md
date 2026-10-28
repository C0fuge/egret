# Server comparison - Report 3: ROBUSTNESS (compare run 40736487295)

Same runner type and containers as Reports 1 and 2 (server: `eclipse-temurin:21-jre`, 2 CPUs on cpus 0,1, 6 GB, `-Xmx3g -XX:MaxDirectMemorySize=2g`; clients on cpus 2,3). Servers: ours-new = `7562a5bdb7b9`; ours-27f5 = `27f583adccd7`; up-native = `1de5f6b4b218f83f01a3adf2708af5f36f80811b`; up-main = `dbacd8d585bce2ef2a449c821fe3a53cc6060b57`.

## 3-node cluster: i18-dc-off-vs-on (s3)

Side A = 2cfa23eb62f9 `-DdistributedComplete=false`, rounds with data: 2

| check | wall s median | per round wall s | correct / queries per round | failed |
|---|---|---|---|---|
| all-up | 405.5 | r1=328.7 r2=482.4 | 22/22 22/22 | - |
| node3-stopped | 426.0 | r1=328.8 r2=523.1 | 22/22 22/22 | - |
| node3-back | 421.4 | r1=329.8 r2=512.9 | 22/22 22/22 | - |
| node2-dead | 429.5 | r1=326.7 r2=532.3 | 22/22 22/22 | - |
| node2-back | 423.4 | r1=326.6 r2=520.1 | 22/22 22/22 | - |

- r1: cluster start: all 3 nodes started in 20.1s
- r1: cluster stop-node3: docker stop took 1.1s
- r1: cluster rejoin-node3 (new container): 5.8s
- r1: cluster kill-node2-mid-query: q18=ok q21=ok  
- r1: cluster recover-after-kill: first correct q06 through node 1 after 61.8s, attempts=1
- r1: cluster restart-node2: 5.6s
- r2: cluster start: all 3 nodes started in 25.3s
- r2: cluster stop-node3: docker stop took 0.8s
- r2: cluster rejoin-node3 (new container): 5.1s
- r2: cluster kill-node2-mid-query: q18=ok q21=ok  
- r2: cluster recover-after-kill: first correct q06 through node 1 after 98.4s, attempts=1
- r2: cluster restart-node2: 5.1s

Side B = 2cfa23eb62f9 `-DdistributedComplete=true`, rounds with data: 2

| check | wall s median | per round wall s | correct / queries per round | failed |
|---|---|---|---|---|
| all-up | 456.5 | r1=408.0 r2=505.0 | 22/22 22/22 | - |
| node3-stopped | 545.5 | r1=548.1 r2=543.0 | 22/22 22/22 | - |
| node3-back | 529.2 | r1=525.4 r2=533.0 | 22/22 22/22 | - |
| node2-dead | 545.1 | r1=545.8 r2=544.4 | 22/22 22/22 | - |
| node2-back | 526.2 | r1=517.3 r2=535.2 | 22/22 22/22 | - |

- r1: cluster start: all 3 nodes started in 20.7s
- r1: cluster stop-node3: docker stop took 1.1s
- r1: cluster rejoin-node3 (new container): 5.3s
- r1: cluster kill-node2-mid-query: q18=ok q21=ok  
- r1: cluster recover-after-kill: first correct q06 through node 1 after 109.0s, attempts=1
- r1: cluster restart-node2: 5.4s
- r2: cluster start: all 3 nodes started in 19.3s
- r2: cluster stop-node3: docker stop took 1.0s
- r2: cluster rejoin-node3 (new container): 5.4s
- r2: cluster kill-node2-mid-query: q18=ok q21=ok  
- r2: cluster recover-after-kill: first correct q06 through node 1 after 104.0s, attempts=1
- r2: cluster restart-node2: 5.4s

