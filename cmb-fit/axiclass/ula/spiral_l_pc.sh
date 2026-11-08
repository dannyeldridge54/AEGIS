#!/usr/bin/env bash
# WSL, on the PC: S8-L (light angle). Build the ULA AxiCLASS copy, run gate G-L (allowed before the lock), then WAIT for
# field_tests/rules/PREREG_SPIRAL_L.md.sha256 (the lock) and run the three fits. Log: cmb-fit/results/spiral_l_pc_log.txt
set -uo pipefail
U="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$U/../../.." && pwd)"
CF="$ROOT/cmb-fit"; R="$CF/results"; LOG="$R/spiral_l_pc_log.txt"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
export COBAYA_PACKAGES_PATH="${COBAYA_PACKAGES_PATH:-$CF/packages}" TWIST_RESULTS="$R"
mkdir -p "$R/lanes"
say() { echo "$(date '+%F %T') $*" | tee -a "$LOG"; }
say "S8-L build start"
bash "$U/build_ula.sh" >> "$LOG" 2>&1 || { say "build FAILED (see log)"; exit 1; }
if [ ! -f "$R/spiral_l_gate_pc.json" ]; then
  say "gate G-L start"
  (cd "$U" && OMP_NUM_THREADS=4 "$PY" spiral_l_fit.py gate_pc) >> "$LOG" 2>&1 || { say "gate script FAILED: no fits"; exit 1; }
fi
"$PY" -c "import json,sys; sys.exit(0 if json.load(open('$R/spiral_l_gate_pc.json'))['all_pass'] else 1)" \
  || { say "gate G-L FAILED: no fits (results/spiral_l_gate_pc.json)"; exit 1; }
say "gate G-L passed; waiting for the lock (PREREG_SPIRAL_L.md.sha256)"
until [ -f "$ROOT/field_tests/rules/PREREG_SPIRAL_L.md.sha256" ]; do sleep 60; done
say "rule locked: fits start"
for n in spiralL spiralL_dovekie spiralL_union3; do
  [ -f "$R/cmp_$n.json" ] && continue
  say "S8-L fit $n start"
  ( cd "$U" && OMP_NUM_THREADS=2 nice -n 5 "$PY" spiral_l_fit.py "$n" > "$R/lanes/$n.log" 2>&1 \
      && say "S8-L fit $n done" || say "S8-L fit $n FAILED (see results/lanes/$n.log)" ) &
  sleep 15
done
wait
say "S8-L finished"
