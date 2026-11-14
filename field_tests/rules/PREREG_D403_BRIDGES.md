# PREREG D403 — "Wheatstone bridge" null tests for the Twist / Twist-2 (locked 14:30 CT 14 Nov 2026, before computing)

Idea (Danny, 14:17): build combinations of observables in which the poorly known quantities cancel, so the model predicts a balance
(zero) and any imbalance is a clean failure.

Script: theory/twist2/bridges_d403.py (computes the theory side; nothing is fitted).

**Bridge 1 (inflation; N* and reheating cancel).** B1 = r − 3(1 − n_s)², B2 = α_s + ½(1 − n_s)². Theory value: the script's Twist numbers at
N* = 57.2 (D391); theory tolerance = the spread of B over N* ∈ [55, 60] plus 1×10⁻⁴ (B1) / 2×10⁻⁴ (B2) for higher-order and Kähler-correction
uncertainty. Scoring rule (future data: SO, LiteBIRD, or any joint n_s–r–α_s posterior): BALANCED if |B_meas − B_th| ≤ 2√(σ_meas² + tol²);
otherwise OUT OF BALANCE → the α = 1 plateau (hence Twist inflation) fails regardless of N*. Current data: r is only an upper limit, so
B1 is reported as the implied prediction r = 3(1 − n_s)² for CMB-SPA n_s = 0.9684 ± 0.0030 and for n_s = 0.9728 ± 0.0027 (+DESI); not scored.

**Bridge 2 (dark energy ↔ atomic clocks; the field's history cancels).** R = (α̇/α)/[H0 √(3 Ω_DE (1 + w0))] must equal ζ(k) =
6.97×10⁻³ (k/3) √(2/k) for a rolling modulus with K ⊃ −k ln(X+X̄). Already scored in D400 (out of balance by ~10⁶ for DESI w0);
restated here as the bridge; scoring rule for future data: BALANCED if the clock arm is within 2σ of ζ × the DESI arm.

**Bridge 3 (birefringence ↔ dark energy; the initial angle cancels).** For one thawing axion doing both jobs (Twist-2 variant),
β² = c_γ² K1 (1 + w0). K1 is computed by the script over f ∈ {0.5, 1, 2} M_P, θ_i ∈ {0.3, 0.5, 1.0, 1.5} using the locked D393 code; the
bridge is declared valid only if K1 varies by less than ±25% across θ_i at fixed f (else "no bridge" and only D393's grid stands).
Scoring now (c_γ = 10 as in D393, f = 1): predicted β = 10 √(K1 (1 + w0)) for PantheonPlus w0 = −0.833 ± 0.055 and DESY5 w0 = −0.749 ± 0.057,
against β = 0.261 ± 0.061°; BALANCED if within 2σ (errors combined in quadrature, w0 error propagated). For the separate-axion baseline,
B3 does not apply (no prediction).
No reruns; fixes via a DEVIATIONS file written first.
