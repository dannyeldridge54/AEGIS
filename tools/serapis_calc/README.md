# serapis_calc
Verified building blocks (Eisenstein E(τ,s), SERAPIS potentials, consistency relation, exponent rule).
Rule: run `python3 -m tools.serapis_calc.selftest` from the repo root before every locked run; it must exit 0.
Works here and on Ubuntu (needs python3, numpy, scipy, sympy, mpmath: `pip install numpy scipy sympy mpmath`).
Each function is cross-checked against an independent result (lattice sum, modular invariance, symbolic limits, published numbers).
