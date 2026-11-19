# PREREG_RB5_JUNO — rung R-B5: TM2 against JUNO's first data (locked D1652, 2026-11-19 17:00 CT)
Data: JUNO first results (arXiv:2511.14593): sin²θ₁₂ = 0.3092 ± 0.0087 (NO). NuFIT 6.0: 0.307 (+0.012/−0.011), using σ = 0.012 on the upper side; it is independent of JUNO (solar + KamLAND).
Prediction: TM2, sin²θ₁₂ = 1/(3cos²θ₁₃), with sin²θ₁₃ = 0.02195 ± 0.00056 (propagated).
Reading set in advance: EXACT TM2 survives if it is within 3σ of JUNO alone. Also report the deviation from the inverse-variance combination of JUNO and NuFIT. If exact TM2 fails, the Weave's escape is C-off (a τ_ν offset from i, D1618), and the shift needed, Δsin²θ₁₂, is reported.
Script: field_tests/scripts/rb5/run.py
