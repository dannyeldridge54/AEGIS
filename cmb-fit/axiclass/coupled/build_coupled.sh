#!/bin/bash
# Build the Coupled Twist AxiCLASS copy WITHOUT installing it: the aegis env's classy (used by running fits) is untouched.
# Result: $BLD/AxiCLASS_coupled/python/build/lib*/classy*.so, loaded only by coupled runs via sys.path.
# Portable paths (make_portable.py): override with TWIST_RESULTS, TWIST_BUILDS, TWIST_PY.
AXI="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")"/.. && pwd)"
RES="${TWIST_RESULTS:-$(dirname "$AXI")/results}"
BLD="${TWIST_BUILDS:-$HOME}"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
set -e
ENV="${TWIST_ENV:-$(dirname "$(dirname "$PY")")}"
export PATH="$ENV/bin:/usr/bin:/bin"
cd $BLD/AxiCLASS_coupled
make -j6 MDIR=$BLD/AxiCLASS_coupled libclass.a > /tmp/coupled_make.log 2>&1 || { tail -30 /tmp/coupled_make.log; exit 1; }
echo "libclass.a built"
cd python
rm -rf build
$ENV/bin/python setup.py build > /tmp/coupled_setup.log 2>&1 || { tail -30 /tmp/coupled_setup.log; exit 1; }
ls build/lib*/classy*.so
