"""S4d (locked PREREG_S4d_scalar_stability)."""
import sympy as sp, mpmath as mp
mp.mp.dps = 40
src = open('theory/strings/s4b_6d_vacuum.py').read().split("e1 = ")[0]; ns = {}; exec(compile(src, 's4b', 'exec'), ns)
A, P, y, D, gam, w = ns['A'], ns['P'], ns['y'], ns['D'], ns['gam'], ns['w']
yend = sp.pi/2/(w*sp.sqrt(sp.Rational(2*(D-1), D-2)))
R = sp.lambdify(y, sp.diff(A, y)/sp.diff(P, y), 'mpmath'); thr = -sp.Rational(8, 1)/(gam*(D-2)**2)
ye = mp.mpf(sp.N(yend, 40)); vals = []
for i in range(4000):
    t = mp.mpf('1e-6') + (1 - 2*mp.mpf('1e-6'))*i/mp.mpf(3999); vals.append((R(t*ye), t))
mn = min(vals, key=lambda v: v[0])
L = [f"D = {D}, gamma = {gam}, threshold -8/(gamma (D-2)^2) = {thr} = {float(thr):.6f}",
     f"A'/P' range on (1e-6, 1-1e-6) y_end: min {float(mn[0]):.6f} at y/y_end = {float(mn[1]):.4g}; max {float(max(v[0] for v in vals)):.6f}",
     f"ends: y/y_end=1e-6: {float(vals[0][0]):.6f}; 1-1e-6: {float(vals[-1][0]):.6f}"]
ok = all(v[0] >= thr for v in vals)
L.append("S4d: " + ("condition (5.10) holds everywhere -> SCALAR SECTOR STABLE (b >= 0)" if ok else "condition fails somewhere -> UNDECIDED by this test"))
open('field_tests/results/s4d_scalar.txt', 'w').write('\n'.join(L)+'\n'); print('\n'.join(L))
