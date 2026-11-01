#!/bin/bash
# Late Twist (CubeMind PREREGISTRATION_LATE_TWIST.md): wait for the four A3 AxiCLASS fits, then run the Late Twist and
# its two halofit reference runs in parallel, 5 threads each.
R=/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/results
PY=/home/syndyr/micromamba/envs/aegis/bin/python
S=/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass/early_late_spa.py
need="ax_spa_lcdm ax_spa_w0wa ax_spa_edelock ax_spa_edelock_w0wa"
while true; do
  missing=0
  for n in $need; do [ -f "$R/cmp_$n.json" ] || missing=1; done
  [ $missing -eq 0 ] && break
  echo "$(date '+%F %T') waiting for the A3 fits..."; sleep 900
done
echo "$(date '+%F %T') starting the Late Twist fits"
for n in ax_spa_latetwist ax_spa_lcdm_halofit ax_spa_w0wa_halofit; do
  OMP_NUM_THREADS=5 nohup $PY $S $n > "$R/lanes/$n.log" 2>&1 &
done
wait
echo "$(date '+%F %T') Late Twist fits finished"
