# PREREG D400 — does a DESI-fitting no-scale-type quintessence modulus violate α-variation and equivalence-principle bounds at one loop?
(locked 14:15 CT 14 Nov 2026, before running)

Coefficient: theory/alpha_nogo/kl_coeff.py (run before this lock; output: 16π² d(1/g_a²)/d ln x = −b_a with locality weights, MSSM
b = (33/5, 1, −3); d ln α_em/d ln x = 6.97×10⁻³ for K ⊃ −3 ln; no weight + universal-GS solution with x-independent Yukawas and μ).
General k: K ⊃ −k ln(X+X̄) gives −(k/3) b_a and d ln x/dφ = √(2/k).
Script: theory/alpha_nogo/desi_alpha_d400.py. DESI fits (arXiv:2511.22512, CPL, CMB+DESI+SNe): PantheonPlus (−0.833, −0.65),
DESY5 (−0.749, −0.88), Union3 (−0.664, −1.10); Ω_m = 0.31; H0 = 67.4. Canonical field, w clipped at −1 (a canonical field cannot be phantom;
this UNDER-estimates the excursion relative to the fits).
Bounds (1σ): ESPRESSO Δα/α = (1.3 ± 1.3 ± 0.4) ppm at z = 1.15 (Murphy et al. 2022; combined σ 1.4 ppm); optical clocks α̇/α = (1.8 ± 2.5)×10⁻¹⁹
yr⁻¹ (Filzinger et al. 2023, via review arXiv:2506.18328); MICROSCOPE η = (−0.1 ± 1.3)×10⁻¹⁴ with η ≈ 10⁻³ ζ² (Martins et al., arXiv:2204.02930).
Reading: EXCLUDED for a (fit, k) if any predicted quantity exceeds its bound by more than 5σ; report the factor for each. The claim to be
tested: all three fits are excluded for k = 1, 2, 3 by at least one bound.
Scope/limits: one loop; MSSM matching coefficients; no screening; SM fields not sequestered from the modulus beyond locality metrics;
escapes (non-universal GS per gauge factor, sequestered sectors, axionic quintessence) are discussed, not excluded.
No reruns; fixes via a DEVIATIONS file written first.
