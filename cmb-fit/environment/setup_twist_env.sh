#!/bin/bash
# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under the Hippocratic License 3.0 with the Military Activities and Mass Surveillance modules (HL3-MIL-SV; see LICENSE): free to everyone, for any use that respects human rights.
# Rebuild the exact environment used for every fit in "The Twist" (Linux or WSL; needs git, gcc, make, micromamba or conda).
#   bash setup_twist_env.sh            -> env "twist", the four AxiCLASS builds in $TWIST_BUILDS (default $HOME),
#                                         likelihood data in $COBAYA_PACKAGES_PATH (default ../packages)
# Then:  export TWIST_PY=<env>/bin/python   and run any fit:  $TWIST_PY ../axiclass/early_late_spa.py <run name>
set -e
HERE="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
AXI="$(dirname "$HERE")/axiclass"                               # AEGIS layout: cmb-fit/{environment,axiclass}
[ -d "$AXI" ] || AXI="$(dirname "$HERE")/code/axiclass"         # release layout: {environment,code/axiclass}
BLD="${TWIST_BUILDS:-$HOME}"
PKG="${COBAYA_PACKAGES_PATH:-$(dirname "$HERE")/packages}"
AXICLASS_COMMIT=ae9609e1f96ddebbb6cc8a46de94512514c68781        # PoulinV/AxiCLASS, the base of all four builds
SPT_DATA_COMMIT=f22611a9671d50af6135f048a2ea3f43ef4c2f62        # SouthPoleTelescope/spt_candl_data
MM="$(command -v micromamba || command -v mamba || command -v conda)"

echo "== 1/5 Python environment (exact versions: environment.yml, pip_freeze.txt)"
"$MM" env create -y -n twist -f "$HERE/environment.yml" || "$MM" env update -n twist -f "$HERE/environment.yml"
PY="$("$MM" run -n twist which python)"
ENVDIR="$(dirname "$(dirname "$PY")")"
export TWIST_PY="$PY" TWIST_BUILDS="$BLD" COBAYA_PACKAGES_PATH="$PKG"

echo "== 2/5 AxiCLASS at the pinned commit, built and installed (the 'installed' build)"
[ -d "$BLD/AxiCLASS" ] || git clone https://github.com/PoulinV/AxiCLASS.git "$BLD/AxiCLASS"
git -C "$BLD/AxiCLASS" checkout -q "$AXICLASS_COMMIT"
( cd "$BLD/AxiCLASS" && make -j4 libclass.a && cd python && CC="${CC:-gcc}" "$PY" -m pip install --no-build-isolation . )

echo "== 3/5 The three variant builds (copies; none is installed; scripts load them by path)"
for v in AxiCLASS_nlfix AxiCLASS_coupled; do [ -d "$BLD/$v" ] || cp -r "$BLD/AxiCLASS" "$BLD/$v"; done
"$PY" "$AXI/nlfix/patch_nlfix.py" "$BLD/AxiCLASS_nlfix"
TWIST_ENV="$ENVDIR" bash "$AXI/nlfix/build_nlfix.sh"
"$PY" "$AXI/coupled/patch_coupling.py" "$BLD/AxiCLASS_coupled"
TWIST_ENV="$ENVDIR" bash "$AXI/coupled/build_coupled.sh"
TWIST_ENV="$ENVDIR" bash "$AXI/nlfix/build_coupled_nlfix.sh"   # copies AxiCLASS_coupled -> AxiCLASS_coupled_nlfix

echo "== 4/5 Likelihood data (public; downloaded, not redistributed)"
"$ENVDIR/bin/cobaya-install" planck_2018_lowl.TT planck_2018_lowl.EE act_dr6_cmbonly act_dr6_lenslike \
  bao.desi_dr2.desi_bao_all sn.pantheonplus sn.desy5 sn.desdovekie -p "$PKG"
[ -d "$PKG/spt_candl_data" ] || git clone https://github.com/SouthPoleTelescope/spt_candl_data.git "$PKG/spt_candl_data"
git -C "$PKG/spt_candl_data" checkout -q "$SPT_DATA_COMMIT"
"$PY" -m pip install -e "$PKG/spt_candl_data"

echo "== 5/5 Checks"
"$PY" "$AXI/nlfix/bug_reproducer.py" "$BLD/AxiCLASS/python/build" | tail -1          # expect MISMATCH (the bug)
"$PY" "$AXI/nlfix/bug_reproducer.py" "$BLD/AxiCLASS_nlfix/python/build" | tail -1    # expect MATCH (the fix)
"$PY" "$AXI/early_late_spa.py" smoke ax_spa_lcdm_halofit                              # one likelihood evaluation
echo "Done. export TWIST_PY=$PY TWIST_BUILDS=$BLD COBAYA_PACKAGES_PATH=$PKG"
