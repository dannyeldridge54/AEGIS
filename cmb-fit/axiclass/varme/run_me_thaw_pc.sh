#!/usr/bin/env bash
# PC (WSL): physical-version check after the TWIST-ME fits (no fit). Output: cmb-fit/results/me_thaw_check.json
set -uo pipefail
T="$(cd "$(dirname "$0")" && pwd)"; CF="$(dirname "$(dirname "$T")")"; R="$CF/results"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
export COBAYA_PACKAGES_PATH="${COBAYA_PACKAGES_PATH:-$CF/packages}" TWIST_RESULTS="$R"
# waits for the TWIST-ME fits to finish, so it can be started any time
until grep -q "TWIST-ME fits finished" "$R/me_log.txt" 2>/dev/null; do sleep 120; done
echo "$(date '+%F %T') thaw check start" >> "$R/me_log.txt"
( cd "$T" && OMP_NUM_THREADS=4 "$PY" me_thaw_check.py > "$R/lanes/me_thaw_check.log" 2>&1 )
echo "$(date '+%F %T') thaw check done (results/me_thaw_check.json)" >> "$R/me_log.txt"
