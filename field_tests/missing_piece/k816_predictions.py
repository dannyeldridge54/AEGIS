"""Frozen predictions for the headline late-time model K816 (kappa = sqrt(2/3), beta fitted), 13 Nov 2026, before DESI
DR3 / Euclid. Two fits: TOURNAMENT/Pantheon+ (kappa_alpha1.json FULL) and DES Y5 (desy5_k816.json). Same methods as
pure_twist_growth.py (A_s 2.1e-9, n_s 0.965 for both models; f from linear cb P(k=0.02/Mpc); E_G = Omega_m,eff/f),
BAO D_M/r_d, D_H/r_d at DESI DR2 redshifts vs the matching LCDM fit, and effective w0, wa (effective_w.py). AI-assisted."""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import tournament as T
import types
G = types.SimpleNamespace()
_ns = {'T': T, 'np': np}
exec('ZS = [0.0, 0.3, 0.5, 0.7, 1.0, 1.5]; K, DZ = 0.02, 0.01\nEXTRA = {"A_s": 2.1e-9, "n_s": 0.965, "output": "mPk", "P_k_max_1/Mpc": 1.0, "z_max_pk": 2.0}\n\n\ndef build(version, p):\n    orig = T.classy.Class\n\n    class C2(orig):\n        def set(self, a):\n            a = dict(a); a.update(EXTRA); a.pop("ln10^{10}A_s", None); a.pop("logA", None)\n            return orig.set(self, a)\n    T.classy.Class = C2\n    try:\n        return T.model(version, p)\n    finally:\n        T.classy.Class = orig\n\n\ndef growth(c):\n    bg = c.get_background(); zz = bg["z"][::-1]; rm = bg["(.)rho_b"][::-1] + bg["(.)rho_cdm"][::-1]\n    lnD = lambda q: 0.5 * np.log(c.pk_cb_lin(K, q))\n    out = {}\n    for z in ZS:\n        zl = max(z - DZ, 0.0); f = -(1 + z) * (lnD(z + DZ) - lnD(zl)) / (z + DZ - zl)\n        s8 = c.sigma(8 / c.h(), z)\n        om = float(np.interp(z, zz, rm)) / (1 + z) ** 3 / c.Hubble(0) ** 2\n        out[z] = {"sigma8": s8, "f": f, "fsigma8": f * s8, "E_G": om / f}\n    om0 = (c.omega_b() + c.Omega0_cdm() * c.h() ** 2) / c.h() ** 2\n    return out, out[0.0]["sigma8"] * np.sqrt(om0 / 0.3), om0\n\n\n', _ns)
G.build, G.growth, G.ZS = _ns['build'], _ns['growth'], _ns['ZS']
R = os.path.join(T.AEG, "field_tests", "results")
fits = {"PantheonPlus": (json.load(open(os.path.join(R, "kappa_alpha1.json")))["params"]["FULL"],
                         json.load(open(os.path.join(R, "tournament.json")))["rows"]["LCDM"]["params_FULL"]),
        "DESY5": (json.load(open(os.path.join(R, "desy5_k816.json")))["params"],
                  json.load(open(os.path.join(R, "desy5_swap.json")))["params"]["LCDM"])}
ZB = [0.295, 0.51, 0.706, 0.934, 1.321, 1.484, 2.33]
out = {"model": "K816 (kappa sqrt(2/3), beta fitted)", "frozen": "13 Nov 2026, before DESI DR3 / Euclid", "fits": {}}
for lab, (pk, pl) in fits.items():
    ck = G.build("SPIRAL", list(pk) + [0.8165]); cl = G.build("LCDM", list(pl))
    gk, s8k, omk = G.growth(ck); gl, s8l, oml = G.growth(cl)
    bao = {}
    for z in ZB:
        rk, rl = ck.rs_drag(), cl.rs_drag()
        dmk, dml = ck.angular_distance(z) * (1 + z) / rk, cl.angular_distance(z) * (1 + z) / rl
        dhk, dhl = 1 / ck.Hubble(z) / rk, 1 / cl.Hubble(z) / rl
        bao[z] = {"DM_rd": round(dmk, 3), "DH_rd": round(dhk, 3), "dDM_pct": round(100 * (dmk / dml - 1), 2), "dDH_pct": round(100 * (dhk / dhl - 1), 2)}
    bg = ck.get_background(); z = bg["z"][::-1]; a = 1 / (1 + z)
    rm = bg["(.)rho_b"][::-1] + bg["(.)rho_cdm"][::-1]; rr = bg["(.)rho_g"][::-1] + bg["(.)rho_ur"][::-1]
    rde = bg["(.)rho_crit"][::-1] - rr - float(np.interp(0, z, rm)) * a ** -3; s = z <= 2
    w = -1 - np.gradient(np.log(rde[s]), np.log(a[s])) / 3; g = np.linspace(a[s].min(), 1, 400)
    w0, wa = np.linalg.lstsq(np.vstack([np.ones(400), 1 - g]).T, np.interp(g, a[s][::-1], w[::-1]), rcond=None)[0]
    out["fits"][lab] = {"params_K816": pk, "beta": pk[3], "S8": round(s8k, 4), "S8_LCDM": round(s8l, 4), "Omega_m": round(omk, 4),
                        "w0_eff": round(float(w0), 3), "wa_eff": round(float(wa), 3),
                        "growth": {zz: {"fsigma8": round(gk[zz]["fsigma8"], 4), "d_fsigma8_pct": round(100 * (gk[zz]["fsigma8"] / gl[zz]["fsigma8"] - 1), 2),
                                        "E_G": round(gk[zz]["E_G"], 4), "d_EG_pct": round(100 * (gk[zz]["E_G"] / gl[zz]["E_G"] - 1), 2)} for zz in G.ZS},
                        "bao": bao}
    for c in (ck, cl):
        c.struct_cleanup(); c.empty()
    f = out["fits"][lab]; print(lab, "beta", round(pk[3], 4), "S8", f["S8"], "vs", f["S8_LCDM"], "w0/wa", f["w0_eff"], f["wa_eff"],
                                "fs8 z0.5", f["growth"][0.5]["d_fsigma8_pct"], "% EG z0.5", f["growth"][0.5]["d_EG_pct"], "%", flush=True)
json.dump(out, open(os.path.join(R, "k816_predictions.json"), "w"), indent=1, default=float)
