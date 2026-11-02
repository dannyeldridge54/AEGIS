#!/bin/bash
# Reproducibility snapshot: exact Python environment, the git state of every AxiCLASS build, compiler and OS.
# Writes results/env_snapshot_<date>/ ; read-only for everything else (running fits are untouched).
# Portable paths (make_portable.py): override with TWIST_RESULTS, TWIST_BUILDS, TWIST_PY.
AXI="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
RES="${TWIST_RESULTS:-$(dirname "$AXI")/results}"
BLD="${TWIST_BUILDS:-$HOME}"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
ENV="${TWIST_ENV:-$(dirname "$(dirname "$PY")")}"
OUT=$RES/env_snapshot_$(date +%F)
mkdir -p "$OUT"
$ENV/bin/python -m pip freeze > "$OUT/pip_freeze.txt" 2>/dev/null
( $BLD/bin/micromamba env export -p $ENV || micromamba env export -p $ENV || $ENV/bin/conda env export -p $ENV ) > "$OUT/micromamba_env.yml" 2>/dev/null
$ENV/bin/python --version > "$OUT/python_version.txt" 2>&1
for b in AxiCLASS AxiCLASS_coupled AxiCLASS_nlfix AxiCLASS_coupled_nlfix; do
  d=$BLD/$b
  [ -d "$d" ] || continue
  { echo "== $b"; git -C "$d" log --oneline -3 2>/dev/null; git -C "$d" status --short 2>/dev/null | head -20
    echo "-- diff vs HEAD (sha256):"; git -C "$d" diff HEAD 2>/dev/null | sha256sum
    ls "$d"/python/build/lib*/classy*.so 2>/dev/null | xargs -r sha256sum; } >> "$OUT/axiclass_builds.txt"
done
sha256sum $ENV/lib/python3.11/site-packages/classy*.so >> "$OUT/axiclass_builds.txt" 2>/dev/null
{ gcc --version | head -1; uname -a; nproc; } > "$OUT/system.txt" 2>&1
ls "$OUT"; wc -l "$OUT"/*.txt | tail -1
