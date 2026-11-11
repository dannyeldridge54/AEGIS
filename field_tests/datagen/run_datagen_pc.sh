#!/usr/bin/env bash
# PC (WSL): DATA-GEN. Waits for SELFCHECK V2 (and anything before it) to finish, then 8 fits, 4 at a time.
# Log: cmb-fit/results/datagen_log.txt
set -uo pipefail
T="$(cd "$(dirname "$0")" && pwd)"; AEG="$(dirname "$(dirname "$T")")"; R="$AEG/cmb-fit/results"; LOG="$R/datagen_log.txt"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
export COBAYA_PACKAGES_PATH="${COBAYA_PACKAGES_PATH:-$AEG/cmb-fit/packages}" TWIST_RESULTS="$R"
mkdir -p "$R/lanes"; say() { echo "$(date '+%F %T') $*" | tee -a "$LOG"; }
say "waiting for DESI-MOCK-CMB and SELFCHECK V2 to finish"
sleep 120
while pgrep -f "desi_mock_cmb.py|run_mock_cmb_pc.sh|v2_nosn_fit.py|run_v2_pc.sh" >/dev/null; do sleep 600; done
say "DATA-GEN start"
cd "$T"
run() { OMP_NUM_THREADS=2 nice -n 5 "$PY" datagen_fit.py $1 $2 > "$R/lanes/datagen_$1_$2.log" 2>&1 \
          && say "fit $1 $2 done" || say "fit $1 $2 FAILED (see lanes/datagen_$1_$2.log)"; }
for batch in "gen1 gen2" "gen3 cmbplanck"; do
  for g in $batch; do for m in FLAG1 LCDM; do
    [ -f "$R/cmp_$( [ $m = FLAG1 ] && echo ax_spa_spiraltwist_kappa1_nlfix || echo ax_spa_lcdm_halofit )_${g}_s8y6.json" ] && continue
    run $m $g & sleep 20
  done; done; wait
done
"$PY" datagen_fit.py score >> "$LOG" 2>&1 && say "DATA-GEN scored" || say "DATA-GEN score FAILED"
