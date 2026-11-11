#!/usr/bin/env bash
# PC (WSL): SELFCHECK V2. Waits until the DESI-MOCK-CMB fits have finished, then the two no-SN fits in parallel.
# Log: cmb-fit/results/selfcheck_v2_log.txt
set -uo pipefail
T="$(cd "$(dirname "$0")" && pwd)"; AEG="$(dirname "$(dirname "$T")")"; R="$AEG/cmb-fit/results"; LOG="$R/selfcheck_v2_log.txt"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
export COBAYA_PACKAGES_PATH="${COBAYA_PACKAGES_PATH:-$AEG/cmb-fit/packages}" TWIST_RESULTS="$R"
mkdir -p "$R/lanes"; say() { echo "$(date '+%F %T') $*" | tee -a "$LOG"; }
say "waiting for DESI-MOCK-CMB to finish"
sleep 60
while pgrep -f "desi_mock_cmb.py|run_mock_cmb_pc.sh" >/dev/null; do sleep 600; done
say "V2 start"
cd "$T"
for w in FLAG1 LCDM; do
  ( OMP_NUM_THREADS=2 nice -n 5 "$PY" v2_nosn_fit.py $w > "$R/lanes/selfcheck_v2_$w.log" 2>&1 \
      && say "V2 $w done" || say "V2 $w FAILED (see lanes/selfcheck_v2_$w.log)" ) &
  sleep 20
done
wait; "$PY" v2_nosn_fit.py score >> "$LOG" 2>&1 && say "V2 scored" || say "V2 score FAILED"
