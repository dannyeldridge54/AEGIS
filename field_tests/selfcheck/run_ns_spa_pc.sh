#!/usr/bin/env bash
# PC (WSL): NS-SPA (field_tests/rules/PREREG_NS_SPA.md). Gate, three fits, score.
set -uo pipefail
T="$(cd "$(dirname "$0")" && pwd)"; AEG="$(dirname "$(dirname "$T")")"; R="$AEG/cmb-fit/results"; LOG="$R/ns_spa_log.txt"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
export COBAYA_PACKAGES_PATH="${COBAYA_PACKAGES_PATH:-$AEG/cmb-fit/packages}" TWIST_RESULTS="$R"
say() { echo "$(date '+%F %T') $*" | tee -a "$LOG"; }
[ -f "$AEG/field_tests/rules/PREREG_NS_SPA.md.sha256" ] || { say "rule not locked"; exit 1; }
cd "$T"
"$PY" ns_spa_fit.py gate >> "$LOG" 2>&1 || { say "gate FAILED: NO VERDICT"; exit 1; }
say "gate passed"
for j in PURE_FREE PURE_FIXED LCDM_FIXED; do
  OMP_NUM_THREADS=4 nice -n 5 "$PY" ns_spa_fit.py fit $j > "$R/lanes/ns_spa_${j}.log" 2>&1 && say "fit $j done" || say "fit $j FAILED"
done
"$PY" ns_spa_fit.py score >> "$LOG" 2>&1 && say "NS-SPA scored" || say "NS-SPA score FAILED"
