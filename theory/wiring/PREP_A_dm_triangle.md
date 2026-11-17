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
## 2026-11-17 13:55 UTC — NLO (D1087)
- 2009.00640: resonance 2.282 (LO) → 2.419 TeV (NLO); relic 2.886 → 2.842 TeV.
- The NLO fit is Eq. 3.25 (off-diagonal, in L = ln(m_W r), x0 = 555/94) and Eq. 3.26 (diagonal). The full text is needed to code it.
- Our LO solver reproduces 2.282 with their inputs (+0.15%).
## 2026-11-17 14:20 UTC — NLO potential sourced (2009.00640 via the arXiv PDF; text converted from the PDF, so verify against the journal)
- Eq. 3.25: δV_{00→+−} = (2595 α₂²/(π r)) × { exp[−79(L−787/12)(L−736/373)(L−116/65)(L²−286L/59+533/77) / (34(L−512/19)(L−339/176)(L−501/281)(L²−268L/61+38/7))] for x < x0 ; −exp[−13267(L−76/43)(L−28/17)(L+37/30)(L²−389L/88+676/129) / (5(L−191/108)(L−256/153)(L+8412/13)(L²−457L/103+773/146))] for x > x0 }, with x = m_W r, x0 = 555/94, L = ln x.
- Eq. 3.26: δV_{+−→+−} = δV^{∞}/(1 + (32/11)x^{−22/9}) + δV^{0}/(1 + (7/59)x^{61/29}) + (α/r)[(−1/30 + (4/135)ln x)/(1 + (58/79)x^{−17/15} + (1/30)x^{119/120} + (8/177)x^{17/8})].
- Eq. 3.14: δV^{0} = (α₂²/(2πr))(−(19/6) ln(m_Z r) + 4.92585).
- Eq. 3.18: δV^{∞} = (α²/(2πr))(80/9)(ln(m_Z r) + γ_E).
- LO (Eq. 2.8, ¹S₀): [[0, −√2 α₂ e^{−m_W r}/r], [·, −α/r − α₂ c_W² e^{−m_Z r}/r]] + 2δm on the +− diagonal; this is the same as sommerfeld.wino_s.
- Inputs: on-shell α = 1/128.943, c_W = m_W/m_Z, α₂ = α/s_W², m_W = 80.385, m_Z = 91.1876, δm = 0.1641 GeV.
- Normalisation ambiguity: is δV_{00→+−} added to the matrix entry as is, or with √2? A1c pre-declares "as is" as the primary convention.
## 2026-11-17 15:57 UTC — wino γ-line (prep for lock A2)
- Source 1307.4082 (Cohen, Lisanti, Pierce, Slatyer), as fetched:
  - σ_i v = c_i Σ s_ij Γ_jj' s*_ij' (Eq. A8), with c = 2 for identical χ⁰χ⁰. Same normalisation as our A1 (σv_tot = 2 sΓsᵀ, free s = (1, 0)).
  - At tree level only Γ^γγ_{+−,+−} ≠ 0. The chargino normalisation is σ^γγ_{+−,+−} v = πα²/M₂² (Eq. B5).
  - So σv(χ⁰χ⁰ → γγ) = 2|s_{+−}|² πα²/M² [derived from A8 + B5, taking c = 1 for the distinct-particle χ⁺χ⁻ state; to confirm].
  - H.E.S.S. comparison quantity: σv_γγ + ½σv_γZ (Fig. 1 caption).
  - The paper says γZ uses "the same structure" but gives no γZ normalisation in the fetched text.
  - One-loop corrections reduce the line by ×3–4 (their caveat; this is our A7b "one-loop bracket").
- Still needed for the A2 lock:
  - (a) A sourced Γ^γZ_{+−,+−} (or the ratio σ_γZ/σ_γγ). Candidate: Hisano et al. 2004/2005, or Beneke et al. resummed line papers.
  - (b) The H.E.S.S. line limit at 1–3 TeV (Einasto, 2018, arXiv:1805.05741) as numbers at stated masses.
