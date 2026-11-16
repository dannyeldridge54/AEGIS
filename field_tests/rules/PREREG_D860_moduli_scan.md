# PREREG D860 (M.3): is there one moduli point satisfying every requirement of D857/D859?
Locked before computing, 2026-11-16.
Variables: g_s ∈ [0.05, 0.5] (log grid, 25 pts); A₁, A₂, A₃ ∈ [1, 1e5] string units (log grid, 60 pts each). Cases: f ∈ {1, 4π²} (BHK Im ρ₁ = f·A₁); σ ∈ {1, ½, ¼}; anti-D3 on/off.
Constraints:
C1 BHK tilt: Im S·Im ρ₁ ∈ [563, 731] (anti-D3 on, stacks (5,2), N_eff = 3) or [750, 975] (off, (5,1), N_eff = 4), Im S = 1/(2√2π g_s).
C2 anti-D3 safe (on only): A₂A₃ ≥ 2e4·g_s.
C3 racetrack: at least one k with Im T_k = A_iA_j/g_s ∈ [2, 14.7] (N = 5–10, W0 ∈ [1e-4, 0.3], t > 2).
C4 heavy-ν: for that k, M = M_s exp(−2πσ Im T_k) ∈ [6e10, 5e13] GeV, M_s = g_s^{1/4} M_P/√(4π A₁A₂A₃), M_P = 2.435e18 GeV.
C5 all A_i ≥ 1.
Output per case: number of grid points passing all; one example; otherwise the count of points failing each constraint among those passing C1 and C5 (to name the binding one).
Verdict: CONSISTENT for a case if ≥ 1 point passes; INCONSISTENT otherwise.
Prediction (pre-stated): anti-D3 on + σ = 1 is INCONSISTENT for both f; anti-D3 off has passing points for σ ≤ ½.
