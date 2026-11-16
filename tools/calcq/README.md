# calcq: calculation queue
queue.txt: one job per line `ID|command` (run from the repo root). status.txt: `ID|state|start|end|exit`.
runner.sh runs pending jobs in order, never more than MAXJOBS heavy python jobs at once, logs to logs/ID.log.
A job is only enqueued after its PREREG lock is committed and pushed (lock-before-results rule).
