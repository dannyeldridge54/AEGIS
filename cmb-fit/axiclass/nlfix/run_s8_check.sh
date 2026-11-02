#!/bin/bash
# S8 on the corrected code: Late Twist + LCDM references on AxiCLASS_nlfix, then the Coupled Twist on its fixed build.
cd /mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass/nlfix
PY=/home/syndyr/micromamba/envs/aegis/bin/python
OMP_NUM_THREADS=2 $PY -W ignore s8_check.py ax_spa_latetwist_gF0.4m-0.3_nlfix ax_spa_latetwist_gF0m0.102_desy5_nlfix \
  ax_spa_lcdm_halofit ax_spa_lcdm_halofit_desy5 2>&1 | grep -E '^ax_spa|Error|Traceback' | tail -6
OMP_NUM_THREADS=2 $PY -W ignore s8_check.py ax_spa_coupledtwist_gF0.4m-0.1_nlfix 2>&1 | grep -E '^ax_spa|Error|Traceback' | tail -3
