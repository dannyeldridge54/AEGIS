#!/usr/bin/env bash
# PC (WSL): DESI-MOCK-CMB (field_tests/rules/PREREG_DESI_MOCK_CMB.md). Waits for the FLAG-1 MCMC to finish, then
# truth -> gate G-MC -> 4 fits (LCDM/W0WA x SN/noSN) -> score. Log: cmb-fit/results/mock_cmb_log.txt
set -uo pipefail
T="$(cd "$(dirname "$0")" && pwd)"; AEG="$(dirname "$(dirname "$T")")"; R="$AEG/cmb-fit/results"; LOG="$R/mock_cmb_log.txt"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
export TWIST_PY="$PY" COBAYA_PACKAGES_PATH="${COBAYA_PACKAGES_PATH:-$AEG/cmb-fit/packages}" TWIST_RESULTS="$R"
mkdir -p "$R/lanes" "$R/chains"; say() { echo "$(date '+%F %T') $*" | tee -a "$LOG"; }
say "waiting for the FLAG-1 MCMC to finish"
while pgrep -f flag_mcmc.py >/dev/null; do sleep 600; done
say "MCMC done; DESI-MOCK-CMB start"
cd "$T"
if [ ! -f mock_cmb_truth.npz ]; then
  OMP_NUM_THREADS=4 "$PY" desi_mock_cmb.py truth > "$R/lanes/mock_cmb_truth.log" 2>&1 \
    && say "truth written" || { say "truth FAILED (see lanes/mock_cmb_truth.log)"; exit 1; }
fi
OMP_NUM_THREADS=4 "$PY" desi_mock_cmb.py gate > "$R/lanes/mock_cmb_gate.log" 2>&1 \
  && say "G-MC passed" || { say "G-MC FAILED: no fits (see field_tests/desi_mock/mock_cmb_gate.json)"; exit 1; }
for m in LCDM W0WA; do for c in SN noSN; do
  [ -f "mock_cmb_part_${m}_${c}.json" ] && continue
  say "fit $m $c start"
  ( OMP_NUM_THREADS=2 nice -n 5 "$PY" desi_mock_cmb.py fit $m $c > "$R/lanes/mock_cmb_${m}_${c}.log" 2>&1 \
      && say "fit $m $c done" || say "fit $m $c FAILED (see lanes/mock_cmb_${m}_${c}.log)" ) &
  sleep 20
done; done
wait
"$PY" desi_mock_cmb.py score >> "$LOG" 2>&1; say "DESI-MOCK-CMB finished"
