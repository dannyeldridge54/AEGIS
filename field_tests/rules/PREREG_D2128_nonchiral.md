# PREREG D2128: checklist item 6, independent derivation of the non-chiral spectrum (ping-pong R6-1…R6-3 plus the referee's line references). Locked before computing.

**Formulas (all from p.tex):**
- ω on wrapping numbers (Eq. 1-cycle-orbits, lines 533–545), on all tori: (n,m) → (m, −(n+m)). σ, τ and the Z₂ eigenvalues are unchanged; the fixed-point map 1↻, 4→5→6 preserves the reference and second-point order.
- Orientifold image (Eq. OR_on_n+m, line 555, **A** lattice): (n,m) → (n+m, −m), with σ′ = σ and τ′ = τ. On torus i, τ^{Z₂(i)}_{a′} = τ^{Z₂(i)}_a + σ^iτ^i (from −η_(i)(−1)^{σ^iτ^i} with η = −1, line 3077). This is **calibrated by P0**.
- Per-sector quantities:
  - I_ab = ∏ᵢ I^{(i)};
  - I^{Z₂(i)}_ab = I^{(i)}·f_j·f_k, with f_j = I^{Z₂(j),(j)} from **tab:Wilson_signs** (lines 3041–3066), using the relative Z₂^{(j)} eigenvalue on torus j;
  - χ_sector = −(I + Σᵢ I^{Z₂(i)})/4 (Eq. ChiralMatter, line 1181).
- Multiplicities, from tab:beta_coeffs_Kaehler_metrics via φ = (2/N_b)·b^𝒜:

| Sector type | φ |
|---|---|
| No vanishing angle | \|I + ΣI^{Z₂}\|/4 |
| One vanishing angle (on T²_i) | ½·δ_{σ^i}·δ_{τ^i}·(\|I^{(j)}I^{(k)}\| − f_j f_k) |
| All parallel (b ≠ a) | −½·Σᵢ δ_{σ^i}δ_{τ^i}·f_j f_k |

  The adjoints are φ^Adj_x = |χ^{x(ωx)}| (line 1465).

**Locked targets:**
- **P0 (calibration):** Σ_k χ_sector(x, ω^k y) = the engine χ(x, y), and likewise for (x, y′), for all 25 + 25 pairs. **If P0 fails, nothing else is used.**
- **P1:** total φ per pair equals |χ| for ab, ab′, ac, ac′, bc, bd, bd′, be′, cd, cd′, ce′. Every pair absent from Tables 28/29 (other than xx′) has φ = 0. **φ_bc = 1** (single bidoublet).
- **P2:** adjoints: d = 4; a, b, c, e = 0.
- **P3:** φ_ad = **4** (Table 29: 2×[(4,2̄)+h.c.]) or 2 (HRS text, "one pair"). Report which one results.
- **P4:** φ_de′ = 2 ((2,2) + h.c.).
- **Not computed this pass (secondary):** the xx′ sym/anti sectors, which need the conjectured Möbius sign (line 3293).

**Verdict:** PASS if P0–P2 and P4 hold. P3 settles the R6-2 discrepancy.
