"""D410 CROWN (locked PREREG_D410_CROWN): the five senses fitted together by one Twist-2 parameter set. AI-assisted.
Runs on the PC (WSL env "aegis") from cmb-fit/axiclass, reusing early_late_spa.py (CMB-SPA: Planck low-l + ACT DR6 + SPT-3G D1 +
ACT lensing; DESI DR2 BAO; Pantheon+), w0–wa fluid (PPF, CLP) restricted to the thawing line wa = −1.58 (1 + w0), w0 ∈ [−1, −0.5].
    python crown_d410.py fit THAW_FREE|THAW_TWIST | score
THAW_FREE: n_s free.  THAW_TWIST: n_s fixed at the Twist value 0.9651 (D391/D407)."""
import json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); AEG = os.path.abspath(os.path.join(HERE, "..", ".."))
RULE = os.path.join(AEG, "field_tests", "rules", "PREREG_D410_CROWN.md")
NS_TWIST = 0.9651


def build(job):
    import early_late_spa as E
    base = "ax_spa_w0wa_halofit"; E._maybe_coupled(base); info = E.make(base)
    m = json.load(open(f"{E.OUT}/cmp_{base}.json"))["minimum"]
    info["params"]["w0_fld"] = E.P(-1.0, -0.5, -0.86, 0.03)
    info["params"]["wa_fld"] = {"value": "lambda w0_fld: -1.58*(1+w0_fld)", "derived": False}
    info["prior"].pop("w0wa_bound", None)
    for k, p in info["params"].items():
        if isinstance(p, dict) and "ref" in p and k in m:
            p["ref"]["loc"] = float(m[k])
    if job == "THAW_TWIST":
        info["params"]["n_s"] = NS_TWIST
    info["sampler"]["minimize"]["best_of"] = 4
    info["output"] = f"{E.OUT}/chains/cmp_d410_{job.lower()}"
    return E, info


def fit(job):
    assert os.path.exists(RULE + ".sha256"), "rule not locked"
    from cobaya.run import run as crun
    E, info = build(job); t = time.time(); crun(info); E.save(f"d410_{job.lower()}", time.time() - t)


def blocks(m):
    g = {"CMB": 0.0, "BAO": 0.0, "SN": 0.0}
    for k, v in m.items():
        if not k.startswith("chi2__"): continue
        n = k[6:]
        if n.startswith("bao."): g["BAO"] += v
        elif n.startswith("sn."): g["SN"] += v
        else: g["CMB"] += v
    return g


def score():
    res = os.environ.get("TWIST_RESULTS", os.path.join(AEG, "cmb-fit", "results"))
    ld = lambda n: json.load(open(os.path.join(res, f"cmp_{n}.json")))["minimum"]
    fr, tw, lc, ww = ld("d410_thaw_free"), ld("d410_thaw_twist"), ld("ax_spa_lcdm_halofit"), ld("ax_spa_w0wa_halofit")
    out = {"rule": "PREREG_D410_CROWN.md", "chi2": {"THAW_FREE": fr["chi2"], "THAW_TWIST": tw["chi2"], "LCDM": lc["chi2"], "W0WA_free": ww["chi2"]},
           "n_s_THAW_FREE": fr.get("n_s"), "w0_THAW_FREE": fr.get("w0_fld"), "w0_THAW_TWIST": tw.get("w0_fld")}
    C1 = tw["chi2"] - fr["chi2"]; out["C1_dchi2_fix_ns"] = round(C1, 3); out["C1_pass"] = C1 <= 4.0
    bt, bl = blocks(tw), blocks(lc); d = {k: round(bt[k] - bl[k], 3) for k in bt}; out["C2_blocks_TWIST_minus_LCDM"] = d
    out["C2_pass"] = all(v <= 4.0 for v in d.values())
    w0 = tw.get("w0_fld", -1.0); one = max(1 + w0, 1e-9); cf = 0.261 / (2.5e-3 * one) ** 0.5
    out["C4_cgamma_over_f_needed"] = round(cf, 2); out["C4_pass"] = cf <= 30.0
    out["C3_touch"] = "pass by construction (axion: CP-odd coupling, no alpha drift; D400 applies to moduli only)"
    fails = [s for s, ok in (("CMB+BAO+SN with Twist n_s (C1)", out["C1_pass"]), ("a single sense vs LCDM (C2)", out["C2_pass"]),
                             ("birefringence (C4)", out["C4_pass"])) if not ok]
    out["verdict"] = "CROWN AGREES" if not fails else "SENSES DISAGREE: " + "; ".join(fails)
    p = os.path.join(AEG, "field_tests", "results", "crown_d410.json"); json.dump(out, open(p, "w"), indent=1); print(json.dumps(out, indent=1))


if __name__ == "__main__":
    a = sys.argv[1:]
    score() if a[0] == "score" else fit(a[1])
