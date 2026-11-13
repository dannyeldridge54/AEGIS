#!/usr/bin/env bash
# PC (WSL): NS-PURE (field_tests/rules/PREREG_NS_PURE.md). Waits for V6, reuses its LCDM fit, fits PURE-TWIST, scores.
set -uo pipefail
T="$(cd "$(dirname "$0")" && pwd)"; AEG="$(dirname "$(dirname "$T")")"; R="$AEG/cmb-fit/results"; LOG="$R/ns_pure_log.txt"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
export COBAYA_PACKAGES_PATH="${COBAYA_PACKAGES_PATH:-$AEG/cmb-fit/packages}" TWIST_RESULTS="$R"
say() { echo "$(date '+%F %T') $*" | tee -a "$LOG"; }
[ -f "$AEG/field_tests/rules/PREREG_NS_PURE.md.sha256" ] || { say "rule not locked; not running"; exit 1; }
say "waiting for V6"; sleep 60
while pgrep -f "v6_pr4_fit.py|run_v6_pc.sh" >/dev/null; do sleep 600; done
cd "$T"
for w in PURE LCDM; do "$PY" ns_pure_fit.py gate $w >> "$LOG" 2>&1 || { say "gate $w FAILED: NO VERDICT"; exit 1; }; done
LC="$R/cmp_ax_spa_lcdm_halofit_pr4_s8y6.json"
[ -f "$LC" ] && say "reusing V6 LCDM fit" || { OMP_NUM_THREADS=4 "$PY" ns_pure_fit.py fit LCDM >> "$R/lanes/ns_lcdm.log" 2>&1; }
OMP_NUM_THREADS=4 nice -n 5 "$PY" ns_pure_fit.py fit PURE > "$R/lanes/ns_pure.log" 2>&1 && say "fit PURE done" || say "fit PURE FAILED"
"$PY" ns_pure_fit.py score >> "$LOG" 2>&1 && say "NS-PURE scored" || say "NS-PURE score FAILED"
