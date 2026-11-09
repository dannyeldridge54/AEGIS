"""V8 one-command check: rebuild the SF likelihoods and evaluate them at the STORED best points of the Spiral (Pantheon+)
and its LCDM reference; report each chi2 against the stored value and the Spiral - LCDM difference.
    $TWIST_PY repro_eval.py [spiral_run] [lcdm_run]     (defaults: ax_spa_spiraltwist_nlfix ax_spa_lcdm_halofit)
PASS if each chi2 matches the stored chi2 within 0.1. Evaluation only, no fitting (a full refit is early_late_spa.py)."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "axiclass"))
import early_late_spa as E  # noqa: E402


def chi2_at_stored(run):
    from cobaya.model import get_model
    E._maybe_coupled(run)
    info = E.make(run)
    for k in ("sampler", "output", "resume", "force"):
        info.pop(k, None)
    model = get_model(info)
    m = json.load(open(os.path.join(E.OUT, f"cmp_{run}.json")))["minimum"]
    point = {k: m[k] for k in model.parameterization.sampled_params()}
    chi2 = -2 * sum(model.loglikes(point, as_dict=True)[0].values())   # as spiral_l_fit.gate_pc
    return chi2, m["chi2"]


if __name__ == "__main__":
    runs = sys.argv[1:3] or ["ax_spa_spiraltwist_nlfix", "ax_spa_lcdm_halofit"]
    res = {}
    for r in runs:
        c, s = chi2_at_stored(r)
        res[r] = {"chi2": round(c, 3), "stored": round(s, 3), "diff": round(c - s, 3), "pass": abs(c - s) <= 0.1}
        print(r, res[r], flush=True)
    a, b = runs
    res["delta_chi2"] = {"reproduced": round(res[a]["chi2"] - res[b]["chi2"], 3),
                         "stored": round(res[a]["stored"] - res[b]["stored"], 3)}
    res["all_pass"] = all(v["pass"] for v in res.values() if "pass" in v)
    print(json.dumps(res, indent=1))
    json.dump(res, open(os.path.join(HERE, "repro_eval_result.json"), "w"), indent=1)
