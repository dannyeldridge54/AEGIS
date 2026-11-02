# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under the Hippocratic License 3.0 with the Military Activities and Mass Surveillance modules (HL3-MIL-SV; see LICENSE): free to everyone, for any use that respects human rights.
# UNTESTED (no container runtime on the author's PC). It wraps setup_twist_env.sh, which is the tested path's pieces.
# Reports of success or failure are welcome. Build from the repository root (the folder holding code/ and environment/):
#   docker build -f environment/Dockerfile -t twist .
#   docker run --rm -it twist bash -lc 'python verify.py && python code/analysis/paper_numbers_check.py'
#   docker run --rm -it twist bash -lc '$TWIST_PY code/axiclass/early_late_spa.py ax_spa_lcdm_halofit_desy5'
FROM mambaorg/micromamba:1.5.10
USER root
RUN apt-get update && apt-get install -y --no-install-recommends git gcc g++ gfortran make ca-certificates \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /twist
COPY . /twist
ENV TWIST_BUILDS=/opt/axiclass COBAYA_PACKAGES_PATH=/opt/cobaya_packages TWIST_RESULTS=/twist/fit_results
RUN mkdir -p $TWIST_BUILDS $COBAYA_PACKAGES_PATH && bash environment/setup_twist_env.sh
ENV TWIST_PY=/opt/conda/envs/twist/bin/python PATH=/opt/conda/envs/twist/bin:$PATH
