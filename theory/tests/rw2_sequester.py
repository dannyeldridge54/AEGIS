"""RW2 — PREREG_RW2_SEQUESTER. AI-assisted."""
import json, math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools", "weave_cm"))
import weave_reverse as wr

V, tv, td = 1.0e5, 20.15, 38.6
BOUND, MARTINS = 1.66e-6, 5.9e-8
m32 = 2.5e5 / wr.MP_GEV
H0 = wr.H0_GEV / wr.MP_GEV
rhoL = 7.1e-121
beta = 2 * math.sqrt(2)

dKdphi, Kd, Kdd = wr.dK_dphi_move_one(V, tv, td)
rng = wr.dlnalpha_dK_range()
lo, hi = min(rng.values()), max(rng.values())
C1 = 0.0
C2_lo, C2_hi = lo * abs(dKdphi), hi * abs(dKdphi)
# C4: α⁻¹ = Re T_vis + 9 Re S ⇒ ∂α_vis⁻¹/∂τ_vis = 1; δτ_vis/δφ ~ ρ_Λ/m_heavy² (M_P = 1); α_em leak ~ α_em·that
C4 = wr.ALPHA_EM * rhoL / m32**2
# C5: light-eigenvector admixture δτ_v/δτ_d ~ (m_φ²/m_heavy²)·G_vd/G_vv; per canonical φ: × dτ_d/dφ = 1/√(2G_dd)
Gvv, Gdd, Gvd = wr.G_matrix(V, tv, td)
C5 = wr.ALPHA_EM * (H0**2 / m32**2) * abs(Gvd) / Gvv / math.sqrt(2 * Gdd)
largest = max(C1, C2_lo, C4, C5)
verdict = "PASS" if largest < BOUND else ("TENSION" if largest < 10 * BOUND else "FAIL")
single = wr.dK_dphi_single(3)
out = {
    "inputs": {"Vol": V, "tau_vis": tv, "tau_dark": td},
    "dK_dphi_swiss_move_td": dKdphi, "K_d": Kd, "K_dd": Kdd,
    "dlnalpha_dK_variants": rng,
    "C1_tree": C1, "C2_range": [C2_lo, C2_hi], "C4_adiabatic": C4, "C5_kinetic_mixing": C5,
    "largest_lower": largest, "bound": BOUND, "ratio_to_bound": largest / BOUND,
    "ratio_to_Martins_bound": largest / MARTINS,
    "verdict": verdict,
    "report_K_minus3ln": {"dK_dphi": single, "zeta_range": [lo * single, hi * single]},
    "report_Vol_needed_for_bound": {k: wr.vol_needed(td, BOUND, c) for k, c in rng.items()},
    "report_Vol_needed_for_Martins": {k: wr.vol_needed(td, MARTINS, c) for k, c in rng.items()},
    "report_C7_fixed_volume_direction": "dK = 0 along the light direction (only C4/C5-size leaks remain)",
    "report_C6": "zero if visible/dark intersection numbers vanish; else O(b_ab/4pi) per unit dln t (condition)",
    "report_uplift_slope_ratio": (m32**2 * abs(dKdphi)) / (rhoL * beta),
}
os.makedirs(os.path.join(os.path.dirname(__file__), "..", "..", "field_tests", "results"), exist_ok=True)
p = os.path.join(os.path.dirname(__file__), "..", "..", "field_tests", "results", "rw2_sequester.json")
json.dump(out, open(p, "w"), indent=2)
print(json.dumps(out, indent=2))
