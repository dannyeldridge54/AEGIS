# Referee pass R2 on the v3.2 draft (text changed since the D871 commit d14dfac; 2026-11-16, D894)
Scope: serapis_v3.2_draft.tex lines changed since D871, read against the abstract, Sec. VII, the caveats list, and prediction_sheet.md.

## Major
1. **Two yields for the same Affleck–Dine mechanism disagree.** At τ = i the draft's own numerical integration (Sec. "Affleck–Dine along LH_u", D646/D646a) gives m_ν₁ ≃ 2e-13–9e-11 eV for T_R = 1e3–1e5 GeV and states the yield is independent of m_soft. At ρ the caveats (D880) use the Fujii–Hamaguchi–Yanagida scaling n_B/s ∝ m_ν₁^{-3/2}·m_{3/2}, giving m_ν₁ ≈ 4e-9–7e-8 eV at T₂ = 1e5–1e6 GeV. At T = 1e5 GeV the two differ by a factor ≈ 49 in m_ν₁ (≈ 340 in yield at fixed m_ν₁). The source is the m_{3/2} (A-term) dependence: D646 used Hubble-induced A-terms (c_H = |a_H| = 1), FHY a low-energy A-term ∝ m_{3/2}. The paper must either use one treatment for both vacua or explain why the two vacua differ (at ρ, m_{3/2} ~ 1e5–1e6 GeV enters; at i the D646 integration says it does not). Until resolved, the ρ m_ν₁ window and the Weinberg bound (D891, which uses that window) carry this uncertainty.

## Minor
2. **Stale general statement.** "Consequence. If Affleck–Dine is the source, baryogenesis requires … m_ν₁ ≲ 1e-10 eV" reads as general. With the ρ route (D880) the window at ρ is different (see item 1). Restrict it to τ = i or update it after item 1.
3. **Abstract omits the ρ chain's conditions.** It says LH_u AD "gives the observed asymmetry inside the frozen band for an essentially massless lightest neutrino (post hoc)". The body now attaches five conditions (Γ₂-singlet leptons, two extra singlets, E₄ protection, the post hoc lift ε, instanton-only Weinberg term; D893). Add "under conditions on the lepton sector".
4. **Abstract, fitted parameters.** "The tilt at i and ρ is fitted" — the ρ lepton lift ε ≈ 2e-3 (D888a–D890) is a second fitted small number on that branch; mention it in one clause, or say "fitted small parameters".
5. **prediction_sheet.md is stale on ρ baryogenesis.** Line 59 still names the "SERAPIS-E/ρ, self-diluted" history (D792, T₂ ≈ 150–1100 GeV, outside the band) as ρ's route; D880 superseded it with LH_u AD inside the band. Line 15's m_ν₁ row covers τ = i only. Add a ρ row (post hoc, D880, with the item-1 caveat) and mark D792 as superseded.

## Checked, consistent
- ε at τ = i: abstract (1.3–1.6)e-4 and the corrected-reheating window (1.40–1.45)e-4 agree with Sec. "origin of ε" and the τ = i item.
- T₂ ≳ 1e5–1e6 GeV agrees between the ρ caveat, footnote e of the prediction table, and D880.
- The new D885–D893 sentences cite their D-notes and carry post hoc / estimate labels.
