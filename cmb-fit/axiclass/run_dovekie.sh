#!/bin/bash
# CubeMind PREREGISTRATION_DOVEKIE.md (locked 09:56:48): A3 with DES-Dovekie supernovae, 3 fits, 2 threads each.
# Portable paths (make_portable.py): override with TWIST_RESULTS, TWIST_BUILDS, TWIST_PY.
AXI="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
RES="${TWIST_RESULTS:-$(dirname "$AXI")/results}"
BLD="${TWIST_BUILDS:-$HOME}"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
R=$RES
S=$AXI/early_late_spa.py
echo "$(date '+%F %T') Dovekie A3 fits starting"
for n in ax_spa_lcdm_dovekie ax_spa_w0wa_dovekie ax_spa_edelock_w0wa_dovekie; do
  OMP_NUM_THREADS=2 nohup $PY $S $n > "$R/lanes/$n.log" 2>&1 &
done
wait
echo "$(date '+%F %T') Dovekie A3 fits finished"
