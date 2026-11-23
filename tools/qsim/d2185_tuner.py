import sys, math, json, numpy as np
sys.path.insert(0, 'tools/qsim'); from d2185_lib import ham, coherent
TMAX = 0.3*35.0
def state(B, N, r0, eta):   # theta = pi, M = 0: phi+ = (pi + eta)/2, phi- = (pi - eta)/2, phi0 = 0
    s = math.sqrt((1 - r0)/2); return coherent(B, N, s*np.exp(1j*(math.pi + eta)/2), math.sqrt(r0), s*np.exp(1j*(math.pi - eta)/2))
def goal(N, x, cache={}):
    p, r0, eta = x; H, B = ham(N, p); w, V = np.linalg.eigh(H.toarray()); c = V.conj().T @ state(B, N, r0, eta)
    ts = np.linspace(0, TMAX, 1051); amp = np.abs(np.exp(-2j*math.pi*np.outer(ts, w)) @ (np.abs(c)**2))**2
    i = int(np.argmax(np.diff(np.sign(np.diff(amp))) > 0)) + 1; k = i + int(np.argmax(amp[i:]))
    return float(amp[k]), float(ts[k])
LO = np.array([0.0, 0.3, 0.0]); HI = np.array([1.0, 0.9, 2*math.pi]); STEP = np.array([0.02, 0.02, 0.1])
out = {}
for N in (6, 10, 16, 24):
    x = np.array([0.33, 0.6, 0.0]); g, tr = goal(N, x); lr = 0.05; log = [dict(step=0, x=x.tolist(), goal=g, t_rev=tr)]
    for it in range(1, 26):
        grad = np.array([(goal(N, np.clip(x + e, LO, HI))[0] - goal(N, np.clip(x - e, LO, HI))[0])/(2*s) for e, s in ((np.eye(3)[j]*STEP[j], STEP[j]) for j in range(3))])
        scale = np.abs(grad*(HI - LO)); dom = ['p/c2', 'rho0', 'eta'][int(np.argmax(scale))]
        xn = np.clip(x + lr*grad/(np.linalg.norm(grad/(HI - LO)) + 1e-12)*(HI - LO)**0 * (HI - LO)/np.max(HI - LO), LO, HI)
        gn, trn = goal(N, xn)
        if gn > g: x, g, tr = xn, gn, trn; lr *= 1.5
        else: lr *= 0.5
        log.append(dict(step=it, x=x.tolist(), goal=g, t_rev=tr, compass=grad.tolist(), dominant=dom, lr=lr))
        print(N, it, np.round(x, 3).tolist(), round(g, 4), round(tr, 3), dom, flush=True)
    out[str(N)] = dict(best_x=dict(p_over_c2=x[0], rho0=x[1], eta=x[2]), best_F=g, t_rev_units=tr, t_rev_ms_c2_35Hz=tr/35.0*1e3, log=log)
json.dump(out, open('field_tests/results/d2185_tuner.json', 'w'), indent=1); print('TUNER DONE')
