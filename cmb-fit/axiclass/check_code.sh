#!/bin/bash
# Health check: compile Python, syntax-check shell scripts, confirm build fingerprints, duplicate runs, disk and memory.
# Portable paths (make_portable.py): override with TWIST_RESULTS, TWIST_BUILDS, TWIST_PY.
AXI="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
RES="${TWIST_RESULTS:-$(dirname "$AXI")/results}"
BLD="${TWIST_BUILDS:-$HOME}"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
cd $AXI
R=$RES
$PY -m py_compile early_late_spa.py pick_late_dovekie.py grid_tools.py nlfix/nlfix_tools.py nlfix/patch_nlfix.py \
  coupled/coupled_weff.py && echo "python: ok"
bad=0; for f in run_*.sh nlfix/*.sh coupled/*.sh; do bash -n "$f" || { echo "BAD $f"; bad=1; }; done; [ $bad = 0 ] && echo "shell: ok"
echo "-- build fingerprints now vs snapshot"
for b in AxiCLASS AxiCLASS_coupled AxiCLASS_nlfix AxiCLASS_coupled_nlfix; do
  now=$(sha256sum $BLD/$b/python/build/lib*/classy*.so 2>/dev/null | cut -c1-16)
  snap=$(grep "$BLD/$b/python/build/.*classy.cpython" $R/env_snapshot_2026-11-01/axiclass_builds.txt | head -1 | cut -c1-16)
  echo "$b now=$now snapshot=$snap $([ "$now" = "$snap" ] && echo MATCH || echo DIFF)"
done
echo "-- duplicate running fits"
ps -eo args | grep 'early_late_spa.py ax_' | grep -v grep | grep -v 'bash -c' | awk '{print $NF}' | sort | uniq -d | sed 's/^/DUP /'
echo "running: $(ps -eo args | grep 'early_late_spa.py ax_' | grep -v grep | grep -vc 'bash -c')"
df -h /mnt/c | tail -1; free -g | sed -n 2p; uptime
