#!/bin/bash
# C4 / true Omega_m / S8 for a Coupled Twist run (CubeMind PREREGISTRATION_COUPLED_TWIST.md).
cd /mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass/coupled
OMP_NUM_THREADS=2 timeout 1200 /home/syndyr/micromamba/envs/aegis/bin/python -W ignore coupled_weff.py "$1" 2>&1 | grep -v -i -E 'warn|jaxlib|cuda' | tail -25
