#!/bin/bash
# AxiCLASS + Cobaya inside WSL Ubuntu WITHOUT sudo (AEGIS Phase 1 step 1.3). Uses micromamba (conda-forge) for the
# compilers, make, git and Python, all inside $HOME. Logged to setup_wsl.log next to this file. Safe to re-run.
#   bash /mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass/setup_wsl_nosudo.sh
set -euo pipefail
HERE=/mnt/c/Users/Danny/.copilot/repos/AEGIS/cmb-fit/axiclass
LOG="$HERE/setup_wsl.log"
exec > >(tee -a "$LOG") 2>&1
echo "=== $(date) start, no-sudo route (user $(whoami))"

echo "--- 1/4 micromamba (~/bin/micromamba)"
mkdir -p "$HOME/bin"
if [ ! -x "$HOME/bin/micromamba" ]; then
  # The minimal Ubuntu image has no bzip2, so unpack the .tar.bz2 with Python's tarfile instead of tar -j.
  curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/latest -o "$HOME/micromamba.tar.bz2"
  python3 -c "import os, tarfile; tarfile.open(os.path.expanduser('~/micromamba.tar.bz2')).extract('bin/micromamba', os.path.expanduser('~'))"
  chmod +x "$HOME/bin/micromamba"
  rm -f "$HOME/micromamba.tar.bz2"
fi
export MAMBA_ROOT_PREFIX="$HOME/micromamba"
eval "$("$HOME/bin/micromamba" shell hook -s bash)"

echo "--- 2/4 environment 'aegis' (compilers, make, git, Python 3.11, NumPy<2, Cython<3)"
if ! micromamba env list | grep -q '^ *aegis '; then
  micromamba create -y -n aegis -c conda-forge python=3.11 "numpy<2" "cython<3" scipy compilers make git pip
fi
micromamba activate aegis
pip install cobaya getdist

echo "--- 3/4 AxiCLASS (~/AxiCLASS)"
[ -d "$HOME/AxiCLASS" ] || git clone --depth 1 https://github.com/PoulinV/AxiCLASS.git "$HOME/AxiCLASS"
cd "$HOME/AxiCLASS"
make -j"$(nproc)" CC="${CC:-gcc}" libclass.a class
cd python
CC="${CC:-gcc}" pip install --no-build-isolation .

echo "--- 4/4 smoke test"
python - <<'EOF'
from classy import Class
c = Class()
c.set({"output": "tCl,pCl,lCl,mPk", "lensing": "yes", "h": 0.6736, "omega_b": 0.02237, "omega_cdm": 0.12})
c.compute()
print("AxiCLASS OK: H0 =", round(c.h() * 100, 2), " sigma8 =", round(c.sigma8(), 4))
c.struct_cleanup()
EOF
echo "=== $(date) done"
