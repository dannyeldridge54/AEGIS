# PREREG J8 — Janus vs ASPIC through ASPIC's (w_reh, ln ρ_reh) reheating route (follows J7c2/D1008)
Locked 2026-11-17 before any J8 number.
Matching (fetched, Martin & Ringeval 1004.5525): Eq. 13 ln R_rad = [(1 − 3w)/(12(1 + w))] ln(ρ_reh/ρ_end), and the exact Eq. 15
route of J7c2: ΔN* = ln R_rad − N_0 + ln H* − ¼ ln(3H_end²), with physical units fixed by M⁴ = P*/P̂(pivot), ρ_end = 3H_end²
(physical). Both ln R_rad and ΔN* depend on M⁴, so they are iterated together (exact: MS amplitude; Janus: second-order
amplitude, as J7c2). N_0, P* = ASPIC's constants.
ASPIC: foo_x_star(params, x_end, w, ln ρ_reh, P*, bfoldstar) (driver theory/janus/aspic/j8_aspic.f90), spectra via srflow.
Points: the 16 J7b/J7c2 models, w = 0, ln(ρ_reh/M_P⁴) ∈ {−100, −150} (32 points).
Claims/verdict exactly as PREREG_J7c2 (C1–C3; C5 pivot error reported; C6 flag if ASPIC's median ΔN* error > 0.5).
