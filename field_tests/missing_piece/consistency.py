"""CONSISTENCY (rule: field_tests/rules/PREREG_CONSISTENCY.md): beta from expansion vs beta from growth. AI-assisted.
    python consistency.py      -> field_tests/results/consistency.json      (needs betaz/const_dr2.json)
Method notes (not choices the rule leaves open):
- beta_exp: the constant-beta fit on the compressed DR2 anchor (betaz/const_dr2.json); its error from a finite-difference
  Hessian of the same chi2 at that point (steps 1e-4 in h, omega_b, omega_c; 0.005 in beta), as in betaz_fit.py.
- beta_grow: background parameters h, omega_b, omega_c from that fit; the early coupling (z >= 2) held at beta_exp;
  one late coupling beta (all three late bins equal) scanned 0 ... 0.15 in steps of 0.0025. The compressed fit carries
  no primordial amplitude, so A_s, n_s and tau come from the stored FLAG-1 Pantheon+ s8y6 minimum (the growth amplitude
  must come from somewhere; this is the flagship's own value).
- Growth data: DESI DR1 full-shape f sigma_s8 (SELFCHECK V3 conversion, EH98 no-wiggle primary, diagonal errors) and
  ACT DR6 x BOSS E_G (as MISSING-PIECE M2: asymmetric errors, systematics in quadrature)."""
import json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import betaz_build as B                      # loads the beta(z) build before anything imports classy
import betaz_fit as F
AEG = B.AEG; E = B.E; classy = B.classy; spiral_guess = B.spiral_guess
sys.path.insert(0, os.path.join(AEG, "field_tests", "selfcheck"))
import v3_desi_fs as V3
RULE = os.path.join(AEG, "field_tests", "rules", "PREREG_CONSISTENCY.md")
assert os.path.exists(RULE + ".sha256"), "rule not locked"
EG_DATA = [(0.555, 0.31, 0.06, 0.05, 0.03), (0.316, 0.49, 0.14, 0.11, 0.04)]
GRID = [round(0.0025 * i, 4) for i in range(61)]


def growth_chi2(c, wb, wc, tmpl):
    h, rd = c.h(), c.rs_drag()
    x = 0.0
    for i, z in enumerate(V3.ZEFF):
        sh = V3.shape(c, wb, wc, h, rd, z)
        sig, A, m = V3.sigma_s8(sh, tmpl["z"][V3.TRACERS[i]]["shape"], i, "nw")
        x += (c.scale_independent_growth_factor_f(z) * sig - V3.DATA[i]) ** 2 / V3.VAR[i]
    bg = c.get_background(); zz = bg["z"][::-1]; rm = bg["(.)rho_b"][::-1] + bg["(.)rho_cdm"][::-1]; H0 = c.Hubble(0)
    for z, obs, up, lo, sysf in EG_DATA:
        lnD = lambda q: 0.5 * np.log(c.pk_cb_lin(0.02, q))
        f = -(1 + z) * (lnD(z + 0.01) - lnD(z - 0.01)) / 0.02
        eg = float(np.interp(z, zz, rm)) / (1 + z) ** 3 / H0 ** 2 / f
        s = math.hypot(up if eg > obs else lo, sysf * obs); x += ((eg - obs) / s) ** 2
    return x


def main():
    cp = json.load(open(os.path.join(F.OUTD, "const_dr2.json")))["params"]
    h, wb, wc, be = cp
    chi2, _ = F.make_chi2("dr2", False)
    err = F.hessian_errors(lambda q: chi2(q, False), cp, [1e-4, 1e-4, 1e-4, 0.005])
    s_exp = err[3]
    st = json.load(open(os.path.join(E.OUT, "cmp_ax_spa_spiraltwist_kappa1_nlfix_s8y6.json")))["minimum"]
    _, tmpl = V3.template()                  # LCDM template, unchanged in this build (gated in V3)
    scan = []
    for b in GRID:
        g = spiral_guess.mu1_guess(1.0, be, wb, wc, h=h)
        a = dict(B.SPIRAL, h=h, omega_b=wb, omega_cdm=wc, tau_reio=st["tau_reio"], A_s=1e-10 * np.exp(st["logA"]),
                 n_s=st["n_s"], output="mPk", z_max_pk=2.0, scf_coupling_beta=be, scf_beta1=b, scf_beta2=b, scf_beta3=b,
                 scf_parameters=f"1.0, 0.0, {g}, 0.0, 0.0, 0.0", **{"P_k_max_1/Mpc": 2.0})
        try:
            c = classy.Class(); c.set(a); c.compute(); x = growth_chi2(c, wb, wc, tmpl); c.struct_cleanup(); c.empty()
        except Exception as ex:
            x = None; print(b, "failed", ex, flush=True)
        scan.append([b, x]); print(b, x, flush=True)
    ok = [(b, x) for b, x in scan if x is not None]
    bmin, xmin = min(ok, key=lambda t: t[1])
    inside = [b for b, x in ok if x <= xmin + 1]
    lo, hi = min(inside), max(inside)
    s_grow = (hi - lo) / 2 if hi > lo else 0.0025
    edge = lo <= GRID[0] or hi >= GRID[-1]
    sc = math.hypot(s_exp or 0, s_grow); d = abs(bmin - be)
    if d <= 2 * sc:
        reading = "ONE COUPLING EXPLAINS BOTH" if (s_grow < 0.04 and not edge) else "CONSISTENT BUT UNCONSTRAINED"
    else:
        reading = "TENSION" if d <= 3 * sc else "INCONSISTENT"
    out = {"rule": "PREREG_CONSISTENCY.md", "beta_exp": be, "sigma_exp": s_exp, "beta_grow": bmin,
           "interval_grow_dchi2_1": [lo, hi], "sigma_grow": s_grow, "interval_hits_scan_edge": edge,
           "sigma_comb": sc, "diff_in_sigma": d / sc if sc else None, "reading": reading,
           "precision_note": "sigma_grow < 0.01 would test beta = 0.041 from growth alone at ~2.5-4 sigma",
           "scan": scan, "amplitude_from": "cmp_ax_spa_spiraltwist_kappa1_nlfix_s8y6 (logA, n_s, tau_reio)"}
    json.dump(out, open(os.path.join(AEG, "field_tests", "results", "consistency.json"), "w"), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != "scan"}, indent=1))


if __name__ == "__main__":
    main()
