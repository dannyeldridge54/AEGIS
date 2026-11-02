#!/bin/bash
# CubeMind PREREGISTRATION_TORSION_F.md (locked 2026-11-02 14:51:28): F fixed at sqrt(3/2) and sqrt6 M_Pl, m free.
# DES Y5 and Pantheon+ start now; the Union3 pair starts once the LU batch (run_union3.sh) has finished, so the box is
# not oversubscribed.
# Portable paths (make_portable.py): override with TWIST_RESULTS, TWIST_BUILDS, TWIST_PY.
AXI="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
RES="${TWIST_RESULTS:-$(dirname "$AXI")/results}"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
start() {
  [ -f "$RES/cmp_$1.json" ] && return                 # early_late_spa.py makes its own atomic .claim
  echo "$(date '+%F %T') TF start $1"
  ( OMP_NUM_THREADS=2 nice -n 5 $PY $AXI/early_late_spa.py "$1" > "$RES/lanes/$1.log" 2>&1; echo "$(date '+%F %T') TF done $1" ) &
  sleep 15
}
for f in 0.0880 0.3891; do start ax_spa_latetwist_fF${f}_desy5_nlfix; start ax_spa_latetwist_fF${f}_nlfix; done
until grep -q "LU finished" "$RES/lanes/run_union3.log" 2>/dev/null; do sleep 120; done
for f in 0.0880 0.3891; do start ax_spa_latetwist_fF${f}_union3_nlfix; done
wait
echo "$(date '+%F %T') TF finished"
