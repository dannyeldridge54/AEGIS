#!/bin/bash
# AxiCLASS + Cobaya inside WSL Ubuntu, for AEGIS Phase 1 step 1.3 (exact scalar-field solution instead of CAMB's
# fluid approximation). Run once from the Ubuntu window:
#   bash /mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass/setup_wsl.sh
# It asks for your Ubuntu (sudo) password once, for the system build tools. Everything is logged to setup_wsl.log
# next to this file, so it can be read from Windows. Safe to run again: finished steps are skipped.
set -euo pipefail
HERE=/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass
LOG="$HERE/setup_wsl.log"
exec > >(tee -a "$LOG") 2>&1
echo "=== $(date) start (user $(whoami))"

echo "--- 1/4 system build tools"
sudo apt-get update -y
sudo apt-get install -y build-essential gfortran git python3-venv python3-dev

echo "--- 2/4 Python environment (~/aegis-venv)"
VENV="$HOME/aegis-venv"
[ -d "$VENV" ] || python3 -m venv "$VENV"
source "$VENV/bin/activate"
pip install --upgrade pip wheel setuptools
# classy (the CLASS Python wrapper) in older CLASS forks needs Cython < 3 and NumPy < 2.
pip install "numpy<2" "cython<3" scipy cobaya getdist

echo "--- 3/4 AxiCLASS (~/AxiCLASS)"
[ -d "$HOME/AxiCLASS" ] || git clone --depth 1 https://github.com/PoulinV/AxiCLASS.git "$HOME/AxiCLASS"
cd "$HOME/AxiCLASS"
make -j"$(nproc)" libclass.a class
cd python
pip install --no-build-isolation .

echo "--- 4/4 smoke test"
python - <<'EOF'
from classy import Class
c = Class()
c.set({"output": "tCl,pCl,lCl", "lensing": "yes", "h": 0.6736, "omega_b": 0.02237, "omega_cdm": 0.12})
c.compute()
print("AxiCLASS OK: H0 =", round(c.h() * 100, 2), " sigma8 =", round(c.sigma8(), 4))
c.struct_cleanup()
EOF
echo "=== $(date) done"
