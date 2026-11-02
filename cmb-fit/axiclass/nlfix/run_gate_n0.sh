#!/bin/bash
# Gate N0 for the nlfix replication: validate both fixed builds through early_late_spa's own switch.
# Portable paths (make_portable.py): override with TWIST_RESULTS, TWIST_BUILDS, TWIST_PY.
AXI="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")"/.. && pwd)"
RES="${TWIST_RESULTS:-$(dirname "$AXI")/results}"
BLD="${TWIST_BUILDS:-$HOME}"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
cd $AXI/nlfix
for k in latetwist coupled; do
  OMP_NUM_THREADS=2 $PY -W ignore validate_nlfix_builds.py "$k" 2>&1 | grep -E 'N0|Error' | tail -3
done
