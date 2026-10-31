#!/bin/bash
set -euo pipefail
HERE=/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass
exec > >(tee "$HERE/debug_ede.log") 2>&1
export MAMBA_ROOT_PREFIX="$HOME/micromamba"
eval "$("$HOME/bin/micromamba" shell hook -s bash)"
micromamba activate aegis
export OMP_NUM_THREADS=1
python "$HERE/debug_ede.py"
echo "=== done"
