#!/usr/bin/env bash
# PC (WSL): JOINT-SHEAR fits (field_tests/rules/PREREG_JOINT_SHEAR.md) once the cloud calibration passed G-JS
# (js_calib.json committed). Gate G-JS-PC, then 6 fits (S8-A and LCDM x 3 SN sets). Log: cmb-fit/results/js_log.txt.
# Safe to rerun (skips finished fits).
set -uo pipefail
J="$(cd "$(dirname "$0")" && pwd)"; ROOT="$(cd "$J/../../.." && pwd)"; CF="$ROOT/cmb-fit"; R="$CF/results"; LOG="$R/js_log.txt"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
export COBAYA_PACKAGES_PATH="${COBAYA_PACKAGES_PATH:-$CF/packages}" TWIST_RESULTS="$R"
mkdir -p "$R/lanes"; say() { echo "$(date '+%F %T') $*" | tee -a "$LOG"; }
say "start"
( cd "$J" && OMP_NUM_THREADS=2 "$PY" js_fit.py gate_pc > "$R/lanes/js_gate_pc.log" 2>&1 ) \
  && say "G-JS-PC passed" || { say "G-JS-PC FAILED: no fits (see results/js_gate_pc.json, lanes/js_gate_pc.log)"; exit 1; }
for n in S8A ax_spa_lcdm_halofit S8A_dovekie ax_spa_lcdm_halofit_dovekie S8A_union3 ax_spa_lcdm_halofit_union3; do
  [ -f "$R/cmp_${n}__jsfit.json" ] && continue
  say "fit $n start"
  ( cd "$J" && OMP_NUM_THREADS=2 nice -n 5 "$PY" js_fit.py "$n" > "$R/lanes/js_$n.log" 2>&1 \
      && say "fit $n done" || say "fit $n FAILED (see results/lanes/js_$n.log)" ) &
  sleep 15
done
wait; say "JOINT-SHEAR fits finished"
