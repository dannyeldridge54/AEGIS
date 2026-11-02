#!/bin/bash
# CubeMind PREREGISTRATION_LATE_UNION3.md (locked 2026-11-02 14:23:26): the Late Twist at the DES Y5 best point on Union3.
# Portable paths (make_portable.py): override with TWIST_RESULTS, TWIST_BUILDS, TWIST_PY.
AXI="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
RES="${TWIST_RESULTS:-$(dirname "$AXI")/results}"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
for n in ax_spa_latetwist_gF0m0.102_union3_nlfix ax_spa_lcdm_halofit_union3 ax_spa_w0wa_halofit_union3; do
  [ -f "$RES/cmp_$n.json" ] && continue            # early_late_spa.py makes its own atomic .claim
  echo "$(date '+%F %T') LU start $n"
  ( OMP_NUM_THREADS=2 nice -n 5 $PY $AXI/early_late_spa.py "$n" > "$RES/lanes/$n.log" 2>&1; echo "$(date '+%F %T') LU done $n" ) &
  sleep 15
done
wait
echo "$(date '+%F %T') LU finished"
