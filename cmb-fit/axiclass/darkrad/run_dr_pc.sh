#!/usr/bin/env bash
# PC (WSL): TWIST-DR (field_tests/rules/PREREG_TWIST_DR.md). Gate G-DR-PC, then 3 fits. Log: cmb-fit/results/dr_log.txt
set -uo pipefail
T="$(cd "$(dirname "$0")" && pwd)"; CF="$(dirname "$(dirname "$T")")"; R="$CF/results"; LOG="$R/dr_log.txt"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
export TWIST_PY="$PY" COBAYA_PACKAGES_PATH="${COBAYA_PACKAGES_PATH:-$CF/packages}" TWIST_RESULTS="$R"
mkdir -p "$R/lanes"; say() { echo "$(date '+%F %T') $*" | tee -a "$LOG"; }
say "start"
if [ ! -f "$R/dr_gate_pc.json" ] || ! grep -q '"all_pass": true' "$R/dr_gate_pc.json"; then
  ( cd "$T" && OMP_NUM_THREADS=2 "$PY" dr_fit.py gate_pc > "$R/lanes/dr_gate_pc.log" 2>&1 ) \
    && say "G-DR-PC passed" || { say "G-DR-PC FAILED: no fits (see results/dr_gate_pc.json)"; exit 1; }
fi
for n in DR DR_dovekie DR_union3; do
  [ -f "$R/cmp_$n.json" ] && continue
  say "fit $n start"
  ( cd "$T" && OMP_NUM_THREADS=2 nice -n 5 "$PY" dr_fit.py "$n" > "$R/lanes/$n.log" 2>&1 \
      && say "fit $n done" || say "fit $n FAILED (see results/lanes/$n.log)" ) &
  sleep 15
done
wait; say "TWIST-DR fits finished"
