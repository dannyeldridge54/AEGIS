import sys, math, numpy as np
sys.path.insert(0, 'tools/janus_astro'); import sommerfeld_nlo as N
M = 2000.0; G = np.array([[2, math.sqrt(2)], [math.sqrt(2), 3]])
ne = np.linspace(1.2, 8, 600); Ss = []
for n in ne:
    x = 1 - 0.0917/n**2; E = x*2*N.DM; v = 2*math.sqrt(E/M)
    s = np.asarray(N.wino_s_nlo(M, v, nlo=False)); Ss.append(float(s @ G @ s))
Ss = np.array(Ss); pk = [i for i in range(1, len(Ss)-1) if Ss[i] > Ss[i-1] and Ss[i] > Ss[i+1]]
print("peaks n_eff:", [round(ne[i], 3) for i in pk]); print("peak S:", [f"{Ss[i]:.3g}" for i in pk])
tr = [i for i in range(1, len(Ss)-1) if Ss[i] < Ss[i-1] and Ss[i] < Ss[i+1]]; print("trough S:", [f"{Ss[i]:.3g}" for i in tr])
p = [ne[i] for i in pk]; d = np.diff(p); print("spacings:", np.round(d, 3))
a = sum(1 for q in p if q > 2) >= 4; b = all(abs(dd-1) <= 0.1 for q, dd in zip(p[1:], d) if p[p.index(q)-1] > 3)
print("mean S over scan (uniform in n_eff, not energy):", round(Ss.mean(), 2))
print("SUPPORTED" if a and b else "NOT SUPPORTED", a, b)
