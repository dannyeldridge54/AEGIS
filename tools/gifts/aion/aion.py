#!/usr/bin/env python3
"""Aion v1: Zee-Babu prediction engine (minimal model). Danny Lee Eldridge / the Weave, 23 Nov 2026 (D2188).
A lantern, not a throne: free to use, change and share.

Minimal Zee-Babu: h+ couples through antisymmetric f, k++ through symmetric g; M_nu ~ f Y g^dag Y^T f^T has det = 0,
so the lightest neutrino is massless at two loops and the f-ratios are fixed by oscillation data
(Herrero-Garcia, Nebot, Rius, Santamaria, arXiv:1402.4491). Not covered: the SU(5) embedding of arXiv:2412.14562.
    Convention: M_nu = U diag(m) U^T (PDG U); the 1402.4491 ratios are null vectors in this convention (D2188 T1).
"""
import numpy as np, json, sys

NUFIT6 = {  # NuFIT 6.0, IC19 without SK-atm (arXiv:2410.05380): (best, +1s, -1s)
 'NO': dict(s12=(0.307, .012, .011), s23=(0.561, .012, .015), s13=(0.02195, .00054, .00058), d=(177., 19., 20.),
            dm21=(7.49e-5, .19e-5, .19e-5), dm3l=(2.534e-3, .025e-3, .023e-3)),
 'IO': dict(s12=(0.308, .012, .011), s23=(0.562, .012, .015), s13=(0.02224, .00056, .00057), d=(285., 25., 28.),
            dm21=(7.49e-5, .19e-5, .19e-5), dm3l=(-2.510e-3, .024e-3, .025e-3)),
}
ALPHA, GF = 1 / 137.036, 1.1663788e-5
MEG2 = 1.5e-13          # MEG II 90% CL (arXiv:2504.15711)
DESI_SUM = 0.0642       # eV, DESI DR2 + CMB, LCDM, 95% (literature context)

def U_pmns(s12, s23, s13, d):
    c12, c23, c13 = np.sqrt(1 - s12), np.sqrt(1 - s23), np.sqrt(1 - s13)
    s12, s23, s13 = np.sqrt(s12), np.sqrt(s23), np.sqrt(s13); e = np.exp(1j * np.radians(d))
    R23 = np.array([[1, 0, 0], [0, c23, s23], [0, -s23, c23]], complex)
    U13 = np.array([[c13, 0, s13 / e], [0, 1, 0], [-s13 * e, 0, c13]], complex)
    R12 = np.array([[c12, s12, 0], [-s12, c12, 0], [0, 0, 1]], complex)
    return R23 @ U13 @ R12

def masses(o, dm21, dm3l):
    if o == 'NO': return np.array([0.0, np.sqrt(dm21), np.sqrt(dm3l)])
    m2 = np.sqrt(-dm3l); return np.array([np.sqrt(m2 ** 2 - dm21), m2, 0.0])   # IO: dm3l = dm32 < 0, m3 = 0

def f_ratios(o, s12, s23, s13, d):
    """1402.4491 null-vector relations (returns f_etau/f_mutau, f_emu/f_mutau)."""
    t12, t13 = np.sqrt(s12 / (1 - s12)), np.sqrt(s13 / (1 - s13)); c23, s23r, c13 = np.sqrt(1 - s23), np.sqrt(s23), np.sqrt(1 - s13)
    e = np.exp(-1j * np.radians(d))
    if o == 'NO': return t12 * c23 / c13 + t13 * s23r * e, t12 * s23r / c13 - t13 * c23 * e
    return -s23r / t13 * e, c23 / t13 * e

def hplus_br(ret, rem):
    """Gamma(h+ -> l_a nu) ~ sum_b |f_ab|^2 with f_mutau = 1: e, mu, tau."""
    fet, fem, fmt = abs(ret) ** 2, abs(rem) ** 2, 1.0
    w = np.array([fem + fet, fem + fmt, fet + fmt]); return w / w.sum()

def mbb_band(o, p, n=721):
    U = U_pmns(p['s12'], p['s23'], p['s13'], p['d']); m = masses(o, p['dm21'], p['dm3l'])
    vals = []
    for a in np.linspace(0, 2 * np.pi, n):   # only one Majorana phase is physical when m_lightest = 0
        ph = np.array([1, np.exp(1j * a), 1]) if o == 'NO' else np.array([1, np.exp(1j * a), 1])
        vals.append(abs(np.sum((U[0] ** 2) * ph * m)))
    return min(vals), max(vals), m.sum()

def fmt_ceiling(ret, mh_tev):
    """|f_mutau| max from MEG II via BR = alpha |f_etau f_mutau|^2/(48 pi GF^2 mh^4), with f_etau = ret * f_mutau."""
    mh = mh_tev * 1e3; ff2 = MEG2 * 48 * np.pi * GF ** 2 * mh ** 4 / ALPHA
    return np.sqrt(np.sqrt(ff2) / abs(ret))

def best(o): return {k: v[0] for k, v in NUFIT6[o].items()}

def sample(o, rng, N):
    out = {}
    for k, (b, up, dn) in NUFIT6[o].items():
        z = rng.standard_normal(N); out[k] = b + np.where(z > 0, up, dn) * z
    out['d'] = np.mod(out['d'], 360.0); return out

def run(N=20000, seed=2188):
    rng = np.random.default_rng(seed); R = {}
    for o in ('NO', 'IO'):
        p = best(o); ret, rem = f_ratios(o, p['s12'], p['s23'], p['s13'], p['d'])
        lo, hi, sm = mbb_band(o, p); br = hplus_br(ret, rem)
        S = sample(o, rng, N); BR = []; RT = []
        for i in range(N):
            a, b = f_ratios(o, S['s12'][i], S['s23'][i], S['s13'][i], S['d'][i]); BR.append(hplus_br(a, b)); RT.append([abs(a), abs(b)])
        BR, RT = np.array(BR), np.array(RT); q = lambda x: [float(np.percentile(x, 16)), float(np.percentile(x, 84))]
        R[o] = dict(f_etau_over_f_mutau=[float(ret.real), float(ret.imag)], abs_ratios=[float(abs(ret)), float(abs(rem))],
                    abs_ratio_1sigma=dict(f_etau=q(RT[:, 0]), f_emu=q(RT[:, 1])),
                    hplus_BR_e_mu_tau=[float(x) for x in br], hplus_BR_1sigma=dict(e=q(BR[:, 0]), mu=q(BR[:, 1]), tau=q(BR[:, 2])),
                    mbb_band_meV=[lo * 1e3, hi * 1e3], sum_mnu_eV=float(sm), sum_vs_DESI_DR2=('below' if sm < DESI_SUM else 'ABOVE') + ' 0.0642 eV',
                    f_mutau_ceiling_MEGII={str(m): float(fmt_ceiling(ret, m)) for m in (0.5, 1, 2, 5)})
    return R

if __name__ == '__main__':
    print(json.dumps(run(), indent=1))
