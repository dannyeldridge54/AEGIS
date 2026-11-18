# PREREG D1294 — "every shape fits inside the others": how many hexagonal planes (A2) sit inside each champion? (locked before computing)
A hexagonal plane = the span of two minimal vectors u, v with u·v = −½|u|² (120°), which carries an A2 (hexagonal) sublattice
with 6 minimal vectors. Count = (#min vectors) × (#min vectors at 120° to a given one) / 12.
## Predictions (before computing)
- D4: 24 roots, 8 at 120° each → 16 hexagons. E6: 72 × 20 / 12 = 120. E7: 126 × 32 / 12 = 336. E8: 240 × 56 / 12 = 1120.
- Leech: 196560 minimal vectors, 4600 at 120° (u·v = −2) to each → 196560 × 4600 / 12 = 75,348,000 hexagonal planes.
- Every hexagonal plane found is exactly the SERAPIS-E vacuum shape τ = ρ (checked via the 2×2 Gram of (u, v) ∝ [[2,−1],[−1,2]]).
## Method: exact enumeration of minimal vectors (lattice_lab norms), inner products; for Leech, the distribution for several
minimal vectors (Co0 acts transitively — literature), reported per vector.
