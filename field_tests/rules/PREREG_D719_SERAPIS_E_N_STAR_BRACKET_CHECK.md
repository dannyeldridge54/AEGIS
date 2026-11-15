# PREREG D719: SERAPIS-E N-star bracket check
Locked 2026-11-15 before computing. Script: theory/modular/nstar_check_d719.py. Output: field_tests/results/nstar_check_d719.txt.

## Question
Check, from first principles, the N* = 48.4–49.9 bracket used in the frozen SERAPIS-E lock (D693, from the D692 estimate) by the standard matching equation.

## Inputs (fixed now)
- SERAPIS-E V/V0 = P_E(1 + CÊ), C = 1.15e-6 (mid); V* from the CMB normalisation V* = (3π²/2) A_s r* M_P⁴ with A_s = 2.1e-9 and r* from the model; ρ_end = (3/2)V_end at ε = 1; matter-like reheating (w = 0) from the end of inflation to T_R; T_R ∈ {1e6, 1e7, 1e8} GeV (D692 bracket) plus {1e4, 1e10} for context; g* = 106.75 (g*s the same).
- Matching equation (Liddle & Leach 2003, eq. for general w): N* = 66.89 − ln(k/a0H0) + ¼ ln(V*/M_P⁴) + ¼ ln(V*/ρ_end) + (1−3w)/(12(1+w)) ln(ρ_reh/ρ_end) − (1/12) ln(g*/106.75)... with k = 0.05 Mpc⁻¹, H0 = 67.4 (k/a0H0 = 222.4); solved self-consistently with r*(N*) and V_end from the model.

## Method
Iterate N* ↔ (r*, V*/V_end) using the D691/D698 slow-roll code until |ΔN*| < 0.01.

## Decision rule (written before running)
- CONSISTENT if the computed N* for T_R = 1e6–1e8 GeV lies within 48.4–49.9 ± 0.5.
- INCONSISTENT otherwise → a correction note to D692/D693 (no retuning of the frozen bands; record the size of the shift in n_s it would imply).
- What happens if the run crashes or times out: fixes only through D719_DEVIATIONS.md, written before any rerun.

## Labels
Mark every number in the write-up as computed / estimate / literature / from memory.
