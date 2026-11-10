#!/usr/bin/env bash
# AEGIS job runner (PC, WSL). Started once (START_RUNNER.bat); then any job file dropped in method/runner/queue/
# (one line: a script path relative to the repo, e.g. cmb-fit/axiclass/darkrad/run_dr_pc.sh) is started in the
# background and the job file moved to method/runner/started/. Only .sh scripts under cmb-fit/ or field_tests/ run.
# Heartbeat: method/runner/heartbeat (updated every 30 s). Stop: close the AEGIS-RUNNER window.
REPO="$(cd "$(dirname "$0")/../.." && pwd)"; Q="$REPO/method/runner/queue"; S="$REPO/method/runner/started"
mkdir -p "$Q" "$S"; LOG="$REPO/method/runner/runner_log.txt"
echo "$(date '+%F %T') runner up (pid $$)" >> "$LOG"
while true; do
  date '+%F %T' > "$REPO/method/runner/heartbeat"
  for j in "$Q"/*.job; do
    [ -e "$j" ] || continue
    rel="$(head -n1 "$j" | tr -d '\r')"
    case "$rel" in
      cmb-fit/*.sh|field_tests/*.sh) ;;
      *) echo "$(date '+%F %T') REFUSED $j: $rel" >> "$LOG"; mv "$j" "$S/$(basename "$j").refused"; continue ;;
    esac
    case "$rel" in *..*) echo "$(date '+%F %T') REFUSED $j: $rel" >> "$LOG"; mv "$j" "$S/$(basename "$j").refused"; continue ;; esac
    if [ -f "$REPO/$rel" ]; then
      mv "$j" "$S/"
      echo "$(date '+%F %T') start $rel" >> "$LOG"
      ( bash "$REPO/$rel" >> "$LOG" 2>&1; echo "$(date '+%F %T') finished $rel (exit $?)" >> "$LOG" ) &
    else
      echo "$(date '+%F %T') MISSING $rel" >> "$LOG"; mv "$j" "$S/$(basename "$j").missing"
    fi
  done
  sleep 30
done
