#!/bin/bash
# Install the ACT DR6 likelihoods into the 'aegis' env (same versions as the Windows venv) and run the P-ACT
# cross-engine check. Logged to cross_engine.log next to this file.
set -euo pipefail
HERE=/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass
exec > >(tee "$HERE/cross_engine.log") 2>&1
export MAMBA_ROOT_PREFIX="$HOME/micromamba"
eval "$("$HOME/bin/micromamba" shell hook -s bash)"
micromamba activate aegis
# Same sources and versions as the Windows venv (act_dr6_cmbonly from the ACT GitHub at the pinned commit).
pip install -q "git+https://github.com/ACTCollaboration/DR6-ACT-lite.git@627aeafb88ae5ad1aa66b406bea2d65cfa66a27d" \
               "act_dr6_lenslike==1.2.1"
export OMP_NUM_THREADS=1
python "$HERE/cross_engine_pact.py"
echo "=== $(date) done"
