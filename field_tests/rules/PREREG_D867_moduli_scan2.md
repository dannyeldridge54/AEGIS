# PREREG D867: moduli feasibility scan with the corrected BHK mapping (D866, D857a)
Locked before computing, 2026-11-16. New script; D860 not rerun.
Mapping: Im T₁ = A₂A₃/g_s (4-cycle transverse to the inflaton torus; BHK's tilt modulus), Im T₂ = A₁A₃/g_s, Im T₃ = A₁A₂/g_s; Im S = 1/(2√2π g_s).
v₄ of D833 is the geometric volume of the two non-inflaton tori, A₂A₃, independent of the BHK mapping [derived: the anti-D3 interaction's T⁴ zero mode].
Grid: g_s ∈ [1e-3, 0.5] (log, 30); A₁, A₂, A₃ ∈ [1, 1e5] (log, 60 each).
Constraints: C1 Im S·Im T₁ ∈ [750, 975] (anti-D3 off) or [563, 731] (on); C2 (on only) A₂A₃ ≥ 2e4 g_s; C3 racetrack on cycle k ∈ {1,2,3}: Im T_k ∈ [2, 14.7]; C4 M = M_s e^{−2πσ Im T_k} ∈ [6e10, 5e13] GeV, M_s = g_s^{1/4} M_P/√(4πA₁A₂A₃), σ ∈ {1, ½, ¼}; C5 A_i ≥ 1.
Report per (k, σ, anti-D3): passing count, one example, max of min(A_i) among passing points, and the binding constraint if none pass.
Prediction (pre-stated): anti-D3 ON is impossible for every k (C1 and C2 together need Im S·Im T₁ ≥ 2e4/(2√2π g_s²)·g_s... ≥ ~4e3 > 731); racetrack on T₁ impossible (D866); racetrack on T₂/T₃ passes with anti-D3 off for σ ≤ ½, with the small tori able to exceed string size.
