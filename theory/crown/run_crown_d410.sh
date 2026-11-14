#!/usr/bin/env bash
# PC (WSL): D410 crown fits (field_tests/rules/PREREG_D410_CROWN.md). Two fits in parallel, then score.
set -uo pipefail
A="$(cd "$(dirname "$0")" && pwd)"; AEG="$(dirname "$(dirname "$A")")"; R="$AEG/cmb-fit/results"; LOG="$R/d410_log.txt"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
export COBAYA_PACKAGES_PATH="${COBAYA_PACKAGES_PATH:-$AEG/cmb-fit/packages}" TWIST_RESULTS="$R"
say() { echo "$(date '+%F %T') $*" | tee -a "$LOG"; }
[ -f "$AEG/field_tests/rules/PREREG_D410_CROWN.md.sha256" ] || { say "rule not locked"; exit 1; }
mkdir -p "$R/lanes"; cd "$A"; say "D410 start"
for j in THAW_FREE THAW_TWIST; do
  ( OMP_NUM_THREADS=4 nice -n 5 "$PY" crown_d410.py fit $j > "$R/lanes/d410_${j}.log" 2>&1 && say "fit $j done" || say "fit $j FAILED" ) &
  sleep 20
done
wait
"$PY" crown_d410.py score >> "$LOG" 2>&1 && say "D410 scored" || say "D410 score FAILED"
say "D410 all done"
