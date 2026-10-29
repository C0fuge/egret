# Server comparison - Report 3: ROBUSTNESS (compare run 40823529991)

Same runner type and containers as Reports 1 and 2 (server: `eclipse-temurin:21-jre`, 2 CPUs on cpus 0,1, 6 GB, `-Xmx3g -XX:MaxDirectMemorySize=2g`; clients on cpus 2,3). Servers: ours-new = `7562a5bdb7b9`; ours-27f5 = `27f583adccd7`; up-native = `1de5f6b4b218f83f01a3adf2708af5f36f80811b`; up-main = `dbacd8d585bce2ef2a449c821fe3a53cc6060b57`.

## 3-node cluster: i18-dc-off-vs-on (s3)

Side A = 06833e736572 `-DdistributedComplete=false`, rounds with data: 2

| check | wall s median | per round wall s | correct / queries per round | failed |
|---|---|---|---|---|
| all-up | 389.7 | r1=320.0 r2=459.4 | 22/22 22/22 | - |
| node3-stopped | 320.8 | r1=314.2 r2=327.4 | 22/22 22/22 | - |
| node3-back | 318.2 | r1=317.9 r2=318.6 | 22/22 22/22 | - |
| node2-dead | 312.9 | r1=311.4 r2=314.4 | 22/22 22/22 | - |
| node2-back | 311.1 | r1=309.0 r2=313.3 | 22/22 22/22 | - |

- r1: cluster start: all 3 nodes started in 19.6s
- r1: cluster stop-node3: docker stop took 1.0s
- r1: cluster rejoin-node3 (new container): 5.9s
- r1: cluster kill-node2-mid-query: q18=ok q21=ok  
- r1: cluster recover-after-kill: first correct q06 through node 1 after 58.7s, attempts=1
- r1: cluster restart-node2: 5.6s
- r2: cluster start: all 3 nodes started in 21.0s
- r2: cluster stop-node3: docker stop took 0.9s
- r2: cluster rejoin-node3 (new container): 5.8s
- r2: cluster kill-node2-mid-query: q18=ok q21=ok  
- r2: cluster recover-after-kill: first correct q06 through node 1 after 58.6s, attempts=1
- r2: cluster restart-node2: 5.6s

Side B = 06833e736572 `-DdistributedComplete=true`, rounds with data: 2

| check | wall s median | per round wall s | correct / queries per round | failed |
|---|---|---|---|---|
| all-up | 414.4 | r1=350.5 r2=478.4 | 22/22 22/22 | - |
| node3-stopped | 503.6 | r1=505.4 r2=501.9 | 22/22 22/22 | - |
| node3-back | 488.8 | r1=488.7 r2=488.8 | 22/22 22/22 | - |
| node2-dead | 504.6 | r1=507.2 r2=502.0 | 22/22 22/22 | - |
| node2-back | 495.7 | r1=489.2 r2=502.2 | 22/22 22/22 | - |

- r1: cluster start: all 3 nodes started in 20.9s
- r1: cluster stop-node3: docker stop took 1.0s
- r1: cluster rejoin-node3 (new container): 5.4s
- r1: cluster kill-node2-mid-query: q18=ok q21=ok  
- r1: cluster recover-after-kill: first correct q06 through node 1 after 90.2s, attempts=1
- r1: cluster restart-node2: 5.6s
- r2: cluster start: all 3 nodes started in 19.8s
- r2: cluster stop-node3: docker stop took 0.9s
- r2: cluster rejoin-node3 (new container): 5.6s
- r2: cluster kill-node2-mid-query: q18=ok q21=ok  
- r2: cluster recover-after-kill: first correct q06 through node 1 after 103.0s, attempts=1
- r2: cluster restart-node2: 5.4s

