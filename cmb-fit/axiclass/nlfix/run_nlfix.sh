#!/bin/bash
# NR replication queue (CubeMind PREREGISTRATION_NLFIX_REPLICATION.md; speed deviation 18:59:09).
# Stage 1 (Late Twist grids + edge + HC) fills free slots as soon as fewer than 8 fits run on the machine.
# Stage 2 (LD) waits for stage 1 and for tonight's "LD finished" (it uses the DES-Dovekie references). Stage 3 (Coupled
# grid) follows stage 1; stage 4 (C5 + beta profile) follows stage 3. 2 threads per fit; early_late_spa.py loads the
# fixed builds for "_nlfix" names and warm-starts from the same-named original run.
R=/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/results
A=/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass
PY=/home/syndyr/micromamba/envs/aegis/bin/python
T=$A/nlfix/nlfix_tools.py
running() { ps -eo args | grep 'early_late_spa.py ax_' | grep -v grep | grep -vc 'bash -c'; }
nr_running() { ps -eo args | grep 'early_late_spa.py ax_.*_nlfix' | grep -v grep | grep -vc 'bash -c'; }
originals_done() { grep -q "HC finished" "$R/lanes/run_hc.log" 2>/dev/null && grep -q "grid fits finished" "$R/lanes/run_grid.log" 2>/dev/null; }
busy() {                                         # the official queues keep priority: NR uses at most 4 slots until they end
  [ "$(running)" -ge 8 ] && return 0
  originals_done || [ "$(nr_running)" -lt 4 ] || return 0
  return 1
}
pending() { while read n; do [ -f "$R/cmp_$n.json" ] || [ -f "$R/lanes/$n.claim" ] || echo "$n"; done; }
launch() {                                       # start each name when a slot is free; then wait for all of them
  for n in $(cat); do
    while busy; do sleep 60; done
    echo "$(date '+%F %T') NR start $n"
    ( OMP_NUM_THREADS=2 $PY $A/early_late_spa.py "$n" > "$R/lanes/$n.log" 2>&1; echo "$(date '+%F %T') NR done $n" ) &
    sleep 20
  done
  wait
}
echo "$(date '+%F %T') NR stage 1: Late Twist grids, edge, HC (slot-based)"
$PY $T stage1 | pending | launch
echo "$(date '+%F %T') NR stage 3: Coupled grid"
$PY $T coupled | pending | launch
until grep -q "LD finished" "$R/lanes/run_late_dovekie.log" 2>/dev/null; do sleep 300; done
echo "$(date '+%F %T') NR stage 2: LD"
$PY $T ld | pending | launch
echo "$(date '+%F %T') NR stage 4: C5 and beta profile"
$PY $T final | pending | launch
echo "$(date '+%F %T') NR finished"
