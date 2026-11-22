# PREREG D2106: the breathing torus, a long-running banded search with an in/out pulse each band (Danny 08:43). Locked before running.

**Space:** T⁶/(Z₂×Z₂), tilted T₃; filters and goalposts exactly as D2103/D2105 (PS 3 + 3, tadpole + K, fitted-K confinement, α_s within 2σ, M_s ≥ 4e15).

**Bands** (alternately the grid grows, then the wrap range L):
- grid Q_k = {p/q : 1 ≤ p, q ≤ Q}, restricted to [1/Q, Q];
- B1 (L = 4, Q = 4), B2 (5, 4), B3 (5, 5), B4 (6, 5), B5 (6, 6), and so on.

**Each band breathes:**
1. **OUT-1:** scan each χ in the band grid not already scanned at ≥ this L (60 s per χ).
2. **IN:** re-test every catalogued PS model whose χ is in the grid, using this band's hidden-brane set.
3. **OUT-2:** for every exotic-safe model, probe its 36 neighbours (each visible stack, each wrapping integer ±1) at the same χ.

**Catalogue:** tools/seed/torus/catalog.jsonl, one line per PS model. Fields: band, phase, χ, wrappings, Re z, α_s, M_s, exotic-safe flag, ring/visible ratios, **direction** (ln χ₁, ln χ₂, ln χ₃), and for OUT-2 the move. A checkpoint (state.json) makes the run resumable.

**Stop rule:**
- **NULL** after 2 consecutive bands with no new exotic-safe model and no improvement in the best |Δα_s|;
- or a hit (report immediately);
- or Danny says stop.

Each process runs ≤ 110 min, then resumes from the checkpoint.

**Verdict per band:** hits / near / 0.09 look-elsewhere, as before.
