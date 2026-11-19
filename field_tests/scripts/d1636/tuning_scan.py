"""D1636 tuning flag (PREREG): fraction of the viable u_i range with chi2 <= chi2_min + 1, other params at RT10 best fit (cloud arm)."""
import sys, json, numpy as np
out = {}
for sn in ('pantheonplus', 'union3', 'desy5'):
    import importlib.util
    sys.argv = ['x', 'rt10', sn]
    spec = importlib.util.spec_from_file_location(f'rtfit_{sn}', 'field_tests/scripts/d1636/rt_fit.py')
    mod = importlib.util.module_from_spec(spec); sys.modules[spec.name] = mod; spec.loader.exec_module(mod); G = vars(mod)
    b = json.load(open(f'field_tests/results/D1636/rt10_{sn}.json'))['best']
    us = np.linspace(0.002, 0.3, 150); c = np.array([G['chi2']([b['H0'], b['ombh2'], b['omch2'], u]) for u in us])
    ok = c < 1e9; umax = float(us[ok].max()); cmin = float(c[ok].min())
    win = us[ok & (c <= cmin + 1)]
    out[sn] = dict(u_viable_max=umax, chi2_min_scan=cmin, window=[float(win.min()), float(win.max())],
                   frac_of_viable=float((win.max() - win.min()) / umax), chi2_at_u0=float(c[0]))
    print(sn, out[sn], flush=True)
json.dump(out, open('field_tests/results/D1636/tuning_scan.json', 'w'), indent=1)
