# PREREG D2140: τ_q moduli cosmology, negative-space nodes N4(a)–(c) (Danny 19:25: "keep running it until it's fully balanced")
Locked before computing. Labels: [S] standard formula, [R] value from the record, [E] estimate.

## Inputs
- m_τq = 2e10 GeV, the record's lower edge. Also report 1e11 GeV.
- φ0 = 1 M_P, the record's default. Also report the φ0 needed to pass.
- T_R = 1.34e9 GeV [R, WEAVE_FACTS].
- m3/2 = 2.6e5 GeV and gravitino lifetime τ_3/2 = 1.4e-3 s [R, D1946].
- Wino mass m_w = 0.7 TeV [R].
- Wino budget: Ω_w h² ≤ 0.036, i.e. ≤ 30% of DM [R].

## Formulas
- **Decay:** Γ = m³/(4π M_P²) and T_d = (90/π² g*)^{1/4} √(Γ M_P), with g* = 106.75 [S].
- **(a) Dilution:** D = T_R φ0²/(6 T_d) [R, D1766]. PASS if D ≤ 1e3, the leptogenesis room [R, F2].
- **(b) Moduli-induced gravitinos:**
  - Y_3/2 = 2 Br_3/2 · (3 T_d / 4 m) · min(1, D) [S, the modulus-domination yield; the min(1, D) factor is E].
  - Three readings of Br_3/2: 0.01 and 0.1 (generic, Endo–Hamaguchi–Takahashi 2006), and (m3/2/m)², the suppressed case for a supersymmetrically stabilised, sequestered modulus [E].
  - Each gravitino gives one wino.
  - Re-annihilation at T_3/2, the temperature at t = τ_3/2 with g* = 10.75, caps the yield at Y_cap = H/(s⟨σv⟩).
  - Three readings of ⟨σv⟩: 2.5e-25, 1e-24 and 3e-24 cm³/s (tree level up to Sommerfeld) [E].
  - Final yield Y = min(Y_3/2, Y_cap). Then Ωh² = 2.744e8 · m_w[GeV] · Y.
- **(c)** Report whether this channel alone can supply the record's non-thermal wino share. Report only.

## Verdict for (b)
- **PASS:** Ωh² ≤ 0.036 at generic Br = 0.01, for the median σv.
- **CONDITIONAL:** passes only with the suppressed Br.
- **FAIL:** no reading passes.

No reruns to chase results.
