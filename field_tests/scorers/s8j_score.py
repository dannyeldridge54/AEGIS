"""Score S8-J (field_tests/rules/PREREG_S8_JOINT.md) exactly as written.
    python s8j_score.py   (reads cmb-fit/results/cmp_*_s8y6.json; $TWIST_RESULTS overrides)  -> ../results/s8j_score.json"""
import json, math, os
HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.environ.get("TWIST_RESULTS", os.path.join(HERE, "..", "..", "cmb-fit", "results"))
SETS = {"Pantheon+": "", "DES-Dovekie": "_dovekie", "Union3": "_union3"}
OBS, UP, DN, ONU = 0.798, 0.014, 0.015, 0.06 / 93.14


def load(n):
    p = os.path.join(RES, f"cmp_{n}.json")
    return json.load(open(p))["minimum"] if os.path.exists(p) else None


def best_lcdm(n):
    """Deviation S8J-D3: the LCDM reference is the lower chi2 of its 2 restarts and the 2 extra restarts (_more)."""
    a, b = load(n), load(n + "_more")
    c = [x for x in (a, b) if x and math.isfinite(x["chi2"])]
    return min(c, key=lambda x: x["chi2"]) if c else None


def s8(m):
    return m["sigma8"] * math.sqrt((m["omega_b"] + m["omega_cdm"] + ONU) / (m["H0"] / 100) ** 2 / 0.3)


def no_s8(m):
    return m["chi2"] - m.get("chi2__s8_desy6", 0.0)


rows, ds = {}, []
for sn, suf in SETS.items():
    sj, lj = load(f"ax_spa_spiraltwist{suf}_nlfix_s8y6"), best_lcdm(f"ax_spa_lcdm_halofit{suf}_s8y6")
    sf, lf = load(f"ax_spa_spiraltwist{suf}_nlfix"), load(f"ax_spa_lcdm_halofit{suf}")
    if not (sj and lj and all(math.isfinite(x["chi2"]) for x in (sj, lj))):
        rows[sn] = {"verdict": "NO VERDICT (fit missing or non-finite)"}
        continue
    d = sj["chi2"] - lj["chi2"]; ds.append(d)
    rows[sn] = {"chi2_spiral_S8": round(sj["chi2"], 3), "chi2_LCDM_S8": round(lj["chi2"], 3), "delta": round(d, 2),
                "lensing_cost": round((no_s8(sj) - sf["chi2"]) - (no_s8(lj) - lf["chi2"]), 2),
                "chi2_S8_term": {"spiral": round(sj.get("chi2__s8_desy6", float("nan")), 2),
                                 "LCDM": round(lj.get("chi2__s8_desy6", float("nan")), 2)},
                "S8": {"spiral": round(s8(sj), 4), "LCDM": round(s8(lj), 4), "spiral_SF": round(s8(sf), 4)},
                "beta_eff": round(sj.get("scf_coupling_beta", float("nan")), 4), "beta_eff_SF": round(sf["scf_coupling_beta"], 4),
                "kappa": round(sj.get("spiral_kappa", float("nan")), 3)}
n_beat = sum(d <= -4 for d in ds)
if len(ds) < 3 and n_beat < 2:
    verdict = f"INCOMPLETE ({len(ds)} of 3 sets)"
elif n_beat >= 2:
    verdict = "SURVIVES LENSING"
elif n_beat == 0 and all(d < 2 for d in ds):
    verdict = "TIE"
else:
    verdict = "MIXED"
out = {"rule": "PREREG_S8_JOINT.md", "rows": rows, "verdict_vs_LCDM": verdict}
os.makedirs(os.path.join(HERE, "..", "results"), exist_ok=True)
json.dump(out, open(os.path.join(HERE, "..", "results", "s8j_score.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
