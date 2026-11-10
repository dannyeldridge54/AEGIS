"""Diagnosis of the failed G-TF-PC gate (PREREG_TWOFIELD.md). No fit, no new data: at each stored FLAG-1 best fit, the
per-likelihood chi2 from (a) the flagship's own build (AxiCLASS_coupled_nlfix, its exact fit setup) and (b) the two-field
build with the early field off (the gate's setup), next to the stored per-term values. Says whether the gate's -0.85
comes from the two-field engine or from the stored chi2 not being reproduced at the stored point by the flagship itself.
    python tf_gate_diag.py            -> results/tf_gate_diag.json  (each engine runs in its own process)"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def one(engine):
    import twofield_fit as T
    sys.path.insert(0, os.path.join(T.AEGIS, "field_tests", "S8_WL", "joint"))
    from cobaya.model import get_model
    import early_late_spa as E
    import s8_joint_fit as J
    out = {}
    for name, base in T.FLAG.items():
        if engine == "twofield":
            info, E = T.make(name, early=False)
        else:
            E._maybe_coupled(base)
            info = E.make(base)
            J.add_s8(info)
        info.pop("sampler", None)
        info.pop("output", None)
        m = get_model(info)
        st = json.load(open(f"{E.OUT}/cmp_{base}_s8y6.json"))["minimum"]
        ll = m.loglikes({k: st[k] for k in m.parameterization.sampled_params()}, as_dict=True)[0]
        out[name] = {k: {"now": round(-2 * v, 3), "stored": st.get("chi2__" + k),
                         "diff": round(-2 * v - st.get("chi2__" + k, float("nan")), 3)} for k, v in ll.items()}
        out[name]["TOTAL"] = round(sum(-2 * v for v in ll.values()) - st["chi2"], 3)
        print(engine, name, out[name]["TOTAL"], flush=True)
    return out


if __name__ == "__main__":
    if len(sys.argv) > 1:
        print("JSON", json.dumps(one(sys.argv[1])))
        sys.exit()
    res = {}
    for eng in ("flagship", "twofield"):
        r = subprocess.run([sys.executable, __file__, eng], capture_output=True, text=True, cwd=HERE)
        line = [x for x in r.stdout.splitlines() if x.startswith("JSON ")]
        res[eng] = json.loads(line[0][5:]) if line else {"error": r.stderr[-3000:]}
    out = os.path.join(os.environ.get("TWIST_RESULTS", os.path.join(HERE, "..", "..", "results")), "tf_gate_diag.json")
    json.dump(res, open(out, "w"), indent=1)
    print("wrote", out)
