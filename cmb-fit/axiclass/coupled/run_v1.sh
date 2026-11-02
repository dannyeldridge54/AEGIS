#!/bin/bash
# Gate V1: beta = 0 must reproduce the original AxiCLASS chi2 at the same Late Twist point (to within 0.05).
# Portable paths (make_portable.py): override with TWIST_RESULTS, TWIST_BUILDS, TWIST_PY.
AXI="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")"/.. && pwd)"
RES="${TWIST_RESULTS:-$(dirname "$AXI")/results}"
BLD="${TWIST_BUILDS:-$HOME}"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
P=$PY
S=$AXI/coupled/gates.py
cd /tmp
for w in original coupled; do
  OMP_NUM_THREADS=3 $P $S chi2 "$w" 0.0 2>&1 | grep '^{'
done
