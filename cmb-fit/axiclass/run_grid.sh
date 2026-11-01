#!/bin/bash
# (F, m) profile grid queue (deviation 08:58). Replaces the free Late Twist DES Y5 fit and the free Coupled Twist fits.
# Stage 1: R2 references + Late Twist grid (Pantheon+ and DES Y5). Stage 2: Coupled Twist 3x3 grid around the best
# Late Twist point (beta free). Stage 3: C5 and the beta profile at the best coupled point. 2 threads per fit.
R=/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/results
A=/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass
PY=/home/syndyr/micromamba/envs/aegis/bin/python
run() { OMP_NUM_THREADS=2 $PY $A/early_late_spa.py "$1" > "$R/lanes/$1.log" 2>&1; echo "$(date '+%F %T') done $1"; }
export -f run; export R A PY
skip_done() { while read n; do [ -f "$R/cmp_$n.json" ] || echo "$n"; done; }
echo "$(date '+%F %T') stage 1: references + Late Twist grids"
{ echo ax_spa_lcdm_halofit_desy5; echo ax_spa_w0wa_halofit_desy5
  $PY $A/grid_tools.py latetwist; $PY $A/grid_tools.py latetwist _desy5; } | skip_done | xargs -P 4 -I{} bash -c 'run {}'
echo "$(date '+%F %T') stage 2: Coupled Twist grid"
$PY $A/grid_tools.py coupled | skip_done | xargs -P 7 -I{} bash -c 'run {}'
echo "$(date '+%F %T') stage 3: C5 and beta profile"
$PY $A/grid_tools.py final | skip_done | xargs -P 7 -I{} bash -c 'run {}'
echo "$(date '+%F %T') grid fits finished"
