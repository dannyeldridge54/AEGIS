# PREREG_RW12_K1_THREAD — the Z₂-protected α leak for a k = 1 modular thread ending at U = i
Locked 21 Nov 2026 before computing. AI-assisted. Script theory/tests/rw12_k1.py; result field_tests/results/rw12_k1.json.

## Why (from RW3 R2, run 1, which needs no ODE)
The Weave tilts √2 and 2√2 are exactly k = 1 (K = −ln(−i(U−Ū))) with y⁻¹, y⁻² corrections, and the ζ(5) tilt 4√2 is y⁻⁴.
So take the thread to be a k = 1 modular modulus U = iy rolling along Re U = 0 to the knot i (y = 1).
Canonical: dφ = dy/(√2 y).

## Leak model (fixed now)
The modular-invariant one-loop threshold (Dixon–Kaplunovsky–Louis, N = 2 sectors): 16π² δ(1/g_a²) = −b_a^{N=2} δG,
G(y) = ln(y |η(iy)|⁴). Hence |d ln α_em/dφ| = α_em·b/(4π)·|dG/dφ|, with b ≡ b_em^{N=2} in {1, 12} (O(1) and MSSM-size).
By the Z₂ at i, G′(1) = 0 (checked numerically, |G′(1)| < 1e-10). Quadratic coefficient c = α_em·b/(4π)·|d²G/dφ²|(y=1),
d²G/dφ² = 2(y²G″ + yG′). η from mpmath (40 digits).

## Tests (same bounds as RW6)
- T1: c·Δφ²/2 with Δφ = 0.64 (field at i today: the most favourable case) < 1e-6.
- T2: ζ today = c·d with d = 0.467 (the RW6 estimate) < 1.66e-6.
Verdict: PASS if T1 and T2 pass at b = 12; FAIL if T1 fails at b = 1; TENSION otherwise.
Also report the exact (non-quadratic) G(y) difference between y_today and y = 1 for d = 0.467 and Δφ = 0.64
(y = e^{√2 φ} relation), as a check of the quadratic approximation.
