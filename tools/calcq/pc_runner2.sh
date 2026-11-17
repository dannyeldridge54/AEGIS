#!/bin/bash
# AEGIS PC runner v2: up to MAXJ jobs at once, per-job wall limit, auto-unpack, status file. Jobs: queue/<ID>.job = "<workdir>|<limit_s>|<command>"
# (v1 two-field lines "<workdir>|<command>" still work, limit 7200 s). A <workdir>/*.tgz is unpacked into <workdir> before the job starts.
cd /mnt/c/Users/Danny/Desktop/AEGIS_PCJOBS || exit 1
PY=/home/syndyr/micromamba/envs/aegis/bin/python; [ -x "$PY" ] || PY=python3
MAXJ=${MAXJ:-$(( $(nproc) > 8 ? 3 : 2 ))}
echo "AEGIS PC runner v2 started $(date). Up to $MAXJ jobs at once. Close this window to stop."
mkdir -p queue/done queue/logs queue/running
while true; do
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
      echo "$st $(date) exit $ec" > "queue/logs/$id.status"; mv "queue/running/$id.job" queue/done/
      echo "[$id] $(date +%H:%M) $st (exit $ec)" ) &
  done
  date +%s > queue/logs/heartbeat.txt
  sleep 30
done
