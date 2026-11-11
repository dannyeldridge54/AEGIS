"""SELFCHECK V4 (cluster S8) and V5 (dark-matter fifth force): reported checks under PREREG_SELFCHECK.md.

Inputs are frozen: FLAG-1 S8 and its LCDM+S8 partners as listed in PREREG_LENSING_FORECASTS_FLAG1.md; FLAG-1 beta_eff
from the stored s8y6 minima (cmb-fit/results/cmp_ax_spa_spiraltwist_kappa1*_nlfix_s8y6.json). AI-assisted.

V4 values, checked against the abstracts on 11 Nov 2026:
  eRASS1, Ghirardini et al. 2024, arXiv:2402.08458: S8 = sigma8 (Om/0.3)^0.5 = 0.86 +/- 0.01
  SPT clusters + DES/HST WL, Bocquet et al. 2024, arXiv:2401.02075: S8 = 0.795 +/- 0.029
Test A form (PREREG_LENSING_FORECASTS.md): penalty = ((S8_model - S8_obs)/sigma)^2, dP = penalty(FLAG-1) - penalty(LCDM);
PASSES if dP <= +2 on at least 2 of 3 SN sets, per survey.

V5 convention (this build, cmb-fit/axiclass/spiral_guess.py): rho_c ∝ a^-3 e^(beta phi), i.e. m_c ∝ e^(beta phi), phi in
reduced Planck units (8 pi G = 1); field equation phi'' + ... + V' = beta rho_c. For a light canonical field the
DM-DM scalar force is 2 beta^2 times gravity: G_eff/G - 1 = 2 beta^2.
 1. Pettorino 2013, arXiv:1305.7457: Q = -beta rho_c phi', phi in units of the reduced Planck mass (same definition of
    beta as this build, up to the sign of phi). Planck WP + BAO: beta = 0.0364 +/- 0.0163 (abstract 0.036 +/- 0.016).
    Note: their Eq. 7 prints G_eff = G(1 + beta^2); the beta values compare directly whatever the force normalisation.
 2. Kesden & Kamionkowski 2006 (Sagittarius stream symmetry), as restated by arXiv:0903.4458: attractive DM forces
    greater than 10% of gravity excluded, F = G m^2 (1 + beta_KNP)/r^2, so the bound is G_eff/G - 1 < 0.1. It applies to
    a force range of order the satellite scale or longer; this field is light (range ~ Hubble), so it applies.
 No cluster-scale DM-DM fifth-force bound with a stated convention was found in the search on 11 Nov 2026; none is
 quoted, and the reading uses the bounds above only.
"""
import json, math, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SETS = ["Pantheon+", "Dovekie", "Union3"]
SUFFIX = {"Pantheon+": "", "Dovekie": "_dovekie", "Union3": "_union3"}
S8_FLAG1 = {"Pantheon+": 0.8251, "Dovekie": 0.8282, "Union3": 0.8249}   # PREREG_LENSING_FORECASTS_FLAG1.md
S8_LCDM = {"Pantheon+": 0.8142, "Dovekie": 0.8157, "Union3": 0.8137}
SURVEYS = {"eRASS1 (arXiv:2402.08458)": (0.86, 0.01), "SPT clusters (arXiv:2401.02075)": (0.795, 0.029)}


def pen(s8, obs, sig):
    return ((s8 - obs) / sig) ** 2


out = {"rule": "field_tests/rules/PREREG_SELFCHECK.md", "V4": {}, "V5": {}}
for name, (obs, sig) in SURVEYS.items():
    rows = {}
    for s in SETS:
        pf, pl = pen(S8_FLAG1[s], obs, sig), pen(S8_LCDM[s], obs, sig)
        rows[s] = {"S8_flag1": S8_FLAG1[s], "S8_lcdm": S8_LCDM[s], "penalty_flag1": round(pf, 3),
                   "penalty_lcdm": round(pl, 3), "dP": round(pf - pl, 3)}
    npass = sum(r["dP"] <= 2 for r in rows.values())
    out["V4"][name] = {"S8_obs": obs, "sigma": sig, "rows": rows, "passes_on": npass,
                       "reading": "PASSES" if npass >= 2 else "OVER"}

beta = {}
for s in SETS:
    f = os.path.join(ROOT, f"cmb-fit/results/cmp_ax_spa_spiraltwist_kappa1{SUFFIX[s]}_nlfix_s8y6.json")
    beta[s] = json.load(open(f))["minimum"]["scf_coupling_beta"]
P_MEAN, P_SIG = 0.0364, 0.0163
STREAM = 0.1
rows = {}
for s in SETS:
    b = beta[s]
    rows[s] = {"beta_eff": round(b, 5), "G_eff_over_G_minus_1": round(2 * b * b, 5),
               "pull_vs_Pettorino_sigma": round((b - P_MEAN) / P_SIG, 2),
               "within_2sigma_Pettorino": abs(b - P_MEAN) <= 2 * P_SIG,
               "inside_stream_bound": 2 * b * b < STREAM}
ok = all(r["inside_stream_bound"] for r in rows.values())
out["V5"] = {"convention": "m_c ∝ e^(beta phi), phi in reduced Planck units; G_eff/G - 1 = 2 beta^2",
             "Pettorino2013": {"beta": P_MEAN, "sigma": P_SIG, "data": "Planck WP + BAO"},
             "stream_bound": {"G_eff_over_G_minus_1_max": STREAM, "source": "Kesden & Kamionkowski 2006 via arXiv:0903.4458"},
             "cluster_bound": "none found with a stated convention (11 Nov 2026); not quoted",
             "rows": rows, "reading": "PASSES" if ok else "FAILS (stream bound)"}

dst = os.path.join(ROOT, "field_tests/results/selfcheck_v4_v5.json")
json.dump(out, open(dst, "w"), indent=1, ensure_ascii=False)
print(json.dumps(out, indent=1, ensure_ascii=False))
