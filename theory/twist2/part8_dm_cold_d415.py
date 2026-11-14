"""D415 (locked PREREG_D415_PART8): Part 8 (gravity-only DM, 100–200 TeV) — is DM born in χ̃ decays cold enough? AI-assisted.
χ̃ decays at m_χ̃ ≈ 0.052 M_P (D118) = 1.27e17 GeV around T_prod ≈ T_RH ≈ 5.6e14 GeV; DM momentum at birth ≤ m_χ̃/2 (two-body upper bound).
p ∝ 1/a ∝ T (entropy-conserving, ignoring g* steps: conservative within ×2): non-relativistic at T_NR = m_DM T_prod / p_birth.
Lyman-α: thermal warm DM must be ≳ 5 keV, i.e. non-relativistic by T ~ keV; require T_NR ≥ 1 MeV for a wide margin."""
MP = 2.435e18; mchi = 0.052 * MP; Tp = 5.6e14
for mdm in (1e5, 1.5e5, 2e5):
    pb = mchi / 2; TNR = mdm * Tp / pb
    print(f"m_DM {mdm:.1e} GeV: p_birth ≤ {pb:.2e} GeV (p/T = {pb/Tp:.0f}), T_NR ≥ {TNR:.2e} GeV  → margin over 1 MeV: {TNR/1e-3:.1e}")
