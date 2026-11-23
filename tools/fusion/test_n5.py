"""N5 (PREREG_N5_DOPPLER)."""
import json, os, sys, warnings, numpy as np
warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ndata as N, resonance as R, doppler as D
ENDF = os.path.join(HERE, 'ndata', 'endf')
def run(nuc, tape, EH, awr):
    E0, el0h = N.xs(nuc, 2, '0K'); x = R.xs(os.path.join(ENDF, tape), E0)
    Ec294, c294 = N.xs(nuc, 102, '294K')
    el_in = np.where(E0 <= EH, x['elastic'], el0h)                     # above the RRR: evaluated 0 K elastic (smooth)
    cap_in = np.where(E0 <= EH, x['capture'], np.interp(E0, Ec294, c294))
    res = {}
    for T in (294, 900):
        for mt, inp in ((2, el_in), (102, cap_in)):
            Et, st = N.xs(nuc, mt, f'{T}K'); sel = (Et >= 1.0) & (Et <= EH) & (st > 0); Eo = Et[sel]
            ours = D.broaden(E0, inp, awr, T, Eo); rd = np.abs(ours / st[sel] - 1)
            res[f'{T}K_MT{mt}'] = dict(n=int(sel.sum()), median=float(np.median(rd)), p95=float(np.percentile(rd, 95)), max=float(rd.max()), E_at_max=float(Eo[np.argmax(rd)]))
            if mt == 102 and T == 900:
                u = np.interp(Eo, E0, cap_in); ru = np.abs(u / st[sel] - 1); res['unbroadened_vs_900K_capture_median'] = float(np.median(ru))
    th0 = float(np.interp(0.0253, E0, cap_in)); th9 = float(D.broaden(E0, cap_in, awr, 900, np.array([0.0253]))[0])
    res['thermal_0K'] = th0; res['thermal_900K'] = th9
    return res
mn = run('Mn55', 'n-025_Mn_055-ENDF8.0.endf', 125e3, 54.4661)
zr = run('Zr90', 'n-040_Zr_090-ENDF8.0.endf', 200e3, 89.22686)
ok = lambda r: all(r[k]['median'] <= .002 and r[k]['p95'] <= .01 for k in r if k.endswith(('MT2', 'MT102')))
G = dict(P1=ok(mn), P2=ok(zr), P3=mn['unbroadened_vs_900K_capture_median'] > .02, P4=abs(mn['thermal_900K'] / mn['thermal_0K'] - 1) <= .005)
out = dict(goals=G, Mn55=mn, Zr90=zr)
json.dump(out, open(os.path.join(HERE, '..', '..', 'field_tests', 'results', 'n5_doppler.json'), 'w'), indent=1)
print(json.dumps(out, indent=1))
