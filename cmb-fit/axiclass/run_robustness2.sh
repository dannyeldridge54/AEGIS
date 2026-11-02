#!/bin/bash
# CubeMind PREREGISTRATION_ROBUSTNESS.md, requeued (run_robustness.sh waited on the Late Twist file, which was archived for
# the approved rerun). Batch 1 does not need the Late Twist: start it now, 2 threads each beside the 4-thread rerun.
# Batch 2 (Late Twist with DES Y5) starts once batch 1 and the Late Twist rerun have both finished.
# Portable paths (make_portable.py): override with TWIST_RESULTS, TWIST_BUILDS, TWIST_PY.
AXI="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
RES="${TWIST_RESULTS:-$(dirname "$AXI")/results}"
BLD="${TWIST_BUILDS:-$HOME}"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
R=$RES
S=$AXI/early_late_spa.py
echo "$(date '+%F %T') batch 1: R1 and R2 (A3 with DES Y5)"
for n in ax_spa_w0wa_b4 ax_spa_edelock_w0wa_b4 ax_spa_lcdm_desy5 ax_spa_w0wa_desy5 ax_spa_edelock_w0wa_desy5; do
  OMP_NUM_THREADS=2 nohup $PY $S $n > "$R/lanes/$n.log" 2>&1 &
done
wait
echo "$(date '+%F %T') batch 1 finished"
while [ ! -f "$R/cmp_ax_spa_latetwist.json" ]; do
  echo "$(date '+%F %T') waiting for the Late Twist rerun..."; sleep 600
done
echo "$(date '+%F %T') batch 2: R2 (Late Twist with DES Y5)"
for n in ax_spa_latetwist_desy5 ax_spa_lcdm_halofit_desy5 ax_spa_w0wa_halofit_desy5; do
  OMP_NUM_THREADS=5 nohup $PY $S $n > "$R/lanes/$n.log" 2>&1 &
done
wait
echo "$(date '+%F %T') robustness fits finished"
