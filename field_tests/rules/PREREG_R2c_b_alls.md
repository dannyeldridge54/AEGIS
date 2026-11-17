# PREREG R2c-b — full LO Sommerfeld thermal σ_eff (all charge and spin sectors) — locked 2026-11-17, before any code or run
Sources: hep-ph/0610249, Eqs. 2–8, 11 and 13 (recorded in the sourcing D-note this tick). Units: πα₂²/M². The constants are those of sommerfeld_nlo (LO).
Sommerfeld factors per sector, as functions of each pair's own relative v (E = Mv²/4 above that pair's threshold):
- **(00, +−) S=0:** coupled. Rows 0 and 1 come from two_channel_open (E > 2δm, measured from the 00 threshold) and wino_s_nlo(nlo=False) (row 0, closed side). Charged-pair-incoming row 1 is defined only above its own threshold: χ⁺χ⁻ in with relative KE E₊ = E − 2δm ≥ 0.
- **+− S=1:** single_channel, V = −α/r − α₂c_W²e^{−m_Z r}/r, alpha_tail = +α.
- **0± (S=0, 1):** single_channel, V = −α₂e^{−m_W r}/r, alpha_tail = 0.
- **±± S=0:** single_channel, V = +α/r + α₂c_W²e^{−m_Z r}/r, alpha_tail = −α.
Pieces, all spin-weighted (assumption stated in the D-note):
- ⟨σ00 v⟩ = ¼·2·⟨s₀Γs₀†⟩/2·…, which equals ¼·c·⟨sΓs†⟩ with Γ = ½[[2,√2],[√2,3]], as R2c-a with c = 2.
- ⟨σ+− v⟩ = ¼·⟨s₁Γs₁†⟩ + ¾·(25/24)⟨S_{+−,1}⟩.
- ⟨σ0± v⟩ = ¼·½⟨S_{0±}⟩ + ¾·(25/24)⟨S_{0±}⟩.
- ⟨σ±± v⟩ = ¼·2·½⟨S_{±±}⟩.
Eq. 13 sum over ordered pairs: σ_eff = (4/g_eff²)[σ00 + 4·w₁·σ0± + 2·w₂·σ+− + 2·w₂·σ±±], with w₁ = (1+δm/M)^{3/2}e^{−xδm/M} and w₂ = w₁².
Maxwell average: as R2c-a, with the full normalisation. Grids: 40/80 log-spaced v on [1e-3, 2] for the single channels, plus the R2c-a scheme for the coupled sector. Converged iff within 1%.
Output: R_eff = σ_eff(Sommerfeld)/σ_eff(Born) at x = 20, 25, 30, for M = 2000 and 2842.
Scored tests:
- T1: all potentials → 0 gives R_eff = 1 within 1e-4.
- T2: convergence within 1%.
No physics pass/fail (the relic mass comes in R2d).
