#!/usr/bin/env bash
# Build CAMB 2.0.5 with the two-field UB module (DarkEnergyUBField.f90) into the CURRENT Python environment.
# Linux / WSL. Needs a Fortran compiler: if gfortran is missing, in a micromamba env run
#   micromamba install -y -c conda-forge gfortran make
# Then:  bash cmb-fit/ub2_camb/build_ub2_camb.sh   and check with:  python cmb-fit/ub2_camb/validate_single_field.py
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
W="$(mktemp -d)"
cd "$W"
pip download camb==2.0.5 --no-binary :all: --no-deps -q -d .
tar xzf camb-2.0.5.tar.gz
cd camb-2.0.5
cp "$HERE/DarkEnergyUBField.f90" fortran/
patch -p1 < "$HERE/makefile.patch"
patch -p1 < "$HERE/dark_energy_ubfield.patch"
pip install --no-build-isolation --no-deps --force-reinstall .
python -c "from camb.dark_energy import UBField; UBField(); print('UBField OK')"
