#!/bin/bash
# CubeMind PREREGISTRATION_TORSION_F_PLANCK.md (locked 2026-11-02 14:55:36): F fixed at (4/pi) sqrt(3/2) M_Pl, m free.
# DES Y5 + Pantheon+ start when the Coupled cold restart has finished (frees 2 cores); Union3 after the LU batch.
# Portable paths (make_portable.py): override with TWIST_RESULTS, TWIST_BUILDS, TWIST_PY.
AXI="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
RES="${TWIST_RESULTS:-$(dirname "$AXI")/results}"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
start() {
  [ -f "$RES/cmp_$1.json" ] && return                 # early_late_spa.py makes its own atomic .claim
  echo "$(date '+%F %T') TFP start $1"
  ( OMP_NUM_THREADS=2 nice -n 5 $PY $AXI/early_late_spa.py "$1" > "$RES/lanes/$1.log" 2>&1; echo "$(date '+%F %T') TFP done $1" ) &
  sleep 15
}
until [ -f "$RES/cmp_ax_spa_coupledtwist_gF0.4m-0.1_nlfix_r4.json" ]; do sleep 120; done
start ax_spa_latetwist_fF0.1930_desy5_nlfix; start ax_spa_latetwist_fF0.1930_nlfix
until grep -q "LU finished" "$RES/lanes/run_union3.log" 2>/dev/null; do sleep 120; done
start ax_spa_latetwist_fF0.1930_union3_nlfix
wait
echo "$(date '+%F %T') TFP finished"
