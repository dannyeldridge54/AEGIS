#!/usr/bin/env bash
# Cloud: KAPPA-ALPHA1 fits (PREREG_KAPPA_ALPHA1.md), resumable. Relaunch until 3/3, then score.
source /tmp/claude-0/-home-claude/c19a5ec8-2fdf-518d-a2d4-024b6ab629a5/scratchpad/env.sh
export TWIST_RESULTS=/home/claude/aegis/cmb-fit/results OMP_NUM_THREADS=1
cd /home/claude/aegis/field_tests/missing_piece
for c in FULL NOBAO SDSS; do python3 kappa_alpha1.py fit $c; done >> kappa_alpha1.log 2>&1
n=$(ls kappa_alpha1/K816_FULL.json kappa_alpha1/K816_NOBAO.json kappa_alpha1/K816_SDSS.json 2>/dev/null | wc -l)
echo "$(date '+%F %T') fits done: $n/3" >> kappa_alpha1.log
[ "$n" = 3 ] && python3 kappa_alpha1.py score >> kappa_alpha1.log 2>&1 && echo "$(date '+%F %T') scored" >> kappa_alpha1.log
