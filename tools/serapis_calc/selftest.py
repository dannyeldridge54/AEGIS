"""Independent cross-checks. Exit code 0 only if every check passes."""
import math, sys
import mpmath as mp
from .eisenstein import E_fourier, E_lattice
from .potentials import slope_sign_symbolic, P3
from . import relation as R
fails = []
def check(name, ok, info=''):
    print(('PASS ' if ok else 'FAIL ') + name + ('  ' + info if info else ''))
    if not ok: fails.append(name)
# 1. Fourier vs lattice at rho, i, 2i (lattice truncation error ~ 2*pi*y/(2N^2) relative)
for (x, y) in [(0.5, 3**0.5/2), (0.0, 1.0), (0.0, 2.0)]:
    f, l = E_fourier(x, y), E_lattice(x, y)
    check(f'E(tau,2) Fourier=lattice at ({x},{y:.4f})', abs(f-l) < 2e-4, f'{f:.6f} vs {l:.6f}')
# 2. modular invariance: E(-1/tau) = E(tau) at a generic point
t = complex(0.23, 1.37); tt = -1/t
check('E invariant under S', abs(E_fourier(t.real, t.imag)-E_fourier(tt.real, tt.imag)) < 1e-9)
check('E invariant under T', abs(E_fourier(0.23, 1.37)-E_fourier(1.23, 1.37)) < 1e-9)
# 3. rho is the minimum of E(tau,2) (Rankin/Montgomery): compare nearby points
er = E_fourier(0.5, 3**0.5/2)
check('E(rho,2) below neighbours', all(E_fourier(0.5+dx, 3**0.5/2+dy) > er for dx, dy in [(0.02,0),(0,0.02),(0,-0.0),(-0.02,0.01)] if (dx,dy)!=(0,0)))
# 4. slope sign of P3 (D943 lesson)
check('dP3/dE > 0 (no turnaround)', str(slope_sign_symbolic()) == '(C*E**2 + 2*C*E + 1)/(E + 1)**2', str(slope_sign_symbolic()))
# 5. relation: x=0 limits and the paper-1 worked numbers
ns = 0.972
r0 = 2*((1-ns)/(2*math.sqrt(2)))**2   # r that gives x=0 for p=2sqrt2
check('alpha_s(x=0) = -(1-ns)^2/2', abs(R.alpha_s(ns, r0, 2*math.sqrt(2), 0.5)+(1-ns)**2/2) < 1e-15)
check('beta_s(x=0) = -(1-ns)^3/2', abs(R.beta_s(ns, r0, 2*math.sqrt(2), 0.5)+(1-ns)**3/2) < 1e-15)
a = R.alpha_s(0.972, 5e-4, 2*math.sqrt(2), 0.5)
check('paper 1: SERAPIS alpha_s = -8.1e-4 at (0.972, 5e-4)', abs(a+8.1e-4) < 0.06e-4, f'{a:.3e}')
# 6. exponent rule (D929)
p, al = R.exponent(1, 2)
check('p(n=1,k=2) = 2sqrt2, alpha = 1/12', abs(p-2*math.sqrt(2)) < 1e-12 and abs(al-1/12) < 1e-12)
from .eisenstein import E_paper
check('E_paper(rho,2) = 5.7833593 (v3 convention)', abs(E_paper(0.5,3**0.5/2)-5.7833593)<1e-5, f'{E_paper(0.5,3**0.5/2):.7f}')
# 7. exact MS against the quadratic potential (slow-roll: n_s = 1 - 2/(N+1/2), r = 8/(N+1/2))
from .ms import Background, spectra
bg = Background(lambda p: 0.5*p*p, lambda p: p, 17.0)
res = spectra(bg, 60.0)
check('MS quadratic N=60: n_s ~ 0.9669', abs(res['ns']-(1-2/60.5)) < 1e-3, f"{res['ns']:.5f}")
check('MS quadratic N=60: r ~ 0.1322', abs(res['r']/(8/60.5)-1) < 0.02, f"{res['r']:.4f}")
check('MS quadratic: alpha_s ~ -2/(N+1/2)^2', abs(res['alpha_s']+2/60.5**2) < 2e-4, f"{res['alpha_s']:.2e}")
# --- level tests (one independent check per level) ---
import numpy as np
# L4: power-law inflation is exact: n_s = 1 - 2/(q-1), r = 16/q, alpha_s = 0 (q = 2/lam^2)
lamb = 0.2; q = 2/lamb**2
bgp = Background(lambda p: math.exp(-lamb*p), lambda p: -lamb*math.exp(-lamb*p), 0.0, Nmax=60)
rp = spectra(bgp, None, Npivot=30.0)
check('L4 power-law exact n_s', abs(rp['ns']-(1-2/(q-1))) < 1e-4, f"{rp['ns']:.6f} vs {1-2/(q-1):.6f}")
check('L4 power-law exact r = 16/q', abs(rp['r']/(16/q)-1) < 5e-3, f"{rp['r']:.5f}")
check('L4 power-law alpha_s = 0', abs(rp['alpha_s']) < 2e-5, f"{rp['alpha_s']:.1e}")
# L2: vacuum at rho with Z3-symmetric (equal) masses
from .landscape import V_tau, find_vacuum, hessian_canonical
Er = E_paper(0.5, 3**0.5/2)
Vf = lambda x, y: V_tau(x, y, Er=Er)
(xv, yv), Vv = find_vacuum(Vf, (0.47, 0.9))
check('L2 vacuum found at rho', abs(xv-0.5) < 1e-4 and abs(yv-3**0.5/2) < 1e-4 and Vv < 1e-12, f'({xv:.5f},{yv:.5f}) V={Vv:.1e}')
ev = hessian_canonical(Vf, 0.5, 3**0.5/2)
check('L2 Z3: equal masses at rho', abs(ev[0]/ev[1]-1) < 1e-3, f'{ev}')
# L3b: multifield with a decoupled second field reproduces the single-field e-folds
from .multifield import run
V2 = lambda f: 0.5*f[0]**2*(1+0*f[1]); g2 = lambda f: [f[0], 0.0]
s2, Ne2 = run(V2, g2, np.array([17.0, 0.3]), v0=np.array([-2/17.0, 0.0]))
bgq = Background(lambda p: 0.5*p*p, lambda p: p, 17.0)
check('L3b multifield = single field (decoupled)', abs(Ne2-bgq.Nend) < 2e-3, f'{Ne2:.4f} vs {bgq.Nend:.4f}')
# L6: N* matching reproduces D719 (T_R = 1e6: r 4.954e-4, V*/V_end 1.357 -> N* 47.81)
from .nstar import Nstar
check('L6 N* reproduces D719', abs(Nstar(4.954e-4, 1.357, 1e6)-47.81) < 0.02, f'{Nstar(4.954e-4,1.357,1e6):.3f}')
print(f'{len(fails)} failure(s)')
sys.exit(1 if fails else 0)
