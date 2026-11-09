# V8 — Independent reproducibility package

**Goal.** A third party reproduces the headline Spiral Δχ² (SF, one SN set) with one command, from public data.

**Contents.**
- Environment: `micromamba env export -n aegis --no-builds` (WSL) and `pip freeze` (venv312), pinned; AxiCLASS
  coupled + nlfix build reproduced from upstream commit + `patch_coupling.py` + `patch_nlfix.py`, with SHA-256 of
  each patched source file; CAMB 2.0.5 + `DarkEnergyUBField.f90` for UB tests.
- Data: Cobaya `install` manifests for every likelihood (Planck 2018 low-ℓ, ACT DR6 lite + lensing, SPT-3G D1 candl,
  DESI DR2, Pantheon+, DES-Dovekie, Union3), with versions.
- One script: build → gate (reproduce stored χ² at the stored best point to ±0.1) → evaluate; optional full refit.
- Container (Docker/Apptainer) once the env is pinned.
- README in technical terms; expected output and tolerances; known caveats (coupled-build H0 label; nlfix residual).

**Existing pieces.** Zenodo theory-note v2 supplement (28 scripts); verify.py in the public release repo
(the-twist-torsion-cosmology); mirror tests (solver vs Ramos-Hamud 10⁻¹⁰, AxiCLASS mirror 2×10⁻⁵).
**Cost.** Cloud + one PC export step. **Next:** export the PC environment (needs WSL; via the after-S8 queue or Danny).

## Status 9 Nov (step-6 check-in): what is still missing for a one-command reproduction of the SF Pantheon+ Δχ²
1. **Current PC environment record.** `environment.yml` / `pip_freeze.txt` date from 1 Nov, before the coupled, nlfix
   and ULA builds were used for the S8 work. → `cmb-fit/repro/export_pc_env.sh` (Danny: double-click
   `cmb-fit/repro/START_V8_EXPORT.bat`; read-only, a few minutes, safe while fits run) writes `cmb-fit/repro/pc_export/`.
2. **Patched-source hashes.** No SHA-256 of the patched AxiCLASS sources is recorded for any build. → the export hashes
   every .c/.h/.pyx of all six builds and saves each build's diff against the pinned upstream commit (ae9609e).
3. **Likelihood data versions.** Only ACT DR6-lite (git pin) and SPT candl data (commit f22611a) are pinned; Planck
   low-ℓ, DESI DR2, Pantheon+, DES-Dovekie, Union3 data are installed by name, not version. → the export hashes every
   file under the packages folder and records git commits where present.
4. **Union3 is not in `setup_twist_env.sh`'s install list** (the Union3 fits need `sn.union3`). Not needed for the
   Pantheon+ headline; to add when the env file is refreshed from the export.
5. **One-command check.** → `cmb-fit/repro/reproduce_sf.sh` (setup, then `repro_eval.py`: rebuild the likelihoods,
   evaluate the stored Spiral and ΛCDM best points, PASS if each χ² is within 0.1 of the stored value, print Δχ²).
   **Untested**: the cloud has no candl/likelihood data; first real test is on the PC or a clean machine.
6. **Container.** The Dockerfile (7 Nov) has never been built; build and run `reproduce_sf.sh` inside it after items 1–3.
