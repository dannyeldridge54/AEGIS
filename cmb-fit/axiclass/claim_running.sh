#!/bin/bash
# Write claim files for fits already running (started before claims existed), so the helper worker skips them.
# Portable paths (make_portable.py): override with TWIST_RESULTS, TWIST_BUILDS, TWIST_PY.
AXI="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
RES="${TWIST_RESULTS:-$(dirname "$AXI")/results}"
BLD="${TWIST_BUILDS:-$HOME}"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
L=$RES/lanes
R=$RES
for n in $(ps -eo args | grep 'early_late_spa.py ax_' | grep -v grep | grep -v 'bash -c' | sed 's/.*early_late_spa.py //'); do
  [ -f "$L/$n.claim" ] || { echo "running-before-claims $(date '+%F %T')" > "$L/$n.claim"; echo "claimed $n"; }
done
# finished or failed grid points also count as taken (they are never retried)
for f in "$L"/ax_spa_latetwist_gF*.log; do
  n=$(basename "$f" .log)
  [ -f "$L/$n.claim" ] || { echo "finished-before-claims" > "$L/$n.claim"; echo "claimed (done) $n"; }
done
