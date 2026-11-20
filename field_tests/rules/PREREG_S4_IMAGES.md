# PREREG_S4_IMAGES — BIG LOOP Q1: under modular S₄, which images of i give TM1 and which give TM2? (locked D1668, 2026-11-20 00:12 UTC)
Setup: S₄ ≅ Γ₄ triplet in the NPPT basis, ρ(S) = ½[[0,√2,√2],[√2,−1,1],[√2,1,−1]], ρ(T) = diag(1, i, −i). Check: S² = 1, T⁴ = 1, (ST)³ = 1, and the closure has 24 elements (else STOP).
Charged leptons at the ρ-image fixed by ST (Z₃): U_e = eigenvectors of ρ(ST). Neutrinos at an image of i: its residual Z₂ is a conjugate g = hSh⁻¹ of S. The unique-eigenvalue eigenvector of ρ(g) is a fixed column of U_ν, so the fixed PMNS column is |U_e† v|².
Count, over all distinct conjugates of S: the number giving TM1 (2/3, 1/6, 1/6 up to permutation), TM2 (1/3, 1/3, 1/3), or other.
Reading: this answers "if the neutrino modulus lands on a random image of i, how often is the pattern TM1?". It is a pure group computation. Equal weight per conjugate is assumed (basin weights per image are left for later).
Script: field_tests/scripts/s4img/run.py
