#!/bin/bash
# w0-wa (CPL) mapping of the official best Late Twist grid points (Pantheon+ and DES Y5).
# Portable paths (make_portable.py): override with TWIST_RESULTS, TWIST_BUILDS, TWIST_PY.
AXI="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
RES="${TWIST_RESULTS:-$(dirname "$AXI")/results}"
BLD="${TWIST_BUILDS:-$HOME}"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
cd $AXI
for n in "$@"; do
  echo "== $n"
  OMP_NUM_THREADS=2 timeout 900 $PY -W ignore latetwist_cpl.py "$n" 2>&1 | grep -v -i -E 'warn|jaxlib|cuda' | tail -6
done
