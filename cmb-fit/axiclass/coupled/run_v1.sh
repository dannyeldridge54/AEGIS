#!/bin/bash
# Gate V1: beta = 0 must reproduce the original AxiCLASS chi2 at the same Late Twist point (to within 0.05).
P=/home/syndyr/micromamba/envs/aegis/bin/python
S=/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass/coupled/gates.py
cd /tmp
for w in original coupled; do
  OMP_NUM_THREADS=3 $P $S chi2 "$w" 0.0 2>&1 | grep '^{'
done
