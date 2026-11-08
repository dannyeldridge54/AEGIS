#!/usr/bin/env bash
# WSL, PC. Started once by START_AFTER_S8.bat (8 Nov). Waits until no S8-J / S8-L fit is running (all 9 fits + the 3 extra
# LCDM restarts), then:
#   1. bracket (Kronos PREREG_BRACKET.md, unchanged): Danny decided 8 Nov 05:47 CT to restart the 4 jobs that were
#      interrupted when their windows were closed. Their logs are renamed *_interrupted.txt (never deleted) and
#      start_bracket_if_needed.bat is called, which starts only jobs with no log (Windows venv312, 2 threads each).
#   2. POWER_N n = 1 on AxiCLASS (power_n1_fit.py): starts as soon as PREREG_POWER_N1_AXICLASS.md.sha256 exists
#      (waits for the lock if needed).
# Log: cmb-fit/results/after_s8_log.txt
set -uo pipefail
cd /mnt/c/Users/Danny 2>/dev/null || true
CF="$(cd "$(dirname "$0")" && pwd)"; ROOT="$(cd "$CF/.." && pwd)"; R="$CF/results"; LOG="$R/after_s8_log.txt"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
export COBAYA_PACKAGES_PATH="${COBAYA_PACKAGES_PATH:-$CF/packages}" TWIST_RESULTS="$R"
say() { echo "$(date '+%F %T') $*" | tee -a "$LOG"; }
busy() { pgrep -f "s8_joint_fit.py|spiral_l_fit.py" > /dev/null; }
say "waiting for the S8-J / S8-L fits to finish"
quiet=0
while [ $quiet -lt 3 ]; do
  if busy; then quiet=0; else quiet=$((quiet + 1)); fi
  sleep 120
done
say "no S8 fit running for 6 minutes"
# 1. bracket restart
for n in edelockP_th2.41421_F10_deep edelockP_th2.777_F8_deep edelockP_th2.777_F9_deep edelockP_th2.777_F10_deep; do
  if [ -f "$R/${n}_log.txt" ] && [ ! -f "$R/cmp_$n.json" ]; then
    mv "$R/${n}_log.txt" "$R/${n}_log_interrupted.txt" && say "renamed ${n}_log.txt -> ${n}_log_interrupted.txt"
  fi
done
/mnt/c/Windows/System32/cmd.exe /c "C:\\Users\\Danny\\.copilot\\repos\\AEGIS\\cmb-fit\\start_bracket_if_needed.bat" >> "$LOG" 2>&1 \
  && say "bracket launcher called" || say "bracket launcher FAILED to start (see log)"
# 2. POWER_N n = 1
until [ -f "$ROOT/field_tests/rules/PREREG_POWER_N1_AXICLASS.md.sha256" ]; do sleep 300; done
if [ ! -f "$R/cmp_ax_spa_edelock_n1.json" ]; then
  say "POWER_N n=1 fit start"
  (cd "$CF/axiclass" && OMP_NUM_THREADS=2 nice -n 5 "$PY" power_n1_fit.py > "$R/lanes/ax_spa_edelock_n1.log" 2>&1) \
    && say "POWER_N n=1 fit done" || say "POWER_N n=1 fit FAILED (see results/lanes/ax_spa_edelock_n1.log)"
fi
say "after-S8 queue finished"
