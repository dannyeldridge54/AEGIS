#!/bin/bash
# CubeMind PREREGISTRATION_SPIRAL_FIT.md (locked 2026-11-02 17:01:01): effective Spiral Twist on Pantheon+, DES-Dovekie,
# Union3 (no DES Y5). Starts after the pincer batch (cores), and only if the LCDM-limit gate passed.
A="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
R="${TWIST_RESULTS:-$(dirname "$A")/results}"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
CM="${CUBEMIND:-/mnt/c/Users/Danny/Desktop/CubeMind_side_project}"
grep -q '"dLCDM_limit"' "$CM/spiral_fit_mirror.json" || { echo "gate file missing"; exit 1; }
$PY -c "import json,sys; d=json.load(open('$CM/spiral_fit_mirror.json')); sys.exit(0 if abs(d['dLCDM_limit'])<=1.0 else 1)" \
  || { echo "$(date '+%F %T') SF gate FAILED: no fits"; exit 1; }
# Starts together with the pincer batch once the torsion-F runners finish (3 + 3 fits x 2 threads fit in 16 cores).
[ -n "$NO_WAIT" ] || until grep -q "TF finished" "$R/lanes/run_torsion_f.log" 2>/dev/null && grep -q "TFP finished" "$R/lanes/run_torsion_f_planck.log" 2>/dev/null; do sleep 120; done
for n in ax_spa_spiraltwist_nlfix ax_spa_spiraltwist_dovekie_nlfix ax_spa_spiraltwist_union3_nlfix; do
  [ -f "$R/cmp_$n.json" ] && continue
  echo "$(date '+%F %T') SF start $n"
  ( OMP_NUM_THREADS=2 nice -n 5 $PY $A/early_late_spa.py "$n" > "$R/lanes/$n.log" 2>&1; echo "$(date '+%F %T') SF done $n" ) &
  sleep 15
done
wait
echo "$(date '+%F %T') SF finished"
