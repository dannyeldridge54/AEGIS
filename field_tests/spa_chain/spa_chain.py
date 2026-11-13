"""SPA-CHAIN (rule: field_tests/rules/PREREG_SPA_CHAIN.md, estimation only). MCMC of PURE-TWIST and LCDM on the NS-SPA likelihood set
(ACT DR6 + SPT-3G + Planck low-l + ACT lensing + DESI DR2 BAO + Pantheon+ + DES Y6 S8), n_s free. PC, WSL env "aegis". AI-assisted.
    python spa_chain.py PURE|LCDM"""
import json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); AEG = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(AEG, "cmb-fit", "axiclass")); sys.path.insert(0, os.path.join(AEG, "field_tests", "S8_WL", "joint"))
BASE = {"PURE": "ax_spa_spiraltwist_kappa0.8165_beta0_nlfix", "LCDM": "ax_spa_lcdm_halofit"}
START = {"PURE": "ns_spa_pure_free", "LCDM": "ax_spa_lcdm_halofit_s8y6"}
def main(model):
    assert os.path.exists(os.path.join(AEG, "field_tests", "rules", "PREREG_SPA_CHAIN.md.sha256")), "rule not locked"
    import early_late_spa as E, s8_joint_fit as J
    from cobaya.run import run as crun
    E._maybe_coupled(BASE[model]); info = E.make(BASE[model]); J.add_s8(info)
    m = json.load(open(f"{E.OUT}/cmp_{START[model]}.json"))["minimum"]
    for k, p in info["params"].items():
        if isinstance(p, dict) and "prior" in p and k in m:          # D2: every sampled parameter, not only those with a ref
            old = p.get("ref"); sc = old.get("scale") if isinstance(old, dict) else None
            p["ref"] = {"dist": "norm", "loc": float(m[k]), "scale": abs(float(sc)) if sc else 1e-3 * max(abs(float(m[k])), 1e-3)}
    for d in ("H0", "Omega_m", "sigma8", "S8"):
        info["params"].setdefault(d, {"latex": d})
    info["sampler"] = {"mcmc": {"Rminus1_stop": 0.02, "Rminus1_cl_stop": 0.2, "max_tries": 1000, "learn_proposal": True,
                                "output_every": "60s", "measure_speeds": True}}
    info["output"] = f"{E.OUT}/chains/spa_chain_{model.lower()}"; info.pop("force", None); info.pop("resume", None)
    t = time.time(); crun(info, resume=True, force=False); print(f"{model} chain done in {time.time()-t:.0f}s", flush=True)
if __name__ == "__main__":
    main(sys.argv[1])
