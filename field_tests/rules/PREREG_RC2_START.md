# PREREG_RC2_START — rung R-C2: does the Weave set the dark thread's starting height? (locked D1642, 2026-11-19 16:30 CT)
Conjecture tested (C-start, WEAVE_POSTULATES): the Y-fork / basin flow places the dark thread in its 1% window (D1628).
Mapping (derived): the plateau 1 − 7.30 e^{−βψ} is 1 − 7.30 y^{−2} with y = e^{βψ/2} = Im τ_Λ, so amp = 7.30/y².
Computations:
Q1 (frozen?): for the dark thread, the ratio m_eff²/H² = |V''|/H² at its window position, at the end of inflation, at BBN and today, using V_Λ from D1628. If ≪ 1 until today, the field cannot have moved since inflation, and no post-inflation dynamics (Y-fork, basins) can set its height.
Q2 (prior probability): with a frozen field the start is an initial condition. The Weave's natural measure is the SL(2,Z)-invariant hyperbolic area on the fundamental domain (as in PREREG_BASINS), total π/3. P(window) = ∫ dy/y² over the window (x-width 1 at y > 1) / (π/3), using each β's best amp and window width Δln(amp) from field_tests/results/GENESIS_DE/tuning.json.
Q3 (quantum spread during inflation): ΔΦ ≈ (H_inf/2π)√N for N = 60, H_inf = 2.4 × 10⁻⁶ M_P (Weave), compared with the window width in field units, Δψ = Δln(amp)/β.
Reading set in advance: C-start SUPPORTED if Q1 shows the field can move before today AND P ≥ 5%. If the field is frozen, C-start is FALSE and P is reported as the measured tuning of the Weave start: < 1% "tuned"; 1–5% "mild".
Script: field_tests/scripts/rc2/run.py
