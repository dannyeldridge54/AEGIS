# PREREG D823: can a multiplicative BHK correction tilt the τ = i plateau in place of ε? (accuracy queue 9; Jl tick 61)
Locked before computing, 2026-11-16.
Model: V = [I²/(I²+1)]·[1 + C(E(τ,2) − E(i,2))] along the imaginary axis (x = 0), with ε = 0. I is the paper's |j − 1728| invariant from running_d632.py, and E is Ese from inflaton_ad_d790.py (both unchanged). Family convention φ = ln y/√2.
MS code: running_d632.py lines 1–41 exec'd unchanged; V redefined only through the potential function.
Scan C ∈ {0, 2e-7, 4e-7, 6e-7, 8e-7, 1e-6, 1.5e-6} at N* = 46.08 and 49.21. Report n_s, r, α_s and y*.
Question: the C range that gives n_s 0.970–0.975 (the frozen τ = i band), and whether r and α_s land in the frozen ranges (r 4.8–5.7e-4; α_s −(8.6–9.9)e-4).
K4: C = 0 must reproduce Kairos (D642: n_s 0.9587 / 0.9612).
Caveat stated in advance: the vacuum is then massless (octic, as Kairos), so N* is the stiff-phase value; a separate mass source is still needed. A natural BHK size is C ~ 1e-7 – 1e-6 (D689, D696).
