#!/bin/bash
# Write claim files for fits already running (started before claims existed), so the helper worker skips them.
L=/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/results/lanes
R=/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/results
for n in $(ps -eo args | grep 'early_late_spa.py ax_' | grep -v grep | grep -v 'bash -c' | sed 's/.*early_late_spa.py //'); do
  [ -f "$L/$n.claim" ] || { echo "running-before-claims $(date '+%F %T')" > "$L/$n.claim"; echo "claimed $n"; }
done
# finished or failed grid points also count as taken (they are never retried)
for f in "$L"/ax_spa_latetwist_gF*.log; do
  n=$(basename "$f" .log)
  [ -f "$L/$n.claim" ] || { echo "finished-before-claims" > "$L/$n.claim"; echo "claimed (done) $n"; }
done
