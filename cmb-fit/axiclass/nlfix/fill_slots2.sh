#!/bin/bash
# Scheduling helper 2 (CubeMind SCALES_CHECKPOINT 2 Nov): once the NR Coupled grid is fully accounted, start NR stage 2
# (LD) and stage 4 (C5 + beta profile) together instead of one after the other. Same run names; atomic claims mean
# run_nlfix.sh skips anything started here.
# Portable paths (make_portable.py): override with TWIST_RESULTS, TWIST_BUILDS, TWIST_PY.
AXI="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")"/.. && pwd)"
RES="${TWIST_RESULTS:-$(dirname "$AXI")/results}"
BLD="${TWIST_BUILDS:-$HOME}"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
R=$RES
A=$AXI
running() { ps -eo args | grep 'early_late_spa.py ax_' | grep -v grep | grep -vc 'bash -c'; }
coupled_done() {
  for n in $($PY $A/nlfix/nlfix_tools.py coupled); do
    [ -f "$R/cmp_$n.json" ] && continue
    grep -qE -- '-100000|Cannot reproduce log minimum' "$R/lanes/$n.log" 2>/dev/null && continue
    return 1
  done
  return 0
}
until coupled_done; do sleep 120; done
echo "$(date '+%F %T') coupled grid accounted; starting LD + final"
for n in $($PY $A/nlfix/nlfix_tools.py ld) $($PY $A/nlfix/nlfix_tools.py final); do
  [ -f "$R/cmp_$n.json" ] || [ -f "$R/lanes/$n.claim" ] && continue
  while [ "$(running)" -ge 8 ]; do sleep 60; done
  echo "$(date '+%F %T') fill2 start $n"
  ( OMP_NUM_THREADS=2 $PY $A/early_late_spa.py "$n" > "$R/lanes/$n.log" 2>&1; echo "$(date '+%F %T') fill2 done $n" ) &
  sleep 20
done
wait
echo "$(date '+%F %T') fill2 finished"
