# Server comparison - Report 3: ROBUSTNESS (compare run 40849719732)

Same runner type and containers as Reports 1 and 2 (server: `eclipse-temurin:21-jre`, 2 CPUs on cpus 0,1, 6 GB, `-Xmx3g -XX:MaxDirectMemorySize=2g`; clients on cpus 2,3). Servers: ours-new = `7562a5bdb7b9`; ours-27f5 = `27f583adccd7`; up-native = `1de5f6b4b218f83f01a3adf2708af5f36f80811b`; up-main = `dbacd8d585bce2ef2a449c821fe3a53cc6060b57`.

## 3-node cluster: i18-dc-off-vs-on (s3)

Side A = b3bbcce19996 `-DdistributedComplete=false`, rounds with data: 2

| check | wall s median | per round wall s | correct / queries per round | failed |
|---|---|---|---|---|
| all-up | 369.0 | r1=296.9 r2=441.1 | 22/22 22/22 | - |
| node3-stopped | 379.5 | r1=298.4 r2=460.7 | 22/22 22/22 | - |
| node3-back | 382.8 | r1=298.9 r2=466.6 | 22/22 22/22 | - |
| node2-dead | 386.9 | r1=297.5 r2=476.2 | 22/22 22/22 | - |
| node2-back | 349.6 | r1=297.4 r2=401.9 | 22/22 22/22 | - |

- r1: cluster start: all 3 nodes started in 21.9s
- r1: cluster stop-node3: docker stop took 0.8s
- r1: cluster rejoin-node3 (new container): 5.4s
- r1: cluster kill-node2-mid-query: q18=ok q21=ok  
- r1: cluster recover-after-kill: first correct q06 through node 1 after 58.7s, attempts=1
- r1: cluster restart-node2: 6.3s
- r2: cluster start: all 3 nodes started in 20.4s
- r2: cluster stop-node3: docker stop took 0.9s
- r2: cluster rejoin-node3 (new container): 6.5s
- r2: cluster kill-node2-mid-query: q18=ok q21=ok  
- r2: cluster recover-after-kill: first correct q06 through node 1 after 93.1s, attempts=1
- r2: cluster restart-node2: 5.6s

Side B = b3bbcce19996 `-DdistributedComplete=true`, rounds with data: 2

| check | wall s median | per round wall s | correct / queries per round | failed |
|---|---|---|---|---|
| all-up | 384.5 | r1=308.9 r2=460.1 | 22/22 22/22 | - |
| node3-stopped | 465.5 | r1=436.9 r2=494.1 | 22/22 22/22 | - |
| node3-back | 482.6 | r1=482.0 r2=483.2 | 22/22 22/22 | - |
| node2-dead | 484.9 | r1=494.3 r2=475.4 | 22/22 22/22 | - |
| node2-back | 478.6 | r1=475.9 r2=481.4 | 22/22 22/22 | - |

- r1: cluster start: all 3 nodes started in 19.1s
- r1: cluster stop-node3: docker stop took 1.1s
- r1: cluster rejoin-node3 (new container): 5.6s
- r1: cluster kill-node2-mid-query: q18=ok q21=ok  
- r1: cluster recover-after-kill: first correct q06 through node 1 after 91.4s, attempts=1
- r1: cluster restart-node2: 5.6s
- r2: cluster start: all 3 nodes started in 19.6s
- r2: cluster stop-node3: docker stop took 1.1s
- r2: cluster rejoin-node3 (new container): 5.6s
- r2: cluster kill-node2-mid-query: q18=ok q21=ok  
- r2: cluster recover-after-kill: first correct q06 through node 1 after 103.8s, attempts=1
- r2: cluster restart-node2: 5.6s

