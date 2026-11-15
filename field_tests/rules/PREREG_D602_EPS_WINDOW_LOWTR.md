# PREREG D602: ε window for two-term SERAPIS at the D601 reheating temperature (locked before computing)
Machinery: the D578 nstar/infl functions (slow-roll count, model 'e'), except that T_RH is FIXED at {1e3, 1e5} GeV instead of being derived from c_Γ. Phases: octic (w = 3/5 bound and w = 0 bound) from ρ_end to ρ_x, then matter until ρ_R. One N* iteration, as in D578.
Correction: add the D588 exact-MS offset Δn_s = −0.0003 to every reported n_s (the midpoint of D588's −0.0002 to −0.0004). y* is reported as computed, with a note that D588 lowers it by ~0.4.
Grid: ε ∈ {1.0e-4, 1.3e-4, 1.6e-4, 2.0e-4, 2.5e-4}.
Window: ε is allowed if every row (both T_R values, both w bounds) is home-safe (y* ≤ 25 after the −0.4 D588 shift) and has |n_s − 0.9728| ≤ 2 × 0.0027.
Report N*, y*, n_s (corrected), r, and the allowed set. Leptogenesis is via AD (D599–D601) and not checked here.
Fixes go in PREREG_D602_DEVIATIONS.md, written first.
