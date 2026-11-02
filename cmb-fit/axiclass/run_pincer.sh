#!/bin/bash
# CubeMind PREREGISTRATION_PINCER.md (locked 2026-11-02 16:22:30): CMB-only fits, then late-data predictions.
# Waits for the torsion-F runners to finish so cores are free. Portable paths: TWIST_RESULTS, TWIST_PY, CUBEMIND.
A="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
R="${TWIST_RESULTS:-$(dirname "$A")/results}"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
CM="${CUBEMIND:-/mnt/c/Users/Danny/Desktop/CubeMind_side_project}"
[ -n "$NO_WAIT" ] || until grep -q "finished" "$R/lanes/run_torsion_f.log" 2>/dev/null && grep -q "finished" "$R/lanes/run_torsion_f_planck.log" 2>/dev/null; do
  sleep 120
done
for n in ax_spa_lcdm_halofit_cmbonly ax_spa_latetwist_gF0m0.102_cmbonly_nlfix ax_spa_latetwist_gF0.4m-0.3_cmbonly_nlfix; do
  [ -f "$R/cmp_$n.json" ] && continue
  echo "$(date '+%F %T') PC start $n"
  ( OMP_NUM_THREADS=2 nice -n 5 $PY $A/early_late_spa.py "$n" > "$R/lanes/$n.log" 2>&1; echo "$(date '+%F %T') PC done $n" ) &
  sleep 15
done
wait
cd "$CM"
for n in ax_spa_lcdm_halofit_cmbonly ax_spa_latetwist_gF0m0.102_cmbonly_nlfix ax_spa_latetwist_gF0.4m-0.3_cmbonly_nlfix; do
  OMP_NUM_THREADS=2 $PY pincer.py eval "$n" 2>&1 | grep -v '^\[' | tail -4
done
$PY pincer.py score
echo "$(date '+%F %T') PC finished"
