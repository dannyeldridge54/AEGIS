#!/bin/bash
# B0 fix for the Coupled Twist build: copy /home/syndyr/AxiCLASS_coupled (used by running fits; untouched) to
# /home/syndyr/AxiCLASS_coupled_nlfix, apply patch_nlfix.py, and build WITHOUT installing.
set -e
ENV=/home/syndyr/micromamba/envs/aegis
export PATH="$ENV/bin:/usr/bin:/bin"
SRC=/home/syndyr/AxiCLASS_coupled
DST=/home/syndyr/AxiCLASS_coupled_nlfix
[ -d "$DST" ] || cp -a "$SRC" "$DST"
rm -rf "$DST/python/build"
$ENV/bin/python /mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass/nlfix/patch_nlfix.py "$DST"
cd "$DST"
make -j4 MDIR="$DST" libclass.a > /tmp/cnlfix_make.log 2>&1 || { tail -30 /tmp/cnlfix_make.log; exit 1; }
echo "libclass.a built"
cd python
$ENV/bin/python setup.py build > /tmp/cnlfix_setup.log 2>&1 || { tail -30 /tmp/cnlfix_setup.log; exit 1; }
ls build/lib*/classy*.so
