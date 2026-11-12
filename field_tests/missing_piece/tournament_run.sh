#!/usr/bin/env bash
# Cloud: all TOURNAMENT fits (PREREG_TOURNAMENT.md), two workers, resumable per start. Relaunch until 24/24, then score.
source /tmp/claude-0/-home-claude/c19a5ec8-2fdf-518d-a2d4-024b6ab629a5/scratchpad/env.sh
export TWIST_RESULTS=/home/claude/aegis/cmb-fit/results OMP_NUM_THREADS=1
cd /home/claude/aegis/field_tests/missing_piece
J0="LCDM FLAG1 SPIRAL0 ON2"; J1="ON1 ON05 SPIRAL W0WA"
( for v in $J0; do for c in FULL NOBAO SDSS; do python3 tournament.py fit $v $c; done; done >> tournament_w0.log 2>&1 ) &
( for v in $J1; do for c in FULL NOBAO SDSS; do python3 tournament.py fit $v $c; done; done >> tournament_w1.log 2>&1 ) &
wait
n=$(ls tournament/*_FULL.json tournament/*_NOBAO.json tournament/*_SDSS.json 2>/dev/null | wc -l)
echo "$(date '+%F %T') fits done: $n/24" >> tournament_log.txt
[ "$n" = 24 ] && python3 tournament.py score >> tournament_log.txt 2>&1 && echo "$(date '+%F %T') scored" >> tournament_log.txt
