#!/bin/bash
# CubeMind PREREGISTRATION_ROBUSTNESS.md (post-hoc): wait for the three Late Twist fits, then
# batch 1 = R1 (best of 4) + R2 A3 part (DES Y5), 3 threads each; batch 2 = R2 Late Twist part, 5 threads each.
R=/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/results
PY=/home/syndyr/micromamba/envs/aegis/bin/python
S=/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass/early_late_spa.py
need="ax_spa_latetwist ax_spa_lcdm_halofit ax_spa_w0wa_halofit"
while true; do
  missing=0
  for n in $need; do [ -f "$R/cmp_$n.json" ] || missing=1; done
  [ $missing -eq 0 ] && break
  echo "$(date '+%F %T') waiting for the Late Twist fits..."; sleep 900
done
echo "$(date '+%F %T') batch 1: R1 and R2 (A3 with DES Y5)"
for n in ax_spa_w0wa_b4 ax_spa_edelock_w0wa_b4 ax_spa_lcdm_desy5 ax_spa_w0wa_desy5 ax_spa_edelock_w0wa_desy5; do
  OMP_NUM_THREADS=3 nohup $PY $S $n > "$R/lanes/$n.log" 2>&1 &
done
wait
echo "$(date '+%F %T') batch 2: R2 (Late Twist with DES Y5)"
for n in ax_spa_latetwist_desy5 ax_spa_lcdm_halofit_desy5 ax_spa_w0wa_halofit_desy5; do
  OMP_NUM_THREADS=5 nohup $PY $S $n > "$R/lanes/$n.log" 2>&1 &
done
wait
echo "$(date '+%F %T') robustness fits finished"
