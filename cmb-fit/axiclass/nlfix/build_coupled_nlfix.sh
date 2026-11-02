#!/bin/bash
# B0 fix for the Coupled Twist build: copy $BLD/AxiCLASS_coupled (used by running fits; untouched) to
# $BLD/AxiCLASS_coupled_nlfix, apply patch_nlfix.py, and build WITHOUT installing.
# Portable paths (make_portable.py): override with TWIST_RESULTS, TWIST_BUILDS, TWIST_PY.
AXI="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")"/.. && pwd)"
RES="${TWIST_RESULTS:-$(dirname "$AXI")/results}"
BLD="${TWIST_BUILDS:-$HOME}"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
set -e
ENV="${TWIST_ENV:-$(dirname "$(dirname "$PY")")}"
export PATH="$ENV/bin:/usr/bin:/bin"
SRC=$BLD/AxiCLASS_coupled
DST=$BLD/AxiCLASS_coupled_nlfix
[ -d "$DST" ] || cp -a "$SRC" "$DST"
rm -rf "$DST/python/build"
$ENV/bin/python $AXI/nlfix/patch_nlfix.py "$DST"
cd "$DST"
make -j4 MDIR="$DST" libclass.a > /tmp/cnlfix_make.log 2>&1 || { tail -30 /tmp/cnlfix_make.log; exit 1; }
echo "libclass.a built"
cd python
$ENV/bin/python setup.py build > /tmp/cnlfix_setup.log 2>&1 || { tail -30 /tmp/cnlfix_setup.log; exit 1; }
ls build/lib*/classy*.so
