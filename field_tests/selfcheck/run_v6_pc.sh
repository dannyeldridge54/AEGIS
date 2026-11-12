#!/usr/bin/env bash
# PC (WSL): V6 Planck PR4 (field_tests/rules/PREREG_V6_PR4.md). Waits for the DESI-HOLDOUT job, links the PR4 CamSpec
# data already on the PC into the packages folder (no download), runs the gate, then both fits in parallel, then scores.
# Log: cmb-fit/results/v6_log.txt
set -uo pipefail
T="$(cd "$(dirname "$0")" && pwd)"; AEG="$(dirname "$(dirname "$T")")"; R="$AEG/cmb-fit/results"; LOG="$R/v6_log.txt"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
export COBAYA_PACKAGES_PATH="${COBAYA_PACKAGES_PATH:-$AEG/cmb-fit/packages}" TWIST_RESULTS="$R"
mkdir -p "$R/lanes"; say() { echo "$(date '+%F %T') $*" | tee -a "$LOG"; }
[ -f "$AEG/field_tests/rules/PREREG_V6_PR4.md.sha256" ] || { say "rule not locked; not running"; exit 1; }
say "waiting for DESI-HOLDOUT to finish"
sleep 60
while pgrep -f "desi_holdout.py|run_holdout_pc.sh" >/dev/null; do sleep 600; done
PR4="$COBAYA_PACKAGES_PATH/data/planck_NPIPE_CamSpec"
if [ ! -e "$PR4" ]; then
  for src in /mnt/c/Users/Danny/ufe_data/packages/data/planck_NPIPE_CamSpec "$HOME/mnt/ufe_data/packages/data/planck_NPIPE_CamSpec"; do
    [ -d "$src" ] && ln -s "$src" "$PR4" && say "linked PR4 data from $src" && break
  done
fi
[ -e "$PR4" ] || { say "PR4 CamSpec data not found; NO VERDICT"; exit 1; }
cd "$T"
for w in FLAG1 LCDM; do "$PY" v6_pr4_fit.py gate $w >> "$LOG" 2>&1 || { say "gate $w FAILED: NO VERDICT"; exit 1; }; done
say "gate passed; fits start"
for w in FLAG1 LCDM; do
  ( OMP_NUM_THREADS=2 nice -n 5 "$PY" v6_pr4_fit.py fit $w > "$R/lanes/v6_$w.log" 2>&1 \
      && say "fit $w done" || say "fit $w FAILED (see lanes/v6_$w.log)" ) &
  sleep 20
done
wait
"$PY" v6_pr4_fit.py score >> "$LOG" 2>&1 && say "V6 scored" || say "V6 score FAILED"
