#!/bin/bash
# CubeMind PREREGISTRATION_HIGH_MASS_CORNER.md: 9 Late Twist points at sub-Planckian F and large m (Pantheon+).
# Starts after the LD runner has finished; at most 8 fits run at once.
R=/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/results
PY=/home/syndyr/micromamba/envs/aegis/bin/python
S=/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass/early_late_spa.py
PTS="gF-0.6m0.751 gF-0.6m1.052 gF-0.6m1.353 gF-0.4m0.551 gF-0.4m0.852 gF-0.4m1.153 gF-0.2m0.351 gF-0.2m0.652 gF-0.2m0.953"
running() { ps -eo args | grep 'early_late_spa.py ax_' | grep -v grep | grep -vc 'bash -c'; }
until grep -q "LD finished" "$R/lanes/run_late_dovekie.log" 2>/dev/null; do sleep 300; done
for p in $PTS; do
  n=ax_spa_latetwist_$p
  [ -f "$R/cmp_$n.json" ] || [ -f "$R/lanes/$n.claim" ] && continue
  while [ "$(running)" -ge 8 ]; do sleep 60; done
  echo "$(date '+%F %T') HC start $n"
  ( OMP_NUM_THREADS=2 $PY $S $n > "$R/lanes/$n.log" 2>&1; echo "$(date '+%F %T') HC done $n" ) &
  sleep 20
done
wait
echo "$(date '+%F %T') HC finished"
