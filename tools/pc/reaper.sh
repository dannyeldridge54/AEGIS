#!/bin/bash
# AEGIS queue reaper (2026-11-18). Reclaims running/ slots left behind by crashed/hung/deadlocked jobs so the
# MAXJ gate can never freeze the whole queue. Called by AEGIS_Watchdog.bat every 10 min (no runner restart needed).
# A running job is reaped if it is past its wall-limit (+5 min grace) OR its log has been idle longer than IDLE_CAP.
cd /mnt/c/Users/Danny/Desktop/AEGIS_PCJOBS || exit 0
IDLE_CAP=${IDLE_CAP:-7200}
for rj in queue/running/*.job; do
  [ -e "$rj" ] || continue
  rid=$(basename "$rj" .job); sf="queue/logs/$rid.status"; lf="queue/logs/$rid.log"; now=$(date +%s)
  stm=$(stat -c %Y "$sf" 2>/dev/null || echo "$now"); lgm=$(stat -c %Y "$lf" 2>/dev/null || echo "$stm")
  lim=$(sed -n 's/.*limit \([0-9]\+\).*/\1/p' "$sf" 2>/dev/null); lim=${lim:-7200}
  age=$((now-stm)); idle=$((now-lgm))
  if [ "$age" -gt $((lim+300)) ] || [ "$idle" -gt "$IDLE_CAP" ]; then
    reason="overdue"; [ "$idle" -gt "$IDLE_CAP" ] && reason="idle"
    echo "$(date) WD-REAP $rid ($reason) age=${age}s idle=${idle}s lim=${lim}s -> done"
    echo "STALE $(date) wd-reaped ($reason) age=$age idle=$idle" > "$sf"
    mv "$rj" queue/done/ 2>/dev/null
  fi
done
