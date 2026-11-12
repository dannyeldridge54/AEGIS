#!/usr/bin/env bash
# Cloud: all BETA(z) fits (PREREG_BETAZ.md), two workers, resumable (each start saved). Relaunch until every
# betaz/<label>.json exists, then: python3 betaz_fit.py score. Log: missing_piece/betaz_log.txt
source /tmp/claude-0/-home-claude/c19a5ec8-2fdf-518d-a2d4-024b6ab629a5/scratchpad/env.sh
export TWIST_RESULTS=/home/claude/aegis/cmb-fit/results OMP_NUM_THREADS=1
cd /home/claude/aegis/field_tests/missing_piece
( for l in const_dr2 bz_dr2 sm_dr2; do python3 betaz_fit.py fit $l; done >> betaz_w0.log 2>&1 ) &
( for l in const_dr1 const_dr2_ho bz_dr1 bz_dr2_ho sm_dr2_ho; do python3 betaz_fit.py fit $l; done >> betaz_w1.log 2>&1 ) &
wait
n=$(for l in const_dr2 bz_dr2 sm_dr2 const_dr1 bz_dr1 const_dr2_ho bz_dr2_ho sm_dr2_ho; do [ -f betaz/$l.json ] && echo x; done | wc -l)
echo "$(date '+%F %T') labels done: $n/8" >> betaz_log.txt
[ "$n" = 8 ] && python3 betaz_fit.py score >> betaz_log.txt 2>&1 && echo "$(date '+%F %T') scored" >> betaz_log.txt
