#!/bin/bash
# NR replication queue (CubeMind PREREGISTRATION_NLFIX_REPLICATION.md). Starts only after tonight's queue has finished
# (grid stage 3, LD, HC). Stages: 1 Late Twist grids + edge + HC; 2 LD; 3 Coupled grid; 4 C5 + beta profile.
# At most 8 fits at once, 2 threads each. early_late_spa.py loads the fixed builds for "_nlfix" names.
R=/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/results
A=/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass
PY=/home/syndyr/micromamba/envs/aegis/bin/python
T=$A/nlfix/nlfix_tools.py
run() { OMP_NUM_THREADS=2 $PY $A/early_late_spa.py "$1" > "$R/lanes/$1.log" 2>&1; echo "$(date '+%F %T') NR done $1"; }
export -f run; export R A PY
skip_done() { while read n; do [ -f "$R/cmp_$n.json" ] || [ -f "$R/lanes/$n.claim" ] || echo "$n"; done; }
until grep -q "grid fits finished" "$R/lanes/run_grid.log" 2>/dev/null \
   && grep -q "LD finished" "$R/lanes/run_late_dovekie.log" 2>/dev/null \
   && grep -q "HC finished" "$R/lanes/run_hc.log" 2>/dev/null; do sleep 300; done
echo "$(date '+%F %T') NR stage 1: Late Twist grids, edge, HC"
$PY $T stage1 | skip_done | xargs -P 8 -I{} bash -c 'run {}'
echo "$(date '+%F %T') NR stage 2: LD"
$PY $T ld | skip_done | xargs -P 8 -I{} bash -c 'run {}'
echo "$(date '+%F %T') NR stage 3: Coupled grid"
$PY $T coupled | skip_done | xargs -P 8 -I{} bash -c 'run {}'
echo "$(date '+%F %T') NR stage 4: C5 and beta profile"
$PY $T final | skip_done | xargs -P 8 -I{} bash -c 'run {}'
echo "$(date '+%F %T') NR finished"
