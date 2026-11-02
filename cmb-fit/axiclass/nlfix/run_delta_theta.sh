#!/bin/bash
# B4 input: delta_theta at the NR (corrected-code) Late Twist best fits (Pantheon+ grid best, DES Y5 official best).
cd /mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass/nlfix
OMP_NUM_THREADS=2 /home/syndyr/micromamba/envs/aegis/bin/python -W ignore delta_theta.py \
  ax_spa_latetwist_gF0.4m-0.3_nlfix ax_spa_latetwist_gF0m0.102_desy5_nlfix 2>&1 | grep -E 'delta_theta|Error|Traceback|Key' | tail -6
