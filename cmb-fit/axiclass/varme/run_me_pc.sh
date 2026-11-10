#!/usr/bin/env bash
# PC (WSL): TWIST-ME (field_tests/rules/PREREG_TWIST_ME.md). Gate G-ME-PC, then 3 fits. Log: cmb-fit/results/me_log.txt
set -uo pipefail
T="$(cd "$(dirname "$0")" && pwd)"; CF="$(dirname "$(dirname "$T")")"; R="$CF/results"; LOG="$R/me_log.txt"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
export TWIST_PY="$PY" COBAYA_PACKAGES_PATH="${COBAYA_PACKAGES_PATH:-$CF/packages}" TWIST_RESULTS="$R"
mkdir -p "$R/lanes"; say() { echo "$(date '+%F %T') $*" | tee -a "$LOG"; }
say "start"
if [ ! -f "$R/me_gate_pc.json" ] || ! grep -q '"all_pass": true' "$R/me_gate_pc.json"; then
  ( cd "$T" && OMP_NUM_THREADS=2 "$PY" me_fit.py gate_pc > "$R/lanes/me_gate_pc.log" 2>&1 ) \
    && say "G-ME-PC passed" || { say "G-ME-PC FAILED: no fits (see results/me_gate_pc.json)"; exit 1; }
fi
for n in ME ME_dovekie ME_union3; do
  [ -f "$R/cmp_$n.json" ] && continue
  say "fit $n start"
  ( cd "$T" && OMP_NUM_THREADS=2 nice -n 5 "$PY" me_fit.py "$n" > "$R/lanes/$n.log" 2>&1 \
      && say "fit $n done" || say "fit $n FAILED (see results/lanes/$n.log)" ) &
  sleep 15
done
wait; say "TWIST-ME fits finished"
