# PREREG LVSDIL — axio-dilaton route step 2: integrate out the LVS volume with an S-duality-invariant ξ(τ) (Danny 04:28 "get ahead")

Locked 2026-11-19 before computing.
Model [literature: LVS, Balasubramanian–Berglund–Conlon–Quevedo; ξ̂ = ξ/g_s^{3/2} → ξ₀·E(τ,3/2)/(2ζ(3)) by the SL(2,Z) completion,
Green–Gutperle; at weak coupling E(τ,3/2) ≈ 2ζ(3)(Im τ)^{3/2} reproduces ξ/g_s^{3/2}]: at the LVS minimum τ_s^{3/2} ∝ ξ̂ and
V_LVS,min ∝ −W₀²·ξ̂^{1/3}·exp(−3aτ_s) up to slowly varying factors ⇒ along the dilaton direction (volume and τ_s integrated out)
  F(E) = E^{1/3}·exp(−k·E^{2/3}),   V(τ) = V₀[1 − F(E(τ,3/2))/F(E(ρ,3/2))]   (uplift tuned at ρ),
with k = 3a·c the single combination of LVS data (a = 2π/N, c from τ_s^{3/2} = c'ξ̂). Note F decreases with E for k·E^{2/3} > ½,
so the vacuum is at ρ only if k·E(ρ,3/2)^{2/3} > ½ (E(ρ,3/2)^{2/3} = 4.29 ⇒ k > 0.117) — checked per run.
Scan: k ∈ {0.15, 0.3, 0.6, 1.2}; pipeline path (Re τ = ½, n = 1), λ = 1, C = 0, start by the DILATON32 D1 bisection rule; E_paper → G
with G chosen so the pipeline's e/(e+1) equals the plateau exactly: e = F(E_ρ)/F(E) − 1.
Report n_s, r, α_s, N*, and Im τ at horizon exit. Rule: "in band"/"near" as in PREREG_SMSCAN. Expectation stated now: the
super-exponential approach (exp(−kE^{2/3}) with E^{2/3} ∝ Im τ) gives very small r (≪ 1e-4) and n_s ≈ 1 − 2/N-type values —
i.e. LVS-integration is expected to OVER-flatten; if so the one-power form A (D1479) must come from elsewhere.
No reruns to chase results; fixes only via PREREG_LVSDIL_DEVIATIONS.md written first.
