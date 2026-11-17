# PREREG C5 — GW forecast: can LIGO tell SLy from AP4? (Djl C) — locked 2026-11-17
Inputs: D1099 chain (Λ_1.4 SLy 295.6, AP4 247.6; 6PN tidal phase), the A2c PSD method (lalsimulation, tabulated and interpolated), gw.amplitude0 (0PN amplitude).
System: 1.4 + 1.4 M_⊙, single detector, optimal orientation, f = 20 Hz to f_ISCO. Distances 40 Mpc (GW170817-like) and 100 Mpc.
PSDs: SimNoisePSDaLIGO140MpcT1800545 (O4-like) and SimNoisePSDaLIGOAPlusDesignSensitivityT1800042 (A+).
Overlap O = max over (t_c, φ_c) of |∫ w(f) e^{i(Δψ(f) + 2πf t)} df| / ∫ w df, with w = |h|²/S_n and Δψ = the SLy − AP4 tidal phase. The maximisation over t uses a bounded scalar search over ±10 ms.
Criterion: distinguishable if 2(1 − O)ρ² > 1. This is the Lindblom–Owen–Brown 2008 indistinguishability criterion, written from memory and labelled; it is not fetched.
Reported per (PSD, D): ρ, 1 − O, 2(1 − O)ρ², DISTINGUISHABLE or NOT, and the ρ needed.
Caveats fixed in advance: 0PN amplitude, inspiral-only tides, no 6.5/7PN tidal terms, single detector, no parameter degeneracies (masses and spins fixed). So this is an optimistic upper bound on distinguishability.
Script theory/wiring/c5_eos_forecast.py (written after this lock).
