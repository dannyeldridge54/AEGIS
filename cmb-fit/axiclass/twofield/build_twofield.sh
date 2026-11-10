#!/bin/bash
# Two-field build (route 1): copy $BLD/AxiCLASS_coupled_nlfix (untouched) to $BLD/AxiCLASS_twofield, apply patch_twofield.py,
# build WITHOUT installing. Same pattern as nlfix/build_coupled_nlfix.sh.
AXI="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")"/.. && pwd)"
BLD="${TWIST_BUILDS:-$HOME}"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
set -e
ENV="${TWIST_ENV:-$(dirname "$(dirname "$PY")")}"
export PATH="$ENV/bin:/usr/bin:/bin"
SRC=$BLD/AxiCLASS_coupled_nlfix
DST=$BLD/AxiCLASS_twofield
[ -d "$DST" ] || { cp -a "$SRC" "$DST"; "$PY" "$AXI/twofield/patch_twofield.py" "$DST"; }
# a build made before the HALOFIT fix (TWOFIELD_DEVIATIONS.md, D1) gets only that fix
grep -q "two-field: the dilaton is dark energy" "$DST/external/Halofit/halofit.c" || "$PY" "$AXI/twofield/patch_twofield.py" "$DST" --halofit-only
rm -rf "$DST/python/build"
cd "$DST"
make -j4 MDIR="$DST" libclass.a > /tmp/twofield_make.log 2>&1 || { tail -30 /tmp/twofield_make.log; exit 1; }
echo "libclass.a built"
cd python
"$PY" setup.py build > /tmp/twofield_setup.log 2>&1 || { tail -30 /tmp/twofield_setup.log; exit 1; }
ls build/lib*/classy*.so
