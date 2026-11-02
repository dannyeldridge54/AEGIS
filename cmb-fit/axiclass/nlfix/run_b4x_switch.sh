#!/bin/bash
# B4-X switch numbers (R, z_on, b0) at the NR Late Twist best fits.
# Portable paths (make_portable.py): override with TWIST_RESULTS, TWIST_BUILDS, TWIST_PY.
AXI="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")"/.. && pwd)"
RES="${TWIST_RESULTS:-$(dirname "$AXI")/results}"
BLD="${TWIST_BUILDS:-$HOME}"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
cd $AXI/nlfix
OMP_NUM_THREADS=2 $PY -W ignore b4x_switch.py \
  ax_spa_latetwist_gF0.4m-0.3_nlfix ax_spa_latetwist_gF0m0.102_desy5_nlfix 2>&1 | grep -E '^ax_spa|Error|Traceback|Key' | tail -6
