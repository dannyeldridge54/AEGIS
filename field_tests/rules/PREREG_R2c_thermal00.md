# PREREG R2c (stage a) — thermal average of the χ⁰χ⁰-incoming Sommerfeld factor at freeze-out — locked 2026-11-17, before any code or run
Source for the averaging: Hisano et al. hep-ph/0610249, Eqs. (11) and (13).
- ⟨σ_ij v⟩ = (m/4πT)^{3/2} ∫4πv² dv (σ_ij v) exp(−mv²/4T), with v the relative velocity.
- g_eff = 2 + 4(1+δm/m)^{3/2} e^{−xδm/m}.
SCOPE (honest label): this stage covers ONLY the charge-0 sector with χ⁰χ⁰ incoming (row 0). The χ⁺χ⁻-incoming, χ⁰χ^± and χ^±χ^± channels and the g_eff sum come in later stages. So this is NOT yet ⟨σ_eff v⟩.
Quantity: R₀₀(x) = ⟨S⟩/S_free, where S = sΓs† (Γ = [[2,√2],[√2,3]]) and S_free = 2.
- Maxwell weight w(v) ∝ v² exp(−x v²/4), with x = M/T.
- Open side (E > 2δm): sommerfeld.two_channel_open row 0, full α, tails = (0, ALPHA), potential as in r2b4/r2b5 (λ = 1).
- Closed side (E < 2δm, v < v_th): its Maxwell weight is reported. It is included only if that weight is > 1e-4; otherwise it is excluded and the bound is stated.
- Grid: n log-spaced v ∈ [1.001·v_th, 2.0], trapezoid in v. n = 40 and 80. Converged iff they agree within 1%.
- Points: M = 2000 and 2842 GeV; x = 20, 25, 30.
Reported:
- R₀₀ at each (M, x).
- The Maxwell weight of the threshold band x_E = E/2δm ∈ [0.9, 1.1].
- The weight of v > 2 that is dropped.
Scored: convergence only (1%). There is no physics pass/fail at this stage (no sourced number for R₀₀ alone).
