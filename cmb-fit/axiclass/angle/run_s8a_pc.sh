#!/usr/bin/env bash
# PC (WSL): S8-A (field_tests/rules/PREREG_S8A_ANGLE.md). Build the angle engine, run the cloud gates again on the PC
# build, gate G-A-PC, then the 3 fits. Log: cmb-fit/results/s8a_log.txt. Safe to rerun (skips finished steps).
set -uo pipefail
A="$(cd "$(dirname "$0")" && pwd)"; AXI="$(dirname "$A")"; CF="$(dirname "$AXI")"; R="$CF/results"; LOG="$R/s8a_log.txt"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
export TWIST_PY="$PY" COBAYA_PACKAGES_PATH="${COBAYA_PACKAGES_PATH:-$CF/packages}" TWIST_RESULTS="$R"
BLD="${TWIST_BUILDS:-$HOME}"; mkdir -p "$R/lanes"; say() { echo "$(date '+%F %T') $*" | tee -a "$LOG"; }
say "start"
if ! ls "$BLD"/AxiCLASS_coupled_nlfix_angle/python/build/lib*/classy*.so >/dev/null 2>&1; then
  bash "$A/build_angle.sh" >> "$LOG" 2>&1 && say "angle build done" || { say "angle build FAILED"; exit 1; }
fi
( cd "$A" && "$PY" angle_gates.py > "$R/lanes/s8a_engine_gates_pc.log" 2>&1 ) && cp "$A/angle_gates.json" "$R/angle_gates_pc.json" \
  && say "engine gates rerun on the PC build (results/angle_gates_pc.json)" || say "engine gates on PC FAILED to run (see lanes/s8a_engine_gates_pc.log)"
( cd "$A" && OMP_NUM_THREADS=2 "$PY" angle_fit.py gate_pc > "$R/lanes/s8a_gate_pc.log" 2>&1 ) \
  && say "G-A-PC passed" || { say "G-A-PC FAILED: no fits (see results/s8a_gate_pc.json)"; exit 1; }
for n in S8A S8A_dovekie S8A_union3; do
  [ -f "$R/cmp_$n.json" ] && continue
  say "fit $n start"
  ( cd "$A" && OMP_NUM_THREADS=2 nice -n 5 "$PY" angle_fit.py "$n" > "$R/lanes/$n.log" 2>&1 \
      && say "fit $n done" || say "fit $n FAILED (see results/lanes/$n.log)" ) &
  sleep 15
done
wait; say "S8-A finished"
