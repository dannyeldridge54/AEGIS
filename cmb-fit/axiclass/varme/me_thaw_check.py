"""Physical-version check for TWIST-ME (EXPLORATORY, not a verdict of PREREG_TWIST_ME.md): at each stored ME best fit,
recompute the total chi2 with the electron-mass step switched off at z = 500 (thawing field that passes the quasar and
atomic-clock bounds, field_tests/dilaton_me/constants_check.json) instead of z = 50. If |chi2(500) - chi2(50)| is small,
the physical two-field version inherits the TWIST-ME reading. No fit; per-term output.
    python me_thaw_check.py   -> results/me_thaw_check.json"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import me_fit as M
from cobaya.model import get_model
out = {}
for name in M.FLAG:
    row = {}
    for zt in (50., 500.):
        info, E = M.make(name, free=False)
        info["theory"]["classytwist"]["extra_args"]["varying_transition_redshift"] = zt
        info.pop("sampler", None); info.pop("output", None)
        st = json.load(open(f"{E.OUT}/cmp_{name}.json"))["minimum"]
        info["params"]["varying_me"] = st["varying_me"]
        m = get_model(info)
        ll = m.loglikes({k: st[k] for k in m.parameterization.sampled_params()}, as_dict=True)[0]
        row[f"z{int(zt)}"] = {"chi2": round(-2 * sum(ll.values()), 3), "terms": {k: round(-2 * v, 3) for k, v in ll.items()}}
    row["stored_chi2"] = st["chi2"]; row["varying_me"] = st["varying_me"]
    row["diff_500_minus_50"] = round(row["z500"]["chi2"] - row["z50"]["chi2"], 3)
    out[name] = row
    print(name, row["varying_me"], row["diff_500_minus_50"], flush=True)
json.dump(out, open(os.path.join(E.OUT, "me_thaw_check.json"), "w"), indent=1)
