#!/usr/bin/env bash
# WSL, PC: S8J-D3, two extra restarts for each LCDM+S8 reference. Log: cmb-fit/results/s8j_more_pc_log.txt
set -uo pipefail
J="$(cd "$(dirname "$0")" && pwd)"; ROOT="$(cd "$J/../../.." && pwd)"; CF="$ROOT/cmb-fit"; R="$CF/results"
LOG="$R/s8j_more_pc_log.txt"; PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
export COBAYA_PACKAGES_PATH="${COBAYA_PACKAGES_PATH:-$CF/packages}" TWIST_RESULTS="$R"
say() { echo "$(date '+%F %T') $*" | tee -a "$LOG"; }
for b in ax_spa_lcdm_halofit ax_spa_lcdm_halofit_dovekie ax_spa_lcdm_halofit_union3; do
  n="${b}_s8y6"; [ -f "$R/cmp_${n}_more.json" ] && continue
  say "S8-J extra restarts $n start"
  ( cd "$J" && OMP_NUM_THREADS=2 nice -n 5 "$PY" s8_joint_fit.py more "$n" > "$R/lanes/${n}_more.log" 2>&1 \
      && say "S8-J extra restarts $n done" || say "S8-J extra restarts $n FAILED" ) &
  sleep 15
done
wait; say "S8-J extra restarts finished"
