# Server comparison - Report 3: ROBUSTNESS (compare run 40772225000)

Same runner type and containers as Reports 1 and 2 (server: `eclipse-temurin:21-jre`, 2 CPUs on cpus 0,1, 6 GB, `-Xmx3g -XX:MaxDirectMemorySize=2g`; clients on cpus 2,3). Servers: ours-new = `7562a5bdb7b9`; ours-27f5 = `27f583adccd7`; up-native = `1de5f6b4b218f83f01a3adf2708af5f36f80811b`; up-main = `dbacd8d585bce2ef2a449c821fe3a53cc6060b57`.

## 3-node cluster: i18-dc-off-vs-on (s3)

Side A = 9044653333cd `-DdistributedComplete=false`, rounds with data: 2

| check | wall s median | per round wall s | correct / queries per round | failed |
|---|---|---|---|---|
| all-up | 360.5 | r1=291.0 r2=430.0 | 22/22 22/22 | - |
| node3-stopped | 368.3 | r1=286.0 r2=450.6 | 22/22 22/22 | - |
| node3-back | 368.1 | r1=281.3 r2=455.0 | 22/22 22/22 | - |
| node2-dead | 376.8 | r1=291.0 r2=462.6 | 22/22 22/22 | - |
| node2-back | 373.8 | r1=295.3 r2=452.3 | 22/22 22/22 | - |

- r1: cluster start: all 3 nodes started in 23.5s
- r1: cluster stop-node3: docker stop took 1.1s
- r1: cluster rejoin-node3 (new container): 5.9s
- r1: cluster kill-node2-mid-query: q18=ok q21=ok  
- r1: cluster recover-after-kill: first correct q06 through node 1 after 65.1s, attempts=1
- r1: cluster restart-node2: 5.8s
- r2: cluster start: all 3 nodes started in 22.8s
- r2: cluster stop-node3: docker stop took 1.0s
- r2: cluster rejoin-node3 (new container): 5.9s
- r2: cluster kill-node2-mid-query: q18=ok q21=ok  
- r2: cluster recover-after-kill: first correct q06 through node 1 after 89.4s, attempts=1
- r2: cluster restart-node2: 5.6s

Side B = 9044653333cd `-DdistributedComplete=true`, rounds with data: 2

| check | wall s median | per round wall s | correct / queries per round | failed |
|---|---|---|---|---|
| all-up | 371.8 | r1=298.2 r2=445.3 | 22/22 22/22 | - |
| node3-stopped | 430.9 | r1=398.9 r2=463.0 | 22/22 22/22 | - |
| node3-back | 469.7 | r1=466.7 r2=472.7 | 22/22 22/22 | - |
| node2-dead | 463.9 | r1=459.9 r2=468.0 | 22/22 22/22 | - |
| node2-back | 462.2 | r1=463.9 r2=460.6 | 22/22 22/22 | - |

- r1: cluster start: all 3 nodes started in 21.4s
- r1: cluster stop-node3: docker stop took 1.0s
- r1: cluster rejoin-node3 (new container): 5.9s
- r1: cluster kill-node2-mid-query: q18=ok q21=ok  
- r1: cluster recover-after-kill: first correct q06 through node 1 after 96.0s, attempts=1
- r1: cluster restart-node2: 5.9s
- r2: cluster start: all 3 nodes started in 21.2s
- r2: cluster stop-node3: docker stop took 1.0s
- r2: cluster rejoin-node3 (new container): 6.8s
- r2: cluster kill-node2-mid-query: q18=ok q21=ok  
- r2: cluster recover-after-kill: first correct q06 through node 1 after 89.7s, attempts=1
- r2: cluster restart-node2: 5.6s

