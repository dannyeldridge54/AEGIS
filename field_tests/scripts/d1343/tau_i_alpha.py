"""D1343 (locked PREREG_D1343): tau = i alpha_s on the ripple-free compiled exact MS path. AI-assisted."""
import sys, math, numpy as np, sympy as sp
sys.path.insert(0, '.')
from tools.serapis_calc.ms_jit import build, spectra_msjit
x, eps = sp.symbols('x eps'); y = sp.exp(sp.sqrt(2)*x); q = sp.exp(-2*sp.pi*y)
lj = 2*sp.pi*y + sp.log(1 + 744*q + 196884*q**2); L = lj + sp.log(1 - 1728*sp.exp(-lj))          # l < 300 branch, y > 1 (j > 1728)
I = sp.log(sp.exp(2*(L - sp.log(1728))) + 1)/(4*sp.pi); I1 = sp.log(sp.exp(L - sp.log(1728)) + 1)/(4*sp.pi)
OLD = {1.40e-4: (0.97462, 4.8335e-4, -8.543e-4), 1.45e-4: (0.97509, 4.9100e-4, -8.587e-4)}
phi0 = math.log(40)/math.sqrt(2); dl = tuple(np.linspace(-0.1, 0.1, 9))
for e in (1.40e-4, 1.45e-4):
    m = 2.28e11 + (e - 1.3e-4)/0.3e-4*(2.65e11 - 2.28e11); Ns = 50.31 + 0.5*math.log(m/1.9e11)
    mj = build((I**2/(I**2 + 1) + e*I1).subs(eps, e), x)
    s = spectra_msjit(mj, phi0, Ns, dlnk=dl, bd=4000.0); n0, r0, a0 = OLD[e]
    gate = abs(s['ns'] - n0) <= 5e-5 and abs(s['r']/r0 - 1) <= 0.01
    print(f"eps={e:.2e} N*={Ns:.3f}: n_s {s['ns']:.6f} (D1247 {n0}) r {s['r']:.5e} (D1247 {r0:.4e}) alpha_s {s['alpha_s']:.5e} (D1247 {a0:.3e}) "
          f"d_alpha {s['alpha_s'] - a0:+.2e}  gate {'PASS' if gate else 'FAIL'}", flush=True)
