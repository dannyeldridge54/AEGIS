"""Backlog G (exploratory, not locked): growth predictions for PURE-TWIST (kappa = sqrt(2/3), beta = 0) vs LCDM.
Uses the frozen best fits in field_tests/results/pure_twist_predictions.json (h, omega_b, omega_cdm) and the
tournament CLASS builder. Same primordial amplitude for both (A_s = 2.1e-9, n_s = 0.965) so the difference is the
late-time expansion only. Outputs sigma8, S8, f sigma8(z), E_G(z) (method of freeze_eg.py). AI-assisted."""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import tournament as T

AEG = os.path.abspath(os.path.join(HERE, "..", ".."))
P = json.load(open(os.path.join(AEG, "field_tests/results/pure_twist_predictions.json")))
ZS = [0.0, 0.3, 0.5, 0.7, 1.0, 1.5]; K, DZ = 0.02, 0.01
EXTRA = {"A_s": 2.1e-9, "n_s": 0.965, "output": "mPk", "P_k_max_1/Mpc": 1.0, "z_max_pk": 2.0}


def build(version, p):
    orig = T.classy.Class

    class C2(orig):
        def set(self, a):
            a = dict(a); a.update(EXTRA); a.pop("ln10^{10}A_s", None); a.pop("logA", None)
            return orig.set(self, a)
    T.classy.Class = C2
    try:
        return T.model(version, p)
    finally:
        T.classy.Class = orig


def growth(c):
    bg = c.get_background(); zz = bg["z"][::-1]; rm = bg["(.)rho_b"][::-1] + bg["(.)rho_cdm"][::-1]
    lnD = lambda q: 0.5 * np.log(c.pk_cb_lin(K, q))
    out = {}
    for z in ZS:
        zl = max(z - DZ, 0.0); f = -(1 + z) * (lnD(z + DZ) - lnD(zl)) / (z + DZ - zl)
        s8 = c.sigma(8 / c.h(), z)
        om = float(np.interp(z, zz, rm)) / (1 + z) ** 3 / c.Hubble(0) ** 2
        out[z] = {"sigma8": s8, "f": f, "fsigma8": f * s8, "E_G": om / f}
    om0 = (c.omega_b() + c.Omega0_cdm() * c.h() ** 2) / c.h() ** 2
    return out, out[0.0]["sigma8"] * np.sqrt(om0 / 0.3), om0


res = {}
for lab, ver, p in (("PURE", "SPIRAL", list(P["pure_twist_params"]) + [0.0, 0.8165]), ("LCDM", "LCDM", P["lcdm_params"])):
    c = build(ver, p); g, s8, om = growth(c); res[lab] = {"by_z": g, "S8": s8, "Omega_m": om}
    c.struct_cleanup(); c.empty()
    print(lab, f"S8 {s8:.4f} Omega_m {om:.4f}", flush=True)
for z in ZS:
    a, b = res["PURE"]["by_z"][z], res["LCDM"]["by_z"][z]
    print(f"z {z}: fsigma8 PURE {a['fsigma8']:.4f} LCDM {b['fsigma8']:.4f} ({100 * (a['fsigma8'] / b['fsigma8'] - 1):+.2f}%); "
          f"E_G PURE {a['E_G']:.4f} LCDM {b['E_G']:.4f} ({100 * (a['E_G'] / b['E_G'] - 1):+.2f}%)", flush=True)
res["note"] = "same A_s/n_s for both; background-fit parameters; exploratory"
json.dump(res, open(os.path.join(AEG, "field_tests/results/pure_twist_growth.json"), "w"), indent=1, default=float)
