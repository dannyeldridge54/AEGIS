#!/bin/bash
# S8-A build: copy $BLD/AxiCLASS_coupled_nlfix_ula (untouched) to $BLD/AxiCLASS_coupled_nlfix_angle, apply patch_angle.py,
# build WITHOUT installing. Same pattern as nlfix/build_coupled_nlfix.sh.
AXI="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")"/.. && pwd)"
BLD="${TWIST_BUILDS:-$HOME}"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
set -e
ENV="${TWIST_ENV:-$(dirname "$(dirname "$PY")")}"
export PATH="$ENV/bin:/usr/bin:/bin"
SRC=$BLD/AxiCLASS_coupled_nlfix_ula
DST=$BLD/AxiCLASS_coupled_nlfix_angle
[ -d "$DST" ] || { cp -a "$SRC" "$DST"; "$PY" "$AXI/angle/patch_angle.py" "$DST"; }
rm -rf "$DST/python/build"
cd "$DST"
make -j4 MDIR="$DST" libclass.a > /tmp/angle_make.log 2>&1 || { tail -30 /tmp/angle_make.log; exit 1; }
echo "libclass.a built"
cd python
"$PY" setup.py build > /tmp/angle_setup.log 2>&1 || { tail -30 /tmp/angle_setup.log; exit 1; }
ls build/lib*/classy*.so
