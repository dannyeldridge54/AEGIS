#!/usr/bin/env bash
# PC (WSL): two-field Twist (field_tests/rules/PREREG_TWOFIELD.md). Build AxiCLASS_twofield, gate G-TF-PC, then 3 fits.
# Log: cmb-fit/results/tf_log.txt. Safe to rerun (skips finished steps). The fit code refuses to run before the lock.
set -uo pipefail
T="$(cd "$(dirname "$0")" && pwd)"; AXI="$(dirname "$T")"; CF="$(dirname "$AXI")"; R="$CF/results"; LOG="$R/tf_log.txt"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
export TWIST_PY="$PY" COBAYA_PACKAGES_PATH="${COBAYA_PACKAGES_PATH:-$CF/packages}" TWIST_RESULTS="$R"
BLD="${TWIST_BUILDS:-$HOME}"; mkdir -p "$R/lanes"; say() { echo "$(date '+%F %T') $*" | tee -a "$LOG"; }
say "start"
if ! ls "$BLD"/AxiCLASS_twofield/python/build/lib*/classy*.so >/dev/null 2>&1; then
  bash "$T/build_twofield.sh" >> "$LOG" 2>&1 && say "two-field build done" || { say "two-field build FAILED"; exit 1; }
fi
( cd "$T" && OMP_NUM_THREADS=2 "$PY" twofield_fit.py gate_pc > "$R/lanes/tf_gate_pc.log" 2>&1 ) \
  && say "G-TF-PC passed" || { say "G-TF-PC FAILED: no fits (see results/tf_gate_pc.json)"; exit 1; }
for n in TF TF_dovekie TF_union3; do
  [ -f "$R/cmp_$n.json" ] && continue
  say "fit $n start"
  ( cd "$T" && OMP_NUM_THREADS=2 nice -n 5 "$PY" twofield_fit.py "$n" > "$R/lanes/$n.log" 2>&1 \
      && say "fit $n done" || say "fit $n FAILED (see results/lanes/$n.log)" ) &
  sleep 15
done
wait; say "two-field fits finished"
