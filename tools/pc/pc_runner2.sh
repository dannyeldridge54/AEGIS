#!/bin/bash
# AEGIS PC runner v2.1: up to MAXJ jobs at once, per-job wall limit, auto-unpack, status file. Jobs: queue/<ID>.job = "<workdir>|<limit_s>|<command>"
# (v1 two-field lines "<workdir>|<command>" still work, limit 7200 s). A <workdir>/*.tgz is unpacked into <workdir> before the job starts.
# v2.1 (2026-11-18): REAPER — a crashed/hung/deadlocked job used to leave its .job in running/ forever, filling the MAXJ gate
#   and freezing the whole queue (that is exactly what stalled LEARN for hours). Each loop now reclaims any running slot whose
#   job is past its wall-limit OR whose log has been idle longer than IDLE_CAP (default 2h), moving it to done/ as STALE.
cd /mnt/c/Users/Danny/Desktop/AEGIS_PCJOBS || exit 1
PY=/home/syndyr/micromamba/envs/aegis/bin/python; [ -x "$PY" ] || PY=python3
MAXJ=${MAXJ:-$(( $(nproc) > 8 ? 3 : 2 ))}
IDLE_CAP=${IDLE_CAP:-7200}   # reap a running job whose log has not grown in this many seconds (hung/deadlocked)
echo "AEGIS PC runner v2.1 started $(date). Up to $MAXJ jobs at once; reaper on (IDLE_CAP=${IDLE_CAP}s). Close this window to stop."
mkdir -p queue/done queue/logs queue/running
while true; do
  # --- reaper: reclaim leaked/stale running slots so the queue can never freeze on a dead job ---
  for rj in queue/running/*.job; do
    [ -e "$rj" ] || continue
    rid=$(basename "$rj" .job); sf="queue/logs/$rid.status"; lf="queue/logs/$rid.log"; nowr=$(date +%s)
    stm=$(stat -c %Y "$sf" 2>/dev/null || echo "$nowr"); lgm=$(stat -c %Y "$lf" 2>/dev/null || echo "$stm")
    lim=$(sed -n 's/.*limit \([0-9]\+\).*/\1/p' "$sf" 2>/dev/null); lim=${lim:-7200}
    age=$((nowr-stm)); idle=$((nowr-lgm))
    if [ "$age" -gt $((lim+300)) ] || [ "$idle" -gt "$IDLE_CAP" ]; then
      reason="overdue"; [ "$idle" -gt "$IDLE_CAP" ] && reason="idle"
      echo "$(date) STALE-REAP $rid ($reason) age=${age}s idle=${idle}s lim=${lim}s -> done" | tee -a queue/logs/watchdog.log
      echo "STALE $(date) reaped ($reason) age=$age idle=$idle" > "$sf"
      mv "$rj" queue/done/ 2>/dev/null
    fi
  done
  for jf in queue/*.job; do
    [ -e "$jf" ] || continue
    [ "$(ls queue/running | wc -l)" -ge "$MAXJ" ] && break
    id=$(basename "$jf" .job); line=$(head -1 "$jf" | tr -d '\r')
    wd=${line%%|*}; rest=${line#*|}
    if [[ "$rest" =~ ^[0-9]+\| ]]; then lim=${rest%%|*}; cmd=${rest#*|}; else lim=7200; cmd=$rest; fi
    case "$wd" in *..*|/*) echo "[$id] rejected: workdir"; mv "$jf" queue/done/; continue;; esac
    mkdir -p "$wd"; for t in "$wd"/*.tgz; do [ -e "$t" ] && tar xzf "$t" -C "$wd" && mv "$t" "$t.unpacked"; done
    mv "$jf" queue/running/
    echo "[$id] $(date +%H:%M) start (limit ${lim}s): $cmd"
    ( echo "running $(date) limit $lim" > "queue/logs/$id.status"
      cd "$wd" && timeout "$lim" bash -c "${cmd//python3/$PY}" > "../queue/logs/$id.log" 2>&1; ec=$?
      cd ..; st=done; [ $ec -eq 124 ] && st=TIMEOUT
      # only finalize if we still own the slot (the reaper may have reclaimed it)
      if [ -e "queue/running/$id.job" ]; then
        echo "$st $(date) exit $ec" > "queue/logs/$id.status"; mv "queue/running/$id.job" queue/done/
      fi
      echo "[$id] $(date +%H:%M) $st (exit $ec)" ) &
  done
  date +%s > queue/logs/heartbeat.txt
  sleep 30
done
