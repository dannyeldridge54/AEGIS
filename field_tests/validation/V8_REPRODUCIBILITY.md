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
