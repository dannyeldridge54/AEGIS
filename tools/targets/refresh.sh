#!/bin/bash
# keeps the target-acquisition table current while searches run (every 60 s, for up to 2 h)
cd "$(dirname "$0")/../.."; for i in $(seq 1 120); do python3 tools/targets/track.py backfill > /dev/null 2>&1; sleep 60; done
