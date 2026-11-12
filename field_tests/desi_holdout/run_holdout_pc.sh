#!/usr/bin/env bash
# PC (WSL): DESI-HOLDOUT Test A (field_tests/rules/PREREG_DESI_HOLDOUT.md). Waits for DATA-GEN, then the gate,
# the two holdout fits in parallel, the two predictions and the Test A score. Test B (mock) runs in the cloud after.
# Log: cmb-fit/results/holdout_log.txt
set -uo pipefail
T="$(cd "$(dirname "$0")" && pwd)"; AEG="$(dirname "$(dirname "$T")")"; R="$AEG/cmb-fit/results"; LOG="$R/holdout_log.txt"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
export COBAYA_PACKAGES_PATH="${COBAYA_PACKAGES_PATH:-$AEG/cmb-fit/packages}" TWIST_RESULTS="$R"
mkdir -p "$R/lanes"; say() { echo "$(date '+%F %T') $*" | tee -a "$LOG"; }
say "waiting for DATA-GEN to finish"
sleep 60
while pgrep -f "datagen_fit.py|run_datagen_pc.sh" >/dev/null; do sleep 600; done
cd "$T"
say "gate start"
for w in FLAG1 LCDM; do "$PY" desi_holdout.py predict $w stored >> "$LOG" 2>&1 || say "gate $w FAILED"; done
say "fits start"
for w in FLAG1 LCDM; do
  ( OMP_NUM_THREADS=2 nice -n 5 "$PY" desi_holdout.py fit $w > "$R/lanes/holdout_$w.log" 2>&1 \
      && say "fit $w done" || say "fit $w FAILED (see lanes/holdout_$w.log)" ) &
  sleep 20
done
wait
for w in FLAG1 LCDM; do "$PY" desi_holdout.py predict $w >> "$LOG" 2>&1 || say "predict $w FAILED"; done
"$PY" desi_holdout.py score >> "$LOG" 2>&1 && say "Test A scored" || say "Test A score FAILED"
