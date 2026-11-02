#!/bin/bash
# C4 / true Omega_m / S8 for a Coupled Twist run (CubeMind PREREGISTRATION_COUPLED_TWIST.md).
# Portable paths (make_portable.py): override with TWIST_RESULTS, TWIST_BUILDS, TWIST_PY.
AXI="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")"/.. && pwd)"
RES="${TWIST_RESULTS:-$(dirname "$AXI")/results}"
BLD="${TWIST_BUILDS:-$HOME}"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
cd $AXI/coupled
OMP_NUM_THREADS=2 timeout 1200 $PY -W ignore coupled_weff.py "$1" 2>&1 | grep -v -i -E 'warn|jaxlib|cuda' | tail -25
