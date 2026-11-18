<!-- AEGIS-FP B6X6NUPF7FDOEFIG · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License) -->
# Referee pass R3 on the v3.2 draft (whole draft, cross-section numeric check; 2026-11-16, D899)
Scope and method: the whole serapis_v3.2_draft.tex (89 kB) checked section against section for the quantities N*, T_R, ε, m_ν₁, m_{3/2}, the wino window, Σm_ν and the n_s/r bands, and for references to results corrected today (D880a, D888a, D892 withdrawn, D792 superseded); plus prediction_sheet.md. This is a targeted consistency read (keyword-anchored), not a line-by-line prose review.

## Major
1. **τ = i Affleck–Dine window uses a superseded reheating temperature.** The AD section quotes m_ν₁ ≃ 2e-13–9e-11 eV "for T_R = 10³–10⁵ GeV" (D646, from the constant-W₀ era), and the Consequence paragraph and prediction_sheet.md row 15 inherit "≲ 1e-10 eV at τ = i". The draft's own corrected τ = i reheating is T_R ≈ (0.8–3)×10⁶ GeV (D727, D815). With the same D646 yield, that gives m_ν₁ ≈ 1.6e-10–2.7e-9 eV (arithmetic, median to max Q). The τ = i window must be restated at the corrected T_R (and D653's thermal check extended to T_R ~ 3e6 GeV). Same lesson as D894: one formula, consistent inputs.

## Minor
2. **Stale T_R ~ 10⁵ GeV.** The proton-stability paragraph says the 2⊕1 splitting ΔM/M ≈ 0.08–0.5 restores "T_R ~ 10⁵ GeV (estimate; D690)". The reheating section says that with the unsuppressed decay T_R ≈ (0.8–3)×10⁶ GeV does not depend on the splitting (D727). Update the proton paragraph's clause to the D727 value or mark D690 superseded.
3. **CP-phase paragraph points to the superseded ρ route.** "The post-hoc self-diluted ρ history of Sec. limits needs no such phases": ρ's preferred route is now LH_u AD (D880/D895), whose condensate phase must itself be spontaneous (as the ρ caveat says). Reword: the ρ AD route needs a spontaneous condensate phase; the superseded self-diluted history needed none.
4. **Cap paragraph's ρ example.** It cites the self-diluted ρ history as the example outside the bounds; fine as a statement, but add "(superseded as ρ's preferred route, D895)" to avoid implying it is the live ρ history.

## Checked, consistent
- Wino window 0.67–1.85 TeV and m_{3/2} = (2.5–7)×10⁵ GeV agree across the supergravity section, the SERAPIS-E section and the prediction sheet.
- Σm_ν = 0.0587 eV (NO floor) and the DESI bound agree in body and sheet.
- N* = 46–49 (τ = i), 48.4–49.9 (ρ frozen) are used consistently with their stated origins.
- ε at τ = i (abstract and body) and the ρ numbers updated in D898 agree.

## Responses (D900–D901)
1. RESOLVED. Locked recomputation D900: at the corrected τ = i reheating T_R = (0.8–3)e6 GeV the window is m_ν₁ ≈ 1.6e-10–2.7e-9 eV, and the D653 thermal check still passes (φ/T ≥ 4.9e4). AD section, Consequence paragraph (now gives both vacua's windows) and prediction_sheet row 15 updated; D646's numbers kept as the record at the old T_R.
2. FIXED: proton paragraph now gives T_R ≈ (0.8–3)e6 GeV from the unsuppressed decay (D727), superseding D690's 1e5 GeV.
3. FIXED: CP-phase paragraph now says ρ's LH_u AD route needs a spontaneous condensate phase.
4. FIXED: cap paragraph marks the self-diluted ρ history as superseded (D895).
