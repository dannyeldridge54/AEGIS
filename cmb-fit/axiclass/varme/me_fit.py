"""TWIST-ME fit (rule: field_tests/rules/PREREG_TWIST_ME.md; refuses to fit before it is locked).
Model = FLAG-1 exactly (PREREG_FLAGSHIP.md: S8-J setup, kappa = 1, beta_eff free, DES Y6 S8 term, same data, same build
AxiCLASS_coupled_nlfix) PLUS one parameter: the electron mass before z = 50, varying_me in [0.9, 1.1] (CLASS v3.3 built-in
"varying_fundamental_constants = instantaneous": m_e/m_e0 = varying_me for z > 50, 1 after; alpha fixed to 1).
    python me_fit.py gate_pc               # G-ME-PC: varying_me = 1, at the FLAG-1 best fits: chi2 = stored FLAG-1 within 0.05
    python me_fit.py ME[_dovekie|_union3]
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
RULE = os.path.join(AEGIS, "field_tests", "rules", "PREREG_TWIST_ME.md")
FLAG = {"ME": "ax_spa_spiraltwist_kappa1_nlfix", "ME_dovekie": "ax_spa_spiraltwist_kappa1_dovekie_nlfix",
        "ME_union3": "ax_spa_spiraltwist_kappa1_union3_nlfix"}
VARCONST = {"varying_fundamental_constants": "instantaneous", "varying_alpha": 1.0, "varying_transition_redshift": 50.}


def make(name, free=True):
    import early_late_spa as E
    import s8_joint_fit as J
    base = FLAG[name]
    E._maybe_coupled(base)
    info = E.make(base)
    J.add_s8(info)
    info["theory"]["classytwist"]["extra_args"].update(VARCONST)
    p = info["params"]
    flag = json.load(open(f"{E.OUT}/cmp_{base}_s8y6.json"))["minimum"]     # start at the FLAG-1 best fit
    for k, v in p.items():
        if isinstance(v, dict) and "ref" in v and k in flag:
            v["ref"]["loc"] = float(flag[k])
    p["varying_me"] = E.P(0.9, 1.1, 1.0, 0.005, r"m_e/m_{e,0}") if free else 1.0
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
    json.dump(out, open(os.path.join(E.OUT, "me_gate_pc.json"), "w"), indent=1)
    return out["all_pass"]


def run(name):
    assert name in FLAG, f"unknown run {name}"
    assert os.path.exists(RULE + ".sha256"), "PREREG_TWIST_ME.md is not locked; no fit runs before the lock"
    from cobaya.run import run as crun
    t = time.time()
    info, E = make(name)
    crun(info)
    E.save(name, time.time() - t)


if __name__ == "__main__":
    if sys.argv[1] == "gate_pc":
        sys.exit(0 if gate_pc() else 1)
    run(sys.argv[1])
