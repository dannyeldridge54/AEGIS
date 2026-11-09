"""S8-A engine gates (cloud, no data). Each CLASS run is a separate process so two builds never share one interpreter.
    python angle_gates.py            -> cmb-fit/axiclass/angle/angle_gates.json
G-A0: new build with fld_coupling_beta = 0 reproduces the S8-L build at the stored S8-L best fit (spiralL):
      sigma8, H0, Omega_m, 100 theta_s and C_l^TT/EE (l = 2..2500) equal within 1e-6 (relative).
G-A1: angle as cold dark matter: share f = 0.99, angle made heavy (log10 a_c = -7), coupled at beta_a; CDM
      uncoupled. Must match the coupled-CDM build with all dark matter coupled at beta = beta_a f + ... i.e.
      the same run with the CDM coupled at beta_a (share 1 - f uncoupled is 1%): compare against the S8-L build
      with f = 0.01 light uncoupled share and CDM coupled at beta_a. sigma8 and H0 within 2e-3, C_l within 2e-3.
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
  "S8": c.sigma8()*(c.Omega_m()/0.3)**0.5, "tt": cl["tt"][2:].tolist(), "ee": cl["ee"][2:].tolist(),
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
    # G-A1: angle as heavy matter, coupled at beta_a, vs CDM coupled at beta_a
    om = a.get("omega_cdm", 0) + a.get("omega_fld", 0)
    f = 0.99
    heavy = dict(a, omega_cdm=om * (1 - f), omega_fld=om * f, log10_a_c=-7.0, scf_coupling_beta=0.0,
                 fld_coupling_beta=BETA_A)
    ref = dict(a, omega_cdm=om * f, omega_fld=om * (1 - f), log10_a_c=-7.0, scf_coupling_beta=BETA_A)
    r1 = run(ANG, heavy); r2 = run(ULA, ref)
    d1 = {k: abs(r1[k] / r2[k] - 1) for k in ("sigma8", "H0")}
    d1["tt"] = rel(r1["tt"][:2400], r2["tt"][:2400])
    res["G-A1"] = {"max_rel_diffs": d1, "pass": max(d1.values()) <= 2e-3,
                   "note": "heavy angle (a_c=1e-7) coupled at sqrt(2/3) vs CDM coupled at sqrt(2/3); 1% uncoupled rest"}
    # G-A2: the physical S8-A point (report)
    beff = best.get("scf_coupling_beta")
    fa = beff / BETA_A
    phys = dict(a, omega_cdm=om * (1 - fa), omega_fld=om * fa, scf_coupling_beta=0.0, fld_coupling_beta=BETA_A)
    r3 = run(ANG, phys)
    res["G-A2"] = {"share_f": fa, "S8L_build": {k: r_ula[k] for k in ("sigma8", "S8", "H0", "Omega_m", "phi_today")},
                   "angle_coupled": {k: r3[k] for k in ("sigma8", "S8", "H0", "Omega_m", "phi_today")}}
    json.dump(res, open(os.path.join(HERE, "angle_gates.json"), "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
