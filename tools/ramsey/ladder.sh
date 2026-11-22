#!/bin/bash
# core 1: known-answer calibration ladder (R(3,K)-1 vertices must be found); logs time-to-solution
cd "$(dirname "$0")"
for nk in "27 8 1 600" "27 8 2 600" "27 8 3 600" "35 9 1 1800" "35 9 2 1800" "39 10 1 2400"; do set -- $nk
  s=$(date +%s.%N); ./r310 $3 $4 $1 $2 > out_$1_$2_$3.txt 2> log_$1_$2_$3.txt; rc=$?; e=$(date +%s.%N)
  echo "N=$1 K=$2 seed=$3 found=$([ $rc -eq 0 ] && echo yes || echo no) secs=$(echo "$e - $s" | bc) $(tail -1 log_$1_$2_$3.txt)" >> ladder_results.txt
done
