"""Two-field engine gates, dilaton part (cloud, no data). Each CLASS run is its own process.
    python tf_gates.py   -> cmb-fit/axiclass/twofield/tf_gates.json
G-2F0: AxiCLASS_twofield with dilaton off reproduces AxiCLASS_coupled_nlfix at the FLAG-1 Pantheon+ best fit
       (sigma8, H0, C_l^TT/EE/pp l = 2..2500) within 1e-6 relative.
G-2F2: the flagship's dilaton moved from scf to the new "dil" field (dilaton = yes, dil_kappa = kappa, dil_beta = beta,
       Lambda's budget handed over by the closure loop), no scf: same sigma8, H0 within 1e-4 and C_l^TT/EE/pp within
       1e-4 rms (l 30-2500). Differences come only from the closure method (iteration vs shooting)."""
import json
import os
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "angle"))
import angle_gates as AG

B = AG.B
NL = f"{B}/AxiCLASS_coupled_nlfix/python/build"
TF = f"{B}/AxiCLASS_twofield/python/build"
RUN = os.environ.get("TF_RUN", "ax_spa_spiraltwist_kappa1_nlfix_s8y6")


def args_for(run):
    code = ("import json,sys; sys.path.insert(0,%r); import forward_predictions_cloud as F; a,b=F.args_for(%r); "
            "a={k:v for k,v in a.items() if k not in ('output','z_max_pk','P_k_max_1/Mpc','non_linear','l_max_scalars')}; "
            "print('JSON'+json.dumps([a,b]))") % (os.path.join(HERE, "..", "..", "..", "theory"), run)
    r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=1800,
                       env=dict(os.environ, TWIST_BUILDS=B))
    line = [x for x in r.stdout.splitlines() if x.startswith("JSON")]
    if not line:
        raise RuntimeError(r.stderr[-3000:])
    a, best = json.loads(line[0][4:])
    a.update({"output": "tCl,pCl,lCl,mPk", "lensing": "yes", "l_max_scalars": 2600, "P_k_max_1/Mpc": 1.0})
    return a, best


def to_dil(a):
    d = {k: v for k, v in a.items() if not k.startswith(("scf_", "do_shooting_scf", "attractor_ic_scf", "Omega_scf"))}
    pars = [float(x) for x in a["scf_parameters"].split(",")]
    d.pop("Omega_Lambda", None)
    # flagship scf: double_exp V = p2^4 exp(-p0 phi) (p1 = p3 = 0), and this build sets phi_ini = p0 (= kappa)
    d.update({"dilaton": "yes", "dil_kappa": pars[0], "dil_beta": a.get("scf_coupling_beta", 0.0),
              "dil_phi_ini": pars[0], "Omega_fld": 0})
    return d


def rms(a, b, lo=28):
    a, b = np.array(a)[lo:], np.array(b)[lo:]
    return float(np.sqrt(np.mean(((a - b) / b) ** 2)))


def main():
    a, best = args_for(RUN)
    out = {"run": RUN, "args": a}
    r_nl = AG.run(NL, a)
    r_tf = AG.run(TF, a)
    g0 = max(AG.rel([r_tf[k]], [r_nl[k]]) for k in ("sigma8", "H0"))
    g0 = max([g0] + [AG.rel(r_tf[k], r_nl[k]) for k in ("tt", "ee", "pp")])
    out["G-2F0"] = {"max_rel": g0, "pass": g0 <= 1e-6}
    print("G-2F0", out["G-2F0"], flush=True)
    d = to_dil(a)
    out["dil_args"] = d
    r_d = AG.run(TF, {k: v for k, v in d.items() if v is not None})
    g2 = {"sigma8": AG.rel([r_d["sigma8"]], [r_nl["sigma8"]]), "H0": AG.rel([r_d["H0"]], [r_nl["H0"]])}
    g2.update({k: rms(r_d[k], r_nl[k]) for k in ("tt", "ee", "pp")})
    out["G-2F2"] = {**g2, "pass": g2["sigma8"] <= 1e-4 and g2["H0"] <= 1e-4 and max(g2[k] for k in ("tt", "ee", "pp")) <= 1e-4}
    print("G-2F2", out["G-2F2"], flush=True)
    json.dump(out, open(os.path.join(HERE, "tf_gates.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
