import json, math, numpy as np, sys
sys.path.insert(0, 'tools/qsim'); from loom_qsim import mf_run
c2 = 23.7; w = 2*math.pi   # energies in Hz -> angular: H/hbar = 2*pi*E[Hz]; time in s
def period(q, Tmax=0.2, n=4000):
    z = np.array([math.sqrt(0.25), math.sqrt(0.5), math.sqrt(0.25)], complex)   # rho0 = 0.5, theta = 0
    ts = np.linspace(0, Tmax, n+1)[1:]; out, _ = mf_run(z[None, :].copy(), w*c2, w*q, 0.0, ts, dt=2e-5)
    r = np.array([abs(p[0, 1])**2 for p in out]); y = r - r.mean(); i = np.where((y[:-1] < 0) & (y[1:] >= 0))[0]
    if len(i) < 2: return float('nan'), float(r.max()-r.min())
    cr = ts[i] + (ts[i+1]-ts[i])*(-y[i])/(y[i+1]-y[i]); return float(np.mean(np.diff(cr))*1e3), float(r.max()-r.min())
qs = np.arange(10, 70.01, 1.0); T = []; A = []
for q in qs: t, a = period(q); T.append(t); A.append(a)
T = np.array(T); fine = np.arange(18, 30.01, 0.25); Tf = [period(q)[0] for q in fine]
Tf = np.array(Tf); qstar = float(fine[np.nanargmax(Tf)]) if np.any(np.isfinite(Tf)) else float('nan')
def at(q): return period(q)[0]
P1 = abs(qstar - c2)/c2 < 0.10
t15, t42, t65 = at(15), at(42), at(65)
P2 = all(5 <= x <= 40 for x in (t15, t42, t65)) and t65 < t42
R = dict(c2_Hz=c2, q_star_Hz=qstar, P1=bool(P1), T15=t15, T42=t42, T65=t65, P2=bool(P2),
         T_curve=dict(q_Hz=qs.tolist(), T_ms=[None if not np.isfinite(x) else x for x in T], amp=A),
         fine=dict(q_Hz=fine.tolist(), T_ms=[None if not np.isfinite(x) else x for x in Tf]),
         P3_estimate='t_break ~ sqrt(N): N=1e5 -> ~ (1e5/2000)^0.49 * t_b(2000) ≈ 6.8x longer than at N=2000 (label: estimate from D2183 L3)')
json.dump(R, open('field_tests/results/d2184_qsim_vs_liu2023.json', 'w'), indent=1); print({k: v for k, v in R.items() if k not in ('T_curve', 'fine')})
