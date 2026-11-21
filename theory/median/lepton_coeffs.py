"""Normalised flux-6 (a = 0) turnover amplitudes at the Higgs corner -> lepton coefficients (D1893)."""
import sys, json, math, numpy as np
sys.path.insert(0, 'theory/tests'); from z3_modes import z3_classes, modes, w
M, a = 6, 0.0
g = 160; s, t = np.meshgrid((np.arange(g)+.5)/g, (np.arange(g)+.5)/g); Z = (s + w*t).ravel()
fps = np.array([0, 0.5773502692j, 0.5 + 0.2886751346j])
res, ev, V, C = z3_classes(M, a, a); cls = np.round(((np.angle(ev)/(2*math.pi)) % 1)*3) % 3
Fz = modes(M, a, a, Z); Ff = modes(M, a, a, fps)
def basis(c):
    B = V[:, cls == c]; G = (Fz@B).conj().T@(Fz@B)/len(Z)         # Gram over the cell (mean |psi|^2)
    L = np.linalg.cholesky(G); return B@np.linalg.inv(L).conj().T  # orthonormal (mean |psi|^2 = 1)
dims = {c: int((cls == c).sum()) for c in np.unique(cls)}; e_cls = [c for c, d in dims.items() if d == 1][0]
Be = basis(e_cls)[:, 0]; ae = np.abs(Ff@Be); own = np.argmax(ae)
rat = {j: ae[j]/ae[own] for j in range(3) if j != own}; cH = min(rat, key=lambda j: abs(rat[j]-0.177))
print('electron class', e_cls, 'own corner', own, 'ratios', {k: round(v, 4) for k, v in rat.items()}, '-> Higgs corner', cH)
amp = {}
for c in dims:
    if c == e_cls: continue
    B = basis(c); amp[c] = float(np.linalg.norm(Ff[cH]@B))      # max normalised |psi(cH)| over the class
tau_c = max(amp, key=amp.get); mu_c = min(amp, key=amp.get)
a_e = float(ae[cH]); print('normalised amps at Higgs corner: e %.4f  mu(class %d) %.4f  tau(class %d) %.4f' % (a_e, mu_c, amp[mu_c], tau_c, amp[tau_c]))
ce, cmu = a_e/amp[tau_c], amp[mu_c]/amp[tau_c]; print('c_e = %.4f  c_mu = %.4f' % (ce, cmu))
p = 'theory/median/centre.json'; c = json.load(open(p)); c['electron_corner_amp'] = round(ce, 5); c['c_mu'] = round(cmu, 5); json.dump(c, open(p, 'w'), indent=1)
