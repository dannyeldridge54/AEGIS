#!/usr/bin/env bash
# WSL, on the PC: S8-J (field_tests/rules/PREREG_S8_JOINT.md, locked 8 Nov). Gate G-J first (evaluation only); the six
# fits start only if it passes. Log: cmb-fit/results/s8j_pc_log.txt. Each fit 2 threads; 6 fits = 12 cores.
set -uo pipefail
J="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$J/../../.." && pwd)"
CF="$ROOT/cmb-fit"; R="$CF/results"; LOG="$R/s8j_pc_log.txt"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
export COBAYA_PACKAGES_PATH="${COBAYA_PACKAGES_PATH:-$CF/packages}" TWIST_RESULTS="$R"
mkdir -p "$R/lanes"
say() { echo "$(date '+%F %T') $*" | tee -a "$LOG"; }
[ -f "$ROOT/field_tests/rules/PREREG_S8_JOINT.md.sha256" ] || { say "rule not locked: nothing runs"; exit 1; }
say "S8-J gate G-J start (python $PY)"
RUNS="ax_spa_spiraltwist_nlfix ax_spa_spiraltwist_dovekie_nlfix ax_spa_spiraltwist_union3_nlfix ax_spa_lcdm_halofit ax_spa_lcdm_halofit_dovekie ax_spa_lcdm_halofit_union3"
for r in $RUNS; do   # one process per run (S8J-D2)
  (cd "$J" && OMP_NUM_THREADS=4 "$PY" s8_joint_fit.py gate_pc "$r") >> "$LOG" 2>&1 || say "gate run $r FAILED (see log)"
done
(cd "$J" && "$PY" s8_joint_fit.py gate_sum) >> "$LOG" 2>&1
"$PY" -c "import json,sys; sys.exit(0 if json.load(open('$R/s8j_gate_pc.json'))['all_pass'] else 1)" \
  || { say "gate G-J FAILED: no fits (results/s8j_gate_pc.json)"; exit 1; }
say "gate G-J passed"
for b in ax_spa_spiraltwist_nlfix ax_spa_spiraltwist_dovekie_nlfix ax_spa_spiraltwist_union3_nlfix \
         ax_spa_lcdm_halofit ax_spa_lcdm_halofit_dovekie ax_spa_lcdm_halofit_union3; do
  n="${b}_s8y6"
  [ -f "$R/cmp_$n.json" ] && continue
  say "S8-J fit $n start"
  ( cd "$J" && OMP_NUM_THREADS=2 nice -n 5 "$PY" s8_joint_fit.py "$n" > "$R/lanes/$n.log" 2>&1 \
      && say "S8-J fit $n done" || say "S8-J fit $n FAILED (see results/lanes/$n.log)" ) &
  sleep 15
done
wait
say "S8-J finished"
