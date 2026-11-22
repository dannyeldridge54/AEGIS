# PREREG D2009: Extra inflaton decay channels for T_R. Formulas and inputs locked; no new fit.
**Inputs (from the D-notes, unchanged):**
- Γ_D3 = κ m_φ³/M_P², with κ = 12·4/(128π) = 0.119 (12 SM gauge bosons, n = 1; D1665);
- m_φ = 4.9e12 GeV; M_P = 2.435e18 GeV;
- T(Γ) = (90/(π² g*))^{1/4} √(Γ M_P), with g* = 106.75;
- T_D3 = 1.34e9 GeV;
- visible flux share x = 0.279 (amplitude ∝ x, so Γ_vis = x² Γ_D3; T_vis = x T_D3 = 3.74e8; D1801).
- **Target:** T_vis ∈ [1.54e9, 2.09e9] GeV (D-notes 19802).

**Channels (each computed exactly as written):**
- **C1, gaugino pairs.** For a modulus, Γ(φ → λλ) ∝ (m_{1/2}/m_φ)² Γ_gauge (helicity suppression). Inputs: m_{1/2} ~ wino 0.66–1.85 TeV.
  - Expected negligible. It is reported only as a check.
- **C2, hidden gauge sector with f_hid = S** (coupling share x_h = 1), with N_h gauge bosons.
  - Γ_tot = Γ_D3 (x² + N_h/12).
  - If each sector thermalises separately and the energy splits by branching ratio: T_vis = (Γ_vis/Γ_tot)^{1/4} · T(Γ_tot).
  - Evaluated for N_h = 0, 12, 248 (one E8), 496 (E8×E8 hidden), with no other choice.
  - **Conflict flag, stated now:** the model card says "only our side is heated" (D1801/U21 map). So C2, if it works, **contradicts a model statement**, and must also pass ΔN_eff (dark radiation from the hidden sector).
- **C3, moduli mixing.** S mixes with T by angle θ, so the visible amplitude becomes (x + θ·∂_T f_vis/Re f_vis).
  - θ is not derived in the notes, so C3 is **recorded only as the θ needed** (no fit claimed).

**Pass:** a channel passes only if T_vis lands in the target **and** its other filters pass (ΔN_eff < 0.3 for C2; the gravitino box T_R ≤ 3e9).

*Disclosure:* while drafting, a rough mental estimate of C2 with N_h = 248 gave T_vis ≈ 1.5e9. The lock was written after that estimate; the formula and N_h list were not changed because of it.
