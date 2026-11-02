#!/bin/bash
# CubeMind PREREGISTRATION_COUPLED_TWIST.md (gates V1-V4 passed, COUPLED_TWIST_GATES.md). Waits for the robustness
# queue and the Late Twist rerun, then: batch A = free fit (C1-C4) + C5 at beta = +-0.816; batch B = beta profile.
# Portable paths (make_portable.py): override with TWIST_RESULTS, TWIST_BUILDS, TWIST_PY.
AXI="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
RES="${TWIST_RESULTS:-$(dirname "$AXI")/results}"
BLD="${TWIST_BUILDS:-$HOME}"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
R=$RES
S=$AXI/early_late_spa.py
until grep -q "robustness fits finished" "$R/lanes/run_robustness.log" 2>/dev/null && [ -f "$R/cmp_ax_spa_latetwist.json" ]; do
  echo "$(date '+%F %T') waiting for robustness batch 2 and the Late Twist rerun..."; sleep 900
done
echo "$(date '+%F %T') batch A: coupled free fit + C5"
for n in ax_spa_coupledtwist ax_spa_coupledtwist_beta0.816 ax_spa_coupledtwist_beta-0.816; do
  OMP_NUM_THREADS=5 nohup $PY $S $n > "$R/lanes/$n.log" 2>&1 &
done
wait
echo "$(date '+%F %T') batch B: beta profile"
for b in -0.1 -0.05 0 0.05 0.1; do
  n=ax_spa_coupledtwist_beta$b
  OMP_NUM_THREADS=3 nohup $PY $S $n > "$R/lanes/$n.log" 2>&1 &
done
wait
echo "$(date '+%F %T') coupled fits finished"
