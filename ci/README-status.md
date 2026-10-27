## In progress

- Server comparison task `ci/COMPARE-TASK.md` (4 servers: ours-new, ours-27f5, up-native, up-main). Report 1 SPEED:
  `compare` wave `c2-speed` with every server in an identically limited container (2 CPUs, 6 GB), clients pinned to the
  other cores: run id in the next commit. Run 40481152975 (same wave, dispatched before the container rule) is kept only
  as a no-container reference. Earlier `c1-servers` runs were superseded and cancelled (40478832460 cancelled 09:33 UTC).
