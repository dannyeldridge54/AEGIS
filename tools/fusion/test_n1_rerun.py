import json, os, sys, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import neutron_birth as NB
from scipy import constants as sc
def hist_fwhm(T, seed):   # DEV-2: direct half-maximum width of the weighted spectrum
    rng = np.random.default_rng(seed); n = 2_000_000; kT = T * 1e-3
    vD = rng.normal(0, np.sqrt(kT / NB.MD), (n, 3)); vT = rng.normal(0, np.sqrt(kT / NB.MT), (n, 3))
    def four(m, v): g = 1 / np.sqrt(1 - (v ** 2).sum(1)); return g * m, (g * m)[:, None] * v
    ED, pD = four(NB.MD, vD); ET, pT = four(NB.MT, vT); Et, pt = ED + ET, pD + pT; s = Et ** 2 - (pt ** 2).sum(1); rs = np.sqrt(s)
    Ecm = (rs - NB.MD - NB.MT) * 1e3; vr = np.linalg.norm(vD - vT, axis=1)
    with np.errstate(over='ignore'): w = NB.sigma_bh(np.maximum(Ecm, 1e-3)) * vr
    Ens = (s + NB.MN ** 2 - NB.MA ** 2) / (2 * rs); ps = np.sqrt(Ens ** 2 - NB.MN ** 2)
    u = rng.normal(size=(n, 3)); u /= np.linalg.norm(u, axis=1)[:, None]; beta = pt / Et[:, None]; g = 1 / np.sqrt(1 - (beta ** 2).sum(1))
    E = (g * (Ens + (beta * u).sum(1) * ps) - NB.MN) * 1e3
    h, edges = np.histogram(E, bins=np.arange(E.min(), E.max() + 5, 5.0), weights=w)
    from scipy.ndimage import gaussian_filter1d
    h = gaussian_filter1d(h, 3); c = 0.5 * (edges[1:] + edges[:-1]); half = h.max() / 2; above = c[h >= half]
    return above.max() - above.min()
out = {}
for T in (5.0, 10.0, 20.0):
    rs = [NB.spectrum(T, seed=s) for s in range(1, 9)]; b = NB.ballabio(T)
    sh = np.array([r['shift_keV'] for r in rs]); fw = np.array([r['FWHM_keV'] for r in rs]); hf = np.array([hist_fwhm(T, s) for s in (11, 12, 13)])
    out[T] = dict(shift=sh.mean(), shift_sd=sh.std(ddof=1), ball_shift=b['shift_keV'], r_shift=sh.mean() / b['shift_keV'] - 1, r_shift_sigmas=(sh.mean() - b['shift_keV']) / (sh.std(ddof=1) / np.sqrt(8)),
                  FWHM_var=fw.mean(), FWHM_sd=fw.std(ddof=1), FWHM_hist=hf.mean(), ball_FWHM=b['FWHM_keV'], r_FWHM_var=fw.mean() / b['FWHM_keV'] - 1, r_FWHM_hist=hf.mean() / b['FWHM_keV'] - 1)
G = dict(B1=all(abs(v['r_shift']) <= .05 for v in out.values()), B2=all(abs(v['r_FWHM_var']) <= .02 for v in out.values()))
json.dump(dict(goals=G, rows={str(k): v for k, v in out.items()}), open(os.path.join(HERE, '..', '..', 'field_tests', 'results', 'n1_rerun.json'), 'w'), indent=1, default=float)
print(G); [print(T, {k: round(float(x), 4) for k, x in v.items()}) for T, v in out.items()]
