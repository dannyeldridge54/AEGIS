"""Two-field engine gates, early-field part (cloud, no data).   python tf_gates_ede.py  -> tf_gates_ede.json
Reference: CAMB EarlyQuintessence (n = 3, use_zc) C_l at the stored Locked Twist best fit edelockP
(tf_camb_ref.py, written to camb_cl_lock.json; same file used for the failed fluid test G-2F1).
G-2F3: AxiCLASS_twofield's native scf axion field (n = 3, KG + AxiCLASS fluid switch), Lambda closure, dilaton off,
       with AxiCLASS's shooting targets (fraction_axion_ac, log10_axion_ac) adjusted by an outer secant until the EXACT
       f_EDE and z_c (classy fEDE(), zc()) equal CAMB's fde_zc and zc (rel. 1e-4): C_l^TT (l 30-2500) and C_l^EE
       (l 50-2500) within 0.3% rms of CAMB (the plain-LCDM engine agreement in G-2F1 was 0.2%).
G-2F4: the same point with the dilaton on but frozen (dil_kappa = 1e-6, dil_beta = 0) in place of Lambda:
       C_l within 1e-5 rms of G-2F3's AxiCLASS C_l (the two-field code path with both fields present)."""
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "angle"))
import angle_gates as AG

TF = f"{AG.B}/AxiCLASS_twofield/python/build"
RES = os.path.join(HERE, "..", "..", "results")
EDE = {"scf_potential": "axion", "n_axion": 3, "security_small_Omega_scf": 0.001, "n_axion_security": 2.09,
       "use_big_theta_scf": "yes", "scf_has_perturbations": "yes", "attractor_ic_scf": "no", "scf_tuning_index": 0,
       "do_shooting": "yes", "do_shooting_scf": "yes"}
RUNNER_BG = r'''
import glob, json, sys
sys.path.insert(0, glob.glob(sys.argv[1] + "/lib*")[0])
import classy
a = json.loads(sys.argv[2]); c = classy.Class(); c.set(a); c.compute(level=["background"])
print("JSON" + json.dumps({"fEDE": c.fEDE(), "zc": c.zc(), "H0": c.h()*100}))
'''


def bg(args):
    import subprocess
    r = subprocess.run([sys.executable, "-c", RUNNER_BG, TF, json.dumps(args)], capture_output=True, text=True, timeout=1800)
    line = [x for x in r.stdout.splitlines() if x.startswith("JSON")]
    if not line:
        raise RuntimeError(r.stdout[-1500:] + r.stderr[-1500:])
    return json.loads(line[0][4:])


def point_args(m):
    return {"H0": m["H0"], "omega_b": m["ombh2"], "omega_cdm": m["omch2"], "A_s": m["As"], "n_s": m["ns"],
            "tau_reio": m["tau"], "N_ur": 2.0328, "N_ncdm": 1, "m_ncdm": 0.06, **EDE,
            "scf_parameters": f"{m['theta_i']}, 0."}


def match(m, extra=None):
    """outer 2D secant: targets (log10 fraction_axion_ac, log10_axion_ac) -> exact (log10 fEDE, log10 zc) = CAMB's"""
    want = np.array([math.log10(m["fde_zc"]), math.log10(m["zc"])])
    x = want.copy()
    x[1] = -math.log10(1 + m["zc"])                          # log10_axion_ac = log10 a_c
    hist = []

    def f(x):
        a = point_args(m) | (extra or {}) | {"fraction_axion_ac": 10 ** x[0], "log10_axion_ac": x[1]}
        r = bg(a)
        y = np.array([math.log10(r["fEDE"]), math.log10(r["zc"])])
        hist.append({"x": x.tolist(), "fEDE": r["fEDE"], "zc": r["zc"]})
        return y - want
    J = np.array([[1.0, 0.0], [0.0, -1.0]])                   # d(log zc)/d(log a_c) ~ -1
    fx = f(x)
    for _ in range(12):
        if np.max(np.abs(fx)) < 4.3e-5:                      # 1e-4 relative
            break
        dx = -np.linalg.solve(J, fx)
        xn = x + dx
        fn = f(xn)
        J = J + np.outer(fn - fx - J @ dx, dx) / (dx @ dx)    # Broyden
        x, fx = xn, fn
    return x, hist, bool(np.max(np.abs(fx)) < 4.3e-5)


def main():
    m = json.load(open(os.path.join(RES, "cmp_edelockP.json")))["minimum"]
    cam = json.load(open(os.path.join(HERE, "camb_cl_lock.json")))["edelockP"]
    out = {"point": "edelockP", "camb": {"zc": m["zc"], "fde_zc": m["fde_zc"], "theta_i": m["theta_i"]}}
    x, hist, ok = match(m)
    out["match"] = {"targets": x.tolist(), "converged": ok, "history": hist}
    print("match", ok, hist[-1], flush=True)
    full = point_args(m) | {"fraction_axion_ac": 10 ** x[0], "log10_axion_ac": x[1],
                            "output": "tCl,pCl,lCl,mPk", "lensing": "yes", "l_max_scalars": 2600, "P_k_max_1/Mpc": 1.0}
    r = AG.run(TF, full)
    T = 2.7255e6
    l = np.arange(2, 2501)
    g3 = {}
    for k, lo in (("tt", 30), ("ee", 50)):
        D = np.array(r[k][:2499]) * l * (l + 1) / (2 * np.pi) * T ** 2
        rel = (D / np.array(cam[k][2:2501]) - 1)[lo - 2:]
        g3[k] = {"rms": float(np.sqrt((rel ** 2).mean())), "mean": float(rel.mean()), "max_abs": float(np.abs(rel).max())}
    g3["sigma8"] = {"axiclass": r["sigma8"], "camb": cam["sigma8"]}
    g3["pass"] = g3["tt"]["rms"] <= 3e-3 and g3["ee"]["rms"] <= 3e-3
    out["G-2F3"] = g3
    print("G-2F3", g3, flush=True)
    full_d = dict(full)
    full_d.update({"dilaton": "yes", "dil_kappa": 1e-6, "dil_beta": 0.0, "Omega_fld": 0})
    r2 = AG.run(TF, full_d)
    g4 = {k: float(np.sqrt(np.mean(((np.array(r2[k][28:]) - np.array(r[k][28:])) / np.array(r[k][28:])) ** 2)))
          for k in ("tt", "ee", "pp")}
    g4["pass"] = max(g4.values()) <= 1e-5
    out["G-2F4"] = g4
    print("G-2F4", g4, flush=True)
    json.dump(out, open(os.path.join(HERE, "tf_gates_ede.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
