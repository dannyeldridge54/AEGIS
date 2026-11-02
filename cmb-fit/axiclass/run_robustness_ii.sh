#!/bin/bash
# CubeMind PREREGISTRATION_ROBUSTNESS_II.md (locked 2026-11-02 12:35:12): B2 BAO dissection + R3 cold restarts.
# 8 fits at 2 threads each. (Not run_robustness2.sh, which is the October R1/R2 batch.)
R=/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/results
A=/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass
PY=/home/syndyr/micromamba/envs/aegis/bin/python
RUNS="ax_spa_lcdm_halofit_desy5_nobao ax_spa_latetwist_gF0m0.102_desy5_nobao_nlfix ax_spa_w0wa_halofit_desy5_nobao
ax_spa_lcdm_halofit_nobao ax_spa_coupledtwist_gF0.4m-0.1_nobao_nlfix ax_spa_w0wa_halofit_nobao
ax_spa_latetwist_gF0m0.102_desy5_nlfix_r4 ax_spa_coupledtwist_gF0.4m-0.1_nlfix_r4"
for n in $RUNS; do
  [ -f "$R/cmp_$n.json" ] && continue            # early_late_spa.py makes its own atomic .claim
  echo "$(date '+%F %T') RII start $n"
  ( OMP_NUM_THREADS=2 nice -n 5 $PY $A/early_late_spa.py "$n" > "$R/lanes/$n.log" 2>&1; echo "$(date '+%F %T') RII done $n" ) &
  sleep 15
done
wait
echo "$(date '+%F %T') robustness II finished"
