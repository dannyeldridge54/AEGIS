import json, math, time, numpy as np, sys
sys.path.insert(0, 'tools/qsim'); from loom_qsim import *
def zeta(r0, ph): return np.array([math.sqrt((1-r0)/2)*np.exp(1j*ph/2), math.sqrt(r0), math.sqrt((1-r0)/2)*np.exp(1j*ph/2)])
def tbreak(N, c, q, r0, ph, T=40.0, n=800):
    ts = np.linspace(0, T, n+1)[1:]; z = zeta(r0, ph)
    rq, _ = sma_rho0(N, c, q, z, ts); out, _ = mf_run(z[None, :].copy(), c, q, 0.0, ts, dt=2e-3); rm = np.array([abs(p[0,1])**2 for p in out])
    i = np.where(abs(rq - rm) > 0.02)[0]; return float(ts[i[0]]) if len(i) else float(T)
def obs(c, q, r0, ph, J, U):
    o = osc_obs(c, q, rho0=r0, phi=ph); e = bh_spectrum(4, 4, J, U, 2)[0]
    z = zeta(r0, ph); ts = np.linspace(0, 12, 601)[1:]; out, _ = mf_run(z[None,:].copy(), c, q, 0.0, ts, dt=2e-3)
    return dict(period=o['period'], amplitude=o['amplitude'], mean_rho0=float(np.mean([abs(p[0,1])**2 for p in out])),
                t_break=tbreak(2000, c, q, r0, ph), E0=float(e[0]), gap=float(e[1]-e[0]))
R = {}
d0 = dict(c=1.0, q=0.3, r0=0.5, ph=0.5, J=0.2, U=1.0)
cp = compass(lambda **k: obs(**k), d0, eps=2e-2)
names = list(cp['base']); dials = list(d0)
M = np.array([[cp['log_sensitivity'][d][o] for d in dials] for o in names])
s = np.linalg.svd(np.nan_to_num(M), compute_uv=False)
R['L1'] = dict(base=cp['base'], jacobian_rows=names, jacobian_cols=dials, J=M.tolist(), singular_values=s.tolist(),
               lens_rank=int(np.sum(s/s[0] > 1e-2)), dominant_dial=cp['dominant_dial'])
cs = np.linspace(0.8, 1.2, 7); qs = np.linspace(0.1, 0.6, 7); X = []; Y = []
t0 = time.time()
for c in cs:
    for q in qs:
        o = osc_obs(c, q); X.append((c, q)); Y.append((o['period'], o['amplitude']))
t_twin = (time.time() - t0)/len(X); X = np.array(X); Y = np.array(Y)
def feats(x): c, q = x[:,0], x[:,1]; return np.vstack([np.ones_like(c), c, q, c*c, c*q, q*q]).T
err = []
for i in range(len(X)):
    m = np.ones(len(X), bool); m[i] = False
    co = np.linalg.lstsq(feats(X[m]), Y[m], rcond=None)[0]; pr = feats(X[i:i+1]) @ co
    err.append(np.abs(pr[0] - Y[i])/np.abs(Y[i]))
err = np.array(err); co = np.linalg.lstsq(feats(X), Y, rcond=None)[0]
t0 = time.time(); [feats(X[:1]) @ co for _ in range(2000)]; t_emu = (time.time() - t0)/2000
R['L2'] = dict(grid='c 0.8-1.2 x q 0.1-0.6 (7x7)', loo_max_rel_err_period=float(err[:,0].max()), loo_max_rel_err_amp=float(err[:,1].max()),
               loo_median_rel_err=[float(np.median(err[:,0])), float(np.median(err[:,1]))], twin_s_per_eval=t_twin, emu_s_per_eval=t_emu,
               speedup=t_twin/t_emu, pass_=bool(err.max() < 0.02))
Ns = [250, 500, 1000, 2000, 4000, 8000]; tb = [tbreak(N, 1.0, 0.3, 0.5, 0.5, T=80.0, n=1600) for N in Ns]
lN = np.log(Ns); a, b = np.polyfit(lN, np.log(tb), 1); r_pow = float(np.std(np.log(tb) - (a*lN + b)))
al, bl = np.polyfit(lN, tb, 1); r_log = float(np.std(np.array(tb) - (al*lN + bl))/np.mean(tb))
R['L3'] = dict(N=Ns, t_break=tb, power_law_exponent=float(a), power_resid_rel=r_pow, lnN_slope=float(al), lnN_resid_rel=r_log,
               better_fit='power law' if r_pow < r_log else 'ln N')
json.dump(R, open('field_tests/results/d2183_lenses.json', 'w'), indent=1, default=float)
print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk not in ('J',)} for k, v in R.items()}, indent=1, default=float))
