#!/bin/bash
# Run bug_reproducer.py on the installed AxiCLASS and on the fixed build; then the fixed build at smaller field masses
# (a harder-frozen field) to show the small remaining non-linear difference shrinks with m.
# Portable paths (make_portable.py): override with TWIST_RESULTS, TWIST_BUILDS, TWIST_PY.
AXI="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")"/.. && pwd)"
RES="${TWIST_RESULTS:-$(dirname "$AXI")/results}"
BLD="${TWIST_BUILDS:-$HOME}"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
cd "$(dirname "$0")"
for b in AxiCLASS AxiCLASS_nlfix; do
  echo "== $b"
  OMP_NUM_THREADS=1 $PY -W ignore bug_reproducer.py $BLD/$b/python/build 2>&1 | tail -5
done
