"""MISSING-PIECE M3 (field_tests/rules/PREREG_MISSING_PIECE.md): BAO residual map, DESI DR2 and SDSS, against the
DESI-HOLDOUT LCDM fit (no BAO), with the holdout FLAG-1 overlaid.
    python m3_map.py     -> field_tests/results/missing_piece_m3.json      (coupled build, both models; AI-assisted)
Needs cmb-fit/results/cmp_*_nodesi_s8y6.json and field_tests/desi_holdout/predict_LCDM.json (Test A)."""
import json, os, sys, types
import numpy as np
from scipy.stats import chi2 as C2

HERE = os.path.dirname(os.path.abspath(__file__)); AEG = os.path.abspath(os.path.join(HERE, "..", ".."))
RULE = os.path.join(AEG, "field_tests", "rules", "PREREG_MISSING_PIECE.md")
assert os.path.exists(RULE + ".sha256"), "rule not locked"
for n in ("candl", "candl.interface", "spt_candl_data"):
    sys.modules.setdefault(n, types.SimpleNamespace(CandlCobayaLikelihood=None, SPT3G_D1_TnE=None, interface=None))
sys.modules["candl"].interface = sys.modules["candl.interface"]
sys.path.insert(0, os.path.join(AEG, "cmb-fit", "axiclass"))
import early_late_spa as E, spiral_guess
FLAG = "ax_spa_spiraltwist_kappa1_nlfix"; E._maybe_coupled(FLAG)
import classy


def cls(base, st):
    """The same CLASS setup from a stored minimum as m2_eg.cls (copied, so M2 is not re-run on import)."""
    info = E.make(base)
    a = dict(info["theory"]["classytwist"]["extra_args"])
    for k in ("lensing", "l_max_scalars", "non_linear"): a.pop(k, None)
    a.update({"A_s": 1e-10 * np.exp(st["logA"]), "n_s": st["n_s"], "100*theta_s": st["theta_s_1e2"],
              "omega_b": st["omega_b"], "omega_cdm": st["omega_cdm"], "tau_reio": st["tau_reio"], "output": ""})
    if "spiraltwist" in base:
        b = st["scf_coupling_beta"]; a["scf_coupling_beta"] = b
        a["scf_parameters"] = f"1.0, 0.0, {spiral_guess.mu1_guess(1.0, b, st['omega_b'], st['omega_cdm'])}, 0.0, 0.0, 0.0"
    c = classy.Class(); c.set(a); c.compute()
    return c
C = 299792.458
D = os.path.join(AEG, "cmb-fit", "packages", "data", "bao_data")


def load():
    S = []   # surveys: (name, z array, quantity array, value array, cov)
    m = np.loadtxt(os.path.join(D, "desi_bao_dr2", "desi_gaussian_bao_ALL_GCcomb_mean.txt"), dtype=str)
    S.append(("DESI DR2", m[:, 0].astype(float), m[:, 2], m[:, 1].astype(float),
              np.loadtxt(os.path.join(D, "desi_bao_dr2", "desi_gaussian_bao_ALL_GCcomb_cov.txt"))))
    m = np.loadtxt(os.path.join(D, "sdss_DR12Consensus_bao.dat"), dtype=str)
    S.append(("SDSS DR12", m[:, 0].astype(float), m[:, 2], m[:, 1].astype(float), np.loadtxt(os.path.join(D, "BAO_consensus_covtot_dM_Hz.txt"))))
    m = np.loadtxt(os.path.join(D, "sdss_DR16_LRG_BAO_DMDH.dat"), dtype=str)
    S.append(("SDSS DR16 LRG", m[:, 0].astype(float), m[:, 2], m[:, 1].astype(float), np.loadtxt(os.path.join(D, "sdss_DR16_LRG_BAO_DMDH_covtot.txt"))))
    m = np.loadtxt(os.path.join(D, "sdss_DR16_QSO_BAO_DMDH.txt"), dtype=str)
    S.append(("SDSS DR16 QSO", m[:, 0].astype(float), m[:, 2], m[:, 1].astype(float), np.loadtxt(os.path.join(D, "sdss_DR16_QSO_BAO_DMDH_covtot.txt"))))
    return S


def pred(c, z, q):
    rd = c.rs_drag(); dm = c.angular_distance(z) * (1 + z); hz = c.Hubble(z); dh = 1 / hz
    return {"DM_over_rs": dm / rd, "DH_over_rs": dh / rd, "DV_over_rs": (z * dm * dm * dh) ** (1 / 3) / rd,
            "bao_Hz_rs": hz * C * rd / 147.78}[q]


def pred_all(c, S):
    out = []
    for name, zs, qs, vals, cov in S:
        p = np.array([pred(c, z, q) * (147.78 if (name == "SDSS DR12" and q == "DM_over_rs") else 1) for z, q in zip(zs, qs)])
        out.append(p)
    return out


def main():
    S = load()
    mods = {}
    for lab, base, name in (("LCDM", "ax_spa_lcdm_halofit", "ax_spa_lcdm_halofit_nodesi_s8y6"),
                            ("FLAG-1", FLAG, "ax_spa_spiraltwist_kappa1_nlfix_nodesi_s8y6")):
        st = json.load(open(f"{E.OUT}/cmp_{name}.json"))["minimum"]
        c = cls(base, st); mods[lab] = pred_all(c, S); c.struct_cleanup(); c.empty()
    ref = mods["LCDM"]
    res, chi = {}, {"LCDM": {}, "FLAG-1": {}}
    R = {}
    for (name, zs, qs, vals, cov), r0, f1 in zip(S, ref, mods["FLAG-1"]):
        frac = vals / r0 - 1; J = np.diag(1 / r0); fc = J @ cov @ J
        R[name] = (zs, qs, frac, fc)
        res[name] = [{"z": float(z), "q": q, "frac_resid": round(float(x), 5), "err": round(float(np.sqrt(fc[i, i])), 5),
                      "flag1_frac": round(float(f1[i] / r0[i] - 1), 5)} for i, (z, q, x) in enumerate(zip(zs, qs, frac))]
        Ci = np.linalg.inv(cov)
        for lab, p in (("LCDM", r0), ("FLAG-1", f1)):
            d = vals - p; chi[lab][name] = round(float(d @ Ci @ d), 3)
    # gate: DESI chi2 of the holdout LCDM vs Test A (Cobaya)
    ta = json.load(open(os.path.join(AEG, "field_tests", "desi_holdout", "predict_LCDM.json")))["chi2_DESI"]
    gate = abs(chi["LCDM"]["DESI DR2"] - ta) <= 0.1
    # matched comparison: DESI vs SDSS at z ~ 0.51, 0.70, 1.48 (DM, DH); SDSS DR12 H residual -> DH residual = -H residual
    def pick(name, z, q):
        zs, qs, frac, fc = R[name]; i = [k for k in range(len(zs)) if abs(zs[k] - z) < 0.02 and qs[k] == q][0]; return i
    pairs = [(("DESI DR2", 0.51, "DM_over_rs"), ("SDSS DR12", 0.51, "DM_over_rs"), 1),
             (("DESI DR2", 0.51, "DH_over_rs"), ("SDSS DR12", 0.51, "bao_Hz_rs"), -1),
             (("DESI DR2", 0.706, "DM_over_rs"), ("SDSS DR16 LRG", 0.698, "DM_over_rs"), 1),
             (("DESI DR2", 0.706, "DH_over_rs"), ("SDSS DR16 LRG", 0.698, "DH_over_rs"), 1),
             (("DESI DR2", 1.484, "DM_over_rs"), ("SDSS DR16 QSO", 1.48, "DM_over_rs"), 1),
             (("DESI DR2", 1.484, "DH_over_rs"), ("SDSS DR16 QSO", 1.48, "DH_over_rs"), 1)]
    n = len(pairs); dvec = np.zeros(n); Cd = np.zeros((n, n))
    for a, (A, B, sg) in enumerate(pairs):
        ia = pick(*A); ib = pick(*B)
        dvec[a] = R[A[0]][2][ia] - sg * R[B[0]][2][ib]
        for b, (A2, B2, sg2) in enumerate(pairs):
            ja = pick(*A2); jb = pick(*B2)
            if A[0] == A2[0]: Cd[a, b] += R[A[0]][3][ia, ja]
            if B[0] == B2[0]: Cd[a, b] += sg * sg2 * R[B[0]][3][ib, jb]
    x2 = float(dvec @ np.linalg.inv(Cd) @ dvec); p = float(C2.sf(x2, n))
    reading = ("NO VERDICT (gate failed)" if not gate else "SURVEYS AGREE" if p >= 0.05 else
               "TENSION" if p >= 0.01 else "SURVEYS DISAGREE")
    out = {"rule": "PREREG_MISSING_PIECE.md M3", "reference": "DESI-HOLDOUT LCDM (no BAO)",
           "gate": {"chi2_DESI_LCDM_here": chi["LCDM"]["DESI DR2"], "testA_cobaya": ta, "pass": bool(gate)},
           "residuals": res, "chi2_by_survey": chi,
           "desi_minus_sdss": {"pairs": [f"{A[0]} z{A[1]} {A[2]} vs {B[0]} z{B[1]} {B[2]}" for A, B, _ in pairs],
                               "diff": [round(float(v), 5) for v in dvec], "err": [round(float(np.sqrt(Cd[i, i])), 5) for i in range(n)],
                               "chi2": round(x2, 3), "dof": n, "p": p},
           "reading": reading}
    json.dump(out, open(os.path.join(AEG, "field_tests", "results", "missing_piece_m3.json"), "w"), indent=1)
    print(json.dumps({k: out[k] for k in ("gate", "chi2_by_survey", "desi_minus_sdss", "reading")}, indent=1))


if __name__ == "__main__":
    main()
