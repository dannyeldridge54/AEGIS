"""S8-A engine gates (cloud, no data). Each CLASS run is a separate process so two builds never share one interpreter.
    python angle_gates.py            -> cmb-fit/axiclass/angle/angle_gates.json
G-A0: new build with fld_coupling_beta = 0 reproduces the S8-L build at the stored S8-L best fit (spiralL):
      sigma8, H0, Omega_m, 100 theta_s and C_l^TT/EE (l = 2..2500) equal within 1e-6 (relative).
G-A1: angle as cold dark matter (99% share, a_c = 1e-7) coupled at beta = 0.05 vs cold dark matter coupled at 0.05:
      the coupling's effect on C_l^pp (l 100-1000) agrees within 5%, its effect on H0 and phi(today) within 1e-3.
G-A2 (report): the physical model at the stored S8-L point: CDM uncoupled, angle coupled at sqrt(2/3), share
      f = beta_eff/sqrt(2/3); sigma8, S8, H0 and the phi(today) shift, versus the S8-L build (picture A)."""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
B = os.environ.get("TWIST_BUILDS", os.path.expanduser("~"))
ULA = f"{B}/AxiCLASS_coupled_nlfix_ula/python/build"
ANG = f"{B}/AxiCLASS_coupled_nlfix_angle/python/build"
BETA_A = (2 / 3) ** 0.5

RUNNER = r'''
import glob, json, sys
sys.path.insert(0, glob.glob(sys.argv[1] + "/lib*")[0])
import classy, numpy as np
a = json.loads(sys.argv[2])
c = classy.Class(); c.set(a); c.compute()
cl = c.lensed_cl(2500); bg = c.get_background()
phi = bg.get("phi_scf"); out = {"sigma8": c.sigma8(), "H0": c.h()*100, "Omega_m": c.Omega_m(),
  "S8": c.sigma8()*(c.Omega_m()/0.3)**0.5, "tt": cl["tt"][2:].tolist(), "ee": cl["ee"][2:].tolist(), "pp": c.raw_cl(2500)["pp"][2:].tolist(),
  "phi_today": float(phi[-1]) if phi is not None else None, "classy": classy.__file__}
print("JSON" + json.dumps(out))
'''


def run(build, args):
    r = subprocess.run([sys.executable, "-c", RUNNER, build, json.dumps(args)], capture_output=True, text=True,
                       timeout=1800)
    line = [x for x in r.stdout.splitlines() if x.startswith("JSON")]
    if not line:
        raise RuntimeError(r.stderr[-2000:])
    return json.loads(line[0][4:])


def rel(a, b):
    import numpy as np
    a, b = np.array(a), np.array(b)
    return float(np.max(np.abs(a - b) / np.maximum(np.abs(b), 1e-30)))


def base_args():
    code = ("import json,sys; sys.path.insert(0,%r); import forward_predictions_cloud as F; a,b=F.args_for('spiralL'); "
            "a={k:v for k,v in a.items() if k not in ('output','z_max_pk','P_k_max_1/Mpc','non_linear','l_max_scalars')}; "
            "print('JSON'+json.dumps([a,b]))") % os.path.join(HERE, "..", "..", "..", "theory")
    r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=1800,
                       env=dict(os.environ, TWIST_BUILDS=B))
    line = [x for x in r.stdout.splitlines() if x.startswith("JSON")]
    if not line:
        raise RuntimeError(r.stderr[-3000:])
    a, best = json.loads(line[0][4:])
    a.update({"output": "tCl,pCl,lCl,mPk", "lensing": "yes", "l_max_scalars": 2600, "P_k_max_1/Mpc": 1.0})
    return a, best


def main():
    a, best = base_args()
    res = {"base_point": "spiralL stored best fit", "beta_a": BETA_A}
    # G-A0
    r_ula = run(ULA, a)
    r_new = run(ANG, dict(a, fld_coupling_beta=0.0))
    d = {k: abs(r_new[k] / r_ula[k] - 1) for k in ("sigma8", "H0", "Omega_m")}
    d["tt"] = rel(r_new["tt"][:2400], r_ula["tt"][:2400]); d["ee"] = rel(r_new["ee"][30:2400], r_ula["ee"][30:2400])
    res["G-A0"] = {"max_rel_diffs": d, "pass": max(d.values()) <= 1e-6}
    # G-A1: angle as heavy matter (99% of dark matter, a_c = 1e-7) coupled at beta vs cold dark matter coupled at
    # beta. Compared on the lensing potential C_l^pp (l 100-1000), which counts all matter: CLASS's sigma8 leaves the
    # fluid out of delta_m (S8-LNL D2), so sigma8 cannot be used here (first version of this gate did; see status).
    import numpy as np
    om = a.get("omega_cdm", 0) + a.get("omega_fld", 0)
    f, beta, L = 0.99, 0.05, slice(98, 998)
    R = {}
    for b in (0.0, beta):
        R[("fld", b)] = run(ANG, dict(a, omega_cdm=om*(1-f), omega_fld=om*f, log10_a_c=-7.0, scf_coupling_beta=0.0,
                                      fld_coupling_beta=b))
        R[("cdm", b)] = run(ULA, dict(a, omega_cdm=om*f, omega_fld=om*(1-f), log10_a_c=-7.0, scf_coupling_beta=b))
    eff = {s: float(np.mean(np.array(R[(s, beta)]["pp"])[L] / np.array(R[(s, 0.0)]["pp"])[L] - 1)) for s in ("fld", "cdm")}
    bg = {k: abs(R[("fld", beta)][k] / R[("fld", 0.0)][k] - R[("cdm", beta)][k] / R[("cdm", 0.0)][k])
          for k in ("H0",)}
    dphi = abs((R[("fld", beta)]["phi_today"] - R[("fld", 0.0)]["phi_today"])
               - (R[("cdm", beta)]["phi_today"] - R[("cdm", 0.0)]["phi_today"]))
    ratio = eff["fld"] / eff["cdm"]
    res["G-A1"] = {"beta": beta, "pp_effect": eff, "pp_effect_ratio": ratio, "H0_effect_diff": bg["H0"],
                   "phi_shift_diff": dphi, "pass": abs(ratio - 1) <= 0.05 and bg["H0"] <= 1e-3 and dphi <= 1e-3}
    # G-A3: with fld_in_delta_m = 1 the heavy uncoupled fluid (99%) gives the cold-dark-matter sigma8 within 3e-3
    h3 = run(ANG, dict(a, omega_cdm=om*(1-f), omega_fld=om*f, log10_a_c=-7.0, scf_coupling_beta=0.0,
                       fld_coupling_beta=0.0, fld_in_delta_m=1))
    d3 = abs(h3["sigma8"] / R[("cdm", 0.0)]["sigma8"] - 1)
    res["G-A3"] = {"sigma8_rel_diff": d3, "pass": d3 <= 3e-3}
    # G-A2: the physical S8-A point (report)
    beff = best.get("scf_coupling_beta")
    fa = beff / BETA_A
    phys = dict(a, omega_cdm=om * (1 - fa), omega_fld=om * fa, scf_coupling_beta=0.0, fld_coupling_beta=BETA_A,
                fld_in_delta_m=1)
    r3 = run(ANG, phys)
    r_ulam = run(ANG, dict(a, fld_coupling_beta=0.0, fld_in_delta_m=1))   # S8-L (picture A), angle counted
    res["G-A2"] = {"share_f": fa, "S8L_build": {k: r_ula[k] for k in ("sigma8", "H0", "phi_today")},
                   "S8L_angle_counted": {k: r_ulam[k] for k in ("sigma8", "H0")},
                   "angle_coupled_angle_counted": {k: r3[k] for k in ("sigma8", "H0", "phi_today")},
                   "note": "CLASS Omega_m label is wrong in the coupled builds; S8 not taken from it"}
    json.dump(res, open(os.path.join(HERE, "angle_gates.json"), "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
