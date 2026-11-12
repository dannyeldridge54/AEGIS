#!/usr/bin/env bash
# Cloud follow-up after the PC holdout job (PREREG_DESI_HOLDOUT.md Test B; PREREG_MISSING_PIECE.md M3).
# Needs, copied from the PC: cmb-fit/results/cmp_ax_spa_{spiraltwist_kappa1_nlfix,lcdm_halofit}_nodesi_s8y6.json and
# field_tests/desi_holdout/predict_{FLAG1,LCDM}{,_stored}.json. Each step runs once; outputs are not overwritten by reruns.
set -uo pipefail
T="$(cd "$(dirname "$0")" && pwd)"; AEG="$(dirname "$(dirname "$T")")"
export TWIST_RESULTS="$AEG/cmb-fit/results" OMP_NUM_THREADS=1
LOG="$T/cloud_log.txt"; say() { echo "$(date '+%F %T') $*" | tee -a "$LOG"; }
for f in cmb-fit/results/cmp_ax_spa_spiraltwist_kappa1_nlfix_nodesi_s8y6.json cmb-fit/results/cmp_ax_spa_lcdm_halofit_nodesi_s8y6.json \
         field_tests/desi_holdout/predict_FLAG1.json field_tests/desi_holdout/predict_LCDM.json \
         field_tests/desi_holdout/predict_FLAG1_stored.json field_tests/desi_holdout/predict_LCDM_stored.json; do
  [ -f "$AEG/$f" ] || { say "missing $f"; exit 1; }
done
cd "$T"
[ -f "$AEG/field_tests/results/missing_piece_m3.json" ] || { python3 "$AEG/field_tests/missing_piece/m3_map.py" >> "$LOG" 2>&1 && say "M3 done" || say "M3 FAILED"; }
[ -f truth.json ] || { python3 desi_holdout.py truth >> "$LOG" 2>&1 && say "truth done" || { say "truth FAILED"; exit 1; }; }
( [ -f desi_mock_part_SN.json ] || python3 desi_holdout.py mock SN >> "$T/mock_SN.log" 2>&1 ) &
( [ -f desi_mock_part_noSN.json ] || python3 desi_holdout.py mock noSN >> "$T/mock_noSN.log" 2>&1 ) &
wait
[ -f desi_mock_result.json ] || { say "mock result missing"; exit 1; }
python3 desi_holdout.py score >> "$LOG" 2>&1 && say "Test A + B scored" || say "score FAILED"
