#!/usr/bin/env bash
# Cloud: PURE-TWIST fits (PREREG_PURE_TWIST.md), resumable. Relaunch until 3/3, then score.
source /tmp/claude-0/-home-claude/c19a5ec8-2fdf-518d-a2d4-024b6ab629a5/scratchpad/env.sh
export TWIST_RESULTS=/home/claude/aegis/cmb-fit/results OMP_NUM_THREADS=1
cd /home/claude/aegis/field_tests/missing_piece
for c in FULL NOBAO SDSS; do python3 pure_twist.py fit $c; done >> pure_twist.log 2>&1
n=$(ls pure_twist/K816B0_FULL.json pure_twist/K816B0_NOBAO.json pure_twist/K816B0_SDSS.json 2>/dev/null | wc -l)
echo "$(date '+%F %T') fits done: $n/3" >> pure_twist.log
[ "$n" = 3 ] && python3 pure_twist.py score >> pure_twist.log 2>&1 && echo "$(date '+%F %T') scored" >> pure_twist.log
