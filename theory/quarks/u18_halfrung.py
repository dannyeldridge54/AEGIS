"""PREREG_U18_HALFRUNG"""
import sys, json, numpy as np
sys.path.insert(0, 'theory/quarks'); import q11_minima as Q
w = np.exp(2j * np.pi / 3); out = {}
for m in (0.25, 0.5, 0.75, 1.0):
    t, v = Q.minimum(m, 0); e = t - w
    out[str(m)] = dict(tau=[t.real, t.imag], eps_abs=abs(e), arg_deg=float(np.degrees(np.angle(e))), V=v, formula=0.0251 / (m + 1 / 16))
print(json.dumps(out, indent=1))
