import time, json, math, numpy as np, sys
sys.path.insert(0, 'tools/qsim')
from loom_qsim import sma_rho0, mf_run, osc_obs, bh_spectrum
from spindle_fast import sma_rho0_fast, mf_single_fast, period_analytic, bh_spectrum_sparse, _z
def tm(f, n=3):
    ts = []
    for _ in range(n): a = time.perf_counter(); r = f(); ts.append(time.perf_counter() - a)
    return sorted(ts)[n//2], r
R = {}
# S1
w = 0.0; t_ref = t_fast = 0.0
zeta = (math.sqrt(0.25), math.sqrt(0.5), math.sqrt(0.25))
for N in (6, 40, 200):
    ts = np.linspace(0, 20, 400)
    a, (r_ref, _) = tm(lambda: sma_rho0(N, 1.0, 0.3, zeta, ts)); b, (r_f, _) = tm(lambda: sma_rho0_fast(N, 1.0, 0.3, zeta, ts))
    w = max(w, float(np.max(abs(r_ref - r_f)))); t_ref += a; t_fast += b
R['S1'] = dict(max_abs=w, t_ref=t_ref, t_fast=t_fast, pass_=bool(w < 1e-12))
# S2, S3
cases = [(1, 0.3, 0.5, 0.5), (1, 1.5, 0.3, 0.0), (-1, 0.5, 0.6, 1.0)]
w2 = 0.0; t_ref = t_fast = 0.0; per = []
for c, q, r0, ph in cases:
    ts = np.linspace(0, 12, 1201)[1:]
    a, (out, _) = tm(lambda: mf_run(_z(r0, ph)[None, :].copy(), c, q, 0.0, ts, dt=1e-3), 1)
    rr = np.array([abs(p[0, 1])**2 for p in out])
    b, rf = tm(lambda: mf_single_fast(c, q, r0, ph, ts))
    w2 = max(w2, float(np.max(abs(rr - rf)))); t_ref += a; t_fast += b
    a3, ob = tm(lambda: osc_obs(c, q, r0, ph), 1); b3, pa = tm(lambda: period_analytic(c, q, r0, ph))
    per.append(dict(case=[c, q, r0, ph], period_ref=ob['period'], period_analytic=pa, rel=abs(pa/ob['period'] - 1), t_ref=a3, t_analytic=b3))
R['S2'] = dict(max_abs=w2, t_ref=t_ref, t_fast=t_fast, pass_=bool(w2 < 1e-6))
R['S3'] = dict(cases=per, pass_=bool(all(p['rel'] < 2e-3 for p in per)))
# S4
a, (e_d, D) = tm(lambda: bh_spectrum(5, 5, 0.2, 1.0, 3)); b, (e_s, _) = tm(lambda: bh_spectrum_sparse(5, 5, 0.2, 1.0, 3))
big = {}
for L in (6, 7):
    c4, (e, D2) = tm(lambda: bh_spectrum_sparse(L, L, 0.2, 1.0, 3), 1); big[f'{L},{L}'] = dict(dim=D2, E=[float(x) for x in e], t=c4)
R['S4'] = dict(max_abs=float(np.max(abs(e_d - e_s))), dim=D, t_dense=a, t_sparse=b, bigger=big, pass_=bool(np.max(abs(e_d - e_s)) < 1e-10))
json.dump(R, open('field_tests/results/speed_spindle.json', 'w'), indent=1, default=float); print(json.dumps(R, indent=1, default=float))
