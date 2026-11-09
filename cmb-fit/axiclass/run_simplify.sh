#!/usr/bin/env bash
# WSL, on the PC: SIMPLIFY-L (field_tests/rules/PREREG_SIMPLIFY_LATE.md). Waits for bracket round 3 (3 result files) and
# for the lock file, then runs the 6 fixed-kappa Spiral fits. Log: cmb-fit/results/simplify_log.txt
set -uo pipefail
A="$(cd "$(dirname "$0")" && pwd)"; ROOT="$(cd "$A/../.." && pwd)"; R="$ROOT/cmb-fit/results"; LOG="$R/simplify_log.txt"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
export COBAYA_PACKAGES_PATH="${COBAYA_PACKAGES_PATH:-$ROOT/cmb-fit/packages}" TWIST_RESULTS="$R"
mkdir -p "$R/lanes"; say() { echo "$(date '+%F %T') $*" | tee -a "$LOG"; }
say "waiting for bracket round 3 and the lock"
until [ -f "$R/cmp_pact_edelock_th2.777_F9_deep.json" ] && [ -f "$R/cmp_edelockP_s8A_th2.777_F9_deep.json" ] \
      && [ -f "$R/cmp_edelockP_s8B_th2.777_F9_deep.json" ] && [ -f "$ROOT/field_tests/rules/PREREG_SIMPLIFY_LATE.md.sha256" ]; do sleep 120; done
say "start"
for k in 0.8165 1; do for s in "" _dovekie _union3; do
  n="ax_spa_spiraltwist_kappa${k}${s}_nlfix"; [ -f "$R/cmp_$n.json" ] && continue
  say "fit $n start"
  ( cd "$A" && OMP_NUM_THREADS=2 nice -n 5 "$PY" early_late_spa.py "$n" > "$R/lanes/$n.log" 2>&1 \
      && say "fit $n done" || say "fit $n FAILED (see results/lanes/$n.log)" ) &
  sleep 15
done; done
wait; say "SIMPLIFY-L finished"
