#!/bin/bash
# Build the halofit-fixed AxiCLASS copy WITHOUT installing it: the aegis env's classy (used by running fits) is untouched.
# Result: /home/syndyr/AxiCLASS_nlfix/python/build/lib*/classy*.so, loaded only by scripts that put it on sys.path.
set -e
ENV=/home/syndyr/micromamba/envs/aegis
export PATH="$ENV/bin:/usr/bin:/bin"
cd /home/syndyr/AxiCLASS_nlfix
make -j4 MDIR=/home/syndyr/AxiCLASS_nlfix libclass.a > /tmp/nlfix_make.log 2>&1 || { tail -30 /tmp/nlfix_make.log; exit 1; }
echo "libclass.a built"
cd python
rm -rf build
$ENV/bin/python setup.py build > /tmp/nlfix_setup.log 2>&1 || { tail -30 /tmp/nlfix_setup.log; exit 1; }
ls build/lib*/classy*.so
