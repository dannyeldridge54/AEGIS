"""JOINT-SHEAR calibration (field_tests/rules/PREREG_JOINT_SHEAR.md; refuses to run before the lock).
    TWIST_RESULTS=<scratch dir with links to cmb-fit/results> CSL_DIR=... python js_calibrate.py points|run|fit
points: write the design (seed 0) and held-out (seed 1) points as cmp_<base>__js<tag>.json into TWIST_RESULTS.
run:    for each point not yet done: axiclass_pk -> axhm_pk -> two sequential Nelder-Mead shear minimisations
        (first from the model's LATE-BASE best nuisances, second from the first); appends to js_calib.json.
fit:    least-squares quadratic q(S8, Omega_m[, beta_eff]) on design + centre; gate G-JS on held-out (|q-full| <= 0.5)."""
import itertools
import json
import os
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
WL = os.path.dirname(HERE)
AEGIS = os.path.abspath(os.path.join(WL, "..", ".."))
RULE = os.path.join(AEGIS, "field_tests", "rules", "PREREG_JOINT_SHEAR.md")
RES = os.environ["TWIST_RESULTS"]
TABLE = os.path.join(HERE, "js_calib.json")
OUTR = os.path.join(WL, "results")
F_BETA = 0.816
MODELS = {   # base run, varied dims, LATE-BASE best nuisances (Pantheon+ rows of part2_desy3.json)
    "S8A": dict(base="S8A", n=13, dims=["logA", "omega_dm", "beta_eff"],
                start=os.path.join(OUTR, "part2_S8A_axhm_round3_own_best.ini")),
    "LCDM": dict(base="ax_spa_lcdm_halofit", n=9, dims=["logA", "omega_cdm"],
                 start=os.path.join(OUTR, "s8a_lcdm_partner", "part2_ax_spa_lcdm_halofit_axhm_round3_own_best.ini"))}
HALF = {"logA": 0.06, "omega_dm": 0.005, "omega_cdm": 0.005, "theta_s_1e2": 0.0005, "n_s": 0.008, "omega_b": 0.0003}
EXTRA = ["theta_s_1e2", "n_s", "omega_b"]          # varied only at held-out points


def centre(m):
    return json.load(open(os.path.join(RES, f"cmp_{MODELS[m]['base']}.json")))["minimum"]


def lhs(d, n, seed):
    from scipy.stats import qmc
    return qmc.LatinHypercube(d=d, seed=seed).random(n)


def point(m, u, dims):
    c = dict(centre(m))
    for x, d in zip(u, dims):
        if d == "beta_eff":
            c[d] = 0.12 * x
        elif d == "omega_dm":
            c[d] = c["omega_cdm"] + c["omega_fld"] + HALF[d] * (2 * x - 1)
        else:
            c[d] = c[d] + HALF[d] * (2 * x - 1)
    if m == "S8A":
        f = c["beta_eff"] / F_BETA
        dm = c.get("omega_dm", c["omega_cdm"] + c["omega_fld"])
        c["omega_dm"], c["omega_cdm"], c["omega_fld"] = dm, dm * (1 - f), dm * f
    # sigma8, Omega_m, H0 keep the centre values as placeholders only: S8, Omega_m and h come from CLASS (pk file)
    return c


def make_points():
    assert os.path.exists(RULE + ".sha256"), "PREREG_JOINT_SHEAR.md is not locked"
    pts = {}
    for m, s in MODELS.items():
        base = s["base"]
        pts[f"{base}__jsc"] = (m, "design", centre(m))
        for i, u in enumerate(lhs(len(s["dims"]), s["n"], 0)):
            pts[f"{base}__jsd{i:02d}"] = (m, "design", point(m, u, s["dims"]))
        for i, u in enumerate(lhs(len(s["dims"]) + 3, 4, 1)):
            pts[f"{base}__jsh{i:02d}"] = (m, "heldout", point(m, u, s["dims"] + EXTRA))
    for name, (m, kind, mn) in pts.items():
        if name.endswith("__jsc"):
            continue                                   # the centre is the stored fit itself (its own files)
        for n in (name, name + "_axhm"):
            json.dump({"minimum": mn, "js": {"model": m, "kind": kind}}, open(os.path.join(RES, f"cmp_{n}.json"), "w"), indent=1)
    json.dump({k: [v[0], v[1]] for k, v in pts.items()}, open(os.path.join(HERE, "js_points.json"), "w"), indent=1)
    print(len(pts), "points")


def sh(cmd, cwd):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(r.stdout[-2000:] + r.stderr[-2000:])
    return r.stdout


def run_all():
    assert os.path.exists(RULE + ".sha256")
    sys.path.insert(0, os.path.join(WL, "part2"))
    import run_part2 as P
    pts = json.load(open(os.path.join(HERE, "js_points.json")))
    tab = json.load(open(TABLE)) if os.path.exists(TABLE) else {"rule": "PREREG_JOINT_SHEAR.md", "points": {}}
    order = sorted(pts, key=lambda n: (not n.endswith("__jsc"), "__jsh" in n, n))    # centres, design, held-out
    for name in order:
        if name in tab["points"]:
            continue
        m, kind = pts[name]
        run = name.replace("__jsc", "")
        if not name.endswith("__jsc"):
            if not os.path.exists(os.path.join(OUTR, f"pk_{name}.npz")):
                sh([sys.executable, "axiclass_pk.py", name], os.path.join(WL, "part2"))
            if not os.path.exists(os.path.join(OUTR, f"pk_{name}_axhm.npz")):
                sh([sys.executable, "axhm_pk.py", name], os.path.join(WL, "nonlinear"))
        pk = np.load(os.path.join(OUTR, f"pk_{run}_axhm.npz"))
        s8 = float(pk["sigma_8"][0]) * (float(pk["omega_m"]) / 0.3) ** 0.5
        a = P.run("pk", f"{run}_axhm", MODELS[m]["start"], "__jsA" if name.endswith("__jsc") else "_A")
        b = P.run("pk", f"{run}_axhm", a["best_ini"], "__jsB" if name.endswith("__jsc") else "_B")
        mn = json.load(open(os.path.join(RES, f"cmp_{run}.json")))["minimum"]
        tab["points"][name] = {"model": m, "kind": kind, "S8": s8, "Omega_m": float(pk["omega_m"]),
                               "beta_eff": mn.get("beta_eff"), "chi2_WL": min(a["chi2_WL"], b["chi2_WL"]),
                               "tries": [a["chi2_WL"], b["chi2_WL"]]}
        json.dump(tab, open(TABLE, "w"), indent=1)
        print(name, tab["points"][name], flush=True)


def feats(r, m):
    x = [r["S8"], r["Omega_m"]] + ([r["beta_eff"]] if m == "S8A" else [])
    out = [1.0] + x + [a * b for a, b in itertools.combinations_with_replacement(x, 2)]
    return out


def fit():
    tab = json.load(open(TABLE))
    res = {}
    for m in MODELS:
        rows = [r for r in tab["points"].values() if r["model"] == m]
        d = [r for r in rows if r["kind"] == "design"]
        h = [r for r in rows if r["kind"] == "heldout"]
        X = np.array([feats(r, m) for r in d])
        y = np.array([r["chi2_WL"] for r in d])
        coef = np.linalg.lstsq(X, y, rcond=None)[0]
        dev = [float(np.dot(feats(r, m), coef) - r["chi2_WL"]) for r in h]
        res[m] = {"coef": coef.tolist(), "n_design": len(d), "design_rms": float(np.std(X @ coef - y)),
                  "heldout_dev": dev, "G-JS": "PASS" if h and max(abs(v) for v in dev) <= 0.5 else "FAIL"}
    tab["fit"] = res
    json.dump(tab, open(TABLE, "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    {"points": make_points, "run": run_all, "fit": fit}[sys.argv[1]]()
