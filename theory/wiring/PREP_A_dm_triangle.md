# PREP (A) Dark-matter triangle — sourcing log (Djl loop, 17 Nov 2026)
Goal: halo-independent wino test — p_ann(M) = f_eff · ⟨σv⟩(v_rec) / M (× f_wino²) vs the Planck 2018 limit, with the A7b Sommerfeld solver.

## Sourced (tick 1, 13:01 UTC)
- Tree-level wino annihilation χ⁰χ⁰ → W⁺W⁻: (σv) = 2πα₂²/M² — arXiv:1009.5058 Eq. 13.
- Annihilation matrix in the (w⁰w⁰, w⁺w⁻) basis, S-wave spin singlet (NREFT): Γ = (πα₂²/2M²) [[2, √2], [√2, 3]] — arXiv:1712.07142 Eq. 3.4; upper/lower diagonals are half the LO w⁰w⁰ rate and the LO w⁺w⁻ rate. Inclusive LO rates: 2v₀σ₀ = 2πα₂²/M², 2v₁σ₁ = 3πα₂²/(2M²) (Eqs. 2.1a,b).
- CAUTION (same source, footnote 2): refs differ by a factor 1/2 in the off-diagonal element — the basis normalisation of the w⁰w⁰ state must be matched to our solver's potential (1307.4082 App. A: off-diagonal −√2 α_W e^{−m_W r}/r). Implied rule to verify before use: σv = 2 s Γ s† with s = (1, 0) at tree level reproducing 2πα₂²/M².

## Still to source (next ticks)
- Planck 2018 p_ann 95% limit (value and the f_eff convention).
- f_eff(M) for the W⁺W⁻ channel at 0.5–3 TeV (Slatyer 2016 tables or the Planck 2018 paper's convention).
- An independent numerical anchor for the Sommerfeld-enhanced total σv (e.g. a quoted value at the 2.4 TeV resonance or at 1–3 TeV, v ~ 1e-3) to fix the off-diagonal convention.
Then: lock PREREG_A1 (wino p_ann vs Planck), run, D-note.

## Sourced 2026-11-17 (Djl tick A)
- p_ann (Planck 2018): p_ann < 3.2e-28 cm^3 s^-1 GeV^-1, p_ann ≡ f_eff<σv>/m_DM (Slatyer, Les Houches lectures arXiv:2109.02696, citing Planck 2018 VI). CL not stated there → treat as Planck 95% pending a direct quote.
- Earlier bound 4.1e-28 (Planck 2015 / Slatyer 1506.03811).
- f_eff: 1506.03811 gives no W+W- number in text (Fig. 4 only; tables at nebel.rc.fas.harvard.edu/epsilon, not reachable from here).
  Derived bracket (labelled DERIVED, not quoted): paper states high-mass SM-channel CMB limits lie at <σv> ≲ 1–3e-27 (m/GeV) cm^3/s with p_ann < 4.1e-28 → f_eff ≈ 0.14–0.41. e+e-/γ asymptote f_eff ≈ 0.4 (quoted).
  A1 will scan f_eff over [0.14, 0.41] instead of using one value.
- Still missing: one numerical anchor for wino Sommerfeld total σv (needed to lock A1).
