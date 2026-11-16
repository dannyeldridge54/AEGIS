# PREREG D815: exact MS for Chronos (τ = i) at the corrected T_R (accuracy queue 6a; Jl tick 54)
Locked before computing, 2026-11-16.
Code: theory/modular/running_d632.py lines 1–41 (the D632/D642 MS code for the τ = i two-term potential), exec'd unchanged as D642 does.
K4: two-term 1.3e-4 at N* = 46.08 must reproduce D642 (results/running_nstar_d642.txt).
(a) D729's 8 rows: ε ∈ {1.3e-4, 1.6e-4} at the N* values read from results/chronos_tr_d729.txt (49.95, 48.38, 50.31, 48.75; 49.93, 48.40, 50.30, 48.76).
(b) ε window: ε ∈ {1.30, 1.35, 1.40, 1.45, 1.50, 1.55, 1.60}e-4 at N* = 48.38 and 50.31 (the bracket extremes). For each N*, find the ε range where n_s ∈ [0.970, 0.975] AND r ∈ [4.8, 5.7]e-4 (frozen τ = i band).
Compare with D729's SR values (n_s 0.9720–0.9765, r 4.63–5.34e-4; "band met only for ε ≈ 1.40–1.46e-4").
Paper sentences updated to the MS values.
