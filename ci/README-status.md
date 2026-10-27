## In progress

- `compare` wave `c1-servers`, run [40478832460](https://github.com/C0fuge/egret/actions/runs/40478832460): the four
  45fc0a9e6e02 vs 27f583adccd7 jobs (its upstream job failed: `actions/checkout` cannot fetch a short SHA).
- `compare` wave `c1-servers`, upstream pair: run 40478981558 failed (upstream build: copy-dependencies outside the reactor), re-run as [40479274289](https://github.com/C0fuge/egret/actions/runs/40479274289) (upstream 07631d72954a, `duckDbThreads=2`, vs 45fc0a9e6e02, `duckDbThreads=4`).
