# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under the Hippocratic License 3.0 with the Military Activities and Mass Surveillance modules (HL3-MIL-SV; see LICENSE): free to everyone, for any use that respects human rights.
"""The FP rule's own regression check: with axion_sinh_x0 off, the Fingerprint build must reproduce the base build to
every printed digit. Also checks that with it on, the field near its minimum matches the plain cosine (g(d) ~ d).
    python regress_sinh.py      -> fp_regress.json (gate for the FP fits: "pass": true)
Each build is loaded in its own process (two classy modules cannot share one)."""
import glob
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BLD = os.environ.get("TWIST_BUILDS", os.path.expanduser("~"))
BASE = os.path.join(BLD, "AxiCLASS/python/build")
SINH = os.path.join(BLD, "AxiCLASS_sinh/python/build")
POINT = {"omega_b": 0.02261, "omega_cdm": 0.1260, "H0": 70.6, "tau_reio": 0.0553, "A_s": 2.128e-9, "n_s": 0.9805,
         "N_ncdm": 1, "m_ncdm": 0.06, "N_ur": 2.0328, "output": "tCl,pCl,lCl,mPk", "lensing": "yes", "l_max_scalars": 3000,
         "do_shooting": "yes", "do_shooting_scf": "yes", "scf_potential": "axion", "n_axion": 3,
         "security_small_Omega_scf": 0.001, "n_axion_security": 2.09, "use_big_theta_scf": "yes",
         "scf_has_perturbations": "yes", "attractor_ic_scf": "no", "scf_tuning_index": 0,
         "fraction_axion_ac": 0.078, "log10_axion_ac": -3.553, "scf_parameters": "2.79, 0."}
CHILD = r'''
import glob, json, sys
sys.path.insert(0, glob.glob(sys.argv[1] + "/lib*")[0])
import classy
assert classy.__file__.startswith(sys.argv[1])
c = classy.Class(); c.set(json.loads(sys.argv[2])); c.compute()
cl = c.lensed_cl(2500)
out = {"h": c.h(), "sigma8": c.sigma8(), "rs_drag": c.rs_drag(),
       "tt": [cl["tt"][l] for l in (2, 30, 220, 800, 1500, 2500)], "ee": [cl["ee"][l] for l in (30, 300, 1000, 2000)]}
print(json.dumps(out))
'''


def run(build, extra=None):
    p = dict(POINT, **(extra or {}))
    r = subprocess.run([sys.executable, "-c", CHILD, build, json.dumps(p)], capture_output=True, text=True)
    if r.returncode:
        return {"error": r.stderr.strip()[-400:]}
    return json.loads(r.stdout.strip().splitlines()[-1])


def flat(d):
    return [d["h"], d["sigma8"], d["rs_drag"], *d["tt"], *d["ee"]]


def main():
    base, off, on = run(BASE), run(SINH), run(SINH, {"axion_sinh_x0": 2.1445})
    out = {"base": base, "sinh_off": off, "sinh_on_x0_2.1445": on}
    if any("error" in d for d in (base, off)):
        out.update({"pass": False, "reason": "a build failed to run"})
    else:
        same = all(a == b for a, b in zip(flat(base), flat(off)))         # every digit, as the rule requires
        out["option_off_identical"] = same
        out["option_on_runs"] = "error" not in on
        if "error" not in on:
            out["option_on_max_rel_diff_vs_cosine"] = max(abs(a / b - 1) for a, b in zip(flat(on), flat(base)))
        out["pass"] = bool(same and "error" not in on)
    json.dump(out, open(os.path.join(HERE, "fp_regress.json"), "w"), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k not in ("base", "sinh_off", "sinh_on_x0_2.1445")}, indent=1))


if __name__ == "__main__":
    main()
