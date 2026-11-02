#!/bin/bash
# Gate N0 for the nlfix replication: validate both fixed builds through early_late_spa's own switch.
cd /mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass/nlfix
for k in latetwist coupled; do
  OMP_NUM_THREADS=2 /home/syndyr/micromamba/envs/aegis/bin/python -W ignore validate_nlfix_builds.py "$k" 2>&1 | grep -E 'N0|Error' | tail -3
done
