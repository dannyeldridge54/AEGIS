#!/usr/bin/env bash
# PC (WSL): SPA-CHAIN (field_tests/rules/PREREG_SPA_CHAIN.md). Two MCMC chains in parallel, resumable.
T="$(cd "$(dirname "$0")" && pwd)"; AEG="$(dirname "$(dirname "$T")")"; R="$AEG/cmb-fit/results"; LOG="$R/spa_chain_log.txt"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
export COBAYA_PACKAGES_PATH="${COBAYA_PACKAGES_PATH:-$AEG/cmb-fit/packages}" TWIST_RESULTS="$R"
cd "$T"; mkdir -p "$R/lanes"
for m in PURE LCDM; do
  ( OMP_NUM_THREADS=2 nice -n 5 "$PY" spa_chain.py $m > "$R/lanes/spa_chain_$m.log" 2>&1; echo "$(date '+%F %T') chain $m exit $?" >> "$LOG" ) &
done
wait; echo "$(date '+%F %T') SPA-CHAIN both chains finished" >> "$LOG"
