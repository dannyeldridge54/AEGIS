# PREREG_PLANCK_CLASS (D1713) — the reverse thread, uncoupled and coupled to dark matter, on full Planck in a patched CLASS
Locked 19 Nov 2026, before any fit. Replaces the invalid PPF route for the coupled model (PREREG_PLANCK_COUPLED DEVIATIONS D1).

Code: CLASS v3.3.0 + patch field_tests/scripts/pc_planck/aegis_class_d1713.patch (sha256 14f6e9aecc71618f…), driver field_tests/scripts/pc_planck/coupled_class.py (sha256 d0dece62ff19de60…).
Patch: exact Weave curve V = V_L[(2/3)(3/2 − 2cu/(1+cu))]², u = e^{−βφ}, β = 2√2, c = 2ζ(2)/ζ(3); CDM ρ_c ∝ a⁻³e^{b(φ−φ_i)}; force bρ_c on φ; synchronous-gauge CDM perturbations δ_c' = −θ_c − h'/2 + bδφ', θ_c' = −(ℋ + bφ')θ_c + bk²δφ, and −a²bρ_cδ_c in the δφ equation. The thread is left out of CLASS's Ω_m(z) bookkeeping (otherwise halofit is corrupted). The coupling acts from the start of the CLASS integration (not from a = 10⁻³ as in D1710), so this is the more physical version of the model; amp and b are refit.
Validation done in the cloud before locking (numbers in D1713): background E(z) vs an independent Python integration, max rel. error 3e-7 (uncoupled and coupled); sub-horizon growth z = 3 → 0 vs a G_eff = 1 + 2b² ODE, agreement 1e-5.

Data: Planck 2018 low-ℓ TT, low-ℓ EE, plik-lite TTTEEE, lensing; DESI DR2 BAO; one of Pantheon+ / DES-Y5 / Union3 (same likelihood files as D1636).
Runs (9): lcdm, thread (b = 0), coupled (b free), each × 3 SN sets. Free: logA, n_s, H0, ω_b, ω_cdm, τ (+ amp ∈ [1e-6, 3] for thread/coupled, + b ∈ [−0.3, 0.1] for coupled). One massive ν (0.06 eV), halofit for all three models. Minimiser: Cobaya bobyqa, best_of 4.
Gate (before any model run is read): build_check pass (E(z) to 1e-4 vs the cloud reference) AND CLASS ΛCDM χ² within 2.0 of the stored CAMB ΛCDM χ² for each SN set (2433.52 / 2677.37 / 1056.28). Failing the ΛCDM gate → stop and log; no model numbers reported.
Metric: Δχ² = χ²(model) − χ²(CLASS ΛCDM), same build, same SN set.
Verdicts (per SN set, and overall = all three):
- fix_confirmed: coupled Δχ² ≤ −6 on ≥ 2 of 3 sets AND coupled beats the uncoupled thread by ≥ 4 on those sets.
- fix_partial: coupled beats thread by ≥ 2 on ≥ 2 sets, but the first condition fails.
- fix_fails: otherwise.
Also reported (no verdict): best b, its sign vs D1710 (b < 0 expected), amp, Ω_m, σ8, and w0wa CAMB Δχ² for context (different code, so context only).
Caveat stated in advance: scalar-field perturbations in CLASS synchronous gauge are standard; the coupled perturbation terms are new code validated only sub-horizon.
