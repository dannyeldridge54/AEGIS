#!/bin/bash
# Start NR stage 2 (LD on DES-Dovekie) now in idle slots; it depends only on the finished stage 1 grids and edge.
# Atomic claims mean fill_slots2.sh and run_nlfix.sh skip these later.
# Portable paths (make_portable.py): override with TWIST_RESULTS, TWIST_BUILDS, TWIST_PY.
AXI="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")"/.. && pwd)"
RES="${TWIST_RESULTS:-$(dirname "$AXI")/results}"
BLD="${TWIST_BUILDS:-$HOME}"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
R=$RES
A=$AXI
for n in $($PY $A/nlfix/nlfix_tools.py ld); do
  [ -f "$R/cmp_$n.json" ] || [ -f "$R/lanes/$n.claim" ] && continue
  echo "$(date '+%F %T') LD-now start $n"
  ( OMP_NUM_THREADS=2 $PY $A/early_late_spa.py "$n" > "$R/lanes/$n.log" 2>&1; echo "$(date '+%F %T') LD-now done $n" ) &
  sleep 20
done
wait
echo "$(date '+%F %T') LD-now finished"
