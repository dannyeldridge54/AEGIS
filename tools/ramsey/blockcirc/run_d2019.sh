#!/bin/bash
# D2019 continuous run (no ticks): every block-circulant case back to back; stops at a witness or when all cases are done.
cd "$(dirname "$0")"; out=d2019_results.txt; echo "start $(date -u +%FT%TZ)" > $out
for bm in "2 20" "5 8" "8 5" "4 10"; do set -- $bm; s=$(date +%s); ./bc $1 $2 10 9 5 >> $out; echo "  (B=$1 m=$2: $(( $(date +%s)-s ))s)" >> $out
  if grep -q WITNESS $out; then echo "STOP: witness found" >> $out; break; fi; done
echo "DONE $(date -u +%FT%TZ)" >> $out
