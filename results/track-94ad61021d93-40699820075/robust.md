# Server comparison - Report 3: ROBUSTNESS (compare run 40699820075)

Same runner type and containers as Reports 1 and 2 (server: `eclipse-temurin:21-jre`, 2 CPUs on cpus 0,1, 6 GB, `-Xmx3g -XX:MaxDirectMemorySize=2g`; clients on cpus 2,3). Servers: ours-new = `7562a5bdb7b9`; ours-27f5 = `27f583adccd7`; up-native = `9db2bf16a0d15a657f491bb18de1ef50e2e208a8`; up-main = `dbacd8d585bce2ef2a449c821fe3a53cc6060b57`.

## 3-node cluster: i18-dc-off-vs-on (s3)

Side A = 94ad61021d93 `-DdistributedComplete=false`, rounds with data: 3

| check | wall s median | per round wall s | correct / queries per round | failed |
|---|---|---|---|---|
| all-up | 400.8 | r1=313.7 r2=487.8 | 22/22 22/22 | - |
| node3-stopped | 409.8 | r1=317.0 r2=502.5 | 22/22 22/22 | - |
| node3-back | 407.7 | r1=315.8 r2=499.6 | 22/22 22/22 | - |
| node2-dead | 416.3 | r1=313.7 r2=518.9 | 22/22 22/22 | - |
| node2-back | 415.6 | r1=318.1 r2=513.0 | 22/22 22/22 | - |

- r1: cluster start: all 3 nodes started in 18.2s
- r1: cluster stop-node3: docker stop took 0.9s
- r1: cluster rejoin-node3 (new container): 5.3s
- r1: cluster kill-node2-mid-query: q18=ok q21=ok  
- r1: cluster recover-after-kill: first correct q06 through node 1 after 62.9s, attempts=1
- r1: cluster restart-node2: 6.0s
- r2: cluster start: all 3 nodes started in 18.9s
- r2: cluster stop-node3: docker stop took 0.7s
- r2: cluster rejoin-node3 (new container): 5.0s
- r2: cluster kill-node2-mid-query: q18=ok q21=ok  
- r2: cluster recover-after-kill: first correct q06 through node 1 after 100.2s, attempts=1
- r2: cluster restart-node2: 5.5s
- r3: cluster start: all 3 nodes started in 18.5s

Side B = 94ad61021d93 `-DdistributedComplete=true`, rounds with data: 2

| check | wall s median | per round wall s | correct / queries per round | failed |
|---|---|---|---|---|
| all-up | 423.9 | r1=369.4 r2=478.4 | 22/22 22/22 | - |
| node3-stopped | 523.7 | r1=521.6 r2=525.8 | 22/22 22/22 | - |
| node3-back | 520.6 | r1=520.5 r2=520.7 | 22/22 22/22 | - |
| node2-dead | 530.4 | r1=526.2 r2=534.6 | 22/22 22/22 | - |
| node2-back | 522.4 | r1=527.3 r2=517.5 | 22/22 22/22 | - |

- r1: cluster start: all 3 nodes started in 18.6s
- r1: cluster stop-node3: docker stop took 1.0s
- r1: cluster rejoin-node3 (new container): 5.0s
- r1: cluster kill-node2-mid-query: q18=ok q21=ok  
- r1: cluster recover-after-kill: first correct q06 through node 1 after 102.8s, attempts=1
- r1: cluster restart-node2: 5.5s
- r2: cluster start: all 3 nodes started in 19.0s
- r2: cluster stop-node3: docker stop took 0.9s
- r2: cluster rejoin-node3 (new container): 5.3s
- r2: cluster kill-node2-mid-query: q18=ok q21=ok  
- r2: cluster recover-after-kill: first correct q06 through node 1 after 104.3s, attempts=1
- r2: cluster restart-node2: 6.0s

