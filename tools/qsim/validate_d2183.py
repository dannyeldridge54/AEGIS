import json, math, numpy as np, sys
sys.path.insert(0, 'tools/qsim'); from loom_qsim import *
R = {}
e, D = bh_spectrum(5, 5, 1.0, 0.0); R['V1'] = dict(E0=e[0], expect=-2*5, err=abs(e[0] + 10), dim=D, pass_=abs(e[0] + 10) < 1e-9)
e, D = bh_spectrum(5, 5, 0.0, 1.0); R['V2'] = dict(E0=e[0], gap=e[1] - e[0], err=max(abs(e[0]), abs(e[1] - e[0] - 1)), pass_=max(abs(e[0]), abs(e[1] - e[0] - 1)) < 1e-9)
N, c, q = 2000, 1.0, 0.3; rho0, phi = 0.5, 0.5
z = np.array([math.sqrt((1 - rho0)/2)*np.exp(1j*phi/2), math.sqrt(rho0), math.sqrt((1 - rho0)/2)*np.exp(1j*phi/2)])
ob = osc_obs(c, q); T1 = ob['period']; ts = np.linspace(0, T1, 201)[1:]
rq, H = sma_rho0(N, c, q, z, ts); out, _ = mf_run(z[None, :].copy(), c, q, 0.0, ts, dt=1e-3); rm = np.array([abs(p[0, 1])**2 for p in out])
R['V3'] = dict(N=N, period=T1, max_diff=float(np.max(abs(rq - rm))), pass_=float(np.max(abs(rq - rm))) < 0.02)
rng = np.random.default_rng(0); L = 8; psi = (rng.normal(size=(L, 3)) + 1j*rng.normal(size=(L, 3))); psi *= math.sqrt(100*L/np.sum(abs(psi)**2))
nb = float(np.sum(abs(psi)**2))/L; E0 = mf_energy(psi, 1.0, 0.3, 0.5, nb); N0 = float(np.sum(abs(psi)**2))
out, _ = mf_run(psi, 1.0, 0.3, 0.5, [5.0], dt=1e-3); p = out[-1]
dE = abs(mf_energy(p, 1.0, 0.3, 0.5, nb) - E0)/abs(E0); dN = abs(np.sum(abs(p)**2) - N0)/N0
R['V4'] = dict(dE_rel=dE, dN_rel=float(dN), pass_=dE < 1e-6 and dN < 1e-6)
herm = float(np.max(abs(H - H.T))); R['V5'] = dict(hermiticity=herm, pass_=herm < 1e-12)
R['ALL_PASS'] = all(v['pass_'] for k, v in R.items() if k.startswith('V'))
R['compass_sodium'] = compass(lambda c, q: osc_obs(c, q), dict(c=1.0, q=0.3))
R['compass_BH'] = compass(lambda J, U: dict(E0=bh_spectrum(4, 4, J, U, 2)[0][0], gap=float(np.diff(bh_spectrum(4, 4, J, U, 2)[0])[0])), dict(J=0.2, U=1.0))
json.dump(R, open('field_tests/results/d2183_loom_qsim.json', 'w'), indent=1, default=float); print(json.dumps(R, indent=1, default=float))
