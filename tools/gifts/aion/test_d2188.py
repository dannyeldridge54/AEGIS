import numpy as np, json
from aion import *
out = {}
for o in ('NO', 'IO'):
    p = best(o); U = U_pmns(p['s12'], p['s23'], p['s13'], p['d']); m = masses(o, p['dm21'], p['dm3l'])
    ret, rem = f_ratios(o, p['s12'], p['s23'], p['s13'], p['d']); v = np.array([1.0, -ret, rem])
    res = {}
    for name, M in (('M=U* D U^dag', U.conj() @ np.diag(m) @ U.conj().T), ('M=U D U^T', U @ np.diag(m) @ U.T)):
        res[name] = float(np.linalg.norm(M @ v) / (np.linalg.norm(M) * np.linalg.norm(v)))
    lo, hi, sm = mbb_band(o, p)
    t2 = (1.0 <= lo * 1e3 and hi * 1e3 <= 4.5) if o == 'NO' else (15 <= lo * 1e3 and hi * 1e3 <= 50)
    out[o] = dict(T1_null_residual=res, T1_pass_any=bool(min(res.values()) < 1e-10), T1_convention_that_passes=min(res, key=res.get), mbb_meV=[lo * 1e3, hi * 1e3], T2_pass=bool(t2), sum_mnu=float(sm))
    print(o, res, 'mbb %.2f-%.2f meV' % (lo * 1e3, hi * 1e3), 'T2', t2, 'sum %.4f' % sm)
json.dump(out, open('d2188_tests.json', 'w'), indent=1)
