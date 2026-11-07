#!/bin/bash
# Run every locked AxiCLASS field test on the PC (WSL), blind samples first, in parallel lanes, then score.
#   bash field_tests/run_pc.sh            # run what is missing, then score
#   bash field_tests/run_pc.sh --push     # also commit results + STATUS to branch field-results and push it
# Safe to re-run: finished runs (cmp_<name>.json) are skipped, so a nightly schedule resumes after a stop.
# Settings are the locked ones: every run name already encodes model, data and options; nothing is changed here.
# Paths follow the other runners: TWIST_PY, TWIST_RESULTS, TWIST_BUILDS (see cmb-fit/environment/setup_twist_env.sh).
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
ROOT="$(dirname "$HERE")"
AXI="$ROOT/cmb-fit/axiclass"
RES="${TWIST_RESULTS:-$ROOT/cmb-fit/results}"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
LANES="${LANES:-7}"                  # 7 lanes x 2 threads fits a 16-core PC with room to spare
LOG="$RES/lanes/field_tests.log"; mkdir -p "$RES/lanes"
say() { echo "$(date '+%F %T') $*" | tee -a "$LOG"; }

# Blind samples first (Union3), then the rest; TF-P before TF.
QUEUE=$($PY -c "
import json; t=json.load(open('$HERE/TESTS.json'))['tests']
runs=[r for x in t if x['where'].startswith('PC') and not x.get('code_missing') for r in x.get('runs',[])]
print(' '.join(sorted(runs, key=lambda r: (0 if 'union3' in r else 1, runs.index(r)))))")

# SF counts only if its locked gate passed.
GATE_OK=$($PY -c "import json; d=json.load(open('$HERE/gates/spiral_fit_mirror.json')); print(int(abs(d['dLCDM_limit'])<=1.0))")

say "field tests start: lanes=$LANES python=$PY results=$RES"
for n in $QUEUE; do
  [ -f "$RES/cmp_$n.json" ] && { say "skip (done) $n"; continue; }
  if [[ "$n" == *spiraltwist* && "$GATE_OK" != 1 ]]; then say "skip $n: SF gate failed"; continue; fi
  while [ "$(jobs -rp | wc -l)" -ge "$LANES" ]; do wait -n; done
  say "start $n"
  ( OMP_NUM_THREADS=2 nice -n 5 "$PY" "$AXI/early_late_spa.py" "$n" > "$RES/lanes/$n.log" 2>&1
    if [ -f "$RES/cmp_$n.json" ]; then say "done $n"; else say "NO RESULT $n (counts as the rule says; see lanes/$n.log)"; fi ) &
  sleep 15
done
wait
say "all runs finished; scoring"
TWIST_RESULTS="$RES" "$PY" "$HERE/score.py" > /dev/null && say "STATUS written: field_tests/STATUS.md"

if [ "${1:-}" = "--push" ]; then
  cd "$ROOT" || exit 1
  files=$(for n in $QUEUE; do [ -f "$RES/cmp_$n.json" ] && echo "$RES/cmp_$n.json"; done)
  git add -f $files field_tests/STATUS.md field_tests/STATUS.json 2>/dev/null
  git commit -q -m "field tests: results and locked-rule scores $(date '+%F %T')" -- $files field_tests/STATUS.md field_tests/STATUS.json \
    && git push -q origin HEAD:refs/heads/field-results && say "pushed to branch field-results"
fi
