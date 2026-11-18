<!-- AEGIS-FP IHYE6X4XD7NSVAZ2 · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License) -->
# serapis_calc
Verified building blocks (Eisenstein E(τ,s), SERAPIS potentials, consistency relation, exponent rule).
Rule: run `python3 -m tools.serapis_calc.selftest` from the repo root before every locked run; it must exit 0.
Works here and on Ubuntu (needs python3, numpy, scipy, sympy, mpmath: `pip install numpy scipy sympy mpmath`).
Each function is cross-checked against an independent result (lattice sum, modular invariance, symbolic limits, published numbers).

Speed: `ms.spectra_fast` integrates all k-modes in one vectorised ODE with exact de Sitter initial modes; about 3.5x faster; validated for n_s and r only (selftest L4e). For alpha_s use `ms.spectra` (and check Bunch-Davies convergence, L4c). Locked runs state which one they use.
