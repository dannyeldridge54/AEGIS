#!/bin/bash
# w0-wa (CPL) mapping of the official best Late Twist grid points (Pantheon+ and DES Y5).
cd /mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass
for n in "$@"; do
  echo "== $n"
  OMP_NUM_THREADS=2 timeout 900 /home/syndyr/micromamba/envs/aegis/bin/python -W ignore latetwist_cpl.py "$n" 2>&1 | grep -v -i -E 'warn|jaxlib|cuda' | tail -6
done
