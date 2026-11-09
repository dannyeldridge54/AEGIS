"""Score S8-A (field_tests/rules/PREREG_S8A_ANGLE.md) exactly as written (same arithmetic as spiral_l_score.py).
    python s8a_score.py   (reads cmb-fit/results/cmp_S8A*.json) -> ../results/s8a_score.json
sigma8 of S8-A counts the angle (fld_in_delta_m = 1); S8-L's does not (D2), reported beside it.
Mass: approximate, m ~ 3 H(a_c) with radiation + matter at the best fit (reported, not a verdict)."""
import json, math, os
HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.environ.get("TWIST_RESULTS", os.path.join(HERE, "..", "..", "cmb-fit", "results"))
SETS = {"Pantheon+": "", "DES-Dovekie": "_dovekie", "Union3": "_union3"}
OBS, UP, DN, ONU, OGR = 0.798, 0.014, 0.015, 0.06 / 93.14, 4.18e-5   # omega_r h^2 incl. massless nu (approx.)
H100_EV = 2.1332e-33


def load(n):
    p = os.path.join(RES, f"cmp_{n}.json")
    return json.load(open(p))["minimum"] if os.path.exists(p) else None


def s8(m):
    wm = m["omega_b"] + m["omega_cdm"] + m.get("omega_fld", 0.0) + ONU
    return m["sigma8"] * math.sqrt(wm / (m["H0"] / 100) ** 2 / 0.3)


def pen(x):
    return ((x - OBS) / (UP if x > OBS else DN)) ** 2


def mass_ev(m):
    a = 10 ** m["log10_a_c"]
    wm = m["omega_b"] + m["omega_cdm"] + m.get("omega_fld", 0.0) + ONU
    return 3 * H100_EV * math.sqrt(OGR / a ** 4 + wm / a ** 3)


rows, d_l, p_ok = {}, [], []
for sn, suf in SETS.items():
    L, ref, sf = load(f"S8A{suf}"), load(f"ax_spa_lcdm_halofit{suf}"), load(f"spiralL{suf}")
    if not (L and math.isfinite(L["chi2"])):
        rows[sn] = {"verdict": "NO VERDICT (fit missing or non-finite)"}
        continue
    d = L["chi2"] - ref["chi2"]; d_l.append(d)
    p = pen(s8(L)) - pen(s8(ref)); p_ok.append(p <= 2)
    rows[sn] = {"chi2": round(L["chi2"], 3), "delta_vs_LCDM": round(d, 2), "S8": round(s8(L), 4),
                "S8_LCDM": round(s8(ref), 4), "S8_S8L": round(s8(sf), 4), "DES_Y6_penalty": round(p, 2),
                "delta_vs_S8L": round(L["chi2"] - sf["chi2"], 2), "H0": round(L["H0"], 2),
                "log10_a_c": round(L["log10_a_c"], 3), "mass_eV_approx": f"{mass_ev(L):.2e}",
                "beta_eff": round(L["beta_eff"], 4), "angle_share_f": round(L["beta_eff"] / (2/3)**0.5, 4), "kappa": round(L.get("spiral_kappa", 0), 3)}
n = len(d_l)
beats = sum(x <= -4 for x in d_l) >= 2
vs = ("BEATS" if beats else "TIE" if all(-4 < x < 2 for x in d_l) and n == 3 else "MIXED" if n == 3 else f"INCOMPLETE ({n} of 3)")
lens_ok = sum(p_ok) >= 2
lensing = ("LENSING FIXED" if lens_ok and beats else "TRADE-OFF" if lens_ok else
           "NOT FIXED" if n == 3 else f"INCOMPLETE ({n} of 3)")
out = {"rule": "PREREG_S8A_ANGLE.md", "rows": rows, "vs_LCDM": vs, "lensing": lensing}
os.makedirs(os.path.join(HERE, "..", "results"), exist_ok=True)
json.dump(out, open(os.path.join(HERE, "..", "results", "s8a_score.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
