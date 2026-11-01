#!/bin/bash
# Build the Coupled Twist AxiCLASS copy WITHOUT installing it: the aegis env's classy (used by running fits) is untouched.
# Result: /home/syndyr/AxiCLASS_coupled/python/build/lib*/classy*.so, loaded only by coupled runs via sys.path.
set -e
ENV=/home/syndyr/micromamba/envs/aegis
export PATH="$ENV/bin:/usr/bin:/bin"
cd /home/syndyr/AxiCLASS_coupled
make -j6 MDIR=/home/syndyr/AxiCLASS_coupled libclass.a > /tmp/coupled_make.log 2>&1 || { tail -30 /tmp/coupled_make.log; exit 1; }
echo "libclass.a built"
cd python
rm -rf build
$ENV/bin/python setup.py build > /tmp/coupled_setup.log 2>&1 || { tail -30 /tmp/coupled_setup.log; exit 1; }
ls build/lib*/classy*.so
