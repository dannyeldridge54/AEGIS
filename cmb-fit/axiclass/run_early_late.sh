#!/bin/bash
# ROUTE.md A3: wait until the Windows CAMB queue (power-n test and f profile) is finished, then run the four AxiCLASS
# early/late fits in parallel, 4 threads each (16 cores). Logs in results/lanes/<name>.log.
R=/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/results
PY=/home/syndyr/micromamba/envs/aegis/bin/python
S=/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass/early_late_spa.py
need="spa_edelock_n2 spa_edelock_fde0.01 spa_edelock_fde0.02 spa_edelock_fde0.04 spa_edelock_fde0.06 spa_edelock_fde0.08 spa_edelock_fde0.10 spa_edelock_fde0.12 spa_edelock_th0.5 spa_edelock_th1.0 spa_edelock_th1.5 spa_edelock_th2.0 spa_edelock_th2.4 spa_edelock_th2.7 spa_edelock_th2.9 spa_edelock_th3.05"
while true; do
  missing=0
  for n in $need; do [ -f "$R/cmp_$n.json" ] || missing=1; done
  [ $missing -eq 0 ] && break
  echo "$(date '+%F %T') waiting for the CAMB queue to finish..."; sleep 600
done
echo "$(date '+%F %T') starting the four AxiCLASS fits"
for n in ax_spa_lcdm ax_spa_w0wa ax_spa_edelock ax_spa_edelock_w0wa; do
  OMP_NUM_THREADS=4 nohup $PY $S $n > "$R/lanes/$n.log" 2>&1 &
done
wait
echo "$(date '+%F %T') all four AxiCLASS fits finished"
