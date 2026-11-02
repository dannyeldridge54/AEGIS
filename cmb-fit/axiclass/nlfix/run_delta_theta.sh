#!/bin/bash
# B4 input: delta_theta at the NR (corrected-code) Late Twist best fits (Pantheon+ grid best, DES Y5 official best).
# Portable paths (make_portable.py): override with TWIST_RESULTS, TWIST_BUILDS, TWIST_PY.
AXI="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")"/.. && pwd)"
RES="${TWIST_RESULTS:-$(dirname "$AXI")/results}"
BLD="${TWIST_BUILDS:-$HOME}"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
cd $AXI/nlfix
OMP_NUM_THREADS=2 $PY -W ignore delta_theta.py \
  ax_spa_latetwist_gF0.4m-0.3_nlfix ax_spa_latetwist_gF0m0.102_desy5_nlfix 2>&1 | grep -E 'delta_theta|Error|Traceback|Key' | tail -6
