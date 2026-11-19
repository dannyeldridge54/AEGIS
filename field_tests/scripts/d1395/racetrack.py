"""D1395 (locked PREREG_D1395_racetrack.md): racetrack toy for W_s/W at S minima."""
import json, math, numpy as np
d = 0.5; s = np.linspace(0.5, 60, 20000); L = s + d
out = dict(qualifying=[], all_minima=[])
for N, M in ((5, 6), (6, 7), (8, 9), (9, 10), (10, 12)):
    a, b = 2*math.pi/N, 2*math.pi/M
    for B in (0.5, 1, 1.5, 2, 3):
        W = np.exp(-a*s) - B*np.exp(-b*s); Ws = -a*np.exp(-a*s) + b*B*np.exp(-b*s)
        for kap in (0, 0.5, 1, 1.5, 1.9):
            c = kap*W**2   # extra F-term scaled to W² at each point (κ fixed)
            V = L*Ws**2 - 2*W*Ws + (c - 2*W**2)/L
            dV = np.gradient(V, s); d2 = np.gradient(dV, s)
            idx = np.where((dV[:-1] < 0) & (dV[1:] >= 0))[0]
            for i in idx:
                if i < 2 or i > len(s) - 3 or d2[i] <= 0: continue
                ratio = Ws[i]/W[i] if W[i] != 0 else float('nan')
                rec = dict(N=N, M=M, B=B, kappa=kap, s=float(s[i]), Ws_over_W=float(ratio), Beff=float(2*W[i]**2 - c[i]), A0=float(-2*W[i]*Ws[i]))
                out['all_minima'].append(rec)
                if -1e-2 <= ratio <= -1e-3 and rec['Beff'] > 0 and rec['A0'] > 0: out['qualifying'].append(rec)
print('minima found:', len(out['all_minima']), ' qualifying:', len(out['qualifying']))
for r in out['qualifying'][:10]: print(r)
rs = sorted(r['Ws_over_W'] for r in out['all_minima'])
print('W_s/W over all minima: min %.3g median %.3g max %.3g' % (rs[0], rs[len(rs)//2], rs[-1]) if rs else 'none')
json.dump(out, open('field_tests/results/D1395_racetrack.json', 'w'), indent=1)
