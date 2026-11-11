#!/usr/bin/env bash
# PC (WSL): FLAG-1 MCMC, 4 independent chains x 2 threads (resumes if restarted). Log: cmb-fit/results/mcmc_log.txt
set -uo pipefail
T="$(cd "$(dirname "$0")" && pwd)"; CF="$(dirname "$(dirname "$T")")"; R="$CF/results"; LOG="$R/mcmc_log.txt"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
export COBAYA_PACKAGES_PATH="${COBAYA_PACKAGES_PATH:-$CF/packages}" TWIST_RESULTS="$R"
mkdir -p "$R/lanes" "$R/chains"; say() { echo "$(date '+%F %T') $*" | tee -a "$LOG"; }
say "FLAG-1 MCMC start (4 chains)"
for i in 1 2 3 4; do
  ( cd "$T" && OMP_NUM_THREADS=2 nice -n 5 "$PY" flag_mcmc.py $i > "$R/lanes/FLAG1_mcmc_c$i.log" 2>&1 \
      && say "chain $i done" || say "chain $i stopped (see lanes/FLAG1_mcmc_c$i.log)" ) &
  sleep 20
done
wait; say "FLAG-1 MCMC finished"
