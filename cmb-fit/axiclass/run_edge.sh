#!/bin/bash
# CubeMind PREREGISTRATION_EDGE_SCAN.md (locked 12:34:01): 8 edge points x {DES Y5 (blind, first), Pantheon+}.
# Starts each run only when fewer than 8 fits are running; early_late_spa.py claims each run atomically.
R=/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/results
PY=/home/syndyr/micromamba/envs/aegis/bin/python
S=/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass/early_late_spa.py
PTS="gF0m0.057 gF0m0.102 gF0.2m-0.143 gF0.2m-0.098 gF0.4m-0.343 gF0.4m-0.298 gF0.5m-0.443 gF0.5m-0.398"
names=""
for p in $PTS; do names="$names ax_spa_latetwist_${p}_desy5"; done
for p in $PTS; do names="$names ax_spa_latetwist_${p}"; done
running() { ps -eo args | grep 'early_late_spa.py ax_' | grep -v grep | grep -vc 'bash -c'; }
for n in $names; do
  [ -f "$R/cmp_$n.json" ] || [ -f "$R/lanes/$n.claim" ] && continue
  while [ "$(running)" -ge 8 ]; do sleep 60; done
  echo "$(date '+%F %T') edge start $n"
  ( OMP_NUM_THREADS=2 $PY $S $n > "$R/lanes/$n.edge.log" 2>&1
    if grep -q "claimed by another worker" "$R/lanes/$n.edge.log"; then rm -f "$R/lanes/$n.edge.log"
    else mv -f "$R/lanes/$n.edge.log" "$R/lanes/$n.log"; echo "$(date '+%F %T') edge done $n"; fi ) &
  sleep 20
done
wait
echo "$(date '+%F %T') edge scan finished"
