#!/bin/bash
# Portable paths (make_portable.py): override with TWIST_RESULTS, TWIST_BUILDS, TWIST_PY.
AXI="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
RES="${TWIST_RESULTS:-$(dirname "$AXI")/results}"
BLD="${TWIST_BUILDS:-$HOME}"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
set -euo pipefail
HERE=$AXI
exec > >(tee "$HERE/debug_ede.log") 2>&1
export MAMBA_ROOT_PREFIX="$HOME/micromamba"
eval "$("$HOME/bin/micromamba" shell hook -s bash)"
micromamba activate aegis
export OMP_NUM_THREADS=1
python "$HERE/debug_ede.py"
echo "=== done"
