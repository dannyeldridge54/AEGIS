#!/usr/bin/env bash
# WSL, on the PC: build CAMB 2.0.5 + the two-field UB module into the micromamba env 'aegis', validate it, then run the
# UB-2 engine gates (G1-G3, Planck data). No UB-2 data fit runs here (the rule is not locked).
#   bash cmb-fit/ub2_camb/ub2_pc.sh     (log: cmb-fit/results/ub2_pc_log.txt)
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
CF="$(dirname "$HERE")"
LOG="$CF/results/ub2_pc_log.txt"
MM="${MAMBA_EXE:-$HOME/.local/bin/micromamba}"; [ -x "$MM" ] || MM="$(command -v micromamba || echo /home/syndyr/.local/bin/micromamba)"
ENV=aegis
PY="$HOME/micromamba/envs/$ENV/bin/python"; [ -x "$PY" ] || PY=/home/syndyr/micromamba/envs/aegis/bin/python
say() { echo "$(date '+%F %T') $*" | tee -a "$LOG"; }
say "UB-2 PC setup start (python $PY)"
if ! "$PY" -c "from camb.dark_energy import UBField" 2>/dev/null; then
  if ! "$HOME/micromamba/envs/$ENV/bin/gfortran" --version >/dev/null 2>&1; then
    say "installing gfortran + make into env $ENV (conda-forge)"
    "$MM" install -y -n "$ENV" -c conda-forge gfortran make >> "$LOG" 2>&1 || { say "FAILED: gfortran install"; exit 1; }
  fi
  say "building CAMB 2.0.5 + UBField"
  PATH="$(dirname "$PY"):$PATH" bash "$HERE/build_ub2_camb.sh" >> "$LOG" 2>&1 || { say "FAILED: build (see log)"; exit 1; }
fi
say "validate: two-field module vs CAMB EarlyQuintessence"
(cd "$HERE" && "$PY" validate_single_field.py) >> "$LOG" 2>&1 || say "validation script failed (see log)"
say "UB-2 gates G1-G3"
(cd "$CF" && COBAYA_PACKAGES_PATH="${COBAYA_PACKAGES_PATH:-$CF/packages}" "$PY" ub2_fit.py gates) >> "$LOG" 2>&1 \
  && say "gates written: results/ub2_gates.json" || say "gates FAILED (see log)"
# UB-2 fits (only once the rule is locked): variant B on the three supernova sets, in parallel, 2 threads each
if [ -f "$CF/../field_tests/rules/PREREG_UNIFY_DATA.md.sha256" ]; then
  for n in ub2B ub2B_dovekie ub2B_union3; do
    if [ ! -f "$CF/results/cmp_$n.json" ] && [ ! -f "$CF/results/${n}_log.txt" ]; then
      say "UB-2 fit $n start"
      (cd "$CF" && OMP_NUM_THREADS=2 COBAYA_PACKAGES_PATH="${COBAYA_PACKAGES_PATH:-$CF/packages}" nice -n 5 "$PY" ub2_fit.py "$n" > "results/${n}_log.txt" 2>&1 \
        && say "UB-2 fit $n done" || say "UB-2 fit $n FAILED (see results/${n}_log.txt)") &
    fi
  done
  wait
fi
