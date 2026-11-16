#!/bin/bash
# usage: bash tools/calcq/runner.sh   (from repo root; exits after IDLE_MAX seconds with nothing pending)
cd "$(git rev-parse --show-toplevel)"
Q=tools/calcq/queue.txt; S=tools/calcq/status.txt; mkdir -p tools/calcq/logs; touch $Q $S
MAXJOBS=${MAXJOBS:-2}; IDLE_MAX=${IDLE_MAX:-5400}; idle=0
while true; do
  next=""
  while IFS='|' read -r id cmd; do
    [ -z "$id" ] && continue
    grep -q "^$id|" $S || { next="$id|$cmd"; break; }
  done < $Q
  if [ -z "$next" ]; then sleep 30; idle=$((idle+30)); [ $idle -ge $IDLE_MAX ] && exit 0; continue; fi
  idle=0
  running=$(pgrep -c -f "python3 .*(theory|tools)/" || true)
  if [ "${running:-0}" -ge "$MAXJOBS" ]; then sleep 20; continue; fi
  id=${next%%|*}; cmd=${next#*|}
  echo "$id|running|$(date -u +%H:%MZ)||" >> $S
  ( bash -c "$cmd" > tools/calcq/logs/$id.log 2>&1; ec=$?
    sed -i "s#^$id|running|\([^|]*\)||#$id|done|\1|$(date -u +%H:%MZ)|$ec#" $S ) &
  sleep 5
done
