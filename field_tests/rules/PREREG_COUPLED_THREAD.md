# PREREG_COUPLED_THREAD — can a thread–dark-matter coupling fix the Weave's phantom weak spot? (locked D1708, 2026-11-20 01:47 UTC)
Motivation: with the CMB, CPL beats the thread by 6 because the data favour an apparent w < −1 at high z (D1694, register C8). In coupled quintessence, energy exchange with dark matter makes the dark energy APPEAR phantom to an uncoupled fit, while the field itself never crosses −1.
Model: the thread (leading order, β = 2√2) plus coupling ρ_c ∝ a⁻³ e^{b_c(φ − φ_i)}, with baryons uncoupled (Ω_b = ω_b/h²). Field equation: φ'' + (3 − ε)φ' + [V′ + b_c ρ_c]/H² = 0. Ω_m is the EARLY (pre-roll) matter density, as used for r_d and θ*. V_Λ is shot to H(a = 1) = 1. Parameters: Ω_m, h, ω_b, amp, b_c ∈ [−2, 2].
Data: BAO + SN + CMB (PREREG_REALDATA_CMB). Compared with ΛCDM 1650.38, thread −4.84, CPL −10.84.
Reading: the coupling "closes the gap" if Δχ²(coupled) ≤ −9 (within ~2 of CPL, at the same 2 extra parameters as CPL). Report b_c and the effective w_eff(z) seen by an uncoupled observer at z = 0, 0.5, 1, 2.
Theory note: a coupling between a modulus and dark matter is natural if X's mass depends on the modulus. Fifth-force bounds on dark matter only (not baryons) are weak; b_c ≲ O(0.1) is typical from the CMB in literature (not checked here).
Script: field_tests/scripts/realdata/coupled.py (background)
