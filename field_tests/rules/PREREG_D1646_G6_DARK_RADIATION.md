# PREREG_D1646_G6_DARK_RADIATION — how cold is the dark side after SERAPIS reheating? (Janus genesis G6; locked 2026-11-19 ~22:44Z before any number)
Input: D1637 — the inflaton decays through Planck-suppressed (gravitational-strength) couplings, T_R ≈ 0.8–4 × 10⁹ GeV, visible g*s(T_R) = 106.75.
Assumption A-dem [estimate]: gravitational-strength decay is DEMOCRATIC per light degree of freedom (equal energy per d.o.f.) ⇒ both sectors start at the same temperature, ξ(T_R) = 1. (Real gravitational decays are channel-dependent — helicity/conformal suppression; stated, not derived.)
Each sector then conserves its own entropy: ξ_today = [g_sD(T_R)/g_sD(now)]^{1/3} / [g_sV(T_R)/g_sV(now)]^{1/3}, g_sV(now) = 3.909.
ΔN_eff = (g_D,now/(7/4)) (11/4)^{4/3} ξ⁴ for bosonic g_D,now (fermions × 7/8).
Cases (locked):
- A full mirror copy (same content as the SM): g_sD identical history ⇒ ξ = 1 ⇒ ΔN_eff = 7.4 (D1632 formula 7.4ξ⁴).
- B minimal ADM sector for P-M: one Dirac dark baryon (5 GeV; g = 4·7/8 = 3.5, non-relativistic today, symmetric part annihilated into) one dark photon (g = 2, massless): g_sD(T_R) = 5.5, g_sD(now) = 2.
- C full copy with asymmetric reheating: the branching needed, Γ_D/Γ_V ≤ ξ_max⁴ with 7.4ξ_max⁴ = 0.3.
Pass rule: a case is VIABLE if ΔN_eff < 0.3 (the bound used in D1632 T4). Report ΔY_p = 0.0130·ΔN_eff (D1633/D1634 slope). Verdict on C-cold (WEAVE_POSTULATES C5): if B is viable, "a cold dark side needs no special branching once the dark sector is minimal"; if only C, state the required branching.
Script: field_tests/scripts/janus_g/g6_dark_radiation.py → field_tests/results/D1646_G6_dark_radiation.json
