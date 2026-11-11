"""SELFCHECK V3: DESI DR1 full-shape fσ_s8 (PREREG_SELFCHECK.md; conversion fixed in SELFCHECK_DEVIATIONS.md D2).
    python v3_desi_fs.py gate    -> template vs Table 11 (must pass before any model is computed)
    python v3_desi_fs.py score   -> field_tests/results/selfcheck_v3.json
AI-assisted."""
import json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "theory"))

ZEFF = [0.295, 0.510, 0.706, 0.919, 1.317, 1.491]
TRACERS = ["BGS", "LRG1", "LRG2", "LRG3", "ELG2", "QSO"]
SIG_FID = [0.6936, 0.6210, 0.5638, 0.5108, 0.4320, 0.4042]     # Table 11
FS_FID = [0.4723, 0.4733, 0.4608, 0.4398, 0.3944, 0.3750]      # Table 11
RD_FID_H = 99.0792                                              # Mpc/h, Table 11
DATA = [0.396326, 0.547632, 0.479541, 0.438454, 0.372661, 0.436849]          # Appendix A, SF+BAO
VAR = [x * 1e-4 for x in (80.924891, 35.284297, 23.061044, 17.011310, 11.811326, 21.028703)]
A_SH, S8 = 0.6, 8.0
TEMPLATE = {"omega_b": 0.02237, "omega_cdm": 0.1200, "h": 0.6736, "n_s": 0.9649, "A_s": 2.0830e-9, "tau_reio": 0.0544,
            "N_ur": 2.0328, "N_ncdm": 1, "m_ncdm": 0.06, "output": "mPk", "z_max_pk": 2.0, "P_k_max_1/Mpc": 2.0}
H_FID = TEMPLATE["h"]
KP = math.pi / (RD_FID_H / H_FID)            # 1/Mpc


def eh98_ratio(k, wb, wc, h, Tcmb=2.7255):
    """EH98 no-wiggle / full transfer squared, k in 1/Mpc (Eisenstein & Hu 1998, eqs. 2-24, 29-31)."""
    wm = wb + wc; fb = wb / wm; fc = wc / wm; th = Tcmb / 2.7
    zeq = 2.50e4 * wm * th ** -4; keq = 7.46e-2 * wm * th ** -2
    b1 = 0.313 * wm ** -0.419 * (1 + 0.607 * wm ** 0.674); b2 = 0.238 * wm ** 0.223
    zd = 1291 * wm ** 0.251 / (1 + 0.659 * wm ** 0.828) * (1 + b1 * wb ** b2)
    R = lambda z: 31.5 * wb * th ** -4 * (1e3 / z)
    Req, Rd = R(zeq), R(zd)
    s = 2 / (3 * keq) * math.sqrt(6 / Req) * math.log((math.sqrt(1 + Rd) + math.sqrt(Rd + Req)) / (1 + math.sqrt(Req)))
    ksilk = 1.6 * wb ** 0.52 * wm ** 0.73 * (1 + (10.4 * wm) ** -0.95)
    q = k / (13.41 * keq)
    a1 = (46.9 * wm) ** 0.670 * (1 + (32.1 * wm) ** -0.532); a2 = (12.0 * wm) ** 0.424 * (1 + (45.0 * wm) ** -0.582)
    ac = a1 ** -fb * a2 ** (-fb ** 3)
    bb1 = 0.944 / (1 + (458 * wm) ** -0.708); bb2 = (0.395 * wm) ** -0.0266
    bc = 1 / (1 + bb1 * (fc ** bb2 - 1))
    def T0(kk, al, be):
        qq = kk / (13.41 * keq); C = 14.2 / al + 386 / (1 + 69.9 * qq ** 1.08)
        L = np.log(math.e + 1.8 * be * qq); return L / (L + C * qq * qq)
    f = 1 / (1 + (k * s / 5.4) ** 4)
    Tc = f * T0(k, 1, bc) + (1 - f) * T0(k, ac, bc)
    y = (1 + zeq) / (1 + zd)
    G = y * (-6 * math.sqrt(1 + y) + (2 + 3 * y) * math.log((math.sqrt(1 + y) + 1) / (math.sqrt(1 + y) - 1)))
    ab = 2.07 * keq * s * (1 + Rd) ** -0.75 * G
    bnode = 8.41 * wm ** 0.435; bbeta = 0.5 + fb + (3 - 2 * fb) * math.sqrt((17.2 * wm) ** 2 + 1)
    st = s / (1 + (bnode / (k * s)) ** 3) ** (1 / 3)
    Tb = (T0(k, 1, 1) / (1 + (k * s / 5.2) ** 2) + ab / (1 + (bbeta / (k * s)) ** 3) * np.exp(-(k / ksilk) ** 1.4)) \
        * np.sinc(k * st / math.pi)
    T = fb * Tb + fc * Tc
    # no-wiggle (eqs. 29-31)
    ag = 1 - 0.328 * math.log(431 * wm) * fb + 0.38 * math.log(22.3 * wm) * fb ** 2
    snw = 44.5 * math.log(9.83 / wm) / math.sqrt(1 + 10 * wb ** 0.75)       # Mpc
    gam = wm / h * (ag + (1 - ag) / (1 + (0.43 * k * snw) ** 4))
    qn = k / h * th ** 2 / gam
    L0 = np.log(2 * math.e + 1.8 * qn); C0 = 14.2 + 731 / (1 + 62.5 * qn)
    Tnw = L0 / (L0 + C0 * qn * qn)
    return (Tnw / T) ** 2


def pk_funcs(c, wb, wc, h, z, kk):
    try:
        P = np.array([c.pk_cb_lin(k, z) for k in kk])
    except Exception:
        P = np.array([c.pk_lin(k, z) for k in kk])
    return P, P * eh98_ratio(kk, wb, wc, h)


def shape(c, wb, wc, h, rd_mpc, z, fid=None):
    """Return dict(nw={Asp, lnratio slope inputs}, raw=...) for a model at z."""
    rho = (RD_FID_H / H_FID) / rd_mpc
    eps = 0.02
    kk = KP * np.exp(np.array([-eps, 0.0, eps]))
    P_raw, P_nw = pk_funcs(c, wb, wc, h, z, kk * rho)
    return {"raw": rho ** 3 * P_raw, "nw": rho ** 3 * P_nw}


def sigma_s8(sh, shf, i, kind):
    A = sh[kind][1] / shf[kind][1]
    lr = np.log(sh[kind] / shf[kind])
    m = (lr[2] - lr[0]) / (2 * 0.02)
    sig = SIG_FID[i] * math.sqrt(A) * math.exp(m / (2 * A_SH) * math.tanh(A_SH * math.log(RD_FID_H / S8)))
    return sig, A, m


def template():
    import classy
    c = classy.Class(); c.set(TEMPLATE); c.compute()
    rd = c.rs_drag(); h = c.h()
    out = {"rd_mpc": rd, "rd_mpch": rd * h, "z": {}}
    for i, z in enumerate(ZEFF):
        f = c.scale_independent_growth_factor_f(z)
        try: s = c.sigma_cb(S8 / h, z)
        except Exception: s = c.sigma(S8 / h, z)
        out["z"][TRACERS[i]] = {"f": f, "sigma_s8_class": s, "fs_class": f * s,
                                "shape": shape(c, TEMPLATE["omega_b"], TEMPLATE["omega_cdm"], h, rd, z)}
    return c, out


def gate():
    c, t = template()
    rows, ok = {}, True
    for i, tr in enumerate(TRACERS):
        z = t["z"][tr]
        dev = z["fs_class"] / FS_FID[i] - 1
        sig, A, m = sigma_s8(z["shape"], z["shape"], i, "nw")
        fs_conv = z["f"] * sig
        dev2 = fs_conv / FS_FID[i] - 1
        rows[tr] = {"fs_table11": FS_FID[i], "fs_template_direct": round(z["fs_class"], 5),
                    "fs_template_via_Eq11": round(fs_conv, 5), "dev_direct": round(dev, 5), "dev_Eq11": round(dev2, 5),
                    "A": A, "m": m}
        ok &= abs(dev2) <= 0.01 and abs(A - 1) < 1e-9 and abs(m) < 1e-9
    res = {"rd_fid_mpch_class": t["rd_mpch"], "rd_fid_table11": RD_FID_H, "rows": rows, "GATE": "PASS" if ok else "FAIL"}
    print(json.dumps(res, indent=1, default=float))
    json.dump(res, open(os.path.join(ROOT, "field_tests/results/selfcheck_v3_gate.json"), "w"), indent=1, default=float)
    return c, t, ok


def model_args(name):
    import forward_predictions_cloud as F
    a, best = F.args_for(name)
    a["z_max_pk"] = 2.0; a["P_k_max_1/Mpc"] = 2.0
    return a, best


def score():
    from scipy.stats import chi2 as C2
    sys.path.insert(0, os.path.join(ROOT, "cmb-fit", "axiclass"))
    import early_late_spa as E0
    E0._maybe_coupled("ax_spa_spiraltwist_kappa1_nlfix")   # coupled build for template and all fits (as V1)
    c0, t, ok = gate()
    if not ok:
        print("GATE FAILED: NO VERDICT"); return
    import classy
    sets = [("Pantheon+", ""), ("Dovekie", "_dovekie"), ("Union3", "_union3")]
    out = {"rule": "PREREG_SELFCHECK.md V3; conversion D2", "gate": "PASS", "fits": {}}
    for sn, suf in sets:
        for lab, name in (("FLAG-1", f"ax_spa_spiraltwist_kappa1{suf}_nlfix_s8y6"), ("LCDM", f"ax_spa_lcdm_halofit{suf}_s8y6")):
            a, best = model_args(name)
            c = classy.Class(); c.set(a); c.compute()
            h, rd = c.h(), c.rs_drag()
            r = {"pred": {}, "chi2": {}}
            for kind in ("nw", "raw"):
                pr, ch = [], 0.0
                for i, z in enumerate(ZEFF):
                    sh = shape(c, best["omega_b"], best["omega_cdm"], h, rd, z)
                    sig, A, m = sigma_s8(sh, t["z"][TRACERS[i]]["shape"], i, kind)
                    fs = c.scale_independent_growth_factor_f(z) * sig
                    pr.append({"tracer": TRACERS[i], "fs8": round(fs, 5), "A": round(A, 5), "m": round(m, 5)})
                    ch += (fs - DATA[i]) ** 2 / VAR[i]
                p = float(C2.sf(ch, 6))
                r["pred"][kind] = pr
                r["chi2"][kind] = {"chi2": round(ch, 3), "p": p,
                                   "reading": "CONSISTENT" if p >= 0.01 else ("FAIL" if p < 0.001 else "TENSION")}
            c.struct_cleanup()
            out["fits"].setdefault(sn, {})[lab] = r
            print(sn, lab, r["chi2"], flush=True)
        f, l = out["fits"][sn]["FLAG-1"]["chi2"], out["fits"][sn]["LCDM"]["chi2"]
        out["fits"][sn]["dchi2_FS"] = {k: round(f[k]["chi2"] - l[k]["chi2"], 3) for k in ("nw", "raw")}
    agree = all(out["fits"][sn][m]["chi2"]["nw"]["reading"] == out["fits"][sn][m]["chi2"]["raw"]["reading"]
                for sn, _ in sets for m in ("FLAG-1", "LCDM"))
    P = out["fits"]["Pantheon+"]
    out["READING"] = (f"FLAG-1 {P['FLAG-1']['chi2']['nw']['reading']}, LCDM {P['LCDM']['chi2']['nw']['reading']} (Pantheon+ primary)"
                      if agree else "NO VERDICT (primary and alternative P_nw disagree)")
    json.dump(out, open(os.path.join(ROOT, "field_tests/results/selfcheck_v3.json"), "w"), indent=1, default=float)
    print(out["READING"])


if __name__ == "__main__":
    {"gate": gate, "score": score}[sys.argv[1]]()
