# PREREG D813: exact MS spectra for the self-diluted ρ history (accuracy queue 6a; Jl tick 52)
Locked before computing, 2026-11-16.
Code: theory/modular/serapis_e_exact_d692.py UNCHANGED (MS solver = running_d632 verbatim; same potential and convention), importing everything above its scan loop. The only change is the scan: C ∈ {1.0e-6, 1.15e-6, 1.3e-6} × N* ∈ {44.89, 45.15, 45.55} (D793's T₂ = 150, 330, 1100 GeV), plus K4: C = 1.0e-6, N* = 48.4 must reproduce D692.
Report n_s, r, α_s and the differences from D793's SR1 values (n_s 0.9667–0.9703, r 5.127–5.588e-4).
Expectation: |Δn_s| ≤ 0.002 and |Δr|/r ≤ 10% versus SR1 (D635-type corrections).
Rule: the paper and sheet get the MS numbers (post hoc model, allowed); "pending" is removed.
