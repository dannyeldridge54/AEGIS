#!/bin/bash
# Run bug_reproducer.py on the installed AxiCLASS and on the fixed build; then the fixed build at smaller field masses
# (a harder-frozen field) to show the small remaining non-linear difference shrinks with m.
cd "$(dirname "$0")"
PY=/home/syndyr/micromamba/envs/aegis/bin/python
for b in AxiCLASS AxiCLASS_nlfix; do
  echo "== $b"
  OMP_NUM_THREADS=1 $PY -W ignore bug_reproducer.py /home/syndyr/$b/python/build 2>&1 | tail -5
done
