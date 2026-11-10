#!/usr/bin/env bash
# PC (WSL): diagnosis of the failed G-TF-PC gate (no fit). Output: cmb-fit/results/tf_gate_diag.json
set -uo pipefail
T="$(cd "$(dirname "$0")" && pwd)"; CF="$(dirname "$(dirname "$T")")"; R="$CF/results"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
export TWIST_PY="$PY" COBAYA_PACKAGES_PATH="${COBAYA_PACKAGES_PATH:-$CF/packages}" TWIST_RESULTS="$R"
echo "$(date '+%F %T') gate diagnosis start" >> "$R/tf_log.txt"
( cd "$T" && OMP_NUM_THREADS=4 "$PY" tf_gate_diag.py > "$R/lanes/tf_gate_diag.log" 2>&1 )
echo "$(date '+%F %T') gate diagnosis done (results/tf_gate_diag.json)" >> "$R/tf_log.txt"
