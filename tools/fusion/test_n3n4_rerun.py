"""N3+N4 (PREREG_N3N4_RESONANCE)."""
import json, os, sys, warnings, numpy as np
warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ndata as N, resonance as R
ENDF = os.path.join(HERE, 'ndata', 'endf')
th = 0.0253; d1 = {'Li6_n,t': (N.at('Li6', 105, th), 940, .02), 'H1_n,g': (N.at('H1', 102, th), .3326, .02), 'Li7_n,g': (N.at('Li7', 102, th), .0454, .05),
                   'Fe56_n,g': (N.at('Fe56', 102, th), 2.59, .03), 'Mn55_n,g': (N.at('Mn55', 102, th), 13.3, .03)}
E14 = 14.1e6
li7t = N.at('Li7', 205, E14) if 205 in N.mts('Li7') else None
d2 = {'Be9_n,2n': (N.at('Be9', 16, E14), .5, .20), 'Pb208_n,2n': (N.at('Pb208', 16, E14), 2.2, .15), 'Li7_triton(MT205)': (li7t, .3, .30)}
ok = lambda v: v[0] is not None and abs(v[0] / v[1] - 1) <= v[2]
res = dict(D1={k: dict(value=v[0], ref=v[1], ok=ok(v)) for k, v in d1.items()}, D2={k: dict(value=v[0], ref=v[1], ok=ok(v)) for k, v in d2.items()})
def compare(nuc, tape, EH, form=None):
    E0, el0 = N.xs(nuc, 2, '0K'); Ec, cc = N.xs(nuc, 102, '294K'); cap0 = np.interp(E0, Ec, cc); sel = (E0 >= 1e-5) & (E0 <= EH); E = E0[sel]   # DEV-0: no 0 K capture in HDF5 (info only)
    x = R.xs(os.path.join(ENDF, tape), E, form)
    out = {}
    for nm, ref, ours in (('elastic', el0[sel], x['elastic']), ('capture', cap0[sel], x['capture'])):
        m = ref > 0; rd = np.abs(ours[m] / ref[m] - 1)
        out[nm] = dict(n=int(m.sum()), median=float(np.median(rd)), p95=float(np.percentile(rd, 95)), max=float(rd.max()))
    return out, E, x, el0[sel]
mn, Emn, xmn, elmn = compare('Mn55', 'n-025_Mn_055-ENDF8.0.endf', 125e3)
zr, _, _, _ = compare('Zr90', 'n-040_Zr_090-ENDF8.0.endf', 200e3)
zs, _, _, _ = compare('Zr90', 'n-040_Zr_090-ENDF8.0.endf', 200e3, 'SLBW')
w = (Emn > 200) & (Emn < 500); i = np.argmax(xmn['elastic'][w]); j = np.argmax(elmn[w])
peak = dict(E_ours=float(Emn[w][i]), E_eval=float(Emn[w][j]), el_ours=float(xmn['elastic'][w][i]), el_eval=float(elmn[w][j]))
G = dict(D1=all(v['ok'] for v in res['D1'].values()), D2=all(v['ok'] for v in res['D2'].values()),
         R1=mn['elastic']['median'] <= .005 and mn['elastic']['p95'] <= .03, R2=zr['elastic']['median'] <= .005 and zr['elastic']['p95'] <= .03,   # DEV-0
         R3=abs(peak['E_ours'] - 340.7875) <= 1 and abs(peak['el_ours'] / peak['el_eval'] - 1) <= .02, R4=zs['elastic']['median'] > .005)
res.update(goals=G, Mn55_RM=mn, Zr90_MLBW=zr, Zr90_SLBW=zs, Mn55_peak=peak)
json.dump(res, open(os.path.join(HERE, '..', '..', 'field_tests', 'results', 'n3n4_rerun.json'), 'w'), indent=1, default=float)
print(json.dumps(res, indent=1, default=float))
