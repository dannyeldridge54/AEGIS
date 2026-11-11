"""DATA-GEN (field_tests/rules/PREREG_DATA_GENERATIONS.md): FLAG-1 and LCDM refit on older generations of late-time data.
    python datagen_fit.py <FLAG1|LCDM> <gen1|gen2|gen3|cmbplanck>   (PC, WSL env "aegis") -> cmb-fit/results/cmp_<name>.json
    python datagen_fit.py score                                       -> field_tests/results/datagen.json"""
import json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); AEG = os.path.abspath(os.path.join(HERE, "..", ".."))
RULE = os.path.join(AEG, "field_tests", "rules", "PREREG_DATA_GENERATIONS.md")
sys.path.insert(0, os.path.join(AEG, "cmb-fit", "axiclass")); sys.path.insert(0, os.path.join(AEG, "field_tests", "S8_WL", "joint"))
BASE = {"FLAG1": "ax_spa_spiraltwist_kappa1_nlfix", "LCDM": "ax_spa_lcdm_halofit"}
GEN = {  # generation -> (engine suffix selecting the SN set / CMB, BAO likelihoods or None to keep DESI DR2)
    "gen1": ("_snjla", ["bao.sixdf_2011_bao", "bao.sdss_dr7_mgs", "bao.sdss_dr12_consensus_bao"]),
    "gen2": ("_snpantheon", ["bao.sdss_dr7_mgs", "bao.sdss_dr12_lrg_bao_dmdh", "bao.sdss_dr16_lrg_bao_dmdh",
                             "bao.sdss_dr16_bao_elg", "bao.sdss_dr16_qso_bao_dmdh", "bao.sdss_dr16_baoplus_lyauto",
                             "bao.sdss_dr16_baoplus_lyxqso"]),
    "gen3": ("", ["bao.desi_2024_bao_all"]),
    "cmbplanck": ("_planckfull", None),
}


def name(which, gen):
    return f"{BASE[which]}_{gen}_s8y6"


def fit(which, gen):
    assert os.path.exists(RULE + ".sha256"), "rule not locked"
    import early_late_spa as E
    import s8_joint_fit as J
    from cobaya.run import run as crun
    suf, bao = GEN[gen]
    engine = BASE[which].replace("_nlfix", "") + suf + ("_nlfix" if which == "FLAG1" else "")
    t = time.time()
    E._maybe_coupled(engine)
    info = E.make(engine)
    if bao is not None:
        info["likelihood"] = {k: v for k, v in info["likelihood"].items() if not k.startswith("bao.")}
        info["likelihood"].update({b: None for b in bao})
    J.add_s8(info)
    m = json.load(open(f"{E.OUT}/cmp_{BASE[which]}_s8y6.json"))["minimum"]
    for k, p in info["params"].items():
        if isinstance(p, dict) and "ref" in p and k in m:
            p["ref"]["loc"] = float(m[k])
    info["sampler"]["minimize"]["best_of"] = 4
    n = name(which, gen)
    info["output"] = f"{E.OUT}/chains/cmp_{n}"
    print("likelihoods:", sorted(info["likelihood"]), flush=True)
    crun(info)
    E.save(n, time.time() - t)


def score():
    res = os.environ.get("TWIST_RESULTS", os.path.join(AEG, "cmb-fit", "results"))
    ld = lambda n: json.load(open(os.path.join(res, f"cmp_{n}.json")))["minimum"]
    rows = {}
    for g in ("gen1", "gen2", "gen3", "gen4", "cmbplanck"):
        if g == "gen4":
            f, l = ld("ax_spa_spiraltwist_kappa1_nlfix_s8y6"), ld("ax_spa_lcdm_halofit_s8y6")
        else:
            f, l = ld(name("FLAG1", g)), ld(name("LCDM", g))
        rows[g] = {"delta": round(f["chi2"] - l["chi2"], 3), "beta_eff": f.get("scf_coupling_beta"),
                   "H0": [f.get("H0"), l.get("H0")], "sigma8": [f.get("sigma8"), l.get("sigma8")],
                   "chi2_parts_FLAG1": {k: v for k, v in f.items() if k.startswith("chi2__")},
                   "chi2_parts_LCDM": {k: v for k, v in l.items() if k.startswith("chi2__")}}
    D = {g: rows[g]["delta"] for g in ("gen1", "gen2", "gen3", "gen4")}
    B = {g: rows[g]["beta_eff"] or 0 for g in ("gen3", "gen4")}
    if any(d > 2 for d in D.values()):
        reading = "DOES NOT HOLD"
    elif all(d <= 0 for d in D.values()) and all(b > 0.01 for b in B.values()):
        reading = "HOLDS AND STRENGTHENS" if D["gen4"] <= D["gen1"] - 2 else "HOLDS (FLAT)"
    elif D["gen1"] > -1 and D["gen2"] > -1 and D["gen3"] <= -2 and D["gen4"] <= -2:
        reading = "NEWEST-DATA ONLY"
    else:
        reading = "MIXED"
    out = {"rule": "PREREG_DATA_GENERATIONS.md", "reading": reading, "deltas": D, "rows": rows}
    json.dump(out, open(os.path.join(AEG, "field_tests", "results", "datagen.json"), "w"), indent=1)
    print(json.dumps({"reading": reading, "deltas": D, "cmbplanck": rows["cmbplanck"]["delta"]}, indent=1))


if __name__ == "__main__":
    score() if sys.argv[1] == "score" else fit(sys.argv[1], sys.argv[2])
