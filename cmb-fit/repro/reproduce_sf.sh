#!/usr/bin/env bash
# V8: one command from a clean Linux/WSL machine to the SF Pantheon+ Spiral - LCDM chi2 difference.
#   bash cmb-fit/repro/reproduce_sf.sh
# Step 1 builds the pinned environment, the AxiCLASS builds and downloads the public likelihood data
# (cmb-fit/environment/setup_twist_env.sh); step 2 evaluates both stored best points (repro_eval.py).
set -e
H="$(cd "$(dirname "$0")" && pwd)"
bash "$H/../environment/setup_twist_env.sh"
MM="$(command -v micromamba || command -v mamba || command -v conda)"
PY="$("$MM" run -n twist which python)"
TWIST_BUILDS="${TWIST_BUILDS:-$HOME}" COBAYA_PACKAGES_PATH="${COBAYA_PACKAGES_PATH:-$H/../packages}" "$PY" "$H/repro_eval.py"
