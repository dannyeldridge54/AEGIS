#!/bin/bash
# Gap queue (Danny, 2 Nov: "All gaps scheduled"). Batch A after the spiral + pincer batch; batch B (torsion-F rerun,
# unchanged locked rules) after A. Portable paths: TWIST_RESULTS, TWIST_PY.
A="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
R="${TWIST_RESULTS:-$(dirname "$A")/results}"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
until grep -q "SF finished" "$R/lanes/run_spiral.log" 2>/dev/null && grep -q "PC finished" "$R/lanes/run_pincer.log" 2>/dev/null; do sleep 120; done
# Batch A: CubeMind PREREGISTRATION_SPIRAL_ROBUSTNESS.md (8 fits x 2 threads)
for n in ax_spa_spiraltwist_nobao_nlfix ax_spa_spiraltwist_dovekie_nobao_nlfix ax_spa_spiraltwist_union3_nobao_nlfix \
         ax_spa_lcdm_halofit_dovekie_nobao ax_spa_lcdm_halofit_union3_nobao \
         ax_spa_spiraltwist_nlfix_r4 ax_spa_spiraltwist_dovekie_nlfix_r4 ax_spa_spiraltwist_union3_nlfix_r4; do
  [ -f "$R/cmp_$n.json" ] && continue
  echo "$(date '+%F %T') SR start $n"
  ( OMP_NUM_THREADS=2 nice -n 5 $PY $A/early_late_spa.py "$n" > "$R/lanes/$n.log" 2>&1; echo "$(date '+%F %T') SR done $n" ) &
  sleep 15
done
wait
echo "$(date '+%F %T') SR finished"
# Batch B: torsion-F rerun under the locked TF / TF-P rules (their runners skip finished fits)
bash $A/run_torsion_f.sh > "$R/lanes/run_torsion_f.log" 2>&1 &
sleep 30
bash $A/run_torsion_f_planck.sh > "$R/lanes/run_torsion_f_planck.log" 2>&1 &
wait
echo "$(date '+%F %T') GAPS finished"
