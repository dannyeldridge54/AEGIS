#!/bin/bash
# D2169: wait for the D2163 best-of-4 pair to finish, then run the tightened minimiser on the same pair
while pgrep -f "OUT_SUFFIX_BO4_MARK|weave_lcdm_pr4.py [LW] desdovekie hillipop" >/dev/null; do sleep 60; done
cd /home/claude/aegis
export BEST_OF=4 OUT_SUFFIX=_tight OVERRIDE_BOBYQA='{"rhoend": 0.005, "seek_global_minimum": true, "objfun_has_noise": true}'
timeout 7000 python3 field_tests/weave_lcdm/weave_lcdm_pr4.py L desdovekie hillipop > /tmp/claude-0/tight_L.log 2>&1 &
timeout 7000 python3 field_tests/weave_lcdm/weave_lcdm_pr4.py W desdovekie hillipop > /tmp/claude-0/tight_W.log 2>&1 &
wait; tail -1 /tmp/claude-0/tight_L.log; tail -1 /tmp/claude-0/tight_W.log
