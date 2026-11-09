#!/usr/bin/env bash
# WSL, on the PC (9 Nov): FLAG-1 flagship fits (3, 2 threads each) and V6 chains (Pantheon+ first: Spiral, S8-L, LCDM,
# 4 chains each, 1 thread each). Dovekie and Union3 chains start when the Pantheon+ ones finish ("if time allows").
# Logs: cmb-fit/results/flagship_v6_log.txt, per-job logs in cmb-fit/results/lanes/. Safe to rerun (resumes).
set -uo pipefail
V="$(cd "$(dirname "$0")" && pwd)"; ROOT="$(cd "$V/../.." && pwd)"; CF="$ROOT/cmb-fit"; R="$CF/results"
J="$ROOT/field_tests/S8_WL/joint"; LOG="$R/flagship_v6_log.txt"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
export COBAYA_PACKAGES_PATH="${COBAYA_PACKAGES_PATH:-$CF/packages}" TWIST_RESULTS="$R"
mkdir -p "$R/lanes"; say() { echo "$(date '+%F %T') $*" | tee -a "$LOG"; }
say "start (cores: $(nproc))"
for s in "" _dovekie _union3; do
  n="ax_spa_spiraltwist_kappa1${s}_nlfix_s8y6"; [ -f "$R/cmp_$n.json" ] && continue
  say "FLAG-1 fit $n start"
  ( cd "$J" && OMP_NUM_THREADS=2 nice -n 5 "$PY" flagship_fit.py "$n" > "$R/lanes/$n.log" 2>&1 \
      && say "FLAG-1 fit $n done" || say "FLAG-1 fit $n FAILED (see results/lanes/$n.log)" ) &
  sleep 15
done
chains() {
  for run in "$@"; do for i in 1 2 3 4; do
    say "V6 chain $run c$i start"
    ( cd "$V" && OMP_NUM_THREADS=1 nice -n 10 "$PY" v6_chains.py "$run" "$i" > "$R/lanes/v6_${run}_c$i.log" 2>&1 \
        && say "V6 chain $run c$i done" || say "V6 chain $run c$i STOPPED (see results/lanes/v6_${run}_c$i.log)" ) &
    sleep 20
  done; done
  wait
}
chains ax_spa_spiraltwist_nlfix spiralL ax_spa_lcdm_halofit
say "V6 Pantheon+ chains finished; starting DES-Dovekie and Union3"
chains ax_spa_spiraltwist_dovekie_nlfix spiralL_dovekie ax_spa_lcdm_halofit_dovekie
chains ax_spa_spiraltwist_union3_nlfix spiralL_union3 ax_spa_lcdm_halofit_union3
say "all finished"
