#!/bin/bash
cd "$(dirname "$0")"; : > d2018_results.txt
for f in tables/[DQZ][0-9Q48x]*_phi*.txt; do s=$(date +%s); ./cay $f 10 9 5 >> d2018_results.txt; echo "  ($(( $(date +%s)-s ))s)" >> d2018_results.txt; done
echo DONE >> d2018_results.txt
