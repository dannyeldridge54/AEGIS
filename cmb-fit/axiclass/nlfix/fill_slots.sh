#!/bin/bash
# Scheduling helper (CubeMind SCALES_CHECKPOINT 2 Nov): start NR stage 3 (Coupled grid) in free slots while the slow
# last HC points of stage 1 finish. Same run names; atomic claims mean run_nlfix.sh later skips anything started here.
R=/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/results
A=/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass
PY=/home/syndyr/micromamba/envs/aegis/bin/python
running() { ps -eo args | grep 'early_late_spa.py ax_' | grep -v grep | grep -vc 'bash -c'; }
for n in $($PY $A/nlfix/nlfix_tools.py coupled); do
  [ -f "$R/cmp_$n.json" ] || [ -f "$R/lanes/$n.claim" ] && continue
  while [ "$(running)" -ge 8 ]; do sleep 60; done
  echo "$(date '+%F %T') fill start $n"
  ( OMP_NUM_THREADS=2 $PY $A/early_late_spa.py "$n" > "$R/lanes/$n.log" 2>&1; echo "$(date '+%F %T') fill done $n" ) &
  sleep 20
done
wait
echo "$(date '+%F %T') fill finished"
