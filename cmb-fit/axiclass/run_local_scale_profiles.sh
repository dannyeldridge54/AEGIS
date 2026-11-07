#!/bin/bash
# Planck high-l/lensing profile grid with each locally staged SN sample, kept separate from the ACT/SPT suite.
# Late-Twist cells use the B0-fixed AxiCLASS build; unpatched n=1 scalar-field outputs have invalid sigma8/Omega_m.
A="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
R="${TWIST_RESULTS:-$(dirname "$A")/results}"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
mkdir -p "$R/lanes"
failed=0

run_fit() {
  local n="$1"
  if [ -f "$R/cmp_$n.json" ]; then
    echo "$(date '+%F %T') skip completed $n"
    return 0
  fi
  if [ -e "$R/lanes/$n.claim" ]; then
    echo "$(date '+%F %T') blocked by existing claim (inspect its log): $n" >&2
    return 1
  fi
  echo "$(date '+%F %T') start $n"
  OMP_NUM_THREADS=2 nice -n 5 "$PY" "$A/early_late_spa.py" "$n" > "$R/lanes/$n.log" 2>&1
  local rc=$?
  if [ "$rc" -eq 0 ] && [ -f "$R/cmp_$n.json" ]; then
    echo "$(date '+%F %T') done $n"
    return 0
  fi
  echo "$(date '+%F %T') failed $n (exit $rc); see $R/lanes/$n.log" >&2
  return 1
}
export -f run_fit
export A R PY

sn_tags=("" "_snpantheon" "_snjla" "_desy5" "_dovekie" "_union3" "_snshoes")
for sn_tag in "${sn_tags[@]}"; do
  suffix="_planckfull${sn_tag}"
  reference="ax_spa_lcdm_halofit${suffix}"
  if ! run_fit "$reference"; then
    failed=1
    echo "$(date '+%F %T') skipping profile for $suffix because its matched reference failed"
    continue
  fi
  mapfile -t grid < <("$PY" "$A/grid_tools.py" latetwist)
  printf '%s\n' "${grid[@]}" | xargs -P 4 -I{} bash -c 'run_fit "${1}${2}_nlfix"' _ {} "$suffix" || failed=1
done

echo "$(date '+%F %T') Planck local scale profiles finished (failed or blocked batches: $failed)"
exit "$failed"
