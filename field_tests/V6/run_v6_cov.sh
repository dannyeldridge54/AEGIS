#!/usr/bin/env bash
# V6 restart with deviation V6-D1 (V6_DEVIATIONS.md, 9 Nov, on Danny's "Ok" to options a + c):
#  1. stop the first V6 chains (no starting proposal; ~71 s per CLASS call -> weeks) and their launcher loop;
#     the three FLAG-1 flagship fits are NOT touched;
#  2. Laplace step at the stored best fits (Pantheon+ first): evidence cross-check + starting proposal covariance;
#  3. restart the Pantheon+ chains (4 per model) with that proposal; Laplace for DES-Dovekie/Union3 once the flagship
#     fits finish; their chains follow the Pantheon+ ones. Log: cmb-fit/results/flagship_v6_log.txt
set -uo pipefail
V="$(cd "$(dirname "$0")" && pwd)"; ROOT="$(cd "$V/../.." && pwd)"; CF="$ROOT/cmb-fit"; R="$CF/results"
LOG="$R/flagship_v6_log.txt"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
export COBAYA_PACKAGES_PATH="${COBAYA_PACKAGES_PATH:-$CF/packages}" TWIST_RESULTS="$R"
say() { echo "$(date '+%F %T') $*" | tee -a "$LOG"; }
P0="$(pgrep -o -f run_flagship_v6.sh || true)"
[ -n "$P0" ] && kill "$P0" && say "V6-D1: stopped the first launcher loop (pid $P0); flagship fits keep running"
pkill -f "v6_chains.py" && say "V6-D1: stopped the first V6 chains (no proposal covariance)"
laplace() { ( cd "$V" && OMP_NUM_THREADS=1 nice -n 10 "$PY" v6_laplace.py "$1" "$2" > "$R/lanes/v6_laplace_$1.log" 2>&1 \
              && say "V6 Laplace $1 done" || say "V6 Laplace $1 FAILED (see results/lanes/v6_laplace_$1.log)" ); }
chains() {
  for run in "$@"; do for i in 1 2 3 4; do
    say "V6 chain $run c$i start (proposal covariance from Laplace step)"
    ( cd "$V" && OMP_NUM_THREADS=1 nice -n 10 "$PY" v6_chains.py "$run" "$i" > "$R/lanes/v6_${run}_cov_c$i.log" 2>&1 \
        && say "V6 chain $run c$i done" || say "V6 chain $run c$i STOPPED (see results/lanes/v6_${run}_cov_c$i.log)" ) &
    sleep 20
  done; done
}
say "V6 Laplace (Pantheon+) start"
laplace ax_spa_spiraltwist_nlfix 3 & laplace spiralL 3 & laplace ax_spa_lcdm_halofit 3 & wait
chains ax_spa_spiraltwist_nlfix spiralL ax_spa_lcdm_halofit
CH=$(jobs -p)
until [ -f "$R/cmp_ax_spa_spiraltwist_kappa1_nlfix_s8y6.json" ] && [ -f "$R/cmp_ax_spa_spiraltwist_kappa1_dovekie_nlfix_s8y6.json" ] \
      && [ -f "$R/cmp_ax_spa_spiraltwist_kappa1_union3_nlfix_s8y6.json" ]; do sleep 300; done
say "flagship fits finished; V6 Laplace for DES-Dovekie and Union3"
for r in ax_spa_spiraltwist_dovekie_nlfix spiralL_dovekie ax_spa_lcdm_halofit_dovekie \
         ax_spa_spiraltwist_union3_nlfix spiralL_union3 ax_spa_lcdm_halofit_union3; do laplace "$r" 5; done
say "V6 Laplace finished (all 9); waiting for the Pantheon+ chains"
wait $CH
chains ax_spa_spiraltwist_dovekie_nlfix spiralL_dovekie ax_spa_lcdm_halofit_dovekie; wait
chains ax_spa_spiraltwist_union3_nlfix spiralL_union3 ax_spa_lcdm_halofit_union3; wait
say "V6 all chains finished"
