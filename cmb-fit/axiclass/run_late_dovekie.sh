#!/bin/bash
# CubeMind PREREGISTRATION_LATE_DOVEKIE_LEE.md: after the edge scan has finished and no Late Twist grid fit is running,
# run the Dovekie references and the rule-chosen Late Twist points. At most 8 fits run at once.
R=/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/results
PY=/home/syndyr/micromamba/envs/aegis/bin/python
A=/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass
running() { ps -eo args | grep 'early_late_spa.py ax_' | grep -v grep | grep -vc 'bash -c'; }
until grep -q "edge scan finished" "$R/lanes/run_edge.log" 2>/dev/null; do sleep 300; done
while ps -eo args | grep 'early_late_spa.py ax_spa_latetwist_gF' | grep -v grep | grep -v 'bash -c' | grep -qv '_dovekie'; do sleep 300; done
names=$($PY $A/pick_late_dovekie.py)
echo "$(date '+%F %T') LD points: $(echo $names)"
for n in $names; do
  [ -f "$R/cmp_$n.json" ] || [ -f "$R/lanes/$n.claim" ] && continue
  while [ "$(running)" -ge 8 ]; do sleep 60; done
  echo "$(date '+%F %T') LD start $n"
  ( OMP_NUM_THREADS=2 $PY $A/early_late_spa.py $n > "$R/lanes/$n.log" 2>&1; echo "$(date '+%F %T') LD done $n" ) &
  sleep 20
done
wait
echo "$(date '+%F %T') LD finished"
