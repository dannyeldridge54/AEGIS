#!/bin/bash
# B4-X switch numbers (R, z_on, b0) at the NR Late Twist best fits.
cd /mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass/nlfix
OMP_NUM_THREADS=2 /home/syndyr/micromamba/envs/aegis/bin/python -W ignore b4x_switch.py \
  ax_spa_latetwist_gF0.4m-0.3_nlfix ax_spa_latetwist_gF0m0.102_desy5_nlfix 2>&1 | grep -E '^ax_spa|Error|Traceback|Key' | tail -6
