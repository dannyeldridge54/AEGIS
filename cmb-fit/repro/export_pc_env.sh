#!/usr/bin/env bash
# V8 (field_tests/validation/V8_REPRODUCIBILITY.md): record exactly what the PC fits ran with. Read-only on the env and
# builds; writes cmb-fit/repro/pc_export/. Takes a few minutes (hashes the likelihood data). Safe while fits run.
#   wsl bash cmb-fit/repro/export_pc_env.sh
set -uo pipefail
H="$(cd "$(dirname "$0")" && pwd)"; CF="$(dirname "$H")"; OUT="$H/pc_export"; mkdir -p "$OUT"
PY="${TWIST_PY:-/home/syndyr/micromamba/envs/aegis/bin/python}"; [ -x "$PY" ] || PY=python3
ENVDIR="$(dirname "$(dirname "$PY")")"; BLD="${TWIST_BUILDS:-$HOME}"; PKG="${COBAYA_PACKAGES_PATH:-$CF/packages}"
MM="$(command -v micromamba || command -v mamba || command -v conda || true)"
{ date -u '+exported %FT%TZ'; uname -a; "$PY" --version; gcc --version | head -1; gfortran --version 2>/dev/null | head -1
  echo "python: $PY"; echo "builds: $BLD"; echo "packages: $PKG"; } > "$OUT/system.txt" 2>&1
[ -n "$MM" ] && "$MM" env export -p "$ENVDIR" --no-builds > "$OUT/environment.yml" 2>&1
"$PY" -m pip freeze > "$OUT/pip_freeze.txt" 2>&1
"$PY" -c "import cobaya,numpy,scipy;print('cobaya',cobaya.__version__);print('numpy',numpy.__version__);print('scipy',scipy.__version__)" > "$OUT/versions.txt" 2>&1
# Every AxiCLASS build the fits load: upstream commit, local diff vs that commit, SHA-256 of every C source/header.
: > "$OUT/builds.txt"
for b in AxiCLASS AxiCLASS_nlfix AxiCLASS_coupled AxiCLASS_coupled_nlfix AxiCLASS_coupled_nlfix_ula AxiCLASS_sinh; do
  d="$BLD/$b"; [ -d "$d" ] || { echo "$b: MISSING" >> "$OUT/builds.txt"; continue; }
  echo "== $b  commit $(git -C "$d" rev-parse HEAD 2>/dev/null || echo 'not a git checkout')" >> "$OUT/builds.txt"
  (cd "$d" && find source include tools main python -maxdepth 1 -type f \( -name '*.c' -o -name '*.h' -o -name '*.pyx' -o -name '*.pxd' \) \
     -print0 2>/dev/null | sort -z | xargs -0 sha256sum) >> "$OUT/builds.txt"
  git -C "$d" diff > "$OUT/diff_$b.patch" 2>/dev/null || true
done
# Likelihood data: file list with sizes and SHA-256 (no data copied).
(cd "$PKG" && find . -type f -not -path '*/.git/*' -print0 | sort -z | xargs -0 sha256sum) > "$OUT/packages_sha256.txt" 2>/dev/null
for g in "$PKG"/*/ "$PKG"/data/*/; do [ -d "$g/.git" ] && echo "$g $(git -C "$g" rev-parse HEAD)"; done > "$OUT/packages_git.txt" 2>/dev/null
# The stored best fits the reproduction checks against.
(cd "$CF/results" && sha256sum cmp_ax_spa_spiraltwist_nlfix.json cmp_ax_spa_lcdm_halofit.json) > "$OUT/stored_fits_sha256.txt"
echo "V8 export written to $OUT"; ls -la "$OUT"
