"""TWIST-DR fit (rule: field_tests/rules/PREREG_TWIST_DR.md; refuses to fit before it is locked).
Model = FLAG-1 exactly (PREREG_FLAGSHIP.md: S8-J setup, kappa = 1, beta_eff free, DES Y6 S8 term, same data, same build
AxiCLASS_coupled_nlfix) PLUS delta_neff in [0, 1] (free-streaming dark radiation: N_ur = 2.0328 + delta_neff; BBN helium
from CLASS's default table, consistent) and alpha_s in [-0.05, 0.05] (running of n_s).
    python dr_fit.py gate_pc               # G-DR-PC: delta_neff = alpha_s = 0 at the FLAG-1 best fits: chi2 = stored within 0.05
    python dr_fit.py DR[_dovekie|_union3]
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
AX = os.path.dirname(HERE)
AEGIS = os.path.abspath(os.path.join(AX, "..", ".."))
sys.path.insert(0, AX)
sys.path.insert(0, os.path.join(AEGIS, "field_tests", "S8_WL", "joint"))
RULE = os.path.join(AEGIS, "field_tests", "rules", "PREREG_TWIST_DR.md")
FLAG = {"DR": "ax_spa_spiraltwist_kappa1_nlfix", "DR_dovekie": "ax_spa_spiraltwist_kappa1_dovekie_nlfix",
        "DR_union3": "ax_spa_spiraltwist_kappa1_union3_nlfix"}
N_UR0 = 2.0328


def make(name, free=True):
    import early_late_spa as E
    import s8_joint_fit as J
    base = FLAG[name]
    E._maybe_coupled(base)
    info = E.make(base)
    J.add_s8(info)
    assert info["theory"]["classytwist"]["extra_args"].pop("N_ur") == N_UR0
    p = info["params"]
    flag = json.load(open(f"{E.OUT}/cmp_{base}_s8y6.json"))["minimum"]     # start at the FLAG-1 best fit
    for k, v in p.items():
        if isinstance(v, dict) and "ref" in v and k in flag:
            v["ref"]["loc"] = float(flag[k])
    if free:
        p["delta_neff"] = dict(E.P(0.0, 1.0, 0.1, 0.05, r"\Delta N_{\rm eff}"), drop=True)   # only via N_ur
        p["alpha_s"] = E.P(-0.05, 0.05, 0.0, 0.005, r"\alpha_s")
    else:
        p["delta_neff"], p["alpha_s"] = {"value": 0.0, "drop": True}, 0.0
    p["N_ur"] = {"value": f"lambda delta_neff: {N_UR0} + delta_neff", "derived": False}
    info["sampler"] = {"minimize": dict(info["sampler"]["minimize"], best_of=4)}
    info["output"] = f"{E.OUT}/chains/cmp_{name}"
    return info, E


def gate_pc():
    from cobaya.model import get_model
    out = {}
    for name, base in FLAG.items():
        info, E = make(name, free=False)
        info.pop("sampler", None)
        info.pop("output", None)
        m = get_model(info)
        st = json.load(open(f"{E.OUT}/cmp_{base}_s8y6.json"))["minimum"]
        ll = m.loglikes({k: st[k] for k in m.parameterization.sampled_params()}, as_dict=True)[0]
        chi2 = -2 * sum(ll.values())
        out[name] = {"chi2": round(chi2, 3), "stored_FLAG1": round(st["chi2"], 3), "diff": round(chi2 - st["chi2"], 3),
                     "pass": bool(abs(chi2 - st["chi2"]) <= 0.05),
                     "terms": {k: round(-2 * v - st.get("chi2__" + k, float("nan")), 3) for k, v in ll.items()}}
        print(name, out[name], flush=True)
    out["all_pass"] = all(v["pass"] for v in out.values() if isinstance(v, dict))
    json.dump(out, open(os.path.join(E.OUT, "dr_gate_pc.json"), "w"), indent=1)
    return out["all_pass"]


def run(name):
    assert name in FLAG, f"unknown run {name}"
    assert os.path.exists(RULE + ".sha256"), "PREREG_TWIST_DR.md is not locked; no fit runs before the lock"
    from cobaya.run import run as crun
    t = time.time()
    info, E = make(name)
    crun(info)
    E.save(name, time.time() - t)


if __name__ == "__main__":
    if sys.argv[1] == "gate_pc":
        sys.exit(0 if gate_pc() else 1)
    run(sys.argv[1])
