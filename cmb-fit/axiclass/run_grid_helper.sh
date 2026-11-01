#!/bin/bash
# Helper worker for the (F, m) grid (scheduling only; no setting changes). Waits until the Dovekie and best-of-4 fits
# have freed their cores, then takes Late Twist grid points from the END of the stage-1 list (DES Y5 first, reversed)
# while run_grid.sh works from the start. early_late_spa.py claims each run atomically, so no point runs twice.
R=/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/results
A=/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass
PY=/home/syndyr/micromamba/envs/aegis/bin/python
run() { [ -f "$R/lanes/$1.claim" ] && exit 0
        OMP_NUM_THREADS=2 $PY $A/early_late_spa.py "$1" > "$R/lanes/$1.helper.log" 2>&1
        grep -q "claimed by another worker" "$R/lanes/$1.helper.log" && rm -f "$R/lanes/$1.helper.log" && exit 0
        mv -f "$R/lanes/$1.helper.log" "$R/lanes/$1.log"; echo "$(date '+%F %T') helper done $1"; }
export -f run; export R A PY
while ps -eo args | grep -E 'early_late_spa.py ax_spa_(.*dovekie|edelock_w0wa_b4)' | grep -vq grep; do
  echo "$(date '+%F %T') helper waiting for Dovekie and best-of-4 fits to finish"; sleep 300
done
echo "$(date '+%F %T') helper starting (4 workers, 2 threads each)"
{ $PY $A/grid_tools.py latetwist; $PY $A/grid_tools.py latetwist _desy5; } | tac |
  while read n; do [ -f "$R/cmp_$n.json" ] || [ -f "$R/lanes/$n.claim" ] || echo "$n"; done |
  xargs -P 4 -I{} bash -c 'run {}'
echo "$(date '+%F %T') helper finished"
