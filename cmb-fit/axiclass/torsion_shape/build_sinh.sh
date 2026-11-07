#!/bin/bash
# Build the Fingerprint AxiCLASS (FP, PREREGISTRATION_SINH.md): copy of the pinned base build + patch_sinh.py.
# Usage: bash build_sinh.sh     (uses TWIST_BUILDS, TWIST_PY like the other build scripts)
HERE="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
BLD="${TWIST_BUILDS:-$HOME}"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
set -e
ENV="${TWIST_ENV:-$(dirname "$(dirname "$PY")")}"
export PATH="$ENV/bin:/usr/bin:/bin"
[ -d "$BLD/AxiCLASS" ] || { echo "base build $BLD/AxiCLASS missing: run cmb-fit/environment/setup_twist_env.sh first"; exit 1; }
[ -d "$BLD/AxiCLASS_sinh" ] || cp -r "$BLD/AxiCLASS" "$BLD/AxiCLASS_sinh"
"$PY" "$HERE/patch_sinh.py" "$BLD/AxiCLASS_sinh"
cd "$BLD/AxiCLASS_sinh"
make -j4 MDIR="$BLD/AxiCLASS_sinh" libclass.a > /tmp/sinh_make.log 2>&1 || { tail -30 /tmp/sinh_make.log; exit 1; }
cd python && rm -rf build
"$PY" setup.py build > /tmp/sinh_setup.log 2>&1 || { tail -30 /tmp/sinh_setup.log; exit 1; }
ls build/lib*/classy*.so && echo "Fingerprint build ready. Next: $PY $HERE/regress_sinh.py"
