# PREREG B5 — LINX second BBN network (Djl D; cross-check for B4/B4b) — locked 2026-11-17
Code: LINX (pip linx-bbn, JAX; Giovanetti, Lisanti, Liu, Mishra-Sharma, Ruderman). Defaults: Ωbh2 = 0.02242 (= ours), standard background, network 'key_PRIMAT_2023', all nuclear-rate nuisance parameters q = 0, eta_fac = tau_n_fac = 1. Usage copied from its nuclear_evolution example notebook.
Outputs: final Y_p (mass fraction), D/H, ³He/H, and ⁷Li/H (⁷Li + ⁷Be) if the key network carries them.
Checks:
- X1 (scored, cross-code): vs our PRIMAT 2021 table at the same ω_b (D1082: Y_p 0.24721, 10⁵D/H 2.4393). CONSISTENT if |ΔY_p| ≤ 0.002 and |ΔD/H|/D/H ≤ 2% (2021 vs 2023 rates).
- X2 (reported): ⁷Li/H vs PRyMordial's 5.497e-10 (D1104, at 0.02230) and vs the quoted 4.94 ± 0.72e-10.
- X3 (reported): Y_p vs PRyMordial's 0.24555, to test D1104's −0.7% offset.
Script theory/wiring/b5_linx.py (written after this lock). Species indices are read from LINX's own network definition, not assumed.
